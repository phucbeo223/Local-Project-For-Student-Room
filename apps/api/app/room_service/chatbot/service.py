from __future__ import annotations

import re
import time

from .parser import merge_filters, parse_query
from .providers import EmbeddingProvider, ResponseGenerator, GroundedTemplateGenerator
from .repo import ChatRepository
from .schemas import (
    ChatAskRequest,
    ChatAskResponse,
    ChatEvaluationContext,
    ChatHistoryMessage,
    ChatListing,
    ChatSource,
)

FOLLOW_UP_MARKERS = (
    "còn phòng nào",
    "rẻ hơn",
    "gần hơn",
    "rộng hơn",
    "phòng đầu",
    "phòng thứ",
    "trong số đó",
    "có máy lạnh không",
)


def rewrite_query(message: str, history: list[ChatHistoryMessage | dict]) -> str:
    """Resolve short follow-ups from at most five client-side turns."""
    if not history:
        return message
    normalized = message.strip().lower()
    is_follow_up = len(normalized.split()) <= 8 or any(
        marker in normalized for marker in FOLLOW_UP_MARKERS
    )
    if not is_follow_up:
        return message
    previous_users: list[str] = []
    for item in history[-10:]:
        role = item.role if isinstance(item, ChatHistoryMessage) else item.get("role")
        content = (
            item.content
            if isinstance(item, ChatHistoryMessage)
            else item.get("content")
        )
        if role == "user" and content:
            previous_users.append(str(content))
    if not previous_users:
        return message
    return f"{' . '.join(previous_users[-5:])}. Yêu cầu tiếp theo: {message}"


def _risk_level(item: dict) -> str:
    if item.get("risk_evaluated_at") is None:
        return "unknown"
    score = float(item.get("risk_score") or 0.0)
    if score < 0.3:
        return "safe"
    if score < 0.6:
        return "caution"
    return "suspicious"


def _citation_accuracy(answer: str, listings: list[dict]) -> float:
    if not listings:
        return 1.0
    citations = [int(value) for value in re.findall(r"\[(\d+)\]", answer)]
    if not citations:
        return 0.0
    valid = {int(item["rank"]) for item in listings}
    return round(sum(citation in valid for citation in citations) / len(citations), 4)


def _evaluation_context(item: dict) -> str:
    amenities = ", ".join(
        key
        for key, enabled in (item.get("parsed_amenities") or {}).items()
        if enabled is True
    )
    return " | ".join(
        str(value)
        for value in (
            item.get("title"),
            item.get("price"),
            item.get("area"),
            item.get("address") or item.get("district"),
            amenities,
            item.get("description"),
        )
        if value not in (None, "")
    )


class ChatService:
    """Stateless orchestration: parse, hybrid retrieve, rerank, answer."""

    def __init__(
        self,
        repo: ChatRepository,
        embedder: EmbeddingProvider,
        generator: ResponseGenerator,
        confidence_threshold: float = 0.65,
        max_results: int = 5,
    ):
        self.repo = repo
        self.embedder = embedder
        self.generator = generator
        self.confidence_threshold = confidence_threshold
        self.max_results = min(max_results, 5)

    def _ask_legal(
        self,
        query: str,
        body: ChatAskRequest,
        started: float,
    ) -> ChatAskResponse:
        degraded_reasons: list[str] = []
        embedded = self.embedder.embed_query(query)
        if embedded.degraded_reason:
            degraded_reasons.append(embedded.degraded_reason)
        chunks = self.repo.retrieve_legal(
            query, embedded.vector, limit=self.max_results
        )
        retrieval_mode = (
            "legal_hybrid" if embedded.vector is not None else "legal_lexical"
        )
        top_score = float(chunks[0]["similarity_score"]) if chunks else 0.0
        confidence = min(0.97, 0.22 + 0.75 * top_score) if chunks else 0.0
        # Legal BM25 scores are normalized inside the candidate corpus and should
        # not inherit the stricter listing recommendation threshold.
        if confidence < self.confidence_threshold:
            chunks = []
        generated = self.generator.generate(query, chunks, context_kind="legal")
        if not chunks or _citation_accuracy(generated.text, chunks) < 1:
            generated = GroundedTemplateGenerator().generate(
                query, chunks, context_kind="legal"
            )
            degraded_reasons.append(
                "Câu trả lời dùng mẫu theo nguồn vì chưa đủ bằng chứng hoặc trích dẫn không hợp lệ"
            )
        degraded_reasons.extend(generated.degraded_reasons)
        sources = [
            ChatSource(
                kind="legal_document",
                document_id=int(item["document_id"]),
                chunk_id=int(item["chunk_id"]),
                rank=int(item["rank"]),
                similarity_score=float(item["similarity_score"]),
                title=str(item["title"]),
                source="legal_corpus",
                source_path=item.get("source_path"),
                category=item.get("category"),
                page_from=item.get("page_from"),
                page_to=item.get("page_to"),
                heading=item.get("heading"),
            )
            for item in chunks
        ]
        contexts = (
            [
                ChatEvaluationContext(
                    kind="legal_document",
                    chunk_id=int(item["chunk_id"]),
                    rank=int(item["rank"]),
                    content=str(item["content"]),
                )
                for item in chunks
            ]
            if body.include_evaluation_contexts
            else []
        )
        response = ChatAskResponse(
            answer=generated.text,
            intent="legal_question",
            confidence=round(confidence, 4),
            listings=[],
            sources=sources,
            no_answer=not chunks,
            degraded=bool(degraded_reasons),
            degraded_reasons=degraded_reasons,
            retrieval_mode=retrieval_mode,
            generation_provider=generated.provider,
            generation_model=generated.model,
            latency_ms=max(0, int((time.perf_counter() - started) * 1000)),
            citation_accuracy=_citation_accuracy(generated.text, chunks),
            evaluation_contexts=contexts,
        )
        if hasattr(self.repo, "record_event"):
            response.event_id = self.repo.record_event(
                {
                    "intent": response.intent,
                    "confidence": response.confidence,
                    "no_answer": response.no_answer,
                    "degraded": response.degraded,
                    "retrieval_mode": response.retrieval_mode,
                    "generation_provider": response.generation_provider,
                    "result_count": len(chunks),
                    "latency_ms": response.latency_ms,
                }
            )
        return response

    def ask(self, body: ChatAskRequest) -> ChatAskResponse:
        started = time.perf_counter()
        query = rewrite_query(body.message, body.conversation_history)
        parsed = parse_query(query)
        if parsed.intent == "legal_question":
            return self._ask_legal(query, body, started)
        # Parse each turn separately so a newer budget replaces the older budget.
        # Assistant text is never treated as a source of user preferences.
        filters = parsed.filters
        if query != body.message:
            from .schemas import ChatFilters

            filters = ChatFilters()
            for turn in body.conversation_history[-10:]:
                if turn.role == "user":
                    filters = merge_filters(filters, parse_query(turn.content).filters)
            filters = merge_filters(filters, parse_query(body.message).filters)
        filters = merge_filters(filters, body.filters)

        degraded_reasons: list[str] = []
        listings: list[dict] = []
        retrieval_mode = "rule"
        if parsed.intent == "out_of_scope":
            answer = "Mình chỉ hỗ trợ tìm và so sánh nhà trọ quanh Đại học Cần Thơ."
            confidence = 0.0
            generation_provider = "rule"
            generation_model = None
        elif parsed.intent == "clarify":
            answer = "Bạn muốn tìm phòng ở khu vực nào, khoảng giá bao nhiêu và cần tiện ích gì?"
            confidence = 0.0
            generation_provider = "rule"
            generation_model = None
        else:
            embedded = self.embedder.embed_query(query)
            if embedded.degraded_reason:
                degraded_reasons.append(embedded.degraded_reason)
            listings = self.repo.retrieve(
                query, filters, embedded.vector, limit=self.max_results
            )
            retrieval_mode = (
                "hybrid" if embedded.vector is not None else "lexical_structured"
            )
            filter_count = sum(
                value not in (None, [], "phong_tro")
                for value in filters.model_dump().values()
            )
            top_score = listings[0]["similarity_score"] if listings else 0.0
            second_score = listings[1]["similarity_score"] if len(listings) > 1 else 0.0
            margin = max(0.0, top_score - second_score)
            confidence = (
                min(
                    0.97,
                    0.10
                    + 0.46 * top_score
                    + 0.24 * parsed.confidence
                    + 0.04 * min(filter_count, 3)
                    + 0.08 * min(1.0, margin * 4),
                )
                if listings
                else 0.0
            )
            if confidence < self.confidence_threshold:
                listings = []
            generated = self.generator.generate(query, listings)
            if not listings or _citation_accuracy(generated.text, listings) < 1:
                generated = GroundedTemplateGenerator().generate(query, listings)
                degraded_reasons.append(
                    "Câu trả lời dùng mẫu theo nguồn vì chưa đủ bằng chứng hoặc trích dẫn không hợp lệ"
                )
            answer = generated.text
            generation_provider = generated.provider
            generation_model = generated.model
            degraded_reasons.extend(generated.degraded_reasons)

        latency_ms = max(0, int((time.perf_counter() - started) * 1000))
        listing_models = [
            ChatListing(
                id=item["id"],
                title=item["title"],
                price=item.get("price"),
                area=item.get("area"),
                address=item.get("address"),
                district=item.get("district"),
                amenities=item.get("parsed_amenities") or {},
                distance_to_ctu=item.get("distance_to_ctu"),
                route_time_campus=item.get("route_time_campus"),
                source=item["source"],
                source_url=item.get("source_url"),
                similarity_score=item["similarity_score"],
                vector_score=float(item.get("vector_score") or 0.0),
                bm25_score=float(item.get("bm25_score") or 0.0),
                rank=item["rank"],
                match_reasons=item.get("match_reasons") or [],
                risk_score=(
                    float(item.get("risk_score") or 0.0)
                    if item.get("risk_evaluated_at") is not None
                    else None
                ),
                risk_level=_risk_level(item),
            )
            for item in listings
        ]
        sources = [
            ChatSource(
                listing_id=item.id,
                rank=item.rank,
                similarity_score=item.similarity_score,
                title=item.title,
                source=item.source,
                source_url=item.source_url,
            )
            for item in listing_models
        ]
        citation_accuracy = _citation_accuracy(answer, listings)
        contexts = (
            [
                ChatEvaluationContext(
                    listing_id=int(item["id"]),
                    rank=int(item["rank"]),
                    content=_evaluation_context(item),
                )
                for item in listings
            ]
            if body.include_evaluation_contexts
            else []
        )
        response = ChatAskResponse(
            answer=answer,
            intent=parsed.intent,
            confidence=round(confidence, 4),
            listings=listing_models,
            sources=sources,
            no_answer=not listings,
            degraded=bool(degraded_reasons),
            degraded_reasons=degraded_reasons,
            retrieval_mode=retrieval_mode,
            generation_provider=generation_provider,
            generation_model=generation_model,
            latency_ms=latency_ms,
            citation_accuracy=citation_accuracy,
            evaluation_contexts=contexts,
        )
        if hasattr(self.repo, "record_event"):
            response.event_id = self.repo.record_event(
                {
                    "intent": response.intent,
                    "confidence": response.confidence,
                    "no_answer": response.no_answer,
                    "degraded": response.degraded,
                    "retrieval_mode": response.retrieval_mode,
                    "generation_provider": response.generation_provider,
                    "result_count": len(response.listings),
                    "latency_ms": response.latency_ms,
                }
            )
        return response

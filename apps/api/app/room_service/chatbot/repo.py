from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from .providers import normalize_text
from .schemas import ChatFilters
from .legal_retrieval import expand_legal_query, legal_tokens, rerank_legal, electricity_question, rental_electricity_question
from ..legal_knowledge.quality import usable_legal_text


STOP_WORDS = {
    "anh", "ban", "can", "cho", "co", "cua", "duoc", "giup", "la",
    "minh", "nha", "phong", "tim", "toi", "tro", "va", "voi",
}


def _vector_literal(vector: list[float]) -> str:
    return "[" + ",".join(f"{value:.9g}" for value in vector) + "]"


def _tokens(value: str) -> list[str]:
    return [
        token
        for token in normalize_text(value).split()
        if len(token) > 1 and token not in STOP_WORDS
    ]


def _listing_document(item: dict[str, Any]) -> str:
    amenities = item.get("parsed_amenities") or {}
    enabled_amenities = " ".join(
        key.replace("_", " ") for key, enabled in amenities.items() if enabled is True
    )
    # Repeating title and district gives important short fields more BM25 weight.
    return " ".join(
        str(value or "")
        for value in (
            item.get("title"), item.get("title"), item.get("description"),
            item.get("address"), item.get("district"), item.get("district"),
            enabled_amenities, item.get("listing_type"),
        )
    )


def bm25_scores(
    query: str,
    documents: list[str],
    *,
    k1: float = 1.5,
    b: float = 0.75,
    tokenizer=None,
) -> list[float]:
    """BM25 from the old Hybrid project, adapted to live listing rows."""

    if not documents:
        return []
    tokenize = tokenizer or _tokens
    query_terms = Counter(tokenize(query))
    tokenized = [tokenize(document) for document in documents]
    if not query_terms or not any(tokenized):
        return [0.0] * len(documents)

    document_frequency: Counter[str] = Counter()
    for tokens in tokenized:
        document_frequency.update(set(tokens))
    average_length = sum(len(tokens) for tokens in tokenized) / len(tokenized) or 1.0
    total = len(tokenized)
    raw_scores: list[float] = []
    for tokens in tokenized:
        frequencies = Counter(tokens)
        length_norm = k1 * (1 - b + b * len(tokens) / average_length)
        score = 0.0
        for term, query_count in query_terms.items():
            frequency = frequencies.get(term, 0)
            if not frequency:
                continue
            inverse_frequency = math.log(
                1 + (total - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5)
            )
            score += query_count * inverse_frequency * (frequency * (k1 + 1)) / (
                frequency + length_norm
            )
        raw_scores.append(score)
    maximum = max(raw_scores, default=0.0)
    return [score / maximum if maximum > 0 else 0.0 for score in raw_scores]


def _preference_score(
    filters: ChatFilters, item: dict[str, Any]
) -> tuple[float, list[str]]:
    checks: list[tuple[bool, str]] = []
    price = item.get("price")
    area = item.get("area")
    distance = item.get("distance_to_ctu")
    route_times = [
        value for value in (item.get("route_time_campus") or []) if value is not None
    ]
    amenities = item.get("parsed_amenities") or {}

    if filters.min_price is not None:
        checks.append((price is not None and price >= filters.min_price, "Đúng mức giá"))
    if filters.max_price is not None:
        checks.append((price is not None and price <= filters.max_price, "Trong ngân sách"))
    if filters.min_area is not None:
        checks.append((area is not None and area >= filters.min_area, "Đủ diện tích"))
    if filters.district:
        checks.append(
            (
                filters.district.lower() in str(item.get("district") or "").lower(),
                f"Khu vực {filters.district}",
            )
        )
    if filters.max_distance_ctu is not None:
        checks.append(
            (distance is not None and distance <= filters.max_distance_ctu, "Gần CTU")
        )
    if filters.max_route_minutes is not None:
        checks.append(
            (
                bool(route_times) and min(route_times) <= filters.max_route_minutes,
                "Đúng thời gian di chuyển",
            )
        )
    for amenity in filters.amenities:
        checks.append((amenities.get(amenity) is True, "Đủ tiện ích yêu cầu"))

    if not checks:
        return 0.55, []
    matched = [reason for passed, reason in checks if passed]
    return sum(passed for passed, _ in checks) / len(checks), list(dict.fromkeys(matched))


class ChatRepository:
    """Read-only repository for stateless hybrid housing retrieval."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def retrieve(
        self,
        query: str,
        filters: ChatFilters,
        vector: list[float] | None,
        limit: int = 5,
    ) -> list[dict]:
        clauses = [
            "status = 'active'",
            "(source = 'user' OR cleaning_status = 'cleaned')",
        ]
        params: dict[str, Any] = {"candidate_limit": 250}
        if filters.listing_type:
            clauses.append("listing_type = CAST(:listing_type AS listing_type_enum)")
            params["listing_type"] = filters.listing_type
        if filters.min_price is not None:
            clauses.append("price >= :min_price")
            params["min_price"] = filters.min_price
        if filters.max_price is not None:
            clauses.append("price <= :max_price")
            params["max_price"] = filters.max_price
        if filters.min_area is not None:
            clauses.append("area >= :min_area")
            params["min_area"] = filters.min_area
        if filters.district:
            clauses.append("district ILIKE :district")
            params["district"] = f"%{filters.district}%"
        if filters.max_distance_ctu is not None:
            clauses.append("distance_to_ctu <= :max_distance")
            params["max_distance"] = filters.max_distance_ctu
        if filters.max_route_minutes is not None:
            clauses.append(
                "LEAST(COALESCE(route_time_campus[1], 1e9), "
                "COALESCE(route_time_campus[2], 1e9), COALESCE(route_time_campus[3], 1e9)) "
                "<= :max_minutes"
            )
            params["max_minutes"] = filters.max_route_minutes
        for index, amenity in enumerate(filters.amenities):
            key = f"amenity_{index}"
            clauses.append(
                f"COALESCE((parsed_amenities ->> :{key})::boolean, false) IS TRUE"
            )
            params[key] = amenity
        if filters.gender:
            clauses.append(
                "COALESCE(parsed_amenities ->> 'gender', 'any') IN ('any', :gender)"
            )
            params["gender"] = filters.gender

        if vector is not None:
            vector_sql = (
                "CASE WHEN embedding_vector IS NULL THEN 0 ELSE "
                "GREATEST(0, LEAST(1, 1 - (embedding_vector <=> CAST(:query_vector AS vector)))) END"
            )
            params["query_vector"] = _vector_literal(vector)
            order_sql = "vector_score DESC, quality_score DESC NULLS LAST"
        else:
            vector_sql = "0"
            order_sql = "quality_score DESC NULLS LAST, freshness_score DESC NULLS LAST"

        sql = text(
            "SELECT id, title, price, area, address, district, description, parsed_amenities, "
            "distance_to_ctu, route_time_campus, source, source_url, quality_score, "
            "freshness_score, risk_score, risk_evaluated_at, listing_type, "
            f"{vector_sql} AS vector_score FROM aggregated_listings "
            f"WHERE {' AND '.join(clauses)} ORDER BY {order_sql} LIMIT :candidate_limit"
        )
        with self.engine.connect() as conn:
            rows = [dict(row) for row in conn.execute(sql, params).mappings().all()]

        lexical_scores = bm25_scores(query, [_listing_document(item) for item in rows])
        for item, bm25_score in zip(rows, lexical_scores):
            vector_score = float(item.get("vector_score") or 0.0)
            quality = max(0.0, min(1.0, float(item.get("quality_score") or 0.0)))
            freshness = max(0.0, min(1.0, float(item.get("freshness_score") or 0.0)))
            # Unknown risk is neutral, never treated as safer than an evaluated listing.
            safety = (
                0.5
                if item.get("risk_evaluated_at") is None
                else 1.0 - max(0.0, min(1.0, float(item.get("risk_score") or 0.0)))
            )
            distance = item.get("distance_to_ctu")
            proximity = (
                1.0 / (1.0 + max(0.0, float(distance)) / 2000)
                if distance is not None
                else 0.25
            )
            preference, reasons = _preference_score(filters, item)

            if vector is None:
                final_score = (
                    0.45 * bm25_score
                    + 0.22 * preference
                    + 0.14 * quality
                    + 0.10 * freshness
                    + 0.06 * safety
                    + 0.03 * proximity
                )
            else:
                final_score = (
                    0.35 * vector_score
                    + 0.25 * bm25_score
                    + 0.15 * preference
                    + 0.10 * quality
                    + 0.08 * freshness
                    + 0.05 * safety
                    + 0.02 * proximity
                )
            if vector_score >= 0.6:
                reasons.insert(0, "Khớp ngữ nghĩa")
            if bm25_score >= 0.5:
                reasons.insert(0, "Khớp từ khóa")
            if quality >= 0.75:
                reasons.append("Tin chất lượng tốt")
            item["bm25_score"] = round(bm25_score, 6)
            item["similarity_score"] = round(max(0.0, min(1.0, final_score)), 6)
            item["match_reasons"] = list(dict.fromkeys(reasons))[:3]

        rows.sort(
            key=lambda item: (
                -item["similarity_score"],
                -float(item.get("quality_score") or 0.0),
                item["id"],
            )
        )
        for rank, item in enumerate(rows[:limit], 1):
            item["rank"] = rank
        return rows[:limit]

    def retrieve_legal(
        self,
        query: str,
        vector: list[float] | None,
        limit: int = 5,
    ) -> list[dict]:
        """Hybrid retrieval over OCR/indexed legal chunks.

        Missing migration/data is treated as an empty knowledge base so a rolling
        deployment never makes the existing housing chatbot unavailable.
        """
        expanded = expand_legal_query(query)
        # Independent lexical and vector pools avoid excluding a relevant law
        # merely because it was indexed earlier than 600 other chunks.
        terms = list(dict.fromkeys(term for term in re.findall(r"[^\W_]{2,}", expanded.lower()) if legal_tokens(term)))
        category = "electricity" if electricity_question(query) and "nuoc" not in normalize_text(query) else None
        params: dict[str, Any] = {"candidate_limit": 120, "tsquery": " | ".join(terms) or "empty",
                                  "category": category, "rental_query": rental_electricity_question(query)}
        if vector is not None:
            vector_sql = (
                "CASE WHEN c.embedding_vector IS NULL THEN 0 ELSE "
                "GREATEST(0, LEAST(1, 1 - (c.embedding_vector <=> CAST(:query_vector AS vector)))) END"
            )
            params["query_vector"] = _vector_literal(vector)
        else:
            vector_sql = "0"
        base_sql = (
            "SELECT c.id AS chunk_id,c.chunk_index,d.id AS document_id,d.title,d.category,d.source_path,"
            "c.page_from,c.page_to,c.heading,c.content,"
            f"{vector_sql} AS vector_score,"
            "ts_rank_cd(c.content_tsv,to_tsquery('simple',:tsquery)) AS lexical_rank "
            "FROM legal_chunks c JOIN legal_documents d ON d.id=c.document_id WHERE d.status='ready' "
            "AND (CAST(:category AS text) IS NULL OR d.category=:category) "
        )
        sql = text("WITH candidates AS (" + base_sql + "), lexical AS ("
                   "SELECT * FROM candidates WHERE lexical_rank > 0 ORDER BY lexical_rank DESC,chunk_id LIMIT :candidate_limit), "
                   "phrases AS (SELECT * FROM candidates WHERE :rental_query AND (content ILIKE '%thu tiền điện%' "
                   "OR content ILIKE '%người thuê nhà%' OR content ILIKE '%định mức%') "
                   "ORDER BY lexical_rank DESC,chunk_id LIMIT :candidate_limit) "
                   + (", semantic AS (SELECT * FROM candidates ORDER BY vector_score DESC,chunk_id LIMIT :candidate_limit) "
                      "SELECT * FROM lexical UNION SELECT * FROM semantic UNION SELECT * FROM phrases" if vector is not None
                      else "SELECT * FROM lexical UNION SELECT * FROM phrases"))
        try:
            with self.engine.connect() as conn:
                rows = [dict(row) for row in conn.execute(sql, params).mappings().all()]
        except SQLAlchemyError:
            return []

        documents = [
            " ".join(
                str(value or "")
                for value in (item.get("title"), item.get("heading"), item.get("content"))
            )
            for item in rows
        ]
        lexical_scores = bm25_scores(expanded, documents, tokenizer=legal_tokens)
        for item, bm25_score in zip(rows, lexical_scores):
            vector_score = float(item.get("vector_score") or 0.0)
            item["bm25_score"] = round(bm25_score, 6)
            item["similarity_score"] = round(
                max(
                    0.0,
                    min(
                        1.0,
                        0.55 * vector_score + 0.45 * bm25_score
                        if vector is not None
                        else bm25_score,
                    ),
                ),
                6,
            )
        # With lexical-only retrieval, zero-score rows are arbitrary and unsafe to cite.
        if vector is None:
            rows = [item for item in rows if item["bm25_score"] > 0]
        else:
            rows = [
                item
                for item in rows
                if item["bm25_score"] > 0 or float(item.get("vector_score") or 0) >= 0.35
            ]
        rows = rerank_legal(query, rows, limit=30)
        selected = []
        seen: set[tuple] = set()
        # Keep complete clauses and associated effectiveness/transition provisions.
        with self.engine.connect() as conn:
            for item in rows:
                group = (item["document_id"], item.get("heading") or item["chunk_id"])
                if group in seen:
                    continue
                seen.add(group)
                item = dict(item)
                if item.get("heading"):
                    siblings = [dict(row) for row in conn.execute(text(
                        "SELECT id AS chunk_id,chunk_index,content,page_from,page_to FROM legal_chunks "
                        "WHERE document_id=:doc AND heading=:heading ORDER BY chunk_index"
                    ), {"doc": item["document_id"], "heading": item["heading"]}).mappings()]
                    # Nearest continuation first; never drop the matching chunk.
                    siblings.sort(key=lambda row: abs(row["chunk_index"] - item["chunk_index"]))
                    included = []
                    size = 0
                    for sibling in siblings:
                        if not usable_legal_text(sibling["content"]) or size + len(sibling["content"]) > 5500:
                            continue
                        included.append(sibling)
                        size += len(sibling["content"])
                    if included:
                        included.sort(key=lambda row: row["chunk_index"])
                        item["content"] = "\n\n".join(row["content"] for row in included)
                        item["page_from"] = min((row["page_from"] for row in included if row["page_from"] is not None), default=None)
                        item["page_to"] = max((row["page_to"] for row in included if row["page_to"] is not None), default=None)
                selected.append(item)
                core_limit = min(2, max(1, limit - 1)) if rental_electricity_question(query) else max(1, limit - 2)
                if len(selected) >= core_limit:
                    break
            doc_ids = list(dict.fromkeys(item["document_id"] for item in selected))
            if doc_ids and len(selected) < limit:
                effect_rows = [dict(row) for row in conn.execute(text(
                    "SELECT c.id AS chunk_id,c.chunk_index,d.id AS document_id,d.title,d.category,d.source_path,"
                    "c.page_from,c.page_to,c.heading,c.content FROM legal_chunks c "
                    "JOIN legal_documents d ON d.id=c.document_id WHERE d.id=ANY(:ids) "
                    "AND (c.heading ILIKE '%Hiệu lực%' OR c.heading ILIKE '%chuyển tiếp%' "
                    "OR c.heading ILIKE '%hình thức xử phạt%') "
                    "ORDER BY d.id,c.chunk_index"
                ), {"ids": doc_ids}).mappings()]
                for doc_id in doc_ids:
                    effects = [row for row in effect_rows if row["document_id"] == doc_id
                               and usable_legal_text(row["content"])
                               and row["chunk_id"] not in {part["chunk_id"] for part in selected}]
                    # Effectiveness first (contains delayed commencement), then
                    # transition clauses. Each document gets its own citation.
                    effects.sort(key=lambda row: ("hiệu lực" not in (row["heading"] or "").lower(), row["chunk_index"]))
                    included = []
                    size = 0
                    for row in effects:
                        # Commencement conditions are essential; mailing lists,
                        # repeal inventories and annex tables are not context.
                        normalized_content = normalize_text(row["content"])
                        if len(row["content"]) < 80 or "noi nhan:" in normalized_content:
                            continue
                        if "bai bo" in normalized_content or "cac quy dinh sau het hieu luc" in normalized_content:
                            continue
                        if size + len(row["content"]) <= 2400:
                            included.append(row)
                            size += len(row["content"])
                    if included:
                        item = dict(included[0])
                        item["content"] = "\n\n".join((row["heading"] or "") + "\n" + row["content"] for row in included)
                        item["heading"] = "Hiệu lực, phạm vi mức phạt và điều khoản chuyển tiếp"
                        item["page_from"] = min((row["page_from"] for row in included if row["page_from"] is not None), default=None)
                        item["page_to"] = max((row["page_to"] for row in included if row["page_to"] is not None), default=None)
                        item["similarity_score"] = selected[0]["similarity_score"]
                        selected.append(item)
                    if len(selected) >= limit:
                        break
        for rank, item in enumerate(selected, 1):
            item["rank"] = rank
        return selected

    def record_event(self, payload: dict[str, Any]) -> int | None:
        """Store aggregate research telemetry; never stores the user's message."""
        try:
            with self.engine.begin() as conn:
                return int(
                    conn.execute(
                        text(
                            "INSERT INTO chatbot_events "
                            "(intent, confidence, no_answer, degraded, retrieval_mode, "
                            "generation_provider, result_count, latency_ms) "
                            "VALUES (:intent, :confidence, :no_answer, :degraded, :retrieval_mode, "
                            ":generation_provider, :result_count, :latency_ms) RETURNING id"
                        ),
                        payload,
                    ).scalar_one()
                )
        except Exception:
            # Telemetry is optional during rolling migration and must not break chat.
            return None

    def add_feedback(self, payload: dict[str, Any]) -> int:
        with self.engine.begin() as conn:
            return int(
                conn.execute(
                    text(
                        "INSERT INTO chatbot_feedback (event_id, rating, reason, comment) "
                        "VALUES (:event_id, :rating, :reason, :comment) RETURNING id"
                    ),
                    payload,
                ).scalar_one()
            )

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.engine import Engine

from ...config import settings
from ...auth import get_current_user
from ...auth.schemas import UserOut
from ...auth.lifecycle import rate_limit
from sqlalchemy import text
from .providers import (
    E5EmbeddingProvider,
    FallbackResponseGenerator,
    GeminiGenerator,
    GroundedTemplateGenerator,
    OllamaQwenGenerator,
)
from .repo import ChatRepository
from .schemas import (
    ChatAskRequest,
    ChatAskResponse,
    ChatFeedbackCreate,
    ChatFeedbackOut,
)
from .service import ChatService

router = APIRouter(prefix="/chat", tags=["chatbot"])
_service: ChatService | None = None


def init_chatbot(engine: Engine) -> None:
    global _service
    providers = []
    degraded_reasons: list[str] = []

    if settings.chatbot_llm_provider in ("auto", "qwen"):
        providers.append(
            OllamaQwenGenerator(
                settings.ollama_base_url,
                settings.ollama_model,
                settings.chatbot_llm_timeout_seconds,
                context_length=settings.ollama_context_length,
                max_output_tokens=settings.chatbot_max_output_tokens,
                keep_alive=settings.ollama_keep_alive,
                legal_timeout_seconds=settings.chatbot_legal_timeout_seconds,
            )
        )

    if settings.chatbot_llm_provider in ("auto", "gemini"):
        if settings.gemini_api_key:
            providers.append(
                GeminiGenerator(
                    settings.gemini_api_key,
                    settings.gemini_model,
                    settings.gemini_base_url,
                    settings.chatbot_llm_timeout_seconds,
                    max_output_tokens=settings.chatbot_max_output_tokens,
                )
            )
        elif settings.chatbot_llm_provider == "gemini":
            degraded_reasons.append(
                "Gemini được chọn nhưng GEMINI_API_KEY chưa cấu hình"
            )

    _service = ChatService(
        ChatRepository(engine),
        E5EmbeddingProvider(settings.chatbot_embedding_model),
        FallbackResponseGenerator(
            providers,
            GroundedTemplateGenerator(),
            initial_degraded_reasons=degraded_reasons,
        ),
        confidence_threshold=settings.chatbot_confidence_threshold,
        max_results=settings.chatbot_max_results,
    )


def get_service() -> ChatService:
    if _service is None:
        raise HTTPException(503, "Chatbot chưa khởi tạo")
    return _service


def warmup_chatbot() -> None:
    service = get_service()
    for provider in service.generator.providers:
        if isinstance(provider, OllamaQwenGenerator):
            try:
                provider.warmup(settings.chatbot_warmup_timeout_seconds)
            except Exception:
                logging.getLogger(__name__).warning("Chat model warmup unavailable")
    try:
        service.embedder.warmup()
    except Exception:
        logging.getLogger(__name__).info("Embedding warmup skipped; model not available locally")


def close_chatbot() -> None:
    if _service:
        for provider in _service.generator.providers:
            if hasattr(provider, "close"):
                provider.close()


@router.post("/ask", response_model=ChatAskResponse)
def ask_chatbot(
    body: ChatAskRequest,
    user: UserOut = Depends(get_current_user),
    service: ChatService = Depends(get_service),
):
    rate_limit(service.repo.engine, f"chat:{user.id}", 12)
    if body.include_evaluation_contexts and user.role != "admin":
        raise HTTPException(403, "Chỉ admin được lấy dữ liệu đánh giá")
    result = service.ask(body)
    if result.event_id:
        with service.repo.engine.begin() as conn:
            conn.execute(
                text("UPDATE chatbot_events SET user_id=:uid WHERE id=:id"),
                {"uid": user.id, "id": result.event_id},
            )
    return result


@router.post("/feedback", response_model=ChatFeedbackOut, status_code=201)
def submit_chat_feedback(
    body: ChatFeedbackCreate, user: UserOut = Depends(get_current_user)
):
    """Anonymous-safe feedback: no message content and no client-supplied user id."""
    if _service is None:
        raise HTTPException(503, "Chatbot chưa khởi tạo")
    rate_limit(_service.repo.engine, f"chat-feedback:{user.id}", 30)
    with _service.repo.engine.connect() as conn:
        owned = conn.execute(
            text("SELECT 1 FROM chatbot_events WHERE id=:id AND user_id=:uid"),
            {"id": body.event_id, "uid": user.id},
        ).first()
    if not owned:
        raise HTTPException(404, "Không tìm thấy lượt chat của bạn")
    feedback_id = _service.repo.add_feedback(body.model_dump())
    return ChatFeedbackOut(id=feedback_id)

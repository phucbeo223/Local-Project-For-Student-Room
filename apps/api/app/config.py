from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    database_url: str = "postgresql+psycopg://nckh:nckh@db:5432/nckh"
    redis_url: str = "redis://redis:6379/0"

    # bật scheduler crawler trong app (tắt mặc định: dev/test không tự crawl ra mạng)
    crawler_enabled: bool = False

    # auth (Sprint 1.9). Secret THẬT đặt trong .env, KHÔNG commit.
    jwt_secret: str = "dev-insecure-change-me"
    jwt_algorithm: str = "HS256"
    access_token_ttl_min: int = 15
    refresh_token_ttl_days: int = 7
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = True
    smtp_from: str = "no-reply@localhost"
    web_public_url: str = "http://localhost:3000"
    google_client_id: str = ""  # bắt buộc khi dùng Google login

    ors_api_key: str = ""  # OpenRouteService — route time/geometry; rỗng = tắt routing

    # Room-service AI. `auto`: Qwen local -> Gemini nếu có khóa -> template grounded.
    chatbot_embedding_model: str = "intfloat/multilingual-e5-small"
    chatbot_confidence_threshold: float = 0.65
    chatbot_max_results: int = 5
    chatbot_llm_provider: Literal["auto", "qwen", "gemini", "template"] = "auto"
    chatbot_llm_timeout_seconds: float = 4.0
    chatbot_legal_timeout_seconds: float = Field(default=120.0, gt=0, le=300)
    chatbot_max_output_tokens: int = Field(default=384, ge=128, le=4096)
    chatbot_warmup_enabled: bool = True
    chatbot_warmup_timeout_seconds: float = Field(default=30, gt=0, le=120)
    listing_stats_cache_seconds: int = Field(default=30, ge=0, le=300)

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    ollama_context_length: int = 8192
    ollama_keep_alive: str = "30m"

    # Không ghi khóa thật vào source; chỉ đặt GEMINI_API_KEY trong .env/runtime.
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.7-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"

    risk_auto_assess: bool = True
    risk_auto_assess_limit: int = 1000


settings = Settings()

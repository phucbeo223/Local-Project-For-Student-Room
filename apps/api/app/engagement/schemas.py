from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator

from ..listings.schemas import ListingOut


class InteractionType(str, Enum):
    view = "view"
    bookmark = "bookmark"
    click_source = "click_source"
    click_phone = "click_phone"
    dismiss = "dismiss"


class InteractionCreate(BaseModel):
    listing_id: int = Field(gt=0)
    type: InteractionType
    duration_ms: int | None = Field(default=None, ge=0, le=86_400_000)


class InteractionOut(InteractionCreate):
    id: int
    created_at: datetime


class FavoriteOut(BaseModel):
    listing: ListingOut
    created_at: datetime


class SavedSearchCriteria(BaseModel):
    q: str | None = Field(default=None, max_length=200)
    min_price: int | None = Field(default=None, ge=0)
    max_price: int | None = Field(default=None, ge=0)
    min_area: float | None = Field(default=None, ge=0)
    district: str | None = Field(default=None, max_length=80)
    amenities: list[str] = Field(default_factory=list, max_length=20)
    max_distance_ctu: float | None = Field(default=None, ge=0, le=100_000)

    @model_validator(mode="after")
    def validate_prices(self):
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("min_price không được lớn hơn max_price")
        return self


class SavedSearchCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    criteria: SavedSearchCriteria
    notify_enabled: bool = True


class SavedSearchOut(SavedSearchCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    last_notified_at: datetime | None = None


class RecommendationItem(BaseModel):
    listing: ListingOut
    score: float = Field(ge=0, le=1)
    reasons: list[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    cold_start: bool
    profile_evidence: int
    items: list[RecommendationItem]


class AIDashboardSummary(BaseModel):
    period_days: int
    chatbot_requests: int
    no_answer_rate: float
    degraded_rate: float
    average_confidence: float
    p95_latency_ms: float
    positive_feedback_rate: float | None = None
    feedback_count: int
    interaction_count: int
    favorite_count: int
    saved_search_count: int
    risk_not_evaluated: int
    risk_safe: int
    risk_caution: int
    risk_suspicious: int
    risk_override_count: int
    latest_evaluation: dict[str, Any] | None = None


class EvaluationRunCreate(BaseModel):
    dataset_version: str = Field(min_length=1, max_length=100)
    model_version: str | None = Field(default=None, max_length=120)
    prompt_version: str | None = Field(default=None, max_length=120)
    metrics: dict[str, float | int | bool]
    passed: bool


class NotificationOut(BaseModel):
    id: int
    search_id: int | None = None
    listing_id: int | None = None
    listing_title: str | None = None
    message: str
    read_at: datetime | None = None
    created_at: datetime


class NotificationRefreshOut(BaseModel):
    created: int
    items: list[NotificationOut]

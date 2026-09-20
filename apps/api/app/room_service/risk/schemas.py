from datetime import datetime

from pydantic import BaseModel, Field


class RiskSignal(BaseModel):
    code: str
    message: str
    weight: float = Field(ge=0, le=1)


class RiskAssessment(BaseModel):
    listing_id: int
    risk_score: float = Field(ge=0, le=1)
    risk_level: str
    risk_reasons: list[str] = Field(default_factory=list)
    signals: list[RiskSignal] = Field(default_factory=list)
    model_version: str
    evaluated_at: datetime
    persisted: bool = False
    evaluation_status: str = "evaluated"
    statistical_status: str = "not_run"


class RiskHistoryItem(BaseModel):
    id: int
    listing_id: int
    risk_score: float
    risk_level: str
    risk_reasons: list[str] = Field(default_factory=list)
    model_version: str
    evaluation_type: str
    overridden_by: int | None = None
    override_note: str | None = None
    created_at: datetime


class RiskOverrideIn(BaseModel):
    risk_score: float = Field(ge=0.01, le=0.95)
    note: str = Field(min_length=5, max_length=1000)


class RiskBatchResponse(BaseModel):
    processed: int
    safe: int
    caution: int
    suspicious: int
    failed_listing_ids: list[int] = Field(default_factory=list)

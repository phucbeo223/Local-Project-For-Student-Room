from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class SortBy(str, Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    newest = "newest"
    nearest = "nearest"
    freshness = "freshness"
    quality = "quality"


def risk_level(score: float | None) -> str:
    """risk_score → nhãn badge (FR-7.2). ✅ safe / ⚠️ caution / 🔴 suspicious."""
    # ponytail: risk engine chưa build (team làm sau) → score=0 mặc định = CHƯA đánh giá,
    # không phải "an toàn". Bỏ guard này khi risk detection ghi score thật.
    if not score:
        return "unknown"
    if score < 0.3:
        return "safe"
    if score < 0.6:
        return "caution"
    return "suspicious"


def freshness_label(last_seen: datetime | None, now: datetime | None = None) -> str:
    """last_seen → 'cập nhật X giờ/ngày trước' (FR-2.8)."""
    if last_seen is None:
        return "không rõ"
    from datetime import timezone

    now = now or datetime.now(timezone.utc)
    if last_seen.tzinfo is None:
        last_seen = last_seen.replace(tzinfo=timezone.utc)
    secs = max(0, (now - last_seen).total_seconds())
    if secs < 3600:
        return f"cập nhật {int(secs // 60)} phút trước"
    if secs < 86400:
        return f"cập nhật {int(secs // 3600)} giờ trước"
    return f"cập nhật {int(secs // 86400)} ngày trước"


class SearchParams(BaseModel):
    q: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    min_area: float | None = None
    max_area: float | None = None
    ward: str | None = None
    district: str | None = None
    amenities: list[str] = Field(default_factory=list)
    max_distance_ctu: float | None = None  # mét
    sort: SortBy = SortBy.newest
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class ListingOut(BaseModel):
    id: int
    title: str
    price: int | None = None
    area: float | None = None
    address: str | None = None
    district: str | None = None
    ward: str | None = None
    parsed_amenities: dict[str, bool] = Field(default_factory=dict)
    lat: float | None = None
    lng: float | None = None
    distance_to_ctu: float | None = None
    description: str | None = None
    images: list[str] = Field(default_factory=list)
    source: str
    source_url: str | None = None
    posted_by: int | None = None
    risk_score: float | None = None
    risk_reasons: list[str] = Field(default_factory=list)
    risk_level: str = "unknown"
    risk_status: str = "not_evaluated"
    geocode_confidence: str | None = None
    freshness_score: float | None = None
    freshness_label: str = ""
    quality_score: float | None = None
    last_seen: datetime | None = None
    route_time_campus: list[float] | None = (
        None  # [khuI, khuII, khuIII] phút, None = chưa route
    )
    report_count: int = 0


class SearchResult(BaseModel):
    total: int
    page: int
    size: int
    items: list[ListingOut]


class ListingCreate(BaseModel):
    """Payload đăng tin UGC (FR-3.1)."""

    title: str = Field(min_length=5, max_length=200)
    price: int | None = Field(default=None, ge=0, le=100_000_000)
    area: float | None = Field(default=None, gt=0, le=10_000)
    address: str | None = Field(default=None, max_length=500)
    district: str | None = Field(default=None, max_length=80)
    description: str | None = Field(default=None, max_length=10_000)
    images: list[str] = Field(default_factory=list, max_length=20)


class ListingUpdate(BaseModel):
    """Payload sửa tin UGC — mọi field optional (partial update)."""

    title: str | None = Field(default=None, min_length=5, max_length=200)
    price: int | None = Field(default=None, ge=0, le=100_000_000)
    area: float | None = Field(default=None, gt=0, le=10_000)
    address: str | None = Field(default=None, max_length=500)
    district: str | None = Field(default=None, max_length=80)
    description: str | None = Field(default=None, max_length=10_000)
    images: list[str] | None = Field(default=None, max_length=20)

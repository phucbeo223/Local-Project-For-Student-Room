from __future__ import annotations

from collections import Counter
from statistics import mean

from fastapi import HTTPException

from ..listings.repo import ListingQueryRepo
from .repo import EngagementRepository
from .schemas import (
    AIDashboardSummary,
    FavoriteOut,
    InteractionCreate,
    InteractionOut,
    RecommendationItem,
    RecommendationResponse,
    NotificationOut,
    NotificationRefreshOut,
    SavedSearchCreate,
    SavedSearchOut,
)


INTERACTION_WEIGHTS = {
    "view": 1.0,
    "click_source": 2.0,
    "click_phone": 3.0,
    "bookmark": 4.0,
    "dismiss": -2.0,
}


class EngagementService:
    def __init__(self, repo: EngagementRepository, listings: ListingQueryRepo):
        self.repo = repo
        self.listings = listings

    def interaction(self, user_id: int, body: InteractionCreate) -> InteractionOut:
        if not self.repo.listing_exists(body.listing_id):
            raise HTTPException(404, "Không tìm thấy tin")
        row = self.repo.add_interaction(user_id, body.listing_id, body.type.value, body.duration_ms)
        return InteractionOut(**row)

    def favorite(self, user_id: int, listing_id: int) -> FavoriteOut:
        listing = self.listings.get_visible(listing_id)
        if listing is None:
            raise HTTPException(404, "Không tìm thấy tin")
        row = self.repo.add_favorite(user_id, listing_id)
        return FavoriteOut(listing=listing, created_at=row["created_at"])

    def unfavorite(self, user_id: int, listing_id: int) -> None:
        if not self.repo.remove_favorite(user_id, listing_id):
            raise HTTPException(404, "Tin chưa nằm trong danh sách yêu thích")

    def favorites(self, user_id: int) -> list[FavoriteOut]:
        output: list[FavoriteOut] = []
        for row in self.repo.favorite_rows(user_id):
            listing = self.listings.get_visible(row["listing_id"])
            if listing is not None:
                output.append(FavoriteOut(listing=listing, created_at=row["created_at"]))
        return output

    def create_saved_search(self, user_id: int, body: SavedSearchCreate) -> SavedSearchOut:
        import json

        row = self.repo.create_saved_search(
            user_id,
            {
                "name": body.name,
                "criteria": json.dumps(body.criteria.model_dump(), ensure_ascii=False),
                "notify_enabled": body.notify_enabled,
            },
        )
        return SavedSearchOut(**row)

    def saved_searches(self, user_id: int) -> list[SavedSearchOut]:
        return [SavedSearchOut(**row) for row in self.repo.saved_searches(user_id)]

    def delete_saved_search(self, user_id: int, search_id: int) -> None:
        if not self.repo.delete_saved_search(user_id, search_id):
            raise HTTPException(404, "Không tìm thấy bộ lọc đã lưu")

    def recommendations(self, user_id: int, limit: int) -> RecommendationResponse:
        history = self.repo.interaction_history(user_id)
        candidates = self.repo.recommendation_candidates()
        positive = [row for row in history if INTERACTION_WEIGHTS.get(row["type"], 0) > 0]
        dismissed_ids = {int(row["id"]) for row in history if row["type"] == "dismiss"}
        cold_start = len(positive) < 3

        weighted_prices = [
            (float(row["price"]), INTERACTION_WEIGHTS.get(row["type"], 1.0))
            for row in positive
            if row.get("price")
        ]
        preferred_price = (
            sum(price * weight for price, weight in weighted_prices)
            / sum(weight for _, weight in weighted_prices)
            if weighted_prices
            else None
        )
        districts: Counter[str] = Counter()
        amenities: Counter[str] = Counter()
        for row in positive:
            weight = INTERACTION_WEIGHTS.get(row["type"], 1.0)
            if row.get("district"):
                districts[row["district"]] += weight
            for key, enabled in (row.get("parsed_amenities") or {}).items():
                if enabled is True:
                    amenities[key] += weight
        preferred_district = districts.most_common(1)[0][0] if districts else None
        preferred_amenities = {key for key, _ in amenities.most_common(4)}

        scored: list[tuple[float, int, list[str]]] = []
        for row in candidates:
            listing_id = int(row["id"])
            if listing_id in dismissed_ids:
                continue
            quality = max(0.0, min(1.0, float(row.get("quality_score") or 0.0)))
            freshness = max(0.0, min(1.0, float(row.get("freshness_score") or 0.0)))
            safety = (
                0.5
                if row.get("risk_evaluated_at") is None
                else 1.0 - max(0.0, min(1.0, float(row.get("risk_score") or 0.0)))
            )
            reasons: list[str] = []
            preference = 0.5
            if not cold_start:
                pieces: list[float] = []
                if preferred_price and row.get("price"):
                    ratio = abs(float(row["price"]) - preferred_price) / max(preferred_price, 1)
                    price_match = max(0.0, 1.0 - ratio)
                    pieces.append(price_match)
                    if price_match >= 0.75:
                        reasons.append("Gần mức giá bạn quan tâm")
                if preferred_district:
                    district_match = 1.0 if row.get("district") == preferred_district else 0.0
                    pieces.append(district_match)
                    if district_match:
                        reasons.append(f"Đúng khu vực {preferred_district}")
                if preferred_amenities:
                    enabled = {
                        key for key, value in (row.get("parsed_amenities") or {}).items() if value is True
                    }
                    amenity_match = len(enabled & preferred_amenities) / len(preferred_amenities)
                    pieces.append(amenity_match)
                    if amenity_match >= 0.5:
                        reasons.append("Có tiện ích bạn thường xem")
                preference = mean(pieces) if pieces else 0.5
            else:
                reasons.append("Tin mới, chất lượng tốt")

            score = 0.42 * preference + 0.25 * quality + 0.18 * freshness + 0.15 * safety
            if safety < 0.4:
                score *= 0.6
            if quality >= 0.75:
                reasons.append("Thông tin đầy đủ")
            if safety >= 0.7:
                reasons.append("Rủi ro thấp")
            scored.append((max(0.0, min(1.0, score)), listing_id, list(dict.fromkeys(reasons))[:3]))

        scored.sort(key=lambda item: (-item[0], item[1]))
        items: list[RecommendationItem] = []
        for score, listing_id, reasons in scored:
            listing = self.listings.get_visible(listing_id)
            if listing is not None:
                items.append(
                    RecommendationItem(listing=listing, score=round(score, 4), reasons=reasons)
                )
            if len(items) >= limit:
                break
        return RecommendationResponse(
            cold_start=cold_start,
            profile_evidence=len(positive),
            items=items,
        )

    def dashboard(self, days: int) -> AIDashboardSummary:
        data = self.repo.dashboard(days)
        chat = data["chat"]
        feedback = data["feedback"]
        product = data["product"]
        risk = data["risk"]
        return AIDashboardSummary(
            period_days=days,
            chatbot_requests=int(chat["requests"]),
            no_answer_rate=round(float(chat["no_answer_rate"]), 4),
            degraded_rate=round(float(chat["degraded_rate"]), 4),
            average_confidence=round(float(chat["avg_confidence"]), 4),
            p95_latency_ms=round(float(chat["p95_latency"]), 2),
            positive_feedback_rate=(
                round(float(feedback["positive_rate"]), 4)
                if feedback["positive_rate"] is not None
                else None
            ),
            feedback_count=int(feedback["count"]),
            interaction_count=int(product["interactions"]),
            favorite_count=int(product["favorites"]),
            saved_search_count=int(product["saved_searches"]),
            risk_not_evaluated=int(risk["not_evaluated"]),
            risk_safe=int(risk["safe"]),
            risk_caution=int(risk["caution"]),
            risk_suspicious=int(risk["suspicious"]),
            risk_override_count=data["overrides"],
            latest_evaluation=data["latest_evaluation"],
        )

    def notifications(self, user_id: int) -> list[NotificationOut]:
        return [NotificationOut(**row) for row in self.repo.notifications(user_id)]

    def mark_notification_read(self, user_id: int, notification_id: int) -> NotificationOut:
        row = self.repo.mark_notification_read(user_id, notification_id)
        if row is None:
            raise HTTPException(404, "Không tìm thấy thông báo")
        return NotificationOut(**row)

    def refresh_notifications(self, user_id: int) -> NotificationRefreshOut:
        created = self.repo.refresh_notifications(user_id)
        return NotificationRefreshOut(created=created, items=self.notifications(user_id))

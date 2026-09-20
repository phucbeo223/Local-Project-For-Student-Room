from __future__ import annotations

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


class EngagementService:
    def __init__(self, repo: EngagementRepository, listings: ListingQueryRepo):
        self.repo = repo
        self.listings = listings

    def interaction(self, user_id: int, body: InteractionCreate) -> InteractionOut:
        if not self.repo.listing_exists(body.listing_id):
            raise HTTPException(404, "Không tìm thấy tin")
        row = self.repo.add_interaction(
            user_id, body.listing_id, body.type.value, body.duration_ms
        )
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
                output.append(
                    FavoriteOut(listing=listing, created_at=row["created_at"])
                )
        return output

    def create_saved_search(
        self, user_id: int, body: SavedSearchCreate
    ) -> SavedSearchOut:
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
        from .recommender import rank

        history = self.repo.interaction_history(user_id)
        preferences = self.repo.preferences(user_id)
        profile, ranked = rank(
            self.repo.recommendation_candidates(), history, preferences, limit
        )
        self.repo.save_vector(user_id, profile)
        items = []
        for score, row, explore in ranked:
            listing = self.listings.get_visible(row["id"])
            if listing:
                reason = (
                    "Khám phá trong tiêu chí của bạn"
                    if explore
                    else (
                        "Tương đồng với hồ sơ và tương tác của bạn"
                        if profile
                        else "Được nhiều người quan tâm trong 30 ngày"
                    )
                )
                items.append(
                    RecommendationItem(
                        listing=listing,
                        score=round(
                            max(0, min(1, score if profile else score / (score + 1))), 4
                        ),
                        reasons=[reason],
                    )
                )
        return RecommendationResponse(
            cold_start=profile is None, profile_evidence=len(history), items=items
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

    def mark_notification_read(
        self, user_id: int, notification_id: int
    ) -> NotificationOut:
        row = self.repo.mark_notification_read(user_id, notification_id)
        if row is None:
            raise HTTPException(404, "Không tìm thấy thông báo")
        return NotificationOut(**row)

    def refresh_notifications(self, user_id: int) -> NotificationRefreshOut:
        created = self.repo.refresh_notifications(user_id)
        return NotificationRefreshOut(
            created=created, items=self.notifications(user_id)
        )

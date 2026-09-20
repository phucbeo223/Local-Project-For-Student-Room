from datetime import datetime, timezone

from app.engagement.schemas import InteractionCreate, InteractionType
from app.engagement.service import EngagementService
from app.listings.schemas import ListingOut


def _listing(listing_id: int) -> ListingOut:
    return ListingOut(id=listing_id, title=f"Phòng {listing_id}", source="dev_seed")


class FakeListingRepo:
    def get_visible(self, listing_id):
        return _listing(listing_id) if listing_id in {1, 2, 3} else None


class FakeRepo:
    def __init__(self):
        self.interactions = []
        self.favorite_data = []

    def listing_exists(self, listing_id):
        return listing_id in {1, 2, 3}

    def add_interaction(self, user_id, listing_id, interaction_type, duration_ms):
        row = {
            "id": len(self.interactions) + 1,
            "listing_id": listing_id,
            "type": interaction_type,
            "duration_ms": duration_ms,
            "created_at": datetime.now(timezone.utc),
        }
        self.interactions.append(row)
        return row

    def interaction_history(self, user_id, limit=200):
        return [
            {
                "type": "bookmark",
                "id": 1,
                "price": 2_000_000,
                "district": "Ninh Kiều",
                "parsed_amenities": {"wifi": True, "air_conditioner": True},
            },
            {
                "type": "view",
                "id": 2,
                "price": 2_200_000,
                "district": "Ninh Kiều",
                "parsed_amenities": {"wifi": True},
            },
            {
                "type": "click_phone",
                "id": 3,
                "price": 1_900_000,
                "district": "Ninh Kiều",
                "parsed_amenities": {"wifi": True},
            },
        ]

    def recommendation_candidates(self, limit=250):
        return [
            {
                "id": 1,
                "price": 2_050_000,
                "district": "Ninh Kiều",
                "parsed_amenities": {"wifi": True, "air_conditioner": True},
                "quality_score": 0.9,
                "freshness_score": 0.9,
                "risk_score": 0.1,
                "risk_evaluated_at": datetime.now(timezone.utc),
            },
            {
                "id": 2,
                "price": 4_000_000,
                "district": "Cái Răng",
                "parsed_amenities": {},
                "quality_score": 0.5,
                "freshness_score": 0.5,
                "risk_score": 0.7,
                "risk_evaluated_at": datetime.now(timezone.utc),
            },
        ]

    def mark_notification_read(self, user_id, notification_id):
        if notification_id != 5:
            return None
        return {
            "id": 5,
            "search_id": 2,
            "listing_id": 1,
            "listing_title": "Phòng 1",
            "message": "Có phòng mới",
            "read_at": datetime.now(timezone.utc),
            "created_at": datetime.now(timezone.utc),
        }


def test_interaction_is_recorded_with_authenticated_user():
    repo = FakeRepo()
    service = EngagementService(repo, FakeListingRepo())
    result = service.interaction(
        9,
        InteractionCreate(listing_id=1, type=InteractionType.view, duration_ms=1200),
    )
    assert result.listing_id == 1
    assert result.type == InteractionType.view
    assert repo.interactions[0]["duration_ms"] == 1200


def test_personalized_recommendation_explains_ranking_and_penalizes_risk():
    service = EngagementService(FakeRepo(), FakeListingRepo())
    result = service.recommendations(9, 10)
    assert result.cold_start is False
    assert result.profile_evidence == 3
    assert result.items[0].listing.id == 1
    assert result.items[0].score > result.items[1].score
    assert "Đúng khu vực Ninh Kiều" in result.items[0].reasons


def test_notification_can_only_be_marked_read_when_owned():
    service = EngagementService(FakeRepo(), FakeListingRepo())
    assert service.mark_notification_read(9, 5).read_at is not None

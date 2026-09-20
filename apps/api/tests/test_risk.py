from datetime import datetime, timezone

import pytest
from fastapi import HTTPException

from app.room_service.risk.scoring import MODEL_VERSION, score_listing
from app.room_service.risk.service import RiskService


def _listing(**overrides):
    value = {
        "id": 12,
        "title": "Phòng trọ sinh viên gần Đại học Cần Thơ",
        "description": "Phòng sạch sẽ, có gác, cho xem phòng trực tiếp và ký hợp đồng rõ ràng.",
        "price": 2_000_000,
        "area": 20,
        "address": "Đường 3/2, Xuân Khánh",
        "district": "Ninh Kiều",
        "images": ["https://example.com/room.jpg"],
        "source": "user",
        "source_url": None,
        "listing_type": "phong_tro",
        "quality_score": 0.9,
        "freshness_score": 0.9,
        "geocode_confidence": "high",
    }
    value.update(overrides)
    return value


def test_safe_listing_has_evaluated_floor_instead_of_unknown_zero():
    now = datetime(2026, 8, 31, tzinfo=timezone.utc)

    result = score_listing(_listing(), district_median_price=2_100_000, now=now)

    assert result.score == 0.01
    assert result.level == "safe"
    assert result.reasons == []
    assert result.evaluated_at == now


def test_scam_language_and_no_inspection_are_suspicious():
    result = score_listing(
        _listing(
            title="Giá sốc, chốt ngay hôm nay",
            description="Đặt cọc trước để giữ chỗ, không cho xem phòng, chỉ giao dịch online.",
        ),
        district_median_price=2_000_000,
    )

    assert result.score >= 0.6
    assert result.level == "suspicious"
    assert {signal.code for signal in result.signals} >= {
        "advance_payment",
        "no_inspection",
        "urgency",
    }


def test_unusually_low_price_is_explained():
    result = score_listing(_listing(price=700_000), district_median_price=2_000_000)

    assert result.score == 0.3
    assert result.level == "caution"
    assert [signal.code for signal in result.signals] == ["price_extreme"]


def test_community_reports_raise_risk_and_explain_why():
    result = score_listing(
        _listing(report_count=1, scam_report_count=1),
        district_median_price=2_000_000,
    )

    assert result.score == 0.3
    assert result.level == "caution"
    assert {signal.code for signal in result.signals} == {
        "community_reports",
        "community_scam_reports",
    }


class FakeRepo:
    def __init__(self, listings, pending=None):
        self.listings = listings
        self.pending = pending or []
        self.saved = []

    def get_listing(self, listing_id):
        return self.listings.get(listing_id)

    def district_median_price(self, listing):
        return 2_000_000

    def save(self, listing_id, result):
        self.saved.append((listing_id, result))

    def pending_ids(self, limit):
        return self.pending[:limit]

    def history(self, listing_id):
        return [
            {
                "id": 1,
                "listing_id": listing_id,
                "risk_score": 0.7,
                "risk_level": "suspicious",
                "risk_reasons": ["Kiểm thử"],
                "model_version": MODEL_VERSION,
                "evaluation_type": "automatic",
                "overridden_by": None,
                "override_note": None,
                "created_at": datetime.now(timezone.utc),
            }
        ]

    def override(self, listing_id, score, note, admin_id):
        if listing_id not in self.listings:
            return None
        return {
            "id": 2,
            "listing_id": listing_id,
            "risk_score": score,
            "risk_level": "safe" if score < 0.3 else "caution" if score < 0.6 else "suspicious",
            "risk_reasons": [f"Admin override: {note}"],
            "model_version": "manual-override",
            "evaluation_type": "manual",
            "overridden_by": admin_id,
            "override_note": note,
            "created_at": datetime.now(timezone.utc),
        }


def test_preview_does_not_persist_but_assess_does():
    repo = FakeRepo({12: _listing()})
    service = RiskService(repo)

    preview = service.assess(12, persist=False)
    persisted = service.assess(12, persist=True)

    assert preview.persisted is False
    assert persisted.persisted is True
    assert persisted.model_version == MODEL_VERSION
    assert len(repo.saved) == 1
    assert repo.saved[0][0] == 12


def test_missing_listing_returns_404():
    service = RiskService(FakeRepo({}))

    with pytest.raises(HTTPException) as error:
        service.assess(404, persist=False)

    assert error.value.status_code == 404


def test_batch_reports_levels_and_failed_ids():
    repo = FakeRepo(
        {
            1: _listing(id=1),
            2: _listing(
                id=2,
                description="Cọc ngay, chuyển khoản trước. Không cho xem phòng, chỉ giao dịch online.",
            ),
        },
        pending=[1, 2, 999],
    )

    result = RiskService(repo).assess_pending(10)

    assert result.processed == 2
    assert result.safe == 1
    assert result.suspicious == 1
    assert result.failed_listing_ids == [999]


def test_history_and_manual_override_keep_audit_information():
    service = RiskService(FakeRepo({12: _listing()}))
    assert service.history(12)[0].model_version == MODEL_VERSION
    override = service.override(12, 0.2, "Đã xác minh trực tiếp", admin_id=7)
    assert override.evaluation_type == "manual"
    assert override.overridden_by == 7
    assert override.override_note == "Đã xác minh trực tiếp"

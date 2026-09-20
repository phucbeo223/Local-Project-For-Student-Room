import math
import random

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.auth.security import (
    hash_password,
    verify_password,
    make_refresh_token,
    decode_token,
)
from app.engagement.recommender import content_vector, profile_vector, rank
from app.engagement.schemas import PreferenceQuiz
from app.listings.repo import build_filters
from app.listings.schemas import SearchParams
from app.room_service.chatbot.schemas import ChatAskRequest
from app.room_service.chatbot.providers import (
    DeterministicFakeEmbedder,
    GenerationResult,
    GroundedTemplateGenerator,
)
from app.room_service.chatbot.service import ChatService
from app.room_service.risk.scoring import score_listing


def test_long_unicode_passwords_do_not_truncate():
    password = "mật-khẩu-" * 12
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password(password + "x", hashed)


def test_refresh_tokens_unique_and_seven_days(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "refresh_token_ttl_days", 7)
    first, second = make_refresh_token(1), make_refresh_token(1)
    assert first != second
    payload = decode_token(first, "refresh")
    assert payload["exp"] - payload["iat"] == 7 * 86400


def test_search_extra_filters_are_bound_parameters():
    sql, params = build_filters(
        SearchParams(max_area=30, ward="x' OR true--", amenities=["wifi"])
    )
    assert "area <= :max_area" in sql and "ward ILIKE :ward" in sql
    assert "OR true" not in sql
    assert params["ward"] == "%x' OR true--%"


def test_quiz_rejects_invalid_preferences():
    with pytest.raises(ValidationError):
        PreferenceQuiz(max_price=-1, max_distance_ctu=0)
    with pytest.raises(ValidationError):
        PreferenceQuiz(max_price=2000000, max_distance_ctu=2000, amenities=["invented"])


def test_vector_stable_normalized_and_384d():
    row = {
        "price": 2000000,
        "distance_to_ctu": 1000,
        "district": "Ninh Kiều",
        "parsed_amenities": {"wifi": True},
    }
    vector = content_vector(row)
    assert len(vector) == 384 and vector == content_vector(row)
    assert math.isclose(sum(v * v for v in vector), 1)


def test_repeat_views_do_not_dominate_profile():
    event = {"id": 1, "type": "view", "price": 2000000}
    assert profile_vector(None, [event]) == profile_vector(None, [event] * 100)


def test_recommendations_80_20_unique_with_hard_constraints():
    candidates = [
        {
            "id": i,
            "price": 1000000 + i * 10000,
            "distance_to_ctu": 1000,
            "parsed_amenities": {"wifi": True},
            "popularity": i,
        }
        for i in range(30)
    ]
    candidates += [
        {
            "id": 100,
            "price": 9000000,
            "distance_to_ctu": 1000,
            "parsed_amenities": {"wifi": True},
        }
    ]
    prefs = {"max_price": 2000000, "max_distance_ctu": 3000, "amenities": ["wifi"]}
    _, items = rank(candidates, [], prefs, 10, random.Random(42))
    assert len(items) == 10 and sum(explore for _, _, explore in items) == 2
    assert len({row["id"] for _, row, _ in items}) == 10
    assert all(row["id"] != 100 for _, row, _ in items)


def test_popularity_fallback_and_dismissal():
    profile, items = rank(
        [{"id": 1, "popularity": 8}, {"id": 2, "popularity": 20}], [], None
    )
    assert profile is None and items[0][1]["id"] == 2
    _, items = rank([{"id": 1}, {"id": 2}], [{"id": 2, "type": "dismiss"}], None)
    assert [row["id"] for _, row, _ in items] == [1]


class ChatRepo:
    def retrieve(self, query, filters, vector, limit):
        self.filters = filters
        return [
            {
                "id": 1,
                "title": "Phòng",
                "price": 1800000,
                "source": "test",
                "rank": 1,
                "similarity_score": 0.99,
            }
        ]


def test_chat_memory_keeps_old_district_and_new_budget():
    repo = ChatRepo()
    service = ChatService(
        repo, DeterministicFakeEmbedder(), GroundedTemplateGenerator()
    )
    service.ask(
        ChatAskRequest(
            message="Dưới 1.8 triệu nhé",
            conversation_history=[
                {"role": "user", "content": "Tìm phòng Ninh Kiều dưới 2 triệu"},
                {"role": "assistant", "content": "Phòng ở Cái Răng giá 5 triệu"},
                {"role": "user", "content": "có wifi nữa"},
            ],
        )
    )
    assert repo.filters.district == "Ninh Kiều"
    assert repo.filters.max_price == 1800000
    assert "wifi" in repo.filters.amenities


def test_chat_invalid_citations_fall_back_to_grounded_answer():
    class BadGenerator:
        def generate(self, *args, **kwargs):
            return GenerationResult("Phòng giá 1 đồng [99]", "malicious")

    service = ChatService(ChatRepo(), DeterministicFakeEmbedder(), BadGenerator())
    response = service.ask(ChatAskRequest(message="Tìm phòng Ninh Kiều dưới 2 triệu"))
    assert "[99]" not in response.answer and "1 đồng" not in response.answer
    assert response.generation_provider == "template" and response.degraded


def test_new_budget_replaces_old_range_and_topic_switch_drops_history():
    repo = ChatRepo()
    service = ChatService(
        repo, DeterministicFakeEmbedder(), GroundedTemplateGenerator()
    )
    history = [
        {"role": "user", "content": "Tìm phòng Ninh Kiều từ 2 triệu đến 3 triệu"}
    ]
    service.ask(
        ChatAskRequest(message="Dưới 1 triệu thôi", conversation_history=history)
    )
    assert repo.filters.min_price is None and repo.filters.max_price == 1000000
    response = service.ask(
        ChatAskRequest(
            message="Dự báo thời tiết ngày mai", conversation_history=history
        )
    )
    assert response.intent == "out_of_scope" and response.no_answer


def test_risk_new_layers_are_explainable():
    result = score_listing(
        {
            "source": "user",
            "statistical_anomaly": True,
            "perceptual_image_conflict": True,
            "owner_recent_listing_count": 10,
        }
    )
    codes = {s.code for s in result.signals}
    assert {"isolation_forest", "cross_platform_image", "recent_posting_burst"} <= codes


def test_chat_requires_auth_before_accessing_provider():
    from app.room_service.chatbot.router import router

    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    assert client.post("/chat/ask", json={"message": "Tìm phòng"}).status_code in {
        401,
        403,
    }
    assert client.post(
        "/chat/feedback", json={"event_id": 1, "rating": 1}
    ).status_code in {401, 403}


def test_isolation_forest_requires_real_cohort_and_detects_extreme_outlier():
    pytest.importorskip("sklearn")
    from app.room_service.risk.anomaly import anomaly_signal

    class Repo:
        engine = object()

        def anomaly_cohort(self, listing):
            return [
                {"price": 1500000 + i * 15000, "area": 18 + i % 10} for i in range(120)
            ]

    abnormal, status = anomaly_signal(
        Repo(), {"district": "test", "price": 100000, "area": 500}
    )
    assert status == "available" and abnormal

    class EmptyRepo(Repo):
        engine = object()

        def anomaly_cohort(self, listing):
            return []

    assert anomaly_signal(
        EmptyRepo(), {"district": "test", "price": 2000000, "area": 20}
    ) == (False, "insufficient_cohort")

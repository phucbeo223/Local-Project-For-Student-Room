"""Run only on an isolated PostgreSQL test database: RUN_DB_TESTS=1."""

import os
import re
from uuid import uuid4
from urllib.parse import urlparse, parse_qs

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_DB_TESTS") != "1",
    reason="Requires isolated PostgreSQL; set RUN_DB_TESTS=1",
)


@pytest.fixture
def account(monkeypatch):
    from app.main import app, engine
    from fastapi.testclient import TestClient
    from app.auth import lifecycle

    sent = []
    monkeypatch.setattr(
        lifecycle, "send_email", lambda email, subject, content: sent.append(content)
    )
    return TestClient(app), engine, sent, f"fr-{uuid4().hex}@example.com"


def register_verified(account):
    client, engine, sent, email = account
    response = client.post(
        "/auth/register", json={"email": email, "password": "testpass123"}
    )
    assert response.status_code == 202, response.text
    assert "access_token" not in response.json()
    code = re.search(r"\b\d{6}\b", sent[-1]).group()
    response = client.post("/auth/verify-email", json={"email": email, "code": code})
    assert response.status_code == 200, response.text
    return response.json(), code


def test_otp_single_use_refresh_rotation_logout(account):
    client, _, _, email = account
    pair, code = register_verified(account)
    assert (
        client.post(
            "/auth/verify-email", json={"email": email, "code": code}
        ).status_code
        == 400
    )
    refreshed = client.post(
        "/auth/refresh", json={"refresh_token": pair["refresh_token"]}
    )
    assert refreshed.status_code == 200, refreshed.text
    assert (
        client.post(
            "/auth/refresh", json={"refresh_token": pair["refresh_token"]}
        ).status_code
        == 401
    )
    token = refreshed.json()["refresh_token"]
    assert client.post("/auth/logout", json={"refresh_token": token}).status_code == 200
    assert (
        client.post("/auth/refresh", json={"refresh_token": token}).status_code == 401
    )


def test_otp_attempt_limit_and_expiry(account):
    from sqlalchemy import text

    client, engine, sent, email = account
    assert (
        client.post(
            "/auth/register", json={"email": email, "password": "testpass123"}
        ).status_code
        == 202
    )
    code = re.search(r"\b\d{6}\b", sent[-1]).group()
    wrong = "000000" if code != "000000" else "111111"
    for _ in range(3):
        assert (
            client.post(
                "/auth/verify-email", json={"email": email, "code": wrong}
            ).status_code
            == 400
        )
    assert (
        client.post(
            "/auth/verify-email", json={"email": email, "code": code}
        ).status_code
        == 400
    )
    with engine.begin() as conn:
        conn.execute(
            text(
                "UPDATE auth_challenges SET attempts=0,expires_at=now()-interval '1 second' WHERE email=:email"
            ),
            {"email": email},
        )
    assert (
        client.post(
            "/auth/verify-email", json={"email": email, "code": code}
        ).status_code
        == 400
    )


def test_lockout_and_reset_revoke_sessions(account):
    client, _, sent, email = account
    pair, _ = register_verified(account)
    for _ in range(5):
        assert (
            client.post(
                "/auth/login", json={"email": email, "password": "wrong"}
            ).status_code
            == 401
        )
    assert (
        client.post(
            "/auth/login", json={"email": email, "password": "testpass123"}
        ).status_code
        == 429
    )
    assert (
        client.post("/auth/forgot-password", json={"email": email}).status_code == 200
    )
    token = parse_qs(urlparse(sent[-1]).query)["token"][0]
    body = {"email": email, "token": token, "password": "newpassword123"}
    assert client.post("/auth/reset-password", json=body).status_code == 200
    assert client.post("/auth/reset-password", json=body).status_code == 400
    assert (
        client.post(
            "/auth/refresh", json={"refresh_token": pair["refresh_token"]}
        ).status_code
        == 401
    )
    assert (
        client.get(
            "/auth/me", headers={"Authorization": f"Bearer {pair['access_token']}"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/auth/login", json={"email": email, "password": "newpassword123"}
        ).status_code
        == 200
    )


def test_sql_contracts_search_recommendation_risk_and_feedback(account):
    from sqlalchemy import text
    from app.room_service.risk.repo import RiskRepository
    from app.room_service.risk.service import RiskService
    from app.room_service.chatbot.repo import ChatRepository

    client, engine, _, _ = account
    pair, _ = register_verified(account)
    headers = {"Authorization": f"Bearer {pair['access_token']}"}
    uid = client.get("/auth/me", headers=headers).json()["id"]
    with engine.begin() as conn:
        lid = conn.execute(
            text(
                "INSERT INTO aggregated_listings(title,price,area,address,district,ward,source,status,cleaning_status,listing_type,distance_to_ctu,parsed_amenities,posted_by) VALUES ('Test FR room',1500000,20,'Đường test','Ninh Kiều','TestWard','user','active','cleaned','phong_tro',500,CAST(:amenities AS jsonb),:uid) RETURNING id"
            ),
            {"amenities": '{"wifi":true}', "uid": uid},
        ).scalar_one()
    result = client.get(
        "/listings", params={"ward": "TestWard", "max_area": 25, "amenities": "wifi"}
    )
    assert result.status_code == 200, result.text
    assert any(
        item["id"] == lid and item["parsed_amenities"]["wifi"]
        for item in result.json()["items"]
    )
    result = client.post(
        "/recommend/quiz",
        headers=headers,
        json={"max_price": 2000000, "max_distance_ctu": 1000, "amenities": ["wifi"]},
    )
    assert result.status_code == 200, result.text
    result = client.get("/recommend/for-you", headers=headers)
    assert result.status_code == 200, result.text
    assert not result.json()["cold_start"]
    assert any(item["listing"]["id"] == lid for item in result.json()["items"])
    with engine.connect() as conn:
        assert (
            conn.execute(
                text("SELECT vector_dims(preference_vector) FROM users WHERE id=:id"),
                {"id": uid},
            ).scalar_one()
            == 384
        )
    risk = RiskService(RiskRepository(engine))
    assert risk.assess(lid, persist=True).statistical_status == "insufficient_cohort"
    risk.override(lid, 0.1, "Kiểm tra thủ công", uid)
    assert risk.assess(lid, persist=True).model_version == "manual-override"
    event = ChatRepository(engine).record_event(
        {
            "intent": "find_listing",
            "confidence": 0.8,
            "no_answer": False,
            "degraded": False,
            "retrieval_mode": "hybrid",
            "generation_provider": "template",
            "result_count": 1,
            "latency_ms": 10,
        }
    )
    assert (
        client.post(
            "/chat/feedback", headers=headers, json={"event_id": event, "rating": 1}
        ).status_code
        == 404
    )
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE chatbot_events SET user_id=:uid WHERE id=:id"),
            {"uid": uid, "id": event},
        )
    assert (
        client.post(
            "/chat/feedback", headers=headers, json={"event_id": event, "rating": 1}
        ).status_code
        == 201
    )

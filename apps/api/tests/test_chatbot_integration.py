"""PostgreSQL integration tests for the stateless chatbot API."""

from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app, engine

client = TestClient(app)


def test_chatbot_vector_schema_exists():
    with engine.connect() as conn:
        extensions = {
            row[0] for row in conn.execute(text("SELECT extname FROM pg_extension"))
        }
        vector_type = conn.execute(
            text(
                "SELECT format_type(a.atttypid, a.atttypmod) FROM pg_attribute a "
                "JOIN pg_class c ON c.oid=a.attrelid "
                "WHERE c.relname='aggregated_listings' AND a.attname='embedding_vector'"
            )
        ).scalar_one()
    assert {"postgis", "vector"} <= extensions
    assert vector_type == "vector(384)"


def test_ask_is_stateless_and_history_routes_are_not_exposed():
    from app.auth.repo import AuthRepo
    from app.auth.security import make_access_token
    from uuid import uuid4

    user = AuthRepo(engine).create_user_with_identity(
        email=f"chat-{uuid4().hex}@example.com",
        name="Test",
        provider="local",
        provider_user_id=uuid4().hex,
        secret_hash=None,
    )
    asked = client.post(
        "/chat/ask",
        headers={
            "Authorization": f"Bearer {make_access_token(user['user_id'],'user')}"
        },
        json={"message": "Tìm phòng trọ dưới 2 triệu ở Ninh Kiều có wifi"},
    )
    assert asked.status_code == 200, asked.text
    body = asked.json()
    assert body["retrieval_mode"] in {"hybrid", "lexical_structured"}
    assert len(body["listings"]) <= 5
    assert body["answer"]
    assert "session_id" not in body
    assert "session_token" not in body
    assert "message_id" not in body
    assert client.get("/chat/history/1").status_code == 404
    assert (
        client.post("/chat/messages/1/feedback", json={"is_helpful": True}).status_code
        == 404
    )

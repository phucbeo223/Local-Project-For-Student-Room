import os
from pathlib import Path

from app import main


def test_main_registers_public_and_admin_review_routes():
    methods_by_path: dict[str, set[str]] = {}
    for route in main.app.routes:
        if hasattr(route, "methods"):
            methods_by_path.setdefault(route.path, set()).update(route.methods or [])

    assert "GET" in methods_by_path["/listings/{listing_id}/reviews"]
    assert "POST" in methods_by_path["/listings/{listing_id}/reviews"]
    assert "GET" in methods_by_path["/admin/reviews/flagged"]
    assert "PATCH" in methods_by_path["/admin/reviews/{review_id}"]


def test_dependency_health_does_not_expose_exception_details(monkeypatch):
    class BrokenEngine:
        def connect(self):
            raise RuntimeError("postgresql://user:secret@private-db/internal")

    class BrokenRedis:
        def ping(self):
            raise RuntimeError("redis://private-cache:6379/0")

    monkeypatch.setattr(main, "engine", BrokenEngine())
    monkeypatch.setattr(main, "redis_client", BrokenRedis())

    result = main.health_deps()

    assert result == {
        "postgres": "error",
        "postgis": "unknown",
        "pgvector": "unknown",
        "redis": "error",
    }
    assert "secret" not in repr(result)
    assert "private" not in repr(result)


def test_upgrade_scripts_include_latest_additive_migrations():
    configured_root = os.environ.get("PROJECT_ROOT")
    project_root = (
        Path(configured_root)
        if configured_root
        else Path(__file__).resolve().parents[3]
    )
    expected = ("95_fr_delivery.sql", "96_reviews_sentiment.sql")
    apply_script = (project_root / "scripts/apply_room_services.py").read_text(
        encoding="utf-8"
    )
    chatbot_script = (project_root / "scripts/apply_chatbot_dev.py").read_text(
        encoding="utf-8"
    )
    start_script = (project_root / "scripts/start_all.ps1").read_text(
        encoding="utf-8"
    )

    for migration in expected:
        assert migration in apply_script
        assert migration in chatbot_script
        assert migration.replace("_", "-") in start_script

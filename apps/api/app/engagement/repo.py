from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class EngagementRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def listing_exists(self, listing_id: int) -> bool:
        with self.engine.connect() as conn:
            return (
                conn.execute(
                    text(
                        "SELECT 1 FROM aggregated_listings WHERE id = :id "
                        "AND status NOT IN ('expired', 'hidden')"
                    ),
                    {"id": listing_id},
                ).first()
                is not None
            )

    def add_interaction(
        self,
        user_id: int,
        listing_id: int,
        interaction_type: str,
        duration_ms: int | None,
    ) -> dict:
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "INSERT INTO user_interactions (user_id, listing_id, type, duration_ms) "
                        "VALUES (:user_id, :listing_id, :type, :duration_ms) "
                        "RETURNING id, listing_id, type, duration_ms, created_at"
                    ),
                    {
                        "user_id": user_id,
                        "listing_id": listing_id,
                        "type": interaction_type,
                        "duration_ms": duration_ms,
                    },
                )
                .mappings()
                .one()
            )
        return dict(row)

    def add_favorite(self, user_id: int, listing_id: int) -> dict:
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "INSERT INTO listing_favorites (user_id, listing_id) "
                        "VALUES (:user_id, :listing_id) "
                        "ON CONFLICT (user_id, listing_id) DO UPDATE SET created_at = listing_favorites.created_at "
                        "RETURNING listing_id, created_at"
                    ),
                    {"user_id": user_id, "listing_id": listing_id},
                )
                .mappings()
                .one()
            )
            conn.execute(
                text(
                    "INSERT INTO user_interactions (user_id, listing_id, type) "
                    "SELECT :user_id, :listing_id, 'bookmark' "
                    "WHERE NOT EXISTS (SELECT 1 FROM user_interactions WHERE user_id = :user_id "
                    "AND listing_id = :listing_id AND type = 'bookmark')"
                ),
                {"user_id": user_id, "listing_id": listing_id},
            )
        return dict(row)

    def remove_favorite(self, user_id: int, listing_id: int) -> bool:
        with self.engine.begin() as conn:
            deleted = conn.execute(
                text(
                    "DELETE FROM listing_favorites WHERE user_id = :user_id AND listing_id = :listing_id"
                ),
                {"user_id": user_id, "listing_id": listing_id},
            ).rowcount
        return bool(deleted)

    def favorite_rows(self, user_id: int) -> list[dict]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "SELECT listing_id, created_at FROM listing_favorites "
                        "WHERE user_id = :user_id ORDER BY created_at DESC"
                    ),
                    {"user_id": user_id},
                )
                .mappings()
                .all()
            )
        return [dict(row) for row in rows]

    def create_saved_search(self, user_id: int, data: dict) -> dict:
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "INSERT INTO saved_searches (user_id, name, criteria, notify_enabled) "
                        "VALUES (:user_id, :name, CAST(:criteria AS jsonb), :notify_enabled) "
                        "RETURNING id, user_id, name, criteria, notify_enabled, created_at, "
                        "updated_at, last_notified_at"
                    ),
                    {"user_id": user_id, **data},
                )
                .mappings()
                .one()
            )
        return dict(row)

    def saved_searches(self, user_id: int) -> list[dict]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "SELECT id, user_id, name, criteria, notify_enabled, created_at, "
                        "updated_at, last_notified_at FROM saved_searches "
                        "WHERE user_id = :user_id ORDER BY created_at DESC"
                    ),
                    {"user_id": user_id},
                )
                .mappings()
                .all()
            )
        return [dict(row) for row in rows]

    def delete_saved_search(self, user_id: int, search_id: int) -> bool:
        with self.engine.begin() as conn:
            deleted = conn.execute(
                text(
                    "DELETE FROM saved_searches WHERE id = :id AND user_id = :user_id"
                ),
                {"id": search_id, "user_id": user_id},
            ).rowcount
        return bool(deleted)

    def interaction_history(self, user_id: int, limit: int = 200) -> list[dict]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "SELECT i.type, l.id, l.price, l.district, l.parsed_amenities, l.distance_to_ctu "
                        "FROM user_interactions i JOIN aggregated_listings l ON l.id = i.listing_id "
                        "WHERE i.user_id = :user_id AND (i.type <> 'bookmark' OR EXISTS "
                        "(SELECT 1 FROM listing_favorites f WHERE f.user_id=i.user_id AND f.listing_id=i.listing_id)) "
                        "ORDER BY i.created_at DESC LIMIT :limit"
                    ),
                    {"user_id": user_id, "limit": limit},
                )
                .mappings()
                .all()
            )
        return [dict(row) for row in rows]

    def recommendation_candidates(self, limit: int | None = None) -> list[dict]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "SELECT id, price, district, parsed_amenities, distance_to_ctu, quality_score, freshness_score, "
                        "risk_score, risk_evaluated_at, (SELECT count(DISTINCT i.user_id) FROM user_interactions i "
                        "WHERE i.listing_id=aggregated_listings.id AND i.type <> 'dismiss' "
                        "AND i.created_at > now()-interval '30 days') AS popularity FROM aggregated_listings "
                        "WHERE status = 'active' "
                        "AND (source = 'user' OR (cleaning_status = 'cleaned' AND listing_type = 'phong_tro')) "
                        "ORDER BY quality_score DESC NULLS LAST, freshness_score DESC NULLS LAST "
                        "LIMIT :limit"
                    ),
                    {"limit": limit},
                )
                .mappings()
                .all()
            )
        return [dict(row) for row in rows]

    def preferences(self, user_id: int) -> dict | None:
        with self.engine.connect() as conn:
            return conn.execute(
                text("SELECT recommendation_preferences FROM users WHERE id=:id"),
                {"id": user_id},
            ).scalar()

    def save_preferences(self, user_id: int, preferences: dict):
        import json
        from .recommender import content_vector

        with self.engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE users SET recommendation_preferences=CAST(:prefs AS jsonb), preference_vector=CAST(:vector AS vector) WHERE id=:id"
                ),
                {
                    "id": user_id,
                    "prefs": json.dumps(preferences),
                    "vector": str(content_vector(preferences, quiz=True)),
                },
            )

    def save_vector(self, user_id: int, vector):
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE users SET preference_vector=CAST(:vector AS vector) WHERE id=:id"
                ),
                {"id": user_id, "vector": str(vector) if vector else None},
            )

    def dashboard(self, days: int) -> dict[str, Any]:
        with self.engine.connect() as conn:
            chat = (
                conn.execute(
                    text(
                        "SELECT count(*) AS requests, "
                        "COALESCE(avg(confidence), 0) AS avg_confidence, "
                        "COALESCE(avg(no_answer::int), 0) AS no_answer_rate, "
                        "COALESCE(avg(degraded::int), 0) AS degraded_rate, "
                        "COALESCE(percentile_cont(0.95) WITHIN GROUP (ORDER BY latency_ms), 0) AS p95_latency "
                        "FROM chatbot_events WHERE created_at >= now() - make_interval(days => :days)"
                    ),
                    {"days": days},
                )
                .mappings()
                .one()
            )
            feedback = (
                conn.execute(
                    text(
                        "SELECT count(*) AS count, avg(CASE WHEN rating = 1 THEN 1.0 ELSE 0.0 END) AS positive_rate "
                        "FROM chatbot_feedback WHERE created_at >= now() - make_interval(days => :days)"
                    ),
                    {"days": days},
                )
                .mappings()
                .one()
            )
            product = (
                conn.execute(
                    text(
                        "SELECT (SELECT count(*) FROM user_interactions) AS interactions, "
                        "(SELECT count(*) FROM listing_favorites) AS favorites, "
                        "(SELECT count(*) FROM saved_searches) AS saved_searches"
                    )
                )
                .mappings()
                .one()
            )
            risk = (
                conn.execute(
                    text(
                        "SELECT count(*) FILTER (WHERE risk_evaluated_at IS NULL) AS not_evaluated, "
                        "count(*) FILTER (WHERE risk_evaluated_at IS NOT NULL AND risk_score < 0.3) AS safe, "
                        "count(*) FILTER (WHERE risk_evaluated_at IS NOT NULL AND risk_score >= 0.3 AND risk_score < 0.6) AS caution, "
                        "count(*) FILTER (WHERE risk_evaluated_at IS NOT NULL AND risk_score >= 0.6) AS suspicious "
                        "FROM aggregated_listings WHERE status NOT IN ('expired', 'hidden')"
                    )
                )
                .mappings()
                .one()
            )
            overrides = conn.execute(
                text(
                    "SELECT count(*) FROM risk_assessment_history WHERE evaluation_type = 'manual' "
                    "AND created_at >= now() - make_interval(days => :days)"
                ),
                {"days": days},
            ).scalar_one()
            latest_eval = (
                conn.execute(
                    text(
                        "SELECT dataset_version, model_version, prompt_version, metrics, passed, created_at "
                        "FROM ai_evaluation_runs ORDER BY created_at DESC LIMIT 1"
                    )
                )
                .mappings()
                .first()
            )
        return {
            "chat": dict(chat),
            "feedback": dict(feedback),
            "product": dict(product),
            "risk": dict(risk),
            "overrides": int(overrides),
            "latest_evaluation": dict(latest_eval) if latest_eval else None,
        }

    def create_evaluation_run(self, data: dict) -> dict:
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "INSERT INTO ai_evaluation_runs "
                        "(dataset_version, model_version, prompt_version, metrics, passed) "
                        "VALUES (:dataset_version, :model_version, :prompt_version, CAST(:metrics AS jsonb), :passed) "
                        "RETURNING dataset_version, model_version, prompt_version, metrics, passed, created_at"
                    ),
                    data,
                )
                .mappings()
                .one()
            )
        return dict(row)

    def notifications(self, user_id: int, limit: int = 100) -> list[dict]:
        with self.engine.connect() as conn:
            rows = (
                conn.execute(
                    text(
                        "SELECT n.id, n.search_id, n.listing_id, l.title AS listing_title, "
                        "n.message, n.read_at, n.created_at FROM user_notifications n "
                        "LEFT JOIN aggregated_listings l ON l.id = n.listing_id "
                        "WHERE n.user_id = :user_id ORDER BY n.created_at DESC LIMIT :limit"
                    ),
                    {"user_id": user_id, "limit": limit},
                )
                .mappings()
                .all()
            )
        return [dict(row) for row in rows]

    def mark_notification_read(self, user_id: int, notification_id: int) -> dict | None:
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "UPDATE user_notifications SET read_at = COALESCE(read_at, now()) "
                        "WHERE id = :id AND user_id = :user_id "
                        "RETURNING id, search_id, listing_id, message, read_at, created_at"
                    ),
                    {"id": notification_id, "user_id": user_id},
                )
                .mappings()
                .first()
            )
            if row is None:
                return None
            value = dict(row)
            value["listing_title"] = conn.execute(
                text("SELECT title FROM aggregated_listings WHERE id = :id"),
                {"id": value["listing_id"]},
            ).scalar()
        return value

    def refresh_notifications(self, user_id: int) -> int:
        """Match saved searches against listings changed since the previous check."""
        created = 0
        with self.engine.begin() as conn:
            searches = (
                conn.execute(
                    text(
                        "SELECT id, name, criteria, COALESCE(last_notified_at, created_at) AS since "
                        "FROM saved_searches WHERE user_id = :user_id AND notify_enabled IS TRUE"
                    ),
                    {"user_id": user_id},
                )
                .mappings()
                .all()
            )
            for search in searches:
                criteria = search["criteria"] or {}
                clauses = [
                    "status = 'active'",
                    "updated_at > :since",
                    "(source = 'user' OR (cleaning_status = 'cleaned' AND listing_type = 'phong_tro'))",
                ]
                params: dict[str, Any] = {"since": search["since"]}
                for key, operator in (
                    ("min_price", ">="),
                    ("max_price", "<="),
                    ("min_area", ">="),
                    ("max_distance_ctu", "<="),
                ):
                    value = criteria.get(key)
                    if value is not None:
                        column = (
                            "distance_to_ctu"
                            if key == "max_distance_ctu"
                            else key.replace("min_", "").replace("max_", "")
                        )
                        clauses.append(f"{column} {operator} :{key}")
                        params[key] = value
                if criteria.get("district"):
                    clauses.append("district ILIKE :district")
                    params["district"] = f"%{criteria['district']}%"
                if criteria.get("q"):
                    clauses.append("(title ILIKE :q OR description ILIKE :q)")
                    params["q"] = f"%{criteria['q']}%"
                for index, amenity in enumerate(criteria.get("amenities") or []):
                    param = f"amenity_{index}"
                    clauses.append(
                        f"COALESCE((parsed_amenities ->> :{param})::boolean, false) IS TRUE"
                    )
                    params[param] = amenity
                matches = (
                    conn.execute(
                        text(
                            "SELECT id, title FROM aggregated_listings WHERE "
                            + " AND ".join(clauses)
                            + " ORDER BY updated_at DESC LIMIT 50"
                        ),
                        params,
                    )
                    .mappings()
                    .all()
                )
                for listing in matches:
                    result = conn.execute(
                        text(
                            "INSERT INTO user_notifications (user_id, search_id, listing_id, message) "
                            "VALUES (:user_id, :search_id, :listing_id, :message) "
                            "ON CONFLICT (search_id, listing_id) DO NOTHING"
                        ),
                        {
                            "user_id": user_id,
                            "search_id": search["id"],
                            "listing_id": listing["id"],
                            "message": f"Có phòng mới phù hợp với ‘{search['name']}’: {listing['title']}",
                        },
                    )
                    created += int(result.rowcount or 0)
                conn.execute(
                    text(
                        "UPDATE saved_searches SET last_notified_at = now(), updated_at = now() WHERE id = :id"
                    ),
                    {"id": search["id"]},
                )
        return created

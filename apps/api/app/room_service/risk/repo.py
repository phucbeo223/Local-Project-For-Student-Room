from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine

from .scoring import MODEL_VERSION, ScoreResult


class RiskRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_listing(self, listing_id: int) -> dict | None:
        with self.engine.connect() as conn:
            row = conn.execute(
                text(
                    "SELECT id, title, description, price, area, address, district, images, "
                    "source, source_url, listing_type, quality_score, freshness_score, "
                    "geocode_confidence, risk_score, risk_reasons, risk_model, risk_evaluated_at, "
                    "(SELECT count(*) FROM aggregated_listings owner_l WHERE owner_l.posted_by = aggregated_listings.posted_by "
                    "AND owner_l.status = 'active') AS owner_active_listing_count, "
                    "(SELECT count(*) FROM reports r WHERE r.listing_id = aggregated_listings.id "
                    "AND r.status IN ('pending', 'reviewed')) AS report_count, "
                    "(SELECT count(*) FROM reports r WHERE r.listing_id = aggregated_listings.id "
                    "AND r.status IN ('pending', 'reviewed') AND r.reason = 'scam') AS scam_report_count "
                    "FROM aggregated_listings WHERE id = :id"
                ),
                {"id": listing_id},
            ).mappings().first()
        return dict(row) if row else None

    def district_median_price(self, listing: dict) -> float | None:
        district = listing.get("district")
        if not district:
            return None
        with self.engine.connect() as conn:
            value = conn.execute(
                text(
                    "SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY price) "
                    "FROM aggregated_listings WHERE status = 'active' "
                    "AND cleaning_status = 'cleaned' AND price IS NOT NULL "
                    "AND district = :district "
                    "AND listing_type = CAST(:listing_type AS listing_type_enum)"
                ),
                {
                    "district": district,
                    "listing_type": listing.get("listing_type") or "phong_tro",
                },
            ).scalar()
        return float(value) if value is not None else None

    def save(self, listing_id: int, result: ScoreResult) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    "UPDATE aggregated_listings SET risk_score = :score, "
                    "risk_reasons = :reasons, risk_model = :model, "
                    "risk_evaluated_at = :evaluated_at, risk_status = 'evaluated' WHERE id = :id"
                ),
                {
                    "id": listing_id,
                    "score": result.score,
                    "reasons": result.reasons,
                    "model": MODEL_VERSION,
                    "evaluated_at": result.evaluated_at,
                },
            )
            conn.execute(
                text(
                    "INSERT INTO risk_assessment_history "
                    "(listing_id, risk_score, risk_level, risk_reasons, model_version, evaluation_type, created_at) "
                    "VALUES (:id, :score, :level, :reasons, :model, 'automatic', :evaluated_at)"
                ),
                {
                    "id": listing_id,
                    "score": result.score,
                    "level": result.level,
                    "reasons": result.reasons,
                    "model": MODEL_VERSION,
                    "evaluated_at": result.evaluated_at,
                },
            )

    def pending_ids(self, limit: int) -> list[int]:
        with self.engine.connect() as conn:
            rows = conn.execute(
                text(
                    "SELECT id FROM aggregated_listings WHERE status = 'active' "
                    "AND cleaning_status = 'cleaned' "
                    "AND (risk_evaluated_at IS NULL OR updated_at > risk_evaluated_at) "
                    "ORDER BY updated_at DESC LIMIT :limit"
                ),
                {"limit": limit},
            ).all()
        return [int(row[0]) for row in rows]

    def history(self, listing_id: int, limit: int = 50) -> list[dict]:
        with self.engine.connect() as conn:
            rows = conn.execute(
                text(
                    "SELECT id, listing_id, risk_score, risk_level, risk_reasons, model_version, "
                    "evaluation_type, overridden_by, override_note, created_at "
                    "FROM risk_assessment_history WHERE listing_id = :listing_id "
                    "ORDER BY created_at DESC LIMIT :limit"
                ),
                {"listing_id": listing_id, "limit": limit},
            ).mappings().all()
        output = []
        for row in rows:
            value = dict(row)
            value["risk_reasons"] = value.get("risk_reasons") or []
            output.append(value)
        return output

    def override(self, listing_id: int, score: float, note: str, admin_id: int) -> dict | None:
        from datetime import datetime, timezone

        level = "safe" if score < 0.3 else "caution" if score < 0.6 else "suspicious"
        reason = f"Admin override: {note}"
        now = datetime.now(timezone.utc)
        with self.engine.begin() as conn:
            updated = conn.execute(
                text(
                    "UPDATE aggregated_listings SET risk_score = :score, risk_reasons = :reasons, "
                    "risk_model = 'manual-override', risk_evaluated_at = :created_at, "
                    "risk_status = 'evaluated', updated_at = now() WHERE id = :listing_id"
                ),
                {
                    "listing_id": listing_id,
                    "score": score,
                    "reasons": [reason],
                    "created_at": now,
                },
            )
            if not updated.rowcount:
                return None
            row = conn.execute(
                text(
                    "INSERT INTO risk_assessment_history "
                    "(listing_id, risk_score, risk_level, risk_reasons, model_version, "
                    "evaluation_type, overridden_by, override_note, created_at) "
                    "VALUES (:listing_id, :score, :level, :reasons, 'manual-override', "
                    "'manual', :admin_id, :note, :created_at) "
                    "RETURNING id, listing_id, risk_score, risk_level, risk_reasons, model_version, "
                    "evaluation_type, overridden_by, override_note, created_at"
                ),
                {
                    "listing_id": listing_id,
                    "score": score,
                    "level": level,
                    "reasons": [reason],
                    "admin_id": admin_id,
                    "note": note,
                    "created_at": now,
                },
            ).mappings().one()
        return dict(row)

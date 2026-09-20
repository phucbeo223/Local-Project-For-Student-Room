"""Repository contracts against an isolated PostgreSQL database."""
import os
from contextlib import nullcontext

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.skipif(os.environ.get("RUN_DB_TESTS") != "1", reason="isolated DB required")


def test_stats_are_uncapped_and_map_preserves_visibility_and_has_small_payload():
    from app.main import engine
    from app.listings.repo import ListingQueryRepo

    with engine.connect() as conn:
        transaction = conn.begin()
        try:
            conn.execute(text("CREATE TEMP TABLE aggregated_listings (LIKE public.aggregated_listings INCLUDING DEFAULTS) ON COMMIT DROP"))
            conn.execute(text("""
                INSERT INTO aggregated_listings(id,title,source,status,cleaning_status,listing_type,
                    price,geom,images,description)
                SELECT n,'Room ' || n,'user','active','cleaned','phong_tro',1500000,
                    ST_SetSRID(ST_MakePoint(105.7683,10.0322),4326),
                    ARRAY['first.jpg','second.jpg'],repeat('long description ',500)
                FROM generate_series(1,305) AS n
            """))
            conn.execute(text("UPDATE aggregated_listings SET status='hidden' WHERE id=1"))
            conn.execute(text("UPDATE aggregated_listings SET status='expired' WHERE id=2"))
            conn.execute(text("UPDATE aggregated_listings SET source='crawl',cleaning_status='raw' WHERE id=3"))

            class SameConnection:
                def connect(self):
                    return nullcontext(conn)

            repo = ListingQueryRepo(SameConnection())
            stats = repo.stats()
            assert stats.total == stats.nearby_count == 302
            assert stats.median_price == 1500000
            items = repo.map_listings(10.0322, 105.7683, 3000)
            assert len(items) == 300
            assert not {1, 2, 3}.intersection(item.id for item in items)
            assert all(item.images == ["first.jpg"] for item in items)
            assert all("description" not in item.model_dump() for item in items)
            conn.execute(text("DELETE FROM aggregated_listings"))
            assert repo.stats().model_dump() == {"total": 0, "nearby_count": 0, "median_price": None}
        finally:
            transaction.rollback()

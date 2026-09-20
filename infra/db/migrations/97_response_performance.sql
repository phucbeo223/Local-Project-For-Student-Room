-- Match ST_DWithin's geography expression; the geometry index cannot serve it.
CREATE INDEX IF NOT EXISTS idx_listings_geography
    ON aggregated_listings USING GIST ((geom::geography))
    WHERE geom IS NOT NULL;

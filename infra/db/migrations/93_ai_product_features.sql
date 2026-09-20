-- Product and AI research features. This migration intentionally does not
-- modify crawler bookkeeping or crawler source data.

ALTER TABLE aggregated_listings
    ADD COLUMN IF NOT EXISTS risk_status VARCHAR(20) NOT NULL DEFAULT 'not_evaluated';

UPDATE aggregated_listings
SET risk_status = CASE
    WHEN risk_evaluated_at IS NULL THEN 'not_evaluated'
    ELSE 'evaluated'
END;

CREATE TABLE IF NOT EXISTS risk_assessment_history (
    id              BIGSERIAL PRIMARY KEY,
    listing_id      INTEGER NOT NULL REFERENCES aggregated_listings(id) ON DELETE CASCADE,
    risk_score      REAL NOT NULL,
    risk_level      VARCHAR(20) NOT NULL,
    risk_reasons    TEXT[] NOT NULL DEFAULT '{}',
    model_version   VARCHAR(80) NOT NULL,
    evaluation_type VARCHAR(20) NOT NULL DEFAULT 'automatic',
    overridden_by   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    override_note   TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_risk_history_listing_created
    ON risk_assessment_history (listing_id, created_at DESC);

CREATE TABLE IF NOT EXISTS listing_favorites (
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    listing_id  INTEGER NOT NULL REFERENCES aggregated_listings(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, listing_id)
);
CREATE INDEX IF NOT EXISTS idx_listing_favorites_user_created
    ON listing_favorites (user_id, created_at DESC);

ALTER TABLE saved_searches
    ADD COLUMN IF NOT EXISTS name VARCHAR(100) DEFAULT 'Tìm kiếm đã lưu',
    ADD COLUMN IF NOT EXISTS notify_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ADD COLUMN IF NOT EXISTS last_notified_at TIMESTAMPTZ;

UPDATE saved_searches SET name = 'Tìm kiếm #' || id WHERE name IS NULL;
ALTER TABLE saved_searches ALTER COLUMN name SET DEFAULT 'Tìm kiếm đã lưu';
ALTER TABLE saved_searches ALTER COLUMN name SET NOT NULL;

CREATE TABLE IF NOT EXISTS chatbot_events (
    id                  BIGSERIAL PRIMARY KEY,
    intent              VARCHAR(40) NOT NULL,
    confidence          REAL NOT NULL,
    no_answer           BOOLEAN NOT NULL,
    degraded            BOOLEAN NOT NULL,
    retrieval_mode      VARCHAR(40) NOT NULL,
    generation_provider VARCHAR(40) NOT NULL,
    result_count        INTEGER NOT NULL,
    latency_ms          INTEGER NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_chatbot_events_created
    ON chatbot_events (created_at DESC);

CREATE TABLE IF NOT EXISTS chatbot_feedback (
    id          BIGSERIAL PRIMARY KEY,
    event_id    BIGINT REFERENCES chatbot_events(id) ON DELETE SET NULL,
    user_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
    rating      SMALLINT NOT NULL CHECK (rating IN (-1, 1)),
    reason      VARCHAR(80),
    comment     TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_chatbot_feedback_created
    ON chatbot_feedback (created_at DESC);

CREATE TABLE IF NOT EXISTS ai_evaluation_runs (
    id              BIGSERIAL PRIMARY KEY,
    dataset_version VARCHAR(100) NOT NULL,
    model_version   VARCHAR(120),
    prompt_version  VARCHAR(120),
    metrics         JSONB NOT NULL,
    passed          BOOLEAN NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_ai_evaluation_runs_created
    ON ai_evaluation_runs (created_at DESC);

CREATE TABLE IF NOT EXISTS user_notifications (
    id          BIGSERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    search_id   INTEGER REFERENCES saved_searches(id) ON DELETE CASCADE,
    listing_id  INTEGER REFERENCES aggregated_listings(id) ON DELETE CASCADE,
    message     TEXT NOT NULL,
    read_at     TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (search_id, listing_id)
);
CREATE INDEX IF NOT EXISTS idx_user_notifications_user_created
    ON user_notifications (user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_user_interactions_user_type_created
    ON user_interactions (user_id, type, created_at DESC);

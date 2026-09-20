-- Additive migration. Run once on existing databases; never recreate volumes.
ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_version integer NOT NULL DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS recommendation_preferences jsonb;
ALTER TABLE user_identities ADD COLUMN IF NOT EXISTS failed_attempts integer NOT NULL DEFAULT 0;
ALTER TABLE user_identities ADD COLUMN IF NOT EXISTS locked_until timestamptz;
CREATE TABLE IF NOT EXISTS auth_challenges (
  email text NOT NULL, purpose text NOT NULL, digest text NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}', attempts integer NOT NULL DEFAULT 0,
  expires_at timestamptz NOT NULL, sent_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(email, purpose)
);
CREATE TABLE IF NOT EXISTS auth_sessions (
  digest text PRIMARY KEY, user_id bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  expires_at timestamptz NOT NULL, revoked boolean NOT NULL DEFAULT false
);
CREATE INDEX IF NOT EXISTS auth_sessions_user_idx ON auth_sessions(user_id);
CREATE TABLE IF NOT EXISTS request_buckets (
  key text PRIMARY KEY, count integer NOT NULL, expires_at timestamptz NOT NULL
);
ALTER TABLE aggregated_listings ADD COLUMN IF NOT EXISTS ward text;
ALTER TABLE chatbot_events ADD COLUMN IF NOT EXISTS user_id bigint REFERENCES users(id) ON DELETE SET NULL;
CREATE TABLE IF NOT EXISTS listing_image_hashes (
  listing_id bigint NOT NULL REFERENCES aggregated_listings(id) ON DELETE CASCADE,
  image_url text NOT NULL, phash bit(64) NOT NULL, PRIMARY KEY(listing_id,image_url)
);

-- ACG Dealer Portal — D1 schema (Phase 1)
--
-- Apply with:
--   wrangler d1 execute acg-dealer-portal --file=./schema.sql
-- For local dev:
--   wrangler d1 execute acg-dealer-portal --local --file=./schema.sql
--
-- This is Phase 1 only. Phases 2–4 add: dealers, sessions, password_reset_tokens,
-- quotes, generated PDF metadata. We'll add them as separate migration files
-- (002_dealers.sql, 003_quotes.sql, etc.) when each phase ships, never editing
-- this file.

CREATE TABLE IF NOT EXISTS dealer_applications (
  id                  TEXT PRIMARY KEY,                 -- UUID
  created_at          TEXT NOT NULL,                    -- ISO 8601
  status              TEXT NOT NULL DEFAULT 'pending',  -- pending | approved | rejected
  status_updated_at   TEXT,

  -- Application fields (mirror REQUIRED_FIELDS / ALLOWED_FIELDS in worker.js)
  company             TEXT NOT NULL,
  contact_name        TEXT NOT NULL,
  email               TEXT NOT NULL,
  phone               TEXT NOT NULL,
  address             TEXT NOT NULL,
  license_number      TEXT,
  years_in_business   TEXT NOT NULL,                    -- enum-as-string: <1, 1-3, 4-10, 10+
  manufacturers       TEXT NOT NULL,
  annual_volume       TEXT NOT NULL,                    -- enum-as-string range
  notes               TEXT,

  -- Audit
  submitted_ip        TEXT,
  user_agent          TEXT
);

CREATE INDEX IF NOT EXISTS idx_dealer_applications_status_created
  ON dealer_applications (status, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_dealer_applications_email
  ON dealer_applications (email);

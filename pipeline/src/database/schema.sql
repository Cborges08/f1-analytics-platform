-- F1 Analytics Platform — Database Schema
-- All tables include year column for multi-season ML training

CREATE TABLE IF NOT EXISTS sessions (
    session_key       INTEGER PRIMARY KEY,
    session_name      VARCHAR(50),
    session_type      VARCHAR(20),  -- Practice, Qualifying, Race
    date_start        TIMESTAMPTZ,
    year              INTEGER,
    circuit_key       INTEGER,
    circuit_short_name VARCHAR(50),
    country_name      VARCHAR(50),
    location          VARCHAR(50),
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS drivers (
    id                SERIAL PRIMARY KEY,
    session_key       INTEGER REFERENCES sessions(session_key),
    driver_number     INTEGER,
    full_name         VARCHAR(100),
    name_acronym      VARCHAR(5),
    team_name         VARCHAR(100),
    team_colour       VARCHAR(10),
    country_code      VARCHAR(5),
    headshot_url      TEXT,
    year              INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_key, driver_number)
);

CREATE TABLE IF NOT EXISTS race_results (
    id                SERIAL PRIMARY KEY,
    session_key       INTEGER REFERENCES sessions(session_key),
    driver_number     INTEGER,
    position          INTEGER,
    year              INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_key, driver_number)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_sessions_year ON sessions(year);
CREATE INDEX IF NOT EXISTS idx_drivers_session ON drivers(session_key);
CREATE INDEX IF NOT EXISTS idx_race_results_driver ON race_results(driver_number);
CREATE INDEX IF NOT EXISTS idx_race_results_year ON race_results(year);
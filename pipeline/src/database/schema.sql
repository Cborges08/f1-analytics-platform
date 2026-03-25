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

CREATE TABLE IF NOT EXISTS pit_stops (
    id                SERIAL PRIMARY KEY,
    session_key       INTEGER REFERENCES sessions(session_key),
    driver_number     INTEGER,
    pit_duration      NUMERIC(8,3),   -- seconds
    lap_number        INTEGER,
    year              INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS race_control_events (
    id                SERIAL PRIMARY KEY,
    session_key       INTEGER REFERENCES sessions(session_key),
    date              TIMESTAMPTZ,
    lap_number        INTEGER,
    category          VARCHAR(50),    -- Flag, SafetyCar, etc
    flag              VARCHAR(20),    -- YELLOW, RED, GREEN, etc
    message           TEXT,
    year              INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS qualifying_results (
    id                SERIAL PRIMARY KEY,
    session_key       INTEGER REFERENCES sessions(session_key),
    driver_number     INTEGER,
    position          INTEGER,
    q1_time           VARCHAR(20),
    q2_time           VARCHAR(20),
    q3_time           VARCHAR(20),
    year              INTEGER,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_key, driver_number)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_sessions_year ON sessions(year);
CREATE INDEX IF NOT EXISTS idx_drivers_session ON drivers(session_key);
CREATE INDEX IF NOT EXISTS idx_race_results_driver ON race_results(driver_number);
CREATE INDEX IF NOT EXISTS idx_race_results_year ON race_results(year);
CREATE INDEX IF NOT EXISTS idx_pit_stops_session ON pit_stops(session_key);
CREATE INDEX IF NOT EXISTS idx_pit_stops_driver ON pit_stops(driver_number);
CREATE INDEX IF NOT EXISTS idx_race_control_session ON race_control_events(session_key);
CREATE INDEX IF NOT EXISTS idx_race_control_flag ON race_control_events(flag);
CREATE INDEX IF NOT EXISTS idx_qualifying_session ON qualifying_results(session_key);
CREATE INDEX IF NOT EXISTS idx_qualifying_driver ON qualifying_results(driver_number);
CREATE INDEX IF NOT EXISTS idx_qualifying_year ON qualifying_results(year);
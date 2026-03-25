import pandas as pd
from sqlalchemy import create_engine, text
from database.connection import get_engine


def save_sessions(df: pd.DataFrame, year: int) -> int:
    """Save sessions to database. Returns rows inserted."""
    if df.empty:
        return 0

    cols = [
        "session_key", "session_name", "date_start",
        "circuit_key", "circuit_short_name",
        "country_name", "location"
    ]
    existing_cols = [c for c in cols if c in df.columns]
    data = df[existing_cols].copy()
    data["year"] = year

    # Derive session_type from session_name
    def classify(name):
        if "Race" in str(name): return "Race"
        if "Qualifying" in str(name): return "Qualifying"
        if "Practice" in str(name): return "Practice"
        if "Sprint" in str(name): return "Sprint"
        return "Other"

    data["session_type"] = data["session_name"].apply(classify)

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
                INSERT INTO sessions (
                    session_key, session_name, session_type, date_start,
                    circuit_key, circuit_short_name, country_name, location, year
                ) VALUES (
                    :session_key, :session_name, :session_type, :date_start,
                    :circuit_key, :circuit_short_name, :country_name, :location, :year
                )
                ON CONFLICT (session_key) DO NOTHING
            """), row.to_dict())
        conn.commit()

    return len(data)


def save_drivers(df: pd.DataFrame, session_key: int, year: int) -> int:
    """Save drivers to database. Returns rows inserted."""
    if df.empty:
        return 0

    cols = [
        "driver_number", "full_name", "name_acronym",
        "team_name", "team_colour", "country_code", "headshot_url"
    ]
    existing_cols = [c for c in cols if c in df.columns]
    data = df[existing_cols].copy()
    data["session_key"] = session_key
    data["year"] = year

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
                INSERT INTO drivers (
                    session_key, driver_number, full_name, name_acronym,
                    team_name, team_colour, country_code, headshot_url, year
                ) VALUES (
                    :session_key, :driver_number, :full_name, :name_acronym,
                    :team_name, :team_colour, :country_code, :headshot_url, :year
                )
                ON CONFLICT (session_key, driver_number) DO NOTHING
            """), row.to_dict())
        conn.commit()

    return len(data)


def save_race_results(df: pd.DataFrame, session_key: int, year: int) -> int:
    """Save race results to database. Returns rows inserted."""
    if df.empty:
        return 0

    # Get final position per driver (last entry in position data)
    final = df.sort_values("date").groupby("driver_number").last().reset_index()
    data = final[["driver_number", "position"]].copy()
    data["session_key"] = session_key
    data["year"] = year

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
                INSERT INTO race_results (
                    session_key, driver_number, position, year
                ) VALUES (
                    :session_key, :driver_number, :position, :year
                )
                ON CONFLICT (session_key, driver_number) DO NOTHING
            """), row.to_dict())
        conn.commit()

    return len(data)

def save_pit_stops(df: pd.DataFrame, session_key: int, year: int) -> int:
    """Save pit stop data. Returns rows inserted."""
    if df.empty:
        return 0

    cols = ["driver_number", "pit_duration", "lap_number"]
    existing_cols = [c for c in cols if c in df.columns]
    data = df[existing_cols].copy()
    data["session_key"] = session_key
    data["year"] = year

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
                INSERT INTO pit_stops (
                    session_key, driver_number, pit_duration, lap_number, year
                ) VALUES (
                    :session_key, :driver_number, :pit_duration, :lap_number, :year
                )
                ON CONFLICT (session_key, driver_number, lap_number) DO NOTHING
            """), row.to_dict())
        conn.commit()

    return len(data)

def save_qualifying_results(df: pd.DataFrame, session_key: int, year: int) -> int:
    """Save qualifying results to database. Returns rows inserted."""
    if df.empty:
        return 0

    data = df.copy()
    data["session_key"] = session_key
    data["year"] = year

    # Rename qualifying_position back to position for DB storage
    if "qualifying_position" in data.columns:
        data = data.rename(columns={"qualifying_position": "position"})

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            row_dict = row.to_dict()
            conn.execute(text("""
                INSERT INTO qualifying_results (
                    session_key, driver_number, position, year
                ) VALUES (
                    :session_key, :driver_number, :position, :year
                )
                ON CONFLICT (session_key, driver_number) DO NOTHING
            """), row_dict)
        conn.commit()

    return len(data)


def save_race_control(df: pd.DataFrame, session_key: int, year: int) -> int:
    """Save race control events. Returns rows inserted."""
    if df.empty:
        return 0

    cols = ["date", "lap_number", "category", "flag", "message"]
    existing_cols = [c for c in cols if c in df.columns]
    data = df[existing_cols].copy()
    data["session_key"] = session_key
    data["year"] = year

    engine = get_engine()
    with engine.connect() as conn:
        for _, row in data.iterrows():
            conn.execute(text("""
                INSERT INTO race_control_events (
                    session_key, date, lap_number, category, flag, message, year
                ) VALUES (
                    :session_key, :date, :lap_number, :category, :flag, :message, :year
                )
            """), row.to_dict())
        conn.commit()

    return len(data)
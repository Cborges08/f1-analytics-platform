import pandas as pd
import numpy as np
from sqlalchemy import text
from database.connection import get_engine


def load_features() -> pd.DataFrame:
    """Load mart_race_features from analytics schema."""
    engine = get_engine()
    query = """
        SELECT 
            driver_number,
            driver_name,
            name_acronym,
            team_name,
            circuit_short_name,
            country_name,
            race_date,
            year,
            finish_position,
            result_category,
            total_pit_stops,
            avg_pit_duration,
            fastest_pit,
            total_pit_time,
            first_pit_lap,
            yellow_flags,
            double_yellow_flags,
            red_flags,
            safety_car_events,
            vsc_events,
            total_incidents,
            qualifying_position
        FROM analytics.mart_race_features
        WHERE finish_position IS NOT NULL
        ORDER BY race_date, finish_position
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create ML features from raw data."""
    df = df.copy()
    df["race_date"] = pd.to_datetime(df["race_date"])
    df = df.sort_values(["driver_number", "race_date"])

    # Rolling features — last 3 races per driver
    df["avg_position_last3"] = (
        df.groupby("driver_number")["finish_position"]
        .transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean())
    )

    df["avg_position_last5"] = (
        df.groupby("driver_number")["finish_position"]
        .transform(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
    )

    # Team performance — avg position this season
    team_avg = (
        df.groupby(["team_name", "year"])["finish_position"]
        .transform("mean")
    )
    df["team_avg_position"] = team_avg

    # Encode team as numeric
    df["team_encoded"] = pd.Categorical(df["team_name"]).codes

    # Encode circuit as numeric
    df["circuit_encoded"] = pd.Categorical(df["circuit_short_name"]).codes

    # Total chaotic events in race
    df["chaos_index"] = (
        df["yellow_flags"] +
        df["double_yellow_flags"] * 2 +
        df["red_flags"] * 5 +
        df["safety_car_events"] * 3 +
        df["vsc_events"] * 2
    )

    # Pit stop efficiency
    df["pit_efficiency"] = df["total_pit_time"] / df["total_pit_stops"].replace(0, 1)

    # Fill missing qualifying positions with median
    df["qualifying_position"] = df["qualifying_position"].fillna(df["qualifying_position"].median())

    return df


def get_feature_columns() -> list:
    """Return list of feature columns for the model."""
    return [
        "driver_number",
        "team_encoded",
        "circuit_encoded",
        "total_pit_stops",
        "avg_pit_duration",
        "fastest_pit",
        "total_pit_time",
        "first_pit_lap",
        "pit_efficiency",
        "yellow_flags",
        "red_flags",
        "safety_car_events",
        "vsc_events",
        "chaos_index",
        "team_avg_position",
        "avg_position_last3",
        "avg_position_last5",
        "qualifying_position",
    ]
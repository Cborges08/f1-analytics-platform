import requests
import pandas as pd
from config import OPENF1_BASE_URL


def get_sessions(year: int) -> pd.DataFrame:
    """Fetch all F1 sessions for a given year."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/sessions",
        params={"year": year}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())


def get_drivers(session_key: int) -> pd.DataFrame:
    """Fetch all drivers for a given session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/drivers",
        params={"session_key": session_key}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())


def get_race_results(session_key: int) -> pd.DataFrame:
    """Fetch final positions for a given session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/position",
        params={"session_key": session_key}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())

def get_driver_sessions(driver_number: int, session_key: int) -> pd.DataFrame:
    """Fetch driver data for a specific session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/drivers",
        params={
            "driver_number": driver_number,
            "session_key": session_key
        }
    )
    response.raise_for_status()
    data = response.json()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


def get_driver_positions(driver_number: int, session_key: int) -> pd.DataFrame:
    """Fetch position data for a specific driver in a session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/position",
        params={
            "driver_number": driver_number,
            "session_key": session_key
        }
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())

def get_qualifying_results(session_key: int) -> pd.DataFrame:
    """Fetch qualifying results (final positions) for a qualifying session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/position",
        params={"session_key": session_key}
    )
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    if df.empty:
        return df
    # Get final position per driver (last entry)
    final = df.sort_values("date").groupby("driver_number").last().reset_index()
    return final[["driver_number", "position"]].rename(columns={"position": "qualifying_position"})


def get_pit_stops(session_key: int) -> pd.DataFrame:
    """Fetch all pit stop data for a session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/pit",
        params={"session_key": session_key}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())


def get_race_control(session_key: int) -> pd.DataFrame:
    """Fetch race control messages (flags, safety cars) for a session."""
    response = requests.get(
        f"{OPENF1_BASE_URL}/race_control",
        params={"session_key": session_key}
    )
    response.raise_for_status()
    return pd.DataFrame(response.json())
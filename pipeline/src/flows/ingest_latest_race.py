import time
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta

from ingestion.openf1_client import (
    get_sessions,
    get_drivers,
    get_race_results,
    get_qualifying_results,
    get_pit_stops,
    get_race_control,
)
from database.connection import init_db
from database.repository import (
    save_sessions,
    save_drivers,
    save_race_results,
    save_qualifying_results,
    save_pit_stops,
    save_race_control,
)


SLEEP_BETWEEN_REQUESTS = 1


@task(retries=3, retry_delay_seconds=30)
def fetch_sessions(year: int):
    logger = get_run_logger()
    logger.info(f"Fetching sessions for {year}...")
    sessions = get_sessions(year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return sessions


@task(retries=3, retry_delay_seconds=30)
def fetch_and_save_drivers(session_key: int, year: int):
    drivers = get_drivers(session_key=session_key)
    save_drivers(drivers, session_key=session_key, year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return len(drivers)


@task(retries=3, retry_delay_seconds=30)
def fetch_and_save_results(session_key: int, year: int):
    results = get_race_results(session_key=session_key)
    save_race_results(results, session_key=session_key, year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return len(results)


@task(retries=3, retry_delay_seconds=30)
def fetch_and_save_qualifying(session_key: int, race_session_key: int, year: int):
    quali = get_qualifying_results(session_key=session_key)
    rows = save_qualifying_results(quali, session_key=race_session_key, year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return rows


@task(retries=3, retry_delay_seconds=30)
def fetch_and_save_pits(session_key: int, year: int):
    pits = get_pit_stops(session_key=session_key)
    rows = save_pit_stops(pits, session_key=session_key, year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return rows


@task(retries=3, retry_delay_seconds=30)
def fetch_and_save_race_control(session_key: int, year: int):
    control = get_race_control(session_key=session_key)
    rows = save_race_control(control, session_key=session_key, year=year)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    return rows


@flow(name="ingest-latest-race", log_prints=True)
def ingest_latest_race_flow(year: int = 2025):
    """Ingest the latest race data for a given season."""
    logger = get_run_logger()

    # Initialize database
    init_db()

    # Fetch all sessions for the year
    sessions = fetch_sessions(year)
    save_sessions(sessions, year=year)

    race_sessions = sessions[sessions["session_name"] == "Race"]
    quali_sessions = sessions[sessions["session_name"] == "Qualifying"]

    logger.info(f"Found {len(race_sessions)} races for {year}")

    for _, race in race_sessions.iterrows():
        session_key = int(race["session_key"])
        circuit = race["circuit_short_name"]

        try:
            fetch_and_save_drivers(session_key, year)
            fetch_and_save_results(session_key, year)
            pit_rows = fetch_and_save_pits(session_key, year)
            flag_rows = fetch_and_save_race_control(session_key, year)

            # Qualifying
            circuit_quali = quali_sessions[
                quali_sessions["circuit_short_name"] == circuit
            ]
            quali_rows = 0
            if not circuit_quali.empty:
                quali_key = int(circuit_quali.iloc[0]["session_key"])
                quali_rows = fetch_and_save_qualifying(quali_key, session_key, year)

            logger.info(f"{circuit} — pits: {pit_rows}, flags: {flag_rows}, quali: {quali_rows}")

        except Exception as e:
            logger.error(f"{circuit} — failed: {e}")

    logger.info("Pipeline complete.")


@flow(name="ingest-multi-season", log_prints=True)
def ingest_multi_season_flow(years: list[int] = [2023, 2024, 2025]):
    """Ingest data for multiple seasons."""
    logger = get_run_logger()
    for year in years:
        logger.info(f"Starting season {year}...")
        ingest_latest_race_flow(year=year)
    logger.info("All seasons ingested.")


if __name__ == "__main__":
    ingest_latest_race_flow()

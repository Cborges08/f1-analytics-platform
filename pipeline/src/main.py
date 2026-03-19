import time
from ingestion.openf1_client import (
    get_sessions,
    get_drivers,
    get_race_results,
    get_pit_stops,
    get_race_control
)
from database.connection import init_db
from database.repository import (
    save_sessions,
    save_drivers,
    save_race_results,
    save_pit_stops,
    save_race_control
)

TARGET_YEAR = 2025
SLEEP_BETWEEN_REQUESTS = 1
SLEEP_ON_RATE_LIMIT = 15
MAX_RETRIES = 3


def fetch_with_retry(fn, *args, **kwargs):
    """Call an API function with automatic retry on rate limit."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            result = fn(*args, **kwargs)
            time.sleep(SLEEP_BETWEEN_REQUESTS)
            return result
        except Exception as e:
            if "429" in str(e):
                print(f"      ⏳ Rate limit hit, waiting {SLEEP_ON_RATE_LIMIT}s (attempt {attempt}/{MAX_RETRIES})...")
                time.sleep(SLEEP_ON_RATE_LIMIT)
            else:
                raise e
    raise Exception(f"Failed after {MAX_RETRIES} retries")


def main():
    print("🏎️  F1 Analytics Pipeline starting...")
    print(f"   Season: {TARGET_YEAR}\n")

    # 1. Init database
    print("🗄️  Initializing database...")
    init_db()

    # 2. Fetch and save all sessions
    print("📅 Fetching sessions...")
    sessions = get_sessions(year=TARGET_YEAR)
    race_sessions = sessions[sessions["session_name"] == "Race"]
    saved = save_sessions(sessions, year=TARGET_YEAR)
    print(f"   ✅ {saved} sessions saved ({len(race_sessions)} races)\n")

    # 3. For each race — fetch all data
    print("🏁 Processing race data...")
    for _, race in race_sessions.iterrows():
        session_key = int(race["session_key"])
        circuit = race["circuit_short_name"]

        try:
            all_drivers = fetch_with_retry(get_drivers, session_key=session_key)
            save_drivers(all_drivers, session_key=session_key, year=TARGET_YEAR)

            results = fetch_with_retry(get_race_results, session_key=session_key)
            save_race_results(results, session_key=session_key, year=TARGET_YEAR)

            pits = fetch_with_retry(get_pit_stops, session_key=session_key)
            pit_rows = save_pit_stops(pits, session_key=session_key, year=TARGET_YEAR)

            control = fetch_with_retry(get_race_control, session_key=session_key)
            flag_rows = save_race_control(control, session_key=session_key, year=TARGET_YEAR)

            print(f"   ✅ {circuit} — pits: {pit_rows}, flags: {flag_rows}")

        except Exception as e:
            print(f"   ❌ {circuit} — failed after retries: {e}")

    print("\n✅ Pipeline complete.")


if __name__ == "__main__":
    main()
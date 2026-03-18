import time
from ingestion.openf1_client import (
    get_sessions,
    get_drivers,
    get_race_results
)
from database.connection import init_db
from database.repository import save_sessions, save_drivers, save_race_results

TARGET_YEAR = 2025


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

    # 3. For each race — fetch drivers and results
    print("🏁 Processing race results...")
    for _, race in race_sessions.iterrows():
        session_key = int(race["session_key"])
        circuit = race["circuit_short_name"]

        try:
            # All drivers in session
            all_drivers = get_drivers(session_key=session_key)
            save_drivers(all_drivers, session_key=session_key, year=TARGET_YEAR)

            # Race results (final positions)
            results = get_race_results(session_key=session_key)
            rows = save_race_results(results, session_key=session_key, year=TARGET_YEAR)

            print(f"   ✅ {circuit} — {rows} driver results saved")

        except Exception as e:
            print(f"   ⚠️  {circuit} — skipped: {e}")

        # Respect API rate limit
        time.sleep(1.5)

    print("\n✅ Pipeline complete. Data persisted to PostgreSQL.")


if __name__ == "__main__":
    main()
from ingestion.openf1_client import (
    get_sessions,
    get_driver_sessions,
    get_driver_positions
)

# Driver numbers — 2024 grid
DRIVERS = {
    "Verstappen": 1,
    "Leclerc": 16,
    "Hamilton": 44,
    "Norris": 4,
    "Sainz": 55,
}

TARGET_DRIVER = "Verstappen"
TARGET_YEAR = 2025


def main():
    print("🏎️  F1 Analytics Pipeline starting...")
    print(f"   Target: {TARGET_DRIVER} — {TARGET_YEAR} season\n")

    # 1. All sessions of the year
    print("📅 Fetching sessions...")
    sessions = get_sessions(year=TARGET_YEAR)
    race_sessions = sessions[sessions["session_name"] == "Race"]
    print(f"   ✅ {len(race_sessions)} race sessions found\n")

 # 2. Use last race session to get driver info
    last_race = race_sessions.iloc[-1]
    last_session_key = int(last_race["session_key"])
    circuit = last_race["circuit_short_name"]

    print(f"👤 Fetching {TARGET_DRIVER}'s data from last race: {circuit}...")
    driver_number = DRIVERS[TARGET_DRIVER]
    driver_data = get_driver_sessions(
        driver_number=driver_number,
        session_key=last_session_key
    )

    if driver_data.empty:
        print(f"   ⚠️  No data found for driver #{driver_number}")
        return

    print(f"   ✅ Driver found")
    print(f"   Team: {driver_data['team_name'].iloc[0]}")
    print(f"   Full name: {driver_data['full_name'].iloc[0]}\n")

    # 3. Position data from last race
    print(f"🏁 Fetching positions from: {circuit}...")
    positions = get_driver_positions(
        driver_number=driver_number,
        session_key=last_session_key
    )

    if not positions.empty:
        first_pos = positions.iloc[0]["position"]
        last_pos = positions.iloc[-1]["position"]
        print(f"   Started at position: {first_pos}")
        print(f"   Finished at position: {last_pos}")

    print("\n✅ Pipeline smoke test complete.")


if __name__ == "__main__":
    main()
const express = require("express");
const db = require("../db");
const router = express.Router();

// GET /api/predictions/features/:sessionKey
// Returns ML feature data for a given race session
router.get("/features/:sessionKey", async (req, res) => {
  try {
    const sessionKey = parseInt(req.params.sessionKey);
    const result = await db.query(
      `SELECT
        rr.driver_number,
        d.full_name as driver_name,
        d.name_acronym,
        d.team_name,
        s.circuit_short_name,
        rr.position as finish_position,
        CASE
          WHEN rr.position = 1 THEN 'WIN'
          WHEN rr.position <= 3 THEN 'PODIUM'
          WHEN rr.position <= 10 THEN 'POINTS'
          ELSE 'OUT_OF_POINTS'
        END as result_category,
        COALESCE(q.position, NULL) as qualifying_position,
        COALESCE(pit.total_stops, 0) as total_pit_stops,
        COALESCE(pit.avg_duration, 0) as avg_pit_duration,
        COALESCE(pit.fastest, 0) as fastest_pit,
        COALESCE(pit.total_time, 0) as total_pit_time,
        COALESCE(flags.yellow_flags, 0) as yellow_flags,
        COALESCE(flags.red_flags, 0) as red_flags,
        COALESCE(flags.safety_cars, 0) as safety_car_events,
        COALESCE(flags.vsc_events, 0) as vsc_events
      FROM race_results rr
      JOIN drivers d ON d.session_key = rr.session_key AND d.driver_number = rr.driver_number
      JOIN sessions s ON s.session_key = rr.session_key
      LEFT JOIN qualifying_results q ON q.session_key = rr.session_key AND q.driver_number = rr.driver_number
      LEFT JOIN (
        SELECT session_key, driver_number,
          COUNT(*) as total_stops,
          ROUND(AVG(pit_duration)::numeric, 3) as avg_duration,
          ROUND(MIN(pit_duration)::numeric, 3) as fastest,
          ROUND(SUM(pit_duration)::numeric, 3) as total_time
        FROM pit_stops
        WHERE pit_duration > 0 AND pit_duration < 120
        GROUP BY session_key, driver_number
      ) pit ON pit.session_key = rr.session_key AND pit.driver_number = rr.driver_number
      LEFT JOIN (
        SELECT session_key,
          COUNT(*) FILTER (WHERE flag = 'YELLOW') as yellow_flags,
          COUNT(*) FILTER (WHERE flag = 'RED') as red_flags,
          COUNT(*) FILTER (WHERE flag = 'SAFETY_CAR') as safety_cars,
          COUNT(*) FILTER (WHERE flag = 'VIRTUAL_SAFETY_CAR') as vsc_events
        FROM race_control_events
        GROUP BY session_key
      ) flags ON flags.session_key = rr.session_key
      WHERE rr.session_key = $1
      ORDER BY rr.position`,
      [sessionKey]
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/predictions/driver-form/:driverNumber?year=2025
// Returns rolling performance form for a driver
router.get("/driver-form/:driverNumber", async (req, res) => {
  try {
    const driverNumber = parseInt(req.params.driverNumber);
    const { year } = req.query;

    let query = `
      SELECT
        rr.session_key,
        s.circuit_short_name,
        s.date_start,
        rr.position,
        d.team_name,
        CASE
          WHEN rr.position = 1 THEN 'WIN'
          WHEN rr.position <= 3 THEN 'PODIUM'
          WHEN rr.position <= 10 THEN 'POINTS'
          ELSE 'OUT_OF_POINTS'
        END as result_category
      FROM race_results rr
      JOIN sessions s ON s.session_key = rr.session_key AND s.session_type = 'Race'
      JOIN drivers d ON d.session_key = rr.session_key AND d.driver_number = rr.driver_number
      WHERE rr.driver_number = $1
    `;
    const params = [driverNumber];
    if (year) {
      query += " AND rr.year = $2";
      params.push(parseInt(year));
    }
    query += " ORDER BY s.date_start";

    const result = await db.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

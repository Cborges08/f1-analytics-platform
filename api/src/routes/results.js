const express = require("express");
const db = require("../db");
const router = express.Router();

// GET /api/results/:sessionKey
router.get("/:sessionKey", async (req, res) => {
  try {
    const sessionKey = parseInt(req.params.sessionKey);
    const result = await db.query(
      `SELECT
        rr.driver_number,
        rr.position,
        d.full_name as driver_name,
        d.name_acronym,
        d.team_name,
        d.team_colour,
        s.circuit_short_name,
        s.country_name,
        s.date_start
      FROM race_results rr
      JOIN drivers d ON d.session_key = rr.session_key AND d.driver_number = rr.driver_number
      JOIN sessions s ON s.session_key = rr.session_key
      WHERE rr.session_key = $1
      ORDER BY rr.position ASC`,
      [sessionKey]
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/results/:sessionKey/pit-stops
router.get("/:sessionKey/pit-stops", async (req, res) => {
  try {
    const sessionKey = parseInt(req.params.sessionKey);
    const result = await db.query(
      `SELECT
        ps.driver_number,
        d.name_acronym,
        d.team_name,
        ps.lap_number,
        ps.pit_duration
      FROM pit_stops ps
      JOIN drivers d ON d.session_key = ps.session_key AND d.driver_number = ps.driver_number
      WHERE ps.session_key = $1
        AND ps.pit_duration > 0
        AND ps.pit_duration < 120
      ORDER BY ps.lap_number, ps.driver_number`,
      [sessionKey]
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/results/:sessionKey/incidents
router.get("/:sessionKey/incidents", async (req, res) => {
  try {
    const sessionKey = parseInt(req.params.sessionKey);
    const result = await db.query(
      `SELECT lap_number, flag, category, message, date
      FROM race_control_events
      WHERE session_key = $1
        AND flag IN ('YELLOW', 'DOUBLE_YELLOW', 'RED')
      ORDER BY date`,
      [sessionKey]
    );
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

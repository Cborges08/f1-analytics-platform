const express = require("express");
const db = require("../db");
const router = express.Router();

const POINTS_SYSTEM = {
  1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
  6: 8, 7: 6, 8: 4, 9: 2, 10: 1,
};

// GET /api/standings/drivers?year=2025
router.get("/drivers", async (req, res) => {
  try {
    const year = parseInt(req.query.year) || 2025;
    const result = await db.query(
      `SELECT
        rr.driver_number,
        d.full_name as driver_name,
        d.name_acronym,
        d.team_name,
        d.team_colour,
        d.headshot_url,
        COUNT(rr.id) as races,
        COUNT(*) FILTER (WHERE rr.position = 1) as wins,
        COUNT(*) FILTER (WHERE rr.position <= 3) as podiums,
        ROUND(AVG(rr.position), 1) as avg_position,
        MIN(rr.position) as best_finish,
        json_agg(json_build_object(
          'session_key', rr.session_key,
          'position', rr.position,
          'circuit', s.circuit_short_name
        ) ORDER BY s.date_start) as race_history
      FROM race_results rr
      JOIN sessions s ON s.session_key = rr.session_key AND s.session_type = 'Race'
      JOIN drivers d ON d.session_key = rr.session_key AND d.driver_number = rr.driver_number
      WHERE rr.year = $1
      GROUP BY rr.driver_number, d.full_name, d.name_acronym, d.team_name, d.team_colour, d.headshot_url
      ORDER BY avg_position ASC`,
      [year]
    );

    // Calculate points
    const standings = result.rows.map((driver) => {
      let points = 0;
      for (const race of driver.race_history) {
        points += POINTS_SYSTEM[race.position] || 0;
      }
      return { ...driver, points };
    });

    standings.sort((a, b) => b.points - a.points);
    res.json(standings);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/standings/constructors?year=2025
router.get("/constructors", async (req, res) => {
  try {
    const year = parseInt(req.query.year) || 2025;
    const result = await db.query(
      `SELECT
        d.team_name,
        d.team_colour,
        COUNT(DISTINCT rr.driver_number) as drivers,
        COUNT(rr.id) as total_races,
        COUNT(*) FILTER (WHERE rr.position = 1) as wins,
        COUNT(*) FILTER (WHERE rr.position <= 3) as podiums,
        ROUND(AVG(rr.position), 1) as avg_position,
        json_agg(json_build_object(
          'position', rr.position,
          'driver_number', rr.driver_number
        )) as all_results
      FROM race_results rr
      JOIN sessions s ON s.session_key = rr.session_key AND s.session_type = 'Race'
      JOIN drivers d ON d.session_key = rr.session_key AND d.driver_number = rr.driver_number
      WHERE rr.year = $1
      GROUP BY d.team_name, d.team_colour
      ORDER BY avg_position ASC`,
      [year]
    );

    const standings = result.rows.map((team) => {
      let points = 0;
      for (const r of team.all_results) {
        points += POINTS_SYSTEM[r.position] || 0;
      }
      return { ...team, points };
    });

    standings.sort((a, b) => b.points - a.points);
    res.json(standings);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

const express = require("express");
const db = require("../db");
const router = express.Router();

// GET /api/drivers?year=2025
router.get("/", async (req, res) => {
  try {
    const { year } = req.query;
    let query = `
      SELECT DISTINCT ON (driver_number, year)
        driver_number, full_name, name_acronym,
        team_name, country_code, headshot_url, year
      FROM drivers
    `;
    const params = [];
    if (year) {
      query += " WHERE year = $1";
      params.push(parseInt(year));
    }
    query += " ORDER BY driver_number, year, created_at DESC";

    const result = await db.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/drivers/:number/stats?year=2025
router.get("/:number/stats", async (req, res) => {
  try {
    const driverNumber = parseInt(req.params.number);
    const { year } = req.query;

    let query = `
      SELECT
        d.full_name,
        d.name_acronym,
        d.team_name,
        COUNT(rr.id) as races,
        ROUND(AVG(rr.position), 1) as avg_position,
        MIN(rr.position) as best_finish,
        COUNT(*) FILTER (WHERE rr.position = 1) as wins,
        COUNT(*) FILTER (WHERE rr.position <= 3) as podiums,
        COUNT(*) FILTER (WHERE rr.position <= 10) as points_finishes
      FROM race_results rr
      JOIN drivers d ON d.driver_number = rr.driver_number AND d.year = rr.year
      WHERE rr.driver_number = $1
    `;
    const params = [driverNumber];
    if (year) {
      query += " AND rr.year = $2";
      params.push(parseInt(year));
    }
    query += " GROUP BY d.full_name, d.name_acronym, d.team_name";

    const result = await db.query(query, params);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Driver not found" });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

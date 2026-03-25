const express = require("express");
const db = require("../db");
const router = express.Router();

// GET /api/sessions?year=2025
router.get("/", async (req, res) => {
  try {
    const { year } = req.query;
    let query = `
      SELECT session_key, session_name, session_type, date_start,
             circuit_short_name, country_name, location, year
      FROM sessions
    `;
    const params = [];
    if (year) {
      query += " WHERE year = $1";
      params.push(parseInt(year));
    }
    query += " ORDER BY date_start DESC";

    const result = await db.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/sessions/races?year=2025
router.get("/races", async (req, res) => {
  try {
    const { year } = req.query;
    let query = `
      SELECT session_key, session_name, date_start,
             circuit_short_name, country_name, location, year
      FROM sessions
      WHERE session_type = 'Race'
    `;
    const params = [];
    if (year) {
      query += " AND year = $1";
      params.push(parseInt(year));
    }
    query += " ORDER BY date_start DESC";

    const result = await db.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;

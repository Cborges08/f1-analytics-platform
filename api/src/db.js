const { Pool } = require("pg");

const pool = new Pool({
  host: process.env.POSTGRES_HOST || "localhost",
  port: parseInt(process.env.POSTGRES_PORT || "5432"),
  database: process.env.POSTGRES_DB || "f1_analytics",
  user: process.env.POSTGRES_USER || "f1_user",
  password: process.env.POSTGRES_PASSWORD || "",
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  pool,
};

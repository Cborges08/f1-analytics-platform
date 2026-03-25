const express = require("express");
const cors = require("cors");
require("dotenv").config({ path: "../.env" });

const db = require("./db");
const sessionsRouter = require("./routes/sessions");
const driversRouter = require("./routes/drivers");
const resultsRouter = require("./routes/results");
const predictionsRouter = require("./routes/predictions");
const standingsRouter = require("./routes/standings");

const app = express();
const PORT = process.env.API_PORT || 3001;

app.use(cors());
app.use(express.json());

// Health check
app.get("/api/health", async (req, res) => {
  try {
    await db.query("SELECT 1");
    res.json({ status: "healthy", timestamp: new Date().toISOString() });
  } catch (err) {
    res.status(503).json({ status: "unhealthy", error: err.message });
  }
});

// Routes
app.use("/api/sessions", sessionsRouter);
app.use("/api/drivers", driversRouter);
app.use("/api/results", resultsRouter);
app.use("/api/predictions", predictionsRouter);
app.use("/api/standings", standingsRouter);

app.listen(PORT, () => {
  console.log(`F1 Analytics API running on port ${PORT}`);
});

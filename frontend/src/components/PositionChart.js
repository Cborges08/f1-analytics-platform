"use client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#e10600", "#0090ff", "#ff8700", "#00d2be",
  "#006f62", "#2b4562", "#b6babd", "#5e8faa",
  "#900000", "#005aff",
];

export default function PositionChart({ standings }) {
  if (!standings || standings.length === 0) return null;

  // Build chart data: one entry per race, showing cumulative points
  const topDrivers = standings.slice(0, 6);
  const raceCount = topDrivers[0]?.race_history?.length || 0;
  if (raceCount === 0) return null;

  const POINTS_MAP = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1,
  };

  const chartData = [];
  for (let i = 0; i < raceCount; i++) {
    const entry = { race: topDrivers[0].race_history[i]?.circuit || `R${i + 1}` };
    for (const driver of topDrivers) {
      let cumulative = 0;
      for (let j = 0; j <= i; j++) {
        cumulative += POINTS_MAP[driver.race_history[j]?.position] || 0;
      }
      entry[driver.name_acronym] = cumulative;
    }
    chartData.push(entry);
  }

  return (
    <div className="chart-container">
      <div className="chart-title">Championship Points Progression</div>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="race"
            tick={{ fill: "#fff", fontSize: 11 }}
            angle={-45}
            textAnchor="end"
            height={60}
          />
          <YAxis tick={{ fill: "#fff", fontSize: 11 }} />
          <Tooltip
            contentStyle={{ background: "#38383f", border: "none", borderRadius: 8 }}
            labelStyle={{ color: "#fff" }}
          />
          {topDrivers.map((driver, i) => (
            <Line
              key={driver.name_acronym}
              type="monotone"
              dataKey={driver.name_acronym}
              stroke={`#${driver.team_colour || COLORS[i].slice(1)}`}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

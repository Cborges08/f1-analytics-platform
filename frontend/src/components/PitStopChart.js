"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function PitStopChart({ pitStops }) {
  if (!pitStops || pitStops.length === 0) return null;

  // Average pit time per driver
  const byDriver = {};
  for (const ps of pitStops) {
    if (!byDriver[ps.name_acronym]) {
      byDriver[ps.name_acronym] = { total: 0, count: 0, team: ps.team_name };
    }
    byDriver[ps.name_acronym].total += parseFloat(ps.pit_duration);
    byDriver[ps.name_acronym].count += 1;
  }

  const chartData = Object.entries(byDriver)
    .map(([name, data]) => ({
      driver: name,
      avg_duration: parseFloat((data.total / data.count).toFixed(2)),
      stops: data.count,
    }))
    .sort((a, b) => a.avg_duration - b.avg_duration);

  return (
    <div className="chart-container">
      <div className="chart-title">Average Pit Stop Duration (s)</div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis type="number" tick={{ fill: "#fff", fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="driver"
            tick={{ fill: "#fff", fontSize: 11 }}
            width={50}
          />
          <Tooltip
            contentStyle={{ background: "#38383f", border: "none", borderRadius: 8 }}
            labelStyle={{ color: "#fff" }}
          />
          <Bar dataKey="avg_duration" fill="#e10600" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

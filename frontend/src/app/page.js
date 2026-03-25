"use client";

import { useEffect, useState } from "react";
import Nav from "@/components/Nav";
import StandingsTable from "@/components/StandingsTable";
import { getDriverStandings, getRaces } from "@/lib/api";

export default function Home() {
  const [standings, setStandings] = useState(null);
  const [races, setRaces] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [standingsData, racesData] = await Promise.all([
          getDriverStandings(2025),
          getRaces(2025),
        ]);
        setStandings(standingsData);
        setRaces(racesData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <main className="min-h-screen bg-gray-900 text-white">
      <Nav />

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">🏎️ F1 Analytics Dashboard</h1>

        {error && (
          <div className="bg-red-600 p-4 rounded mb-8">
            <p>Error loading data: {error}</p>
            <p className="text-sm mt-2">Make sure the API is running on port 3001</p>
          </div>
        )}

        {loading && (
          <div className="text-center py-12">
            <p className="text-xl">Loading race data...</p>
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h2 className="text-2xl font-bold mb-4">Driver Standings</h2>
              {standings ? (
                <StandingsTable standings={standings} />
              ) : (
                <p>No standings data available</p>
              )}
            </div>

            <div>
              <h2 className="text-2xl font-bold mb-4">2025 Season</h2>
              {races && races.length > 0 ? (
                <div className="space-y-2">
                  <p className="text-gray-400">{races.length} races scheduled</p>
                  <ul className="space-y-1">
                    {races.slice(0, 5).map((race, i) => (
                      <li key={i} className="text-sm text-gray-300">
                        • {race.circuit_name || race.location || "TBA"}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p>No race data available</p>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

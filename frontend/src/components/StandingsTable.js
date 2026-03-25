"use client";

export default function StandingsTable({ standings }) {
  if (!standings || standings.length === 0) {
    return <div className="loading">No standings data available</div>;
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Pos</th>
            <th>Driver</th>
            <th>Team</th>
            <th>Points</th>
            <th>Wins</th>
            <th>Podiums</th>
            <th>Avg Pos</th>
          </tr>
        </thead>
        <tbody>
          {standings.map((driver, i) => (
            <tr key={driver.driver_number}>
              <td>
                <span className={`pos ${i < 3 ? `pos-${i + 1}` : i < 10 ? "pos-points" : ""}`}>
                  {i + 1}
                </span>
              </td>
              <td>
                <span
                  className="team-stripe"
                  style={{ backgroundColor: `#${driver.team_colour || "fff"}` }}
                />
                <strong>{driver.name_acronym}</strong>{" "}
                <span style={{ opacity: 0.6 }}>{driver.driver_name}</span>
              </td>
              <td>{driver.team_name}</td>
              <td><strong>{driver.points}</strong></td>
              <td>{driver.wins}</td>
              <td>{driver.podiums}</td>
              <td>{driver.avg_position}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

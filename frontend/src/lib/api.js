const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api";

async function fetchApi(path) {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getDriverStandings(year = 2025) {
  return fetchApi(`/standings/drivers?year=${year}`);
}

export async function getConstructorStandings(year = 2025) {
  return fetchApi(`/standings/constructors?year=${year}`);
}

export async function getRaces(year = 2025) {
  return fetchApi(`/sessions/races?year=${year}`);
}

export async function getRaceResults(sessionKey) {
  return fetchApi(`/results/${sessionKey}`);
}

export async function getRacePitStops(sessionKey) {
  return fetchApi(`/results/${sessionKey}/pit-stops`);
}

export async function getDrivers(year = 2025) {
  return fetchApi(`/drivers?year=${year}`);
}

export async function getDriverStats(driverNumber, year = 2025) {
  return fetchApi(`/drivers/${driverNumber}/stats?year=${year}`);
}

export async function getDriverForm(driverNumber, year = 2025) {
  return fetchApi(`/predictions/driver-form/${driverNumber}?year=${year}`);
}

export async function getPredictionFeatures(sessionKey) {
  return fetchApi(`/predictions/features/${sessionKey}`);
}

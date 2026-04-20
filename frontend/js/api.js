// Single source of truth for the backend URL
const API_BASE = "http://localhost:8000";

// Fetch all markers from the backend
async function fetchMarkers() {
  const res = await fetch(`${API_BASE}/data`);
  if (!res.ok) throw new Error(`Failed to fetch markers: ${res.status} ${res.statusText}`);
  return res.json();
}

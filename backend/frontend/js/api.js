// Dynamically use the origin the page was served from — works locally and on Render
const API_BASE = window.location.origin;

// Fetch all markers from the backend
async function fetchMarkers() {
  const res = await fetch(`${API_BASE}/data`);
  if (!res.ok) throw new Error(`Failed to fetch markers: ${res.status} ${res.statusText}`);
  return res.json();
}

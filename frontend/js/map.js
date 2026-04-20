// Initialize map centered on India
const map = L.map("map").setView([20.5937, 78.9629], 5);

// OpenStreetMap tile layer — no API key required
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19,
}).addTo(map);

// Color assigned to each intelligence type
const TYPE_COLORS = {
  OSINT:  "#3b82f6",  // blue
  HUMINT: "#f59e0b",  // amber
  IMINT:  "#10b981",  // green
};

// Custom circular div icon colored by type
function makeIcon(type) {
  const color = TYPE_COLORS[type] || "#e94560";
  return L.divIcon({
    className: "",
    html: `<span class="marker-dot" style="background:${color};box-shadow:0 0 6px ${color};"></span>`,
    iconSize:   [16, 16],
    iconAnchor: [8, 8],
    popupAnchor:[0, -10],
  });
}

// Build hover popup content; includes image if file_url is present
function buildPopupHTML({ type, description, file_url }) {
  const color = TYPE_COLORS[type] || "#e94560";
  const img = file_url
    ? `<img src="${API_BASE}/${file_url}" alt="image"
         style="margin-top:6px;max-width:180px;max-height:120px;border-radius:4px;display:block;">`
    : "";
  return `
    <strong style="font-size:0.9rem;color:${color};">${type}</strong>
    <p style="margin:4px 0 0;font-size:0.8rem;max-width:180px;">${description}</p>
    ${img}
  `;
}

// Single layer group — all markers live here so they can be cleared at once
const markerLayer = L.layerGroup().addTo(map);

// Clear all existing dots, then draw the new list
function renderMarkers(markers) {
  markerLayer.clearLayers();
  markers.forEach((marker) => {
    const popup = L.popup({ closeButton: false, offset: L.point(0, -10) })
      .setContent(buildPopupHTML(marker));

    L.marker([marker.lat, marker.lon], { icon: makeIcon(marker.type) })
      .bindPopup(popup)
      .on("mouseover", function () { this.openPopup(); })
      .on("mouseout",  function () { this.closePopup(); })
      .addTo(markerLayer);
  });
}

// Fetch full marker list from API and re-render the map
function reloadMarkers() {
  return fetchMarkers()
    .then(renderMarkers)
    .catch((err) => console.error("Could not load markers:", err));
}

// Load markers from API on page load
reloadMarkers();

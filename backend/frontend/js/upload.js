const dropZone  = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const dropLabel = document.getElementById("dropLabel");
const statusSpan = document.getElementById("uploadStatus");

function setStatus(msg, color) {
  statusSpan.textContent = msg;
  statusSpan.style.color = color;
}

// ── Drag-and-drop events ────────────────────────────────────────────────────

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

["dragleave", "dragend"].forEach((evt) =>
  dropZone.addEventListener(evt, () => dropZone.classList.remove("drag-over"))
);

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
});

// ── Browse (click) fallback ─────────────────────────────────────────────────

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) uploadFile(fileInput.files[0]);
});

// ── Core upload function ────────────────────────────────────────────────────

async function uploadFile(file) {
  dropLabel.textContent = file.name;
  setStatus("Uploading…", "#facc15");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res  = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Upload failed");

    const count = data.markers_parsed != null ? ` — ${data.markers_parsed} markers loaded` : "";
    setStatus(`Uploaded successfully${count}.`, "#4ade80");

    // Refetch the full marker list so the map shows fresh data only
    reloadMarkers();

    fileInput.value = "";
    setTimeout(() => { dropLabel.textContent = "Drag & drop a file here"; }, 3000);
  } catch (err) {
    console.error("Upload error:", err);
    setStatus(`Error: ${err.message}`, "#f87171");
    dropLabel.textContent = "Drag & drop a file here";
  }
}

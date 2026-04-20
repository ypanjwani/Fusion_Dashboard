"""Run once to generate data/sample_data.xlsx for testing."""
import openpyxl
from pathlib import Path

rows = [
    ("lat", "lon", "type", "description"),
    (28.61, 77.20, "OSINT",  "Social media spike in New Delhi."),
    (19.07, 72.87, "HUMINT", "Agent report near Mumbai port."),
    (13.08, 80.27, "IMINT",  "New construction detected in Chennai."),
    (22.57, 88.36, "OSINT",  "Dark web chatter near Kolkata."),
    (17.38, 78.48, "HUMINT", "Meeting confirmed in Hyderabad."),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Markers"
for row in rows:
    ws.append(row)

out = Path(__file__).parent / "sample_data.xlsx"
wb.save(out)
print(f"Saved: {out}")

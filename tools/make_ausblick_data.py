"""Erzeugt die Excel-Beispieldaten für die Ausblick-Notebooks (15 Excel, 17 ML).

Alle Werte sind simuliert, mit festem Startwert für den Zufall, damit jeder Lauf
dieselben Zahlen liefert:

- ``daten/umsatz_filialen.xlsx``: Umsatzbericht, wie er aus einer Fachabteilung
  kommt: Titel und Stand über der Tabelle, Gesamtzeile darunter, zweites Blatt
  mit Jahreszielen als saubere Tabelle.
- ``daten/schweissprotokoll.csv``: Protokoll eines Schweißroboters mit
  Prozesswerten je Naht und Prüfergebnis, im deutschen CSV-Format (Semikolon,
  Dezimalkomma), wie es eine Anlage oder Excel exportiert. Roboter R3 driftet
  über die Wochen zu höherem Strom.

Aufruf: ``uv run python tools/make_ausblick_data.py``
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "daten"
SEED = 2026

BRANCHES = [
    ("Köln", "NRW", 182_000),
    ("Bonn", "NRW", 96_000),
    ("Düsseldorf", "NRW", 154_000),
    ("Siegen", "NRW", 61_000),
    ("Frankfurt", "Hessen", 171_000),
    ("Wetzlar", "Hessen", 58_000),
    ("Gießen", "Hessen", 66_000),
    ("Mainz", "Rheinland-Pfalz", 89_000),
]
MONTHS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep"]


def make_sales(rng: random.Random) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Umsatz 2026"
    ws["A1"] = "Umsatzbericht 2026 nach Filialen"
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(MONTHS) + 3)
    ws["A2"] = "Stand: 30.09.2026, Beträge in Euro, Werte simuliert"
    ws.append([])
    header = ["Filiale", "Region", *MONTHS, "Summe"]
    ws.append(header)
    for cell in ws[4]:
        cell.font = Font(bold=True)

    totals = [0] * (len(MONTHS) + 1)
    for name, region, base in BRANCHES:
        season = [0.85, 0.9, 1.0, 1.0, 1.05, 1.0, 0.95, 0.9, 1.1]
        values = [round(base * factor * rng.uniform(0.9, 1.1)) for factor in season]
        values.append(sum(values))
        ws.append([name, region, *values])
        totals = [total + value for total, value in zip(totals, values)]
    ws.append([])
    ws.append(["Gesamt", None, *totals])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 16

    targets = wb.create_sheet("Ziele")
    targets.append(["Filiale", "Jahresziel"])
    for name, _, base in BRANCHES:
        targets.append([name, round(base * 12 * 1.02, -3)])

    wb.save(DATA_DIR / "umsatz_filialen.xlsx")


def german(number: float) -> str:
    return str(number).replace(".", ",")


def make_welding_log(rng: random.Random) -> None:
    rows = [["Zeitpunkt", "Naht", "Roboter", "Strom_A", "Spannung_V",
             "Drahtvorschub_m_min", "Geschwindigkeit_cm_min", "Ergebnis"]]
    start = datetime(2026, 9, 1, 6, 0)
    count = 600
    for number in range(1, count + 1):
        moment = start + timedelta(minutes=round(number * 50.4))
        robot = rng.choice(["R1", "R2", "R3"])
        drift = 40 * number / count if robot == "R3" else 0
        current = rng.gauss(215, 22) + drift
        voltage = 14 + 0.045 * current + rng.gauss(0, 0.6)
        wire_feed = current / 30 + rng.gauss(0, 0.3)
        speed = rng.gauss(45, 7)
        heat_input = voltage * current * 60 / (1000 * speed)  # kJ/cm
        in_window = 5.5 <= heat_input <= 8.5
        failed = rng.random() < (0.03 if in_window else 0.85)
        rows.append([
            f"{moment:%d.%m.%Y %H:%M}",
            f"N-{number:04d}",
            robot,
            german(round(current, 1)),
            german(round(voltage, 1)),
            german(round(wire_feed, 2)),
            german(round(speed, 1)),
            "nicht ok" if failed else "ok",
        ])

    with open(DATA_DIR / "schweissprotokoll.csv", "w", encoding="utf-8",
              newline="") as file:
        csv.writer(file, delimiter=";").writerows(rows)


def main() -> None:
    rng = random.Random(SEED)
    make_sales(rng)
    make_welding_log(rng)
    print("geschrieben: umsatz_filialen.xlsx, schweissprotokoll.csv")


if __name__ == "__main__":
    main()

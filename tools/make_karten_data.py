"""Erzeugt die Kartendaten für Notebook 17 aus zwei amtlichen Quellen.

Quellen (vorher herunterladen, Pfade als Argumente übergeben):

- Verwaltungsgebiete 1:2 500 000 (VG2500, Stand 31.12.2024), ZIP mit Shapefiles:
  https://daten.gdz.bkg.bund.de/produkte/vg/vg2500/2024/vg2500_12-31.utm32s.shape.zip,
  Lizenz Datenlizenz Deutschland – Namensnennung – 2.0, Quellenvermerk laut
  Nutzungsbedingungen im ZIP: "© BKG (2026) dl-de/by-2-0 (Daten verändert), Datenquellen:
  https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf".
  Verändert: nur die Kreise, nur Schlüssel, Name und Art, als GeoPackage gespeichert.
- Gemeindeverzeichnis, Kreisfreie Städte und Landkreise nach Fläche und Bevölkerung
  (31.12.2024), ``04-kreise.xlsx``:
  https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.xlsx,
  Quellenvermerk "© Statistisches Bundesamt (Destatis), 2025".

Ergebnis in ``daten/``:

- ``kreise.gpkg``: Umrisse der Kreise, Koordinaten unverändert in Metern (EPSG:25832).
  Die Länder entstehen im Notebook aus den Kreisen.
- ``kreise_bevoelkerung.csv``: Bundesland, Fläche und Einwohner je Kreis, deutsches CSV-Format.
- ``filialen.csv``: Lage der Filialen aus ``umsatz_filialen.xlsx`` (Stadtmitte).

Aufruf: ``uv run python tools/make_karten_data.py <vg2500.zip> <04-kreise.xlsx>``
"""

import csv
import sys
import zipfile
from pathlib import Path

import geopandas as gpd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "daten"

BRANCHES = [
    ("Köln", 50.9375, 6.9603),
    ("Bonn", 50.7374, 7.0982),
    ("Düsseldorf", 51.2277, 6.7735),
    ("Siegen", 50.8748, 8.0243),
    ("Frankfurt", 50.1109, 8.6821),
    ("Wetzlar", 50.5558, 8.5049),
    ("Gießen", 50.5841, 8.6784),
    ("Mainz", 49.9929, 8.2473),
]


def read_districts(zip_path: Path) -> gpd.GeoDataFrame:
    with zipfile.ZipFile(zip_path) as archive:
        name = next(n for n in archive.namelist() if n.endswith("VG2500_KRS.shp"))
    districts = gpd.read_file(f"zip://{zip_path}!{name}")
    columns = {"ARS": "Schluessel", "GEN": "Kreis", "BEZ": "Art"}
    return districts[[*columns, "geometry"]].rename(columns=columns)


def write_population(xlsx_path: Path, keys: set[str]) -> None:
    ws = load_workbook(xlsx_path, read_only=True)["Kreisfreie Städte u. Landkreise"]
    rows = []
    state = None
    for row in ws.iter_rows(min_row=3, values_only=True):
        key, label, name, _, area, population = row[:6]
        # Zeilen mit zweistelligem Schlüssel sind Überschriften der Länder
        if isinstance(key, str) and len(key) == 2:
            state = label
        if isinstance(key, str) and len(key) == 5 and population is not None:
            rows.append([key, name, state, f"{area:.2f}".replace(".", ","), population])
    missing = keys - {row[0] for row in rows}
    if missing:
        raise SystemExit(f"Kreise ohne Bevölkerung: {sorted(missing)}")
    with open(DATA_DIR / "kreise_bevoelkerung.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(["Schluessel", "Kreis", "Bundesland", "Flaeche_km2", "Einwohner"])
        writer.writerows(rows)


def write_branches() -> None:
    with open(DATA_DIR / "filialen.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";", lineterminator="\n")
        writer.writerow(["Filiale", "Breite", "Laenge"])
        for name, lat, lon in BRANCHES:
            writer.writerow([name, str(lat).replace(".", ","), str(lon).replace(".", ",")])


def main() -> None:
    zip_path, xlsx_path = map(Path, sys.argv[1:3])
    districts = read_districts(zip_path)
    # Polygon bleibt Polygon; nur Kreise mit Inseln sind MultiPolygon wie im Original
    districts.to_file(DATA_DIR / "kreise.gpkg", driver="GPKG", promote_to_multi=False)
    write_population(xlsx_path, set(districts["Schluessel"]))
    write_branches()


if __name__ == "__main__":
    main()

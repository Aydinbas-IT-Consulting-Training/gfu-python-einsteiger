# Python für Programmier-Anfänger (GFU s2099)

Kursmaterial zur GFU-Schulung [Python für Programmier-Anfänger](https://www.gfu.net/s2099).
Begleitbuch: Michael Inden, *Einstieg in Python*, 2. Auflage, dpunkt 2024.

## Einrichtung

1. [uv installieren](https://docs.astral.sh/uv/getting-started/installation/)
2. Repository herunterladen und im Ordner ausführen:

   ```bash
   uv sync
   ```

3. [VS Code](https://code.visualstudio.com/) mit den Erweiterungen **Python** und **Jupyter** installieren.
4. Ordner in VS Code öffnen, ein Notebook aus `notebooks/` öffnen und oben rechts den Kernel `.venv` auswählen.

Skripte startest du im Terminal mit `uv run python projekte/tictactoe.py`.

## Inhalt

| Nr. | Notebook | Buchkapitel |
| --- | --- | --- |
| 00 | Einführung, Setup, Stil (PEP 8) | 1, 2 |
| 01 | Variablen und Datentypen | 2 |
| 02 | Python unter der Haube | – |
| 03 | Operatoren und Bedingungen | 2, 6 |
| 04 | Schleifen | 2 |
| 05 | Strings | 3 |
| 06 | Collections, mutable vs. immutable | 5, 8 |
| 07 | Funktionen | 6, 16 |
| 08 | Module und Pakete | 6 |
| 09 | Fehlerbehandlung | 9 |
| 10 | Dateien | 7 |
| 11 | Klassen und Objekte | 4 |
| 12 | Abschlussprojekt Tic-Tac-Toe | 13 |

## Ordner

```
notebooks/   Notebooks für Teilnehmende, Übungen leer
loesungen/   dieselben Notebooks mit Lösungen
daten/       Beispieldateien (daten/ausgabe/ entsteht beim Arbeiten)
projekte/    lauffähige Skripte
beispiele/   Module und Pakete für Notebook 08
tools/       Hilfsskripte für die Pflege des Materials
```

## Material pflegen

Die Notebooks in `loesungen/` sind die Quelle. Lösungszellen tragen den Tag `solution`,
Zellen mit absichtlichem Fehler den Tag `raises-exception`.

```bash
uv run python tools/check_notebooks.py   # alle Lösungen ausführen
uv run python tools/make_exercises.py    # notebooks/ aus loesungen/ erzeugen
```

Codebeispiele teilweise nach Inden, *Einstieg in Python*, überarbeitet.
`daten/faust.txt` stammt von Project Gutenberg.

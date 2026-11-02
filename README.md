# Python für Programmier-Anfänger (GFU s2099)

Kursmaterial zur GFU-Schulung [Python für Programmier-Anfänger](https://www.gfu.net/s2099).
Begleitbuch: Michael Inden, *Einstieg in Python*, 2. Auflage, dpunkt 2024.

## Einrichtung

1. [uv installieren](https://docs.astral.sh/uv/getting-started/installation/)
2. [VS Code](https://code.visualstudio.com/) mit den Erweiterungen **Python**, **Jupyter** und **Ruff** installieren.
3. Repository herunterladen, auf einem der beiden Wege:
   - ohne Git: auf der GitHub-Seite des Repositorys *Code → Download ZIP* wählen und die ZIP-Datei entpacken,
   - mit Git:

     ```bash
     git clone https://github.com/Aydinbas-IT-Consulting-Training/gfu-python-einsteiger.git
     ```

4. Den Ordner in VS Code öffnen (*Datei → Ordner öffnen*) und dort ein Terminal öffnen: Menü *Terminal → Neues Terminal*, auf einer deutschen Tastatur auch `Strg + ö`. Das Terminal startet im Kursordner. Dort ausführen:

   ```bash
   uv sync
   ```

5. Ein Notebook aus `notebooks/` öffnen und oben rechts den Kernel `.venv` auswählen.

Skripte startest du im Terminal mit `uv run python projekte/tictactoe.py`.

## Inhalt

| Nr. | Notebook | Buchkapitel |
| --- | --- | --- |
| 00 | Einführung, Setup, Stil (PEP 8) | 1, 2 |
| 01 | Variablen und Datentypen | 2 |
| 02 | Python unter der Haube (optional) | – |
| 03 | Operatoren und Bedingungen | 2, 6 |
| 04 | Schleifen | 2, 6 |
| 05 | Strings | 3 |
| 06 | Collections, mutable vs. immutable | 5, 8 |
| 07 | Funktionen | 2, 6, 16 |
| 08 | Module und Pakete | 2, 6 |
| 09 | Fehlerbehandlung | 2, 9 |
| 10 | Dateien | 7, 14 |
| 11 | Datum und Zeit | 10 |
| 12 | Klassen und Objekte (optional) | 4, 6 |
| 13 | Testen mit pytest (Ordner `testen/`, Bonus) | 16 |
| 14 | Abschlussprojekt Tic-Tac-Toe | 13, 16 |

00 bis 07 sind der Kern des Kurses und werden vollständig behandelt. Ab 08 wählen wir im Kurs aus; was offen bleibt, eignet sich zum Weiterlernen nach dem Kurs. Klassen (12) und Tests (13, Schritt 6 im Abschlussprojekt) sind ein Ausblick.

Welche Übungen wir im Kurs gemeinsam machen, entscheiden wir vor Ort; meist sind es die Kurzübungen in den Abschnitten und die leichten Übungen am Ende eines Notebooks, manche schwere führe ich vor. Die übrigen mittleren und schweren Übungen sind zum Vertiefen gedacht: für alle, die schneller fertig sind, und für die Zeit nach dem Kurs. Lösungen liegen im Ordner `loesungen/`.

### Lesepfad zum Buch

Die Notebooks folgen weitgehend der Reihenfolge des Buchs. Vier Abweichungen:

- **Kapitel 2 (Schnelleinstieg)** ist auf mehrere Notebooks verteilt: 01 Variablen, 03 Bedingungen, 04 Schleifen.
- **Kapitel 4 (Klassen)** lesen wir erst spät (Notebook 12), weil Klassen Funktionen voraussetzen.
- **Kapitel 9 (Fehlerbehandlung)** ziehen wir vor Kapitel 7 (Dateien), weil wir `try` und `with` beim Arbeiten mit Dateien brauchen.
- **Kapitel 16 (Testen)** kommt vor dem Abschlussprojekt, damit wir dessen Spiellogik mit Tests absichern.

Zum Mitlesen also die Buchkapitel in dieser Reihenfolge: Kapitel 1 → 2 → 3 → 5 → 6 → 8 → 9 → 7 → 14 → 10 → 4 → 16 → 13.

Teil 13 ist kein Notebook, sondern ein Ordner mit echten Testdateien. Wie du ihn durcharbeitest, steht in `testen/README.md`.

## Ordner

```
notebooks/   Notebooks für Teilnehmende, Übungen leer
loesungen/   dieselben Notebooks mit Lösungen
daten/       Beispieldateien (daten/ausgabe/ entsteht beim Arbeiten)
projekte/    lauffähige Skripte
testen/      Einstieg in pytest: Modul, Testdateien, Übungen
beispiele/   Module und Pakete für Notebook 08
assets/      Grafiken der Notebooks (draw.io-Quelle und PNG)
tools/       Hilfsskripte für die Pflege des Materials
```

## Material pflegen

Die Notebooks in `loesungen/` sind die Quelle; `notebooks/` wird daraus erzeugt und nie
direkt bearbeitet. Lösungszellen tragen den Tag `solution`, Zellen mit absichtlichem Fehler
den Tag `raises-exception`.

```bash
uv run python tools/check_notebooks.py           # alle Lösungen ausführen
uv run python tools/make_exercises.py            # notebooks/ aus loesungen/ erzeugen
uv run python tools/make_exercises.py --check    # prüfen, ob notebooks/ aktuell ist
uv run pytest                                    # Tests in testen/
uv run python tools/export_assets.py             # Grafiken in assets/ nach PNG exportieren
```

Die Grafiken liegen als draw.io-Quelle in `assets/` (`<Notebook-Nr>_<thema>.drawio`), daneben
die exportierte PNG, die die Notebooks mit `![...](../assets/<name>.png)` einbinden. Zum Bearbeiten
braucht man die [draw.io-Desktop-App](https://www.drawio.com); ändere die `.drawio`, nicht die PNG.

Der Kurs unterrichtet Python 3.15 (siehe `.python-version`); `uv sync` installiert es bei Bedarf.

`daten/faust.txt` stammt von Project Gutenberg.

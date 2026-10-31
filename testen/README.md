# Testen mit pytest

Ein Test ist ein kleines Programm, das prüft, ob dein Programm tut, was es soll.
Statt nach jeder Änderung von Hand auszuprobieren, startest du einen Befehl und
siehst sofort, ob noch alles stimmt.

[pytest](https://docs.pytest.org/) ist das Standardwerkzeug dafür. Es ist im
Kursprojekt schon installiert (`uv sync`).

## Was liegt hier?

| Datei | Inhalt |
|---|---|
| `prices.py` | der Code, den wir testen: Preise, Rabatte, Warenkorb |
| `test_00_assert.py` | `assert`, Vergleiche, `pytest.approx` |
| `demo_fehlschlaege.py` | absichtlich rote Tests: so liest man die Ausgabe |
| `test_01_grundlagen.py` | Funktionen testen, `pytest.raises`, `parametrize` |
| `conftest.py` | gemeinsame Fixture `cart` für alle Testdateien |
| `test_02_fixtures.py` | Fixtures, eingebaute Fixture `tmp_path` |
| `test_03_organisieren.py` | Testklassen, `skip`, `skipif`, `xfail` |
| `uebungen.py` | Übungen: Funktionen, für die du Tests schreibst |
| `loesung_test_uebungen.py` | Musterlösung zu den Übungen |

Lies die Dateien in dieser Reihenfolge. Jede beginnt mit einem Kommentar, der
erklärt, worum es geht und wie du sie startest.

## Die Regeln, nach denen pytest Tests findet

- Dateien heißen `test_*.py`.
- Testfunktionen heißen `test_…`.
- Testklassen heißen `Test…` und haben kein `__init__`.
- Ein Test ist grün, wenn kein `assert` fehlschlägt und kein unerwarteter
  Fehler auftritt.

`demo_fehlschlaege.py` und `loesung_test_uebungen.py` folgen der Regel absichtlich
nicht: pytest sammelt sie nicht von selbst ein, du startest sie mit ihrem Namen.

## Tests starten

Alle Befehle im Ordner `testen` ausführen:

```bash
cd testen
```

| Befehl | Wirkung |
|---|---|
| `uv run pytest` | alle Tests im Ordner |
| `uv run pytest -v` | jeder Test mit Namen und Ergebnis |
| `uv run pytest test_01_grundlagen.py` | nur eine Datei |
| `uv run pytest test_01_grundlagen.py::test_discount` | nur ein Test |
| `uv run pytest -k discount` | Tests, deren Name `discount` enthält |
| `uv run pytest -x` | beim ersten roten Test aufhören |
| `uv run pytest --lf` | nur die Tests, die beim letzten Lauf rot waren |
| `uv run pytest -s` | `print()`-Ausgaben in Tests anzeigen |
| `uv run pytest demo_fehlschlaege.py` | rote Tests ansehen |

Im Hauptordner des Kursprojekts startet `uv run pytest` ebenfalls genau diese
Tests: `pyproject.toml` legt das mit `testpaths` fest.

## Die Ausgabe lesen

```text
test_00_assert.py ......                                   [ 15%]
test_01_grundlagen.py ...........                          [ 44%]
test_03_organisieren.py .....ssx                           [100%]
```

| Zeichen | Bedeutung |
|---|---|
| `.` | grün, bestanden |
| `F` | rot, ein `assert` ist fehlgeschlagen |
| `E` | Fehler außerhalb des Tests, etwa in einer Fixture |
| `s` | übersprungen (`skip`, `skipif`) |
| `x` | erwartet fehlgeschlagen (`xfail`) |
| `X` | erwartet fehlgeschlagen, aber bestanden |

Bei einem roten Test zeigt pytest die Zeile, beide Seiten des Vergleichs und bei
Listen, Dictionaries und Strings genau die Stelle, an der sie sich unterscheiden.

## Übungen

Schreibe deine Tests in eine neue Datei `test_uebungen.py`.

1. **count() test-first (leicht):** Ergänze `ShoppingCart` in `prices.py` um
   eine Methode `count()`, die die Anzahl der Produkte liefert. Schreibe den
   Test zuerst, sieh ihn rot werden, dann schreibe die Methode.
2. **Tests für eine Funktion mit verstecktem Fehler (mittel):**
   `late_fee(due, returned)` in `uebungen.py` ist Code, den eine KI geschrieben
   haben könnte (präpariert, ein Fehler eingebaut): Er berechnet die
   Mahngebühr der Bibliothek, 0,50 € pro Tag Verspätung, höchstens 10 €,
   Rückgabe am Fälligkeitstag kostenlos. Schreibe Tests mit `parametrize` und
   `date`-Objekten für normale Fälle und Grenzen, bis einer den Fehler aufdeckt.
3. **Eingabe und Ausgabe testen (schwer):** `ask_quantity()` in `uebungen.py`
   fragt so lange nach einer Menge, bis eine ganze Zahl kommt, und meldet
   ungültige Eingaben. Teste sie: Ersetze `input` mit `monkeypatch` durch
   vorgegebene Antworten (`"drei"`, `"3"`) und prüfe mit `capsys` die Meldung.

Die Musterlösung steht in `loesung_test_uebungen.py`.

Im Abschlussprojekt (Notebook 14) testest du so die Spiellogik von Tic-Tac-Toe.

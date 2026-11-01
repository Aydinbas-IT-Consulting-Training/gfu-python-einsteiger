# 13 · Testen mit pytest

Ein Test ist ein kleines Programm, das prüft, ob dein Programm tut, was es soll.
Statt nach jeder Änderung von Hand auszuprobieren, startest du einen Befehl und
siehst sofort, ob noch alles stimmt.

[pytest](https://docs.pytest.org/) ist das Standardwerkzeug dafür. Es ist im
Kursprojekt schon installiert (`uv sync`).

**Lernziele**

- Du schreibst Tests mit `assert` und startest sie mit pytest.
- Du liest die Ausgabe von pytest und findest den Grund für einen roten Test.
- Du testest viele Fälle auf einmal mit `parametrize` und erwartete Fehler mit
  `pytest.raises`.
- Du bereitest Testdaten mit Fixtures vor, auch mit `tmp_path` für Dateien.
- Du testest Eingabe und Ausgabe mit `monkeypatch` und `capsys`.

Alle Befehle in dieser Anleitung startest du im Ordner `testen`. Wechsle im
Terminal zuerst dorthin:

```bash
cd testen
```

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
| `test_04_ein_ausgabe.py` | `input()` ersetzen mit `monkeypatch`, `print()` prüfen mit `capsys`, `pytest.param` |
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

**Kurzübung 1 (Ein Test verschwindet):** Starte `uv run pytest test_00_assert.py -v`
und zähle die Tests. Benenne dann in `test_00_assert.py` die Funktion
`test_numbers` in `check_numbers` um und starte erneut. Wie viele Tests laufen
jetzt, und warum meldet pytest keinen Fehler? Mache die Umbenennung danach
rückgängig.

<details>
<summary>Lösung</summary>

Erst 6 Tests, danach 5. `check_numbers` beginnt nicht mit `test_`, also hält
pytest die Funktion für eine Hilfsfunktion und führt sie gar nicht aus. Das ist
kein Fehler, sondern still fehlender Schutz: Ein falsch benannter Test fällt
nur auf, wenn du die Anzahl im Blick hast.

</details>

## Tests starten

Alle Befehle im Ordner `testen` ausführen (siehe oben):

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

**Kurzübung 2 (Nur die Rabatt-Tests):** Starte aus `test_01_grundlagen.py` nur
die Tests, deren Name `discount` enthält, und lass dir jeden Test einzeln
anzeigen. Wie viele laufen? Die Datei hat nur zwei Testfunktionen mit
`discount` im Namen: Woher kommen die übrigen?

<details>
<summary>Lösung</summary>

```bash
uv run pytest test_01_grundlagen.py -k discount -v
```

7 Tests laufen, 5 werden abgewählt (`deselected`). `parametrize` führt
`test_discount` viermal und `test_invalid_discount_is_rejected` dreimal aus,
einmal pro Fall; `-v` zeigt die Fälle in eckigen Klammern, etwa
`test_discount[100-10-90.0]`.

</details>

## Die Ausgabe lesen

So sieht `uv run pytest` im Ordner `testen` aus:

```text
test_00_assert.py ......                                                 [ 14%]
test_01_grundlagen.py ............                                       [ 42%]
test_02_fixtures.py .........                                            [ 64%]
test_03_organisieren.py .....ssx                                         [ 83%]
test_04_ein_ausgabe.py .......                                           [100%]

=================== 39 passed, 2 skipped, 1 xfailed in 0.06s ===================
```

Jede Datei bekommt eine Zeile mit einem Zeichen pro Test, rechts steht der
Fortschritt in Prozent. Die letzte Zeile zählt zusammen. Mit `-q` (quiet)
fasst pytest alles in eine Zeile Zeichen zusammen.

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

**Kurzübung 3 (Einen Test rot machen):** Ändere in `test_01_grundlagen.py` in
`test_gross_price_standard_rate` den erwarteten Wert von `119.0` auf `120.0`
und starte die Datei. Welches Zeichen steht in der Fortschrittszeile, und in
welchen Zeilen der Ausgabe liest du den tatsächlichen Wert ab? Setze den Wert
danach zurück.

<details>
<summary>Lösung</summary>

Die Fortschrittszeile zeigt `F...........`: der erste Test rot, die übrigen elf
grün. Unter `FAILURES` stehen die Zeilen mit `E`:

```text
E       assert 119.0 == 120.0
E        +  where 119.0 = gross_price(100)
```

Links steht der tatsächliche Wert, rechts der erwartete; die `where`-Zeile
verrät, woher die 119.0 kommt.

</details>

## Übungen

Schreibe deine Tests in eine neue Datei `test_uebungen.py`. Die Funktionen, die
du testest, stehen in `uebungen.py`.

**Übung 1 (count() test-first, leicht):** Ergänze `ShoppingCart` in `prices.py`
um eine Methode `count()`, die die Anzahl der Produkte liefert. Schreibe den
Test zuerst, sieh ihn rot werden, dann schreibe die Methode. Die Fixture `cart`
aus `conftest.py` liefert dir einen leeren Warenkorb.

**Übung 2 (Preise aus dem Kassenbon, leicht):** `parse_price(text)` wandelt
einen Preis wie `"4,99 €"` in die Zahl `4.99` um und löst bei Text wie
`"gratis"` einen `ValueError` aus. Prüfe mit einem einzigen Test und
`parametrize` mindestens vier Eingaben, etwa `"4,99 €"`, `"12 €"`, `"0,50"` und
`" 3,20 € "`. Schreibe dazu einen Test mit `pytest.raises`, der den Fehler bei
`"gratis"` prüft.

**Übung 3 (Einkaufsliste aus einer Datei, leicht):** `read_shopping_list(path)`
liest eine Textdatei mit einem Eintrag pro Zeile und lässt Leerzeilen und
Leerzeichen am Rand weg. Teste sie, ohne Dateien im Projekt anzulegen: Schreibe
mit der Fixture `tmp_path` eine kleine Liste mit einer Leerzeile in eine Datei
und prüfe das Ergebnis.

**Übung 4 (Tests für eine Funktion mit verstecktem Fehler, mittel):**
`late_fee(due, returned)` ist Code, den eine KI geschrieben haben könnte
(präpariert, ein Fehler eingebaut): Er berechnet die Mahngebühr der
Bibliothek, 0,50 € pro Tag Verspätung, höchstens 10 €, Rückgabe am
Fälligkeitstag kostenlos. Schreibe Tests mit `parametrize` und `date`-Objekten
für normale Fälle und Grenzen, bis einer den Fehler aufdeckt. Erkläre den
Fehler in einem Satz und behebe ihn.

**Übung 5 (Durchschnitt einer leeren Liste, mittel):** `average(numbers)`
liefert den Durchschnitt einer Liste. Teste zwei normale Fälle. Überlege dann,
was bei einer leeren Liste passieren soll, und schreibe einen Test, der einen
`ValueError` mit einer verständlichen Meldung verlangt. Markiere ihn mit
`xfail`, solange `average()` noch falsch reagiert. Korrigiere dann die
Funktion. Welches Zeichen zeigt die Ausgabe vor der Korrektur, welches danach?
Was tust du mit der Markierung, sobald die Funktion stimmt?

**Übung 6 (Eingabe und Ausgabe testen, schwer):** `ask_quantity()` fragt so
lange nach einer Menge, bis eine ganze Zahl kommt, und meldet ungültige
Eingaben. Teste sie: Ersetze `input` mit `monkeypatch` durch vorgegebene
Antworten (`"drei"`, `"3"`) und prüfe mit `capsys` die Meldung. Wie beides
geht, zeigt `test_04_ein_ausgabe.py`.

Tipp: Für mehrere Antworten nacheinander legst du sie in einen Iterator,
`answers = iter(["drei", "3"])`, und ersetzt `input` durch
`lambda prompt: next(answers)`. Jeder Aufruf liefert dann die nächste Antwort.

Die Musterlösung steht in `loesung_test_uebungen.py`.

Im Abschlussprojekt (Notebook 14) testest du so die Spiellogik von Tic-Tac-Toe.

## Zusammenfassung

- pytest sammelt Funktionen `test_…` aus Dateien `test_*.py` und führt sie aus.
- `assert` prüft eine Bedingung; `pytest.approx` vergleicht Kommazahlen mit
  Toleranz.
- `pytest.raises` prüft, dass ein Fehler kommt, `match=` prüft seine Meldung.
- `@pytest.mark.parametrize` führt einen Test für viele Fälle aus,
  `pytest.param(..., id="name")` gibt einem Fall einen sprechenden Namen.
- Fixtures liefern Testdaten; `conftest.py` teilt sie mit allen Testdateien,
  `tmp_path` ist ein frischer Ordner für Dateien.
- `skip`, `skipif` und `xfail` markieren Tests, die nicht laufen sollen oder
  erwartet fehlschlagen.
- `monkeypatch` ersetzt `input()`, `capsys.readouterr().out` liefert die
  Ausgabe von `print()`.

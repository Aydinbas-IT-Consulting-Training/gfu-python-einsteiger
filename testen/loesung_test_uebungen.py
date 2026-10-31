"""Musterlösung zu den Übungen in README.md.

Der Name beginnt nicht mit test_, damit pytest die Lösung nicht von selbst
einsammelt. Starte sie ausdrücklich:

    uv run pytest loesung_test_uebungen.py -v

Einige Tests sind rot, bis du den Code korrigiert oder ergänzt hast:

- Übung 1: test_count, bis ShoppingCart in prices.py diese Methode hat:

    def count(self) -> int:
        return len(self.items)

- Übung 2: zwei Fälle von test_late_fee. late_fee() zählt einen Tag zu viel:
  Am Fälligkeitstag ist (returned - due).days schon 0. Entferne das + 1.

- Zusatz: test_average_of_empty_list_explains_the_problem, solange average()
  bei einer leeren Liste durch 0 teilt. Korrektur zum Beispiel so:

    def average(numbers: list[float]) -> float:
        if not numbers:
            raise ValueError("average() braucht mindestens eine Zahl")
        return sum(numbers) / len(numbers)
"""

from datetime import date

import pytest

from uebungen import ask_quantity, average, late_fee

# --- Übung 1: count() test-first --------------------------------------------


def test_count_of_new_cart_is_zero(cart):
    assert cart.count() == 0


def test_count(cart):
    cart.add("Kaffee", 3.50)
    cart.add("Brezel", 1.20)
    assert cart.count() == 2


# --- Übung 2: late_fee -------------------------------------------------------


@pytest.mark.parametrize(
    ("returned", "expected"),
    [
        (date(2026, 11, 20), 0.0),  # zu früh zurückgegeben
        (date(2026, 11, 30), 0.0),  # am Fälligkeitstag: deckt den Fehler auf
        (date(2026, 12, 1), 0.50),  # ein Tag zu spät
        (date(2026, 12, 20), 10.0),  # genau am Deckel
        (date(2027, 1, 31), 10.0),  # weit darüber
    ],
)
def test_late_fee(returned, expected):
    assert late_fee(date(2026, 11, 30), returned) == expected


# --- Übung 3: Eingabe und Ausgabe -------------------------------------------


def test_ask_quantity_repeats_until_valid(monkeypatch, capsys):
    answers = iter(["drei", "3"])
    # Das lambda braucht den Parameter prompt: input wird mit "Menge: " aufgerufen
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    assert ask_quantity() == 3
    assert "'drei' ist keine ganze Zahl" in capsys.readouterr().out


# --- Zusatz: average ---------------------------------------------------------


def test_average():
    assert average([1, 2, 3, 4]) == 2.5


def test_average_of_one_number():
    assert average([7]) == 7


def test_average_of_empty_list_explains_the_problem():
    # Ohne Korrektur: ZeroDivisionError statt einer verständlichen Meldung
    with pytest.raises(ValueError, match="mindestens eine Zahl"):
        average([])

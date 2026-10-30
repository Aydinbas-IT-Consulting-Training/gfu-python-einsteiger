"""Musterlösung zu uebungen.py.

Der Name beginnt nicht mit test_, damit pytest die Lösung nicht von selbst
einsammelt. Starte sie ausdrücklich:

    uv run pytest loesung_test_uebungen.py -v

Der letzte Test ist rot, solange average() den Fehler hat. Behebe ihn in
uebungen.py, zum Beispiel so:

    def average(numbers: list[float]) -> float:
        if not numbers:
            raise ValueError("average() braucht mindestens eine Zahl")
        return sum(numbers) / len(numbers)
"""

import pytest

from uebungen import average, is_leap_year, withdraw

# --- is_leap_year -----------------------------------------------------------


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (2024, True),  # durch 4 teilbar
        (2023, False),  # nicht durch 4 teilbar
        (1900, False),  # durch 100 teilbar
        (2000, True),  # durch 400 teilbar
    ],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) is expected


# --- withdraw ---------------------------------------------------------------


def test_withdraw_reduces_balance():
    assert withdraw(100, 30) == 70


def test_withdraw_whole_balance():
    assert withdraw(100, 100) == 0


@pytest.mark.parametrize("amount", [0, -10])
def test_withdraw_rejects_non_positive_amount(amount):
    with pytest.raises(ValueError, match="Betrag muss positiv sein"):
        withdraw(100, amount)


def test_withdraw_rejects_overdraft():
    with pytest.raises(ValueError, match="Kontostand reicht nicht aus"):
        withdraw(100, 100.01)


# --- average ----------------------------------------------------------------


def test_average():
    assert average([1, 2, 3, 4]) == 2.5


def test_average_of_one_number():
    assert average([7]) == 7


def test_average_of_empty_list_explains_the_problem():
    # Ohne Korrektur: ZeroDivisionError statt einer verständlichen Meldung
    with pytest.raises(ValueError, match="mindestens eine Zahl"):
        average([])

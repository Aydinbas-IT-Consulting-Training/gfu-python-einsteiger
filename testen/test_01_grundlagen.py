"""Teil 1: Funktionen testen, Fehler testen, viele Fälle auf einmal.

Starten:  uv run pytest test_01_grundlagen.py -v
"""

import pytest

from prices import apply_discount, gross_price

# --- Ein Verhalten pro Test, der Name sagt welches -------------------------


def test_gross_price_standard_rate():
    assert gross_price(100) == 119.0


def test_gross_price_reduced_rate():
    assert gross_price(100, vat_rate=0.07) == 107.0


def test_gross_price_rounds_to_cents():
    # 9,99 € * 1,19 = 11,8881 €, gerundet 11,89 €
    assert gross_price(9.99) == 11.89


# --- Fehler testen ----------------------------------------------------------
# Auch ein Fehler im richtigen Moment ist Verhalten. pytest.raises ist nur dann
# grün, wenn der Block darunter genau diesen Fehler auslöst.


def test_negative_price_is_rejected():
    with pytest.raises(ValueError):
        gross_price(-5)


def test_error_message_names_the_value():
    # match= prüft, ob die Fehlermeldung diesen Text enthält
    with pytest.raises(ValueError, match="-5"):
        gross_price(-5)


# --- Viele Fälle, ein Test --------------------------------------------------
# parametrize führt den Test einmal pro Tupel aus. Mit -v siehst du jeden Fall
# einzeln, etwa test_discount[100-10-90.0].


@pytest.mark.parametrize(
    ("price", "percent", "expected"),
    [
        (100, 10, 90.0),
        (100, 0, 100.0),  # Randfall: kein Rabatt
        (100, 100, 0.0),  # Randfall: alles geschenkt
        (19.99, 15, 16.99),
    ],
)
def test_discount(price, percent, expected):
    # 19,99 * 0,85 ist 16,9915: approx mit abs=0.01 erlaubt einen Cent Abweichung
    assert apply_discount(price, percent) == pytest.approx(expected, abs=0.01)


@pytest.mark.parametrize("percent", [-1, 101, 250])
def test_invalid_discount_is_rejected(percent):
    with pytest.raises(ValueError, match="zwischen 0 und 100"):
        apply_discount(100, percent)

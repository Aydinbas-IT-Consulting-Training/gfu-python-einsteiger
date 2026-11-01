"""Absichtlich rote Tests: So zeigt pytest, was nicht stimmt.

Diese Datei beginnt nicht mit test_, deshalb sammelt pytest sie nicht von
selbst ein. Starte sie ausdrücklich:

    uv run pytest demo_fehlschlaege.py

Lies die Ausgabe zu jedem Test: Die Zeilen mit E zeigen die tatsächlichen
Werte und bei Listen, Dictionaries und Strings genau den Unterschied.
"""

import pytest

from prices import apply_discount, gross_price


def test_wrong_number():
    # pytest zeigt beide Seiten und woher der Wert kommt
    assert gross_price(10) == 12.0


def test_lists_differ():
    # pytest nennt den Index, an dem sich die Listen unterscheiden
    assert [1, 2, 3, 4] == [1, 2, 4, 4]


def test_dicts_differ():
    # pytest listet abweichende und fehlende Schlüssel auf
    expected = {"name": "Ada", "city": "London", "born": 1815}
    actual = {"name": "Ada", "city": "Paris"}
    assert actual == expected


def test_strings_differ():
    # Bei langen Strings markiert pytest die abweichende Stelle
    assert "Explicit is better than implicit." == "Explicit is better then implicit."


def test_expected_error_missing():
    # Rot, weil kein ValueError kommt: 50 % Rabatt sind erlaubt
    with pytest.raises(ValueError):
        apply_discount(100, 50)


def test_unexpected_error():
    # Rot, weil ein Fehler auftritt, den der Test nicht erwartet
    gross_price(-5)

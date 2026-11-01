"""Teil 0: assert, der Grundbaustein jedes Tests.

pytest sammelt alle Funktionen, deren Name mit test_ beginnt, aus allen
Dateien, deren Name mit test_ beginnt, und führt sie aus. Ein Test ist grün,
wenn kein assert fehlschlägt und kein unerwarteter Fehler auftritt.

Starten:  uv run pytest test_00_assert.py -v
"""

import pytest


def test_numbers():
    assert 1 + 1 == 2
    assert 10 > 5
    assert 7 // 2 == 3


def test_strings():
    assert "Py" + "thon" == "Python"
    assert "thon" in "Python"
    assert "python".upper() == "PYTHON"


def test_lists():
    # Listen werden Element für Element verglichen, die Reihenfolge zählt
    assert sorted([3, 1, 2]) == [1, 2, 3]
    assert 2 in [1, 2, 3]
    assert len([1, 2, 3]) == 3


def test_dicts():
    # Bei Dictionaries zählt die Reihenfolge nicht, nur Schlüssel und Werte
    assert {"a": 1, "b": 2} == {"b": 2, "a": 1}
    assert "a" in {"a": 1}


def test_floats():
    # Kommazahlen sind nicht immer exakt: 0.1 + 0.2 ist 0.30000000000000004
    assert 0.1 + 0.2 != 0.3
    # pytest.approx vergleicht mit einer winzigen Toleranz
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_assert_with_message():
    # Hinter dem Komma steht eine Meldung, die nur bei einem Fehlschlag erscheint
    stock = 5
    assert stock > 0, "Das Lager ist leer"


# Wie sieht ein roter Test aus? Das zeigt die Datei demo_fehlschlaege.py:
#     uv run pytest demo_fehlschlaege.py

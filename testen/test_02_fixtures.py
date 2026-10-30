"""Teil 2: Fixtures liefern vorbereitete Testdaten.

Brauchen mehrere Tests dieselben Daten, schreibst du die Vorbereitung einmal
als Fixture. Ein Test bekommt eine Fixture, indem er einen Parameter mit
ihrem Namen hat. pytest ruft die Fixture vor jedem Test neu auf, damit sich
Tests nicht gegenseitig beeinflussen.

Starten:  uv run pytest test_02_fixtures.py -v
"""

from pathlib import Path

import pytest

from prices import ShoppingCart, load_cart

# --- Eine Fixture aus conftest.py ------------------------------------------


def test_new_cart_is_empty(cart):
    # cart kommt aus conftest.py
    assert cart.items == {}
    assert cart.total() == 0


def test_add_product(cart):
    cart.add("Kaffee", 3.50)
    assert cart.items == {"Kaffee": 3.50}


def test_each_test_gets_a_fresh_cart(cart):
    # test_add_product hat Kaffee hinzugefügt, hier ist der Warenkorb trotzdem leer
    assert "Kaffee" not in cart.items


# --- Eine eigene Fixture in dieser Datei ------------------------------------


@pytest.fixture
def full_cart() -> ShoppingCart:
    cart = ShoppingCart()
    cart.add("Kaffee", 3.50)
    cart.add("Kuchen", 4.20)
    cart.add("Wasser", 2.00)
    return cart


def test_total_is_sum_of_gross_prices(full_cart):
    # 4,17 + 5,00 + 2,38 = 11,55 (jeweils brutto)
    assert full_cart.total() == 11.55


def test_remove_product(full_cart):
    full_cart.remove("Kuchen")
    assert list(full_cart.items) == ["Kaffee", "Wasser"]


def test_remove_missing_product_fails(full_cart):
    with pytest.raises(KeyError):
        full_cart.remove("Tee")


def test_same_product_twice_is_rejected(full_cart):
    with pytest.raises(ValueError, match="schon im Warenkorb"):
        full_cart.add("Kaffee", 3.50)


# --- Eingebaute Fixture: tmp_path -------------------------------------------
# pytest bringt eigene Fixtures mit. tmp_path ist ein frischer, leerer Ordner
# (ein Path-Objekt, Notebook 10), den pytest nach dem Test selbst aufräumt.
# So testest du Dateizugriffe, ohne echte Dateien anzufassen.


def test_save_and_load_roundtrip(full_cart, tmp_path: Path):
    path = tmp_path / "warenkorb.txt"
    full_cart.save(path)
    assert path.exists()
    assert load_cart(path) == full_cart  # Datenklassen vergleichen ihre Felder


def test_saved_file_has_one_line_per_product(full_cart, tmp_path: Path):
    path = tmp_path / "warenkorb.txt"
    full_cart.save(path)
    assert path.read_text(encoding="utf-8").splitlines() == [
        "Kaffee;3.5",
        "Kuchen;4.2",
        "Wasser;2.0",
    ]

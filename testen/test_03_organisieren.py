"""Teil 3: Tests ordnen, auswählen und markieren.

Starten:  uv run pytest test_03_organisieren.py -v
Auswahl:  uv run pytest -k discount -v       (nur Tests mit "discount" im Namen)
          uv run pytest test_03_organisieren.py::TestShoppingCart -v
"""

import sys

import pytest

from prices import ShoppingCart, apply_discount

# --- Tests in einer Klasse bündeln ------------------------------------------
# Zusammengehörige Tests darfst du in eine Klasse packen. Ihr Name beginnt mit
# Test, die Methoden mit test_. Ein __init__ braucht die Klasse nicht.


class TestShoppingCart:
    def test_empty_total(self, cart):
        assert cart.total() == 0

    def test_total_with_one_product(self, cart):
        cart.add("Tee", 3.10)
        assert cart.total() == 3.69

    def test_total_with_free_product(self, cart):
        cart.add("Probe", 0)
        assert cart.total() == 0


class TestDiscount:
    def test_half_price(self):
        assert apply_discount(10, 50) == 5

    def test_no_discount(self):
        assert apply_discount(10, 0) == 10


# --- Markierungen -----------------------------------------------------------
# Mit @pytest.mark.… gibst du pytest Hinweise zu einzelnen Tests.


@pytest.mark.skip(reason="Gutscheine sind noch nicht eingebaut")
def test_voucher():
    # skip: Der Test wird übersprungen und in der Ausgabe als s angezeigt
    cart = ShoppingCart()
    cart.redeem("SOMMER10")


@pytest.mark.skipif(sys.platform != "win32", reason="nur unter Windows relevant")
def test_windows_line_endings():
    # skipif: nur überspringen, wenn die Bedingung wahr ist
    assert "\r\n".strip() == ""


@pytest.mark.xfail(reason="Bekannter Fehler: Rabatt wird nicht auf Cent gerundet")
def test_discount_is_rounded_to_cents():
    # xfail: Wir wissen, dass der Test fehlschlägt, und dokumentieren das.
    # Die Ausgabe zeigt x statt F. Wird der Fehler behoben, zeigt sie X.
    assert apply_discount(10, 100 / 3) == 6.67

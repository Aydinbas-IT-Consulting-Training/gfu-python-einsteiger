"""Gemeinsame Fixtures für alle Testdateien in diesem Ordner.

pytest lädt conftest.py automatisch. Jede Fixture hier steht in allen
Testdateien des Ordners zur Verfügung, ohne Import.
"""

import pytest

from prices import ShoppingCart


@pytest.fixture
def cart() -> ShoppingCart:
    """Ein leerer Warenkorb, für jeden Test ein neuer."""
    return ShoppingCart()

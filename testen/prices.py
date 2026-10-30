"""Preisberechnung für einen kleinen Kiosk: der Code, den wir in diesem Ordner testen."""

from dataclasses import dataclass, field
from pathlib import Path


def gross_price(net_price: float, vat_rate: float = 0.19) -> float:
    """Liefert den Bruttopreis, auf Cent gerundet."""
    if net_price < 0:
        raise ValueError(f"Nettopreis darf nicht negativ sein: {net_price}")
    return round(net_price * (1 + vat_rate), 2)


def apply_discount(price: float, percent: float) -> float:
    """Zieht einen Rabatt in Prozent ab."""
    if not 0 <= percent <= 100:
        raise ValueError(f"Rabatt muss zwischen 0 und 100 Prozent liegen: {percent}")
    return price * (1 - percent / 100)


@dataclass
class ShoppingCart:
    """Ein Warenkorb: Produktname -> Nettopreis."""

    items: dict[str, float] = field(default_factory=dict)

    def add(self, product: str, net_price: float) -> None:
        if product in self.items:
            raise ValueError(f"{product} liegt schon im Warenkorb")
        self.items[product] = net_price

    def remove(self, product: str) -> None:
        del self.items[product]  # KeyError, wenn das Produkt fehlt

    def total(self) -> float:
        """Summe der Bruttopreise, auf Cent gerundet."""
        return round(sum(gross_price(price) for price in self.items.values()), 2)

    def save(self, path: Path) -> None:
        """Speichert den Warenkorb als Textdatei, eine Zeile pro Produkt."""
        lines = [f"{product};{price}" for product, price in self.items.items()]
        path.write_text("\n".join(lines), encoding="utf-8")


def load_cart(path: Path) -> ShoppingCart:
    """Liest einen mit save() gespeicherten Warenkorb wieder ein."""
    cart = ShoppingCart()
    for line in path.read_text(encoding="utf-8").splitlines():
        product, price = line.split(";")
        cart.add(product, float(price))
    return cart

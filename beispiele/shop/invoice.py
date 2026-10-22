"""Rechnungszeilen, nutzt das Nachbarmodul pricing."""

from shop.pricing import gross_price


def invoice_line(product: str, net_price: float) -> str:
    return f"{product:<10} {gross_price(net_price):>8.2f} €"

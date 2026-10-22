"""Preisberechnung."""

VAT_RATE = 0.19


def gross_price(net_price: float, vat_rate: float = VAT_RATE) -> float:
    return round(net_price * (1 + vat_rate), 2)

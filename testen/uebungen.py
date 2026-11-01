"""Übungen: Schreibe Tests für diese Funktionen in eine neue Datei test_uebungen.py.

Die Aufgaben stehen in README.md, Abschnitt "Übungen".
Eine Musterlösung steht in loesung_test_uebungen.py.
"""

from datetime import date
from pathlib import Path


def parse_price(text: str) -> float:
    """Wandelt einen Preis wie "4,99 €" in eine Zahl um (ohne Tausenderpunkt)."""
    cleaned = text.replace("€", "").strip().replace(",", ".")
    if not cleaned.replace(".", "", 1).isdigit():
        raise ValueError(f"Kein Preis: {text!r}")
    return float(cleaned)


def read_shopping_list(path: Path) -> list[str]:
    """Liest eine Einkaufsliste: ein Eintrag pro Zeile, Leerzeilen zählen nicht."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def late_fee(due: date, returned: date) -> float:
    """0,50 € pro Tag nach Fälligkeit, höchstens 10 €. Am Fälligkeitstag kostenlos."""
    days_late = (returned - due).days + 1
    return min(max(days_late, 0) * 0.50, 10.0)


def average(numbers: list[float]) -> float:
    """Liefert den Durchschnitt der Zahlen."""
    return sum(numbers) / len(numbers)


def ask_quantity() -> int:
    """Fragt so lange nach einer Menge, bis eine ganze Zahl eingegeben wird."""
    while True:
        answer = input("Menge: ")
        if answer.isdigit():
            return int(answer)
        print(f"'{answer}' ist keine ganze Zahl")

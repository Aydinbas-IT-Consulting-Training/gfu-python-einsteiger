"""Übungen: Schreibe Tests für diese Funktionen in eine neue Datei test_uebungen.py.

Die Aufgaben stehen in README.md, Abschnitt "Übungen".
Eine Musterlösung steht in loesung_test_uebungen.py.
"""

from datetime import date


def late_fee(due: date, returned: date) -> float:
    """0,50 € pro Tag nach Fälligkeit, höchstens 10 €. Am Fälligkeitstag kostenlos."""
    days_late = (returned - due).days + 1
    return min(max(days_late, 0) * 0.50, 10.0)


def ask_quantity() -> int:
    """Fragt so lange nach einer Menge, bis eine ganze Zahl eingegeben wird."""
    while True:
        answer = input("Menge: ")
        if answer.isdigit():
            return int(answer)
        print(f"'{answer}' ist keine ganze Zahl")


def average(numbers: list[float]) -> float:
    """Liefert den Durchschnitt der Zahlen."""
    return sum(numbers) / len(numbers)

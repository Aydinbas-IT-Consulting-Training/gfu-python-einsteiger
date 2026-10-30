"""Übungen: Schreibe Tests für diese Funktionen in eine neue Datei test_uebungen.py.

Eine der Funktionen hat einen Fehler. Finde ihn mit einem Test, bevor du ihn behebst.
Eine Musterlösung steht in loesung_test_uebungen.py.
"""


def is_leap_year(year: int) -> bool:
    """Schaltjahr: durch 4 teilbar, außer durch 100, aber wieder durch 400."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def withdraw(balance: float, amount: float) -> float:
    """Hebt amount vom Konto ab und liefert den neuen Kontostand."""
    if amount <= 0:
        raise ValueError(f"Betrag muss positiv sein, war {amount}")
    if amount > balance:
        raise ValueError("Kontostand reicht nicht aus")
    return balance - amount


def average(numbers: list[float]) -> float:
    """Liefert den Durchschnitt der Zahlen."""
    return sum(numbers) / len(numbers)

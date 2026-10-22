"""Kleines Beispielmodul für Notebook 06."""

import random


def roll_dice(sides: int = 6) -> int:
    """Würfelt eine Zahl von 1 bis ``sides``."""
    return random.randint(1, sides)

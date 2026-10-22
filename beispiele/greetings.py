"""Beispielmodul für Notebook 08: zeigt, wann ein Modul ausgeführt wird."""

print(f"Modul {__name__} wird geladen")

DEFAULT_GREETING = "Hallo"


def greet(name: str, greeting: str = DEFAULT_GREETING) -> str:
    return f"{greeting} {name}!"


if __name__ == "__main__":
    print(greet("Welt"))

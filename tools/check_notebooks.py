"""Führt alle Lösungs-Notebooks aus und meldet unerwartete Fehler.

Zellen, die absichtlich einen Fehler zeigen, tragen den Tag ``raises-exception``.
``input()`` wird durch feste Antworten ersetzt, damit nichts blockiert.

Aufruf: ``uv run python tools/check_notebooks.py``
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT / "loesungen"

FAKE_INPUT = """\
import builtins
import itertools

_fields = itertools.cycle("123456789")
_tips = itertools.cycle(range(1, 101))


def _fake_input(prompt=""):
    print(prompt, end="")
    if "Feld" in prompt:
        return next(_fields)
    if "Tipp" in prompt:
        return str(next(_tips))
    if "Operator" in prompt:
        return "+"
    if "heißt" in prompt or "Name" in prompt:
        return "Ada"
    return "42"


builtins.input = _fake_input
get_ipython().kernel.raw_input = _fake_input
"""


def check(path: Path) -> bool:
    notebook = nbformat.read(path, as_version=4)
    notebook.cells.insert(0, nbformat.v4.new_code_cell(FAKE_INPUT))
    client = NotebookClient(
        notebook, timeout=60, resources={"metadata": {"path": path.parent}}
    )
    try:
        client.execute()
    except CellExecutionError as error:
        print(f"FEHLER {path.name}\n{error}")
        return False
    print(f"ok     {path.name}")
    return True


def main() -> None:
    results = [check(path) for path in sorted(SOLUTIONS_DIR.glob("*.ipynb"))]
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()

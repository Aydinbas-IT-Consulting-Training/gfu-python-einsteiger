"""Erzeugt die Teilnehmer-Notebooks aus den Lösungs-Notebooks.

Zellen mit dem Tag ``solution`` werden durch eine leere Übungszelle ersetzt,
alle Ausgaben werden entfernt.

Aufruf: ``uv run python tools/make_exercises.py``
"""

from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = ROOT / "loesungen"
EXERCISES_DIR = ROOT / "notebooks"
PLACEHOLDER = "# Deine Lösung\n"


def strip_solutions(notebook: nbformat.NotebookNode) -> nbformat.NotebookNode:
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        if "solution" in cell.metadata.get("tags", []):
            cell.source = PLACEHOLDER
            cell.metadata["tags"] = ["exercise"]
        cell.outputs = []
        cell.execution_count = None
    return notebook


def main() -> None:
    EXERCISES_DIR.mkdir(exist_ok=True)
    for source in sorted(SOLUTIONS_DIR.glob("*.ipynb")):
        notebook = strip_solutions(nbformat.read(source, as_version=4))
        nbformat.write(notebook, EXERCISES_DIR / source.name)
        print(f"{source.name} -> notebooks/")


if __name__ == "__main__":
    main()

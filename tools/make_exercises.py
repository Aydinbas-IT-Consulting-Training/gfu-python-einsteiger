"""Erzeugt die Teilnehmer-Notebooks aus den Lösungs-Notebooks.

Zellen mit dem Tag ``solution`` werden durch eine leere Übungszelle ersetzt,
alle Ausgaben werden entfernt.

Aufruf: ``uv run python tools/make_exercises.py``

Mit ``--check`` wird nichts geschrieben: das Skript meldet Notebooks in
``notebooks/``, die von ihrer Quelle in ``loesungen/`` abweichen (etwa weil
jemand ``notebooks/`` direkt bearbeitet hat), und endet dann mit Code 1.
"""

import argparse
import sys
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


def out_of_sync() -> list[str]:
    problems = []
    sources = sorted(SOLUTIONS_DIR.glob("*.ipynb"))
    for source in sources:
        target = EXERCISES_DIR / source.name
        if not target.exists():
            problems.append(f"{target.name}: fehlt in notebooks/")
            continue
        expected = nbformat.writes(strip_solutions(nbformat.read(source, as_version=4)))
        if target.read_text(encoding="utf-8").rstrip("\n") != expected.rstrip("\n"):
            problems.append(f"{target.name}: weicht von loesungen/ ab")
    source_names = {source.name for source in sources}
    for target in sorted(EXERCISES_DIR.glob("*.ipynb")):
        if target.name not in source_names:
            problems.append(f"{target.name}: hat keine Quelle in loesungen/")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="nur prüfen, nichts schreiben"
    )
    args = parser.parse_args()

    if args.check:
        problems = out_of_sync()
        for problem in problems:
            print(problem)
        if problems:
            print("Bearbeite loesungen/ und erzeuge notebooks/ neu.")
            sys.exit(1)
        print("notebooks/ passt zu loesungen/")
        return

    EXERCISES_DIR.mkdir(exist_ok=True)
    for source in sorted(SOLUTIONS_DIR.glob("*.ipynb")):
        notebook = strip_solutions(nbformat.read(source, as_version=4))
        nbformat.write(notebook, EXERCISES_DIR / source.name)
        print(f"{source.name} -> notebooks/")


if __name__ == "__main__":
    main()

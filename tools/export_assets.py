"""Exportiert die Grafiken in ``assets/`` von draw.io nach PNG.

Jede ``assets/<name>.drawio`` wird zu ``assets/<name>.png`` (doppelte Auflösung,
weißer Hintergrund, damit die Bilder auch im dunklen Editor-Thema lesbar sind).
Exportiert wird nur, wenn die PNG fehlt oder älter als ihre Quelle ist.

Aufruf: ``uv run python tools/export_assets.py``

Braucht die draw.io-Desktop-App (https://www.drawio.com). Mit ``--all`` werden
alle Grafiken neu exportiert, mit ``--check`` wird nichts geschrieben: das Skript
meldet fehlende PNGs und Grafiken, die kein Notebook in ``loesungen/`` einbindet,
und endet dann mit Code 1.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
SOLUTIONS_DIR = ROOT / "loesungen"
MAC_APP = Path("/Applications/draw.io.app/Contents/MacOS/draw.io")


def find_drawio() -> str:
    for candidate in ("drawio", "draw.io"):
        if found := shutil.which(candidate):
            return found
    if MAC_APP.exists():
        return str(MAC_APP)
    sys.exit("draw.io nicht gefunden: Desktop-App installieren oder in PATH legen.")


def stale(source: Path) -> bool:
    target = source.with_suffix(".png")
    return not target.exists() or target.stat().st_mtime < source.stat().st_mtime


def check(sources: list[Path]) -> list[str]:
    notebooks = "".join(
        path.read_text(encoding="utf-8") for path in SOLUTIONS_DIR.glob("*.ipynb")
    )
    problems = []
    for source in sources:
        target = source.with_suffix(".png")
        if not target.exists():
            problems.append(f"PNG fehlt: {target.name}")
        elif f"assets/{target.name}" not in notebooks:
            problems.append(f"von keinem Notebook eingebunden: {target.name}")
    return problems


def export(drawio: str, source: Path) -> None:
    target = source.with_suffix(".png")
    subprocess.run(
        [drawio, "-x", "-f", "png", "-s", "2", "-b", "10", "--transparent=false",
         "-o", str(target), str(source)],
        check=True,
        capture_output=True,
    )
    print(f"{source.name} -> {target.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="alle Grafiken exportieren")
    group.add_argument("--check", action="store_true", help="nur prüfen")
    args = parser.parse_args()

    sources = sorted(ASSETS_DIR.glob("*.drawio"))
    if args.check:
        problems = check(sources)
        for problem in problems:
            print(problem)
        if problems:
            sys.exit(1)
        print("assets/ ist vollständig")
        return
    todo = sources if args.all else [s for s in sources if stale(s)]
    drawio = find_drawio()
    for source in todo:
        export(drawio, source)


if __name__ == "__main__":
    main()

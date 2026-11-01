# Hinweise für Coding-Agenten

- Notebooks nur in `loesungen/` bearbeiten; `notebooks/` wird mit `tools/make_exercises.py` daraus erzeugt. Vor jedem Commit: `uv run python tools/make_exercises.py --check`.
- Grafiken: `.drawio` in `assets/` bearbeiten, dann `uv run python tools/export_assets.py`; vor jedem Commit `--check`.
- Pflege-Befehle und Aufbau: `README.md`, Abschnitt "Material pflegen".
- Keine Foliensätze (pptx) ins Repo: das Repo wird mit Teilnehmenden geteilt.

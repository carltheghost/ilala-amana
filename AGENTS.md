# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **single Python CLI package** (`ilala-amana` / SuperSub Agency Agent). There are no long-running servers, databases, Docker services, or external API dependencies required for local development.

### Services

| Component | Role | How to run |
|-----------|------|------------|
| SuperSub CLI | Only runnable product; routes missions in-process | `python3 -m supersub_agency "<mission>"` or `supersub "<mission>"` after editable install |
| Unit tests | Verification (not a daemon) | `python3 -m unittest discover -s tests` |

No ports are opened. Provider lanes (OpenClaw, Hermes, etc.) are in-process stubs only.

### Standard commands

See `README.md` for full examples. Quick reference:

- **Install (editable):** `pip install -e .` (Python ≥3.11)
- **Tests:** `python3 -m unittest discover -s tests`
- **Run agent:** `python3 -m supersub_agency "your mission" --budget 250`
- **JSON output:** add `--json`
- **List lanes:** `python3 -m supersub_agency --capabilities`

### Notes for cloud agents

- **Lint:** No Ruff/Flake8/mypy config in the repo; rely on unit tests for validation.
- **`supersub` on PATH:** After `pip install -e .`, the console script may land in `~/.local/bin`. Prefer `python3 -m supersub_agency` if `supersub` is not found.
- **Git branch:** Application code may exist on `origin/cursor/supersub-agency-agent-702e` while `master` is minimal; the working tree in Cloud Agent VMs typically includes the full package files regardless of detached HEAD.

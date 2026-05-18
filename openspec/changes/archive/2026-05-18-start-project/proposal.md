## Why

The PRD defines **English, Please** — a local GNOME app for offline English proofreading via Ollama — but the repository has no application code yet. We need a runnable foundation that validates the Ollama prompt contract and proves the GTK stack works on the target desktop before building structured review UI and settings.

## What Changes

- Add a Python 3.12 project with `pyproject.toml`, package layout under `src/english_please/`, and a console entry point.
- Add a reusable Ollama HTTP client module that calls `POST /api/chat` with JSON output and parses the PRD response schema.
- Add a minimal libadwaita window: multi-line input, Review button, plain-text result area (M1 spike — not structured panels yet).
- Add GNOME integration: `Gtk.Application` single-instance, `.desktop` file, placeholder icon, and README setup instructions.
- Persist config at `~/.config/english-please/config.json` with default keys (`model`, `review_command`, `post_review_command`).

**Out of scope for this change:** structured OK / corrected / issues panels (M2), streaming preview, model dropdown, Settings dialog, custom shell commands, Flatpak packaging.

## Capabilities

### New Capabilities

- `project-scaffold`: Packaging, dependencies, config path, and documented dev/run workflow.
- `ollama-client`: Local Ollama `/api/chat` integration with PRD JSON schema and connection-error handling.
- `desktop-app-shell`: Minimal libadwaita UI — input, Review, plain output, keyboard shortcuts.
- `gnome-integration`: Single-instance application ID, desktop entry, and applications-menu visibility.

### Modified Capabilities

_None — no existing specs in `openspec/specs/`._

## Impact

- **New files:** `pyproject.toml`, `src/english_please/` (`main.py`, `window.py`, `ollama.py`, `config.py`), `data/com.viniciuskr.EnglishPlease.desktop`, placeholder icon, updated `README.md`.
- **Dependencies:** PyGObject (GTK 4 / libadwaita), `aiohttp`.
- **Runtime:** Requires Ollama on `localhost:11434` for manual review testing; no outbound network from the app itself.
- **Follow-up changes:** `structured-review`, `settings-commands`, and `gnome-shortcut-docs` can build on this scaffold.

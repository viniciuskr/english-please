## Why

The README currently requires users to run several manual steps (apt packages, venv, pip install, copy `.desktop` and icon). PRD milestone **M5** calls for at least an `install.sh` so a developer or end user on Ubuntu/GNOME can go from clone to runnable app in one command.

## What Changes

- Add `install.sh` at the repository root that automates: system dependency check/install (Ubuntu), Python venv creation, editable `pip install`, and GNOME desktop entry + icon installation under `~/.local`.
- Add `--help`, `--dry-run`, and clear error messages when prerequisites are missing (not Ubuntu, no sudo, Python too old).
- Update README to recommend `./install.sh` as the primary install path; keep manual steps as fallback.
- Document Ollama as a post-install prerequisite (script prints hints; does not install Ollama).

**Out of scope:** Flatpak, `.deb` package, installing Ollama or pulling models, configuring global shortcuts automatically.

## Capabilities

### New Capabilities

- `easy-install`: Behavior and UX of the `install.sh` one-command installer.

### Modified Capabilities

- `project-scaffold`: README SHALL document `install.sh` as the recommended install path.
- `gnome-integration`: Desktop entry and icon installation SHALL be performable via `install.sh` (not only manual `cp` commands).

## Impact

- **New files:** `install.sh`
- **Updated:** `README.md`
- **User systems:** writes to `~/.local/share/applications/`, `~/.local/share/icons/`, project `.venv/`, may invoke `sudo apt` on Ubuntu

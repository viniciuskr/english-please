## Context

`start-project` delivered a working app with manual README steps for apt, venv, pip, and GNOME file copies. PRD **M5** requests packaging convenience; this change adds `install.sh` without Flatpak or system packages.

Target user: Ubuntu 24.04 / GNOME, comfortable with `sudo apt`, wants clone → one command → app in menu.

## Goals / Non-Goals

**Goals:**

- Single `./install.sh` for Ubuntu/GNOME local install.
- Idempotent re-runs.
- `--help` and `--dry-run`.
- Desktop `Exec` points at a reliable path (venv binary).
- README updated to lead with the script.

**Non-Goals:**

- Flatpak, snap, `.deb`.
- Installing or configuring Ollama.
- Auto-binding `Super+E`.
- macOS/Windows support.

## Decisions

### Shell: bash with `set -euo pipefail`

POSIX-ish bash for broad Linux compatibility. Fail fast on errors; print actionable messages.

**Alternative:** Makefile target — less discoverable for end users.

### OS detection: `/etc/os-release` + `apt-get`

If `ID`/`ID_LIKE` indicates Debian/Ubuntu, use `apt-get install -y` for a fixed package list matching README. Otherwise exit 1 with manual instructions.

Package list (same as README):

```
python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 \
libgirepository-2.0-dev gcc libcairo2-dev pkg-config python3-venv python3-pip
```

Add `python3-venv` and `python3-pip` explicitly for venv creation.

### Venv: project-local `.venv`

Use `/usr/bin/python3` (or `python3.12` if `python3 --version` < 3.12) to create `.venv`, then `.venv/bin/pip install -e .`.

**Desktop Exec:** Write `Exec=/absolute/path/to/repo/.venv/bin/english-please` in the installed `.desktop` file so the menu works without activating the venv (more reliable than bare `english-please` on PATH).

**Alternative:** Install into `~/.local/bin` via pip `--user` — conflicts with PEP 668 on some systems; venv is cleaner.

### Desktop install: copy + patch Exec

1. Copy `data/com.viniciuskr.EnglishPlease.desktop` to `~/.local/share/applications/`.
2. Replace or set `Exec=` to absolute venv path using `sed` or heredoc.
3. Copy SVG to `~/.local/share/icons/hicolor/scalable/apps/`.
4. Run `update-desktop-database ~/.local/share/applications/` if command exists.

### Flags

| Flag | Behavior |
|------|----------|
| `--help` | Usage, options, manual fallback link |
| `--dry-run` | Echo each step, no writes/sudo |

### Script structure

```
install.sh
├── parse_args
├── detect_os / require_ubuntu
├── install_apt_packages
├── ensure_venv
├── pip_install_editable
├── install_desktop_files
└── print_success_message
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| `sudo` prompts scare users | Print package list before apt; support `--dry-run` |
| Non-Ubuntu users blocked | Clear message + README fallback |
| PyGObject pip build still fails | apt dev packages installed first; README manual path |
| Desktop Exec path breaks if repo moved | Re-run `install.sh` after move; document in success message |

## Migration Plan

Existing manual installs: running `install.sh` is safe (refreshes venv pip install and desktop files). No data migration.

## Open Questions

- Whether to add `~/.local/bin` symlink to `english-please` for terminal use without `source .venv/bin/activate` — recommended as optional post-install step in success message.

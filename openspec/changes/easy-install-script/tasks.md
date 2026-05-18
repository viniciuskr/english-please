## 1. Install script core

- [x] 1.1 Create `install.sh` with `set -euo pipefail`, `--help`, and `--dry-run`
- [x] 1.2 Implement Ubuntu/Debian detection and apt package install block
- [x] 1.3 Implement venv creation and `pip install -e .` using project `.venv`
- [x] 1.4 Make script executable (`chmod +x`) and idempotent on re-run

## 2. GNOME desktop install

- [x] 2.1 Copy and install `.desktop` with absolute `Exec` path to `.venv/bin/english-please`
- [x] 2.2 Copy icon to `~/.local/share/icons/hicolor/scalable/apps/`
- [x] 2.3 Run `update-desktop-database` when available

## 3. UX and errors

- [x] 3.1 Add non-Ubuntu exit path with package list and README pointer
- [x] 3.2 Add Python version check (3.12+)
- [x] 3.3 Print success message: run command, Ollama hints, Super+E reminder

## 4. Documentation

- [x] 4.1 Update README: `./install.sh` as recommended install; manual steps as fallback
- [x] 4.2 Document `--dry-run` and `--help` in README

## 5. Verification

- [x] 5.1 Run `./install.sh --dry-run` and verify output lists expected steps
- [x] 5.2 Run `./install.sh` on Ubuntu (or verify script syntax with `bash -n`)
- [x] 5.3 Confirm installed `.desktop` has correct absolute `Exec` path

## ADDED Requirements

### Requirement: One-command install script exists

The repository SHALL provide an executable `install.sh` at the project root that performs a full local install when run from the repository directory.

#### Scenario: User runs install from repo root

- **WHEN** the user executes `./install.sh` from the repository root on a supported system
- **THEN** the script SHALL complete all install steps without requiring additional copy-paste commands from the README

### Requirement: System dependencies on Ubuntu

On Debian/Ubuntu systems, the script SHALL install required GTK/PyGObject build and runtime packages via `apt` when they are not already present, using `sudo` only when needed.

#### Scenario: Missing apt packages

- **WHEN** required packages (e.g. `python3-gi`, `gir1.2-adw-1`) are not installed
- **THEN** the script SHALL install them via `apt` before proceeding to the Python install

#### Scenario: Non-Debian system

- **WHEN** the script detects a non-apt-based distribution
- **THEN** it SHALL exit with a clear message listing required packages and pointing to the README manual steps

### Requirement: Python virtualenv and package install

The script SHALL create a project-local `.venv` (if missing), install the package in editable mode with `pip install -e .`, and ensure the `english-please` console script is available via `.venv/bin/english-please`.

#### Scenario: Fresh clone install

- **WHEN** `.venv` does not exist
- **THEN** the script SHALL create it and install the application so `.venv/bin/english-please` runs successfully

#### Scenario: Re-run on existing install

- **WHEN** the user runs `install.sh` again after a previous successful install
- **THEN** the script SHALL be idempotent (re-install package, refresh desktop files, no destructive side effects)

### Requirement: GNOME desktop integration

The script SHALL install `data/com.viniciuskr.EnglishPlease.desktop` and the application icon into the user's local share directories and run `update-desktop-database` when available.

#### Scenario: Desktop entry installed

- **WHEN** install completes successfully
- **THEN** `~/.local/share/applications/com.viniciuskr.EnglishPlease.desktop` SHALL exist and reference `english-please` on the user's PATH or an absolute path to `.venv/bin/english-please`

### Requirement: Helpful completion output

On success, the script SHALL print how to run the app (activate venv or PATH hint), that Ollama must be running, and a reminder about optional `Super+E` shortcut setup.

#### Scenario: Successful install

- **WHEN** all steps succeed
- **THEN** the script SHALL print next steps including `english-please` launch command and `ollama serve` / `ollama pull` hints

### Requirement: Dry-run and help flags

The script SHALL support `--help` (usage text) and `--dry-run` (print planned actions without modifying the system).

#### Scenario: Dry run

- **WHEN** the user passes `--dry-run`
- **THEN** the script SHALL list commands it would run and exit 0 without installing

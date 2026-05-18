## MODIFIED Requirements

### Requirement: README documents development setup

The repository README SHALL document: Python version requirement, system packages needed for GTK 4 / libadwaita (PyGObject), editable install command, how to run the app, and that Ollama must be running on `localhost:11434` for review to work. The README SHALL list `./install.sh` as the **recommended** install path for Ubuntu/GNOME users, with manual steps retained as a fallback.

#### Scenario: New developer follows README

- **WHEN** a developer follows the README setup steps on a supported GNOME system
- **THEN** they SHALL be able to launch the app without undocumented manual steps

#### Scenario: README recommends install script

- **WHEN** a user reads the install section of the README
- **THEN** they SHALL see `./install.sh` documented before the manual venv/apt/desktop steps

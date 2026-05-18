## ADDED Requirements

### Requirement: Python project is installable and runnable

The project SHALL provide a `pyproject.toml` targeting Python 3.12 or newer with declared runtime dependencies (PyGObject, aiohttp) and a console script entry point named `english-please` that launches the application.

#### Scenario: Developer runs the app from source

- **WHEN** the developer installs the package in editable mode and runs `english-please`
- **THEN** the GTK application window opens without import errors

### Requirement: Package layout follows a single source tree

The application code SHALL live under `src/english_please/` as an importable package with a `main` module as the entry point.

#### Scenario: Entry point resolves package

- **WHEN** the `english-please` console script is invoked
- **THEN** it SHALL execute `english_please.main:main` (or equivalent documented entry)

### Requirement: Config directory and default file

The application SHALL use `~/.config/english-please/config.json` for persisted settings. On first access, the app SHALL create the config directory and a default JSON file containing at least: `model` (default `llama3.2:latest`), `review_command` (empty string), and `post_review_command` (empty string).

#### Scenario: First launch creates config

- **WHEN** the app starts and the config file does not exist
- **THEN** the app SHALL create `~/.config/english-please/config.json` with the default keys and values

### Requirement: README documents development setup

The repository README SHALL document: Python version requirement, system packages needed for GTK 4 / libadwaita (PyGObject), editable install command, how to run the app, and that Ollama must be running on `localhost:11434` for review to work.

#### Scenario: New developer follows README

- **WHEN** a developer follows the README setup steps on a supported GNOME system
- **THEN** they SHALL be able to launch the app without undocumented manual steps

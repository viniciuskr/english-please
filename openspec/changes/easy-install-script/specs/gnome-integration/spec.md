## MODIFIED Requirements

### Requirement: Desktop entry for applications menu

The repository SHALL ship a `.desktop` file at `data/com.viniciuskr.EnglishPlease.desktop` with at minimum: `Name=English, Please`, `Exec=english-please`, `Icon=com.viniciuskr.EnglishPlease`, `Type=Application`, `Categories=Utility;`, and `StartupWMClass=com.viniciuskr.EnglishPlease`. The desktop entry and icon SHALL be installable via `./install.sh` into the user's local GNOME applications directory without manual `cp` commands.

#### Scenario: Desktop file validates

- **WHEN** the `.desktop` file is installed to `~/.local/share/applications/` (via `install.sh` or per README)
- **THEN** GNOME SHALL list "English, Please" in the applications menu

#### Scenario: Install script installs desktop entry

- **WHEN** the user runs `./install.sh` successfully
- **THEN** the applications menu entry SHALL be available without separate manual copy steps

### Requirement: Placeholder application icon

The repository SHALL include a placeholder icon resource referenced by the desktop file (e.g., under `data/icons/`) so the menu entry is not iconless before custom branding. The icon SHALL be installable via `./install.sh` into `~/.local/share/icons/hicolor/scalable/apps/`.

#### Scenario: Icon path documented

- **WHEN** the developer follows README install steps for the icon
- **THEN** the applications menu entry SHALL display the placeholder icon

#### Scenario: Install script installs icon

- **WHEN** the user runs `./install.sh` successfully
- **THEN** the placeholder icon SHALL be installed to the user's local icon theme path

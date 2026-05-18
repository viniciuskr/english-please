# gnome-integration Specification

## Purpose
TBD - created by archiving change start-project. Update Purpose after archive.
## Requirements
### Requirement: Stable application ID

The application SHALL register with `application_id` `com.viniciuskr.EnglishPlease` via `Gtk.Application` / `Adw.Application`.

#### Scenario: Application registers D-Bus name

- **WHEN** the app starts
- **THEN** it SHALL use `com.viniciuskr.EnglishPlease` as its application ID for single-instance behavior

### Requirement: Single instance with focus on re-launch

Only one application instance SHALL run at a time. A second launch (e.g., from the applications menu or `english-please` while already running) SHALL activate the existing instance and present its window rather than opening a duplicate.

#### Scenario: Second launch focuses existing window

- **WHEN** the app is already running and the user starts `english-please` again
- **THEN** the existing window SHALL be brought to the foreground and no second main window SHALL appear

### Requirement: Desktop entry for applications menu

The repository SHALL ship a `.desktop` file at `data/com.viniciuskr.EnglishPlease.desktop` with at minimum: `Name=English, Please`, `Exec=english-please`, `Icon=com.viniciuskr.EnglishPlease`, `Type=Application`, `Categories=Utility;`, and `StartupWMClass=com.viniciuskr.EnglishPlease`.

#### Scenario: Desktop file validates

- **WHEN** the `.desktop` file is installed to `~/.local/share/applications/` (per README)
- **THEN** GNOME SHALL list "English, Please" in the applications menu

### Requirement: Placeholder application icon

The repository SHALL include a placeholder icon resource referenced by the desktop file (e.g., under `data/icons/`) so the menu entry is not iconless before custom branding.

#### Scenario: Icon path documented

- **WHEN** the developer follows README install steps for the icon
- **THEN** the applications menu entry SHALL display the placeholder icon

### Requirement: Global shortcut documented only

The README SHALL document a suggested global shortcut (`Super+E`) and how to bind it in GNOME Settings. Wiring the shortcut in code is out of scope for this change.

#### Scenario: README mentions shortcut setup

- **WHEN** a user reads the GNOME integration section of the README
- **THEN** they SHALL find instructions to configure `Super+E` manually without requiring in-app shortcut registration


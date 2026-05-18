## ADDED Requirements

### Requirement: Main window layout

The application SHALL present a primary window approximately 600×700 pixels containing: a header with the title "English, Please", a multi-line text input for English text, action buttons (at minimum **Review** and **Clear**), and a read-only result area below a "Result" separator.

#### Scenario: Window opens with expected regions

- **WHEN** the application activates
- **THEN** the user SHALL see an input area, Review and Clear controls, and an empty result area

### Requirement: Review triggers Ollama and shows plain output

Pressing **Review** or `Ctrl+Enter` SHALL read the input text, call the Ollama client, and display the outcome in the result area. For this milestone, the result MAY be prettified JSON or a simple text summary of `status` — structured OK / corrected / issues panels are explicitly deferred.

#### Scenario: Review with Ollama running

- **WHEN** the user enters text, presses Review, and Ollama returns valid JSON
- **THEN** the result area SHALL update to show the review outcome (e.g., formatted JSON or status line) within the same window

#### Scenario: Review while busy

- **WHEN** a review is already in progress
- **THEN** the Review control SHALL be disabled or otherwise prevent duplicate concurrent requests until the current review finishes

### Requirement: Clear resets the session

Pressing **Clear** or `Ctrl+L` SHALL empty the input field and clear the result area.

#### Scenario: User clears after a review

- **WHEN** the user presses Clear or `Ctrl+L`
- **THEN** both input and result areas SHALL be empty and ready for new text

### Requirement: Errors appear in the result area

When the Ollama client or validation fails, the application SHALL display the error message in the result area (not only on stderr).

#### Scenario: Ollama is down

- **WHEN** review is triggered and the Ollama client reports a connection error
- **THEN** the result area SHALL show the friendly error message including the `ollama serve` hint

### Requirement: libadwaita and system theme

The UI SHALL use GTK 4 with libadwaita (`Adw.Application`, `Adw.ApplicationWindow` or equivalent) so the app follows the system light/dark theme and standard GNOME styling.

#### Scenario: App respects system theme

- **WHEN** the user runs the app on a GNOME desktop with dark mode enabled
- **THEN** the window chrome and widgets SHALL follow libadwaita theming without custom hard-coded colors blocking theme adoption

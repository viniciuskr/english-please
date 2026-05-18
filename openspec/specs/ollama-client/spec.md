# ollama-client Specification

## Purpose
TBD - created by archiving change start-project. Update Purpose after archive.
## Requirements
### Requirement: Review via Ollama chat API

The Ollama client SHALL send a `POST` request to `http://localhost:11434/api/chat` with `stream: true` and `format: json`, using the model name from config (default `llama3.2:latest`). The request SHALL include a system prompt that instructs the model to return only a JSON object matching the PRD schema:

```json
{
  "status": "ok" | "needs_changes",
  "corrected": "<string>",
  "issues": [{"original": "...", "fix": "...", "explanation": "..."}]
}
```

#### Scenario: Successful review returns parsed result

- **WHEN** Ollama is running, the configured model is available, and the user submits non-empty English text
- **THEN** the client SHALL consume the streamed response, assemble the full message content, parse it as JSON, and return a structured result with `status`, `corrected`, and `issues` fields

### Requirement: Connection failure is reported clearly

If Ollama is not reachable (e.g., connection refused on port 11434), the client SHALL raise or return an error that includes a user-facing message and a hint to run `ollama serve`.

#### Scenario: Ollama is not running

- **WHEN** the user triggers a review and nothing is listening on `localhost:11434`
- **THEN** the client SHALL NOT crash silently and SHALL surface an error indicating Ollama is unavailable with remediation text

### Requirement: Malformed JSON is handled gracefully

If the assembled response is not valid JSON, the client SHALL return an error describing a parse failure rather than propagating an unhandled exception to the UI layer.

#### Scenario: Model returns non-JSON text

- **WHEN** the stream completes but the content cannot be parsed as JSON
- **THEN** the client SHALL return a parse error suitable for display in the result area

### Requirement: Empty input is rejected before the API call

The client or its caller SHALL NOT send a review request when the input text is empty or whitespace-only.

#### Scenario: User submits empty text

- **WHEN** review is triggered with no substantive input
- **THEN** the app SHALL show a validation message without calling Ollama


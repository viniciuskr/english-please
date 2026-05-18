## 1. Project scaffold

- [x] 1.1 Add `pyproject.toml` (Python 3.12+, PyGObject, aiohttp, `english-please` entry point)
- [x] 1.2 Create `src/english_please/` package with `__init__.py` and `main.py` stub
- [x] 1.3 Update `.gitignore` for Python build artifacts (`__pycache__`, `*.egg-info`, `.venv`)
- [x] 1.4 Expand `README.md` with system deps, editable install, and run instructions

## 2. Configuration

- [x] 2.1 Implement `config.py` — load/save `~/.config/english-please/config.json`
- [x] 2.2 Ensure defaults: `model`, `review_command`, `post_review_command` on first run

## 3. Ollama client

- [x] 3.1 Add PRD system prompt and `ReviewResult` dataclass in `ollama.py`
- [x] 3.2 Implement streaming `POST /api/chat` with `format: json` via `aiohttp`
- [x] 3.3 Assemble stream chunks, parse JSON, map `status` / `corrected` / `issues`
- [x] 3.4 Return friendly connection error when Ollama is unreachable
- [x] 3.5 Reject empty/whitespace input before calling the API

## 4. Desktop app shell

- [x] 4.1 Implement `Adw.Application` in `main.py` with `com.viniciuskr.EnglishPlease`
- [x] 4.2 Build `Adw.ApplicationWindow` — input (`TextView`), Review, Clear, result area
- [x] 4.3 Wire `Ctrl+Enter` → review, `Ctrl+L` → clear
- [x] 4.4 Disable Review while a review is in progress; re-enable on completion

## 5. Wire review flow

- [x] 5.1 Connect Review button to async Ollama call (`asyncio` + `GLib.idle_add` for UI updates)
- [x] 5.2 Display prettified JSON or status summary in result area on success
- [x] 5.3 Display validation and Ollama errors in result area on failure

## 6. GNOME integration

- [x] 6.1 Implement single-instance: second launch presents existing window
- [x] 6.2 Add `data/com.viniciuskr.EnglishPlease.desktop` with correct `Exec` and `Icon`
- [x] 6.3 Add placeholder icon under `data/icons/` and document install in README
- [x] 6.4 Document suggested `Super+E` global shortcut setup in README

## 7. Smoke test

- [x] 7.1 Verify `pip install -e .` and `english-please` opens the window
- [x] 7.2 With Ollama stopped — review shows connection error with `ollama serve` hint
- [x] 7.3 With Ollama running — review returns and displays parsed JSON for sample text
- [x] 7.4 Launch app twice — second launch focuses existing window, no duplicate

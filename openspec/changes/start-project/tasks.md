## 1. Project scaffold

- [ ] 1.1 Add `pyproject.toml` (Python 3.12+, PyGObject, aiohttp, `english-please` entry point)
- [ ] 1.2 Create `src/english_please/` package with `__init__.py` and `main.py` stub
- [ ] 1.3 Update `.gitignore` for Python build artifacts (`__pycache__`, `*.egg-info`, `.venv`)
- [ ] 1.4 Expand `README.md` with system deps, editable install, and run instructions

## 2. Configuration

- [ ] 2.1 Implement `config.py` — load/save `~/.config/english-please/config.json`
- [ ] 2.2 Ensure defaults: `model`, `review_command`, `post_review_command` on first run

## 3. Ollama client

- [ ] 3.1 Add PRD system prompt and `ReviewResult` dataclass in `ollama.py`
- [ ] 3.2 Implement streaming `POST /api/chat` with `format: json` via `aiohttp`
- [ ] 3.3 Assemble stream chunks, parse JSON, map `status` / `corrected` / `issues`
- [ ] 3.4 Return friendly connection error when Ollama is unreachable
- [ ] 3.5 Reject empty/whitespace input before calling the API

## 4. Desktop app shell

- [ ] 4.1 Implement `Adw.Application` in `main.py` with `com.viniciuskr.EnglishPlease`
- [ ] 4.2 Build `Adw.ApplicationWindow` — input (`TextView`), Review, Clear, result area
- [ ] 4.3 Wire `Ctrl+Enter` → review, `Ctrl+L` → clear
- [ ] 4.4 Disable Review while a review is in progress; re-enable on completion

## 5. Wire review flow

- [ ] 5.1 Connect Review button to async Ollama call (`asyncio` + `GLib.idle_add` for UI updates)
- [ ] 5.2 Display prettified JSON or status summary in result area on success
- [ ] 5.3 Display validation and Ollama errors in result area on failure

## 6. GNOME integration

- [ ] 6.1 Implement single-instance: second launch presents existing window
- [ ] 6.2 Add `data/com.viniciuskr.EnglishPlease.desktop` with correct `Exec` and `Icon`
- [ ] 6.3 Add placeholder icon under `data/icons/` and document install in README
- [ ] 6.4 Document suggested `Super+E` global shortcut setup in README

## 7. Smoke test

- [ ] 7.1 Verify `pip install -e .` and `english-please` opens the window
- [ ] 7.2 With Ollama stopped — review shows connection error with `ollama serve` hint
- [ ] 7.3 With Ollama running — review returns and displays parsed JSON for sample text
- [ ] 7.4 Launch app twice — second launch focuses existing window, no duplicate

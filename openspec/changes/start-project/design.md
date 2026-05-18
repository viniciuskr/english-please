## Context

Greenfield repository with [PRD.md](../../../PRD.md) as the product source of truth. Target stack: Python 3.12, GTK 4 + libadwaita via PyGObject, `aiohttp` for non-blocking HTTP to Ollama at `127.0.0.1:11434`. Single user (Vinicius), GNOME on Linux, offline-only.

This change delivers PRD milestones **M0** (Ollama spike), **M1** (minimal UI with plain output), and **partial M3** (desktop entry, single-instance, README shortcut docs).

## Goals / Non-Goals

**Goals:**

- Runnable `english-please` command opening a libadwaita window.
- End-to-end path: paste text → Review → Ollama JSON response shown in result area.
- Config file created on first run; model name read from config.
- Single-instance GTK app with `.desktop` + placeholder icon.

**Non-Goals:**

- Structured panels for `ok` vs `needs_changes` (M2).
- Streaming live preview in the UI (consume stream internally, show final result only).
- Model dropdown, Settings dialog, custom `review_command` / `post_review_command` (M4).
- Flatpak or `install.sh` (M5).
- In-app global shortcut registration.

## Decisions

### Package layout: `src/english_please/`

| Module | Responsibility |
|--------|----------------|
| `main.py` | `Adw.Application` subclass, `application_id`, `run()` entry |
| `window.py` | `Adw.ApplicationWindow`, widgets, signals, calls into Ollama |
| `ollama.py` | `aiohttp` client, prompt, stream assembly, JSON parse |
| `config.py` | Load/save `~/.config/english-please/config.json` |

**Rationale:** Small, flat package keeps M1 simple. Splitting Ollama from UI allows unit-testing JSON parsing later without GTK.

**Alternative considered:** Single `app.py` file — rejected to avoid a monolith before M2 adds result rendering.

### Async: `asyncio` + `aiohttp` on GLib main loop

Review runs in `asyncio.create_task()` from a sync GTK callback. Use one shared `aiohttp.ClientSession` per app lifetime (created on first review or at startup). Completion callbacks marshal UI updates with `GLib.idle_add()` so widgets are touched only on the main thread.

**Rationale:** PRD requires non-blocking HTTP; blocking `urllib` would freeze the UI during LLM latency.

**Alternative considered:** `threading` + sync HTTP — works but harder to cancel and less aligned with future streaming UI.

### Ollama: stream internally, display final JSON

Even though FR-10 streaming UI is deferred, the client SHALL use `stream: true`, accumulate `message.content` chunks, then parse the full string as JSON once complete. This matches production API usage and avoids refactoring the HTTP layer in M2.

Default system prompt copied from PRD §10 (proofreader JSON schema). Request body includes `format: "json"` and `model` from config.

### M1 result display: prettified JSON

`window.py` shows `json.dumps(result, indent=2)` or a one-line summary (`status: ok`) in a read-only `Gtk.TextView` inside a `Gtk.ScrolledWindow`. No `Adw.StatusPage` / stamp UI yet.

**Rationale:** Validates the full pipeline before investing in panel layout.

### Single instance: `Gtk.Application` non-unique

Use default `Gio.Application` behavior: registering the same `application_id` prevents a second process. On second `activate`, call `present()` on the existing window.

### Packaging v1: `pyproject.toml` + manual desktop install

`[project.scripts] english-please = "english_please.main:main"`. README documents:

```bash
pip install -e .
cp data/com.viniciuskr.EnglishPlease.desktop ~/.local/share/applications/
# icon install steps
```

No Flatpak manifest in this change.

### Config defaults

```json
{
  "model": "llama3.2:latest",
  "review_command": "",
  "post_review_command": ""
}
```

`review_command` empty means use built-in Ollama client (only path implemented in this change).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| LLM returns malformed JSON | `format: "json"` on request; catch `json.JSONDecodeError` and show parse error in result area |
| PyGObject / GTK version mismatch on older distros | README states minimum: Ubuntu 24.04 / GNOME 46+ |
| `aiohttp` event loop vs GTK | Single loop via `asyncio` default; document if nested loop issues arise on some distros |
| Plain JSON output feels unfinished | Intentional for M1; M2 change replaces with structured panels |
| Placeholder icon quality | Acceptable for bootstrap; branding deferred to v2 |

## Migration Plan

N/A — greenfield. Developers clone, `pip install -e .`, install `.desktop`, ensure `ollama serve` is running.

## Open Questions

- Whether to add a minimal loading spinner vs disabled Review button only (either satisfies "busy" spec; implement button disable first).
- Exact system package names for README (`python3-gi`, `gir1.2-adw-1`, etc.) — document what was verified on Ubuntu 24.04.

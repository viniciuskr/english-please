# English, Please

Offline GNOME desktop app for English proofreading using a local [Ollama](https://ollama.com) LLM. Paste text, press **Review**, and get structured JSON feedback — no cloud, no account.

## Requirements

- **OS:** Linux with GNOME (tested on Ubuntu 24.04 / GNOME 46+)
- **Python:** 3.12+
- **Ollama:** running locally on `http://localhost:11434` with a model installed (default: `llama3.2:latest`)

### System packages (Ubuntu 24.04)

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 \
  libgirepository-2.0-dev gcc libcairo2-dev pkg-config
```

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Ensure Ollama is running:

```bash
ollama serve
# In another terminal, if needed:
ollama pull llama3.2
```

Run the app:

```bash
english-please
```

## GNOME integration

### Applications menu

```bash
cp data/com.viniciuskr.EnglishPlease.desktop ~/.local/share/applications/
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
cp data/icons/com.viniciuskr.EnglishPlease.svg \
  ~/.local/share/icons/hicolor/scalable/apps/com.viniciuskr.EnglishPlease.svg
update-desktop-database ~/.local/share/applications/
```

### Global shortcut (suggested: Super+E)

1. Open **Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts**
2. Add a shortcut named `English, Please` with command `english-please`
3. Assign **Super+E** (or your preferred binding)

Pressing the shortcut while the app is already running focuses the existing window (single-instance).

## Configuration

Stored at `~/.config/english-please/config.json`:

```json
{
  "model": "llama3.2:latest",
  "review_command": "",
  "post_review_command": ""
}
```

When `review_command` is empty, the built-in Ollama HTTP client is used.

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Review |
| `Ctrl+L` | Clear input and result |

## License

MIT — see [LICENSE](LICENSE).

"""Load and save application configuration."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "english-please"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "model": "llama3.2:latest",
    "review_command": "",
    "post_review_command": "",
}


@dataclass
class Config:
    model: str = DEFAULTS["model"]
    review_command: str = DEFAULTS["review_command"]
    post_review_command: str = DEFAULTS["post_review_command"]


def load_config() -> Config:
    """Load config from disk, creating defaults on first access."""
    if not CONFIG_FILE.exists():
        config = Config()
        save_config(config)
        return config

    data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return Config(
        model=data.get("model", DEFAULTS["model"]),
        review_command=data.get("review_command", DEFAULTS["review_command"]),
        post_review_command=data.get(
            "post_review_command", DEFAULTS["post_review_command"]
        ),
    )


def save_config(config: Config) -> None:
    """Persist config to ~/.config/english-please/config.json."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(asdict(config), indent=2) + "\n",
        encoding="utf-8",
    )

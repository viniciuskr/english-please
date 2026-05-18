"""Ollama HTTP client for English review."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

import aiohttp

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """You are an English proofreader. The user will provide a text written by a non-native English speaker. Respond ONLY with a JSON object of the form:
{
  "status": "ok" | "needs_changes",
  "corrected": "<full corrected text if needs_changes, else empty>",
  "issues": [
    {"original": "...", "fix": "...", "explanation": "..."}
  ]
}
If the text is already correct in grammar, spelling, and natural usage, return status "ok" and empty corrected/issues."""


@dataclass
class ReviewIssue:
    original: str
    fix: str
    explanation: str


@dataclass
class ReviewResult:
    status: str
    corrected: str
    issues: list[ReviewIssue] = field(default_factory=list)


class OllamaError(Exception):
    """Base error for Ollama client failures."""


class EmptyInputError(OllamaError):
    """Raised when review is requested with no substantive text."""


class OllamaConnectionError(OllamaError):
    """Raised when Ollama is not reachable."""


class OllamaParseError(OllamaError):
    """Raised when the model response is not valid JSON."""


def validate_input(text: str) -> str:
    """Return stripped text or raise if empty."""
    stripped = text.strip()
    if not stripped:
        raise EmptyInputError("Please enter some text to review.")
    return stripped


async def review_text(
    session: aiohttp.ClientSession,
    text: str,
    model: str,
) -> ReviewResult:
    """Send text to Ollama and return a parsed review result."""
    payload = validate_input(text)

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": payload},
        ],
        "stream": True,
        "format": "json",
    }

    try:
        async with session.post(OLLAMA_CHAT_URL, json=body) as response:
            if response.status != 200:
                detail = await response.text()
                raise OllamaError(
                    f"Ollama returned HTTP {response.status}: {detail[:200]}"
                )

            content_parts: list[str] = []
            while True:
                raw_line = await response.content.readline()
                if not raw_line:
                    break
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue
                message = chunk.get("message") or {}
                part = message.get("content")
                if part:
                    content_parts.append(part)
                if chunk.get("done"):
                    break

    except aiohttp.ClientConnectorError as exc:
        raise OllamaConnectionError(
            "Cannot connect to Ollama. Is it running?\n\n"
            "Start it with: ollama serve"
        ) from exc
    except aiohttp.ClientError as exc:
        raise OllamaError(f"Network error talking to Ollama: {exc}") from exc

    raw = "".join(content_parts).strip()
    if not raw:
        raise OllamaParseError("Ollama returned an empty response.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise OllamaParseError(
            f"Could not parse model output as JSON.\n\nRaw response:\n{raw[:500]}"
        ) from exc

    issues = [
        ReviewIssue(
            original=item.get("original", ""),
            fix=item.get("fix", ""),
            explanation=item.get("explanation", ""),
        )
        for item in data.get("issues") or []
    ]

    return ReviewResult(
        status=data.get("status", "needs_changes"),
        corrected=data.get("corrected", ""),
        issues=issues,
    )

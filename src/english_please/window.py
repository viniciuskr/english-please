"""Main application window."""

from __future__ import annotations

import asyncio
import json
import threading
from typing import TYPE_CHECKING

import aiohttp
from gi.repository import Adw, GLib, Gtk

from english_please.config import Config, load_config
from english_please.ollama import (
    OllamaError,
    ReviewResult,
    review_text,
)

if TYPE_CHECKING:
    from english_please.main import EnglishPleaseApp


class MainWindow(Adw.ApplicationWindow):
    """Primary window: input, review actions, and plain JSON result."""

    def __init__(self, application: EnglishPleaseApp) -> None:
        super().__init__(application=application, title="English, Please")
        self.set_default_size(600, 700)

        self._config: Config = load_config()
        self._review_in_progress = False

        self._build_ui()
        self._connect_signals()
        self._install_shortcuts()

    def _build_ui(self) -> None:
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(outer)

        header = Adw.HeaderBar()
        title = Gtk.Label(label="English, Please")
        title.add_css_class("title")
        header.set_title_widget(title)
        outer.append(header)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
            hexpand=True,
            vexpand=True,
        )
        outer.append(content)

        input_frame = Gtk.Frame()
        input_frame.add_css_class("card")
        input_scroll = Gtk.ScrolledWindow(
            min_content_height=180,
            hexpand=True,
            vexpand=True,
        )
        self._input_view = Gtk.TextView(
            wrap_mode=Gtk.WrapMode.WORD,
            left_margin=8,
            right_margin=8,
            top_margin=8,
            bottom_margin=8,
        )
        self._input_buffer = self._input_view.get_buffer()
        self._input_buffer.set_text("Type or paste your text here...")
        input_scroll.set_child(self._input_view)
        input_frame.set_child(input_scroll)
        content.append(input_frame)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        button_box.set_halign(Gtk.Align.END)
        self._clear_button = Gtk.Button(label="Clear")
        self._review_button = Gtk.Button(label="Review")
        self._review_button.add_css_class("suggested-action")
        button_box.append(self._clear_button)
        button_box.append(self._review_button)
        content.append(button_box)

        result_label = Gtk.Label(label="Result", xalign=0)
        result_label.add_css_class("heading")
        content.append(result_label)

        result_frame = Gtk.Frame()
        result_frame.add_css_class("card")
        result_scroll = Gtk.ScrolledWindow(
            min_content_height=160,
            hexpand=True,
            vexpand=True,
        )
        self._result_view = Gtk.TextView(
            editable=False,
            wrap_mode=Gtk.WrapMode.WORD,
            left_margin=8,
            right_margin=8,
            top_margin=8,
            bottom_margin=8,
        )
        self._result_buffer = self._result_view.get_buffer()
        result_scroll.set_child(self._result_view)
        result_frame.set_child(result_scroll)
        content.append(result_frame)

    def _connect_signals(self) -> None:
        self._review_button.connect("clicked", self._on_review_clicked)
        self._clear_button.connect("clicked", self._on_clear_clicked)

    def _install_shortcuts(self) -> None:
        controller = Gtk.ShortcutController()
        controller.set_scope(Gtk.ShortcutScope.GLOBAL)

        controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("<Primary>Return"),
                Gtk.CallbackAction.new(self._on_review_shortcut),
            )
        )
        controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("<Primary>l"),
                Gtk.CallbackAction.new(self._on_clear_shortcut),
            )
        )
        self.add_controller(controller)

    def _on_review_shortcut(self, *_args) -> bool:
        self._on_review_clicked()
        return True

    def _on_clear_shortcut(self, *_args) -> bool:
        self._on_clear_clicked()
        return True

    def _get_input_text(self) -> str:
        start, end = self._input_buffer.get_bounds()
        return self._input_buffer.get_text(start, end, True)

    def _set_result_text(self, text: str) -> None:
        self._result_buffer.set_text(text)

    def _set_review_busy(self, busy: bool) -> None:
        self._review_in_progress = busy
        self._review_button.set_sensitive(not busy)

    def _on_clear_clicked(self, *_args) -> None:
        self._input_buffer.set_text("")
        self._result_buffer.set_text("")

    def _on_review_clicked(self, *_args) -> None:
        if self._review_in_progress:
            return
        self._set_review_busy(True)
        self._set_result_text("Reviewing…")

        text = self._get_input_text()
        model = self._config.model
        app = self.get_application()
        session = app.get_http_session()  # type: ignore[attr-defined]

        def run_in_thread() -> None:
            loop = asyncio.new_event_loop()
            try:
                result = loop.run_until_complete(review_text(session, text, model))
                GLib.idle_add(self._on_review_success, result)
            except OllamaError as exc:
                GLib.idle_add(self._on_review_failure, str(exc))
            except Exception as exc:  # noqa: BLE001
                GLib.idle_add(self._on_review_failure, f"Unexpected error: {exc}")
            finally:
                loop.close()
                GLib.idle_add(self._set_review_busy, False)

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _on_review_success(self, result: ReviewResult) -> bool:
        payload = {
            "status": result.status,
            "corrected": result.corrected,
            "issues": [
                {
                    "original": issue.original,
                    "fix": issue.fix,
                    "explanation": issue.explanation,
                }
                for issue in result.issues
            ],
        }
        self._set_result_text(json.dumps(payload, indent=2))
        return False

    def _on_review_failure(self, message: str) -> bool:
        self._set_result_text(message)
        return False

    def present_window(self) -> None:
        """Bring this window to the foreground."""
        self.present()

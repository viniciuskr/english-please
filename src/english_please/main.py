"""Application entry point."""

from __future__ import annotations

import asyncio
import sys

import gi

gi.require_version("Adw", "1")
import aiohttp
from gi.repository import Adw, GLib

from english_please.window import MainWindow

APP_ID = "com.viniciuskr.EnglishPlease"


class EnglishPleaseApp(Adw.Application):
    """GTK application with single-instance behavior."""

    def __init__(self) -> None:
        super().__init__(application_id=APP_ID)
        self._window: MainWindow | None = None
        self._http_session: aiohttp.ClientSession | None = None

    def get_http_session(self) -> aiohttp.ClientSession:
        if self._http_session is None or self._http_session.closed:
            self._http_session = aiohttp.ClientSession()
        return self._http_session

    def do_activate(self) -> None:
        if self._window is None:
            self._window = MainWindow(application=self)
        self._window.present_window()

    def do_shutdown(self) -> None:
        if self._http_session and not self._http_session.closed:
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._http_session.close())
            finally:
                loop.close()
        super().do_shutdown()


def main() -> int:
    Adw.init()
    app = EnglishPleaseApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())

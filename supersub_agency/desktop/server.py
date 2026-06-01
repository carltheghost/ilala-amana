"""Local HTTP server for the SuperSub visual command deck."""

from __future__ import annotations

import json
import mimetypes
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from supersub_agency.agency import AgencyAgent
from supersub_agency.contracts import TaskRequest
from supersub_agency.desktop.serialize import agency_response_to_dict, capabilities_payload

STATIC_ROOT = Path(__file__).resolve().parent.parent / "static" / "desktop"


class DesktopHandler(BaseHTTPRequestHandler):
    """Serve the 4D UI and JSON API for missions and capabilities."""

    server_version = "SuperSubDesktop/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        if getattr(self.server, "quiet", False):
            return
        super().log_message(format, *args)

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(
        self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            return self._serve_file("index.html")

        if path.startswith("/static/"):
            relative = path.removeprefix("/static/")
            return self._serve_file(relative)

        if path == "/api/capabilities":
            return self._send_json({"providers": capabilities_payload()})

        if path == "/api/health":
            return self._send_json({"status": "ok", "surface": "supersub-4d-desktop"})

        self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/mission":
            self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "invalid JSON"}, HTTPStatus.BAD_REQUEST)
            return

        mission = (data.get("mission") or data.get("text") or "").strip()
        if not mission:
            self._send_json({"error": "mission is required"}, HTTPStatus.BAD_REQUEST)
            return

        budget = data.get("budget_usd", data.get("budget"))
        budget_usd = float(budget) if budget is not None else None

        response = AgencyAgent().handle(TaskRequest(text=mission, budget_usd=budget_usd))
        self._send_json(
            {
                "ok": True,
                "response": agency_response_to_dict(response),
                "markdown": response.as_markdown(),
            }
        )

    def _serve_file(self, relative: str) -> None:
        target = (STATIC_ROOT / relative).resolve()
        if not str(target).startswith(str(STATIC_ROOT.resolve())):
            self._send_json({"error": "forbidden"}, HTTPStatus.FORBIDDEN)
            return
        if not target.is_file():
            self._send_json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return

        content_type, _ = mimetypes.guess_type(str(target))
        content_type = content_type or "application/octet-stream"
        self._send_bytes(target.read_bytes(), content_type)


def run_desktop(
    host: str = "127.0.0.1",
    port: int = 8765,
    *,
    open_browser: bool = True,
    quiet: bool = False,
) -> None:
    """Start the visual command deck and optionally open a browser tab."""

    httpd = ThreadingHTTPServer((host, port), DesktopHandler)
    httpd.quiet = quiet  # type: ignore[attr-defined]

    url = f"http://{host}:{port}/"
    print(f"SuperSub 4D Command Deck → {url}")
    print("Press Ctrl+C to stop.")

    if open_browser:

        def _open() -> None:
            webbrowser.open(url)

        threading.Timer(0.6, _open).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down command deck.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run_desktop()

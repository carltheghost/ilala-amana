"""Tests for the visual command deck HTTP API."""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from supersub_agency.desktop.server import DesktopHandler


class DesktopApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), DesktopHandler)
        cls.port = cls.httpd.server_address[1]
        cls.base = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_health(self) -> None:
        with urllib.request.urlopen(f"{self.base}/api/health") as resp:
            payload = json.loads(resp.read().decode())
        self.assertEqual(payload["status"], "ok")

    def test_capabilities(self) -> None:
        with urllib.request.urlopen(f"{self.base}/api/capabilities") as resp:
            payload = json.loads(resp.read().decode())
        self.assertGreaterEqual(len(payload["providers"]), 5)

    def test_mission(self) -> None:
        body = json.dumps({"mission": "research stocks", "budget_usd": 500}).encode()
        req = urllib.request.Request(
            f"{self.base}/api/mission",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            payload = json.loads(resp.read().decode())
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["response"]["intent"], "finance")

    def test_mission_requires_text(self) -> None:
        body = json.dumps({}).encode()
        req = urllib.request.Request(
            f"{self.base}/api/mission",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)

    def test_index_html(self) -> None:
        with urllib.request.urlopen(f"{self.base}/") as resp:
            html = resp.read().decode()
        self.assertIn("4D Command Deck", html)


if __name__ == "__main__":
    unittest.main()

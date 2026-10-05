import base64
import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

from arbitrage_trail.web import make_server

FIX = Path(__file__).parent / "fixtures"


class WebCase(unittest.TestCase):
    env: dict = {}
    vault: str | None = None

    def setUp(self):
        with mock.patch.dict(os.environ, self.env, clear=False):
            self.httpd = make_server("127.0.0.1", 0, vault=self.vault)
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def req(self, path, data=None, headers=None):
        r = urllib.request.Request(self.base + path, data=data, headers=headers or {}, method="POST" if data else "GET")
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, resp.read(), resp.headers
        except urllib.error.HTTPError as e:
            return e.code, e.read(), e.headers


class TestWeb(WebCase):
    def test_index(self):
        status, body, _ = self.req("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Arbitrage Trail", body)

    def test_convert_json(self):
        status, body, _ = self.req("/api/convert?format=json", (FIX / "claude_conversations.json").read_bytes())
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(len(data["conversations"]), 2)
        self.assertTrue(data["conversations"][0]["markdown"].startswith("---"))

    def test_convert_zip_with_selection(self):
        blob = (FIX / "chatgpt_conversations.json").read_bytes()
        status, body, headers = self.req("/api/convert?format=zip&id=6a1f0c2e-1111-4a2b-9c3d-aaaaaaaaaaaa", blob)
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Type"], "application/zip")
        import io, zipfile

        self.assertEqual(len(zipfile.ZipFile(io.BytesIO(body)).namelist()), 1)

    def test_unknown_format(self):
        status, body, _ = self.req("/api/convert", b'[{"x": 1}]')
        self.assertEqual(status, 422)
        self.assertIn("error", json.loads(body))

    def test_vault_disabled(self):
        status, _, _ = self.req("/api/convert?format=vault", (FIX / "claude_conversations.json").read_bytes())
        self.assertEqual(status, 409)


class TestWebAuth(WebCase):
    env = {"ARBITRAGE_USER": "patrice", "ARBITRAGE_PASSWORD": "secret"}

    def test_requires_auth(self):
        status, _, headers = self.req("/")
        self.assertEqual(status, 401)
        self.assertIn("Basic", headers["WWW-Authenticate"])

    def test_accepts_auth(self):
        token = base64.b64encode(b"patrice:secret").decode()
        status, _, _ = self.req("/", headers={"Authorization": f"Basic {token}"})
        self.assertEqual(status, 200)

    def test_rejects_bad_password(self):
        token = base64.b64encode(b"patrice:faux").decode()
        status, _, _ = self.req("/", headers={"Authorization": f"Basic {token}"})
        self.assertEqual(status, 401)


class TestWebVault(WebCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = self._tmp.name
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self._tmp.cleanup()

    def test_writes_to_vault(self):
        status, body, _ = self.req("/api/convert?format=vault", (FIX / "chatgpt_conversations.json").read_bytes())
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)["written"]), 2)
        self.assertEqual(len(os.listdir(self.vault)), 2)


if __name__ == "__main__":
    unittest.main()

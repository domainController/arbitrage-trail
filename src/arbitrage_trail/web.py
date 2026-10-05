"""Web app minimale, bibliothèque standard uniquement (ADR 0002).

Le navigateur envoie le fichier exporté en corps brut (pas de multipart : le
module `cgi` a disparu de Python 3.13). Le serveur ne garde rien : il convertit
et renvoie, sauf demande explicite d'écriture dans le vault configuré.

Routes :
    GET  /                       page
    GET  /api/config             {"vault": bool, "version": str}
    POST /api/convert?format=json|zip|vault[&source=auto|chatgpt|claude]

Sécurité : écoute sur 127.0.0.1 par défaut. Si ARBITRAGE_USER et
ARBITRAGE_PASSWORD sont définis, Basic Auth obligatoire (à n'utiliser que
derrière HTTPS ; voir docs/infra-vps.md).
"""

from __future__ import annotations

import base64
import hmac
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from urllib.parse import parse_qs, urlparse

from . import __version__, markdown
from .export import to_zip, write_dir
from .loader import load_bytes
from .parsers import PARSERS, UnknownFormat

MAX_BYTES = int(os.environ.get("ARBITRAGE_MAX_MB", "500")) * 1024 * 1024


def _index_html() -> bytes:
    return resources.files("arbitrage_trail").joinpath("static/index.html").read_bytes()


class Handler(BaseHTTPRequestHandler):
    server_version = f"ArbitrageTrail/{__version__}"
    vault: str | None = None
    credentials: tuple[str, str] | None = None

    # --- utilitaires -------------------------------------------------------

    def _send(self, status: int, body: bytes, ctype: str, extra: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def _authorized(self) -> bool:
        if not self.credentials:
            return True
        header = self.headers.get("Authorization", "")
        if header.startswith("Basic "):
            try:
                user, _, pwd = base64.b64decode(header[6:]).decode().partition(":")
            except (ValueError, UnicodeDecodeError):
                return False
            ok_user = hmac.compare_digest(user, self.credentials[0])
            ok_pwd = hmac.compare_digest(pwd, self.credentials[1])
            return ok_user and ok_pwd
        return False

    def _deny(self) -> None:
        self._send(
            HTTPStatus.UNAUTHORIZED,
            b"Authentification requise",
            "text/plain; charset=utf-8",
            {"WWW-Authenticate": 'Basic realm="Arbitrage Trail", charset="UTF-8"'},
        )

    # --- routes ------------------------------------------------------------

    def do_GET(self) -> None:
        if not self._authorized():
            return self._deny()
        path = urlparse(self.path).path
        if path == "/":
            return self._send(HTTPStatus.OK, _index_html(), "text/html; charset=utf-8")
        if path == "/api/config":
            return self._json(HTTPStatus.OK, {"vault": bool(self.vault), "version": __version__})
        self._json(HTTPStatus.NOT_FOUND, {"error": "introuvable"})

    def do_POST(self) -> None:
        if not self._authorized():
            return self._deny()
        url = urlparse(self.path)
        if url.path != "/api/convert":
            return self._json(HTTPStatus.NOT_FOUND, {"error": "introuvable"})
        qs = parse_qs(url.query)
        fmt = qs.get("format", ["json"])[0]
        source = qs.get("source", ["auto"])[0]
        if source not in ("auto", *PARSERS):
            return self._json(HTTPStatus.BAD_REQUEST, {"error": f"source inconnue : {source}"})

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "fichier vide"})
        if length > MAX_BYTES:
            return self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "fichier trop volumineux"})
        blob = self.rfile.read(length)

        try:
            convs = load_bytes(blob, source)
        except UnknownFormat as exc:
            return self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(exc)})

        ids = set(qs.get("id", []))
        if ids:
            convs = [c for c in convs if c.id in ids]

        if fmt == "zip":
            return self._send(
                HTTPStatus.OK,
                to_zip(convs),
                "application/zip",
                {"Content-Disposition": 'attachment; filename="arbitrage-trail.zip"'},
            )
        if fmt == "vault":
            if not self.vault:
                return self._json(HTTPStatus.CONFLICT, {"error": "aucun vault configuré sur le serveur"})
            paths = write_dir(convs, self.vault)
            return self._json(HTTPStatus.OK, {"written": [os.path.basename(p) for p in paths]})

        payload = [
            {
                "id": c.id,
                "source": c.source,
                "title": c.title,
                "created": c.created.isoformat() if c.created else None,
                "messages": len(c.messages),
                "warnings": c.warnings,
                "filename": markdown.filename(c),
                "markdown": markdown.render(c),
            }
            for c in convs
        ]
        self._json(HTTPStatus.OK, {"conversations": payload})


def make_server(host: str, port: int, vault: str | None = None) -> ThreadingHTTPServer:
    user, pwd = os.environ.get("ARBITRAGE_USER"), os.environ.get("ARBITRAGE_PASSWORD")
    handler = type(
        "BoundHandler",
        (Handler,),
        {
            "vault": vault or os.environ.get("ARBITRAGE_VAULT") or None,
            "credentials": (user, pwd) if user and pwd else None,
        },
    )
    return ThreadingHTTPServer((host, port), handler)


def serve(host: str = "127.0.0.1", port: int = 8765, vault: str | None = None) -> None:
    httpd = make_server(host, port, vault)
    auth = "avec authentification" if httpd.RequestHandlerClass.credentials else "sans authentification"
    print(f"Arbitrage Trail sur http://{host}:{port} ({auth})")
    if host not in ("127.0.0.1", "localhost", "::1") and not httpd.RequestHandlerClass.credentials:
        print("ATTENTION : écoute hors localhost sans authentification. Voir docs/infra-vps.md.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

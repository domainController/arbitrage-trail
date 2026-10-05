"""Entrée : octets d'un fichier exporté (JSON brut ou zip d'export) -> conversations."""

from __future__ import annotations

import io
import json
import zipfile

from .model import Conversation
from .parsers import PARSERS, UnknownFormat, detect


def _json_from_zip(blob: bytes) -> object:
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        names = [n for n in zf.namelist() if n.rsplit("/", 1)[-1] == "conversations.json"]
        if not names:
            raise UnknownFormat("Archive sans fichier conversations.json.")
        # Le plus court chemin : celui à la racine de l'export.
        with zf.open(sorted(names, key=len)[0]) as fh:
            return json.load(fh)


def load_bytes(blob: bytes, source: str = "auto") -> list[Conversation]:
    if blob[:2] == b"PK":
        data = _json_from_zip(blob)
    else:
        try:
            data = json.loads(blob.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise UnknownFormat(f"Fichier illisible (ni JSON, ni zip) : {exc}") from exc
    if source == "auto":
        source = detect(data)
    if source not in PARSERS:
        raise UnknownFormat(f"Source inconnue : {source}")
    return PARSERS[source](data)


def load_path(path: str, source: str = "auto") -> list[Conversation]:
    with open(path, "rb") as fh:
        return load_bytes(fh.read(), source)

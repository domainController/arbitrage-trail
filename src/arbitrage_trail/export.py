"""Sortie : écrire les fichiers Markdown dans un dossier (vault) ou dans un zip."""

from __future__ import annotations

import io
import os
import zipfile
from datetime import datetime, timezone

from . import markdown
from .model import Conversation


def write_dir(convs: list[Conversation], outdir: str) -> list[str]:
    """Écrit un fichier par conversation. Écriture atomique (tmp + rename)
    pour qu'un outil de synchronisation ne voie jamais un fichier à moitié écrit."""
    os.makedirs(outdir, exist_ok=True)
    now = datetime.now(timezone.utc)
    paths = []
    for conv in convs:
        path = os.path.join(outdir, markdown.filename(conv))
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(markdown.render(conv, exported=now))
        os.replace(tmp, path)
        paths.append(path)
    return paths


def to_zip(convs: list[Conversation]) -> bytes:
    now = datetime.now(timezone.utc)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for conv in convs:
            zf.writestr(markdown.filename(conv), markdown.render(conv, exported=now))
    return buf.getvalue()

"""Rendu Markdown d'une conversation, compatible Obsidian.

Choix (voir specs/002-format-markdown/spec.md) :
- frontmatter YAML : les chaînes sont sérialisées en JSON, qui est du YAML valide ;
- un titre `#`, puis un en-tête `##` par message ;
- le contenu des messages est recopié tel quel (c'est déjà du Markdown) ;
- les pertes (`warnings`) sont annoncées en tête, dans un callout.
"""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone

from .model import Conversation

ROLE_LABELS = {
    "user": "Utilisateur",
    "assistant": "Assistant",
    "tool": "Outil",
    "system": "Système",
}

SOURCE_LABELS = {"chatgpt": "ChatGPT", "claude": "Claude"}


def _iso(dt: datetime | None) -> str | None:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if dt else None


def slugify(text: str, max_len: int = 60) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (text[:max_len].rstrip("-")) or "sans-titre"


def filename(conv: Conversation) -> str:
    """Nom déterministe : réexporter la même conversation écrase le même fichier."""
    date = conv.created.strftime("%Y-%m-%d") if conv.created else "sans-date"
    short_id = re.sub(r"[^a-zA-Z0-9]", "", conv.id)[:8] or "noid"
    return f"{date}_{conv.source}_{slugify(conv.title)}_{short_id}.md"


def render(conv: Conversation, exported: datetime | None = None) -> str:
    exported = exported or datetime.now(timezone.utc)
    fm = {
        "title": conv.title,
        "source": conv.source,
        "conversation_id": conv.id,
        "created": _iso(conv.created),
        "updated": _iso(conv.updated),
        "exported": _iso(exported),
        "messages": len(conv.messages),
    }
    lines = ["---"]
    for key, value in fm.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append(f"tags: [arbitrage-trail, {conv.source}]")
    lines.append("---")
    lines.append("")
    lines.append(f"# {conv.title}")
    lines.append("")

    if conv.warnings:
        lines.append("> [!warning] Export incomplet")
        for w in conv.warnings:
            lines.append(f"> - {w}")
        lines.append("")

    for msg in conv.messages:
        label = ROLE_LABELS.get(msg.role, msg.role)
        if msg.role == "assistant":
            label = f"{label} ({SOURCE_LABELS.get(conv.source, conv.source)})"
        stamp = msg.created.astimezone(timezone.utc).strftime(" · %Y-%m-%d %H:%M UTC") if msg.created else ""
        lines.append(f"## {label}{stamp}")
        lines.append("")
        if msg.attachments:
            lines.append("Pièces jointes : " + ", ".join(f"`{a}`" for a in msg.attachments))
            lines.append("")
        if msg.text:
            lines.append(msg.text)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"

"""Parser de l'export Claude (`conversations.json` dans le zip d'export).

Structure attendue (à revérifier sur un export réel, voir docs/formats/README.md) :
une liste de conversations avec `uuid`, `name`, `created_at`, `updated_at` et
`chat_messages`, une liste *linéaire* de messages (`sender` = human|assistant,
`text`, et parfois `content` = liste de blocs typés).
"""

from __future__ import annotations

from datetime import datetime

from ..model import Conversation, Message


def _ts(value) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _blocks_text(blocks: list, unknown: set[str]) -> str:
    out = []
    for b in blocks:
        if not isinstance(b, dict):
            continue
        kind = b.get("type")
        if kind == "text":
            out.append(b.get("text", ""))
        elif kind == "thinking":
            body = b.get("thinking", "")
            if body:
                out.append("> [!note]- Raisonnement\n> " + body.replace("\n", "\n> "))
        elif kind == "tool_use":
            out.append(f"*[appel d'outil : {b.get('name', '?')}]*")
        elif kind == "tool_result":
            out.append("*[résultat d'outil]*")
        else:
            unknown.add(str(kind))
    return "\n\n".join(x for x in out if x)


def parse_one(raw: dict) -> Conversation:
    unknown: set[str] = set()
    messages: list[Message] = []
    for m in raw.get("chat_messages") or []:
        if not isinstance(m, dict):
            continue
        role = "user" if m.get("sender") == "human" else "assistant"
        blocks = m.get("content")
        text = _blocks_text(blocks, unknown) if isinstance(blocks, list) and blocks else ""
        if not text:
            text = m.get("text") or ""
        text = text.strip()
        files = [
            f.get("file_name") or f.get("name") or "fichier"
            for f in (m.get("attachments") or []) + (m.get("files") or [])
            if isinstance(f, dict)
        ]
        if not text and not files:
            continue
        messages.append(Message(role=role, text=text, created=_ts(m.get("created_at")), attachments=files))

    warnings = []
    if unknown:
        warnings.append("Blocs de contenu non restitués : " + ", ".join(sorted(unknown)) + ".")

    return Conversation(
        source="claude",
        id=str(raw.get("uuid") or ""),
        title=(raw.get("name") or "Sans titre").strip() or "Sans titre",
        created=_ts(raw.get("created_at")),
        updated=_ts(raw.get("updated_at")),
        messages=messages,
        warnings=warnings,
    )


def parse(data) -> list[Conversation]:
    items = data if isinstance(data, list) else [data]
    return [parse_one(c) for c in items if isinstance(c, dict)]

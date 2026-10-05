"""Parser de l'export ChatGPT (`conversations.json`).

Structure attendue (à revérifier sur un export réel, voir docs/formats/README.md) :
une liste de conversations, chacune avec `title`, `create_time`, `update_time`,
`current_node` et `mapping` : un arbre {id: {message, parent, children}}.

ChatGPT stocke un *arbre*, pas une liste : chaque message régénéré ou édité
crée une branche. On exporte la branche affichée (de `current_node` jusqu'à la
racine) et on signale le nombre de branches ignorées.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..model import Conversation, Message


def _ts(value) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def _active_chain(mapping: dict, current: str | None) -> list[dict]:
    if not current or current not in mapping:
        # Pas de current_node : on descend depuis la racine en suivant le
        # dernier enfant, qui est en général la version la plus récente.
        roots = [n for n in mapping.values() if not n.get("parent")]
        if not roots:
            return []
        chain, node, seen = [], roots[0], set()
        while node and node.get("id") not in seen:
            seen.add(node.get("id"))
            chain.append(node)
            children = node.get("children") or []
            node = mapping.get(children[-1]) if children else None
        return chain

    chain, node_id, seen = [], current, set()
    while node_id and node_id in mapping and node_id not in seen:
        seen.add(node_id)
        node = mapping[node_id]
        chain.append(node)
        node_id = node.get("parent")
    chain.reverse()
    return chain


def _render_part(part, unknown: set[str]) -> str:
    if isinstance(part, str):
        return part
    if isinstance(part, dict):
        kind = part.get("content_type", "objet")
        if kind == "image_asset_pointer":
            return "*[image jointe]*"
        if kind == "audio_transcription":
            return part.get("text", "")
        unknown.add(kind)
        return f"*[contenu non textuel : {kind}]*"
    return ""


def _message_text(msg: dict, unknown: set[str]) -> str:
    content = msg.get("content") or {}
    ctype = content.get("content_type", "text")
    if ctype in ("text", "multimodal_text"):
        parts = content.get("parts") or []
        return "\n\n".join(p for p in (_render_part(x, unknown) for x in parts) if p)
    if ctype == "code":
        lang = content.get("language") or ""
        if lang == "unknown":
            lang = ""
        return f"```{lang}\n{content.get('text', '')}\n```"
    if ctype == "execution_output":
        return f"```text\n{content.get('text', '')}\n```"
    if ctype in ("thoughts", "reasoning_recap"):
        # Raisonnement interne affiché replié par l'interface : on le garde,
        # mais marqué, pour ne pas le confondre avec la réponse.
        thoughts = content.get("thoughts") or []
        body = "\n\n".join(t.get("content", "") for t in thoughts if isinstance(t, dict))
        body = body or content.get("content", "")
        return f"> [!note]- Raisonnement\n> " + body.replace("\n", "\n> ") if body else ""
    unknown.add(ctype)
    text = content.get("text")
    if isinstance(text, str) and text:
        return text
    return f"*[contenu non restitué : {ctype}]*"


def parse_one(raw: dict) -> Conversation:
    mapping = raw.get("mapping") or {}
    chain = _active_chain(mapping, raw.get("current_node"))
    unknown: set[str] = set()
    messages: list[Message] = []

    for node in chain:
        msg = node.get("message")
        if not msg:
            continue
        meta = msg.get("metadata") or {}
        if meta.get("is_visually_hidden_from_conversation"):
            continue
        role = (msg.get("author") or {}).get("role", "assistant")
        if role == "system":
            continue
        text = _message_text(msg, unknown).strip()
        if not text:
            continue
        attachments = [a.get("name", "fichier") for a in meta.get("attachments") or [] if isinstance(a, dict)]
        messages.append(Message(role=role, text=text, created=_ts(msg.get("create_time")), attachments=attachments))

    warnings = []
    branching = sum(1 for n in mapping.values() if len(n.get("children") or []) > 1)
    if branching:
        warnings.append(
            f"{branching} point(s) de bifurcation (réponses régénérées ou messages édités) : "
            "seule la branche affichée dans l'interface est exportée."
        )
    if unknown:
        warnings.append("Types de contenu non restitués fidèlement : " + ", ".join(sorted(unknown)) + ".")

    return Conversation(
        source="chatgpt",
        id=str(raw.get("conversation_id") or raw.get("id") or ""),
        title=(raw.get("title") or "Sans titre").strip(),
        created=_ts(raw.get("create_time")),
        updated=_ts(raw.get("update_time")),
        messages=messages,
        warnings=warnings,
    )


def parse(data) -> list[Conversation]:
    items = data if isinstance(data, list) else [data]
    return [parse_one(c) for c in items if isinstance(c, dict)]

"""Registre des parsers et détection de format.

Chaque parser expose `parse(data) -> list[Conversation]`. Pour ajouter une
plateforme : écrire le module, l'ajouter à PARSERS et à `detect`, fournir une
fixture dans tests/fixtures. Rien d'autre ne change.
"""

from __future__ import annotations

from . import chatgpt, claude

PARSERS = {
    "chatgpt": chatgpt.parse,
    "claude": claude.parse,
}


class UnknownFormat(ValueError):
    pass


def detect(data) -> str:
    sample = data[0] if isinstance(data, list) and data else data
    if not isinstance(sample, dict):
        raise UnknownFormat("Le fichier ne contient pas de liste de conversations reconnaissable.")
    if "mapping" in sample:
        return "chatgpt"
    if "chat_messages" in sample:
        return "claude"
    raise UnknownFormat(
        "Format non reconnu. Plateformes prises en charge : " + ", ".join(PARSERS) + "."
    )

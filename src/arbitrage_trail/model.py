"""Modèle pivot : toute plateforme est convertie vers ces deux structures.

Le Markdown n'est produit qu'à partir de ce modèle. Ajouter une plateforme
revient donc à écrire un parser `données brutes -> list[Conversation]`, sans
toucher au rendu.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


ROLES = ("user", "assistant", "tool", "system")


@dataclass
class Message:
    role: str
    text: str
    created: datetime | None = None
    attachments: list[str] = field(default_factory=list)


@dataclass
class Conversation:
    source: str
    id: str
    title: str
    created: datetime | None
    updated: datetime | None
    messages: list[Message]
    # Tout ce qui n'a pas pu être restitué fidèlement. Rendu en tête du
    # fichier : la promesse « rien n'est perdu » impose de dire ce qui l'est.
    warnings: list[str] = field(default_factory=list)

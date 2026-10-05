# ADR 0002 : Python, bibliothèque standard uniquement

**Statut : accepté.**

## Contexte

Le document de fondation exclut les frameworks lourds et les bases de données,
et demande un outil portable (laptop, VPS).

## Décision

Python ≥ 3.10, **aucune dépendance** : `json`, `zipfile`, `http.server`,
`unittest`. Le frontend est une seule page HTML sans bibliothèque.

## Conséquences

- Installation triviale (`pip install .`), rien à mettre à jour côté sécurité
  hormis Python lui-même.
- `http.server` n'est pas un serveur de production : acceptable pour un usage
  personnel derrière Tailscale ou Caddy. À revoir seulement si l'usage change.
- Pas de multipart (le module `cgi` a disparu en Python 3.13) : le navigateur
  envoie le fichier en corps brut.
- Si un besoin justifie une dépendance un jour, il fait l'objet d'un ADR.

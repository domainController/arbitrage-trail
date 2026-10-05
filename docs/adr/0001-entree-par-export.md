# ADR 0001 : Le prototype ne lit que les exports officiels

**Statut : accepté (provisoire, révisable après le spike 005).**

## Contexte

Le document de fondation laisse ouvert le « mode de récupération » (API, scraping,
fichier exporté). Ce choix détermine le régime de l'outil (voir
`docs/01-lecture-critique.md` §1).

## Décision

La v0 lit uniquement les exports officiels (zip ou `conversations.json`).
La récupération par URL est un spike séparé (spec 005). L'accès direct au compte
(cookies, API internes) est hors périmètre.

## Conséquences

- L'outil reste dans un régime borné : fixtures, tests hors réseau, aucune
  dépendance aux changements d'interface des plateformes.
- Le geste unitaire « une conversation, tout de suite » n'est pas couvert. Il
  est remplacé, pour l'instant, par un export périodique rendu idempotent.

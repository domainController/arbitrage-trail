# Instructions pour tout agent (source de vérité)

Langue : français. Termes bilingues FR/EN acceptés quand ils sont conceptuellement utiles. Précision conceptuelle d'abord.

## Ordre de lecture

1. `HANDOFF.md` : où on en est, quoi faire ensuite, décisions en suspens.
2. `docs/00-fondation.md` : le document de fondation de l'utilisateur. Il fait foi sur le besoin et le périmètre. Ne pas le réécrire.
3. `docs/01-lecture-critique.md` : sa formalisation, et pourquoi le mode de récupération décide du régime.
4. La spec concernée : `specs/NNN-*/spec.md`.

## Règle de régime

Chaque spec annonce son régime en tête.

- **Bounded** : exécuter les tâches, avec tests. Pas besoin de demander à chaque pas.
- **Unbounded** : ne pas implémenter à l'aveugle. Spike court, résultat écrit dans la spec, puis demander la suite. Actuellement : spec 005 (URL), 006-b (DeepSeek, Gemini).

Si un module Bounded accumule cas particuliers, bugs ou abstractions, le signaler : il a peut-être basculé.

## Règles de code

- Python ≥ 3.10, **bibliothèque standard uniquement** (ADR 0002). Une dépendance = un ADR.
- Tests : `python -m unittest discover -s tests` (après `pip install -e .`, ou avec `PYTHONPATH=src`). Aucun test ne touche le réseau.
- Ajouter une plateforme = un module dans `parsers/`, une entrée dans `PARSERS` et `detect`, une fixture, des tests. Le rendu Markdown ne change pas.
- Le format de sortie est un contrat avec Second Cortex (ADR 0003) : ne pas modifier le frontmatter ni le nommage des fichiers sans ADR.
- Aucune perte silencieuse : tout contenu non restitué produit un avertissement (spec 001 R5).
- Une décision structurante = un fichier dans `docs/adr/`. Ne pas trancher en silence une question marquée « à décider » dans `HANDOFF.md`.

## Ce que l'agent ne fait pas

- Il ne committe **jamais** un vrai export ni une vraie conversation. Fixtures synthétiques ou extraits anonymisés seulement.
- Il n'écrit pas de code qui se connecte au compte de l'utilisateur (cookies, API internes) : hors périmètre (ADR 0001).
- Il n'expose pas la web app hors `127.0.0.1` sans authentification ou réseau privé.
- Il n'invente pas de specs pour Second Cortex ou les autres instruments : il les demande.
- Il ne rend pas le dépôt public.

## Façon de collaborer avec l'utilisateur

L'utilisateur veut voir plus clair dans son propre fonctionnement, pas qu'on lui dise quoi faire : architecture, structure, modélisation, cartographie, correspondances avec des cadres existants, déconstruction/reconstruction. Face à une intuition brute : la formaliser, la clarifier, la restructurer, expliciter les mécanismes implicites, signaler les recouvrements conceptuels. Éviter la théorisation qui dilue le propos ; rester fidèle au terrain.

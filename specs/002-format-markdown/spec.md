# Spec 002 : Format Markdown de sortie

**Régime : Bounded.** Mais c'est un **contrat** avec Second Cortex (ADR 0003) :
toute modification du frontmatter est une décision, pas un détail.

**État : implémenté (`src/arbitrage_trail/markdown.py`), version 1 du format.**

## Format v1

```markdown
---
title: "Titre de la conversation"
source: "chatgpt"
conversation_id: "…"
created: "2026-10-03T18:00:00Z"
updated: "2026-10-03T18:30:00Z"
exported: "2026-10-05T08:00:00Z"
messages: 12
tags: [arbitrage-trail, chatgpt]
---

# Titre de la conversation

> [!warning] Export incomplet          ← seulement s'il y a des pertes
> - …

## Utilisateur · 2026-10-03 18:00 UTC

Texte du message, recopié tel quel.

## Assistant (ChatGPT) · 2026-10-03 18:00 UTC

…
```

## Règles

- **R1.** Valeurs du frontmatter sérialisées en JSON (donc YAML valide, même avec
  des guillemets ou des deux-points dans le titre).
- **R2.** Nom de fichier déterministe : `AAAA-MM-JJ_source_titre-slug_id8.md`.
  Réexporter écrase le même fichier (idempotence).
- **R3.** Le texte des messages n'est pas réécrit : c'est déjà du Markdown.
- **R4.** Raisonnement interne rendu en callout replié `> [!note]- Raisonnement`,
  pour ne pas le confondre avec la réponse.
- **R5.** Pertes déclarées en tête (callout `warning`).

## Questions ouvertes

- **Q-G (titres en collision).** Les réponses contiennent leurs propres `#` et
  `##`, qui se mêlent aux en-têtes de rôle. Options : (a) laisser (actuel) ;
  (b) décaler les titres du contenu d'un ou deux niveaux ; (c) séparer les
  messages par des callouts plutôt que par des titres. (b) modifie le texte
  source, ce qui contredit R3. À trancher avec les besoins de Second Cortex.
- **Q-H (fuseau horaire).** Tout est en UTC. Afficher l'heure locale serait plus
  lisible mais rend le fichier dépendant de la machine qui l'a produit.

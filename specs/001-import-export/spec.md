# Spec 001 : Import d'un export de plateforme

**Régime : Bounded.** Format statique produit par la plateforme, testable avec
des fixtures, sans réseau.

**État : prototype écrit et testé sur des fixtures synthétiques. Jamais testé
sur un vrai export.** Les structures attendues viennent de connaissances
antérieures, pas d'un export examiné : c'est le premier risque du projet.

## Besoin

Transformer l'export officiel d'un compte (ChatGPT, Claude) en une liste de
conversations dans le modèle pivot (`src/arbitrage_trail/model.py`).

## Règles

- **R1.** Entrée acceptée : le zip d'export tel que reçu, ou le
  `conversations.json` extrait. Détection automatique de la plateforme.
- **R2.** Un parser par plateforme, avec la même signature
  `parse(data) -> list[Conversation]`. Le rendu Markdown ne connaît pas les
  plateformes.
- **R3.** ChatGPT : suivre la branche affichée (`current_node` vers la racine).
  Compter et déclarer les bifurcations ignorées.
- **R4.** Ignorer les messages système et ceux marqués cachés par la plateforme.
- **R5.** Tout contenu non restitué fidèlement produit un avertissement nommant
  son type. Aucune perte silencieuse.
- **R6.** Un fichier illisible ou non reconnu produit une erreur claire, jamais
  un résultat partiel muet.

## Critères d'acceptation

- [x] Fixtures ChatGPT et Claude converties (tests `tests/test_parsers.py`).
- [x] Zip d'export avec `conversations.json` dans un sous-dossier.
- [ ] **Un vrai export ChatGPT converti, écarts notés dans `docs/formats/README.md`.**
- [ ] **Un vrai export Claude converti, écarts notés dans `docs/formats/README.md`.**
- [ ] Fixtures de test remplacées ou complétées par des extraits *anonymisés*
      des vrais exports.

## Hors périmètre

Pièces jointes binaires (spec 006), autres plateformes (spec 006), récupération
par URL (spec 005).

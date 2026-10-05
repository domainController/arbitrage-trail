# ADR 0003 : Le format Markdown de sortie est un contrat versionné

**Statut : accepté.**

## Contexte

Second Cortex lira les fichiers produits par Arbitrage Trail. La séparation des
deux instruments ne tient que si leur interface est stable.

## Décision

Le format défini dans `specs/002-format-markdown/spec.md` est la **v1**. Toute
modification du frontmatter (ajout, retrait, renommage, changement de type) ou
du nommage des fichiers passe par un ADR et une nouvelle version de la spec.

## Conséquences

- Second Cortex peut s'appuyer sur `source`, `conversation_id` et `created` pour
  dédoublonner et dater.
- Ajouter un champ est peu risqué ; en retirer ou en renommer un casse l'aval.

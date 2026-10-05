# Spec 006 : Extensions (pièces jointes, autres plateformes, branches)

Trois chantiers indépendants, chacun à ouvrir en spec séparée quand il devient
prioritaire. Aucun n'est commencé.

## 006-a Pièces jointes binaires — Bounded (après examen d'un vrai export)

L'export ChatGPT contiendrait les fichiers téléversés à côté de
`conversations.json` (à vérifier). Copier les binaires dans le vault
(`attachments/`) et les lier depuis le Markdown (`![[fichier.png]]` pour
Obsidian).

## 006-b DeepSeek et Gemini — Unbounded jusqu'à examen d'un export

- **DeepSeek** : proposerait un export de données ; format non examiné.
- **Gemini** : l'historique passerait par Google Takeout (« Mon activité »),
  dans un format pensé pour l'activité, pas pour des conversations. Probablement
  le plus pauvre des quatre.

Procédure : obtenir un export réel, l'examiner, écrire `docs/formats/README.md`,
*puis* décider du régime. Si le format est propre, c'est un parser de plus
(Bounded). Sinon, spike.

## 006-c Branches ChatGPT — Bounded, mais décision de format d'abord

Exporter aussi les branches abandonnées (Q-F dans `HANDOFF.md`). Pour un outil
nommé *Arbitrage* Trail, ce sont précisément les traces d'arbitrage. Options :
toutes les branches dans un fichier (sections repliées), un fichier par branche,
ou un fichier annexe `…_branches.md`.

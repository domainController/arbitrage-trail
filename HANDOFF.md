# HANDOFF : état du chantier Arbitrage Trail

> Mis à jour à chaque fin de session. La section « Journal » en bas garde
> l'historique.

## Où on en est (2026-10-05)

**Un prototype complet tourne**, sur le mode « import d'export » uniquement :

- CLI : `arbitrage-trail list|convert|serve`.
- Web app : dépôt du zip, liste filtrable, téléchargement `.md` ou `.zip`,
  écriture dans un vault configuré. Testée dans un navigateur à la largeur
  d'un téléphone.
- Parsers ChatGPT et Claude, rendu Markdown compatible Obsidian, avertissements
  en cas de perte.
- 30 tests (`python -m unittest discover -s tests`), aucune dépendance.
- Fichiers de déploiement prêts (`deploy/`) et procédure VPS écrite
  (`docs/infra-vps.md`).

## Ce qui n'existe pas, ou n'est pas vérifié

- **Les parsers n'ont jamais vu un vrai export.** Les formats attendus viennent
  de connaissances antérieures, pas d'un fichier examiné. Premier risque du
  projet ; c'est pour ça que T1 passe en premier.
- Aucune récupération par URL (spec 005, Unbounded, spike non fait).
- Pas de pièces jointes binaires, pas de branches ChatGPT abandonnées, pas de
  DeepSeek ni de Gemini (spec 006).
- Rien de déployé : le VPS n'existe pas encore.
- Commandes Tailscale, Caddy et chemins de menus des plateformes non vérifiés
  en ligne.

## Décisions en suspens (ne pas trancher en silence)

| Id | Question | Recommandation provisoire | Où |
|---|---|---|---|
| Q-A | Accès à l'app sur le VPS : Tailscale, public + mot de passe, ou local seulement ? | Tailscale | `docs/infra-vps.md` |
| Q-B | Arrivée dans le vault : téléchargement, Syncthing ou git ? | Syncthing, ou git si l'historique des versions compte | `docs/infra-vps.md` |
| Q-C | Conserver l'export brut (zip) à côté des `.md` ? | Oui, en lecture seule : le `.md` est une vue dérivée | lecture critique §2 |
| Q-D | Récupération par URL : implémenter, solution pauvre (coller le texte) ou abandonner ? | Décider après le spike 005 | spec 005 |
| Q-E | Structure du vault : à plat, par source, par mois ? | À plat dans `Arbitrage-Trail/` tant que le volume est faible | — |
| Q-F | Branches ChatGPT abandonnées : ignorer (actuel), tout dans un fichier, ou un fichier annexe ? | Fichier annexe : garde le fichier principal lisible | spec 006-c |
| Q-G | Titres `#` des réponses qui se mêlent aux en-têtes de rôle | Laisser tant que Second Cortex n'a pas exprimé de besoin | spec 002 |
| Q-H | Horodatages en UTC ou en heure locale dans le Markdown ? | UTC (fichier indépendant de la machine) | spec 002 |

## Ordre de travail recommandé

1. **T1 (toi, maintenant)** : demander les exports ChatGPT et Claude. Ils
   mettent du temps à arriver : lance-les avant tout le reste.
2. **T2** : à réception, `arbitrage-trail list <export.zip>` puis `convert`.
   Noter les écarts dans `docs/formats/README.md`, corriger les parsers, ajouter
   un test par écart (spec 001, tâches T1.6–T1.8).
3. **T3** : ouvrir quelques fichiers dans Obsidian. Le rendu est-il lisible ?
   Les avertissements sont-ils justes ? Ajuster la spec 002 si besoin.
4. **T4 (jour du VPS)** : trancher Q-A et Q-B (un ADR chacun), puis dérouler
   `docs/infra-vps.md` §4. Critères dans la spec 004.
5. **T5** : spike 005 (demi-journée maximum), puis trancher Q-D.

## Ce que toi seul peux faire

- Demander les exports aux plateformes (T1).
- Louer le VPS, installer Tailscale sur tes appareils.
- Trancher les décisions Q-A à Q-H.
- Fournir la spec de Second Cortex quand on voudra aligner le format (ADR 0003).

## Démarrage rapide (demain, sans VPS)

```bash
git clone https://github.com/domainController/arbitrage-trail.git
cd arbitrage-trail
python3 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/python -m unittest discover -s tests          # 30 tests
.venv/bin/arbitrage-trail list tests/fixtures/chatgpt_conversations.json
.venv/bin/arbitrage-trail serve                          # http://127.0.0.1:8765
```

## Journal

- **2026-10-05** : création du dépôt. Document de fondation importé tel quel,
  lecture critique, specs 001–006, ADR 0001–0003, prototype (CLI + web app),
  30 tests, fichiers de déploiement.

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

Elles ne se tranchent pas toutes au même moment (ADR 0004). Le critère est le
coût d'une erreur : ce qui touche le contenu des fichiers (contrat avec Second
Cortex) se décide avant l'usage ; ce qui est réversible se décide après l'avoir
pratiqué.

**À trancher avant l'usage, ou dès que possible**

| Id | Question | Recommandation provisoire | Où |
|---|---|---|---|
| Q-H | Horodatages en UTC ou en heure locale dans le Markdown ? | UTC (fichier indépendant de la machine). Change le contenu des fichiers : mieux vaut décider avant de remplir le vault | spec 002 |
| Q-C | Conserver l'export brut (zip) à côté des `.md` ? | Oui, en lecture seule : le `.md` est une vue dérivée. Le principe se décide maintenant ; l'emplacement du zip dépend de Q-B | lecture critique §2 |

**Provisoires au déploiement, à confirmer après la prise en main**

| Id | Question | Choix provisoire | Où |
|---|---|---|---|
| Q-A | Accès à l'app sur le VPS : Tailscale, public + mot de passe, ou local seulement ? | Tailscale | `docs/infra-vps.md` |
| Q-B | Arrivée dans le vault : téléchargement, Syncthing ou git ? | Téléchargement manuel ; l'usage dira si le geste gêne au point de justifier Syncthing (confort) ou git (historique des versions) | `docs/infra-vps.md` |

**À trancher après la prise en main**

| Id | Question | Recommandation provisoire | Où |
|---|---|---|---|
| Q-D | Récupération par URL : implémenter, solution pauvre (coller le texte) ou abandonner ? | Ne pas faire le spike 005 avant d'avoir pratiqué le mode par lot : c'est l'usage qui dira si le geste unitaire manque | spec 005 |
| Q-E | Structure du vault : à plat, par source, par mois ? | À plat dans `Arbitrage-Trail/` en attendant de voir le volume réel | — |
| Q-F | Branches ChatGPT abandonnées : ignorer (actuel), tout dans un fichier, ou un fichier annexe ? | Fichier annexe : garde le fichier principal lisible | spec 006-c |

**Dépend d'un tiers**

| Id | Question | Recommandation provisoire | Où |
|---|---|---|---|
| Q-G | Titres `#` des réponses qui se mêlent aux en-têtes de rôle | Laisser tant que Second Cortex n'a pas exprimé de besoin | spec 002 |

## Ordre de travail recommandé

1. **T1 (toi, maintenant)** : demander les exports ChatGPT et Claude. Ils
   mettent du temps à arriver : lance-les avant tout le reste. Ne dépend pas
   du VPS.
2. **T2 (en local, avant le VPS)** : à réception, `arbitrage-trail list
   <export.zip>` puis `convert`. Noter les écarts dans `docs/formats/README.md`,
   corriger les parsers, ajouter un test par écart (spec 001, tâches
   T1.6–T1.8). En local parce qu'une erreur y donne une trace lisible ; via la
   web app, elle ne serait qu'un code 422.
3. **T3** : ouvrir quelques fichiers dans Obsidian. Le rendu est-il lisible ?
   Les avertissements sont-ils justes ? Ajuster la spec 002 si besoin.
4. **T4 (jour du VPS) : déploiement provisoire** avec Q-A = Tailscale et
   Q-B = téléchargement manuel (ADR 0004). Dérouler `docs/infra-vps.md` §4.
   Critères dans la spec 004, partie « provisoire ».
5. **Prise en main** : utiliser l'outil quelque temps en mode par lot, sur le
   téléphone et l'ordinateur. Noter les frictions.
6. **T5** : trancher Q-B, Q-E, Q-F à partir de l'usage (un ADR chacune), puis
   décider si le spike 005 vaut la peine (demi-journée maximum) et trancher Q-D.

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
- **2026-10-05 (2)** : les décisions en suspens sont réparties selon le moment
  où on peut les trancher (avant l'usage, provisoires au déploiement, après la
  prise en main). La spec 004 autorise un déploiement provisoire avec Tailscale
  et téléchargement manuel (ADR 0004). T2 reste en local, avant le VPS.

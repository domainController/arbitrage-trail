# Lecture critique du document de fondation

> Ce document ne remplace pas `00-fondation.md` : il le lit, le formalise et
> signale où il dit plus (ou moins) qu'il ne croit. Les specs en découlent.

---

## 1. La thèse centrale tient, mais pas pour tout l'outil

Le document affirme (§4) qu'Arbitrage Trail est **borné** : specs connues,
abstraction limitée, dépendances stables. Puis il liste (§4.3) cinq décisions
« à prendre au moment de l'implémentation ».

Quatre de ces cinq décisions sont effectivement locales (format de sortie,
interface, plateformes à couvrir d'abord, envoi vers un vault). **Une ne l'est
pas : le mode de récupération.** C'est elle qui décide si l'outil est borné ou
non. Il y a en réalité trois instruments différents cachés sous le verbe
« récupérer » :

| Mode | Ce que c'est | Régime | Pourquoi |
|---|---|---|---|
| **A. Import d'export** | L'utilisateur demande l'export de son compte à la plateforme, reçoit un zip, le donne à l'outil | **Bounded** | Format produit par la plateforme elle-même, fichier statique, testable avec des fixtures, aucune dépendance réseau, aucun problème de conditions d'utilisation |
| **B. Lien de partage** | L'utilisateur colle une URL publique `…/share/…` | **Unbounded** | Pages rendues en JavaScript, structure interne non documentée qui change sans préavis, protections anti-bot, contenu limité à ce qui a été partagé (souvent sans pièces jointes), zone grise des conditions d'utilisation |
| **C. Accès au compte** | L'outil se connecte au compte (cookie de session, API interne) | **Unbounded et risqué** | Il faut stocker une session valide sur un serveur, les API internes ne sont pas publiques, rupture probable des conditions d'utilisation, et un VPS qui détient tes sessions est une cible |

Point à vérifier, mais à forte probabilité : **il n'existe pas d'« API officielle »
pour lire l'historique des conversations** des applications grand public
(ChatGPT, Claude.ai). Les API développeurs de ces fournisseurs servent à *créer*
des conversations, pas à relire celles de l'interface. L'option « API officielle »
de §4.3 est donc probablement vide.

**Conséquence de construction.** Le prototype ne fait que **A**. B fait l'objet
d'un spike séparé (`specs/005`), C est explicitement hors périmètre tant qu'on
n'a pas une raison forte. La phrase « ces décisions peuvent être prises au moment
de l'implémentation » reste vraie, à condition d'avoir sorti la récupération de
la liste : c'est une décision de *régime*, pas d'implémentation.

Correspondance avec la doctrine Bounded / Unbounded de `semantic-log` : c'est le
cas typique d'un projet qui se décrit comme borné parce que son *cœur* l'est
(convertir du JSON en Markdown), alors que sa *frontière* (aller chercher les
données) ne l'est pas. La frontière avec le monde extérieur est presque toujours
là où le régime bascule.

---

## 2. « Rien n'est perdu » : une promesse à reformuler pour être tenable

Un export n'est pas une conversation telle que tu l'as vécue. Des pertes sont
structurelles :

- **Branches.** ChatGPT stocke un *arbre* : chaque réponse régénérée, chaque
  message édité crée une bifurcation. L'interface n'en montre qu'une. Exporter
  « la conversation » revient à choisir une branche. Or pour un outil nommé
  *Arbitrage* Trail, les branches abandonnées sont justement la trace des
  arbitrages.
- **Pièces jointes.** Les images et les fichiers sont des références dans le JSON ;
  les binaires, quand ils sont fournis, sont à côté dans le zip.
- **Contenus riches.** Canvas, artefacts, sorties d'outils, navigation web,
  raisonnement replié : chaque plateforme les encode à sa façon, et certains ne
  sont pas exportés du tout.

Reformulation proposée, qui est tenable et vérifiable :

> **Rien n'est perdu *en silence*.**

Toute perte connue est déclarée dans le fichier produit (callout
`> [!warning] Export incomplet` en tête). C'est ce que fait le prototype : il
compte les bifurcations ignorées et nomme les types de contenu non restitués.
La complétude devient un problème de **traçabilité de la perte** plutôt qu'une
promesse absolue.

Deuxième garde-fou, à décider (Q-C dans `HANDOFF.md`) : **conserver l'export
brut** (le zip) à côté des fichiers Markdown, en lecture seule. Le Markdown est
une *vue dérivée* ; le zip est la *source*. Si un jour on veut récupérer les
branches ou les images, on repart du brut sans redemander d'export.

Correspondances :
- **Archivistique** : distinction entre l'original et sa transcription, principe
  de provenance (on sait toujours d'où vient une pièce : `source`,
  `conversation_id`, `exported` dans le frontmatter).
- **Data engineering** : architecture en couches (*medallion* : bronze / silver /
  gold). Le zip est la couche bronze (brute, immuable), le Markdown la couche
  silver (nettoyée, lisible), Second Cortex produit la couche gold (analysée).

---

## 3. Deux rythmes d'usage, pas un

Le critère de succès (§3.3) décrit un geste **unitaire** : coller *une* URL,
obtenir *un* fichier. L'import d'export est un geste **par lot** : tout le compte,
d'un coup, avec plusieurs heures d'attente côté plateforme.

Ces deux rythmes ne servent pas le même besoin :

| | Par lot (export) | Unitaire (URL) |
|---|---|---|
| Besoin | Archive complète, pérennité | Capturer *cette* décision, maintenant |
| Fréquence | Hebdomadaire ou mensuelle | Juste après une conversation importante |
| Régime | Bounded | Unbounded |

Le prototype rend le lot *répétable* : les noms de fichiers sont déterministes
(`date_source_titre_id.md`), donc relancer la conversion sur un nouvel export
**met à jour** les fichiers existants au lieu de créer des doublons. Un export
hebdomadaire suffit alors à maintenir le vault à jour.

Le geste unitaire reste un vrai besoin. La question est de savoir s'il justifie
le coût d'un régime Unbounded, ou si une solution plus pauvre suffit (coller le
texte de la conversation dans un champ, par exemple). C'est l'objet du spike 005.

---

## 4. « Pas un service cloud » et VPS : pas de contradiction, mais une conséquence

Un VPS que tu loues et administres n'est pas du « cloud » au sens du document
(service tiers qui détient tes données). « Local-first » doit se lire comme :
**les données restent sous ton contrôle, dans des fichiers ouverts.**

La conséquence est ailleurs. Si la web app tourne sur le VPS, **le vault
Obsidian n'y est pas** : il est sur ton ordinateur et ton téléphone. La vraie
question d'infrastructure n'est donc pas « où tourne l'app », mais **« comment
les fichiers arrivent dans le vault »**. Options dans `docs/infra-vps.md`
(Syncthing, git, téléchargement manuel).

Deuxième conséquence : tes conversations sont des données personnelles denses.
Une web app exposée sur Internet sans authentification serait une fuite. Le
prototype écoute sur `127.0.0.1` par défaut et prévoit une authentification
(Basic Auth, derrière HTTPS) ou mieux, un accès privé par Tailscale.

---

## 5. La frontière avec Second Cortex est un contrat

Le document sépare bien les rôles (§6) : Arbitrage Trail récupère, Second Cortex
analyse. Pour que cette séparation tienne, il faut que l'interface entre les deux
soit **stable et explicite**. Cette interface, c'est le **format des fichiers
Markdown**, et en particulier le frontmatter :

```yaml
title: "…"
source: "chatgpt" | "claude"
conversation_id: "…"
created / updated / exported: ISO 8601 UTC
messages: <nombre>
tags: [arbitrage-trail, <source>]
```

Changer ce format casse Second Cortex. D'où l'ADR 0003 : le format de sortie est
versionné et ne change que par décision explicite. C'est le même principe que
« pas de connaissance de domaine dans le noyau » côté `semantic-log` : chaque
instrument reste petit parce que ses frontières sont nettes.

---

## 6. Ce que le document ne dit pas encore (et qu'il faudra décider)

- **Conserver ou non l'export brut** (voir §2). Recommandation : oui.
- **Que faire des branches ChatGPT** : la branche affichée seulement (choix
  actuel), toutes les branches dans un seul fichier, ou un fichier par branche.
  Pour un outil d'arbitrage, la question n'est pas anodine.
- **Structure du vault** : un dossier par source ? par mois ? tout à plat ?
- **Collision de titres** dans le Markdown : les réponses de l'assistant
  contiennent leurs propres titres `#` et `##`, qui se mêlent aux en-têtes de
  rôle. Acceptable en lecture, gênant pour un outil qui découpe par titres
  (Second Cortex). Voir spec 002.

## 7. Coquille dans la source

La section 6.1 de `00-fondation.md` contient le même bloc de code deux fois. Je
n'ai pas modifié le document de fondation, qui reste ta version.

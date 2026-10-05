---
title: Arbitrage Trail — Document de fondation
aliases: [Arbitrage Trail, Trail Foundation]
tags: [instrument, project, founding-doc, markdown, retrieval]
status: concept
created: 2026-10-04
author: Patrice Kenmoé
---

# Arbitrage Trail — Document de fondation

> **Objet** : circonscrire le besoin, la genèse, la proposition de valeur et le périmètre d'Arbitrage Trail, de manière à ce que l'outil puisse être construit par un agent sans nécessiter de longues phases de découverte.

---

## 1. Genèse

### 1.1 Le constat

Les conversations avec les IA génératives (ChatGPT, Claude, DeepSeek, Gemini) sont un **flux de décision**. On y explore, on y pèse, on y tranche. C'est le matériau brut de la pensée en action.

Mais une fois la conversation fermée, **la trace disparaît**. Les décisions restent noyées dans un historique de chat, inaccessibles, non structurées, non exploitables.

### 1.2 La frustration

Récupérer une conversation entière est aujourd'hui :
- **laborieux** : copier-coller manuel, export partiel, formats propriétaires
- **incomplet** : les plateformes n'offrent pas d'export complet
- **non structuré** : ce qui est exporté est brut, non exploitable directement
- **non pérenne** : si la plateforme ferme ou change, la trace est perdue

### 1.3 Le besoin

Un outil qui **sauvegarde l'intégralité** d'une conversation générative et la **convertit en Markdown**, de manière fiable, répétable, sans dépendance à une plateforme.

---

## 2. Proposition de valeur

### 2.1 Ce que fait l'outil

- **Récupère** l'intégralité d'une conversation générative
- **Convertit** le contenu en Markdown propre
- **Sauvegarde** le fichier localement (ou dans un vault Obsidian)
- **Répète** l'opération pour n'importe quelle conversation, sur n'importe quelle plateforme

### 2.2 Ce que l'outil n'est pas

- Ce n'est **pas** un chatbot
- Ce n'est **pas** un outil d'analyse sémantique (ça, c'est Second Cortex)
- Ce n'est **pas** un service cloud
- Ce n'est **pas** un remplacement d'Obsidian

### 2.3 La promesse

> **Rien n'est perdu.**

Chaque conversation, chaque décision, chaque trace de raisonnement est sauvegardée localement, dans un format ouvert, exploitable par n'importe quel outil.

---

## 3. Périmètre

### 3.1 Ce qui est dans le périmètre

- **Récupération** : extraction complète du contenu d'une conversation
- **Conversion** : transformation en Markdown structuré
- **Sauvegarde** : écriture locale d'un fichier `.md`
- **Interface** : web app (accessible depuis un navigateur)

### 3.2 Ce qui est hors périmètre (pour l'instant)

- **Analyse sémantique** : c'est Second Cortex
- **Structuration avancée** : extraction d'entités, détection de contradictions
- **Intégration MCP** : à voir plus tard
- **Multi-utilisateur** : usage personnel uniquement
- **Cloud** : local-first

### 3.3 Le critère de succès

Un utilisateur peut :
1. Ouvrir la web app
2. Coller une URL de conversation (ou uploader un export)
3. Récupérer un fichier `.md` complet, propre, structuré
4. Le déposer dans son vault Obsidian

C'est tout. Rien de plus.

---

## 4. Régime d'exécution

### 4.1 Pourquoi cet outil est borné

Arbitrage Trail est dans un **régime d'exécution** :

- **Les specs sont connues** : récupérer, convertir, sauvegarder
- **L'abstraction est limitée** : pas de modélisation complexe, pas d'algorithme avancé
- **Le périmètre est restreint** : un seul cas d'usage, bien défini
- **Les dépendances sont stables** : formats de conversation, Markdown, système de fichiers

### 4.2 Conséquence pour la construction

Cet outil peut être **donné à un agent** (Claude Code, DeepSeek Harness, OpenCode) avec une angoisse limitée :

- Pas de 10 000 questions à se poser
- Pas de décisions architecturales majeures
- Pas de dépendance à des choix flous
- Juste : **implémenter ce qui est décrit**

Une fois le squelette en place, le reste est du **spike** — raffinement, ajustements, cas limites — dans un cercle très restreint.

### 4.3 Ce qui reste à décider

Même dans un régime d'exécution, quelques décisions restent ouvertes :

- **Format d'entrée** : URL, fichier exporté, ou les deux ?
- **Plateformes ciblées** : ChatGPT, Claude, DeepSeek, Gemini — toutes, ou une seule pour commencer ?
- **Mode de récupération** : API officielle, scraping, ou parsing de fichier exporté ?
- **Sortie** : téléchargement direct, ou envoi vers un vault configuré ?
- **Interface** : web app pure, ou CLI + web app ?

Ces décisions peuvent être prises **au moment de l'implémentation**, pas avant. C'est ça, le régime d'exécution.

---

## 5. Stack technique envisagée

### 5.1 Contraintes

- **Local-first** : pas de dépendance à un service cloud
- **Simple** : pas de framework lourd, pas d'infrastructure complexe
- **Portable** : doit pouvoir tourner sur un VPS, un laptop, ou un navigateur
- **Ouvert** : formats standards, pas de verrouillage

### 5.2 Stack candidate

- **Frontend** : HTML/CSS/JS simple, ou React si nécessaire
- **Backend** : Node.js ou Python, minimal
- **Récupération** : API clients (si disponibles) ou parsing de fichiers exportés
- **Conversion** : bibliothèque Markdown standard
- **Sortie** : fichier `.md` téléchargeable, ou envoi vers un vault configuré

### 5.3 Ce qu'on ne veut pas

- Framework lourd (Next.js, Django) pour un outil aussi simple
- Base de données (le fichier `.md` est la base)
- Dépendance à une API propriétaire unique
- Cloud obligatoire

---

## 6. Lien avec les autres instruments

### 6.1 Second Cortex

**Second Cortex** analyse, structure, interroge. **Arbitrage Trail** récupère et sauvegarde.

Ensemble :

```

Arbitrage Trail  →  récupère et sauvegarde les conversations
Second Cortex    →  analyse et structure le contenu

```

```

Arbitrage Trail  →  récupère et sauvegarde les conversations
Second Cortex    →  analyse et structure le contenu

```


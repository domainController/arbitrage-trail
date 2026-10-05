# Spec 005 : Récupération par lien de partage

**Régime : Unbounded.** Ne pas implémenter à l'aveugle. Spike d'abord.

## Pourquoi c'est non borné

- Les pages de partage sont rendues en JavaScript ; les données sont dans une
  structure interne non documentée qui peut changer sans préavis.
- Protections anti-bot possibles (Cloudflare, etc.), surtout depuis l'IP d'un
  VPS.
- Le lien ne contient que ce qui a été partagé, souvent sans pièces jointes.
- Conditions d'utilisation des plateformes : à lire avant tout code.

## Le besoin réel derrière

Capturer **une** conversation importante **juste après** l'avoir eue, sans
attendre un export complet (voir `docs/01-lecture-critique.md` §3).

## Spike proposé (une demi-journée, pas plus)

1. Créer un lien de partage ChatGPT et un lien Claude sur une conversation
   anodine.
2. Pour chacun, noter : le HTML brut contient-il le texte (sans JavaScript) ?
   Y a-t-il un bloc JSON embarqué ? Que renvoie une requête depuis le VPS ?
3. Écrire le résultat ici, section « Résultat du spike ».
4. Décider : (a) implémenter pour une plateforme, (b) solution pauvre : champ
   « coller le texte de la conversation », (c) abandonner au profit de l'export
   hebdomadaire.

## Alternative pauvre à évaluer en même temps

Un champ texte où l'on colle la conversation copiée depuis l'interface. Perd la
structure (rôles, dates) mais c'est immédiat, robuste et borné. À comparer avec
le coût de (a).

## Résultat du spike

*(vide)*

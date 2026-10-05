# ADR 0004 : Déployer avec des choix provisoires, trancher après la prise en main

**Statut : accepté.**

## Contexte

La spec 004 interdisait de déployer avant d'avoir tranché Q-A (accès) et Q-B
(arrivée dans le vault). Or ces deux questions, comme Q-D, Q-E et Q-F, se
tranchent mieux après avoir utilisé l'outil dans son contexte réel (téléphone,
VPS, vault). La règle créait une boucle : décider pour pouvoir essayer, alors
qu'il faut essayer pour bien décider.

Les décisions en suspens n'ont pas toutes le même coût d'erreur :

- **Irréversibles ou coûteuses** : tout ce qui touche le contenu des fichiers
  produits (contrat avec Second Cortex, ADR 0003). À trancher avant l'usage, ou
  à marquer explicitement provisoire.
- **Réversibles** : l'accès (Q-A), la synchronisation (Q-B), la structure du
  vault (Q-E), le traitement des branches (Q-F). Changer d'avis ne casse rien,
  tant que la source brute est conservée.

## Décision

1. **T2 (validation des parsers sur un vrai export) reste avant le VPS** et se
   fait en local : une erreur y donne une trace lisible, alors que via la web
   app elle ne serait qu'un code 422 ou un fichier plein d'avertissements.
2. **Le VPS peut être déployé avec des choix par défaut provisoires** :
   - Q-A : Tailscale (l'option la moins exposée, donc la plus sûre pour un essai) ;
   - Q-B : téléchargement manuel (aucune infrastructure à installer).
3. **Q-B, Q-E, Q-F et Q-D sont tranchées après une période de prise en main**,
   chacune par un ADR, à partir de ce que l'usage a montré. En particulier, Q-D
   (récupération par URL) ne se tranche qu'une fois le mode par lot pratiqué :
   c'est l'usage qui dira si le geste unitaire manque vraiment.

## Conséquences

- La spec 004 distingue un déploiement provisoire (possible tout de suite) et
  un déploiement définitif (après les ADR Q-A et Q-B).
- Avec le téléchargement manuel, le critère « apparaît dans Obsidian sans geste
  manuel » ne s'applique pas encore : il est reporté au déploiement définitif.
- Le dossier `--vault` du VPS existe déjà, mais n'est synchronisé avec rien tant
  que Q-B n'est pas tranchée.
- Correspondances : *last responsible moment* (lean), portes à sens unique ou à
  double sens (*one-way / two-way doors*), Cynefin en domaine complexe
  (*probe → sense → respond*).

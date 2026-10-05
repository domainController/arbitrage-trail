# Premier prompt à coller dans un agent

## Variante principale : valider sur un vrai export

```
Tu reprends le projet Arbitrage Trail. Lis AGENTS.md, puis HANDOFF.md, puis
docs/01-lecture-critique.md. Ne modifie rien avant de m'avoir fait un état des
lieux en 10 lignes maximum.

Ensuite : j'ai déposé un export réel dans exports/ (ignoré par git, ne jamais
le committer). Lance `arbitrage-trail list` puis `convert` dessus vers vault/.
Fais l'inventaire des avertissements et des anomalies, compare avec les
hypothèses de docs/formats/README.md, remplis la section « Constaté », puis
propose les corrections de parser avant de les appliquer. Un test par écart,
avec une fixture synthétique ou anonymisée.
```

## Variante : jour du VPS

```
Tu reprends Arbitrage Trail. Lis AGENTS.md et HANDOFF.md. J'ai un VPS
(<distribution>, accès SSH). J'ai tranché Q-A = <…> et Q-B = <…>. Écris les
deux ADR correspondants, puis guide-moi pas à pas dans docs/infra-vps.md §4 :
une commande à la fois, en vérifiant chaque résultat avant la suivante. Coche
les critères de specs/004 au fur et à mesure.
```

## Variante : spike URL

```
Tu reprends Arbitrage Trail. Lis AGENTS.md, HANDOFF.md et
specs/005-recuperation-par-url/spec.md. Régime Unbounded : spike seulement,
pas d'implémentation. Voici deux liens de partage : <…>. Examine ce que
contient la page sans JavaScript, écris le résultat dans la spec, et présente-
moi les options (a), (b), (c) avec leur coût. Ne tranche pas Q-D à ma place.
```

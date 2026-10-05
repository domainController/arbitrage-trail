# Spec 004 : Déploiement sur le VPS et arrivée dans le vault

**Régime : Bounded.** Le déploiement se fait en deux temps (ADR 0004) :
provisoire d'abord, avec des choix réversibles, puis définitif une fois Q-A et
Q-B tranchées après la prise en main.

**État : fichiers prêts (`deploy/`), procédure écrite (`docs/infra-vps.md`),
rien d'exécuté. Le VPS n'existe pas encore.**

**Prérequis** : T2 fait en local (parsers validés sur un vrai export).

## Critères d'acceptation : déploiement provisoire

Choix par défaut : Q-A = Tailscale, Q-B = téléchargement manuel.

- [ ] Service systemd actif, `curl 127.0.0.1:8765/api/config` répond.
- [ ] Page accessible depuis le téléphone, **et pas depuis Internet** (vérifier
      depuis une connexion hors tailnet).
- [ ] Un export déposé via la page se télécharge en `.zip` et s'ouvre dans
      Obsidian après dépôt manuel.
- [ ] Procédure de mise à jour testée une fois.

## Critères d'acceptation : déploiement définitif

Après la période de prise en main.

- [ ] Q-A confirmée ou révisée, consignée en ADR.
- [ ] Q-B tranchée (téléchargement, Syncthing ou git), consignée en ADR.
- [ ] Si Syncthing ou git : un export converti via la page apparaît dans
      Obsidian sur l'ordinateur **et** sur le téléphone, sans geste manuel.

# Spec 004 : Déploiement sur le VPS et arrivée dans le vault

**Régime : Bounded une fois les deux décisions prises** (Q-A accès, Q-B
synchronisation). Avant cela, ne pas déployer.

**État : fichiers prêts (`deploy/`), procédure écrite (`docs/infra-vps.md`),
rien d'exécuté. Le VPS n'existe pas encore.**

## Critères d'acceptation

- [ ] Q-A tranchée (Tailscale recommandé) et consignée en ADR.
- [ ] Q-B tranchée (Syncthing ou git) et consignée en ADR.
- [ ] Service systemd actif, `curl 127.0.0.1:8765/api/config` répond.
- [ ] Page accessible depuis le téléphone, **et pas depuis Internet** (vérifier
      depuis une connexion hors tailnet si option B).
- [ ] Un export converti via la page apparaît dans Obsidian sur l'ordinateur
      **et** sur le téléphone, sans geste manuel (si Syncthing / git).
- [ ] Procédure de mise à jour testée une fois.

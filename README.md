# Arbitrage Trail

> Rien n'est perdu *en silence*.

Sauvegarde des conversations génératives (ChatGPT, Claude) en Markdown, un
fichier par conversation, prêt pour un vault Obsidian. Petit instrument, borné,
sans dépendance.

```bash
python3 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/arbitrage-trail list    export.zip
.venv/bin/arbitrage-trail convert export.zip -o ~/Obsidian/Arbitrage-Trail
.venv/bin/arbitrage-trail serve   # web app sur http://127.0.0.1:8765
```

Pour reprendre le travail : `HANDOFF.md`. Pour un agent : `AGENTS.md`.

| Document | Rôle |
|---|---|
| `docs/00-fondation.md` | Le besoin, tel que formulé à l'origine |
| `docs/01-lecture-critique.md` | Sa formalisation : régimes, promesse, rythmes, frontières |
| `specs/` | Une spec par module, chacune avec son régime |
| `docs/adr/` | Décisions prises |
| `docs/infra-vps.md` | Options et procédure de déploiement |
| `docs/formats/` | Formats d'export attendus et constatés |

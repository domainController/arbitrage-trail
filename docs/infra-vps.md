# Infrastructure : options pour le VPS

> Rien dans ce document n'a été vérifié en ligne ce jour : prix, versions et
> commandes exactes sont à confirmer au moment de l'installation. Les principes,
> eux, ne dépendent pas de ces détails.

## La vraie question

L'app est légère : Python, aucune dépendance, quelques Mo de RAM. Elle tournera
sur n'importe quel VPS. Les deux vraies questions sont :

1. **Qui peut l'atteindre ?** Elle manipule des conversations personnelles.
2. **Comment les fichiers arrivent-ils dans le vault Obsidian**, qui vit sur ton
   ordinateur et ton téléphone, pas sur le VPS ?

## 1. Accès : trois options

### Option A : rien sur le VPS (local seulement)

```bash
git clone https://github.com/domainController/arbitrage-trail.git   # dépôt privé : ton git doit être connecté à GitHub
cd arbitrage-trail && python3 -m venv .venv && .venv/bin/pip install .
.venv/bin/arbitrage-trail convert ~/Downloads/export.zip -o ~/Obsidian/Arbitrage-Trail
```

Zéro infra, zéro exposition. Suffisant tant que tu convertis depuis ton
ordinateur. C'est le point de départ recommandé **demain**, avant que le VPS
existe.

### Option B : VPS privé via Tailscale (recommandé)

Tailscale crée un réseau privé entre tes appareils (ordinateur, téléphone,
VPS). L'app n'est accessible que depuis tes appareils, sans port ouvert sur
Internet.

```bash
# sur le VPS
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# l'app écoute en local, Tailscale l'expose en HTTPS sur le réseau privé
sudo tailscale serve --bg 8765
```

Puis, depuis le téléphone (app Tailscale installée) :
`https://<nom-du-vps>.<ton-tailnet>.ts.net`.

- **Pour** : aucune surface publique, HTTPS automatique, pas de mot de passe à
  gérer dans l'app, fonctionne pour tous tes futurs instruments sur le même VPS.
- **Contre** : une app de plus sur chaque appareil.

### Option C : VPS public + Caddy + mot de passe

Un nom de domaine pointe sur le VPS, Caddy fournit HTTPS automatiquement, l'app
exige un mot de passe (`ARBITRAGE_USER` / `ARBITRAGE_PASSWORD`).

- **Pour** : accessible de n'importe quel navigateur, sans rien installer.
- **Contre** : surface publique, Basic Auth est une protection minimale. À
  réserver au cas où Tailscale est impossible.

Fichiers prêts : `deploy/Caddyfile.example`, `deploy/arbitrage-trail.service`.

## 2. Arrivée dans le vault : trois options

| Option | Principe | Pour | Contre |
|---|---|---|---|
| **Téléchargement** | Bouton « Télécharger (.zip) », tu déposes à la main | Rien à installer | Geste manuel à chaque fois |
| **Syncthing** | Le dossier `--vault` du VPS est synchronisé avec le vault de tes appareils | Automatique, pair-à-pair, existe sur Android | Un service de plus à surveiller |
| **Git** | Le dossier vault du VPS est un dépôt ; commit automatique après écriture ; tu tires depuis tes appareils | Historique complet des versions : cohérent avec « rien n'est perdu » | Moins fluide sur téléphone |

Recommandation : **Syncthing** pour le confort, ou **git** si l'historique des
versions compte (et pour un outil d'arbitrage, il peut compter). Le prototype
écrit les fichiers de façon atomique (fichier temporaire puis renommage) pour
qu'un outil de synchronisation ne voie jamais un fichier à moitié écrit.

## 3. Le VPS comme hôte de plusieurs instruments

Tu prévois plusieurs petits instruments (Arbitrage Trail, semantic-log, Second
Cortex…). Une organisation simple et uniforme évite de réinventer à chaque fois :

```
/srv/
  arbitrage-trail/      code + .venv
  semantic-log/
  second-cortex/
  vault/                le dossier synchronisé avec Obsidian
    Arbitrage-Trail/
    ...
/etc/<instrument>.env   secrets, un fichier par instrument
```

- un utilisateur système et un service systemd par instrument ;
- chaque app écoute sur `127.0.0.1:<port>` (8765 pour Arbitrage Trail) ;
- un seul point d'entrée (Tailscale ou Caddy) qui route vers les ports.

Docker n'est pas nécessaire tant que tout est en Python sans dépendance ; il
deviendra utile si un instrument embarque une base ou un modèle (Ollama pour
semantic-log, par exemple).

## 4. Procédure d'installation (option B), à dérouler le jour J

```bash
# 1. base
sudo apt update && sudo apt install -y python3 python3-venv git
sudo useradd --system --create-home --home-dir /srv/arbitrage-trail arbitrage
sudo mkdir -p /srv/vault/Arbitrage-Trail && sudo chown arbitrage: /srv/vault/Arbitrage-Trail

# 2. code (dépôt privé : utiliser une clé de déploiement en lecture seule)
sudo -u arbitrage git clone git@github.com:domainController/arbitrage-trail.git /srv/arbitrage-trail/app
sudo -u arbitrage python3 -m venv /srv/arbitrage-trail/.venv
sudo -u arbitrage /srv/arbitrage-trail/.venv/bin/pip install /srv/arbitrage-trail/app

# 3. service
sudo cp /srv/arbitrage-trail/app/deploy/arbitrage-trail.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now arbitrage-trail
curl -s http://127.0.0.1:8765/api/config      # doit répondre {"vault": true, ...}

# 4. accès privé
sudo tailscale serve --bg 8765
```

Mise à jour ultérieure :

```bash
sudo -u arbitrage git -C /srv/arbitrage-trail/app pull
sudo -u arbitrage /srv/arbitrage-trail/.venv/bin/pip install /srv/arbitrage-trail/app
sudo systemctl restart arbitrage-trail
```

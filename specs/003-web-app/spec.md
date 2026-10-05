# Spec 003 : Web app

**Régime : Bounded.**

**État : implémentée (`web.py`, `static/index.html`), testée (unittest +
navigateur à 390 px de large).**

## Parcours

1. Ouvrir la page.
2. Déposer le zip d'export (ou `conversations.json`).
3. Voir la liste : titre, date, source, nombre de messages, avertissements.
   Filtrer par titre, cocher / décocher.
4. Au choix : télécharger un `.md`, télécharger la sélection en `.zip`, ou
   « Enregistrer dans le vault » si le serveur a un vault configuré.

## Règles

- **R1.** Bibliothèque standard uniquement (ADR 0002). Pas de framework, pas de
  base de données : le fichier `.md` est la base.
- **R2.** Le serveur ne conserve rien, sauf écriture explicite dans le vault.
- **R3.** Écoute sur `127.0.0.1` par défaut. Avertissement au démarrage si on
  écoute ailleurs sans authentification.
- **R4.** Authentification Basic optionnelle (`ARBITRAGE_USER`,
  `ARBITRAGE_PASSWORD`), comparaison en temps constant. Uniquement derrière HTTPS.
- **R5.** Taille maximale configurable (`ARBITRAGE_MAX_MB`, 500 par défaut). Les
  exports de comptes anciens peuvent être lourds.
- **R6.** Utilisable sur téléphone.

## Limites connues

- Le fichier est réenvoyé au serveur à chaque action (liste, zip, vault). Sans
  importance en réseau local ; à revoir si les exports dépassent la centaine de
  Mo sur une connexion mobile.
- L'export entier est chargé en mémoire. Idem.

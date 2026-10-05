# Formats d'export des plateformes

Un fichier par plateforme : ce qu'on **attend** (hypothèses du parser) et ce
qu'on a **constaté** sur un vrai export. Tant que la section « Constaté » est
vide, le parser repose sur des hypothèses.

| Plateforme | Parser | Constaté sur un vrai export |
|---|---|---|
| ChatGPT | oui | non |
| Claude | oui | non |
| DeepSeek | non | non |
| Gemini | non | non |

---

## ChatGPT

**Obtenir l'export** : Paramètres → Contrôle des données → Exporter les données.
Lien envoyé par e-mail (délai variable), zip valable un temps limité.
*(Chemin dans les menus à revérifier.)*

**Attendu** : `conversations.json` = liste de conversations ;
`mapping` = arbre `{id: {message, parent, children}}` ; `current_node` = feuille
affichée ; `message.content.content_type` ∈ `text`, `multimodal_text`, `code`,
`execution_output`, `thoughts`, … ; horodatages en secondes epoch (float).
Fichiers téléversés probablement présents dans le zip à côté du JSON.

**Constaté** : *(à remplir, tâche T1.6)*

---

## Claude

**Obtenir l'export** : Paramètres → Confidentialité → Exporter les données.
Lien envoyé par e-mail. *(Chemin à revérifier.)*

**Attendu** : `conversations.json` = liste ; `uuid`, `name`, `created_at`,
`updated_at` (ISO 8601) ; `chat_messages` linéaire ; `sender` ∈ `human`,
`assistant` ; `text` et parfois `content` (blocs `text`, `thinking`,
`tool_use`, `tool_result`) ; `attachments` (avec texte extrait) et `files`.
Les artefacts n'apparaîtraient que sous forme de blocs d'outils.

**Constaté** : *(à remplir, tâche T1.6)*

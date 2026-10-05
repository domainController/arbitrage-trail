# Tâches : spec 001

- [x] T1.1 Modèle pivot `Conversation` / `Message`.
- [x] T1.2 Parser ChatGPT (arbre, branche affichée, code, images, raisonnement).
- [x] T1.3 Parser Claude (blocs de contenu, pièces jointes, repli sur `text`).
- [x] T1.4 Chargement zip / JSON, détection de format.
- [ ] T1.5 **(utilisateur)** Demander les exports ChatGPT et Claude. Ils arrivent
      par e-mail, parfois après plusieurs heures.
- [ ] T1.6 `arbitrage-trail list <export>` sur chaque vrai export ; noter :
      types de contenu inconnus (avertissements), conversations vides,
      dates absentes, titres bizarres.
- [ ] T1.7 Corriger les parsers ; ajouter un test par écart trouvé.
- [ ] T1.8 Extraire 2–3 conversations réelles **anonymisées** comme nouvelles
      fixtures. Ne jamais committer un export complet.

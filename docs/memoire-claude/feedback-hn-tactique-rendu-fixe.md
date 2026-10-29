---
name: feedback-hn-tactique-rendu-fixe
description: "Hockey Nation tactique = toujours le même rendu depuis les vues gold.hn_tactique_* ; tous les joueurs par poste, spéciales, plan de jeu ; lineup mise à jour à chaque étude de matchs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0f2646b4-ef59-453b-9697-e4298851915a
  modified: 2026-10-29T16:28:02.533Z
---

Pour la tactique Hockey Nation, l'utilisateur veut **à chaque fois le même export, le même résultat** : tous les joueurs par poste, lignes + paires D + gardiens, PP1/PP2, PK4/PK3, 4v4, EXT, rôles, plan de jeu, « que ça soit beau » (2026-10-29, « c'est GENIAL » sur l'ordre d'entraînement en vue gold).

**Why:** il veut un livrable stable qu'on compare d'une fois à l'autre, sans rédaction à la main.

**How to apply:** lire `gold.hn_tactique_effectif_poste`, `gold.hn_tactique_rendu`, `gold.hn_tactique_plan_rendu`, `gold.hn_tactique_controle` et afficher tel quel. Quand l'étude des matchs montre une amélioration : UPDATE `gold.hn_tactique_cible` + ligne dans `gold.hn_tactique_journal` + fichier SQL versionné. Voir [[feedback-format-tactique-parfait]] et [[feedback-hockeynation-rendu-tableaux]].

**2026-10-29, après saisie de la v2 (« SUPER ! ne change jamais le rendu ») :** le rendu est figé (mêmes tableaux, même ordre, « jeu : X » entre parenthèses, pastilles 🟥/🟧). Objectif permanent : toujours la meilleure tactique possible et construire la meilleure équipe possible, en reliant trades, effectif et analyse de matchs à la lineup cible (un achat/échange se juge sur son effet dans la lineup : poste, END, FOF, PP/PK). **Why:** il a validé ce format et veut que chaque décision d'équipe serve la tactique. **How to apply:** Transferts/Effectif/Match partent de `gold.hn_tactique_effectif_poste` et proposent des leviers nommés ; après chaque étude, mettre à jour la cible.

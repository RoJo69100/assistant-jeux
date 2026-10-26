---
name: project-base-transferts-bonnes-affaires
description: "Tous les jeux : chasser les bonnes affaires (joueur très bas prix, achat-revente), tenir une base des transferts passés pour juger si un joueur vaut le coup, puis seulement le delta ; décider de l'usage de l'argent"
metadata:
  node_type: memory
  type: project
  originSessionId: 51b3c17e-7626-42cd-8353-9948150420e9
  modified: 2026-10-26T20:43:54.693Z
---

Demande du 2026-10-26 (valable pour tous les jeux) : l'agent Transferts cherche activement les bonnes affaires, y compris **acheter très bas pour revendre** (hypothèse à prendre en compte, avec la taxe de 5 % et le délai d'une semaine de BasketVibe). Je me construis une **base des joueurs déjà transférés** (BasketVibe : `bronze.raw_pages` page_type `transfers_global-history`, 7 captures le 2026-10-26 ; prix final selon âge, poste, compétences) pour juger si un joueur vaut le coup ; ensuite seulement le delta. Et il a beaucoup d'argent : toujours poser la question « qu'est-ce qu'on fait de l'argent ? ».

**Why:** l'utilisateur ne veut pas de « aucun achat » par défaut quand le solde est large (1 105 193 le 2026-10-26) ; il veut des leviers.

**How to apply:** vue gold d'historique de transferts par jeu (conception, Opus), prix de référence par âge/poste, détection des annonces sous le prix de référence, marge nette de revente. Chaque brief Transferts : bonnes affaires nommées + usage de l'argent. [[feedback-rendu-demain-seulement]]

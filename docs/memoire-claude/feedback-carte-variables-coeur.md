---
name: feedback-carte-variables-coeur
description: "Cœur du projet (2026-10-31) — on trouve une info une fois, on note où (carte par jeu × type de décision), ensuite on ne lit que le nouveau ; les checks s'améliorent avec les matchs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2a6c3e7a-9937-4c9e-bfcf-ef153e4837b3
  modified: 2026-10-31T13:47:17.007Z
---

Chaque décision importante a une carte `docs/decisions/cartes/<jeu>/<type>.md` : variable → où la lire (requête exacte / fichier § section) → check (règle, seuil) → source → dernière valeur. `pipelines/dossier.py` rend la carte + seulement le nouveau depuis le commit « Sources lues » (git diff des skills, fiches, connaissance, learnings, Discord/chat). Fin : carte à jour, commit, `--marquer`.

**Why:** l'utilisateur : « il faut pas relire à chaque fois tout… s'il y a du nouveau dans la règle, il modifie ce check » ; « tu dois apprendre des matchs, être meilleur plus le temps avance… c'est LA CHOSE PRINCIPALE ».

**How to apply:** jamais `--complet` par habitude ; toute variable trouvée hors carte est ajoutée à la carte ; chaque L-nnn devient un check ; un check contredit deux fois est réécrit (historique daté). Complète [[feedback-dossier-complet-police]].

Fait : BasketVibe le 2026-10-31 (registre `docs/couverture/basketvibe.md`, 7 cartes, vue `gold.bv_league_top_players`). Veille des messages joueurs faite le 2026-10-31 (3 agents, 26 193 lignes, connaissance.md à jour). Reste pour BasketVibe : mesures v4 par amicaux de test, suspensions introuvables, jauge des autres académies. Prochains jeux, un par session en Opus : Hockey Nation (jeu modèle), Six Zero League, Team Soccer, Hardwood, Derby Manager (`docs/chose-a-DM.txt`).

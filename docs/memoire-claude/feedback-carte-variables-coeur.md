---
name: feedback-carte-variables-coeur
description: "Cœur du projet (2026-10-31) — on trouve une info une fois, on note où (carte par jeu × type de décision), ensuite on ne lit que le nouveau ; les checks s'améliorent avec les matchs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2a6c3e7a-9937-4c9e-bfcf-ef153e4837b3
  modified: 2026-10-31T12:40:27.598Z
---

Chaque décision importante a une carte `docs/decisions/cartes/<jeu>/<type>.md` : variable → où la lire (requête exacte / fichier § section) → check (règle, seuil) → source → dernière valeur. `pipelines/dossier.py` rend la carte + seulement le nouveau depuis le commit « Sources lues » (git diff des skills, fiches, connaissance, learnings, Discord/chat). Fin : carte à jour, commit, `--marquer`.

**Why:** l'utilisateur : « il faut pas relire à chaque fois tout… s'il y a du nouveau dans la règle, il modifie ce check » ; « tu dois apprendre des matchs, être meilleur plus le temps avance… c'est LA CHOSE PRINCIPALE ».

**How to apply:** jamais `--complet` par habitude ; toute variable trouvée hors carte est ajoutée à la carte ; chaque L-nnn devient un check ; un check contredit deux fois est réécrit (historique daté). Complète [[feedback-dossier-complet-police]].

---
name: feedback-dm-condition-forme-avant-composition
description: "Derby Manager : lire condition, forme et sharpness de chaque joueur (gold.dm_effectif) avant toute composition ; les titulaires sont cramés, la note de poste seule ne suffit pas (2026-11-06)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 78217928-ad50-4892-a38b-144b2b54e727
  modified: 2026-11-06T21:07:26.441Z
---

Avant toute composition Derby Manager, lire `condition_pct`, `form` et `sharpness` de `gold.dm_effectif` pour chaque titulaire et chaque remplaçant, pas seulement `note_poste` de `gold.dm_saisie_squad`. Les matchs sont quotidiens : les titulaires sont cramés (73-88 % de condition le 2026-11-06 après 4 matchs), les réservistes sont à 100 % mais forme 0 et sharpness 1.

**Why:** le 2026-11-06 j'ai proposé Bock à la place d'Arneberg sur la seule note de poste (11,5 contre 10,8) alors que Bock a 0 match, forme 0, sharpness 1 ; l'utilisateur m'a repris : « tu n'as pas pris en compte la forme, la condition, choses très importantes, les joueurs sont cramés, tu devrais le voir dans l'export ».

**How to apply:** tableau condition / forme / sharpness / apps à côté de la note avant de proposer un changement ; règle du jeu dans `derbymanager-regles/references/04-forme-condition-sharpness.md` (blessure = condition manquante, chaque option tactique cochée = −1 % à tous). Voir [[feedback-dm-scouts-academie-gratuits]] et [[project-derbymanager-etat-04-11]].

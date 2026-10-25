---
name: feedback-hn-talents-par-poste
description: "Hockey Nation — juger tout joueur (draft, trade, extension, ligne) sur ses talents fort/faible contre le poste, pas seulement sa note ou ses points"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38147e78-3bd6-4ecb-9584-7e729acc3a46
  modified: 2026-10-23T15:21:57.744Z
---

Pour tout joueur Hockey Nation, lire `talent_strongest` (2 compétences au plus fort potentiel) et `talent_weakest` contre les compétences clés de son poste (`gold.hn_player_fit`, `gold.hn_draft_board`). Un ailier dont les talents forts sont DEF et CHK n'intéresse pas l'utilisateur. Les joueurs à double poste (ex. Flink, Blednov RW/C) l'intéressent : vérifier le poste où leurs talents collent le mieux.

**Why:** l'utilisateur, 2026-10-23 : « il faut qu'on regarde aussi strongest talent et weakest talent … très important pour la suite ». Il a drafté sur les buts/assists ; j'avais retiré Degryse alors que ses talents (GLO, BLO) sont idéaux pour un gardien.

**How to apply:** toute recommandation de joueur HN cite le verdict talents (idéal / correct / contre-emploi). Voir [[feedback-aucun-flou-noms-et-donnees]].

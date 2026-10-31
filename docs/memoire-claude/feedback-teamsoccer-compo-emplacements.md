---
name: feedback-teamsoccer-compo-emplacements
description: "Team Soccer compo validée le 2026-10-31 : colonnes Ultra déf. / Défensive / Médiane / Offensive / Finition + emplacement précis DL/DC/DR et ML/MC/MR (pas DEF/MIL)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5cb4d2e1-13d8-48c1-abb8-ad1a6a727460
  modified: 2026-10-31T18:53:50.982Z
---

Format de composition Team Soccer validé par l'utilisateur (2026-10-31, « super pour les tableaux, tu as mis les bons ordres ») : un tableau par club, une ligne par joueur, colonnes **Ultra déf. | Défensive | Médiane | Offensive | Finition** (consignes + cible « → » milieux/attaquants/défenseurs/ailiers), puis banc de 6 (GB, DC, MC, AC couverts) et « aucun remplacement programmé ».

**Correction :** la colonne Emplacement n'est jamais « DEF » ou « MIL » : toujours le poste exact de l'écran, DC / DL / DR pour la défense et MC / ML / MR pour le milieu. Déduit de l'ordre des emplacements 1–4 (DL, DC, DC, DR) et milieu 5–7 (ML, MC, MR) ou 5–8 (ML, MC, MC, MR) de `silver.ts_match_lineups.player_positions` (cohérent avec Mansour/Martínez, ailières, aux côtés) ; à vérifier une fois sur l'écran.

**Toutes les colonnes remplies (2026-10-31, « il faut remplir toutes les colonnes ») :** aucune cellule vide « — » dans une compo : chaque joueur a une consigne dans les 5 zones (Ultra déf. = Dégager, Défensive = Passer → cible, Finition = Tirer pour tous, comme l'utilisateur les saisit ; le GB Dégager partout). Rendre l'état réellement enregistré (`silver.ts_match_lineups.player_orders` du match, export le plus récent), pas ma proposition ; signaler les écarts et le doublon titulaire/banc.

**Why:** l'utilisateur saisit à l'écran poste par poste ; « Zainab García c'est DEF mais faut DC ou DL/DR ». 
**How to apply:** toute composition Team Soccer (Cows et Donkey) ; ChispasFC22 (match 1970802, 02/11 05:00, type inconnu) est une équipe que je n'ai pas pu identifier : ne pas en faire un sujet, l'utilisateur gère. Voir [[feedback-teamsoccer-compo-complete]].

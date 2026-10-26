---
name: feedback-initiative-multi-jeux
description: "Quand je fais quelque chose pour un jeu, je regarde les autres jeux et je complète ce qui n'existe pas, sans demander"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b607e5c9-e728-4f7c-82cd-4347110c87fe
  modified: 2026-10-26T22:55:07.290Z
---

Demande du 2026-10-26 : base des transferts créée pour BasketVibe seul (`gold.bv_transfer_history`) ; l'utilisateur : « t'as tout, tu devrais savoir… prends l'initiative, si tu fais pour un jeu, regarde les autres et complète si ça n'existe pas ».

**Why:** il ne veut pas avoir à répéter une demande jeu par jeu ; la mémoire disait déjà « par jeu » ([[project-base-transferts-bonnes-affaires]]).

**How to apply:** règle A-10 de `docs/attentes/attentes.md`. Après toute création pour un jeu, vérifier Six Zero League, Team Soccer, Hockey Nation (et BasketVibe) : créer l'équivalent si les données le permettent, sinon noter dans la config du jeu ce qui manque. Dire en une ligne ce qui a été étendu.

**À faire demain :** base des transferts pour Six Zero League (`silver.sz_transfer_listings`) et Team Soccer (`silver.ts_transfer_listings`) : vérifier d'abord si les captures contiennent des ventes conclues avec prix final ; Hockey Nation a déjà `gold.hn_trade_value` (échanges, pas de prix).

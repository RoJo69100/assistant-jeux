---
name: feedback-initiative-multi-jeux
description: "Quand je fais quelque chose pour un jeu (surtout une vue gold), je me demande si je la crée sur les autres jeux, et je le fais sans demander"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b607e5c9-e728-4f7c-82cd-4347110c87fe
  modified: 2026-10-30T08:06:20.964Z
---

Demande du 2026-10-26 : base des transferts créée pour BasketVibe seul (`gold.bv_transfer_history`) ; l'utilisateur : « t'as tout, tu devrais savoir… prends l'initiative, si tu fais pour un jeu, regarde les autres et complète si ça n'existe pas ».

Rappel du 2026-10-30 : « il faut que tu gardes cette idée : tu crées une vue gold très intéressante sur un jeu, il faut que tu te dises : est-ce que je la crée sur un autre jeu ? »

**Why:** il ne veut pas avoir à répéter une demande jeu par jeu ; la mémoire disait déjà « par jeu » ([[project-base-transferts-bonnes-affaires]]). Hockey Nation est le jeu modèle ([[feedback-hockeynation-modele-reference]]).

**How to apply:** règle A-10 de `docs/attentes/attentes.md` (précisée le 2026-10-30 pour les vues gold). Dès qu'une vue gold utile est créée pour un jeu, me poser la question pour Six Zero League, Team Soccer, Hockey Nation et BasketVibe dans la même session : créer l'équivalent si les données le permettent, sinon noter dans la config du jeu ce qui manque. Dire en une ligne ce qui a été étendu.

**À faire :** base des transferts pour Six Zero League (`silver.sz_transfer_listings`) et Team Soccer (`silver.ts_transfer_listings`) : vérifier d'abord si les captures contiennent des ventes conclues avec prix final ; Hockey Nation a déjà `gold.hn_trade_value` (échanges, pas de prix).

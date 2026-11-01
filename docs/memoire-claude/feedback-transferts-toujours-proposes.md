---
name: feedback-transferts-toujours-proposes
description: "Jamais \"je cherche\" sans résultat ; chaque \"que faire\" ouvre par des cibles de transfert chiffrées à vraie valeur ajoutée (2026-11-01)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 742bc766-df25-4412-93eb-b8989d956c18
  modified: 2026-11-01T07:59:58.310Z
---

Chaque réponse "que faire" contient les transferts dans le même tour : cibles nommées, enchère maximale, finançabilité, valeur ajoutée réelle ; sinon la raison chiffrée de n'en proposer aucune. Jamais "je cherche" sans lancer la requête.

**Why:** 2026-11-01 BasketVibe, l'utilisateur : « tu ne peux pas dire je cherche et rien faire, c'est très important ». J'avais oublié les enchères Perry/Boskovic (perdues) et les ventes invendues Henry/Lecomte ; première cible proposée (Grassi) était faible.

**How to apply:** `gold.bv_market_bargains` (marge de revente p25/médiane) + `gold.bv_market_candidates` (gain au poste). Une cible vaut seulement si elle améliore un titulaire ou si la marge de revente au p25 est positive. Vérifier aussi les ventes ouvertes. Voir règle 29 de `docs/retro/regles-apprises.md`, [[feedback-seulement-ce-qui-est-possible]].

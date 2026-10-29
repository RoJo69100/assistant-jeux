---
name: project-reprise-3-jeux-2026-10-30
description: "Première chose à faire à la prochaine session (2026-10-30) : lancer les agents sur Six Zero League, Team Soccer, BasketVibe, un jeu après l'autre"
metadata:
  node_type: memory
  type: project
  originSessionId: cfcf7244-e7c4-4924-a703-f910814ae91f
  modified: 2026-10-29T22:21:02.436Z
---

Demandé le 2026-10-29 : « on fera demain, mets-le dans la première chose à faire ». Dérogation explicite à la règle horizon (l'utilisateur a lui-même reporté).

À faire en début de session du 2026-10-30, dans cet ordre, un jeu à la fois (3 agents au plus par jeu, tableau rendu avant de passer au suivant) :
1. Six Zero League : lecteur-exports puis match / effectif / transferts selon ce qu'il trouve. Aucun brief d'agent depuis le 2026-10-27, exports du 29/10 en base (jusqu'à 11:26 Paris).
2. Team Soccer : transferts + finances (marché, finances, stade, haute performance exportés à 15:20 Paris, après les briefs de 15:09). Briefs du 29/10 non commités dans git.
3. BasketVibe : transferts + tableau tactique de l'amical via gold.bv_saisie_* (exports de 14:56 Paris, après les briefs de 11:15).

**Why:** la session du 29/10 s'est arrêtée avant le lancement ; l'utilisateur n'a pas pu continuer ce soir.
**How to apply:** au début de session, demander `/effort medium` (règle 26), charger deja-fait, relire ce plan, annoncer la durée, puis commencer par Six Zero League. Voir [[feedback-horizon-aujourdhui-demain]].

**Ajout 2026-10-29 (soir)** : avant les agents, séance de conception en Opus pour SZL puis Team Soccer : créer les vues gold du modèle Hockey Nation (`*_today`, `*_exports_state`, `*_saisie_*`) car SZL n'a que `sz_agenda` (11 vues) et TS que `ts_agenda` + `ts_saisie_composition` (20 vues) contre 34 pour HN et 48 pour BV. Team Soccer : marché féminin à ré-exporter (dernier relevé 27/10), état des 8 enchères Cows absent en base, vente Girard (267 689 $) à décider, veille la plus ancienne (27/10). Retour Sonnet + medium ensuite.

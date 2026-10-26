---
name: feedback-bv-fiche-saisie-complete
description: "BasketVibe — toute tactique donnée = fiche de saisie complète, ligue et amical séparés, valeurs d'écran absolues, jamais de « inchangé »"
metadata:
  node_type: memory
  type: feedback
  originSessionId: cf38de0d-12fa-48ec-b712-82e9ad29caf0
  modified: 2026-10-25T08:08:53.388Z
---

Quand je donne une tactique BasketVibe, je donne **tout ce qu'il faut saisir**, en deux blocs séparés : **LIGUE** et **AMICAL**.
- Cinq par quart-temps (Q1–Q4, OT) avec le poste de chaque joueur, minutes par joueur.
- Pour **chaque joueur (les 17)** : Role (passe/tir), Offensive focus, Shooting focus, Defense (agressivité), en valeurs d'écran 1–5 absolues. Jamais « inchangé », jamais « 4 → 3 » seul, jamais les valeurs internes 0–4 de la base (écran = tier + 1).
- Defensive focus **pour chaque joueur adverse nommé** (1 Give up … 5 Lock). Amical : en plus Defensive area (Perimeter/Middle/Rim) par adversaire.
- Les valeurs actuelles se lisent dans `silver.bv_match_tactics.player_directives` (role_tier, offensive_focus_tier, shot_tier, defense_tier ; ne pas trier par fixture_id, c'est un uuid).

- **Ordre des joueurs = ordre de l'écran Schedule** : par poste PG, SG, SF, PF, C, alphabétique dans chaque poste (Baron, Boyer, Fontaine, Richard / Bonnet, Dang, Henry, Leclerc / Durand, Gimenez, Lecomte / Albano, Lefebvre, Legrand / Bernard, Fournier, Klein). Demandé le 2026-10-25 pour recopier ligne à ligne.

- **Les tableaux de focus défensif adverse (ligue : sans area ; amical : focus + area) sont toujours dans le même message que les consignes**, jamais renvoyés à un message précédent. Validé par l'utilisateur le 2026-10-25 : « parfait, à chaque fois tu fais ça ».

- **Les adversaires aussi dans l'ordre de l'écran** : par poste PG, SG, SF, PF, C puis alphabétique sur le nom de famille (hypothèse non confirmée pour l'écran adverse). Colonnes : Poste · Joueur · Focus (· Area en amical). Demandé le 2026-10-25.

**Why:** 2026-10-25, l'utilisateur : « tu me donnes ton réglage pour les matchs, je comprends rien ». Les briefs ne montraient que les deltas et renvoyaient à d'autres sections.
**How to apply:** fiche autonome, une seule version consolidée (analyse de défaite incluse), sans renvoi à un autre brief. Voir [[feedback-synthese-precise-par-jeu]] et [[feedback-bv-amical-sans-preview]].

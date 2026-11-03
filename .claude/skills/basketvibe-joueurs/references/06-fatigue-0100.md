## Fatigue (0–100) [M§5.6]
- **Gain après un match** = minutes × 0,19 × multiplicateur d'agressivité défensive × (1,5 − 0,008 × Endurance).
- **Récupération chaque nuit** = 0,5 + 10 % de la fatigue actuelle (identique pour tous ; l'endurance n'aide pas).
- Amical ≈ 1/10. Coupe : 0 par défaut. Remise à 0 en début de saison.
- La pénalité est fixée par la fatigue au coup d'envoi et reste la même tout le match (s'asseoir un quart-temps ne la réduit pas) :

| Fatigue | 0 | 20 | 40 | 60 | 100 |
|---|---|---|---|---|---|
| Attaque | 0 % | −3 % | −10 % | −20 % | −40 % |
| Défense | 0 % | −2 % | −6 % | −13 % | −26 % |

  Variation linéaire entre ces points. Zones : vert 0–20, jaune 20–40, orange 40–60, rouge 60–100 [M§5.6.1].
- ⚠️ **Moteur v4 (amicaux depuis le 17/10, ligue en saison 2)** : une seule échelle, plus dure, pour l'attaque et la défense : 20 → −4 % ; 40 → −15 % ; 60 → −30 % ; 80 → −50 % [News 2026-10-17]. Détail dans basketvibe-communaute. *Avis (pas une règle)* : en saison 2, viser une fatigue au coup d'envoi en zone verte (≤ 20) pour les titulaires.
- ⚠️ Hypothèse (V-20261030-6) : avant le moteur v4, le développeur a remis lui-même la fatigue à zéro (« repos » au back-office) : 2026-08-19 (par jour sur les amicaux), 2026-08-24 (doublon par erreur), 2026-08-29 (« daily » et avant la dernière journée), 2026-09-13 (solution temporaire) [Dev #general 2026-08-19 09:02, 2026-08-24 19:11, 2026-08-29 13:03 ; release-notes 2026-08-29 ; Dev 2026-09-13 13:31]. On ignore s'il le fait encore : une fatigue plus basse que prévue (`gold.bv_fatigue_plan`) peut venir de là.
- Multiplicateur d'agressivité défensive : soft ×0,75 · ×0,875 · équilibré ×1,00 · ×1,325 · agressif ×1,65 [M§6.3].
- Fatigue stabilisée avant un match du samedi (même usage chaque semaine), extrait [M§5.6.4] :
  - défense équilibrée, endurance 50 : 24 min → 12 ; 36 min → 21 ; 48 min → 30 ;
  - défense agressive, endurance 50 : 36 min → 38 ; 48 min → 52 (orange).


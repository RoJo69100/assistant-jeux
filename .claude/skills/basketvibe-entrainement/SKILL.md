---
name: basketvibe-entrainement
description: Règles BasketVibe de l'entraînement et de la progression — choix principal/secondaire, gains par semaine, potentiel caché (1–10) et son effet, ralentissement au-dessus de 70, courbe d'âge, arrêt à 30 ans, déclin à partir de 31, TSP. À charger pour choisir les entraînements, estimer un potentiel, projeter un joueur sur 1 à 3 saisons.
---

# BasketVibe — entraînement, potentiel, vieillissement

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide (lu le 2026-10-16). **[Obs]** = nos données.

## Fonctionnement [M§8, §1.3]
- Une fois par semaine, le **dimanche à minuit sur le calendrier mondial** [Obs : 04:00 à Paris]. Environ 8 entraînements par saison.
- Pour chaque joueur, deux compétences différentes : une **principale** et une **secondaire**. Sauvegarder avant le passage du dimanche.
- **Joueur blessé = pas de progression cette semaine-là** (ses choix restent enregistrés).
- V-20261027-7 [News 2026-10-25] : l'historique d'entraînement note une ligne chaque semaine, même sans progression, et indique l'entraînement manqué pour blessure. `silver.bv_training_changes` est arrêtée au 18/10 : exporter l'onglet Recent changes le dimanche 01/11 après 04:00.
- La forme et la fatigue n'influencent pas l'entraînement [M§5].
- Le jeu stocke des décimales : une compétence secondaire peut faire +0 puis +1 [M§8].

## Gain par semaine (sur la valeur précise) [M§8.2]
Gain = base × multiplicateur de potentiel × multiplicateur de niveau × multiplicateur d'âge.
- Base : **principale +1,0 ; secondaire +0,5**.
- Âge : maximum vers 18 ans, fort jusqu'au début de la vingtaine, baisse à l'approche de 30, **0 à 30 ans**.
- Repères (potentiel 5, compétence sous 80) : principale ≈ **+0,7 par semaine à 25 ans** ; ≈ **+1,15 à 18 ans**. Plafond 99.

## Potentiel caché 1–10 [M§8.3]
Fixé à l'entrée du joueur dans le monde, ne change jamais, invisible. Il **multiplie** le gain hebdomadaire ; ce n'est **pas un plafond**.

| Potentiel | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Multiplicateur | 0,45 | 0,65 | 0,83 | 1,00 | 1,15 | 1,35 | 1,50 | 1,60 | 1,85 | 2,20 |
| Principale par semaine (16–18 ans, < 80) | +0,45 | +0,65 | +0,83 | +1,00 | +1,15 | +1,35 | +1,50 | +1,60 | +1,85 | +2,20 |

Gains affichés sur une saison (~8 semaines, compétences < 80, sans blessure) [M§8.3] :
| Potentiel | 16 ans : principale / secondaire / total | 25 ans : principale / secondaire / total |
|---|---|---|
| 1 | 3 / 1 / 4 | 2 / 1 / 3 |
| 2 | 5 / 2 / 7 | 3 / 1 / 4 |
| 3 | 6 / 3 / 9 | 4 / 2 / 6 |
| 4 | 8 / 4 / 12 | 4 / 2 / 6 |
| 5 | 9 / 4 / 13 | 5 / 2 / 7 |
| 6 | 10 / 5 / 15 | 6 / 3 / 9 |
| 7 | 12 / 6 / 18 | 7 / 3 / 10 |
| 8 | 12 / 6 / 18 | 7 / 3 / 10 |
| 9 | 14 / 7 / 21 | 9 / 4 / 13 |
| 10 | 18 / 9 / 26 | 10 / 5 / 15 |
Arrondis et semaines manquées : ±1. À 29 ans, gains inférieurs à la colonne 25 ans.

Révéler le potentiel : « Send for tests » à 25 000, sur un prospect d'académie ou un joueur en vente. On obtient seulement une catégorie : Low (1–3), Decent (4–7), High (8–10) [M§4.2, §11.3].

## Ralentissement au-dessus de 70 [M§8.4]
Selon la valeur précise **avant** le passage de l'entraînement (principale et secondaire comptées séparément) :
| Valeur | < 70 | 70 | 75 | 80 | 85 | 90 | 95 | 99+ |
|---|---|---|---|---|---|---|---|---|
| Multiplicateur | ×1 | ×1 | ×0,88 | ×0,75 | ×0,63 | ×0,50 | ×0,21 | ×0 |
Exemple (16–18 ans, potentiel 5) : principale +1,01 par semaine à 75, +0,86 à 80, +0,58 à 90, +0,24 vers 95.

## Après 30 ans [M§8.5]
- 30 ans : les choix d'entraînement n'apportent plus rien.
- À partir de 31 ans : chaque dimanche, **toutes** les compétences baissent. S'entraîner ne compense pas. Le potentiel ne change rien au déclin.
- Perte par saison, par compétence (total des 8) : 31 ans ~1 (~8) ; 33 ans ~2 (~16) ; 35 ans ~4 (~32) ; 38 ans ~5 (~40).
- Retraite à la fin de la saison des 38 ans [M§4].

## TSP (somme des 8 compétences) [M§8.6]
Exemples de carrière : junior de 16 ans recruté au milieu de sa fourchette, entraîné de façon optimale (une compétence jusqu'à 80, puis la suivante), TSP au début de ses 31 ans :
| Académie au rapport | Potentiel | TSP typique au recrutement | TSP au sommet (31 ans) | Fréquence |
|---|---|---|---|---|
| 60 % | 6 | ~304 | ~463 | 2–3 fois par saison |
| 70 % | 7 | ~320 | ~496 | Probable |
| 80 % | 8 | ~336 | ~524 | Rare mais accessible |
| 90 % | 9 | ~360 | ~577 | Rare |
| 100 % | 10 | ~360 | ~623 | Exceptionnel |

## Méthode d'estimation du potentiel (à partir de nos données)
**Ceci est une méthode de calcul, pas une règle du jeu.** Elle s'appuie sur les règles ci-dessus.
- Mesurer le gain réel de la compétence principale sur plusieurs semaines (`silver.bv_player_daily.*_exact`, `gold.bv_skill_progress_weekly`) ; ne retenir que les semaines où le joueur n'était pas blessé et où la compétence était sous 70.
- Comparer ce gain au tableau ci-dessus : âge × potentiel donne le gain attendu. Le manuel ne publie la courbe d'âge exacte qu'à 16–18 ans et 25 ans : entre ces âges, l'estimation est approximative et doit être donnée avec un niveau de confiance.
- Les valeurs précises (décimales) de la page Entraînement permettent une mesure bien plus fine que les chiffres affichés.

### Lecture du potentiel d'un junior sans décimales (16–18 ans, compétence < 70, non blessé) — calcul sur [M§8.3], pas une règle
Hypothèses : départ sans décimales [Dev 2026-09-13, help], facteur d'âge 1 à 16–18 ans, secondaire = moitié de la principale. Concorde avec les observations de joueurs [Com 2026-10-14, dcarra, italia ; Com 2026-10-18, chanceler, portugal ; Com 2026-10-17, aeolian06, general]. Le calcul exact sur décimales reste dans `gold.bv_potential_estimate` (sert de référence quand il a des gains).
Points gagnés par la principale semaine par semaine (entiers affichés, cumul = partie entière de n × multiplicateur) :
| Potentiel | Sem. 1 | Sem. 2 | Sem. 3 | Sem. 4 | Sem. 5 | Cumul sem. 5 |
|---|---|---|---|---|---|---|
| 10 | +2 | +2 | +2 | +2 | +3 | 11 |
| 9 | +1 | +2 | +2 | +2 | +2 | 9 |
| 8 | +1 | +2 | +1 | +2 | +2 | 8 |
| 7 | +1 | +2 | +1 | +2 | +1 | 7 |
| 6 | +1 | +1 | +2 | +1 | +1 | 6 |
- Potentiel 8 à la semaine 5 : 5 × 1,60 = 8,0 pile, donc sensible aux arrondis (la valeur peut s'afficher 7 ou 8) ; ne pas conclure sur cette seule semaine.
- La secondaire fait +1 dès la semaine 1 seulement au potentiel 10 (1,1) ; potentiel 9 : 0 puis +1 ; potentiel 8 : 0, 1, 1, 1, 1.
- **Les potentiels 7 et 8 sont identiques pendant 4 semaines** (cumul 6) ; ils ne se séparent qu'à la semaine 5. 3 semaines suffisent pour 10 contre 9 contre ≤ 8.

## Lecture de nos données
- `silver.bv_player_weekly` : relevé hebdomadaire (valeurs précises + entraînement en cours).
- `silver.bv_training_changes` : chaque progression (avant → après) des ~6 dernières semaines.
- `gold.bv_skill_progress_weekly` : points gagnés par joueur, compétence et semaine.
- [Obs] La page Progress du jeu compte le **nombre** de progressions, pas les points (un +2 compte pour 1).

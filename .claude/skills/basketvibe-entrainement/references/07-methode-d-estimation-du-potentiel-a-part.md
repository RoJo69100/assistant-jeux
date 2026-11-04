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


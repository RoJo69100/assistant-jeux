Amical contre General Mines Ironmasters (21/11)
Verrou : sam. 21/11 07:45 (match 08:00)
Adversaire : General Mines Ironmasters (joueurs inconnus)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Boyer | Legrand | Bernard |
| Q2 | Boyer | Durand | Leclerc | Albano | Bernard |
| Q3 | Baron | Leclerc | Boyer | Legrand | Albano |
| Q4 | Baron | Durand | Albano | Legrand | Bernard |
| Prol. | Baron | Boyer | Durand | Legrand | Albano |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | PG | PG | 36 (+5) | 3 | 3 | 3 | 5 |
| Boyer | PG | SF | PG | SF | — | SG | 36 (+5) | 3 | 3 | 3 | 5 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Leclerc | SG | SG | SF | SG | — | — | 36 | 3 | 3 | 3 | 5 |
| Durand | SF | — | SG | — | SG | SF | 24 (+5) | 3 | 3 | 3 | 5 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Albano | PF | — | PF | C | SF | C | 36 (+5) | 3 | 3 | 3 | 5 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Legrand | PF | PF | — | PF | PF | PF | 36 (+5) | 3 | 3 | 3 | 5 |
| Bernard | C | C | C | — | C | — | 36 | 3 | 3 | 3 | 5 |
| Fournier | C | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 | tous | 3 (Normal) | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Agress. = 5 pour chacun des 12 joueurs
- [ ] Off. focus = 3, Rôle = 3, Tir = 3 pour les 12 joueurs
- [ ] Durand : Min = 24
- [ ] Les 12 adversaires : focus 3, zone Perimeter (1)
## À exporter ensuite
La page du match, après la fin du match (~08:55) : elle donnera les noms adverses.

---
## Annexe — pourquoi

Saisie AUJOURD'HUI jeudi 19/11 (heure Paris 10:43, `pipelines/heure_paris.py`) pour l'amical du 21/11 08:00. Amical : pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Consigne : un seul test, E1 niveau B (`docs/attentes/experiences-amicales-basketvibe.yaml`), agressivité 5 à l'écran (cran 4) pour les 12 joueurs, y compris ceux à 0 min ; tout le reste au neutre.

### Réglage neutre (yaml `neutre` + constants E1)
Zone Perimeter (1), focus défensif 3 sur les adversaires, Off. focus 3 (aucun Primary), aucun Tir cran 4 (Tir 3 écran = cran 2). Rôle 3 et Tir 3 : le yaml ne fixe pas de neutre pour ces deux colonnes, je prends l'écran 3 pour qu'aucune autre variable ne bouge. Aucune valeur isolée : seule l'agressivité (5) diffère du neutre, par construction du test.

### Composition (choisie à l'instant T, 7 joueurs utilisés)
Jeunes d'abord [M§5.4] ; titulaires de ligue protégés : ligue J9 le soir même, samedi 21/11 20:00 (`gold.bv_agenda`) ; ils ont joué J8 le 16/11 (`gold.bv_match_player_lines`, ligue : Bonnet 48, Fournier, Gimenez, Durand, Lefebvre, Bernard, Legrand, Boyer, Richard 24). Gimenez, Lefebvre, Richard, Bonnet, Fournier : 0 min. Minutes : Baron, Boyer, Leclerc, Bernard, Legrand, Albano 36 ; Durand 24 ; total 240. Jeunes ≤ 21 ans (Baron 17, Boyer 20, Leclerc 17, Bernard 18) : 144 min sur 240. Sept joueurs pour cinq emplacements forcent Legrand et Albano à 36 min.
Remplaçants (depth chart) : aucun programmé ; hors jeu si besoin : Lefebvre (PF/C), Fournier (C), Richard (PG), Gimenez (SF), Bonnet (SG).

### Contrôle SQL (fait, `gold.bv_slot_fit` + plan en `values`)
- 5 joueurs différents et 5 emplacements par quart : oui (25 lignes de plan jointes, 7 joueurs).
- Maximum 3 quarts par joueur : oui (6 joueurs à 3, Durand à 2) ; aucun `over_36` hors prolongation.
- `height_eff` ≥ 95 : oui, minimum 98,4 (Leclerc).
- `fit_with_form` moyen : Legrand 53,1, Bernard 50,2, Albano 49,4, Boyer 49,2, Baron 45,3, Durand 44,0, Leclerc 41,9 (le plus bas : seul SG/SF jeune disponible, amical de formation).
- Forme : relevé du 17/11 (`gold.bv_roster_now.day`, semaine du 15/11), postérieur au dimanche 15/11 : à jour. Baron 6, Leclerc 5, Durand 5 sous 7 [M§5.5] ; ils restent pour le temps de jeu des jeunes. Les amicaux des 19 et 20/11 ne sont pas encore au relevé.
- Blessés : aucun (`injury_return_on` vide pour les 12) ; aucun en vente. Plan B : aucun blessé en amical possible [M§1.2].
- Fatigue (`gold.bv_roster_now`) : tous ≤ 21,08 (Bonnet, 0 min). Surcoût de l'agressivité cran 4 : multiplicateur d'amical non présent dans une vue ; ordre de grandeur ≈ 3,5 à 4,3 (dixième de `gold.bv_fatigue_plan`, ligue tier 4, 36 min), non mesuré. Les 7 joueurs du test ne sont pas dans le cinq de ligue de J9.

### Adversaire : General Mines Ironmasters
`gold.bv_saisie_adversaires` : aucune ligne pour lui ; absent des briefs et de `gold.bv_next_opponents` (ligue seulement, requête en délai dépassé : non lue). Joueurs, parts de tirs et 2P/3P inconnus.
**Focus défensif** : aucun joueur adverse connu, donc Normal (3) sur les 12, zone Perimeter, aucun Intense, Light ni Give up. Export à faire : la page du match après ~08:55 le 21/11. Un seul test (agressivité), le focus reste neutre.

### Test E1 niveau B et lecture
Aucun amical en cran 4 depuis `debut` 2026-11-10 ; le niveau B de la file est donc celui-ci (et celui du 20/11 FuzzyTeam, C-128 : deux niveaux B de suite, l'ordre du yaml est A, B, A, B : à signaler, non tranché par moi). Série cran 2 : le 18/11 (Union Heidelberg) L −22, `opp_fg2_pct` 78,0, `pf` 22 ; 12–17/11 `opp_fg2_pct` 49,0–58,0, `pf` 13–19 (`gold.bv_match_report`). Anciens crans 4 (21 et 23/10, L-011) : `pf` 20 puis 27, eFG adverse 59,1 puis 60,7. Hypothèse (confiance faible) : `pf` et `o_fta` montent sans baisse de `opp_fg2_pct` [M§6.3]. Lecture le 21/11 après export : `opp_fg2_pct`, `pf`, `o_fta`, points encaissés contre la série cran 2.
Conseil ajouté : **C-129** dans `outputs/basketvibe/learnings.md`. Aucun levier « interdit » redonné (l'agressivité de ligue n'est pas touchée). Aucun achat, vente ni enchère proposé.

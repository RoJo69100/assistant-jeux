# Journal des enseignements — BasketVibe (Chomelix Cow's)

Tenu par l'agent Match (`.claude/agents/match.md`). Mis à jour après chaque export de match.

**Dernier match analysé : 2026-10-18 — Arios Pagkos (amical) ; dernier match de ligue : 2026-10-17 — Sierra Nevada (J18)** (passage du 2026-10-18, brief `briefs/2026-10-18-match.md`).

## Enseignements
<!-- L-nnn · date · enseignement · matchs de ligue à l'appui · statut (à surveiller / confirmé / infirmé) · source -->
| ID | Date | Enseignement | Matchs ligue | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-10-18 | Victoires et défaites se séparent par le tir (eFG 50,9 contre 42,1), la défense du tir (eFG adverse 43,4 contre 54,2), l'OREB (28,4 contre 19,5) et les pertes adverses (20,4 contre 13,9). Le FT rate ne fait pas la différence. | 18 (7V/11D) | confirmé | `gold.bv_match_factors_by_result` |
| L-002 | 2026-10-18 | Moins de tirs à 3 (part : 44,8 % sur J1–J14, 32,3 % sur J15–J18) va avec une meilleure eFG (43,2 → 53,7). Notre réussite à 3 reste faible (25–29 %). Cause non isolable : 4 changements simultanés. | 4 | à surveiller | `gold.bv_match_report` |
| L-003 | 2026-10-18 | Rotation à 2 unités de 24 min (fin des 5×48) depuis J15 : 3V-1D. Contre les mêmes adversaires qu'à l'aller (J4–J7), cumul +82 contre +34. | 4 | à surveiller | `gold.bv_match_player_lines`, `gold.bv_match_report` ; [M§5.7] |
| L-004 | 2026-10-18 | `defense_tier` 0 depuis J15 (sauf Fournier) : eFG adverse 51,1 → 46,0 (le manuel annonce l'inverse) ; FT rate adverse 31,1 → 19,1 (conforme au manuel). Facteurs confondus. Sens confirmé le 2026-10-18 : cran 0 (écran 1) = Soft. | 4 | à surveiller | `gold.bv_match_player_lines`, `gold.bv_match_report` ; [M§6.3] |
| L-005 | 2026-10-18 | Matchs serrés (écart ≤ 5) : 0 sur 3. En J11 et J16, la fin se joue sur une perte de balle. | 3 | à surveiller (cause non établie) | `gold.bv_match_report`, `silver.bv_match_events` |
| L-006 | 2026-10-18 | Le give_up sur le vrai scoreur adverse (J15 Georgiou, J18 Hola) lui donne 36 à 62 % des tirs et 36 à 39 pts. Miss au sens du manuel. Aucun Hit sur la saison. | 2 | à surveiller | `gold.bv_match_opp_focus` ; [M§6.6], [Com 2026-09-09] |
| L-007 | 2026-10-18 | Sous le régime 5×48 (J1–J14), Q4 à −4,9 contre −3,2 sur les autres quarts : pas de signal net de la pénalité au-delà de 36 min dans le score. | 14 | à surveiller | `gold.bv_match_report` ; [M§5.7] |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut (ouvert / appliqué / partiel / non appliqué) · effet constaté -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-10-16 | Plafonner les minutes à ~34 (Baron, Bernard, Boyer, Fontaine, Fournier, Bonnet, Durand) — agent Effectif, action 1 | `gold.bv_match_player_lines` : aucun `over_36` en ligue | partiel (2026-10-18) : les 7 joueurs cités sont à 24 min ou moins en J18, mais Legrand est à 48 min (`over_36`) | trop tôt (1 match ; la rotation à 24 min date de J15, avant le conseil) |
| C-002 | 2026-10-16 | Entraînement : Gimenez secondaire → trois points ; Bernard secondaire → athlétisme — agent Effectif, action 2 | `silver.bv_player_weekly` : `training_secondary` | **appliqué** (vérifié le 2026-10-18 sur le relevé du 18/10 : Gimenez = three_point, Bernard = athleticism) | 1er entraînement mesuré (18/10, `gold.bv_training_gains_exact`) : Gimenez trois points +0,411, Bernard athlétisme +1,100, conformes au gain attendu (ratio 0,50) — agent Entraînement |
| C-003 | 2026-10-16 | Mettre Nael Fontaine en vente — agent Effectif, action 3 | Fontaine absent de l'effectif ou en vente | appliqué (2026-10-18) : `silver.bv_players.on_transfer_list` = true | sans objet (pas un facteur de match) |
| C-004 | 2026-10-18 | Focus Intense sur le vrai scoreur adverse ; light et give_up seulement sur les joueurs peu utilisés [M§6.6] — agent Match | `gold.bv_match_opp_focus` (ligue) : le joueur au plus fort `shot_share` a `our_focus` in ('intense','lock') ; aucun `give_up` sur un adverse à 30 min ou plus | ouvert | — |
| C-005 | 2026-10-18 | Revenir à `defense_tier` = 2 en ligue, (confirmé le 2026-10-18 : écran 1 = Soft, 3 = Équilibrée) [M§6.3] — agent Match | `gold.bv_match_player_lines` : `defense_tier` = 2 pour tous les joueurs de ligue avec `min` > 0 ; effet sur `opp_efg_pct` (base J15–J18 : 46,0) | ouvert | — |
| C-006 | 2026-10-18 | Remettre Lefebvre dans une unité dès que sa forme atteint 5 ou plus ; Legrand dans une seule unité [M§5.5, §5.7] — agent Match | Ligue : Lefebvre `min` > 0 quand `gold.bv_player_outlook.form` ≥ 5 ; Legrand `over_36` = false | ouvert | — |
| C-007 | 2026-10-18 | Ligue J19–J22 : garder 2 unités de 24 min (A en Q1/Q3/OT, B en Q2/Q4), Lefebvre dans l'unité A même en forme 1 (`fit_with_form` 55,8 au PF contre 48,0 pour Legrand) [M§5.7] — agent Tactique, brief `2026-10-18-tactique.md` | `gold.bv_match_player_lines` (league, `round_number` 19–22) : `over_36` = false pour tous ; `min` ≤ 30 pour tous ; Lefebvre `min` > 0 | ouvert | — |
| C-008 | 2026-10-18 | J19 BARIUM : focus Intense sur Calabrese (28,3 % des tirs à l'aller), Light sur les joueurs peu utilisés, aucun Give up [M§6.6] — agent Tactique | `gold.bv_match_opp_focus` (`round_number` = 19) : `our_focus` = 'intense' pour Egidio Calabrese ; aucune ligne `our_focus` = 'give_up' | ouvert | — |
| C-009 | 2026-10-18 | Amicaux du 19 au 27/10 : 36 min pour chaque jeune (Baron, Leclerc, Lecomte, Bernard, Boyer) [M§5.4] — agent Tactique | `gold.bv_match_player_lines` (friendly, `match_day` entre 2026-10-19 et 2026-10-27) : `min` ≥ 30 pour ces 5 joueurs à chaque match | ouvert | — |
| C-010 | 2026-10-18 | Test v4 de l'agressivité en amical : cran 4 le 20/10 (et le 22/10 si un amical est programmé), cran 2 les autres jours ; décider du réglage de la saison 2 [News 2026-10-11/17, M§6.3] — agent Tactique | `gold.bv_match_report` + `gold.bv_match_player_lines` (friendly, depuis le 2026-10-19) : moyenne de `opp_ft_rate`, `opp_efg_pct` et `pf` par `defense_tier` majoritaire, au moins 2 matchs par cran | ouvert | — |
| C-011 | 2026-10-18 | Entraînement du 25/10 (dernier de S1) : **garder tous les choix**, aucun changement (aucune compétence entraînée ≥ 70, gains conformes au potentiel, pas d'endurance : +1 pt = −0,7 % de fatigue seulement [M§5.6, §8.4]) — agent Entraînement, brief `2026-10-18-entrainement.md` | `silver.bv_player_weekly` (relevé du 2026-10-25) : `training_primary` / `training_secondary` identiques à la fiche de saisie du brief pour les 14 joueurs de moins de 30 ans | ouvert | — |
| C-012 | 2026-10-18 | Acheter Waleed Al-Anazi (SG, 24 ans, libre), maximum 100 000 (110 000 au plus), SG de l'unité B à la place d'Henry (fit 48,7 contre 42,0) [M§11.3, §11.4] — agent Transferts, brief `2026-10-18-transferts.md` | Al-Anazi présent dans `gold.bv_roster_now` après le 19/10 00:08 | ouvert | — |
| C-013 | 2026-10-18 | Min-jun Dang (SG, 29 ans, libre) : si Al-Anazi est gagné, baisser le maximum au prix actuel ; sinon monter à 90 000 — agent Transferts | Au plus un des deux (Al-Anazi, Dang) acheté à plus de 15 000 ; présence dans `gold.bv_roster_now` après le 19/10 21:16 | ouvert | — |
| C-014 | 2026-10-18 | Acheter Anselmo Albano (PF, 26 ans, 205 cm, fit PF 47,1), maximum 60 000, comme 2e intérieur remplaçant derrière Bernard (plan B du brief tactique) ; Duarte Ferreira (max 30 000) seulement s'il est perdu — agent Transferts | Albano (ou Ferreira) présent dans `gold.bv_roster_now` après le 20/10 00:44 | ouvert | — |
| C-015 | 2026-10-18 | Jaylen Daniels (PG, 28 ans) : garder l'enchère mais baisser le maximum de ~100 000 à 60 000 (gain de fit +2,5 seulement sur Boyer) — agent Transferts | Daniels présent dans `gold.bv_roster_now` après le 20/10 14:12 à un prix ≤ 60 000 (`silver.bv_transfers`), ou absent | ouvert | — |
| C-016 | 2026-10-18 | Ventes : Fontaine seulement d'ici la fin de saison (C-003) ; Henry et Klein en vente **après le 26/10** si les recrues sont arrivées ; garder les jeunes (Bernard, Baron, Leclerc) — agent Transferts | `gold.bv_sell_candidates.on_transfer_list` : false pour tous sauf Fontaine jusqu'au 26/10 ; Henry / Klein `on_transfer_list` = true ou absents de `gold.bv_roster_now` début saison 2 | ouvert | — |
| C-017 | 2026-10-18 | Renvoyer les 2 spécialistes marketing le 18/10 (avant J20 au plus tard) : plus que 2 matchs à domicile, gain ≤ 8 000 contre 25 000 de coût ; popularité remise à 70 % en S2 [M§4.3, §10.1.1] — agent Finances, brief `2026-10-18-finances.md` | `gold.bv_personnel_status` (relevé suivant) : marketing `hired` = 0 ; `silver.bv_finance_transactions` du 25/10 : `medical_staff_weekly` sans la part marketing | appliqué (2026-10-18 : 2 marketing renvoyés, dit par l'utilisateur) | — |
| C-018 | 2026-10-18 | Embaucher 3 kinés (4/4) avant J19 (lun. 19/10 19:45) pour les 4 matchs du maintien : +15 000, risque de blessure −50 % [M§4.3, §9.3] — agent Finances | `gold.bv_personnel_status` : kinésithérapeute `hired` = 4 au relevé du 19/10 ou après ; nombre de sorties sur blessure en J19–J22 | appliqué (2026-10-18 : 3 kinés embauchés, dit par l'utilisateur) | — |
| C-019 | 2026-10-18 | Psychologues : garder les 2 jusqu'au tirage de forme du 25/10 (forme de J22), puis renvoyer le 26/10 (forme remise à 6 en S2) ; médecins : garder les 2 jusqu'au 26/10 [M§4.3, §5.5] — agent Finances | `gold.bv_personnel_status` : psychologue `hired` = 2 au 25/10 puis 0 au 1er relevé de S2 ; médecin `hired` = 2 jusqu'au 26/10 | ouvert | — |
| C-020 | 2026-10-18 | Enchères : plafond total de 160 000 de prix d'achat (Al-Anazi + Albano) ; ne pas cumuler les 4 recrues (−90 000 sous la réserve de 2 semaines de charges) [M§10.3] — agent Finances | `silver.bv_transfers` : somme des prix d'achat du 19 au 20/10 ≤ 160 000 ; `gold.bv_finance_health.balance` ≥ 925 000 après le 26/10 | ouvert | — |
| C-021 | 2026-10-18 | Homegrown à 0 depuis J15 : arbitrage à trancher par l'agent Tactique. Bernard au C de l'unité B à la place de Klein (−0,8 de `fit_with_form`) = +14 400 par semaine, ≈ 115 000 en S2 [M§10.1.3] ; garder l'académie à 100 000 tant qu'un amical à domicile est joué chaque jour, sinon la baisser à 50 000 en premier [M§4.2] — agent Finances | `silver.bv_finance_transactions` : `sponsor_homegrown_bonus` le 25/10 (0 ou > 0) ; `gold.bv_finance_health.weekly_academy` ; nombre d'amicaux à domicile par semaine dans `silver.bv_matches` | tranché (2026-10-18) : Bernard au C de l'unité B dans le preset ligue, Klein sur le banc | — |
| C-022 | 2026-10-18 | Rapport du 15/10 (jauge 45 %, P(High) 7,4 %) : ignorer Gay, Brun et Bourgeois, ni test ni signature (PS estimé 30–34 contre 41–46 pour nos juniors ; fin de saison) [M§4.2] — agent Académie, brief `2026-10-18-academie.md` | `silver.bv_finance_transactions` : aucun `academy_scout_tests` entre le 2026-10-15 et le 2026-10-22 09:00 ; aucun nouveau junior dans `gold.bv_roster_now` avant le 22/10 | ouvert | — |
| C-023 | 2026-10-18 | Académie : garder 100 000 par semaine (90 % projeté au rapport du 19/11) ; 50 000 seulement si les amicaux quotidiens ne sont pas tenus (C-021) [M§4.2] — agent Académie | `silver.bv_academy_weekly` : `weekly_investment` = 100 000 ; `academy_score` ≈ 58 (±2) au rapport du 22/10 (contrôle de l'hypothèse de `sql/gold/010_bv_academy.sql`) | ouvert | — |
| C-024 | 2026-10-18 | Signatures : rapport du 22/10 ignoré sauf prospect à PS estimé ≥ 40 (alors 1 test) ; première signature visée au rapport du 19/11 (≥ 90 %), uniquement un prospect testé High [M§4.2] — agent Académie | Nouveau junior dans `gold.bv_roster_now` : pas avant le 19/11 sauf test High (`academy_scout_tests` la même semaine) ; `silver.bv_academy_weekly.academy_score` ≥ 90 au rapport de la signature | ouvert | — |

## Journal des matchs
<!-- date · compétition · adversaire · score · résultat · cause principale (1 ligne) -->
- 2026-09-07 · ligue J1 · KK Uola (dom) · 74-114 · D · eFG 36,7–56,5 (15,8 % à 3 pts) ; Q2 −19
- 2026-09-09 · ligue J2 · Mind Readers (ext) · 93-115 · D · OREB 18,4–36,7 ; Q4 −15
- 2026-09-12 · ligue J3 · Águias do Guadiana (dom) · 71-101 · D · eFG 27,6–54,6 (24,5 % à 2 pts) ; Q2 −20
- 2026-09-14 · ligue J4 · Thrylos (ext) · 97-89 · V · 3 pts adverse à 19,5 % ; Q1 +11
- 2026-09-16 · ligue J5 · Póvoa Riptide (dom) · 74-103 · D · TOV 21,8–11,0 ; Q1 −14
- 2026-09-19 · ligue J6 · San Pancrazio (ext) · 112-78 · V · eFG adverse 32,3, OREB 33,3–19,6
- 2026-09-21 · ligue J7 · Sierra Nevada (ext) · 103-82 · V · TOV adverse 21,9, 57,1 % à 2 pts
- 2026-09-23 · ligue J8 · BARIUM (dom) · 91-95 · D · eFG 38,3 et TOV 18,7 ; mené tout le Q4
- 2026-09-26 · ligue J9 · Žirmūnai (ext) · 96-129 · D · eFG adverse 57,3, OREB adverse 37,0
- 2026-09-28 · ligue J10 · Astur Hoops (dom) · 114-105 · V · eFG 58,0, OREB 35,0
- 2026-09-30 · ligue J11 · Wolves Empire (ext) · 108-111 · D · Cecchetti 38 pts à 71 % ; perte de balle dans la dernière minute
- 2026-10-03 · ligue J12 · KK Uola (ext) · 76-135 · D · eFG adverse 68,0 ; écart de niveau
- 2026-10-05 · ligue J13 · Mind Readers (dom) · 88-111 · D · eFG 33,0, OREB adverse 36,5
- 2026-10-07 · ligue J14 · Águias do Guadiana (ext) · 89-119 · D · eFG adverse 57,1 ; Q2 −23
- 2026-10-10 · amical · Isotopi&aAllies · 131-79 · V · eFG 61,0–38,3
- 2026-10-10 · ligue J15 · Thrylos (dom) · 115-71 · V · eFG 59,1, TOV adverse 30,1 ; 1er match en rotation de 24 min, `defense_tier` 0
- 2026-10-11 · amical · Tenerife · 105-100 · V · FT rate 49,4–13,1, OREB 32,7
- 2026-10-12 · amical · Lila Sólymok · 109-120 · D · eFG 50,5–55,8 ; Q3 −11
- 2026-10-12 · ligue J16 · Póvoa Riptide (ext) · 107-110 · D · TOV 24,2 ; égalité à 0:30 puis perte de balle
- 2026-10-13 · amical · Halifax Wolves · 92-103 · D · box score adverse absent (export à refaire) ; 20 % à 3 pts
- 2026-10-14 · ligue J17 · San Pancrazio (dom) · 100-85 · V · eFG 50,6–41,0, FT rate 39,7–9,6 ; Q4 +15
- 2026-10-15 · amical · veldeman · 106-98 · V · Q1 −15 puis Q3/Q4 +24
- 2026-10-16 · amical · Ironwood Holdings · 112-128 · D · eFG adverse 60,1 ; Q1 −18
- 2026-10-17 · amical · Gremeska Achilles · 107-97 · V · eFG 55,4–45,5 ; Q4 +16
- 2026-10-17 · ligue J18 · Sierra Nevada (dom) · 109-83 · V · TOV 6,0–25,0 ; Hola (give_up) 36 pts ; Lefebvre 0 min
- 2026-10-18 · amical · Arios Pagkos · 138-95 · V · eFG 67,4 ; Lefebvre 40 d'éval

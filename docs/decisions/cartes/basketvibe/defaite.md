# Carte basketvibe — defaite (analyse d'une défaite)

Sources lues : commit 3de9137 (2026-10-31)

Écrite le 2026-10-31 (skills tactique et joueurs, learnings L-001 à L-026, vues gold). Exigences : CLAUDE.md règle 4 (« défaite = analyse détaillée »), règle 19 (toute la saison), A-2.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:50 | selon tous les matchs, le manque de réussite | var. 3-5 |
| :166 | apprendre de ses erreurs | var. 9, § Checks appris |
| :169 | beaucoup de défaites : agir | Rendu tableau 3 |

## Rendu (figé)
1. Une ligne : score via `my_result` (jamais le score brut), écart, quarts (`quarter_margins`).
2. **Causes chiffrées** : `| Facteur | Ce match | Moy. défaites | Moy. victoires | Verdict |` — eFG, eFG adverse, OREB %, OREB adverse %, pertes %, pertes adverses %, FT rate et FT rate adverse, part et réussite à 3 pts, fautes.
3. **Joueur par joueur** (ordre PG→C) : `| Joueur | Min | >36 | Pts | Tirs (3 pts) | Pertes | Fautes | Éval | Consignes jouées |`.
4. **Comparaison** aux défaites précédentes de la saison (même facteur dominant ?).
5. **3 à 5 corrections** : `| Priorité | Correction | Joueur / réglage | Valeur | Match qui teste | Ce qui prouvera l'erreur |`.
Puis la ligne C-nnn → L-nnn à écrire dans `learnings.md`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat, quarts | `select fixture_id, competition, opponent, my_result, my_pts, opp_pts, margin, quarter_margins from gold.bv_match_report order by match_day desc limit 1` | Résultat = `my_result` | CLAUDE.md règle 7 | |
| 2 | Facteurs du match | `gold.bv_match_report` (efg_pct … opp_fg3a_share) | — | — | |
| 3 | Moyennes V/D de la saison | `select * from gold.bv_match_factors_by_result where competition = '<comp>'` | Comparer par compétition (amical ≠ ligue) ; v3 (ligue ≤ 26/10) ≠ v4 | `resume.md` § Rythme | |
| 4 | Joueur par joueur | `select name, position, min, over_36, pts, fga, fg3a, fg3m, tov, pf, fouled_out, eval, role_tier, shot_tier, defense_tier from gold.bv_match_player_lines where fixture_id = <id> order by min desc` | > 36 min = −20 % ; 6 fautes ; tir à 3 sans réussite | [M§5.7] ; L-020, L-025 | |
| 5 | Défaites précédentes | `select match_day, opponent, margin, efg_pct, opp_efg_pct, oreb_pct, opp_oreb_pct, tov_pct from gold.bv_match_report where my_result = 'L' and competition = '<comp>' order by match_day` | Même facteur deux fois = conseil réécrit | A-7 | |
| 6 | Focus défensif réel vs scoreurs | `select name, shot_share, pts, our_focus from gold.bv_match_opp_focus where fixture_id = <id> order by shot_share desc limit 6` | Scoreur à plus de 20 % des tirs non verrouillé = cause | L-006, L-014 | |
| 7 | Zone et réglages joués | `gold.bv_zone_jouee`, `gold.bv_saisie_joueurs` (sauvegarde du match) | Plan non sauvegardé = composition par défaut | L-011, L-024 | |
| 8 | Fatigue au coup d'envoi | `gold.bv_fatigue_plan` (relevé du jour du match) | v4 : > 20 = pénalité | skill joueurs § Fatigue | |
| 9 | Conseils C-nnn appliqués | `outputs/basketvibe/learnings.md` (lignes C du match) | Appliqué ? effet ? | A-7 | |
| 10 | Fin de match | `select period, clock, kind, detail from silver.bv_match_events where fixture_id = <id> and period >= 4 order by seq desc limit 40` | Fautes tactiques de l'équipe menée : pas un défaut de discipline | Dev 2026-09-08/09 (connaissance) ; L-005, L-016 | |
| 11 | Adversaire : minutes de ses titulaires | `silver.bv_match_player_stats where fixture_id = <id> and not is_mine and period = 0` | Adversaire à 5 × 48 min : il faiblit au Q4 | L-019, L-023 | |
| 12 | Avis des amis | connaissance § Tactique / moteur | « défaite à 68 % de victoire = normale » (aléa) | Dev 2026-08-24 | |

## Checks appris des matchs
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-001 / L-016 | eFG et OREB d'abord ; OREB ≤ −13,9 = défaite lourde | 2026-10-31 | |
| L-013 | Défaite aux rebonds : cinq plus grand aux emplacements PF/C | 2026-10-31 | |
| L-015 | Lancers : FT rate adverse élevé avec l'agressivité | 2026-10-31 | |
| L-020 / L-025 | Défaite par l'attaque à 3 pts : tir des joueurs fautifs | 2026-10-31 | |
| L-005 | Matchs serrés perdus sur une perte de balle | 2026-10-31 | |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
| 2026-10-31 | Fautes | LF adverses élevés = cran d'agressivité → idem, et ne pas imputer au moteur v4 (fautes v3 ≈ v4) | mesure du Dev 2026-10-28 |
| 2026-10-31 | Fautes tactiques | présent → inchangé | connaissance : fin de match serré (Dev 2026-09-08/09) |
| 2026-10-31 | Agressivité | LF adverses élevés = regarder le cran d'agressivité de chaque défenseur | avis #portugal 2026-08/10 : 8/10 en agressif → 43 LF contre 15 en soft (v3) |

# Carte basketvibe — academie (rapport du jeudi, test, signature, investissement)

Sources lues : commit 58975fe (2026-10-31)

Écrite le 2026-10-31 (skill `basketvibe-academie`, vues gold d'académie). Rapport : jeudi 09:00 ; investissement à sauvegarder avant.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:10 | comprendre l'académie | skill (cycle, jauge, −50 %) |
| :11 | faut-il scouter (tester) | var. 4-6 |
| :12 | intégrable au club | var. 7-9 |
| :13 | combien on dépense | var. 2 |

## Rendu (figé)
1. `| Prospect | Poste | Âge | Taille | TSP min–max | Compétences clés du poste (fourchettes) | P(High) | Verdict (tester / signer / ignorer) |`, les 3 du rapport.
2. Jauge et investissement : `| Jauge | Investissement/sem. | Projection | Décision |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Jauge et prochain rapport | `select week, academy_score, weekly_investment, next_scout_report from silver.bv_academy_weekly order by week desc limit 1` | 0 investi = −5/sem ; 100 000 maintient 100 % ; 50 000 plafonne vers 89 % | [M§4.2] | |
| 2 | Coût | `gold.bv_finance_health.weekly_academy` | Comparer au gain attendu (potentiel, homegrown) | skill économie § Homegrown | |
| 3 | Prospects | `select slot, name, position, age, height_cm, tsp_min, tsp_max, ps_mid, two_point_min, two_point_max, three_point_min, three_point_max, defense_min, defense_max, rebounding_min, rebounding_max, athleticism_min, athleticism_max from gold.bv_academy_prospects order by scout_report_at desc, slot limit 3` | Fourchette de ~20 points qui contient la vraie valeur | [M§4.2] ; Obs 2026-10-16 | |
| 4 | Probabilités de potentiel | `select label, academy_score, p_low_1_3, p_decent_4_7, p_high_8_10, expected_potential from gold.bv_academy_potential_odds` | Test (25 000) utile si P(High) change la décision | [M§4.2] | |
| 5 | Résultat d'un test | export du rapport testé | Fourchette de 10 points + Low / Decent / High | [M§4.2] | |
| 6 | Argent du test | `gold.bv_finance_health.balance` | Solde positif après 25 000 | [M§4.2] | |
| 7 | Besoin par poste | `select position, depth, ps_avg, best, weakest, age_avg from gold.bv_position_summary` | Poste à faible profondeur = priorité | — | |
| 8 | Taille pour le poste | `height_cm` ; croissance jusqu'à 22 ans (+0 à +4 cm par saison) | Taille cible du poste adulte | [M§5.2] | |
| 9 | Signer = jauge divisée par 2 | `gold.bv_academy_gauge_projection` | Remonter de 50 à 100 % : 5-6 semaines à 100 000 | [M§4.2] | |
| 10 | Revente possible | `gold.bv_market_price_ref` (16-17 ans) | Juniors de l'académie revendables sans délai d'une semaine | [M§11.1] | |
| 11 | Comparaison aux autres clubs | — | Il manque la jauge des autres clubs — cherché dans : bronze, silver, connaissance, Discord — on la réunit en notant les juniors signés vus sur le marché (16-17 ans) | A-8 | |
| 12 | Avis des amis | connaissance § Académie (29/10 : avis opposés sur un junior à 100 %) | Avis seulement ; la décision suit le skill | connaissance | |
| 13 | Postes des 3 candidats | `silver.bv_academy_candidates` | Ne pas déduire le poste d'un candidat de celui des autres | V-20261030-5 (hypothèse, un cas contraire) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

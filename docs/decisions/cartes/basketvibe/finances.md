# Carte basketvibe — finances (argent, sponsor, personnel)

Sources lues : commit 0000000 (2026-10-31)

Écrite le 2026-10-31 (skill `basketvibe-economie`, vues gold de finances). Règles : A-3 (dire quoi faire de l'argent), A-8 (retard mesuré contre les autres clubs), CLAUDE.md « capacité moins dépenses décidées ».

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:16-19 | solde, dépenses, salaires, entrées | var. 1-4 |
| :20 | acheter joueur ? personnel ? rien ? | var. 8-10, 12 |
| :21 | quoi faire dans le futur | var. 6 |
| :22 | sponsors | var. 11 |
| :53-54 | personnel | var. 12 |
| :168 | beaucoup d'argent | var. 8-10 |

## Rendu (figé)
1. `| Poste | Par semaine | Saison à date | Source |` : solde, recettes (sponsor, billetterie, amicaux, homegrown), dépenses (salaires, personnel, académie), résultat.
2. Décision : `| Priorité | Catégorie | Action | Montant | Reste après |`, une décision par usage de l'argent (achat, personnel, académie, réserve), avec ce qui prouvera l'erreur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Solde, popularité | `select as_of, balance, popularity from gold.bv_finance_health` | Solde à zéro = plus d'enchère | [M§10.3] | |
| 2 | Recettes de la semaine | `select sponsor_weekly, ticket_home, tickets_per_week, ticket_friendly, friendlies_per_week, homegrown_last_week, recurring_income_week from gold.bv_finance_health` | Billet 50 × 8 000 × popularité ; amical ~6 % d'un match de ligue | [M§10.1.1] | |
| 3 | Dépenses de la semaine | `select weekly_salaries, weekly_personnel, weekly_academy, weekly_fixed_costs, weekly_result_est from gold.bv_finance_health` | Salaires et personnel le dimanche, académie le jeudi | [M§10, §1.3] | |
| 4 | Résultats par semaine | `select week, income, expenses, result, complete from gold.bv_finance_weekly_result order by week desc limit 4` | Seules les semaines `complete` comptent | skill économie § Lecture | |
| 5 | Saison à date | `select * from gold.bv_finance_season_rates` | — | — | |
| 6 | Projection saison 2 | `select balance_end_s1, reward_if_rank_kept, current_rank, s2_result, safety_reserve, investable_now_end_s1 from gold.bv_finance_s2_projection` | Ne compte ni coupes, ni transferts, ni primes (projection) | skill économie § Lecture | |
| 7 | Prime de classement | `silver.bv_standings_weekly` (rang, `is_mine`) | 1er 400 000 · 2e 300 000 · 3e 200 000 · 4e 100 000 · 5-8e 50 000 | [M§10.1.4] | |
| 8 | Capacité d'investissement | `investable_now_end_s1` et `gold.bv_finance_health.transfer_available − transfer_committed`, moins les dépenses décidées de `outputs/basketvibe/fait-*.md` | Aucune dépense au-delà ; réserve de sécurité gardée | CLAUDE.md § Horizon | |
| 9 | Alternative : achat | carte `achat` var. 1 | Le gain sportif par euro le plus haut gagne | A-3 | |
| 10 | Alternative : académie | carte `academie` var. 1-4 | idem | A-3 | |
| 11 | Sponsor | `select week, phase, choice_pending, brand, variant, weekly_base, win_bonus, offers from silver.bv_sponsor_weekly order by week desc limit 1` | Choix une fois par saison, avant 15 min avant la 1re journée, sinon Stability ; un contrat à primes vaut le coup si le nombre de victoires attendu dépasse le seuil (Fluxora : 11 victoires sur 22 = 805k contre 800k) | [M§10.1.2] ; utilisateur 2026-10-27 ; `fait-2026-10-27.md` | Fluxora Balance choisi (2026-10-27) ; base encore `choosing` au 26/10 |
| 12 | Personnel | `select role, hired, slots, unit_cost, weekly_cost, current_effect from gold.bv_personnel_status order by week desc limit 4` | Médecin −25 % de durée (10 000) ; kiné −12,5 % de risque (5 000) ; psychologue +5 pts de forme (10 000) ; marketing −1 pt de perte de popularité (12 500) ; on paie le maximum employé dans la semaine | [M§4.3] | Piège : médical 85 000 au journal contre 60 000 affichés (25/10) |
| 13 | Comparaison aux autres clubs | `silver.bv_standings_weekly.club_strength` | Retard mesuré contre la ligue | A-8 | |
| 14 | Avis des amis | connaissance § Finances / transferts / personnel | Popularité remise à 70 seulement sous 70 : en doute | connaissance V-20261030-7 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

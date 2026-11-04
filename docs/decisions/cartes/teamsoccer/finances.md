# Carte teamsoccer — finances (solde, stade, entraîneur ; deux clubs, deux économies)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `finances.md`, skills `teamsoccer-club`, `-entrainement` § Entraîneurs, `-saison` § Primes ; connaissance § 2, § 5). Plus d'agent `finances` depuis le 2026-11-02 : je lis ces vues moi-même. Pas de sponsor ni de personnel dans ce jeu (sauf l'entraîneur) ; prix des billets fixes.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:120 | solde actuel | var. 1 |
| :121 | dépenses | var. 2 |
| :122 | salaires | var. 2 |
| :123 | entrées d'argent | var. 3 |
| :124 | acheter ? infrastructure ? rien ? | var. 5-7 |
| :125 | quoi faire dans le futur | var. 4 |
| :126 | sponsors | var. 10 |
| :156 | à quoi sert chaque personnel | var. 10 |
| :157 | niveau de l'entraîneur | var. 6 |
| :168 | beaucoup d'argent | var. 5-7 |

## Rendu (figé)
Un bloc par club : 1) `| Solde | Semaine nette | Salaires | Entretien (écart) | Billetterie / match | Capacité d'investissement | Fin de saison projetée |` ; 2) Stade : `| Type de place | Places | Prix | Net / place / match | Matchs pour rembourser | Places finançables |` ; 3) une décision unique : places, entraîneur, achat de joueur ou garder, avec le chiffre qui la justifie.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Solde | `select team, as_of, balance, week_net, wage_bill, stadium_maintenance, maintenance_gap, attendance_rate, gate_per_home_match, home_league_left, projected_season_end, alert_negative from gold.ts_finance_status` | Négatif = ni achat, ni agrandissement, ni entraîneur ; moral en baisse | connaissance 2.7 | |
| 2 | Dépenses | même vue + `silver.ts_finances` | Entretien = 6 % de la recette à guichets fermés, lundi 00:05 ; `maintenance_gap` = 0 sinon bug (déjà vu 13/10, 19/10) | fiche finances § 3 ; connaissance 2.5, 7.3 | |
| 3 | Recettes | `gate_per_home_match` ; primes : skill saison | Affluence D1 : 1er 100 %, 2e 90 %… 8e 60 % ; coupes et amicaux 50/50 ; primes de ligue D1 800 / 500 / 250 k | connaissance 2.2, 5.1 | |
| 4 | Projection | `projected_season_end` | Approximation : ni primes, ni coupes, ni ventes, ni amicaux | fiche finances § Données | |
| 5 | Capacité d'investissement | `select team, balance, reserve_2_weeks, decided_not_settled, decided_list, capacite_invest, finances_age_days from gold.ts_capacite_invest` | Solde − 2 semaines de salaires et d'entretien − dépenses décidées non relevées (`silver.ts_depenses_decidees`) | règle apprise 16 | |
| 6 | Entraîneur | skill entraînement § Entraîneurs | Niveau 2 = 1 M$, puis 4, 10, 25 M ; un niveau à la fois | connaissance 4.10 | niveau 1 (deux clubs) |
| 7 | Stade | `select team, seat_type, seats, room_left, price, net_per_seat_per_home_match, home_matches_to_repay, seats_affordable, cost_affordable, rank_payback from gold.ts_stade_choix order by team, rank_payback limit 8` | Comparer les 4 types dans un tableau ; acheter si ≤ 14 matchs pour rembourser ; jamais « tout d'un seul type » sans comparaison | fiche finances § Méthode ; consigne finances du 2026-10-27 | basique le meilleur (deux clubs) |
| 8 | Remplissage | `select my_team, match_date_paris, spectators, fill_pct from gold.ts_match_report where venue = 'domicile' order by match_date_paris desc limit 6` | Le taux suit division × rang ; places vides = places × (1 − taux) | fiche finances § Méthode 2 | |
| 9 | Relevé stade | `silver.ts_stadiums` (date) | Relevé du 19/10 : l'achat de places du 27/10 (Cows) est dans `silver.ts_depenses_decidees` | `resume.md` § Pièges | |
| 10 | Sponsor, personnel | — | Pas de sponsor, pas de personnel (hors entraîneur) dans ce jeu | connaissance 2.8 ; fiche finances | |
| 11 | Alternative | carte `achat` var. 1 | Même somme : places, entraîneur ou joueur ; choisir le gain chiffré le plus haut | CLAUDE.md règle 5 | |
| 12 | Écarts non expliqués | `silver.ts_finances` | Ben Ahmed 27/10 : 506 299 $ inexpliqués ; 22/10 : `match_income` +8 375 $ | `resume.md` § Pièges ; fiche finances | |
| 13 | Avis des amis | connaissance § 2, § 5 | Fan club sans lien avec l'affluence ; Idole = affluence ×1,5 | connaissance 2.3, 2.6 | |

## Valeurs et lieux ajoutés par la police (2026-11-04)
| Variable | Où / valeur du jour |
|---|---|
| 2 Dépenses | `weekly_expenses` d'une ligne `silver.ts_finances` = **semaine close** (lignes de la semaine précédente : stadium_building + wages + maintenance) ; wages et maintenance de la ligne = semaine nouvelle. Cows 3 554 021 = 3 369 250 + 155 851 + 28 920 ; `other_expenses` = 0. Entretien attendu = (recette plein stade des places d'avant l'achat) × 6 % : Cows 47 475 le 02/11, pas un bug |
| 3 Recettes | 7 matchs de ligue à domicile par saison (14 journées) ; `gold.ts_season_calendar.home_league_left` = reste ; remplissage Cows 85–90 %, Donkey 80 % |
| 5 Capacité | Cows 459 647, Donkey 251 434 (registre : ligne 4 soldée le 04/11, le solde 873 653 la contient déjà). Règle : une dépense décidée est soldée dès que la ligne `stadium_building` de l'export Finances la montre |
| 6 Entraîneur | `core.staff` : niveau 20 (= niveau 1) les deux clubs, relevé 2026-10-30 |
| HPC | `bronze.raw_pages` page_type `dashboard_high-performance` (HTML, texte) plus récent que `silver.ts_hpc` : 04/11 = relevé du 30/10, 50 TSC, 0 accumulé, 5 semaines ; sous 50 TSC aucun remboursement |
| Limite d'achat | 1 par semaine, lundi 00:00 ; `new_signings` ; « Mes enchères » (export) pour les enchères en cours |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

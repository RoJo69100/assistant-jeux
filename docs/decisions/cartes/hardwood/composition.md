# Carte hardwood — composition (Depth Chart, Game Tactics, Game Management)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `hardwood-tactique`, `-regles` ; veille `v-tactique.md`, `v-joueurs-entrainement.md` § 2-3 ; learnings). Règles : saisie dans l'ordre de l'écran (depth chart poste par poste, puis Game Tactics, puis Game Management joueur par joueur) ; rendu tactique [U] `| Réglage | Actuel | À mettre |` ; exhibition = compo de test, conférence et tournois = Game Plan de référence ; walk-ons jamais proposés [U] ; horizon aujourd'hui.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:6 | coupe / amical / ligue : paramètres | var. 1 |
| :30 | quelles tactiques | var. 4-8 |
| :31 | composition par poste | var. 2, 3 |
| :32 | Game Tactics | var. 4-9 |
| :33 | Game Management | var. 10 |
| :34 | stratégie selon nos matchs contre cet adversaire | var. 11 |
| :35 | stratégie selon toute la saison, manque de réussite | var. 12 |

## Rendu (figé)
1. Depth Chart : `select depth, pos, propose, note, mastery, actuel, controle from gold.hw_depth_suggest order by pos, depth` → `| Poste | Titulaire | 2e | 3e | Contrôle |` dans l'ordre PG, SG, SF, PF, C.
2. Game Tactics : `| Réglage | Actuel | À mettre |` dans l'ordre Pace, Inside/Outside Emphasis, Zone %, Pressure %, Extend (Man % = reste), Substitution Mode, ajustement de mi-temps.
3. Game Management : `| Joueur | Green Light | Offensive Positioning | Playing Time | Foul Trouble Hook | Red Shirt |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Type de match | `select jour, prochain_type, prochain_adversaire, prochain_paris, bilan, bilan_conf from gold.hw_today` | Exhibition = test (ne compte ni au classement ni au redshirt) ; conférence = classement ; même Game Plan en tournoi | `resume.md` § Saison | conférence depuis le 01/11 |
| 2 | Joueur au poste | `select name, pos, cles, score, mastery, height_ok from gold.hw_player_pos_scores order by pos, score desc limit 40` ; `gold.hw_player_fit` | Note = 0,6 × compétences clés + 0,4 × SI/14 [H] ; PG = IQ, Pass, Hnd, Spd ; SG = OS, Spd ; SF = OS, défense, Spd ; Grand = IS, Reb ; un lent ne joue qu'à C | fiche académie § Règles ; v-tactique § 3 | |
| 3 | Disponibles | `gold.hw_effectif` (`injury_days`, `red_shirt`, `walk_on`) | « +0 » = peut jouer ; redshirt (Wallace) et walk-ons jamais au depth chart ; ordre de remplissage PG, C, PF, SF, SG | `fait-2026-11-02.md` ; v-joueurs § 3 | Wallace RS |
| 4 | Pace | `silver.hw_tactics` | Pace et Foul Hook = principaux facteurs de fautes ; +2 de pace = −1 minute tolérable | v-tactique § 2 ; v-joueurs § 2 | 0 |
| 5 | Emphasis | idem | Très puissant (3 pts 0,31 → 0,45 en passant de `i` à `~`, avis) | v-tactique § 2 (en doute) | o |
| 6 | Défense Man / Zone / Pressure | idem | Mélanger man + zone + un peu de pression ; zone = une 3-2, réduit les fautes ; pression = plus de fautes, de fatigue et de blessures | v-tactique § 1-2 | Zone 65, Pressure 15 |
| 7 | Extend | idem | Négatif par défaut (les équipes prennent plus de 2 pts) ; rester entre −3 et +3 ; ajuster selon où l'adversaire marque | v-tactique § 2 | 0 |
| 8 | Substitution Mode | idem | Staggered A / B / C (minutes de repos par poste) ou Mass | skill tactique | Staggered C |
| 9 | Ajustement de mi-temps | idem | Un seul déclenché (le premier) selon l'écart à la mi-temps | v-tactique § 1 | |
| 10 | Game Management | `silver.hw_management` ; `gold.hw_effectif` (`max_minutes`, `green_light`, `off_positioning`, `foul_hook`) | Green Light peu fiable, positioning plus utile ; Playing Time titulaire ≥ 15, moyen 32 ; règle « stamina + 20 minutes », Light au plus ; Overwork (près de 40 min) dure jusqu'à la fin de saison | v-tactique § 2 ; v-joueurs § 2 | |
| 11 | Adversaire | `select match_no, game_date, game_type, adversaire, domicile, rang_conf_adv, bilan_vd, bilan_conf, pf, pa, streak, rpi, sos, nos_resultats_ecart from gold.hw_adversaires limit 3` | Tactique adverse invisible : la déduire du play-by-play et des stats (taux de 3, pace, pression) | v-tactique § 4 | |
| 12 | Toute la saison | `select phase, my_result, matchs, ecart, rim_pct, in_pct, mid_pct, three_pct, opp_three_pct, opp_rim_pct, opp_press from gold.hw_vd_compare` | Comparer V et D par zone de tir | `resume.md` § Ce que l'utilisateur attend | |
| 13 | Avis des amis | v-tactique § 2 | « Owner mode » : régler une fois et ne plus toucher (avis, n = 1) ; les bots s'adaptent | v-tactique § 2 (en doute) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-001 | Plan de référence (7 victoires déclarées) : le garder tant que les défaites ne s'expliquent pas par une zone précise | 2026-11-02 | à vérifier (C-001) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

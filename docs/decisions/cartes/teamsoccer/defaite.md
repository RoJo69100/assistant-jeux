# Carte teamsoccer — defaite (analyse d'une défaite ou d'un nul ; deux clubs)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `match.md`, skills `teamsoccer-match`, `-joueurs` ; connaissance § 6 ; learnings). Règles : CLAUDE.md règle 4 (analyse détaillée, joueur par joueur, toute la saison), règle 7 (résultat = notre côté : `gold.ts_match_report.result`), `analyste` d'office sur une défaite.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:153 | stratégie selon le manque de réussite récent | var. 3, 7 |
| :169 | beaucoup de défaites : agir | var. 10 |

## Rendu (figé)
Un bloc par club concerné :
1. `| Match | Compétition | Lieu | Score | Attaques | Tirs (cadrés) | Conversion % | Ballons perdus (inter. / contrôle / sortie) | Cartons | Note moy. |` : le match, puis la moyenne des V et des D de la saison (`gold.ts_vd_comparatif`).
2. `| Joueur | Poste | Note | Buts | Implications | Ballons perdus |`.
3. `| Cause | Chiffre | Comparaison saison | L-nnn |` (3 à 5).
4. `| Priorité | Catégorie | Correction (fais X) | Ce qui prouvera l'erreur | Match test |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat | `select my_team, match_date_paris, competition, venue, opponent, opp_is_bot, goals_for, goals_against, result from gold.ts_match_report order by match_date_paris desc limit 6` | Toujours `result` (notre côté), jamais le score brut | CLAUDE.md règle 7 | Cows 2-4 contre Potatos y Potitas (1re défaite, L-026) |
| 2 | Volume et cadrage | `my_attacks, opp_attacks, my_shots, opp_shots, my_on_target, opp_on_target, my_conversion_pct` | Comparer à `gold.ts_vd_comparatif` (V, N, D) | L-025, L-026 | |
| 3 | Ballons perdus | `my_lost, my_lost_intercept, my_lost_badcontrol, my_lost_outofbounds` ; actions : `gold.ts_match_plays` | Très variables selon l'adversaire, pas selon la composition (jusqu'à 88 %) ; sans conséquence contre un faible | L-004, L-012, L-014, L-018, L-022 | |
| 4 | Buts encaissés | `opp_on_target`, `my_gk_sector` | 2 buts sur 3 tirs cadrés adverses : gardien (Cows : gardiens faibles, meilleur OVR 60 au 19/10) | L-005 ; fiche effectif § Constat | |
| 5 | Joueur par joueur | `select player, positions, matches, avg_rating, last_rating, goals, involvements, balls_lost from gold.ts_player_match_ratings where team_id = <id> order by last_rating limit 15` | Note = force de l'emplacement (composition), pas la performance : lire les événements | fiche match ⚠️ | |
| 6 | Adversaire | `opp_avg_rating`, `opp_is_bot` ; `gold.ts_adversaires` | Humain fort (77,65 contre 63,7) : écart de niveau, pas un hasard | L-026 ; connaissance 6.3 | |
| 7 | Réussite | `my_posts`, `opp_gk_sector` | Conversion faible avec poteaux / gardien adverse = variance (1-0 contre bot, 17 %) | L-008, L-025 | |
| 8 | Nos réglages | `formation, play_style` ; `silver.ts_match_lineups` | Formation NULL = composition non captée : exporter la page du match | L-016, L-027 | |
| 9 | Forme et fatigue | `silver.ts_players.forme` du jour du match | Forme = plafond ; rendement baisse toutes les 5 min selon l'Endurance | connaissance 4.9 | |
| 10 | Série | `result` des 5 derniers matchs du club | Deux défaites d'affilée : `analyste` + `decideur`, jamais « ne rien changer » | CLAUDE.md usage des agents (4) | |
| 11 | Rang | `silver.ts_standings` (instantané) | Ne jamais citer un rang sans sa date | L-021 | |
| 12 | Conseils appliqués | `outputs/teamsoccer/learnings.md` § Conseils | Chaque C-nnn ouvert confronté ; deux échecs = réécrit | CLAUDE.md § Amélioration continue | |
| 13 | Avis des amis | connaissance § 6 | Clubs inactifs à 60 / Forme 100 battent parfois un favori ; moteur v3 : but = fin / (fin + gardien + 25), aléa ±5 % | connaissance 6.1, 6.4 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |
| L-004 | Ballons perdus élevés : interceptions d'abord | 2026-11-02 | à surveiller | hypothèse |
| L-005 | Peu de tirs adverses mais cadrés : gardien | 2026-11-02 | à surveiller | hypothèse |
| L-008 | Domination sans efficacité | 2026-11-02 | à surveiller | hypothèse |
| L-012 | Pertes selon l'adversaire, pas la composition | 2026-11-02 | confirmé | hypothèse |
| L-014 | Même XI, pertes 6 contre 18 | 2026-11-02 | confirmé (L-012) | hypothèse |
| L-018 | Pertes sans conséquence contre un faible | 2026-11-02 | à surveiller | hypothèse |
| L-021 | Rang daté | 2026-11-02 | règle | hypothèse |
| L-022 | Pertes jusqu'à 88 % | 2026-11-02 | à surveiller | hypothèse |
| L-025 | 1-0 contre bot, conversion 17 % | 2026-11-02 | à surveiller | hypothèse |
| L-026 | 1re défaite : humain fort à l'extérieur | 2026-11-02 | à surveiller | hypothèse |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

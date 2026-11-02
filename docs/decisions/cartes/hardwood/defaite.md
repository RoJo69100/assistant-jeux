# Carte hardwood — defaite (analyse d'une défaite)

Sources lues : commit 90f564f (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skills `hardwood-tactique`, `-regles` ; veille `v-tactique.md` § 3-4, `v-joueurs-entrainement.md` § 2-3). Règles : résultat = `my_result` ; analyse contre toute la saison (`gold.hw_vd_compare`) ; `analyste` d'office.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:35 | manque de réussite récent | var. 2, 3 |
| :19 | effet de la fatigue | var. 5 |

## Rendu (figé)
1. `| Match | Type | Lieu | Score | Écart | Rim % | Intérieur % | Mi-distance % | 3 pts % (tentés) | Adv. 3 pts % | Adv. rim % | Défense adverse (man / zone / press / extend) |`, puis moyennes V et D (`gold.hw_vd_compare`).
2. `| Joueur | Poste | Min | Pts | Reb | Ast | TOV | FG % | +/- | Fatigue |`.
3. `| Cause | Chiffre | Comparaison saison | L-nnn |` ; 4. `| Priorité | Catégorie | Correction (fais X) | Ce qui prouvera l'erreur | Match test |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat et tactique | `select game_day, game_type, opponent, is_home, my_result, my_margin, my_pace, my_emphasis, my_zone_pct, my_pressure_pct, my_extend, my_sub_mode from gold.hw_season_games order by game_day desc limit 8` | Toujours `my_result` | CLAUDE.md règle 7 | |
| 2 | Efficacité par zone | `rim_pct, in_pct, mid_pct, three_pct, opp_*` de `gold.hw_season_games` | Extend selon où l'adversaire marque ; Emphasis selon où nous réussissons | v-tactique § 2, § 4 | |
| 3 | Saison | `gold.hw_vd_compare` | `silver.hw_player_stats` ne compte que les matchs officiels | `resume.md` § Pièges | |
| 4 | Défense adverse mesurée | `opp_man, opp_zone, opp_press, opp_extend` | La défense adverse se resserre pendant la mi-temps selon ce qui marche | v-tactique § 3 | |
| 5 | Fatigue et Overwork | `silver.hw_game_box` (fatigue, minutes) | Light au plus ; Overwork = baisse jusqu'à la fin de saison ; fatigue = plus de blessures et de fautes | v-joueurs § 2-3 | |
| 6 | Joueurs | `silver.hw_game_box` ; `gold.hw_effectif` | Noms abrégés (« E. Corey ») : joindre par initiale + nom ; valeurs affichées ±20 % | `resume.md` § Pièges | |
| 7 | Force adverse | `ecart_wsi_adverse` ; `gold.hw_adversaires` (RPI, SOS) | Taille, envergure et hauteur pèsent beaucoup | v-tactique § 3 | |
| 8 | Série | `my_result` des 5 derniers | Deux défaites d'affilée : `analyste` + `decideur` | CLAUDE.md usage des agents (4) | |
| 9 | Conseils appliqués | `outputs/hardwood/learnings.md` § Conseils | Chaque C-nnn confronté | CLAUDE.md § Amélioration continue | C-001 (Wartburg) |
| 10 | Avis des amis | v-tactique § 2 | Erreurs fréquentes : tout-pression, Green Light à un joueur qui ne finit pas, oublier le Hook d'un grand en faute | v-tactique § 2 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

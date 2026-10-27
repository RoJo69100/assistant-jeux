# Team Soccer — lecteur d'exports, passage du 2026-10-27 (exports 19:55–20:28 UTC, forums exclus)

## 1. Inventaire
| Catégorie | Nombre | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Effectif (dashboard_squad, training) : Cows 22 (Forme), Ben Ahmed 22 | 14 + 11 | Oui (`ts_player_snapshots` day 2026-10-27, `gold.ts_squad_report`) | 0 blessé, 0 suspendu, 0 joueur à 2 jaunes |
| Matchs (dashboard_matches, league, team, match-viewer_id) | 12+22+23+27 | Oui (`ts_matches`, 3 nouveaux matchs). Match 1977456 : détail lu. Ajax et Ben Ahmed–BOT : pas de ligne `ts_match_report` d'événements | voir section 2 |
| Marché (dashboard_transfers) : 62 annonces (page Cows) + 11 (page Ben Ahmed), liste de 8 ids suivis | 10 | Oui (`ts_transfer_listings` vu à 20:28, `ts_my_bids` 8 ids) | ventes ouvertes, section 3 |
| Académie (youth-scout) | 18 | Oui (`gold.ts_academy` as_of 10-27) | Cows 0 révélation restante, Ben Ahmed 3 restantes |
| Finances / stade | 8 + 8 | Finances : oui (`gold.ts_finance_status` as_of 10-27). Stade : `ts_stadiums` encore au 10-19 | section 5 |
| HPC | 0 page | `gold.ts_hpc_status` as_of **2026-10-19** : aucun export HPC depuis | TSC 45/50 pour les deux clubs (vieux) |
| Annexes (classements, stats, visiteurs, login_streak, last_seen_*) | ~60 | Non (hors périmètre) | rien |

## 2. Matchs depuis le brief du 24 (résultat = côté de mon club, jamais le score brut)
| Club | Date Paris | Match | Résultat | Note |
|---|---|---|---|---|
| Cows | 26 10 02:00 | Ajax Amsterdam 4-0 Cows (ext., `is_admin_match`=true, pas amical) | DEFAITE 0-4 | silver `competition`=inconnu : c'est un match d'admin. Composition jamais enregistrée (brief du 25) |
| Ben Ahmed | 26 10 19:30 | BOT–Ben Ahmed (ext., ligue) | NUL 0-0 | 2 tirs contre 1, 3 remplacements, 1 jaune |
| Cows | 27 10 13:50 | BOT 0-1 Cows (ext., ligue) | VICTOIRE 1-0 | Pierre Bonnet 88', tirs 2-2 |

## 3. Marché (extrait du brut, silver à jour)
| Club | Annonce | Valeur |
|---|---|---|
| Cows | Etienne Roux FWD 19 ans, note 63, id 5396 (vente) | 1 093 175 $, 2 enchères, dernier enchérisseur équipe 401, fin 28 10 09:28 UTC |
| Ben Ahmed | Nanami Rousseau DEF 16 ans, note 38, id 5391 (vente) | 239 034 $, 0 enchère, fin 27 10 21:08 UTC (dans ~40 min après l'export) |
| Cows | 8 ids suivis : 391, 397, 440, 526, 660, 778, 872, 5343 | Omar Hassan (5343) n'est plus au marché (clos le 25 10) ; nature de la liste (suivi/enchères) non confirmée |
Nouvelles annonces d'intérêt : Farias DEF 17 ans note 56,2 (5447, 887 412 $, 1 enchère) ; le reste = jeunes de 14-16 ans.

## 4. Académie
Cows : 16 jeunes, 11 sans révélation, **0 révélation restante aujourd'hui**. Ben Ahmed : 18 jeunes, 13 sans révélation, **3 restantes** (reset 01:00 UTC).

## 5. Finances
| Club | Solde | Net semaine (lundi 26) | Entretien stade | Attendu 6 % | Écart |
|---|---|---|---|---|---|
| Cows | 2 328 978 $ | +2 499 859 | 28 920 | 482 000 x 6 % = 28 920 | 0 |
| Ben Ahmed | 505 349 $ | +623 772 | 20 024 | 333 725 x 6 % = 20 023,5 | 0 |
Formule 6 % confirmée, pas de bug de facturation ce lundi. Ventes cumulées : Cows 3 359 956 $ (+1 741 616 depuis le 23 10), Ben Ahmed 1 467 782 $ (+439 037). Solde Ben Ahmed 626 910 (25 10) -> 505 349 : baisse de 121 561 $ sans signature (`total_new_signings` 0) : inexpliquée, à surveiller. Projection fin de saison : Cows 2 955 552 $, Ben Ahmed 843 903 $. HPC : pas d'export (as_of 10-19).

## 6. Effectif (gold.ts_squad_report, 10-27)
Cows : Forme 72 pour 5 jeunes (Lefebvre, Jules Leroy, Thomas David, Thomas Roux, Enzo Roux), Adrien Roux MID 25 ans note 67 avec 1 jaune. Ben Ahmed : Forme 82 pour tous ; Adaeze Wilson FWD 1 jaune.

## 7. Prochains matchs et composition (gold.ts_upcoming) : aucune composition enregistrée
| Club | Match | Date Paris | Limite composition |
|---|---|---|---|
| Cows | coupe, BOT (2082494, dom.) | 28 10 15:11 | 28 10 13:11 |
| Cows | coupe, BOT (2083110, dom.) | 29 10 15:35 | 29 10 13:35 |
| Cows | ligue, FC Bresse (1977459, dom., 3e, 12 pts, note 82,7) | 31 10 13:50 | 31 10 11:50 |
| Ben Ahmed | coupe, Potatos y Potitas (2082895, ext., note 77,58) | 28 10 15:35 | 28 10 13:35 |
| Ben Ahmed | ligue, BOT (2080331, ext.) | 29 10 19:30 | 29 10 17:30 |

## 8. Classement erroné du script
| page_type | Contient autre chose | Critère |
|---|---|---|
| `dashboard`, `dashboard_finances`, `_stadium`, `_training`, `_matches`, `_league`, `_team` | réponses annexes `last_seen_*`, `login_streak`, `cash_balance`, `transfer_listing_id` | vraie donnée = clé propre (`weekly_income`, `rating`, `match_id_int`, etc.) |
| `dashboard_transfers` | liste de 8 `transfer_listing_id`, `cash_balance` | annonce = ligne avec `bids` + `player` |
| `dashboard_matches` / `_league` / `_team` | historique saison (`source_match_id`), classements, stats, noms d'équipes | match = `match_id_int` + `status` |
| `dashboard_training` | fiche joueur complète + plan | plan = `training_type` ; fiche = `last_name` + `rating` |

## 9. Nouveautés (ajoutées à commun.md)
Champs bruts jamais déclarés : `is_admin_match`, `is_promotion`, `time_changed`, `room_challenge_id`, `custom_tournament_id`, `team_morale` (75), `team_spirit` (Normal), `shirt_color`, `name_changed`, `hotlists`, `season_yellow_cards`, `injured_at`. Effet inconnu : à tester, mesure = résultat de match / Forme.

## 10. Reste à exporter
- Composition Cows–BOT du 28 10 (avant 13:11 Paris) : Mon équipe > Composition (Cows), enregistrer puis exporter.
- Composition Ben Ahmed–Potatos y Potitas (avant 13:35 Paris) : même écran côté Ben Ahmed.
- HPC (TSC) : écran Centre de Haute Performance, aucun export depuis le 19 10.
- Page match Ajax–Cows (2080875) et BOT–Ben Ahmed (2080326) : écran match-viewer si l'analyse est voulue.

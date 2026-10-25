# Team Soccer — lecteur d'exports, passage du 2026-10-25 (exports 09:16–09:17 UTC)

## 1. Inventaire
| Catégorie | Nombre | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Académie (youth-scout) : 2 listes de 16 jeunes (Ben Ahmed = académie 376, Cows = 18), 6 POST de révélation, 2 HTML | 12 | Listes : oui (`ts_youth_players` day 2026-10-25 pour Ben Ahmed ; Cows seulement day 2026-10-24). POST : NON (revealed_count/last_reveal_date restent au 10-24). HTML : non | 6 révélations faites, 3/3 par club |
| Effectif Cows (dashboard_squad) : 22 joueurs, plan d'entraînement 22 lignes, cash 1 610 299 $, match_id_int 2080875 | 7 | Oui (`ts_player_snapshots` 22 lignes, `ts_training` 22 lignes, day 2026-10-25) | Forme 96 pour 20/22 |
| Historique Cows (dashboard_team) : matchs de la saison 2 | 1 | Non lu (anciens matchs, aucun intérêt) | rien |
| Marché (dashboard_transfers) : 52 annonces (44 Cows, 8 Women's), 2 HTML, soldes 1 610 299 $ (Cows) et 626 910 $ (Ben Ahmed) | 24 | Annonces : oui (`ts_transfer_listings`, 52 vues aujourd'hui = 52 brutes). Soldes : non (`ts_finances` dernier jour 2026-10-23) | marché à jour |
| Réponses annexes rangées en `dashboard_transfers` : classements, stats joueurs, coupes, matchs d'autres séries, noms d'équipes | environ 14 | Non (hors périmètre) | rien d'utile pour la décision |

## 2. Vérifications demandées
| Question | Réponse |
|---|---|
| Composition Cows–Ajax (2080875, mardi 26 10 02:00 Paris, `competition` = inconnu) | NON enregistrée en base. Aucune ligne `ts_match_lineups` pour ce match ; dernière composition Cows = 2026-10-19 (1-4-3-3). Aucun export du jour ne contient de composition. Silver : `scheduled`, 0 composition. |
| Composition Ben Ahmed–BOT (2080326, lundi 26 10 19:30) | Une ligne existe (`ts_match_lineups`, day 2026-10-23, 1-4-4-2, neutral, `updated_at` null) : exportée avant aujourd'hui, donc impossible de dire si elle est encore à jour. Aucune composition dans les exports de 09:17. |
| Révélations d'académie du jour | FAITES, 3/3 par club (texte du site : « Has usado las 3 revelaciones de hoy », reset 01:00 UTC). |

Révélations extraites du brut (POST) :
| Club | Joueur | Poste | Compétence révélée | Valeur |
|---|---|---|---|---|
| Ben Ahmed | Min-ji Mori (16) | DEF | Endurance | 49 |
| Ben Ahmed | Zainab García (16) | DEF | Définition | 16 |
| Ben Ahmed | Olivia Chukwu (16) | FWD | Gardien | 11 |
| Cows | Jules Bernard (16) | DEF | Endurance | 37 |
| Cows | Jules Bonnet (16) | MID | Endurance | 33 |
| Cows | Baptiste Girard (16) | MID | Conduite | 51 |

Académie : Ben Ahmed niveau Noble, 22/24 ; Cows niveau Intermédiaire, 22/24.

## 3. Extraction directe (non lu par silver)
- Soldes : Cows 1 610 299 $ ; Ben Ahmed 626 910 $.
- Cows, joueurs avec Forme < 96 : Roux (315, FWD 19 ans, note 63) Forme 56 ; Leroy (321, DEF 32 ans, note 56,6) Forme 100 mais entraînement intensité 0 % en défense, progression −0,575 ; les 3 jeunes de 17-18 ans à 72 et le gardien Martin (296384) à 98.
- Cows, meilleurs : Ounahi DEF 19 ans note 90 ; Moreau FWD 20 ans 71 ; Bonnet FWD 24 ans 68 ; Simon DEF 21 ans 68 ; Roux MID 25 ans 67 ; David MID 26 ans 67.
- Marché Cows : Omar Hassan (id 5343, MID 20 ans, note 77,2, Forme 30, 4 enchères, 1 814 459 $ — au-dessus du solde de 1 610 299 $) ; Flores (5350, DEF 28 ans, 65, Forme 100, 0 enchère).

## 4. Classement erroné du script
| page_type | Contient autre chose | Critère |
|---|---|---|
| `dashboard_transfers` | classements, stats, coupes, équipes d'autres séries, soldes, 2 pages HTML | vraie annonce = ligne de `body` avec `bids` et `player` |
| `dashboard_squad` | login_streak, visiteurs, utilisateurs actifs, solde, match_id_int, série | vraie fiche = ligne avec `last_name` + `rating` ; plan d'entraînement = `training_type` |
| `dashboard_team` | historique de matchs de la saison 2 de Cows | `season`, `source_match_id` |
| `dashboard_youth-scout` | session (`session_token`, ne pas recopier), login, POST de révélation | liste = `academy_id` ; POST = `method` = POST + `skill_name` |

## 5. Nouveautés (comparées à `docs/fiches/teamsoccer/`)
Ajoutées à `commun.md`, section « Options observées » : `login_streak` (19), `daily_reveal_count` / `fully_revealed_count`, `eliminated_in_round` (coupe), `reward` / `page_key` (récompense « foros »). Aucun `<select>` ni `<option>` dans les HTML. Effet inconnu : à tester, mesure = résultat des révélations (login_streak non relié à une règle connue).

## 6. Reste à exporter
- Composition Cows–Ajax : à ouvrir « Mon équipe > Composition » (Cows), l'enregistrer, puis exporter la page.
- Composition Ben Ahmed–BOT : même écran côté Ben Ahmed (à réexporter pour confirmer la ligne du 10-23).
- Finances : aucun export depuis le 2026-10-23.

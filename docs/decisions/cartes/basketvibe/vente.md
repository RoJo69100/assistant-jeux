# Carte basketvibe — vente (mise en vente, libération)

Sources lues : commit fa4743a (2026-10-31)

Écrite le 2026-10-31 (skill transferts, vues gold). Règles : CLAUDE.md « Vitesse » 5 (une vente identifiée reste ouverte jusqu'à exécution), règle 11 (ventes ouvertes vérifiées à chaque passage), A-4.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:31 | ce joueur est-il à vendre | var. 1, 7 |
| :37 | revendre nos joueurs | var. 4 |
| :38 | faut-il vendre | var. 1-6 |

## Rendu (figé)
1. Ventes ouvertes d'abord : `| Joueur | Prix actuel | Enchères | Fin (Paris) | Statut |`.
2. `| Priorité | Joueur | Âge | PS | Rang à son emplacement | Min/match | Salaire/sem. | Prix réf. (p25–méd.) | Prix minimum proposé | Verdict |`.
3. Pourquoi, remplaçant interne nommé, ce qui prouvera l'erreur. Rien n'est mis en vente sans accord.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats à la vente | `select name, position, age, ps, salary, salary_per_ps, potential_est, trend_s3, best_slot, rank_in_slot, on_transfer_list, age_flag, available_players from gold.bv_sell_candidates limit 10` | Rang ≥ 3 à son emplacement, peu de minutes, salaire élevé par PS, ou ≥ 30 ans | skill transferts § Points de règle ; [M§8.5] | |
| 2 | Minutes et rendement sur la saison | `select name, games, min_per_game, eval_per_game from gold.bv_player_outlook` | Toute la saison, pas un match | CLAUDE.md règle 5 | |
| 3 | Remplaçant interne | `gold.bv_slot_fit where slot = '<emplacement>' order by rank_in_slot` | Écart de fit avec le remplaçant | — | |
| 4 | Valeur marché | `gold.bv_market_price_ref`, `gold.bv_price_ref_ps`, `gold.bv_resale_stats` | Le vendeur touche 95 % | [M§11.1] | |
| 5 | Règles | skill transferts § Vendre | Enchère ~2 jours, non annulable ; 9 disponibles avant de vendre ; un joueur acheté attend 7 jours | [M§11.1] | |
| 6 | Progression ou déclin | `select name, age, tsp_s1, tsp_s2, trend_s3 from gold.bv_player_outlook` | ≥ 31 ans : déclin ; jeune à fort potentiel : garder sauf prix | [M§8.5] | |
| 7 | Ventes ouvertes | `select name, current_price, bid_count, ends_at, status from silver.bv_transfer_auctions where seller_team_id = (select team_id from silver.bv_my_team) order by seen_at desc limit 5` | Vendu, prix, retiré | CLAUDE.md règle 11 | |
| 8 | Avis des amis | connaissance § Transferts | — | connaissance | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
| 2026-10-31 | Taxe | 5 % → 5 % ; taxe dégressive (semaine 2 à 20 %…) toujours non décidée | vachacz #economy 2026-10-22 |
| 2026-10-31 | Après une vente | — → rouvrir les préréglages et les matchs planifiés (vendre un joueur du préréglage a bloqué la sauvegarde) | tankre1792, Dev 2026-09-18/19 |

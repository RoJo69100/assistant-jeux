# Lecteur d'exports BasketVibe, 2026-10-30, lot 08:41-08:58 UTC (10:41-10:58 Paris)

## 1. Inventaire (heures UTC)
| Catégorie | Nombre | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| API annexes (finance, auctions, academy, fixtures, standings, cup, auth, messages, training) rangées en `club` (17), `unknown` (10), `notifications` (3), `schedule` (2) | 32 | oui (bv_api, finance, standings, training) | solde, enchères, classement, entraînement |
| Effectif (`roster` : overview JSON 08:57:44 + HTML) | 2 | oui (bv_players) mais **gold.bv_roster_now garde Klein et Fontaine** | 16 joueurs réels |
| Match amical 30/10 (`friendly` : preview, play-by-play, 4 period-box, tactics-used, tactics) | 9 | oui (bv_matches, 140 lignes bv_match_player_stats, 408 événements, 1 tactique) ; absent de `bv_fixtures` et de `bv_match_report` | box score ci-dessous |
| Marché (8 pages d'enchères, mes enchères, offres, finance) | 12 | oui (bv_transfer_auctions, gold.bv_market_candidates) | cibles, Burke |
| `transfers_club-history` 08:58:01 / `transfers_global-history` 5 pages | 1 / 6 | oui | Klein vendu |

## 2. Réponses
**Klein** : VENDU 1 000 (fee) à Smart Signs. (ES), réglé le 29/10 à **19:17:00 UTC** (pas 20:16), encaissé 950 (taxe 5 %), solde après 1 087 843. Il n'est plus dans l'overview brut de 08:57 (16 joueurs).

**Amical 30/10 contre Istanbul Cobras** (domicile, 08:00 Paris, fixture 2bfe4b08) : joué et exporté. `my_side` home, `my_result` **W** ; 102-75 ; Q1 19-16, Q2 33-26, Q3 33-21, Q4 17-12 ; affluence 353, billets 17 650. Joueur du match : Bernard 21 pts, 13 reb, éval 31.
| Joueur | Poste | Min | Pts | Tirs | 3pts | LF | Reb | Ast | Stl | TO | PF | +/- | Éval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Leclerc | SG | 36 | 25 | 8/21 | 5/15 | 4/8 | 4 | 5 | 1 | 0 | 1 | +22 | 18 |
| Lecomte | SF | 36 | 10 | 5/11 | 0/2 | 0/0 | 3 | 1 | 4 | 0 | 2 | +15 | 12 |
| Bernard | C | 24 | 21 | 10/12 | 1/1 | 0/0 | 13 | 0 | 1 | 2 | 3 | +10 | 31 |
| Ungureanu | C | 24 | 11 | 5/9 | 1/2 | 0/0 | 16 | 1 | 1 | 2 | 2 | +17 | 23 |
| Albano | PF | 24 | 9 | 2/10 | 0/2 | 5/7 | 7 | 0 | 0 | 4 | 4 | +15 | 2 |
| Legrand | PF | 24 | 7 | 3/11 | 0/3 | 1/2 | 8 | 1 | 0 | 1 | 0 | +12 | 6 |
| Boyer | PG | 24 | 5 | 2/4 | 1/3 | 0/0 | 3 | 2 | 3 | 3 | 0 | +12 | 8 |
| Baron | PG | 24 | 4 | 2/5 | 0/2 | 0/0 | 0 | 1 | 0 | 2 | 0 | +15 | 0 |
| Durand | SF | 12 | 6 | 3/5 | 0/2 | 0/0 | 2 | 0 | 1 | 1 | 1 | +12 | 7 |
| Dang | SG | 12 | 4 | 2/3 | 0/1 | 0/0 | 3 | 0 | 0 | 0 | 1 | +5 | 6 |
Non jouent (0 min) : Fournier, Bonnet, Gimenez, Richard, Lefebvre.
Jeunes : Leclerc 36 min, Lecomte 36 min, Bernard 24 min, Baron 24 min (tous ont joué).

**Roster après l'amical (overview 08:57 UTC, 16 joueurs, forme 6 partout sauf Ungureanu 5, aucune blessure `injury_return_on` nul)** : fatigue Lecomte 0,74 ; Leclerc 0,60 ; Albano 0,60 ; Baron 0,49 ; Bernard 0,49 ; Ungureanu 0,47 ; Boyer 0,38 ; Legrand 0,35 ; Dang 0,23 ; Durand 0,17 ; Fournier, Lefebvre, Richard, Gimenez, Bonnet, Henry 0.

**Marché / argent** : solde et `transfer_available` 1 105 493, `transfer_committed` 0. Burke (Ewan, SG 29 ans, PS 62,7, rang 1 au poste, gain +6,2 sur mon 2e) : prix 660 000 (29/10 10:00) -> 810 000 (12:56) -> **1 200 000** (4 offres, chaleur 4), fin 30/10 20:13 UTC ; mon enchère max 800 000, je ne mène pas : dépassé de 400 000, et 1 200 000 > solde minus rien d'engagé = 1 105 493 : **non finançable**. Autres cibles qui améliorent le cinq (gain contre mon 2e) : Lazauskas SG 62 (1 750 000, fin 30/10 16:06 UTC), Woźniak PG 61,7 (2 038 000, 13 offres), Sokolov SG 60,9 (1 299 999, sans offre, fin 31/10 23:03 UTC) : aucune sous 1 105 493 sauf Perry PF 62 (280 250, 6 offres, fin 31/10 15:00 UTC, gain +3,4) et Bošković PF 60,7 (500, 2 offres, fin 01/11 23:11 UTC, gain +2,1). `capacite_invest` : non lisible (vue finance_health sans valeur, sponsor/recurring null).
Mes ventes : Lecomte 50 000 et Henry 1 000, sans offre, fin 31/10 22:17 UTC. Deux annonces non vendues le 29/10 19:17 (notifications `transfer_listing_unsold`), relistées d'après les dates (inférence).

**Amical 31/10 contre BC Calije (extérieur, fixture 17bcb69d, 08:00 Paris)** : `status` scheduled, `has_saved_match_tactics` **false**, `can_edit` true : **plan non sauvegardé**. Adversaire : seulement nom et lieu dans la liste ; aucun aperçu en base (aucun export pour cet id) : compétences non lisibles. Suivants : 01/11 Granada Sentinel (domicile), 02/11 Galit sa gobyerno (domicile).
Ligue : 02/11 20:00 Paris à Chara legends (extérieur, rang 7, chance 50/50, tactique non sauvegardée).

## 3. Ce que silver ne lit pas / incohérences
- `gold.bv_roster_now` contient encore **Klein** (on_transfer_list vrai) et **Fontaine** (dernier vu 25/10) : à filtrer sur le dernier snapshot (18 lignes au lieu de 16).
- `silver.bv_fixtures` n'a pas l'amical 30/10 ; `gold.bv_match_report` ne couvre que ligue/coupe : box score amical lu depuis `bv_matches` + `bv_match_player_stats`.
- `gold.bv_zone_jouee` s'arrête à la coupe du 29/10 : zone de l'amical 30/10 non calculée.
- Ligue et box : exports de 26/10 (85 h) à refaire pour la ligue du 02/11.

## 4. Classement erroné du script
| page_type | Contenu réel | Critère |
|---|---|---|
| club | 17 API (finance, academy, friendlies, cup, standings, auth...) | classer par `source_url` |
| unknown | notifications, messages, auth, training, watchlist | `source_url` |
| notifications | standings (copie) | `source_url` |
| schedule | friendlies + HTML | `source_url` |
| roster | overview JSON + HTML | `source_url` nul = HTML |
| transfers | finance + my-offers + HTML | `source_url` |
| friendly | `/teams/.../tactics` (équipe, pas du match) | `source_url` |

## 5. Reste à exporter
- Aperçu de l'amical du 31/10 contre BC Calije : ouvre l'amical dans Amicaux (lecture seule, facultatif, adversaire sans importance).
- Ligue 02/11 contre Chara legends : ouvre l'aperçu du match (dernier export 26/10).
- Personnel : dernier export 25/10 (dimanche 01/11).

## 6. Nouveautés
Ajoutées dans `docs/fiches/basketvibe/commun.md` : `heat_level`, `blind_ends_at`, `pending_settlement`, `is_viewer_leading`, `my_max_bid`, `scheduling_hints`, `team_context`. `page_typee_reelle` non ajouté en config (7 types mélangés : classer par `source_url`).

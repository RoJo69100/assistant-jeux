# BasketVibe — inventaire d'ingestion avant l'étude « focus adverse inféré » (16/11/2026)

Source : requêtes `pipelines/sql.py` du 16/11 (lecture seule, 21 requêtes). Saison courante `86a63498…`.
Verdict : **étude non lancée** (seuil fixé : 60 matchs de ligue avec box par quart + play-by-play ; disponible : 42).

## Constat principal
- Captures BasketVibe par jour (UTC) : 10/11 423 · 11/11 37 · 12/11 63 · 13/11 290 (09:00–09:27) · **14/11 0 · 15/11 0** · 16/11 96 (09:26–09:29).
- Depuis le 13/11 : 23 pages match distinctes, 5 pages club d'autres clubs (`/c/air-hache`, `hapoel-nehamia-galil`, `juventus-basket`, `kk-uola`, `maccabi-4`).
- Ingestion silver complète pour ce qui est arrivé : 21/21 matchs de ligue captés ont box et événements. Le manque est en amont (pages non reçues en bronze), pas dans le parsing.

## a. Captures depuis le 13/11 (UTC)
| Source | Type | n | Premier → dernier |
|---|---|---|---|
| page | match | 169 (23 URL) | 13 09:24 → 16 09:29 |
| page | standings (+ clubs/history/transfers) | 62 + 16 | 13 09:23 → 16 09:28 |
| page | unknown (`/c/<club>`, coupe) | 34 (6 URL) | 13 09:23 → 16 09:29 |
| page | friendly / transfers / club / player | 26 / 13 / 13 / 10 | 13 → 16 |
| api | `/fixtures/N/period-box` | 88 | 13 09:24 → 16 09:28 |
| api | `/fixtures/N/play-by-play` | 21 | 13 09:24 → 16 09:28 |
| api | `/fixtures/N/preview` | 24 | 13 09:24 → 16 09:29 |
| api | `/leagues/N/seasons/N/injuries` | 4 | 13 → 16 |
| api | `/leagues/N/recent-transfers` | 3 | 13 → 16 |
| api | `/clubs/<slug>/season-roster` | 2 (juventus, kk-uola) | 16 09:29 |
| api | `/fixtures/N/match-tactics` (le nôtre) | 1 | 13 09:27 |

## b. Matchs de ligue terminés, saison courante (J1–J6), avec box joueur, box par quart et play-by-play
Rattachement ligue par l'équipe à domicile (approximatif : quelques matchs d'autres ligues s'y glissent).
| Ligue | J1 | J2 | J3 | J4 | J5 | J6 | Total captés |
|---|---|---|---|---|---|---|---|
| 45ca… | 0/6 | 0/6 | 0/6 | 2/6 | 6/6 | 2/6 | 10/36 |
| 5fdd… (la nôtre) | 4/6 | 3/6 | 3/6 | 1/6 | 6/6 | 0/6 | ≈17/36 |
| a725… | 3/6 | 3/6 | 3/6 | 0/6 | 6/6 | — | 15/30 + J6 non listée |
Toutes compétitions de ligue confondues : 42 matchs avec box 0, box Q1–Q4 et événements (box et événements toujours ensemble).

### Matchs à rouvrir (onglets Details, Stats par quart, Play-by-play)
- **45ca J1** : Braga Warriors-Pécs Panthers / Papuk Velika-Beogradski Medjedi / Østerbro Nord Goldeneyes-Juventus Basket / BC Greendale Human Beings-BG Bangers / Air Hache-KK Uola / Ballon Basket-Garden City
- **45ca J2** : Papuk Velika-Østerbro Nord Goldeneyes / Garden City-KK Uola / BG Bangers-Ballon Basket / Pécs Panthers-BC Greendale Human Beings / Juventus Basket-Air Hache / Beogradski Medjedi-Braga Warriors
- **45ca J3** : Ballon Basket-Pécs Panthers / KK Uola-BG Bangers / Østerbro Nord Goldeneyes-Beogradski Medjedi / Braga Warriors-BC Greendale Human Beings / Garden City-Juventus Basket / Air Hache-Papuk Velika
- **45ca J4** : Papuk Velika-Garden City / BG Bangers-Juventus Basket / BC Greendale Human Beings-Beogradski Medjedi / Braga Warriors-Ballon Basket
- **45ca J6** : Pécs Panthers-Papuk Velika / Braga Warriors-Juventus Basket / Østerbro Nord Goldeneyes-BG Bangers / Beogradski Medjedi-Ballon Basket
- **5fdd J1** : BC Gelrode-Naked Spartans / BC KIT-Águias do Guadiana
- **5fdd J2** : Naked Spartans-Astur Hoops / BC KIT-BC Gelrode / Wrzos Zmigrod-Chara legends
- **5fdd J3** : C.B.Granada-Naked Spartans / Astur Hoops-BC KIT / BC Gelrode-Águias do Guadiana
- **5fdd J4** : Chara legends-Águias do Guadiana / Žirmūnai-Eindhoven Wizards / Wrzos Zmigrod-Póvoa Riptide / BC KIT-C.B.Granada / BC Gelrode-Astur Hoops
- **5fdd J6** : Águias do Guadiana-Eindhoven Wizards / Žirmūnai-Naked Spartans / Chara legends-Póvoa Riptide / Wrzos Zmigrod-BC KIT / Astur Hoops-C.B.Granada (+ BC Gelrode-Chomelix Cow, à vérifier)
- **a725 J1** : YMCA Łódź-Suricata Squad / DenverNug-AlpaChino / Milano Jazz-Bibim Bożejewice
- **a725 J2** : Rifiuti Organici-Bratrstwo Wlkodlaka / Suricata Squad-Milano Jazz / KK Glen Johnson-DenverNug
- **a725 J3** : DenverNug-Bibim Bożejewice / AlpaChino-Rifiuti Organici / Bratrstwo Wlkodlaka-YMCA Łódź
- **a725 J4** : YMCA Łódź-AlpaChino / KK Glen Johnson-Rifiuti Organici / Milano Jazz-DenverNug / KK Bedex-Bratrstwo Wlkodlaka / Artica Slayers-Suricata Squad / Bibim Bożejewice-Sakar SuperSonics
- **a725 J6** : aucun match listé comme terminé dans `silver.bv_fixtures` → rouvrir le calendrier (round 6) de la ligue a725.

## c. Effectifs (`silver.bv_club_roster`)
- 35 clubs ; 1 snapshot (10/11) pour 32 clubs ; 2 snapshots (10/11, 16/11) : juventus-basket, kk-uola ; 3 : povoa-riptide (06, 09, 10/11).
- Forme, fatigue, expérience renseignées pour tous les joueurs ; date de retour de blessure : 13 joueurs.
- Pages club ouvertes le 13 et le 16/11 sans onglet roster capté : air-hache, hapoel-nehamia-galil, maccabi-4.

## d. Présence
| Donnée | Présent | Exemple de clé |
|---|---|---|
| Blessures de la ligue | oui (3 ligues, 3 à 9 joueurs) | `injuries[].injury_return_on`, `avg_pts` |
| Transferts récents de la ligue | oui (20 par capture) | `transfers[].fee`, `settled_at`, `auction_id` |
| Historique de transferts d'un club | **non** (seul `/transfer-history` global) | `transfers[].fee`, `player_age` |
| Tactiques d'un match d'un autre club | **non** (`match-tactics-used` vu seulement avec `viewer_is_primary = true`, coupe et amical) | `defensive_focus`, `opponent_lineup_by_quarter` |
| « Estimated chance » | oui (preview ligue et amical) | `estimated_chance.home_pct` / `away_pct` |

## e. Tranches vs valeurs exactes du marché
52 joueurs (416 compétences) vus en tranche sur une page club puis au marché. 413/416 dans la tranche ; largeur moyenne 19 ; position moyenne 0,54, médiane 0,58 (0 = bas, 1 = haut) ; 16 au minimum, 32 au maximum. Limite : écart de dates entre snapshot (10/11) et vente non corrigé de l'entraînement.

## f. n disponible par question
| Question | n | Suffisant ? |
|---|---|---|
| Fatigue de ligue v4 | 39 intervalles joueur entre 2 snapshots, 28 avec au moins un match en box | faible (3 clubs seulement) |
| Taux de blessures | 20 160 minutes-joueurs (42 matchs) ; 15 entrées injuries (dernière capture par ligue : 9 + 3 + 3, doublons non contrôlés) | faible |
| Rotations | 7 équipes avec ≥ 4 matchs en box (max 5), 13 avec ≥ 3 | faible |
| Focus adverse | 56 joueurs avec ≥ 4 matchs (≥ 3 hors match testé) | sous le seuil de 60 matchs |
| Modèle joueurs | 102 joueurs avec ≥ 3 matchs, dont 93 avec tranches | utilisable pour un premier essai |

## À faire avant de relancer l'étude
1. Vérifier le userscript : rien n'est arrivé les 14 et 15/11 ; le 16/11 seulement 3 minutes de captures.
2. Rouvrir les matchs listés en b (≈66) avec les 3 onglets ; il en faut au moins 18 de plus pour atteindre 60.
3. Rouvrir l'onglet roster d'air-hache, hapoel-nehamia-galil, maccabi-4, et un 2e snapshot des 32 clubs à 1 snapshot.
4. Contrôler la version du moteur des 3 ligues au relancement (non vérifiée ici, étude non lancée).

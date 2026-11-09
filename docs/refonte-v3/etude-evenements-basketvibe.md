# Étude du moteur de match BasketVibe au niveau de l'événement

Écrit le 2026-11-09. Lecture seule (aucune écriture en base). Contexte : le développeur écrit que le moteur joue possession par possession ([Dev 2026-09-17, engine], skill `basketvibe-communaute`) ; la préanalyse (`docs/refonte-v3/preanalyse-matchs-basketvibe.md`) comptait des matchs. Ici l'unité est l'événement (tir, possession, joueur-quart). Les moteurs v3, v4 et v5 ne sont jamais mélangés, ni la ligue, la coupe et les amicaux.

Groupes : v3 ligue (07/09 au 26/10), v3 amical (10/10), v4 ligue (dès le 02/11), v4 coupe (28/10 au 31/10), v4 amical (11/10 au 27/10), v5 amical (dès le 28/10). La version est déduite des dates (aucune colonne ne la porte) : règle du § 1.1 de la préanalyse.

## Étape 1 : relevé et inventaire (relevé du 2026-11-09, 11:40 Paris)

### 1a) Matchs de ligue v4 terminés, par division
Source : `silver.bv_api` (pages `/leagues/<division>/seasons/<saison>/fixtures`), saison 2 (`86a63498-…`), croisée avec `silver.bv_matches`.

| Division | Matchs au calendrier | Terminés | Terminés avec box score | Terminés sans box score |
|---|---|---|---|---|
| `5fdd980c` (la mienne) | 132 | 18 | 10 | 8 |
| `a7250ea5` | 132 | 18 | 9 | 9 |
| `45caebc5` | 132 | 18 | 0 | 18 |
| Total | 396 | 54 | 19 | 35 |

Les 8 matchs de MA division terminés sans box score (liste exacte, `silver.bv_fixtures` moins `silver.bv_matches`) :

| Journée | Date | Match (domicile − extérieur) |
|---|---|---|
| 1 | 02/11 | BC Gelrode − Naked Spartans |
| 1 | 02/11 | BC KIT − Águias do Guadiana |
| 2 | 04/11 | BC KIT − BC Gelrode |
| 2 | 04/11 | Naked Spartans − Astur Hoops |
| 2 | 04/11 | Wrzos Zmigrod − Chara legends |
| 3 | 07/11 | Astur Hoops − BC KIT |
| 3 | 07/11 | BC Gelrode − Águias do Guadiana |
| 3 | 07/11 | C.B.Granada − Naked Spartans |

### 1b) Niveau événement : `silver.bv_match_events` (33 127 événements, 78 matchs)
Les chiffres ci-dessous sont ceux du relevé de 11:40 ; la base grossit à chaque export, et le script `pipelines/etude_evenements_basketvibe.py inventaire` les rejoue (10 s). Types d'événements et nombre par groupe :

| type | v3 ligue | v3 amical | v4 ligue | v4 coupe | v4 amical | v5 amical | total |
|---|---|---|---|---|---|---|---|
| miss / miss_fg | 2001 | 88 | 1548 | 819 | 1394 | 916 | 6766 |
| dreb / dreb | 1532 | 67 | 1289 | 699 | 1116 | 733 | 5436 |
| ft / ft_make | 784 | 40 | 608 | 381 | 513 | 287 | 2613 |
| fg2 / fg2_make_paint | 588 | 26 | 711 | 350 | 540 | 285 | 2500 |
| assist / assist | 588 | 23 | 690 | 314 | 487 | 321 | 2423 |
| fg2 / fg2_make_mid | 616 | 29 | 485 | 242 | 431 | 310 | 2113 |
| oreb / oreb | 507 | 20 | 438 | 233 | 376 | 203 | 1777 |
| turnover / steal | 434 | 22 | 394 | 227 | 294 | 190 | 1561 |
| fg3 / fg3_make | 401 | 20 | 306 | 134 | 307 | 196 | 1364 |
| foul / foul | 372 | 11 | 317 | 159 | 287 | 149 | 1295 |
| foul / shooting_foul | 379 | 18 | 304 | 191 | 251 | 135 | 1278 |
| turnover / turnover | 303 | 10 | 260 | 136 | 211 | 126 | 1046 |
| ft / ft_miss | 301 | 6 | 233 | 148 | 230 | 113 | 1031 |
| miss / block | 107 | 5 | 174 | 109 | 98 | 47 | 540 |
| dead_ball / dead_ball | 133 | 7 | 97 | 64 | 86 | 63 | 450 |
| period_start / period_start | 88 | 4 | 76 | 40 | 64 | 40 | 312 |
| period_end / period_end | 88 | 4 | 76 | 40 | 64 | 40 | 312 |
| jump_ball / jump_ball | 22 | 1 | 19 | 10 | 16 | 10 | 78 |
| foul / tactical_foul | 5 | 0 | 9 | 14 | 14 | 10 | 52 |
| substitution / foul_out | 17 | 0 | 9 | 9 | 12 | 3 | 50 |
| substitution / substitution_foul_trouble | 17 | 0 | 9 | 9 | 12 | 3 | 50 |
| substitution / player_injury_in | 12 | 0 | 10 | 0 | 0 | 0 | 22 |
| injury / player_injury_out | 12 | 0 | 10 | 0 | 0 | 0 | 22 |
| substitution / substitution_unavailable | 5 | 0 | 7 | 5 | 2 | 0 | 19 |
| endgame / endgame_cue | 2 | 0 | 3 | 4 | 5 | 3 | 17 |

Contenu des événements (requêtes en annexe A) :
- **Tir** : `fg2` (réussi, `fg2_make_paint` cercle ou `fg2_make_mid` mi-distance), `fg3` (réussi), `miss` (`miss_fg` raté, `block` raté contré). Les réussis portent leur zone dans le type ; les ratés ne la portent que dans `payload.shot_zone` (`paint`, `mid`, `three` : 2 288 ratés sur 6 766, versions de coordonnées récentes). L'indicateur `is_three` est renseigné pour les ratés (`miss_fg`) ; il vaut `True` pour 2 réussis seulement : il n'est donc pas fiable pour les réussis, dont le type donne l'information.
- **Coordonnées** `shot_x` et `shot_y` (0 à 1 000 sur chaque axe) : tous les réussis, 6 969 ratés sur 7 306. Tirs avec coordonnées : v3 ligue 3 606 sur 3 713, v4 ligue 3 224 sur 3 224, v4 coupe 1 545 sur 1 654, v4 amical 2 672 sur 2 770, v5 amical 1 736 sur 1 754.
- **Joueur** : `player_id` du tireur, du rebondeur, du passeur (`player2_id` pour la passe) et `payload.player_ids` ; **faute** : `shooting_foul` (faute sur tir, avec `ft_count` lancers), `foul` (autre faute), `tactical_foul` ; **entre-deux** : un par match (`jump_ball`, côté gagnant dans `payload.side`).
- **Remplacements** : 141 événements pour 47 matchs sur 78 (types : sortie pour cinq fautes, gêne de fautes, blessure, joueur indisponible) : pas de remplacement tactique dans le quart. L'effectif sur le terrain d'un quart est donc la composition de début de quart, sauf ces 141 cas.

Couverture par groupe :

| groupe | matchs | événements | tirs | tirs avec coordonnées | fautes sur tir | remplacements | matchs avec remplacement | entre-deux |
|---|---|---|---|---|---|---|---|---|
| v3 ligue | 22 | 9314 | 3713 | 3606 | 379 | 51 | 18 | 22 |
| v3 amical | 1 | 401 | 168 | 163 | 18 | 0 | 0 | 1 |
| v4 ligue | 19 | 8082 | 3224 | 3224 | 304 | 35 | 12 | 19 |
| v4 coupe | 10 | 4337 | 1654 | 1545 | 191 | 23 | 7 | 10 |
| v4 amical | 16 | 6810 | 2770 | 2672 | 251 | 26 | 8 | 16 |
| v5 amical | 10 | 4183 | 1754 | 1736 | 135 | 6 | 2 | 10 |

Compositions de début de quart et réglages tactiques (`silver.bv_match_tactics`) :

| groupe | matchs | dont à nous | avec réglages | composition nôtre | composition adverse | réglages par joueur (nôtres) | focus défensif (nôtre) |
|---|---|---|---|---|---|---|---|
| v3 ligue | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| v3 amical | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| v4 ligue | 19 | 3 | 3 | 3 | 3 | 3 | 3 |
| v4 coupe | 10 | 2 | 1 | 1 | 1 | 1 | 1 |
| v4 amical | 16 | 16 | 14 | 14 | 14 | 14 | 14 |
| v5 amical | 10 | 10 | 9 | 9 | 9 | 9 | 9 |

La composition de début de quart existe **pour les deux équipes** dans nos matchs (50 au total) ; les 16 matchs de ligue v4 d'autres équipes, les 8 de coupe v4 d'autres équipes n'ont ni composition, ni réglage. Les réglages par joueur (rôle, niveau de tir, focus offensif, niveau de défense) sont **les nôtres seulement**.

### 1c) Compétences
**Nos joueurs** (`silver.bv_player_daily`) : 287 lignes, 18 joueurs, 18 jours distincts (relevés les 16, 18, 19, 20, 22 à 27, 29 à 31 octobre, 1er, 2, 4, 6 et 8 novembre), du 2026-10-16 au 2026-11-08, 14 à 17 joueurs par jour ; huit compétences et fatigue, forme, expérience, PS ; compétences à une décimale (`*_exact`) sur 193 lignes sur 287. Avant le 16/10 : aucun relevé. Joueurs-matchs à nous (au moins 1 minute) dont un relevé date de moins d'un jour avant le match :

| groupe | joueurs-matchs à nous | avec un relevé de compétences ≤ 1 jour avant | dont à une décimale |
|---|---|---|---|
| v3 ligue | 163 | 51 | 41 |
| v3 amical | 10 | 0 | 0 |
| v4 ligue | 29 | 29 | 0 |
| v4 coupe | 12 | 12 | 12 |
| v4 amical | 148 | 107 | 79 |
| v5 amical | 94 | 94 | 37 |

**Adversaires, page Preview** (`/fixtures/<id>/preview`, `/friendlies/<id>/preview`, `/cup-fixtures/<id>/preview` ; `silver.bv_api`) :
- Page d'un match **à venir** (`kind = scheduled_lineups`) : 27 pages, 21 matchs. Les joueurs adverses portent `skill_brackets` : **fourchettes de 20 points** (observées : 0–20, 21–40, 41–60, 61–80) pour chacune des huit compétences, avec `skills_visibility = bracket` (334 lignes de joueurs adverses) ; nos joueurs y sont en visibilité complète (`full`, 443 lignes). La page porte aussi la fatigue, la forme et l'expérience des joueurs adverses, leurs statistiques de saison, la composition de début de quart des deux équipes et `estimated_chance` (probabilité estimée de victoire).
- Parmi ces 21 matchs à venir, **17 sont devenus des matchs terminés de nos équipes avec box score** : v3 ligue 4 (19/10, 21/10, 24/10, 26/10), v4 ligue 3 (02/11, 04/11, 07/11), v4 coupe 2 (28/10, 30/10), v4 amical 5 (20/10, 21/10, 24/10, 26/10, 27/10), v5 amical 3 (30/10, 31/10, 05/11) ; 8 à 15 joueurs adverses avec fourchettes par page. Ce sont les seuls matchs où les compétences adverses sont lisibles, sous forme de fourchettes. Les 17 sont tous des matchs de nos équipes (colonne « nous » de la requête de l'annexe A) ; je n'ai pas de preuve qu'une page Preview à venir d'un match d'une autre équipe existe.
- **Page d'un match TERMINÉ** (`kind = finished`), échantillon : 86 pages, 78 matchs, 2 277 lignes de joueurs, dont les matchs d'autres équipes (coupe : 8 ; ligue v4 : 16) : **aucune ligne ne contient de compétence** (`skills`, `skill_brackets` ou `skills_visibility`). Réponse : **non**. La page d'un match terminé porte le box score, la taille, le poids, le numéro de maillot, l'évaluation, `possessions_per_quarter_n`, `estimated_chance`, les quarts-temps et la dynamique du score (`score_momentum`), pas les compétences.
- Autres pages avec compétences d'un joueur : `/players/<id>/season-profile` (14 pages) : profil de statistiques (carrière, moyennes), sans les huit compétences.

## Annexe A : requêtes et sorties de l'étape 1

Commande de l'inventaire (groupes, événements, compositions, compétences de nos joueurs) : `python -I pipelines/etude_evenements_basketvibe.py inventaire` (10,6 s, code 0 ; sortie en tableaux ci-dessus).

Requête 1a (matchs par division) : `select substring(a.endpoint from '^/leagues/([0-9a-f-]{8})') division, count(distinct f->>'id') fixtures, count(distinct f->>'id') filter (where f->>'status'='finished') termines, count(distinct f->>'id') filter (where f->>'status'='finished' and exists (select 1 from silver.bv_matches m where m.fixture_id = (f->>'id')::uuid)) avec_box from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8' group by 1 order by 1` : `45caebc5 132 18 0` ; `5fdd980c 132 18 10` ; `a7250ea5 132 18 9`.

Requête 1a bis (8 matchs manquants de ma division) : `select x.round_number journee, x.match_day jour, x.home_team domicile, x.away_team exterieur from silver.bv_fixtures x where x.season_id = '86a63498-c133-44ea-aedb-f1310ad51ae8' and x.fixture_id in (select (f->>'id')::uuid from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/5fdd980c-032b-4ea3-b608-5eadc0c61f44/seasons/' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8') and x.status = 'finished' and not exists (select 1 from silver.bv_matches m where m.fixture_id = x.fixture_id) order by x.match_day, x.home_team` : 8 lignes (tableau du 1a).

Requête 1b (détails et coordonnées des tirs) : `select kind, detail, count(*) n, count(shot_x) avec_coord, sum(is_three::int) trois from silver.bv_match_events group by 1,2 order by 1, 3 desc` : 25 types ; champs du `payload` par type : `select kind, k, count(*) n from silver.bv_match_events e, jsonb_object_keys(e.payload) k group by 1,2 order by 1, 3 desc` (tir : `sx`, `sy`, `player_ids`, `shot_coords_version`, `putback`, `dunk`, `alley_oop`, `buzzer`, `heave`, `shot_zone` ; faute : `ft_count`, `bonus` ; lancer : `ft_att`, `ft_made` ; entre-deux : `side` ; revirement : `channel`).

Requête 1c (types de pages) : `select regexp_replace(endpoint, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'ID', 'g') motif, count(*) pages, min(captured_at)::date du, max(captured_at)::date au from silver.bv_api group by 1 order by 2 desc` ; Preview par type : `select body->>'kind' kind, count(*) pages from silver.bv_api where endpoint ~ '/preview$' group by 1` : `finished 86`, `scheduled_lineups 27` ; échantillon des pages terminées : `select count(*) pages_terminees, count(distinct a.body->>'fixture_id') matchs, sum(jsonb_array_length(a.body->'players')) joueurs_lignes, sum((select count(*) from jsonb_array_elements(a.body->'players') p where p ? 'skills' or p ? 'skill_brackets' or p ? 'skills_visibility')) avec_competences from silver.bv_api a where a.endpoint ~ '/preview$' and a.body->>'kind'='finished'` : `86 78 2277 0` ; fourchettes des matchs à venir : `select p->'skill_brackets' ... where a.body->>'kind'='scheduled_lineups'` : exemple `{"defense": {"min": 41, "max": 60}, "passing": {"min": 21, "max": 40}, ...}` ; visibilité : `bracket` 334 lignes, `full` 443 lignes.

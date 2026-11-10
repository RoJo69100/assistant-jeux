# Inventaire des sources pour « les meilleurs et les failles » — BasketVibe (10/11/2026)

Lecture seule sur la base (`pipelines/sql.py`). Aucune correction proposée. Quand un payload n'a pas été ouvert, c'est écrit.
Sorties collées telles quelles ; les listes de clés viennent de requêtes `jsonb_object_keys` sur `silver.bv_api` (copie de `payload->'body'` des captures `source='api'`, statut 200) ou de `--page-id N --payload-path …`.

## 1. Les 16 matchs de ligue et les 8 de coupe « sans notre équipe »

**Définition exacte** : un `fixture_id` présent dans `silver.bv_match_player_stats` dont aucune ligne n'a `is_mine = true`. `is_mine` = `p->>'team_side' = m.my_side` (`sql/silver/004_bv_match_stats_team.sql:33`) ; `my_side` = côté (home/away) dont le `team_id` égale `club_id` de `/auth/me` (`sql/silver/003_bv_matches.sql`, vue `silver.bv_my_team`). Ce n'est donc pas un filtre sur la ligue : ce sont des matchs de n'importe quelle équipe dont une page a été ouverte.

Requête :
```sql
select m.competition, m.match_day, m.home_team, m.away_team, m.home_score, m.away_score, m.fixture_id, m.match_id, m.status
from silver.bv_matches m
where m.fixture_id in (select fixture_id from silver.bv_match_player_stats)
  and m.fixture_id not in (select fixture_id from silver.bv_match_player_stats where is_mine)
order by 1,2
```
Sortie (24 lignes) :

| competition | match_day | home_team | away_team | score | fixture_id |
|---|---|---|---|---|---|
| cup | 2026-10-28 | Les sacs de Pessac | Reims Monarchs | 112-119 | e0306d2b-e47d-45b2-9ea6-7d35fa5e5c76 |
| cup | 2026-10-28 | Nebula stickers | Ploppers | 89-118 | 766d70eb-3e58-4d66-a303-31f863af1351 |
| cup | 2026-10-28 | Chara legends | Basktballerz | 72-92 | abde2e6b-87b4-48da-a354-3ce0a74d0ec1 |
| cup | 2026-10-29 | Les Ecureuils Landais | Reims Monarchs | 93-98 | 89fedb58-f665-4d11-868b-33c19612f57e |
| cup | 2026-10-29 | Foo Fighters | Ploppers | 78-89 | 90b94212-eb5f-4b43-93ae-d12d206bb54e |
| cup | 2026-10-30 | Reims Monarchs | Basket pastis | 102-95 | 94aa387a-3b75-4db2-a119-b43b14fb110f |
| cup | 2026-10-30 | Mugertar Hornets | Ploppers | 78-113 | 4eea30f6-91bf-4180-a584-d19344a5a81e |
| cup | 2026-10-31 | Reims Monarchs | Gin Team of Sassenage | 104-97 | 6153a96a-3f34-4b9c-9ede-429ad296a659 |
| league | 2026-11-02 | Bratrstwo Wlkodlaka | Sakar SuperSonics | 83-119 | ffd98d7d-98d7-40c4-a8f9-7dcc1ac85397 |
| league | 2026-11-02 | Artica Slayers | KK Glen Johnson | 128-71 | 1a4f8aa0-bb6e-4db1-8713-bc37582adbe1 |
| league | 2026-11-02 | Eindhoven Wizards | C.B.Granada | 100-83 | 3dfcdddf-0d0d-4aa5-8362-4334063183ff |
| league | 2026-11-02 | Astur Hoops | Póvoa Riptide | 101-111 | d79a55e2-066a-421a-b5d2-07d5c2212607 |
| league | 2026-11-02 | KK Bedex | Rifiuti Organici | 119-96 | e45f9c7a-e6a8-484d-9793-4f027884db23 |
| league | 2026-11-02 | Žirmūnai | Wrzos Zmigrod | 113-100 | f2471c3f-2726-412a-8319-cb7182b67988 |
| league | 2026-11-04 | Águias do Guadiana | Žirmūnai | 116-122 | 9c06fad6-13d0-4a31-b44f-5cff02a8656b |
| league | 2026-11-04 | C.B.Granada | Póvoa Riptide | 97-119 | ad34d9d7-4dc7-49f9-b340-ff380855a279 |
| league | 2026-11-04 | YMCA Łódź | KK Bedex | 77-139 | 09dbb663-14c2-4c37-a4e9-d2c875be1b90 |
| league | 2026-11-04 | AlpaChino | Sakar SuperSonics | 88-96 | 71aeea68-7ef2-444d-9992-41d7f858c598 |
| league | 2026-11-04 | Bibim Bożejewice | Artica Slayers | 82-92 | 20d932c0-e542-4c45-af87-62c4c4f3831e |
| league | 2026-11-07 | KK Bedex | Suricata Squad | 132-106 | 1b77d364-1de6-482a-bcf6-cf3b1bf4a036 |
| league | 2026-11-07 | Milano Jazz | Artica Slayers | 80-112 | 0832dfd6-c56b-4e36-a40d-be138c3d37dc |
| league | 2026-11-07 | Sakar SuperSonics | KK Glen Johnson | 119-73 | baecc636-a83b-44f6-8671-193254634660 |
| league | 2026-11-07 | Eindhoven Wizards | Wrzos Zmigrod | 126-104 | cc3f98a4-2b9c-45fe-b680-86368e5800b3 |
| league | 2026-11-07 | Žirmūnai | Chara legends | 118-90 | f21598c5-525a-496b-82d6-b25ee5ea99e2 |

**Ligue** : 7 matchs de notre ligue (`league_id` 5fdd980c…, saison 86a63498…) et 9 d'une autre ligue (`league_id` a7250ea5…). Requête :
```sql
with d as (select m.* from silver.bv_matches m where m.competition='league' and m.fixture_id in (select fixture_id from silver.bv_match_player_stats)),
c as (select league_id, season_id, home_team_id t from d union select league_id, season_id, away_team_id from d)
select d.league_id::text, d.season_id::text, count(*) matchs,
  count(*) filter (where d.fixture_id not in (select fixture_id from silver.bv_match_player_stats where is_mine)) sans_nous,
  (select count(*) from c where c.league_id=d.league_id and c.season_id=d.season_id) clubs
from d group by d.league_id, d.season_id order by 1,2
```
| league_id | season_id | matchs détaillés | sans nous | clubs |
|---|---|---|---|---|
| 5fdd980c-032b-4ea3-b608-5eadc0c61f44 | 86a63498-c133-44ea-aedb-f1310ad51ae8 | 11 | 7 | 10 |
| 5fdd980c-032b-4ea3-b608-5eadc0c61f44 | 8fa19101-6f06-4e2e-96d5-e3181a8e69f8 | 22 | 0 | 12 |
| a7250ea5-b8b1-4e1d-87c2-020b4572412e | 86a63498-c133-44ea-aedb-f1310ad51ae8 | 9 | 9 | 11 |

**Coupe** : les 8 matchs sont dans `silver.bv_matches` avec 7 `league_id` différents (15f87032, 551af446, 59c51030, 5fdd980c ×4, 6fc35878, 776188b2, 93016d11 ×2, c62fb7d4) — d'autres ligues que la nôtre ; aucun n'a de tactique.

**Type de page d'origine** (requête `silver.bv_fixture_api` ⨝ `bronze.raw_pages`, une ligne par match) :
- 16 matchs de ligue : `page_type = match`, page `/match/<fixture_id>`, captures du 06/11 au 09/11 ; API `/fixtures/<id>/preview`, `/period-box?period=1..4` (4 périodes), `/play-by-play`. Aucun `match-tactics-used` ni `match-tactics`.
- 8 matchs de coupe : `page_type = unknown` (page `/cup/<fixture_id>`, route non reconnue par `pageType()` de `userscripts/basketvibe.user.js:56-80`), captures du 31/10 et du 01/11 ; API `/cup-fixtures/<id>/preview`, `/period-box?period=1..4`, `/play-by-play`. Aucun `match-tactics-used`.

**Box score** : complet. 4 périodes par match (`period-box`) + match complet (`preview`). Clés d'une ligne joueur (capture 38803, 25 joueurs) : `pf ast blk fga fgm fta ftm min pts stl tov dreb eval fg3a fg3m oreb position height_cm last_name player_id team_side weight_kg first_name plus_minus jersey_number injury_return_on nationality_code has_player_avatar`.

**Clés du `preview`** (capture 38803, ligue) : `attendance away_kit away_lineup_by_quarter away_q1_lineup away_score away_team has_play_by_play home_kit home_lineup_by_quarter home_q1_lineup home_score home_team injuries is_walkover kickoff_time kind league_id league_timezone match_day match_id overtime_periods player_of_game players possessions_per_quarter_n quarter_scores round_number score_momentum season_id ticket_revenue fixture_id`. Coupe : mêmes clés plus `cup_name edition_id fixture_kind kickoff_timezone result_revealed`.
**Compositions des deux équipes** : oui, `home_lineup_by_quarter` et `away_lineup_by_quarter` (identifiants de joueurs par quart) sont dans le `preview` des deux équipes. **Tactiques (zone, focus offensif/défensif, consignes par joueur)** : absentes de ces payloads (clés `players` = box score uniquement). Aucune de ces colonnes n'est lue par une vue silver pour les équipes adverses (voir point 5).

## 2. Pages `/c/<club>` classées `unknown`

Requêtes :
```sql
select r.id, regexp_replace(r.page_url,'https?://[^/]+','') u, regexp_replace(r.source_url,'https?://[^/]+','') s, r.source, r.captured_at::date d
from bronze.raw_pages r where r.game='basketvibe' and r.page_type='unknown' and r.page_url ~ '/c/' order by r.captured_at   -- 60 lignes (tronquées)
select regexp_replace(regexp_replace(r.source_url,'^https?://[^/]+/api/v1/clubs/[^/]+/','<club>/'),'\?.*','') ep, count(*) n,
  count(distinct substring(r.source_url from '/clubs/([^/?]+)')) clubs, min(r.captured_at)::date d0, max(r.captured_at)::date d1
from bronze.raw_pages r where r.game='basketvibe' and r.page_url ~ '/c/' and r.source_url ~ '/api/v1/clubs/' group by 1 order by 2 desc
```
| endpoint | captures | clubs | du | au |
|---|---|---|---|---|
| `<club>/schedule` | 9 | 7 | 20/10 | 09/11 |
| `<club>/seasons` | 9 | 9 | 30/10 | 09/11 |
| `<club>/season-history` | 6 | 6 | 09/11 | 09/11 |
| `<club>/trophies` | 6 | 6 | 09/11 | 09/11 |
| `<club>/season-roster` | 2 | 1 | 06/11 | 09/11 |
| `<club>/head-to-head` | 1 | 1 | 06/11 | 06/11 |

**Clubs couverts (10 slugs)** : artica-slayers, baker-street, eindhoven-wizards, havex, istanbul-cobras, kk-bedex, povoa-riptide, sakar-supersonics, vigolana-basket, zirmunai. Seuls 5 ont schedule + season-history + seasons + trophies (artica-slayers, eindhoven-wizards, kk-bedex, sakar-supersonics, zirmunai le 09/11) ; povoa-riptide a en plus season-roster, head-to-head ; baker-street, havex, istanbul-cobras : `seasons` seul ; vigolana-basket : `schedule` seul (20/10).
Les captures du même `page_url` contiennent aussi des endpoints hors club (`/auth/me`, `/leagues/<id>`, `/watchlist/clubs`, `/onboarding/status`, `/maps/countries-50m.json`).

**Contenu (payloads ouverts par `--page-id` / `silver.bv_api`)** :
- `season-roster` (id 37350, povoa-riptide, onglet `?tab=statistics`, saison 86a63498…) : clés `players season_id season_index`; 10 joueurs ; clés d'un joueur : `id age form season fatigue position avatar_id height_cm last_name weight_kg experience first_name avatar_race jersey_number skill_brackets friendly_season injury_return_on is_former_roster nationality_code has_player_avatar is_academy_junior skills_visibility is_on_open_transfer_list`. Valeurs vues : `age 29`, `position C`, `form 6`, `fatigue 7.38`, `experience 4`, `skills_visibility = bracket`, `skill_brackets = {"defense": {"max": 60, "min": 41}, "passing": {"max": 60, …}` : **fourchettes** de compétences, pas les valeurs exactes. Aucune statistique de match (clé `pts` absente).
- `head-to-head` (id 37352) : `filters matches summary viewer_kit opponent_kit season_opti…` ; matches : `match_id match_day season_id away_score fixture_id home_score away_team_id fixture_kind home_team_id round_number season_index viewer_result … has_play_by_play` ; summary : moyennes de marge, points pour/contre, victoires dom./ext., plus grandes victoires/défaites.
- `schedule` (id 37351) : `fixtures season_id team_labels league_timezone` ; 22 fixtures ; clés `id status match_id match_day attendance away_score home_score away_team_id home_team_id round_number result_revealed has_play_by_play can_edit_match_tactics has_saved_match_tactics`.
- `season-history` (id 38590) : `rows team_id league_id team_name league_name league_short_c…` ; 2 lignes ; clés `pa pf diff rank wins losses points league_id season_id league_name season_index league_short_code`.
- `trophies` (id 38591) : `rows team_id cup_rows team_name` ; clés d'une ligne `league_id placement season_id league_name league_tier season_index display_label league_short_code`.
- `seasons` (id 37348) : `seasons current_season_id`.
Effectif : oui (10 joueurs, fourchettes, forme, fatigue) pour 1 club sur 10 ; notes exactes : non ; statistiques de joueur : non ; tactique : non ; classement : non (historique de saisons seulement) ; calendrier : oui. Aucune vue `sql/silver` ni `sql/gold` ne lit `/clubs/…` (grep `/clubs/|season-roster|head-to-head` : 0 résultat).

## 3. Pages `/cup/<id>`

Requête :
```sql
select regexp_replace(regexp_replace(r.source_url,'^https?://[^/]+/api/v1',''),'[0-9a-f-]{36}','<id>') ep, count(*) n,
  count(distinct substring(r.page_url from '/cup/([0-9a-f-]{36})')) fixtures, min(r.captured_at)::date d0, max(r.captured_at)::date d1
from bronze.raw_pages r where r.game='basketvibe' and r.page_url ~ '/cup/' group by 1 order by 2 desc
```
| endpoint | n | matchs | du | au |
|---|---|---|---|---|
| (DOM, sans API) | 18 | 12 | 27/10 | 01/11 |
| `/cup-fixtures/<id>/preview` | 14 | 12 | 27/10 | 01/11 |
| `/cup-fixtures/<id>/period-box?period=1..4` | 10 chacun | 10 | 29/10 | 01/11 |
| `/cup-fixtures/<id>/play-by-play` | 10 | 10 | 29/10 | 01/11 |
| `/leagues/<id>`, `/leagues/<id>/seasons` | 10 | 9 | 29/10 | 01/11 |
| `/cup-fixtures/<id>/match-tactics` | 6 | 4 | 27/10 | 31/10 |
| `/teams/<id>/tactics` | 4 | 4 | 27/10 | 31/10 |
| `/cup-fixtures/<id>/match-tactics-used` | 1 | 1 | 31/10 | 31/10 |
| `/auth/me`, `/news/has-new`, `/teams/<id>/notifications/unread-count` | 3, 1, 2 | — | — | — |

12 matchs de coupe (10 terminés, 2 en `scheduled_lineups`) ; contenu : mêmes box scores et même `preview` (compositions par quart des deux équipes) que la ligue ; cup_name = « National cups », `fixture_kind = cup`. Tactiques : seulement pour 4 matchs de coupe (`match-tactics`, matchs de notre club) et 1 `match-tactics-used`. Les 2 matchs `scheduled_lineups` (Chomelix Cow – Ploppers ; Chomelix Cow – Paris Saint-Germain) : `home_lineup_by_quarter` vide (requête : `lh` = NULL). Lecture par silver : oui, `sql/silver/022_bv_cup_fixtures.sql` (preview, period-box, play-by-play, match-tactics). Le type de page reste `unknown` dans `bronze.raw_pages` (le userscript ne reconnaît pas `/cup/<id>`).

## 4. Onglets `/league/table` du 16/10

Requêtes : `select … from bronze.raw_pages where game='basketvibe' and page_type like 'standings%'` (75 groupes) ; par capture : `jsonb_array_length`, `jsonb_object_keys` sur `silver.bv_api`. Saison de ces captures : **8fa19101-…** (saison précédente ; la saison courante est 86a63498-…, commencée le 27/10).

| page_type | id | endpoint | lignes | ligue | clés d'une ligne |
|---|---|---|---|---|---|
| standings_clubs | 216 | `/leagues/5fdd980c…/human-clubs` | 12 clubs | 5fdd980c (European Division – Tier 3 – League 13, `EU 3.13`) | `rank slug wins losses team_id is_human is_owner league_id team_name arena_name founded_on kit_number kit_pattern league_name league_tier country_code club_strength primary_color arena_capacity … manager_username league_short_code kit_logo_* friendly_allow_invites` |
| standings_teams | 219 | `…/seasons/8fa19101…/team-stats` | 12 équipes | 5fdd980c | `avg_pf fg_pct ft_pct avg_ast avg_blk avg_pts avg_reb avg_stl avg_tov fg3_pct team_id team_name team_slug country_code games_played avg_pts_against` |
| standings_players | 220 | `…/seasons/8fa19101…/player-stats` | 152 joueurs, 12 équipes | 5fdd980c | `fga fg3a fg_pct avg_ast avg_blk avg_pts avg_reb avg_stl avg_tov fg3_pct team_id avg_eval position last_name player_id team_name team_slug first_name country_code games_played double_doubles injury_return_on nationality_code is_on_open_transfer_list` |
| standings_injuries | 221 | `…/seasons/8fa19101…/injuries` | 6 blessés, 3 équipes | 5fdd980c | `avg_ast avg_blk avg_pts avg_reb avg_stl avg_tov team_id position last_name player_id team_name team_slug first_name country_code injury_return_on nationality_code` |
| standings_transfers | 222 | `/leagues/5fdd980c…/recent-transfers?limit=20` | 13 transferts | 5fdd980c | `fee player_id auction_id player_age settled_at to_team_id from_team_id to_team_name … player_position player_height_cm player_last_name player_weight_kg player_first_name … from_team_is_free_agent player_nationality_code` |
| standings_schedule | 180 | (DOM, pas d'API) | — | — | non ouvert |

Une capture chacune (16/10). `team-stats` et `player-stats` n'existent pour **aucune autre date ni saison** (requête `…/seasons/<id>/(team-stats|player-stats|injuries)` : 1 capture chacune, 16/10, saison 8fa19101). Autre endpoint de saison existant : `best-five` (3 captures, 16/10 et 18/10, saison 8fa19101) — **payload non ouvert**. Pour la saison 86a63498 : seulement `standings` (34), `fixtures` (34), `rounds` (4).
**Lecture par silver/gold** : `recent-transfers` oui (`sql/silver/005_bv_club.sql:55`) ; `standings` oui (`005_bv_club.sql:273`) ; `fixtures` oui (vue `silver.bv_fixtures`) ; `team-stats`, `player-stats`, `injuries`, `human-clubs`, `best-five`, `season-history`, `trophies` : non (grep sur `sql/silver` et `sql/gold` : 0 résultat).

## 5. `silver.bv_match_tactics` et `match-tactics-used`

```sql
select count(*) lignes, count(opponent_lineup_by_quarter) non_null,
  count(*) filter (where jsonb_typeof(opponent_lineup_by_quarter)='array' and jsonb_array_length(opponent_lineup_by_quarter)>0) non_vide,
  count(distinct fixture_id) matchs from silver.bv_match_tactics
```
| lignes | non_null | non_vide | matchs |
|---|---|---|---|
| 53 | 53 | 53 | 53 |

`opponent_lineup_by_quarter` est rempli pour les 53 matchs, tous les matchs de notre club (un seul `team_id` dans la table). Contenu : tableau de 5 listes de 5 identifiants de joueurs (ex. `[["6b440bfb-c61d-4a1e-a9d8-b8fe3878e1a9", "46155719-d691-40…`) — la composition adverse par quart, sans réglage.

`match-tactics-used` (`silver.bv_fixture_api.part`) : 53 matchs, 54 captures. Clés du body : `available defensive_focus fixture_id lineup_by_quarter match_id opponent_lineup_by_quarter opponent_team_id opponent_team_name players primary_team_id primary_team_name viewer_is_primary`. Vérification :
```sql
select count(*) n, count(*) filter (where body->>'primary_team_id' = (select team_id::text from silver.bv_my_team)) primaire_nous,
  count(*) filter (where (body->>'viewer_is_primary')='true') viewer_primary from silver.bv_fixture_api where part='match-tactics-used'
```
| n | primaire_nous | viewer_primary |
|---|---|---|
| 54 | 54 | 54 |

et `available = true` pour les 54. Tous nos matchs, jamais ceux d'autres équipes.
- `players[]` (capture 39381) : `position last_name player_id role_tier shot_tier first_name defense_tier nationality_code has_player_avatar offensive_focus_tier` — réglages **de notre équipe** (rôle, tir, défense, focus offensif).
- `defensive_focus[]` : `focus position area_step last_name first_name quarter_slots nationality_code has_player_avatar opponent_player_id` — notre focus défensif, par joueur adverse.
- **Zone, focus offensif et focus défensif adverses : absents.** Seule la composition adverse par quart est fournie. `match-tactics` (20 matchs, 42 captures) : clés `can_edit club_active_preset_id club_lineup_by_quarter cup_fixture_id defensive_focus fixture_id fixture_status friendly_fixture_id has_saved_match_tactics human_team_id is_home league_id player_directives presets preview saved_lineup_by_quarter season_id selected_preset_id` — notre équipe (`human_team_id`). Aucune colonne « zone » dans `silver.bv_match_tactics` (colonnes : `fixture_id team_id team opponent_id opponent defensive_focus lineup_by_quarter opponent_lineup_by_quarter player_directives`).

## 6. Classement

```sql
select regexp_replace(a.endpoint,'^/leagues/([0-9a-f-]{36}).*$','\1') lg, count(distinct x->>'team_id') equipes, max(a.day) dernier, min(a.day) premier, count(distinct a.capture_id) captures
from silver.bv_api a, lateral jsonb_array_elements(a.body->'standings') x
where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/standings$' group by 1 order by 2 desc
```
| league_id | équipes distinctes | premier | dernier | captures |
|---|---|---|---|---|
| 5fdd980c-032b-4ea3-b608-5eadc0c61f44 | 19 | 16/10 | 09/11 | 59 |
| 45caebc5-824f-4d86-85e5-e8956e8cac6a | 12 | 09/11 | 09/11 | 1 |
| a7250ea5-b8b1-4e1d-87c2-020b4572412e | 12 | 09/11 | 09/11 | 3 |
| c62fb7d4-5dd6-4632-8476-371b18f53498 | 12 | 26/10 | 26/10 | 1 |

**Notre ligue** : 5fdd980c (« European Division – Tier 3 – League 13 », `EU 3.13`) ; **12 équipes** dans la saison courante (86a63498, dernière capture 09/11) ; 19 équipes distinctes sur les deux saisons (promotions/relégations). Les 54 équipes de `silver.bv_standings_weekly` = notre ligue (19 sur deux saisons) + 3 autres ligues de 12 (45caebc5, a7250ea5, c62fb7d4) = 55, la différence d'une équipe n'est pas expliquée (non vérifiée). Les noms des 3 autres ligues : introuvables (la requête sur `/leagues/<id>` n'a retourné aucune ligne). Lignes par jour de la vue : 18/10 12 · 25/10 12 · 26/10 19 · 01/11 12 · 08/11 12 · 09/11 36 (3 ligues).
**Colonnes disponibles** (clés d'une ligne du body) : `pa pf diff form rank wins losses points team_id is_human away_wins home_wins is_banned team_name team_slug away_losses home_losses club_strength entry_direction manager_is_online team_country_code manager_last_seen_at manager_public_username entry_from_league_short_code`. La vue `silver.bv_standings_weekly` en garde : `week day season_id rank team_id team wins losses points points_for points_against diff home_wins home_losses away_wins away_losses club_strength is_human form is_mine`. `club_strength` est la force du club ; sa formule : je ne sais pas.
Calendrier de notre ligue (saison courante, `silver.bv_fixtures`) : 60 matchs terminés, 336 programmés.

## 7. Tableau final — une ligne par donnée utile

Légende : E = équipes, T = tactiques, J = joueurs.

| Donnée | Question | En base | Page exacte à exporter, nombre, fréquence |
|---|---|---|---|
| Classement de notre ligue (rang, V/D, points, diff, force du club) | E | oui : 12 équipes, 5 relevés hebdo du 18/10 au 09/11 | `/league/table` (1 page, 1 fois par semaine, déjà exporté) |
| Classement des autres ligues | E | partiel : 3 ligues, 1 à 3 captures, 26/10 et 09/11 | `/league/table` en changeant de ligue, 1 page par ligue ; fréquence : je ne sais pas combien de ligues l'utilisateur veut suivre |
| Stats d'équipe de la saison (tirs, rebonds, passes, pertes, points contre) pour notre ligue | E | partiel : 12 équipes, saison précédente, 1 capture (16/10) ; saison courante : non | `/league/table`, onglet Équipes (1 page, hebdomadaire) |
| Box score complet des matchs de notre ligue | E, J | partiel : 11 matchs détaillés saison courante (4 à nous, 7 sans nous), 10 clubs sur 12 | `/match/<id>` : 60 matchs terminés, 49 manquent ; 3 à 6 par match terminé (preview + 4 périodes + play-by-play, capturés par la même page) ; tous les 2 à 3 jours |
| Box score des matchs des autres ligues | E, J | partiel : 9 matchs de a7250ea5, 8 de coupe | `/match/<id>` ou `/cup/<id>` ; fréquence : à décider |
| Compositions par quart des deux équipes | T, J | oui dans le `preview` de chaque match capturé (81 matchs avec stats) | incluse dans la page match |
| Zone défensive, focus défensif, focus offensif, consignes joueur des adversaires | T | non : 0 ligne pour une équipe autre que la nôtre (`match-tactics-used` : 54/54 « viewer_is_primary ») ; les payloads de matchs d'autres équipes ne contiennent que les compositions | je ne sais pas si le jeu les expose pour les autres équipes : aucun payload en base n'en montre |
| Effectif adverse (âge, poste, forme, fatigue, expérience, fourchettes de compétences) | J | partiel : 1 club sur 10 (10 joueurs, Póvoa Riptide) | `/c/<club>` onglet Statistiques (`season-roster`) : 11 pages pour les 11 autres clubs de la ligue, hebdomadaire |
| Notes exactes de compétences adverses | J | non : `skills_visibility = bracket` (fourchettes) | non exposé dans le payload ouvert |
| Stats saison par joueur, tous clubs de la ligue (pts, rebonds, eval, tirs, matchs joués) | J | partiel : 152 joueurs, saison précédente, 1 capture (16/10) | `/league/table`, onglet Joueurs (1 page, hebdomadaire) |
| Historique des saisons d'un club (rang, V/D, ligue) | E | partiel : 6 clubs, 2 lignes chacun | `/c/<club>` (1 page par club, 1 fois) |
| Trophées/placements | E | partiel : 6 clubs | `/c/<club>` (même page) |
| Confrontations directes | E | partiel : 1 club | `/c/<club>` onglet Face-à-face |
| Calendrier de notre ligue | E | oui : 396 matchs saison courante | `/league/schedule` (1 page, hebdomadaire) |
| Meilleur cinq (`best-five`) | J | partiel : 3 captures, saison précédente, non ouvert | `/league/table` (onglet à identifier ; je ne sais pas lequel) |
| Blessés de la ligue | J | partiel : 6 blessés, 16/10 | `/league/table`, onglet Blessés (hebdomadaire) |
| Transferts récents de la ligue (prix, joueur, âge, poste) | J, E | partiel : 13 transferts, 16/10 ; `silver.bv_transfers` lit `recent-transfers` | `/league/table`, onglet Transferts (quotidien) |
| Matchs de coupe (box scores, compositions) | E, T, J | partiel : 10 terminés, 8 sans nous | `/cup/<id>` (route non reconnue par le userscript → `unknown`) |
| Joueurs adverses avec au moins 5 matchs | J | non : 0 (max 3 matchs dans notre ligue, saison courante ; 48 joueurs à 2 matchs, 9 à 3, 94 en tout) | s'accumule avec les box scores ci-dessus |

## 8. Exports à demander, classés par apport

1. **Tous les matchs terminés de notre ligue, un par un** (`/match/<id>`) — 49 matchs manquants sur 60 ; 1 page par match, tous les 2 à 3 jours ; débloque : box scores + compositions adverses, donc E, J, partiellement T. Apport le plus grand car il fait grossir le nombre de matchs par joueur (max 3 aujourd'hui, seuil 5).
2. **Effectif de chaque club de la ligue** (`/c/<club>`, onglet Statistiques) — 11 pages, une fois par semaine ; débloque : âge, forme, fatigue, fourchettes de compétences des adversaires, pour juger « pourquoi les meilleurs joueurs/équipes ».
3. **`/league/table`, onglets Équipes, Joueurs, Blessés, Transferts de la saison courante** — 4 pages, hebdomadaire (Transferts : quotidien) ; débloque : moyennes par équipe et par joueur sur 12 équipes/152 joueurs sans passer par les matchs.
4. **Classement des 3 autres ligues** (`/league/table` par ligue) — 3 pages, hebdomadaire ; débloque : comparer le haut et le reste dans plusieurs ligues (augmente n).
5. **Matchs de coupe** (`/cup/<id>`) — selon le tableau ; apport faible pour les failles de ligue (compétition différente, 1 tactique).
6. **Test pour savoir si les tactiques adverses existent** : ouvrir l'écran de tactiques d'un match terminé d'une autre équipe et exporter ; 1 page, une fois. Je ne sais pas si le jeu les expose ; si la page reste vide, la donnée n'existe pas pour nous.
7. **`/c/<club>`, onglets Calendrier/Face-à-face/historique** — 11 pages ×3, une fois ; apport faible (résultats déjà dans le classement).

## Points non vérifiés

- Contenu de `best-five`, `standings_schedule` (DOM), `/world`, `/competition/cups` : non ouverts.
- Formule de `club_strength` et signification de `entry_direction` : je ne sais pas.
- Pourquoi 54 équipes au lieu de 55 dans `silver.bv_standings_weekly` : non vérifié.
- Les `schedule` de zirmunai et vigolana-basket (20/10) n'ont pas été ouverts.

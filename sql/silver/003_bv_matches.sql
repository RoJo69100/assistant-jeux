-- Silver BasketVibe : matchs, stats par joueur, play-by-play, tactique jouée.
-- Sources bronze (page /match/<id>) :
--   /fixtures/<id>/preview             → en-tête du match + box score du match complet
--   /fixtures/<id>/period-box?period=N → box score par quart-temps
--   /fixtures/<id>/play-by-play        → événements
--   /fixtures/<id>/match-tactics-used  → tactique jouée
-- Pour chaque match, la dernière capture l'emporte.

-- bv_api garde maintenant la query string (period=N pour les box scores par quart-temps).
create or replace view silver.bv_api with (security_invoker = true) as
select r.id as capture_id,
       r.captured_at,
       (r.captured_at at time zone 'Europe/Paris')::date as day,
       regexp_replace(split_part(r.source_url, '?', 1), '^https://(www\.)?basketvibe\.com/api/v1', '') as endpoint,
       substring(r.source_url from '/teams/([0-9a-f-]{36})') as team_id,
       r.payload->'body' as body,
       nullif(split_part(r.source_url, '?', 2), '') as query
from bronze.raw_pages r
where r.game = 'basketvibe' and r.source = 'api' and (r.payload->>'status')::int = 200;

-- Mon équipe (club_id de /auth/me = id d'équipe).
create or replace view silver.bv_my_team with (security_invoker = true) as
select (a.body->>'club_id')::uuid as team_id, a.body->>'username' as manager
from silver.bv_api a
where a.endpoint = '/auth/me'
order by a.captured_at desc
limit 1;

create or replace view silver.bv_fixture_api with (security_invoker = true) as
select a.*,
       (substring(a.endpoint from '^/fixtures/([0-9a-f-]{36})/'))::uuid as fixture_id,
       substring(a.endpoint from '^/fixtures/[0-9a-f-]{36}/(.+)$') as part
from silver.bv_api a
where a.endpoint ~ '^/fixtures/[0-9a-f-]{36}/';

create or replace view silver.bv_matches with (security_invoker = true) as
select distinct on (f.fixture_id)
       f.fixture_id,
       (b->>'match_id')::uuid           as match_id,
       (b->>'season_id')::uuid          as season_id,
       (b->>'league_id')::uuid          as league_id,
       (b->>'round_number')::int        as round_number,
       (b->>'match_day')::date          as match_day,
       b->>'kickoff_time'               as kickoff_time,
       b->>'kind'                       as status,
       (b->>'is_walkover')::bool        as is_walkover,
       (b->'home_team'->>'id')::uuid    as home_team_id,
       b->'home_team'->>'name'          as home_team,
       (b->'away_team'->>'id')::uuid    as away_team_id,
       b->'away_team'->>'name'          as away_team,
       (b->>'home_score')::int          as home_score,
       (b->>'away_score')::int          as away_score,
       (b->>'overtime_periods')::int    as overtime_periods,
       (b->>'attendance')::int          as attendance,
       (b->>'ticket_revenue')::numeric  as ticket_revenue,
       case m.team_id when (b->'home_team'->>'id')::uuid then 'home'
                      when (b->'away_team'->>'id')::uuid then 'away' end as my_side,
       case when m.team_id not in ((b->'home_team'->>'id')::uuid, (b->'away_team'->>'id')::uuid) then null
            when ((b->>'home_score')::int > (b->>'away_score')::int) = (m.team_id = (b->'home_team'->>'id')::uuid) then 'W'
            else 'L' end                as my_result,
       b->'quarter_scores'              as quarter_scores,
       b->'player_of_game'              as player_of_game,
       f.captured_at
from silver.bv_fixture_api f
cross join lateral (select f.body as b) x
left join silver.bv_my_team m on true
where f.part = 'preview'
order by f.fixture_id, f.captured_at desc;

-- Box score : period = 0 pour le match complet (preview), 1..4 (+ prolongations) par quart-temps.
create or replace view silver.bv_match_player_stats with (security_invoker = true) as
with src as (
  select distinct on (f.fixture_id, period)
         f.fixture_id, f.body,
         case when f.part = 'preview' then 0
              else (substring(f.query from 'period=(\d+)'))::int end as period
  from silver.bv_fixture_api f
  where f.part = 'preview' or (f.part = 'period-box' and f.query ~ 'period=\d+')
  order by f.fixture_id, period, f.captured_at desc
)
select s.fixture_id,
       s.period,
       (p->>'player_id')::uuid               as player_id,
       p->>'first_name' || ' ' || (p->>'last_name') as name,
       p->>'team_side'                       as team_side,
       p->>'position'                        as position,
       (p->>'min')::numeric                  as min,
       (p->>'pts')::int  as pts,
       (p->>'fgm')::int  as fgm,  (p->>'fga')::int  as fga,
       (p->>'fg3m')::int as fg3m, (p->>'fg3a')::int as fg3a,
       (p->>'ftm')::int  as ftm,  (p->>'fta')::int  as fta,
       (p->>'oreb')::int as oreb, (p->>'dreb')::int as dreb,
       (p->>'oreb')::int + (p->>'dreb')::int as reb,
       (p->>'ast')::int  as ast,  (p->>'stl')::int  as stl,
       (p->>'blk')::int  as blk,  (p->>'tov')::int  as tov,
       (p->>'pf')::int   as pf,
       (p->>'plus_minus')::int               as plus_minus,
       (p->>'eval')::numeric                 as eval
from src s, jsonb_array_elements(s.body->'players') p;

create or replace view silver.bv_match_events with (security_invoker = true) as
with src as (
  select distinct on (f.fixture_id) f.fixture_id, f.body
  from silver.bv_fixture_api f
  where f.part = 'play-by-play'
  order by f.fixture_id, f.captured_at desc
)
select s.fixture_id,
       (e->>'seq')::int                      as seq,
       (e->>'period')::int                   as period,
       e->>'clock_display'                   as clock,
       e->>'team_side'                       as team_side,
       e->>'event_kind'                      as kind,
       e->>'message_key'                     as detail,
       (e->'payload'->'player_ids'->>0)::uuid as player_id,
       (e->'payload'->'player_ids'->>1)::uuid as player2_id,
       (e->>'home_score')::int               as home_score,
       (e->>'away_score')::int               as away_score,
       (e->'payload'->>'is_three')::bool     as is_three,
       (e->'payload'->>'sx')::int            as shot_x,
       (e->'payload'->>'sy')::int            as shot_y,
       e->'payload'                          as payload
from src s, jsonb_array_elements(s.body->'play_by_play') e;

create or replace view silver.bv_match_tactics with (security_invoker = true) as
select distinct on (f.fixture_id, f.body->>'primary_team_id')
       f.fixture_id,
       (f.body->>'primary_team_id')::uuid   as team_id,
       f.body->>'primary_team_name'         as team,
       (f.body->>'opponent_team_id')::uuid  as opponent_id,
       f.body->>'opponent_team_name'        as opponent,
       f.body->'defensive_focus'            as defensive_focus,
       f.body->'lineup_by_quarter'          as lineup_by_quarter,
       f.body->'opponent_lineup_by_quarter' as opponent_lineup_by_quarter,
       f.body->'players'                    as player_directives
from silver.bv_fixture_api f
where f.part = 'match-tactics-used'
order by f.fixture_id, f.body->>'primary_team_id', f.captured_at desc;

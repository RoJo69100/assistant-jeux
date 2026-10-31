-- Correctif 2026-10-31 : silver.sz_matches perdait round, competition ('league') et, sans événement, adversaire et domicile/extérieur
-- pour tous les matchs de la saison écoulée, car silver.sz_fixtures ne lit que la DERNIÈRE capture de /seasons/current/my-competition
-- (au changement de saison, les fixtures anciens disparaissent). 2 matchs (24-20 W contre FC Cete, 30-32 L contre HC Roslund,
-- sans événement /teams/mine/events) n'avaient plus d'adversaire.
-- Correctif : silver.sz_fixtures_all = dernière capture connue de CHAQUE match (toutes saisons), utilisée par sz_matches.
-- silver.sz_fixtures reste la saison courante (agenda, classement).
create or replace view silver.sz_fixtures_all with (security_invoker = true) as
select distinct on (f->>'matchId')
       a.day, (f->>'round')::int as round, (f->>'matchId')::uuid as match_id, f->>'status' as status,
       f->>'homeTeamName' as home_team, f->>'awayTeamName' as away_team,
       (f->>'homeTeamId')::uuid as home_team_id, (f->>'awayTeamId')::uuid as away_team_id,
       (f->>'homeTeamIsBot')::bool as home_is_bot, (f->>'awayTeamIsBot')::bool as away_is_bot
from silver.sz_api a
cross join lateral jsonb_array_elements(a.body->'rounds') r
cross join lateral jsonb_array_elements(r->'fixtures') f
where a.endpoint = '/seasons/current/my-competition'
order by f->>'matchId', a.captured_at desc;

-- sz_matches : identique à 020_sz_matches_cup_and_day.sql, sauf « left join silver.sz_fixtures_all f ».
create or replace view silver.sz_matches with (security_invoker = true) as
with me as (select team_id from silver.sz_my_team),
t as (
  select r.match_id, r.captured_at, r.day, (x->>'teamId')::uuid as team_id, x
  from silver.sz_match_stats_raw r, jsonb_array_elements(r.body->'teams') x
),
ev as (
  select distinct on (e->'data'->>'matchId')
         (e->'data'->>'matchId')::uuid as match_id, (e->>'at')::timestamptz as played_at,
         (e->'data'->>'home')::boolean as home, e->'data'->>'opponentName' as opponent
  from silver.sz_api a, jsonb_array_elements(a.body) e
  where a.endpoint = '/teams/mine/events' and e->>'type' = 'match_result'
  order by e->'data'->>'matchId', a.captured_at desc
),
cup as (
  select distinct (tie->>'matchId')::uuid as match_id
  from silver.sz_api a, jsonb_array_elements(a.body->'rounds') r, jsonb_array_elements(r->'ties') tie
  where a.endpoint = '/cups/current' and tie->>'matchId' is not null
)
select mine.match_id, mine.captured_at, mine.day as captured_day,
       (ev.played_at at time zone 'Europe/Paris')::date as match_day, f.round,
       case when f.home_team_id = me.team_id then 'home' when f.away_team_id = me.team_id then 'away'
            when ev.home then 'home' when not ev.home then 'away' end as venue,
       coalesce(case when f.home_team_id = me.team_id then f.away_team else f.home_team end, ev.opponent) as opponent,
       case when f.home_team_id = me.team_id then f.away_is_bot else f.home_is_bot end as opponent_is_bot,
       (mine.x->>'goals')::int as goals, (opp.x->>'goals')::int as opp_goals,
       case when (mine.x->>'goals')::int > (opp.x->>'goals')::int then 'W'
            when (mine.x->>'goals')::int < (opp.x->>'goals')::int then 'L' else 'D' end as result,
       (mine.x->>'shots')::int as shots, (opp.x->>'shots')::int as opp_shots,
       (mine.x->>'shotsOnTarget')::int as shots_on_target, (opp.x->>'shotsOnTarget')::int as opp_shots_on_target,
       round(100.0 * (mine.x->>'goals')::int / nullif((mine.x->>'shots')::int, 0), 1) as shot_pct,
       round(100.0 * (opp.x->>'goals')::int / nullif((opp.x->>'shots')::int, 0), 1) as opp_shot_pct,
       (mine.x->>'saves')::int as saves, (opp.x->>'saves')::int as opp_saves,
       round(100.0 * (mine.x->>'saves')::int / nullif((opp.x->>'shotsOnTarget')::int, 0), 1) as save_pct,
       round(100.0 * (opp.x->>'saves')::int / nullif((mine.x->>'shotsOnTarget')::int, 0), 1) as opp_save_pct,
       (mine.x->>'turnovers')::int as turnovers, (opp.x->>'turnovers')::int as opp_turnovers,
       (mine.x->>'steals')::int as steals, (opp.x->>'steals')::int as opp_steals,
       (mine.x->>'blocks')::int as blocks, (opp.x->>'blocks')::int as opp_blocks,
       (mine.x->>'exclusions')::int as exclusions, (opp.x->>'exclusions')::int as opp_exclusions,
       (mine.x->>'yellowCards')::int as yellow_cards, (opp.x->>'yellowCards')::int as opp_yellow_cards,
       (mine.x->>'redCards')::int as red_cards, (opp.x->>'redCards')::int as opp_red_cards,
       (mine.x->>'sevenMeterGoals')::int as seven_m_goals, (mine.x->>'sevenMeterShots')::int as seven_m_shots,
       (opp.x->>'sevenMeterGoals')::int as opp_seven_m_goals, (opp.x->>'sevenMeterShots')::int as opp_seven_m_shots,
       (mine.x->>'possessionSeconds')::int as possession_s, (opp.x->>'possessionSeconds')::int as opp_possession_s,
       case when f.match_id is not null then 'league' when cup.match_id is not null then 'cup' end as competition,
       ev.played_at
from t mine
cross join me
join t opp on opp.match_id = mine.match_id and opp.team_id <> mine.team_id
left join silver.sz_fixtures_all f on f.match_id = mine.match_id
left join ev on ev.match_id = mine.match_id
left join cup on cup.match_id = mine.match_id
where mine.team_id = me.team_id;

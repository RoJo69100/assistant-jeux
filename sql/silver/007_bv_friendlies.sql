-- Silver BasketVibe : les amicaux (page /friendly/<id>, API /friendlies/<id>/...) rejoignent les vues de match.
-- Même format que la ligue ; seul le préfixe d'URL change. Colonne `competition` : 'league' ou 'friendly'.
-- Les amicaux ont round_number = 0 dans l'API : mis à null.

create or replace view silver.bv_fixture_api with (security_invoker = true) as
select a.*,
       (substring(a.endpoint from '^/(?:fixtures|friendlies)/([0-9a-f-]{36})/'))::uuid as fixture_id,
       substring(a.endpoint from '^/(?:fixtures|friendlies)/[0-9a-f-]{36}/(.+)$') as part,
       case when a.endpoint like '/friendlies/%' then 'friendly' else 'league' end as competition
from silver.bv_api a
where a.endpoint ~ '^/(fixtures|friendlies)/[0-9a-f-]{36}/';

create or replace view silver.bv_matches with (security_invoker = true) as
select distinct on (f.fixture_id)
       f.fixture_id,
       (b->>'match_id')::uuid           as match_id,
       (b->>'season_id')::uuid          as season_id,
       (b->>'league_id')::uuid          as league_id,
       nullif((b->>'round_number')::int, 0) as round_number,
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
       f.captured_at,
       f.competition
from silver.bv_fixture_api f
cross join lateral (select f.body as b) x
left join silver.bv_my_team m on true
where f.part = 'preview'
order by f.fixture_id, f.captured_at desc;

-- Gold : les totaux gardent la compétition ; les tendances restent sur la ligue
-- (en amical : fatigue et expérience à 1/10, rotation différente — pas comparable).
create or replace view gold.bv_match_team_totals with (security_invoker = true) as
select m.fixture_id, m.match_day, m.my_result,
       s.is_mine,
       sum(s.pts) pts, sum(s.fgm) fgm, sum(s.fga) fga, sum(s.fg3m) fg3m, sum(s.fg3a) fg3a,
       sum(s.ftm) ftm, sum(s.fta) fta, sum(s.oreb) oreb, sum(s.dreb) dreb, sum(s.reb) reb,
       sum(s.ast) ast, sum(s.tov) tov, sum(s.stl) stl, sum(s.blk) blk, sum(s.pf) pf,
       m.competition
from silver.bv_matches m
join silver.bv_match_player_stats s using (fixture_id)
where s.period = 0 and m.my_side is not null and m.status = 'finished'
group by m.fixture_id, m.match_day, m.my_result, s.is_mine, m.competition;

create or replace view gold.bv_match_trends with (security_invoker = true) as
with ranked as (
  select t.*, dense_rank() over (order by t.match_day desc, t.fixture_id) as recency
  from gold.bv_match_team_totals t
  where t.competition = 'league'
),
w as (select unnest(array[5, 10]) as last_n)
select w.last_n,
       count(distinct r.fixture_id)                                         as matches,
       count(distinct r.fixture_id) filter (where r.my_result = 'W')         as wins,
       case when r.is_mine then 'moi' else 'adversaires' end                as side,
       round(avg(r.pts), 1) pts,
       round(100.0 * sum(r.fgm) / nullif(sum(r.fga), 0), 1)                 as fg_pct,
       round(avg(r.fg3a), 1) fg3a,
       round(100.0 * sum(r.fg3m) / nullif(sum(r.fg3a), 0), 1)               as fg3_pct,
       round(avg(r.fta), 1) fta,
       round(100.0 * sum(r.ftm) / nullif(sum(r.fta), 0), 1)                 as ft_pct,
       round(avg(r.oreb), 1) oreb, round(avg(r.dreb), 1) dreb, round(avg(r.reb), 1) reb,
       round(avg(r.ast), 1) ast, round(avg(r.tov), 1) tov,
       round(avg(r.stl), 1) stl, round(avg(r.blk), 1) blk, round(avg(r.pf), 1) pf
from w
join ranked r on r.recency <= w.last_n
group by w.last_n, r.is_mine
order by w.last_n, r.is_mine desc;

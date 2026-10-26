-- B1 (rétro 2026-10-24) : un match sans score (non joué, programmé) tombait dans le ELSE 'L'.
-- my_result = NULL tant que home_score ou away_score est NULL. Même colonnes, même ordre.
create or replace view silver.bv_matches with (security_invoker = true) as
select distinct on (f.fixture_id) f.fixture_id,
       (x.b ->> 'match_id')::uuid             as match_id,
       (x.b ->> 'season_id')::uuid            as season_id,
       (x.b ->> 'league_id')::uuid            as league_id,
       nullif((x.b ->> 'round_number')::int, 0) as round_number,
       (x.b ->> 'match_day')::date            as match_day,
       x.b ->> 'kickoff_time'                 as kickoff_time,
       x.b ->> 'kind'                         as status,
       (x.b ->> 'is_walkover')::boolean       as is_walkover,
       (x.b -> 'home_team' ->> 'id')::uuid    as home_team_id,
       x.b -> 'home_team' ->> 'name'          as home_team,
       (x.b -> 'away_team' ->> 'id')::uuid    as away_team_id,
       x.b -> 'away_team' ->> 'name'          as away_team,
       (x.b ->> 'home_score')::int            as home_score,
       (x.b ->> 'away_score')::int            as away_score,
       (x.b ->> 'overtime_periods')::int      as overtime_periods,
       (x.b ->> 'attendance')::int            as attendance,
       (x.b ->> 'ticket_revenue')::numeric    as ticket_revenue,
       case m.team_id when (x.b -> 'home_team' ->> 'id')::uuid then 'home'
                      when (x.b -> 'away_team' ->> 'id')::uuid then 'away' end as my_side,
       case when m.team_id <> (x.b -> 'home_team' ->> 'id')::uuid
             and m.team_id <> (x.b -> 'away_team' ->> 'id')::uuid then null
            when x.b ->> 'home_score' is null or x.b ->> 'away_score' is null then null
            when ((x.b ->> 'home_score')::int > (x.b ->> 'away_score')::int)
                 = (m.team_id = (x.b -> 'home_team' ->> 'id')::uuid) then 'W'
            else 'L' end                      as my_result,
       x.b -> 'quarter_scores'                as quarter_scores,
       x.b -> 'player_of_game'                as player_of_game,
       f.captured_at,
       f.competition
from silver.bv_fixture_api f
cross join lateral (select f.body as b) x
left join silver.bv_my_team m on true
where f.part = 'preview'
order by f.fixture_id, f.captured_at desc;

-- Règle 15 (rétro 2026-10-24) : test à relancer après toute modification d'une vue de résultat.
-- Doit renvoyer 0 ligne.
-- select fixture_id, status, home_score, away_score, my_result from silver.bv_matches
-- where my_result is not null and (home_score is null or away_score is null);

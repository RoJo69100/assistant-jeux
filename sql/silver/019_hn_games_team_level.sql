-- B5 (rétro 2026-10-24) : home_is_mine couvre les 4 équipes (PRO, FRM, U21, U17), bilans mélangés.
-- Ajout en fin de vue : team_level (niveau de mon équipe dans le match, champ teams.<côté>.level)
-- et my_result (W/L, NULL si non joué ou pas mon match — règle 15).
create or replace view silver.hn_games with (security_invoker = true) as
select distinct on (g.value ->> 'id') (g.value ->> 'id')::uuid as game_id,
       g.value ->> 'type'                                as game_type,
       (g.value ->> 'day')::int                          as season_day,
       (g.value ->> 'scheduledAt')::timestamptz          as scheduled_at,
       g.value ->> 'status'                              as status,
       (g.value -> 'teams' -> 'home' ->> 'city') || ' ' || (g.value -> 'teams' -> 'home' ->> 'nickname') as home,
       (g.value -> 'teams' -> 'away' ->> 'city') || ' ' || (g.value -> 'teams' -> 'away' ->> 'nickname') as away,
       (g.value ->> 'homeScore')::int                    as home_score,
       (g.value ->> 'awayScore')::int                    as away_score,
       g.value -> 'winner'                               as winner,
       coalesce((g.value -> 'teams' -> 'home' ->> 'own')::boolean, false) as home_is_mine,
       coalesce((g.value -> 'teams' -> 'away' ->> 'own')::boolean, false) as away_is_mine,
       g.value -> 'teams'                                as teams,
       a.captured_at,
       case when (g.value -> 'teams' -> 'home' ->> 'own')::boolean then g.value -> 'teams' -> 'home' ->> 'level'
            when (g.value -> 'teams' -> 'away' ->> 'own')::boolean then g.value -> 'teams' -> 'away' ->> 'level' end as team_level,
       case when g.value ->> 'homeScore' is null or g.value ->> 'awayScore' is null then null
            when coalesce((g.value -> 'teams' -> 'home' ->> 'own')::boolean, false)
                 then case when (g.value ->> 'homeScore')::int > (g.value ->> 'awayScore')::int then 'W' else 'L' end
            when coalesce((g.value -> 'teams' -> 'away' ->> 'own')::boolean, false)
                 then case when (g.value ->> 'awayScore')::int > (g.value ->> 'homeScore')::int then 'W' else 'L' end
       end                                               as my_result
from silver.hn_api a,
     lateral jsonb_array_elements(a.body) g(value)
where a.route = any (array['/team/:id/schedule', '/club/:id/game-overview'])
order by (g.value ->> 'id'), a.captured_at desc;

-- Test règle 15 (doit renvoyer 0 ligne) :
-- select game_id, status, home_score, away_score, my_result from silver.hn_games
-- where my_result is not null and (home_score is null or away_score is null);

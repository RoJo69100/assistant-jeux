-- 27/11 : team_level vide pour PRO J32 et J33 : la dernière capture de ces matchs (/club/:id/game-overview)
-- n'a pas le champ teams.<côté>.level. Repli : niveau de notre équipe lu dans ses rosters (/team/:id/roster, body.level).
-- Seule la colonne team_level change (coalesce) ; colonnes, ordre et lignes identiques à 019.
create or replace view silver.hn_games with (security_invoker = true) as
with niv as (
  select distinct on (a.body->>'id') a.body->>'id' as team_id, a.body->>'level' as lvl
  from silver.hn_api a
  where a.route = '/team/:id/roster' and a.body->>'level' is not null
  order by a.body->>'id', a.captured_at desc
)
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
       case when (g.value -> 'teams' -> 'home' ->> 'own')::boolean
                 then coalesce(g.value -> 'teams' -> 'home' ->> 'level',
                               (select n.lvl from niv n where n.team_id = g.value -> 'teams' -> 'home' ->> 'id'))
            when (g.value -> 'teams' -> 'away' ->> 'own')::boolean
                 then coalesce(g.value -> 'teams' -> 'away' ->> 'level',
                               (select n.lvl from niv n where n.team_id = g.value -> 'teams' -> 'away' ->> 'id')) end as team_level,
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

-- Test (27/11, doit renvoyer PRO pour les deux) :
-- select game_id, team_level from silver.hn_games
-- where game_id in ('2b841297-7a8b-4864-b988-b740bf466255', '6dcc6508-efe1-4e8b-b21a-763f0d390672');

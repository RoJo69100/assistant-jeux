-- Team Soccer : matchs « admin » (is_admin_match) programmés puis retirés du calendrier par le jeu.
-- Cas du 2026-11-01 : Chomelix – ChispasFC22 (1970802, 02/11 05:00) et Madureira EC (1970772, 1970788, 09/11),
-- vus pour la dernière fois le 27/10, absents de tous les exports suivants, mais toujours dans gold.ts_upcoming,
-- gold.ts_agenda et gold.ts_daily_alerts (« composition non enregistrée », 🟥 à tort).
-- Les matchs admin se jouent parfois (4 joués, dont Ajax le 26/10) : on ne les exclut pas tous, seulement
-- ceux encore « scheduled » qu'aucun export n'a revus depuis 48 h. Colonnes ajoutées : is_admin, last_seen.
create or replace view silver.ts_matches as
with rows as (
  select a.captured_at,
         x.value || jsonb_strip_nulls(jsonb_build_object(
           'series_id', case when not x.value ? 'series_id' then a.q_series_id else null::integer end,
           'cup_id',    case when not x.value ? 'cup_id'    then a.q_cup_id    else null::integer end)) as x
  from silver.ts_api a, lateral jsonb_array_elements(a.body) x(value)
  where a.endpoint = 'matches' and x.value ? 'match_id_int'
), kv as (
  select distinct on (((rows.x ->> 'match_id_int')::bigint), e.key)
         (rows.x ->> 'match_id_int')::bigint as match_id, e.key, e.value, rows.captured_at
  from rows, lateral jsonb_each(rows.x) e(key, value)
  where e.value <> 'null'::jsonb
  order by ((rows.x ->> 'match_id_int')::bigint), e.key, rows.captured_at desc
), m as (
  -- last_seen pris dans kv : un 2e passage sur rows le matérialisait et faisait expirer gold.ts_daily_alerts.
  select kv.match_id, jsonb_object_agg(kv.key, kv.value) as j, max(kv.captured_at) as last_seen
  from kv group by kv.match_id
)
select m.match_id,
       (m.j ->> 'match_date')::timestamptz as match_date,
       ((m.j ->> 'match_date')::timestamptz at time zone 'Europe/Paris') as match_date_paris,
       m.j ->> 'status' as status,
       (m.j ->> 'home_team_id')::integer as home_team_id,
       (m.j ->> 'away_team_id')::integer as away_team_id,
       ht.name as home_team,
       at.name as away_team,
       (m.j ->> 'home_score')::integer as home_score,
       (m.j ->> 'away_score')::integer as away_score,
       (m.j ->> 'home_penalties')::integer as home_penalties,
       (m.j ->> 'away_penalties')::integer as away_penalties,
       (m.j ->> 'series_id')::integer as series_id,
       (m.j ->> 'cup_id')::integer as cup_id,
       (m.j ->> 'cup_round')::integer as cup_round,
       case when (m.j ->> 'is_friendly')::boolean then 'amical'
            when (m.j ->> 'is_promotion')::boolean then 'barrage'
            when m.j ? 'cup_id' then 'coupe'
            when m.j ? 'series_id' then 'ligue'
            when m.j ? 'custom_tournament_id' or m.j ? 'room_challenge_id' then 'autre'
            else 'inconnu' end as competition,
       mine.team_id as my_team_id,
       case when mine.team_id = (m.j ->> 'home_team_id')::integer then 'domicile'
            when mine.team_id is not null then 'extérieur' end as venue,
       coalesce((m.j ->> 'is_admin_match')::boolean, false) as is_admin,
       m.last_seen
from m
left join silver.ts_teams ht on ht.team_id = (m.j ->> 'home_team_id')::integer
left join silver.ts_teams at on at.team_id = (m.j ->> 'away_team_id')::integer
left join silver.ts_my_teams mine on mine.team_id = (m.j ->> 'home_team_id')::integer
                                  or mine.team_id = (m.j ->> 'away_team_id')::integer
where not (coalesce((m.j ->> 'is_admin_match')::boolean, false)
           and m.j ->> 'status' = 'scheduled'
           and m.last_seen < now() - interval '48 hours');

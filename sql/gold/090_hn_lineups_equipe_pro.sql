-- Hockey Nation (2026-11-25) : silver.hn_lineups lisait le dernier export /team/:id/lineups de N'IMPORTE QUELLE équipe.
-- Le 25/11, deux exports d'équipes qui ne sont pas les nôtres (11:00:05 vide, 10:59:59) passaient après celui du PRO (10:59:53) :
-- la lineup PRO paraissait vide (57 cases « à saisir »). La vue ne lit plus que le dernier export de l'équipe PRO (silver.hn_my_teams).
-- Même colonnes, même règle « dernier export seulement » (034_hn_tactique.sql).

create or replace view silver.hn_lineups as
with pro as (select team_id::text as team_id from silver.hn_my_teams where level = 'PRO' limit 1),
dernier as (
  select max(a.captured_at) as captured_at from silver.hn_api a, pro
  where a.route = '/team/:id/lineups' and a.endpoint = '/team/' || pro.team_id || '/lineups')
select distinct on ((l.value ->> 'id'), ln.key, pos.key)
       a.day, (l.value ->> 'id') as lineup, ln.key as line, pos.key as slot,
       ((pos.value #>> '{}'))::uuid as player_id, (l.value -> 'gameplan') as gameplan
from silver.hn_api a cross join pro cross join dernier,
     lateral jsonb_array_elements(a.body) l(value),
     lateral jsonb_each(l.value -> 'lines') ln(key, value), lateral jsonb_each(ln.value) pos(key, value)
where a.route = '/team/:id/lineups' and a.endpoint = '/team/' || pro.team_id || '/lineups'
  and jsonb_typeof(pos.value) = 'string' and a.captured_at = dernier.captured_at
order by (l.value ->> 'id'), ln.key, pos.key, a.captured_at desc;

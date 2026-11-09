-- Étape 5h, N1 (docs/refonte-v3/journal-aujourdhui.md) : gold.bv_zone_jouee lit la zone défensive des réglages
-- utilisés (`match-tactics-used`, via silver.bv_match_tactics) quand le match est joué, et la page d'avant-match
-- (`match-tactics`) seulement pour un match à venir ou sans réglages utilisés. Remplace 025_bv_zone_jouee.sql
-- (erreur du 09/11 : Middle d'après la page du 08/11, Perimeter joué). Colonnes d'origine inchangées, `source` ajoutée.
-- area_step : 1 Perimeter, 3 Middle, 5 Rim. Valeur unique si tous les adversaires ont la même zone, sinon 'mixte'.
create or replace view gold.bv_zone_jouee with (security_invoker = true) as
with avant as (  -- dernière page d'avant-match par match
  select distinct on (f.fixture_id) f.fixture_id, f.competition, f.captured_at, f.body
  from silver.bv_fixture_api f
  where f.part = 'match-tactics'
  order by f.fixture_id, f.captured_at desc
),
joue as (  -- réglages utilisés de notre équipe, match fini seulement
  select t.fixture_id, m.competition, t.defensive_focus,
         (select max(f.captured_at) from silver.bv_fixture_api f
          where f.fixture_id = t.fixture_id and f.part = 'match-tactics-used') as captured_at
  from silver.bv_match_tactics t
  join silver.bv_my_team me on me.team_id = t.team_id
  join silver.bv_matches m on m.fixture_id = t.fixture_id and m.status = 'finished'
),
src as (
  select coalesce(j.fixture_id, a.fixture_id) as fixture_id,
         coalesce(j.competition, a.competition) as competition,
         coalesce(j.captured_at, a.captured_at) as captured_at,
         (a.body ->> 'has_saved_match_tactics')::boolean as sauvegarde_match,
         coalesce(j.defensive_focus, a.body -> 'defensive_focus') as defensive_focus,
         case when j.fixture_id is not null then 'reglages_utilises' else 'avant_match' end as source
  from joue j
  full join avant a on a.fixture_id = j.fixture_id
)
select s.fixture_id,
       s.competition,
       m.match_day,
       s.captured_at,
       s.sauvegarde_match,
       z.nb_adversaires,
       case when z.nb_zones = 1 then z.zone_min::text else 'mixte' end as area_step,
       case when z.nb_zones = 1 then (array['Perimeter','Perimeter','Middle','Middle','Rim'])[z.zone_min] else 'mixte' end as zone,
       s.source
from src s
left join silver.bv_matches m on m.fixture_id = s.fixture_id
cross join lateral (
    select count(*) as nb_adversaires,
           count(distinct (d ->> 'area_step')::int) as nb_zones,
           min((d ->> 'area_step')::int) as zone_min
    from jsonb_array_elements(s.defensive_focus) d
) z;

grant select on gold.bv_zone_jouee to assistant_ro;

-- Test : les amicaux des 07, 08 et 09/11 sortent en Perimeter (1), source reglages_utilises.
-- select m.match_day, z.zone, z.source from gold.bv_zone_jouee z join silver.bv_matches m using (fixture_id)
--   where m.competition = 'friendly' and m.match_day between '2026-11-07' and '2026-11-09' order by 1;

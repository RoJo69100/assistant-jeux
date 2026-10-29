-- Gold BasketVibe : zone défensive (Defensive area) réellement enregistrée par match, lue dans la dernière capture
-- `match-tactics` (page Tactics avant le match). Remplace la lecture de silver.bv_match_tactics, qui ne lit que
-- `match-tactics-used` (absent après le 26/10) : erreur L-024 du 27/10 (test Rim jugé à tort non valide).
-- area_step : 1 Perimeter, 3 Middle, 5 Rim. Valeur unique si les 12 adversaires ont la même zone, sinon 'mixte'.

create or replace view gold.bv_zone_jouee with (security_invoker = true) as
select distinct on (f.fixture_id)
       f.fixture_id,
       f.competition,
       m.match_day,
       f.captured_at,
       (f.body ->> 'has_saved_match_tactics')::boolean as sauvegarde_match,
       z.nb_adversaires,
       case when z.nb_zones = 1 then z.zone_min::text else 'mixte' end as area_step,
       case when z.nb_zones = 1 then (array['Perimeter','Perimeter','Middle','Middle','Rim'])[z.zone_min] else 'mixte' end as zone
from silver.bv_fixture_api f
left join silver.bv_matches m on m.fixture_id = f.fixture_id
cross join lateral (
    select count(*) as nb_adversaires,
           count(distinct (d ->> 'area_step')::int) as nb_zones,
           min((d ->> 'area_step')::int) as zone_min
    from jsonb_array_elements(f.body -> 'defensive_focus') d
) z
where f.part = 'match-tactics'
order by f.fixture_id, f.captured_at desc;

-- Test : l'amical du 27/10 doit sortir en area_step 5 (Rim), 12 adversaires.
-- select competition, match_day, area_step, zone, nb_adversaires, sauvegarde_match from gold.bv_zone_jouee order by match_day;

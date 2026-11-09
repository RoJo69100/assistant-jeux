-- Étape 5g, M2 (docs/refonte-v3/journal-aujourdhui.md) : réglage réellement joué par amical, lu dans la page
-- « réglages utilisés » (`match-tactics-used`) via silver.bv_match_tactics. Vue additive, lecture seule.
-- Sert à vérifier les amicaux de la file d'expériences (docs/attentes/experiences-amicales-basketvibe.yaml).
-- Crans de l'API (0-4) ; écran = cran + 1 (docs/fiches/basketvibe/match.md:19).
-- Joueurs comptés : ceux des cinq de Q1 à Q4 (la 5e case de lineup_by_quarter = prolongation, ignorée).
create or replace view gold.bv_amical_reglage with (security_invoker = true) as
with t as (
  select t.fixture_id, t.opponent, t.player_directives, t.lineup_by_quarter, t.defensive_focus
  from silver.bv_match_tactics t
  join silver.bv_my_team me on me.team_id = t.team_id
),
q as (  -- un joueur par quart-temps joué (Q1-Q4), avec ses consignes du match
  select t.fixture_id, q.i as quart, d
  from t
  cross join lateral jsonb_array_elements(t.lineup_by_quarter) with ordinality q(ids, i)
  cross join lateral jsonb_array_elements(t.player_directives) d
  where q.i <= 4 and q.ids ? (d ->> 'player_id')
),
j as (  -- niveau d'équipe sur les joueurs qui ont joué
  select fixture_id,
         count(distinct d ->> 'player_id') as joueurs,
         min((d ->> 'defense_tier')::int) as agress_min,
         max((d ->> 'defense_tier')::int) as agress_max,
         count(distinct d ->> 'player_id') filter (where (d ->> 'shot_tier')::int = 4) as tir_cran4_joueurs
  from q group by fixture_id
),
p as (  -- quarts-temps avec au moins un joueur au focus offensif Primary (cran 4) sur le terrain
  select fixture_id, count(distinct quart) filter (where (d ->> 'offensive_focus_tier')::int = 4) as primary_quarts,
         max((d ->> 'offensive_focus_tier')::int) as focus_off_max
  from q group by fixture_id
),
z as (
  select t.fixture_id,
         count(distinct (f ->> 'area_step')::int) as nb_zones,
         min((f ->> 'area_step')::int) as zone_min
  from t cross join lateral jsonb_array_elements(t.defensive_focus) f
  group by t.fixture_id
)
select m.fixture_id,
       m.match_day,
       t.opponent,
       m.my_result,
       j.joueurs,
       (j.agress_min = j.agress_max) as agress_uniforme,
       case when j.agress_min = j.agress_max then j.agress_min end as agress_cran,
       case when j.agress_min = j.agress_max then j.agress_min + 1 end as agress_ecran,
       j.agress_min, j.agress_max,
       p.primary_quarts,
       p.focus_off_max,
       j.tir_cran4_joueurs,
       case when z.nb_zones = 1 then (array['Perimeter','Perimeter','Middle','Middle','Rim'])[z.zone_min] else 'mixte' end as zone
from silver.bv_matches m
join t on t.fixture_id = m.fixture_id
join j on j.fixture_id = m.fixture_id
join p on p.fixture_id = m.fixture_id
left join z on z.fixture_id = m.fixture_id
where m.competition = 'friendly' and m.status = 'finished';

grant select on gold.bv_amical_reglage to assistant_ro;

-- Test : les amicaux des 07, 08 et 09/11 sortent en agressivité uniforme cran 0 (écran 1), 0 quart Primary, zone Perimeter.
-- select match_day, opponent, agress_uniforme, agress_ecran, primary_quarts, zone from gold.bv_amical_reglage order by match_day desc limit 3;

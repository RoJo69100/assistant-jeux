-- Hockey Nation (2026-10-29) : gold.hn_coach_options avec CTE matérialisées (la version 030 dépassait le délai).
-- Même logique que 030 : coachs arrivés par offre cette saison exclus, U17 = ok_u17, U21 = ok_u21, offres déjà envoyées exclues.
drop view if exists gold.hn_coach_options;
create view gold.hn_coach_options with (security_invoker = true) as
with fs as (
  select (x->'coach'->>'id') as coach_id, coalesce((x->'coach'->>'firstSeason')::bool, false) as first_season
  from (select body from silver.hn_api where route = '/coach-center/active-jobs' order by captured_at desc limit 1) a, jsonb_array_elements(a.body) x
), staff as (
  select k.key as team_level, c->>'id' as coach_id, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age,
         coalesce((c->'job'->>'head')::bool, false) as head,
         silver.hn_skill(c->'skills','OFP') + silver.hn_skill(c->'skills','DFP') + silver.hn_skill(c->'skills','BAT')
           + silver.hn_skill(c->'skills','PP') + silver.hn_skill(c->'skills','PK') as match_sum
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
), cand as materialized (
  select * from gold.hn_coach_candidats
), decl as materialized (
  select * from silver.hn_declared where kind = 'coach_offre'
)
select s.team_level, s.head, s.coach, s.age, s.match_sum,
       b.coach as meilleur_candidat, b.age as age_candidat, b.xp as xp_candidat, b.match_sum as somme_candidat,
       (b.match_sum - s.match_sum) * case when s.head then 2 else 1 end as gain_equipe,
       b.saisons_avant_retraite,
       (select string_agg(d.name || ' : ' || d.detail, ' ; ') from decl d where d.detail like '%' || s.coach || '%') as offre_en_cours
from staff s
left join fs on fs.coach_id = s.coach_id
left join lateral (
  select m.* from cand m
  where m.match_sum > s.match_sum and not m.offre_envoyee and m.age < 65
    and (s.team_level <> 'U17' or m.ok_u17) and (s.team_level <> 'U21' or m.ok_u21)
  order by m.match_sum desc, m.age limit 1
) b on true
where not coalesce(fs.first_season, false)
order by s.team_level, s.head desc, gain_equipe desc nulls last;

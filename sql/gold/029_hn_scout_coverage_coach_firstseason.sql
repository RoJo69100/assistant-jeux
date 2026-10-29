-- Hockey Nation (2026-10-29) : couverture des scouts (le but : faire repérer le plus de joueurs possible), priorité des candidats par joueurs
-- NOUVEAUX couverts, coachs non remplaçables = arrivés PAR OFFRE cette saison (firstSeason). Remplace hn_scout_priority et hn_coach_options de 027/028.

drop view if exists gold.hn_scout_priority;
create view gold.hn_scout_priority with (security_invoker = true) as
with cls as (
  select b.draft_rank as rang, b.main_position as pos, n.name as nation
  from gold.hn_draft_board b
  left join silver.hn_draft_class d on d.name = b.name and d.draft_rank = b.draft_rank
  left join silver.hn_nations n on n.nation_id = d.nation_id
  where b.season = (select max(season) from gold.hn_draft_board)
    and b.league_id = (select league_id from gold.hn_draft_board where from_my_u17 group by league_id order by count(*) desc limit 1)
), mine as (select preferred_position as pos, nation from silver.hn_scouts where day = (select max(day) from silver.hn_scouts)),
unc as (select * from cls where not exists (select 1 from mine m where m.pos = cls.pos or m.nation = cls.nation)),
apps as (
  select x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as scout, (x->'scout'->>'age')::int as age,
         x->'scout'->>'position' as pos, n.name as nation
  from (select body from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
       jsonb_array_elements(a.body->'applications') x
  left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid
)
select * from (
select a.scout, a.age, a.pos as poste, a.nation,
       (select count(*) from cls where cls.pos = a.pos and cls.nation = a.nation) as top_poste_nation,
       (select count(*) from cls where cls.pos = a.pos) as tous_poste,
       (select count(*) from cls where cls.nation = a.nation) as tous_nation,
       (select count(*) from unc where unc.pos = a.pos or unc.nation = a.nation) as nouveaux_joueurs_couverts,
       case when a.pos = 'G' then 'non : limite de draft G = 0'
            when (select count(*) from unc where unc.pos = a.pos or unc.nation = a.nation) = 0 then 'non : rien de nouveau'
            else 'oui' end as embaucher
from apps a) t
order by (embaucher = 'oui') desc, nouveaux_joueurs_couverts desc, top_poste_nation desc, age;

create or replace view gold.hn_scout_coverage with (security_invoker = true) as
with cls as (
  select b.draft_rank as rang, b.main_position as pos, n.name as nation
  from gold.hn_draft_board b
  left join silver.hn_draft_class d on d.name = b.name and d.draft_rank = b.draft_rank
  left join silver.hn_nations n on n.nation_id = d.nation_id
  where b.season = (select max(season) from gold.hn_draft_board)
    and b.league_id = (select league_id from gold.hn_draft_board where from_my_u17 group by league_id order by count(*) desc limit 1)
), sc as (select name as scout, preferred_position as pos, nation from silver.hn_scouts where day = (select max(day) from silver.hn_scouts))
select sc.scout, sc.pos as poste, sc.nation,
       (select count(*) from cls where cls.pos = sc.pos and cls.nation = sc.nation) as top_poste_nation,
       (select count(*) from cls where cls.pos = sc.pos) as tous_poste,
       (select count(*) from cls where cls.nation = sc.nation) as tous_nation,
       (select count(*) from cls where cls.pos = sc.pos or cls.nation = sc.nation) as total_couvert
from sc
union all
select 'TOUS (joueurs distincts)', null, null, null, null, null,
       (select count(*) from cls where exists (select 1 from sc where sc.pos = cls.pos or sc.nation = cls.nation));

drop view if exists gold.hn_coach_options;
create view gold.hn_coach_options with (security_invoker = true) as
with fs as (
  select (x->'coach'->>'id') as coach_id, coalesce((x->'coach'->>'firstSeason')::bool, false) as first_season
  from (select body from silver.hn_api where route = '/coach-center/active-jobs' order by captured_at desc limit 1) a, jsonb_array_elements(a.body) x
), staff as (
  select k.key as team_level, c->>'id' as coach_id, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age,
         coalesce((c->'job'->>'head')::bool, false) as head, (c->>'rating')::int as rating,
         silver.hn_skill(c->'skills','OFP') + silver.hn_skill(c->'skills','DFP') + silver.hn_skill(c->'skills','BAT')
           + silver.hn_skill(c->'skills','PP') + silver.hn_skill(c->'skills','PK') as match_sum
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
), market as (
  select name, age, rating, ofp, dfp, bat, pp, pk, ofp + dfp + bat + pp + pk as match_sum
  from silver.hn_free_coaches where day = (select max(day) from silver.hn_free_coaches) and coalesce(can_offer, true)
)
select s.team_level, s.head, s.coach, s.age, s.match_sum,
       b.name as meilleur_candidat, b.age as age_candidat, b.match_sum as somme_candidat,
       b.ofp || '-' || b.dfp || '-' || b.bat || '-' || b.pp || '-' || b.pk as ofp_dfp_bat_pp_pk,
       (b.match_sum - s.match_sum) * case when s.head then 2 else 1 end as gain_equipe,
       65 - s.age as saisons_avant_retraite
from staff s
left join fs on fs.coach_id = s.coach_id
left join lateral (
  select m.* from market m
  where m.match_sum > s.match_sum
    and (s.team_level <> 'U17' or m.rating <= 54) and (s.team_level <> 'U21' or m.rating <= 69)
    and m.age < 65
  order by m.match_sum desc, m.age limit 1
) b on true
where not coalesce(fs.first_season, false)
order by s.team_level, s.head desc, gain_equipe desc nulls last;

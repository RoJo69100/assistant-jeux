-- Hockey Nation : correctifs gold du 2026-10-25.
-- 1) gold.hn_draft_board gagne la saison de la classe (dernière colonne).
-- 2) gold.hn_cap_outlook commence à la saison en cours : plafond réel (salaryCap) moins salaires projetés du club
--    (totalProjectedSalary, rachats compris), puis les 4 saisons suivantes comme avant.

create or replace view gold.hn_draft_board with (security_invoker = true) as
select substring(d.endpoint from '/league/([^/]+)/')::uuid as league_id, d.draft_rank, d.name, d.main_position, d.age,
       d.rating, d.scouted_times, d.from_my_u17, d.u17_team,
       d.talents->'strongest' as talent_strongest, d.talents->>'weakest' as talent_weakest,
       case when d.talents is null then null else
         (select count(*) from jsonb_array_elements_text(d.talents->'strongest') t
           where exists (select 1 from gold.hn_position_keys k where k.position = d.main_position and k.skill = t)) end as talents_cles,
       case when d.talents is null then null else
         exists (select 1 from gold.hn_position_keys k where k.position = d.main_position and k.skill = d.talents->>'weakest') end as faible_cle,
       d.special_skill_count,
       (select count(*) from jsonb_array_elements(d.skills) s where s ? 'lvl') as skills_visible,
       case when d.from_my_u17 or d.scouted_times >= 3 then 'tout connu'
            when d.scouted_times = 2 then 'talents + 3-5 compétences'
            when d.scouted_times = 1 then 'note + talents'
            else 'non repéré' end as scouting_state,
       d.day, d.season
from silver.hn_draft_class d;

create or replace view gold.hn_cap_outlook with (security_invoker = true) as
with s as (select max(season) as season from silver.hn_season),
f as (select * from silver.hn_finances order by day desc limit 1),
c as (
  select ps.player_id, ps.name, (x->>'from')::int as from_s, (x->>'to')::int as to_s, (x->>'salary')::bigint as salary,
         coalesce((x->>'frm')::bool, false) as frm
  from (select distinct on (player_id) * from silver.hn_player_snapshots order by player_id, day desc, captured_at desc) ps,
       jsonb_array_elements(coalesce(ps.contracts, '[]'::jsonb)) x
), seasons as (select s.season + k as season, k from s, generate_series(0, 4) k)
select se.season,
       case when se.k = 0 then (f.salary_cap #>> '{}')::bigint
            when se.k = 1 then (f.salary_cap_projection->>'value')::bigint end as cap_projected,
       case when se.k = 0 then (f.total_projected_salary #>> '{}')::bigint
            else sum(c.salary) filter (where not c.frm) end as committed,
       count(*) filter (where not c.frm) as contracts,
       (select coalesce(sum((b->'salaries'->>se.k)::bigint), 0) from jsonb_array_elements(coalesce(f.buyouts, '[]'::jsonb)) b) as buyouts,
       case when se.k = 0 then (f.salary_cap #>> '{}')::bigint - (f.total_projected_salary #>> '{}')::bigint
            when se.k = 1 then (f.salary_cap_projection->>'value')::bigint - coalesce(sum(c.salary) filter (where not c.frm), 0)
            - (select coalesce(sum((b->'salaries'->>se.k)::bigint), 0) from jsonb_array_elements(coalesce(f.buyouts, '[]'::jsonb)) b) end as cap_space
from seasons se cross join f
left join c on se.season between c.from_s and c.to_s
group by se.season, se.k, f.salary_cap, f.salary_cap_projection, f.total_projected_salary, f.buyouts
order by se.season;

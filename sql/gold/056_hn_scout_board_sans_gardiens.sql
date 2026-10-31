-- 2026-10-31 : les gardiens ne comptent pas comme « nouveaux joueurs couverts » (limite de draft G = 0).
-- Cas Koelewijn : ses 3 « nouveaux » étaient 3 gardiens néerlandais, décision « oui » fausse.
create or replace view gold.hn_scout_board with (security_invoker = true) as
with h as (select * from gold.hn_scouts_effectifs),
apps as (
  select x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as scout, (x->'scout'->>'age')::int as age,
         x->'scout'->>'position' as pos, n.name as nation
  from (select body from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
       jsonb_array_elements(a.body->'applications') x
  left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid
), s as (
  select statut, scout, null::int as age, pos, nation from h
  union all
  select 'candidat', a.scout, a.age, a.pos, a.nation from apps a where a.scout not in (select scout from h)
)
select s.statut, s.scout, s.age, s.pos as poste, s.nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos and c.nation = s.nation) as top_poste_nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos) as tous_poste,
       (select count(*) from gold.hn_classe_draft c where c.nation = s.nation) as tous_nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos or c.nation = s.nation) as total_couvert,
       (select count(*) from gold.hn_classe_draft c
         where c.pos <> 'G' and (c.pos = s.pos or c.nation = s.nation)
           and not exists (select 1 from h where h.scout <> s.scout and (h.pos = c.pos or h.nation = c.nation))) as nouveaux_ou_uniques,
       case when s.statut <> 'candidat' then 'en poste'
            when s.pos = 'G' then 'non : limite de draft G = 0'
            when (select count(*) from gold.hn_classe_draft c
                  where c.pos <> 'G' and (c.pos = s.pos or c.nation = s.nation)
                    and not exists (select 1 from h where h.pos = c.pos or h.nation = c.nation)) = 0 then 'non : rien de nouveau (gardiens exclus)'
            else 'oui' end as decision
from s
order by (s.statut = 'candidat'), 10 desc, 6 desc, 3;

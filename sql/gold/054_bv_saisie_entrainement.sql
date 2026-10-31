-- BasketVibe : saisie de l'entraînement dans l'ordre de l'export (page /club/training).
-- Un joueur par ligne, ordre = ordre du tableau `players` du dernier export `training`.
-- Usage : select * from gold.bv_saisie_entrainement order by ordre;
-- Rendu (hook pipelines/forme.py) : tous les joueurs dans cet ordre avec leur entraînement, ou
-- seulement ceux qui changent si peu changent.
create or replace view gold.bv_saisie_entrainement with (security_invoker = true) as
with d as (
  select payload->'body'->'players' as joueurs, captured_at
  from bronze.raw_pages
  where game = 'basketvibe' and page_type = 'training'
  order by captured_at desc
  limit 1
)
select
  p.ordre::int as ordre,
  p.j->>'last_name' as nom,
  p.j->>'first_name' as prenom,
  p.j->>'position' as poste,
  (p.j->>'age')::int as age,
  p.j->>'primary_skill_id' as principale,
  p.j->>'secondary_skill_id' as secondaire,
  coalesce((p.j->>'is_academy_junior')::boolean, false) as junior_academie,
  d.captured_at as export_le
from d, jsonb_array_elements(d.joueurs) with ordinality as p(j, ordre);

-- Silver BasketVibe : la semaine suit l'entraînement (dimanche 04:00 Paris), plus le lundi.
-- week = dimanche du dernier entraînement passé : un relevé du dim. 18/10 au soir et un relevé du lun. 19/10 donnent tous deux week = 2026-10-18.
-- (Un relevé fait le dimanche entre 00:00 et 04:00, avant l'entraînement, serait compté à tort dans la nouvelle semaine : cas rare.)
--
-- 1. bv_player_daily : un relevé de la page Entraînement sans relevé Aperçu le même jour (cas du 22/11) n'est plus perdu.
--    Ses champs d'aperçu (forme, fatigue, PS…) viennent du dernier aperçu antérieur du joueur.
-- 2. bv_player_weekly : par joueur et par semaine, le dernier jour qui a les valeurs précises ;
--    à défaut seulement, le dernier jour tout court. Un relevé sans page Entraînement n'écrase jamais un relevé qui l'a.

--    Pas de jointure latérale : elle recalculait la vue JSON des aperçus pour chaque ligne (> 50 s).
--    Les CTE ov et tr, lues deux fois, sont matérialisées une seule fois ; le dernier aperçu antérieur
--    = max(jour d'aperçu) cumulé par joueur.
create or replace view silver.bv_player_daily with (security_invoker = true) as
with ov as (
  select day, player_id, team_id, capture_id, p from silver.bv_player_overview
),
tr as (
  select day, player_id, team_id, p from silver.bv_player_training
),
jours as (
  select player_id, team_id, day from ov
  union
  select player_id, team_id, day from tr
),
j as (
  select jj.player_id, jj.team_id, jj.day,
         max(o1.day) over (partition by jj.player_id order by jj.day) as o_day   -- dernier aperçu au plus tard ce jour
  from jours jj
  left join ov o1 on o1.player_id = jj.player_id and o1.day = jj.day
)
select j.day,
       j.player_id,
       j.team_id,
       o.p->>'first_name' || ' ' || (o.p->>'last_name') as name,
       o.p->>'position'                      as position,
       (o.p->>'age')::int                    as age,
       (o.p->>'form')::numeric               as form,
       (o.p->>'fatigue')::numeric            as fatigue,
       (o.p->>'experience')::int             as experience,
       (o.p->>'player_strength')::numeric    as ps,
       (o.p->>'injury_return_on')::date      as injury_return_on,
       o.p->>'skills_visibility'             as skills_visibility,
       (o.p->'stats'->>'two_point')::int     as two_point,
       (o.p->'stats'->>'three_point')::int   as three_point,
       (o.p->'stats'->>'defense')::int       as defense,
       (o.p->'stats'->>'passing')::int       as passing,
       (o.p->'stats'->>'ball_handling')::int as ball_handling,
       (o.p->'stats'->>'rebounding')::int    as rebounding,
       (o.p->'stats'->>'stamina')::int       as stamina,
       (o.p->'stats'->>'athleticism')::int   as athleticism,
       (t.p->'stats'->>'two_point')::numeric     as two_point_exact,
       (t.p->'stats'->>'three_point')::numeric   as three_point_exact,
       (t.p->'stats'->>'defense')::numeric       as defense_exact,
       (t.p->'stats'->>'passing')::numeric       as passing_exact,
       (t.p->'stats'->>'ball_handling')::numeric as ball_handling_exact,
       (t.p->'stats'->>'rebounding')::numeric    as rebounding_exact,
       (t.p->'stats'->>'stamina')::numeric       as stamina_exact,
       (t.p->'stats'->>'athleticism')::numeric   as athleticism_exact,
       t.p->>'primary_skill_id'                  as training_primary,
       t.p->>'secondary_skill_id'                as training_secondary,
       o.capture_id
from j
left join ov o on o.player_id = j.player_id and o.day = j.o_day
left join tr t on t.player_id = j.player_id and t.day = j.day;

create or replace view silver.bv_player_weekly with (security_invoker = true) as
select distinct on (d.player_id, (date_trunc('week', d.day + 1) - interval '1 day')::date)
       (date_trunc('week', d.day + 1) - interval '1 day')::date as week,
       d.*
from silver.bv_player_daily d
order by d.player_id, (date_trunc('week', d.day + 1) - interval '1 day')::date,
         (d.two_point_exact is not null) desc, d.day desc;

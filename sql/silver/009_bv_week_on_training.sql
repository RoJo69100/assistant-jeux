-- Silver BasketVibe : la semaine suit l'entraînement (dimanche 04:00 Paris), plus le lundi.
-- week = dimanche du dernier entraînement passé : un relevé du dim. 18/10 au soir et un relevé du lun. 19/10 donnent tous deux week = 2026-10-18.
-- (Un relevé fait le dimanche entre 00:00 et 04:00, avant l'entraînement, serait compté à tort dans la nouvelle semaine : cas rare.)

create or replace view silver.bv_player_weekly with (security_invoker = true) as
select distinct on (d.player_id, (date_trunc('week', d.day + 1) - interval '1 day')::date)
       (date_trunc('week', d.day + 1) - interval '1 day')::date as week,
       d.*
from silver.bv_player_daily d
order by d.player_id, (date_trunc('week', d.day + 1) - interval '1 day')::date, d.day desc;

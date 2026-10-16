-- Silver BasketVibe : relevé hebdomadaire et historique des entraînements.
-- L'entraînement tourne le dimanche à 04:00 (Paris) ; la routine est un export le lundi matin.
-- week = lundi de la semaine de capture (un export du lundi 19/10 donne week = 2026-10-19).

-- Dernier relevé de chaque joueur dans la semaine.
create or replace view silver.bv_player_weekly with (security_invoker = true) as
select distinct on (d.player_id, date_trunc('week', d.day))
       date_trunc('week', d.day)::date as week,
       d.*
from silver.bv_player_daily d
order by d.player_id, date_trunc('week', d.day), d.day desc;

-- Une ligne par changement (skill ou forme) lors d'un entraînement hebdomadaire.
-- Source : /teams/<id>/training/recent-runs (≈ 6 dernières semaines), dédoublonné entre captures.
-- delta peut valoir +2 (ex. 50→52). La page « Progress » du jeu compte les changements (count), pas les points (sum delta).
create or replace view silver.bv_training_changes with (security_invoker = true) as
select distinct on ((r->>'id'), (l->>'player_id'), (l->>'skill_id'))
       (r->>'id')::uuid                                       as run_id,
       (r->>'created_at')::timestamptz                        as run_at,
       ((r->>'created_at')::timestamptz at time zone 'Europe/Paris')::date as run_day,
       a.team_id,
       (l->>'player_id')::uuid                                as player_id,
       l->>'first_name' || ' ' || (l->>'last_name')           as name,
       (l->>'age')::int                                       as age,
       l->>'skill_id'                                         as skill,
       (l->>'display_before')::int                            as value_before,
       (l->>'display_after')::int                             as value_after,
       (l->>'display_after')::int - (l->>'display_before')::int as delta
from silver.bv_api a,
     jsonb_array_elements(a.body->'recent_runs') r,
     jsonb_array_elements(r->'lines') l
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/training/recent-runs$'
order by (r->>'id'), (l->>'player_id'), (l->>'skill_id'), a.captured_at desc;

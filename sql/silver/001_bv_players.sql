-- Silver BasketVibe : joueurs et relevé quotidien (skills, forme, fatigue).
-- Sources bronze :
--   /api/v1/teams/<id>/overview  → fiche, skills affichés (entiers), forme, fatigue, PS
--   /api/v1/teams/<id>/training  → skills précis (décimales), entraînement principal et secondaire
-- Jour = date de capture à Paris. Si plusieurs captures le même jour, la dernière l'emporte.

create schema if not exists silver;
revoke all on schema silver from public, anon, authenticated;

-- Réponses 200 de l'API, avec l'équipe tirée de l'URL.
create or replace view silver.bv_api with (security_invoker = true) as
select r.id as capture_id,
       r.captured_at,
       (r.captured_at at time zone 'Europe/Paris')::date as day,
       regexp_replace(split_part(r.source_url, '?', 1), '^https://(www\.)?basketvibe\.com/api/v1', '') as endpoint,
       substring(r.source_url from '/teams/([0-9a-f-]{36})') as team_id,
       r.payload->'body' as body
from bronze.raw_pages r
where r.game = 'basketvibe' and r.source = 'api' and (r.payload->>'status')::int = 200;

create or replace view silver.bv_player_overview with (security_invoker = true) as
select distinct on (p->>'id', a.day)
       a.day, a.captured_at, a.capture_id, a.team_id,
       (p->>'id')::uuid as player_id, p
from silver.bv_api a, jsonb_array_elements(a.body->'players') p
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/overview$'
order by p->>'id', a.day, a.captured_at desc;

create or replace view silver.bv_player_training with (security_invoker = true) as
select distinct on (p->>'id', a.day)
       a.day, a.captured_at, a.team_id,
       (p->>'id')::uuid as player_id, p
from silver.bv_api a, jsonb_array_elements(a.body->'players') p
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/training$'
order by p->>'id', a.day, a.captured_at desc;

-- Une ligne par joueur et par jour où l'effectif a été capturé.
create or replace view silver.bv_player_daily with (security_invoker = true) as
select o.day,
       o.player_id,
       o.team_id,
       o.p->>'first_name' || ' ' || (o.p->>'last_name') as name,
       o.p->>'position'                      as position,
       (o.p->>'age')::int                    as age,
       (o.p->>'form')::numeric               as form,
       (o.p->>'fatigue')::numeric            as fatigue,
       (o.p->>'experience')::int             as experience,
       (o.p->>'player_strength')::numeric    as ps,
       (o.p->>'injury_return_on')::date      as injury_return_on,
       o.p->>'skills_visibility'             as skills_visibility,
       -- skills affichés (entiers)
       (o.p->'stats'->>'two_point')::int     as two_point,
       (o.p->'stats'->>'three_point')::int   as three_point,
       (o.p->'stats'->>'defense')::int       as defense,
       (o.p->'stats'->>'passing')::int       as passing,
       (o.p->'stats'->>'ball_handling')::int as ball_handling,
       (o.p->'stats'->>'rebounding')::int    as rebounding,
       (o.p->'stats'->>'stamina')::int       as stamina,
       (o.p->'stats'->>'athleticism')::int   as athleticism,
       -- skills précis (décimales), seulement si la page Entraînement a été capturée ce jour-là
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
from silver.bv_player_overview o
left join silver.bv_player_training t on t.player_id = o.player_id and t.day = o.day;

-- Dernier état connu de chaque joueur.
create or replace view silver.bv_players with (security_invoker = true) as
select distinct on (o.player_id)
       o.player_id,
       o.team_id,
       o.p->>'first_name'                 as first_name,
       o.p->>'last_name'                  as last_name,
       o.p->>'position'                   as position,
       (o.p->>'age')::int                 as age,
       (o.p->>'height_cm')::int           as height_cm,
       (o.p->>'weight_kg')::int           as weight_kg,
       o.p->>'nationality_code'           as nationality,
       (o.p->>'is_academy_junior')::bool  as academy_junior,
       (o.p->>'is_on_open_transfer_list')::bool as on_transfer_list,
       o.day                              as last_seen
from silver.bv_player_overview o
order by o.player_id, o.day desc, o.captured_at desc;

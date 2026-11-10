-- BasketVibe : effectifs des autres clubs (pages /c/<club>, onglet statistiques), conçu le 2026-11-10.
-- Design : docs/superpowers/specs/2026-11-10-bv-club-roster-design.md
-- Source : silver.bv_api, endpoint /clubs/<slug>/season-roster (classé par l'URL de l'appel API, pas par page_url :
--   une capture d'effectif peut être rangée sous un autre onglet). Identité du club : dernier /clubs/<slug>/season-history.
-- skills_visibility = 'bracket' : skill_brackets {min, max} ; 'full' : stats exactes (min = max) et player_strength.

create or replace view silver.bv_club_roster with (security_invoker = true) as
with roster as (
  select a.capture_id, a.captured_at, a.day,
         substring(a.endpoint from '^/clubs/([^/]+)/season-roster$') as club_slug,
         (a.body->>'season_id')::uuid as season_id,
         (a.body->>'season_index')::int as season_index,
         a.body->'players' as players
  from silver.bv_api a
  where a.endpoint ~ '^/clubs/[^/]+/season-roster$' and jsonb_typeof(a.body->'players') = 'array'
),
ident as (
  select distinct on (substring(a.endpoint from '^/clubs/([^/]+)/season-history$'))
         substring(a.endpoint from '^/clubs/([^/]+)/season-history$') as club_slug,
         (a.body->>'team_id')::uuid as team_id,
         a.body->>'team_name' as team_name
  from silver.bv_api a
  where a.endpoint ~ '^/clubs/[^/]+/season-history$' and a.body ? 'team_id'
  order by substring(a.endpoint from '^/clubs/([^/]+)/season-history$'), a.captured_at desc
),
cap as (
  select r.*, rank() over (partition by r.club_slug order by r.captured_at desc, r.capture_id desc) = 1 as est_derniere
  from roster r
)
select c.capture_id,
       c.captured_at,
       c.day,
       c.club_slug,
       i.team_id,
       i.team_name,
       c.season_id,
       c.season_index,
       c.est_derniere,
       (x->>'id')::uuid                                    as player_id,
       x->>'first_name' || ' ' || (x->>'last_name')        as name,
       x->>'skills_visibility'                             as skills_visibility,
       coalesce((x->'skill_brackets'->'two_point'->>'min')::int,     (x->'stats'->>'two_point')::int)     as two_point_min,
       coalesce((x->'skill_brackets'->'two_point'->>'max')::int,     (x->'stats'->>'two_point')::int)     as two_point_max,
       coalesce((x->'skill_brackets'->'three_point'->>'min')::int,   (x->'stats'->>'three_point')::int)   as three_point_min,
       coalesce((x->'skill_brackets'->'three_point'->>'max')::int,   (x->'stats'->>'three_point')::int)   as three_point_max,
       coalesce((x->'skill_brackets'->'defense'->>'min')::int,       (x->'stats'->>'defense')::int)       as defense_min,
       coalesce((x->'skill_brackets'->'defense'->>'max')::int,       (x->'stats'->>'defense')::int)       as defense_max,
       coalesce((x->'skill_brackets'->'passing'->>'min')::int,       (x->'stats'->>'passing')::int)       as passing_min,
       coalesce((x->'skill_brackets'->'passing'->>'max')::int,       (x->'stats'->>'passing')::int)       as passing_max,
       coalesce((x->'skill_brackets'->'ball_handling'->>'min')::int, (x->'stats'->>'ball_handling')::int) as ball_handling_min,
       coalesce((x->'skill_brackets'->'ball_handling'->>'max')::int, (x->'stats'->>'ball_handling')::int) as ball_handling_max,
       coalesce((x->'skill_brackets'->'rebounding'->>'min')::int,    (x->'stats'->>'rebounding')::int)    as rebounding_min,
       coalesce((x->'skill_brackets'->'rebounding'->>'max')::int,    (x->'stats'->>'rebounding')::int)    as rebounding_max,
       coalesce((x->'skill_brackets'->'stamina'->>'min')::int,       (x->'stats'->>'stamina')::int)       as stamina_min,
       coalesce((x->'skill_brackets'->'stamina'->>'max')::int,       (x->'stats'->>'stamina')::int)       as stamina_max,
       coalesce((x->'skill_brackets'->'athleticism'->>'min')::int,   (x->'stats'->>'athleticism')::int)   as athleticism_min,
       coalesce((x->'skill_brackets'->'athleticism'->>'max')::int,   (x->'stats'->>'athleticism')::int)   as athleticism_max,
       (x->>'player_strength')::numeric                    as player_strength,
       (x->>'form')::int                                   as form,
       (x->>'fatigue')::numeric                            as fatigue,
       (x->>'age')::int                                    as age,
       (x->>'height_cm')::int                              as height_cm,
       (x->>'weight_kg')::int                              as weight_kg,
       (x->>'experience')::int                             as experience,
       x->>'position'                                      as position,
       (x->>'is_former_roster')::boolean                   as is_former_roster,
       (x->>'is_academy_junior')::boolean                  as is_academy_junior,
       (x->>'injury_return_on')::date                      as injury_return_on,
       (x->'season'->>'games_played')::int                 as games_played,
       (x->'season'->'averages'->>'min')::numeric          as min_avg,
       (x->'season'->'averages'->>'pts')::numeric          as pts_avg,
       (x->'season'->'averages'->>'reb')::numeric          as reb_avg,
       (x->'season'->'averages'->>'ast')::numeric          as ast_avg,
       (x->'season'->'averages'->>'eval')::numeric         as eval_avg,
       (x->'friendly_season'->>'games_played')::int        as friendly_games_played
from cap c
left join ident i on i.club_slug = c.club_slug
cross join lateral jsonb_array_elements(c.players) x;

comment on view silver.bv_club_roster is
  'Effectifs des autres clubs BasketVibe (/clubs/<slug>/season-roster), un joueur par club et par capture ; est_derniere = dernière capture du club. '
  'Compétences en fourchettes de 20 points (skills_visibility = bracket) : un classement, pas une mesure fine ; en full, min = max = valeur exacte. '
  'Les analyses filtrent is_former_roster = false par défaut.';

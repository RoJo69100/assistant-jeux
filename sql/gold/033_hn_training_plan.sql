-- Hockey Nation (2026-10-29) : plan d'entraînement PRO + FRM sans agent.
-- Par joueur : compétence clé du poste principal, non plafonnée, talent fort d'abord puis meilleur coach disponible ;
-- coach = meilleur niveau dans cette compétence parmi les 4 coachs de l'équipe ; ordre de choix = plus jeunes d'abord, puis note.
-- Sources : dernier /team/:id/roster de chaque équipe, dernier /club/:id/coaching-staff, gold.hn_position_keys.
create or replace view gold.hn_training_plan with (security_invoker = true) as
with ros as (
  select distinct on (body->>'level') body->>'level' as team_level, body
  from silver.hn_api where route = '/team/:id/roster' and body->>'level' in ('PRO', 'FRM')
  order by body->>'level', captured_at desc
), pl as (
  select r.team_level, p->>'id' as player_id, p->>'lastname' as joueur, (p->>'age')::int as age, (p->>'rating')::int as note,
         p->'positions'->>0 as pos, p->'talents'->'strongest' as forts, p->'skills' as skills
  from ros r, jsonb_array_elements(r.body->'players') p
), staff as (
  select k.key as team_level, c->>'lastname' as coach, s->>'id' as skill, (s->>'lvl')::int as lvl
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c, jsonb_array_elements(c->'skills') s
  where k.key in ('PRO', 'FRM')
), cand as (
  select pl.*, s->>'id' as skill, (s->>'lvl')::int as niveau, (pl.forts ? (s->>'id')) as talent_fort,
         exists (select 1 from gold.hn_position_keys k where k.position = pl.pos and k.skill = s->>'id') as cle,
         (select coach from staff st where st.team_level = pl.team_level and st.skill = s->>'id' order by lvl desc limit 1) as coach,
         coalesce((select max(lvl) from staff st where st.team_level = pl.team_level and st.skill = s->>'id'), 0) as niveau_coach
  from pl, jsonb_array_elements(pl.skills) s
  where not coalesce((s->>'max')::bool, false)
), best as (
  select distinct on (team_level, player_id) *
  from cand order by team_level, player_id, (cle and niveau_coach > 0) desc, talent_fort desc, niveau_coach desc, niveau
)
select team_level, row_number() over (partition by team_level order by age, note desc) as ordre,
       joueur, age, note, pos as poste, skill as competence, niveau, talent_fort, coach, niveau_coach, cle
from best
union all
select pl.team_level, null, pl.joueur, pl.age, pl.note, pl.pos, 'toutes plafonnées', null, null, null, null, null
from pl where not exists (select 1 from best b where b.player_id = pl.player_id);

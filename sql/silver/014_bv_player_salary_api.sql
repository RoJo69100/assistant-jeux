-- Silver BasketVibe : salaire hebdomadaire par joueur, deux sources (2026-10-22).
-- 1. onglet Effectif > Tiles (capture DOM, voir 006_bv_player_salary.sql) ;
-- 2. page joueur : API /players/<id>/season-profile, champ body.player.weekly_salary (lié par player_id, sans jointure sur le nom).
-- Défaut relevé par l'agent Finances le 2026-10-22 : la vue s'arrêtait au 16/10 (dernier export Tiles), salaires de Dang et Albano absents.
-- Contrôle du 2026-10-22 : Dang 20 636 + Albano 17 668 = 38 304, écart exact des salaires prélevés (330 996 - 292 692).
-- Seuls les joueurs de mon club sont gardés (une page joueur peut être celle d'un joueur d'un autre club).
create or replace view silver.bv_player_salary_weekly with (security_invoker = true) as
with tiles as (
  select r.captured_at,
         (r.captured_at at time zone 'Europe/Paris')::date as day,
         x[1] as name,
         replace(replace(x[2], '.', ''), ',', '')::numeric as salary
  from bronze.raw_pages r,
       regexp_matches(r.payload->>'text', '([^\n]+)\nPS\n\d+\n[A-Z]+\|\d+ yrs\n[^\n]*\nSalary ([0-9.,]+)', 'g') x
  where r.game = 'basketvibe' and r.source = 'dom' and r.page_type = 'roster_tiles'
),
both_sources as (
  select p.player_id, s.name, s.salary, s.day, s.captured_at, 'tiles' as source
  from tiles s
  join silver.bv_players p on p.first_name || ' ' || p.last_name = s.name
  union all
  select (r.payload->'body'->'player'->>'id')::uuid,
         (r.payload->'body'->'player'->>'first_name') || ' ' || (r.payload->'body'->'player'->>'last_name'),
         (r.payload->'body'->'player'->>'weekly_salary')::numeric,
         (r.captured_at at time zone 'Europe/Paris')::date,
         r.captured_at,
         'player_page'
  from bronze.raw_pages r
  join silver.bv_players p on p.player_id = (r.payload->'body'->'player'->>'id')::uuid
  join silver.bv_my_team me on me.team_id::text = p.team_id
  where r.game = 'basketvibe' and r.source = 'api'
    and r.source_url like '%/season-profile%'
    and r.payload->'body'->'player'->>'weekly_salary' is not null
)
select distinct on (player_id, date_trunc('week', day))
       date_trunc('week', day)::date as week,
       player_id,
       name,
       salary,
       day,
       source
from both_sources
order by player_id, date_trunc('week', day), captured_at desc;

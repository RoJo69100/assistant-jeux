-- Hardwood, corrections de 038 après le premier export (2026-10-30).
-- 1. hw_player_ids : une ligne par joueur ; les noms abrégés des pages de stats (« E. Corey ») sont écartés.
-- 2. hw_management : redshirt = case cochée (oui) / grisée (impossible : déjà RS ou trop de matchs) / libre (non) ;
--    « this.checked » du onchange faussait la détection. Foul Trouble Hook en toutes lettres.

create or replace view silver.hw_player_ids with (security_invoker = true) as
select distinct on ((m[1])::int) (m[1])::int as player_id, trim(m[2]) as name
from silver.hw_pages p,
     regexp_matches(coalesce(p.html, ''), 'href="/player/(\d+)"[^>]*>([^<]+)</a>', 'g') m
where trim(m[2]) !~ '^[A-Z]\. '
order by (m[1])::int, p.captured_at desc;

create or replace view silver.hw_management with (security_invoker = true) as
with chunks as (
  select p.captured_at, c
  from silver.hw_pages p, regexp_split_to_table(coalesce(p.html, ''), '<span id="') c
  where p.page_type = 'management'
), kv as (
  select captured_at,
         substring(c from '^([a-z_]+?)_\d+"') as setting,
         substring(c from '^[a-z_]+?_(\d+)"')::int as player_id,
         case when c ~ '^red_shirt_select_'
              then case when c ~ 'checked=""' then 'oui' when c ~ 'disabled=""' then 'impossible' else 'non' end
              when c ~ '^foul_hook_' then substring(c from 'selected="">([^<]*)<')
              else substring(c from 'value="([^"]*)" selected') end as v
  from chunks
  where c ~ '^(green_light|offensive_positioning|playing_time|foul_hook|red_shirt_select)_\d+"'
)
select kv.player_id, i.name, max(kv.captured_at) as captured_at,
       max(v) filter (where setting = 'green_light')::int as green_light,
       max(v) filter (where setting = 'offensive_positioning')::int as off_positioning,
       max(v) filter (where setting = 'playing_time')::int as max_minutes,
       max(v) filter (where setting = 'foul_hook') as foul_hook,
       max(v) filter (where setting = 'red_shirt_select') as red_shirt
from kv left join silver.hw_player_ids i using (player_id)
group by kv.player_id, i.name;

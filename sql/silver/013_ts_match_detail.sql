-- Silver Team Soccer : résumé de match (page /dashboard/match-viewer/<id>), checklist B4.
-- Deux sources : la réponse API match_replays (déroulé du moteur, une ligne par événement) et le HTML de la page
-- (notes par mi-temps et comparatif par secteurs, calculés par le site et absents de l'API).
-- Dernière capture par match. Règles : skill teamsoccer-match (moteur v3, barres de secteurs), teamsoccer-joueurs (notes).

-- Événements : `team` local/visiteur → side home/away. Une action (play_id) va de play_buildup à son issue :
-- play_lost_* (ballon perdu), cross_cleared, ou play_tension > play_resolution > tir (save, shot_blocked, shot_wide,
-- shot_post, goal, header, penalty > goal). Un but se lit au changement de score (les têtes marquées sont `header`).
create or replace view silver.ts_match_events with (security_invoker = true) as
with rep as (
  select distinct on (q.match_id) q.match_id, a.captured_at, b
  from silver.ts_api a
  cross join lateral (select (substring(a.query from 'match_id=eq\.([0-9]+)'))::bigint as match_id) q
  cross join lateral jsonb_array_elements(a.body) b
  where a.endpoint = 'match_replays' and b ? 'events' and q.match_id is not null
  order by q.match_id, a.captured_at desc
), e as (
  select r.match_id, r.captured_at, r.b->>'engine_version' as engine_version, e
  from rep r cross join lateral jsonb_array_elements(r.b->'events') e
)
select e.match_id, e.captured_at, e.engine_version,
       (e->>'sequence')::int as seq, (e->>'minute')::int as minute, e->>'type' as type,
       case e->>'team' when 'local' then 'home' when 'visitor' then 'away' end as side,
       case e->>'team' when 'local' then m.home_team_id when 'visitor' then m.away_team_id end as team_id,
       case when m.venue is null or e->>'team' is null then null
            else (e->>'team' = 'local') = (m.venue = 'domicile') end as is_mine,
       e->>'playId' as play_id, (e->>'phase')::int as phase, (e->>'phaseTotal')::int as phase_total,
       (e->>'actorPlayerId')::int as actor_id, e->>'actorName' as actor,
       (e->>'secondaryPlayerId')::int as secondary_id, e->>'secondaryName' as secondary,
       (e->>'homeScoreAfter')::int as home_score_after, (e->>'awayScoreAfter')::int as away_score_after,
       (e->>'homeScoreAfter')::int + (e->>'awayScoreAfter')::int
         > coalesce(lag((e->>'homeScoreAfter')::int + (e->>'awayScoreAfter')::int)
                      over (partition by e.match_id order by (e->>'sequence')::int), 0) as is_goal,
       e->'attendanceData' as attendance, e->'summaryData' as summary
from e
left join silver.ts_matches m on m.match_id = e.match_id;

-- Page HTML du match, dernière capture complète (le tableau des notes est présent).
create or replace view silver.ts_match_pages with (security_invoker = true) as
select distinct on (q.match_id) q.match_id, r.captured_at, r.payload->>'html' as html,
       regexp_replace(regexp_replace(r.payload->>'html', '<[^>]+>', ' ', 'g'), '\s+', ' ', 'g') as text
from bronze.raw_pages r
cross join lateral (select (substring(r.page_url from '/match-viewer/([0-9]+)'))::bigint as match_id) q
where r.game = 'teamsoccer' and q.match_id is not null and r.payload->>'html' like '%tabular-nums%'
order by q.match_id, r.captured_at desc;

-- Notes des joueurs : un tableau par équipe (domicile d'abord), colonnes Pos., Joueur, Minutes, 1re mi-temps,
-- 2e mi-temps, Note. Le poste est l'abréviation affichée (POR, LAT, DFC, EXT, MC, DEL…).
-- Constat du 2026-10-19 sur 5 matchs : à composition égale, notes identiques d'un match à l'autre (7,3 avec ou sans
-- triplé). Elles reflètent le niveau du joueur dans son emplacement (et la Forme ?), pas sa performance du jour ;
-- la performance se lit dans silver.ts_match_events.
create or replace view silver.ts_match_ratings with (security_invoker = true) as
with blk as (
  select p.match_id, b.ord, b.piece,
         replace(substring(b.piece from '^[^>]*>([^<]*)</p>'), '&amp;', '&') as team_name
  from silver.ts_match_pages p
  cross join lateral regexp_split_to_table(p.html, '<p class="text-xs font-bold uppercase tracking-wider mb-2') with ordinality b(piece, ord)
  where b.ord > 1
), rows as (
  select blk.match_id, blk.team_name, blk.ord, x
  from blk
  cross join lateral regexp_matches(blk.piece,
    '<td[^>]*>([A-Z]{2,4})</td><td[^>]*>([^<]+)</td><td[^>]*>([^<]*)</td><td[^>]*>([0-9.]*)</td><td[^>]*>([0-9.]*)</td><td[^>]*>([0-9.]+)</td>', 'g') x
), t as (
  select rows.*, dense_rank() over (partition by match_id order by ord) as team_rank from rows
)
select t.match_id, m.my_team_id,
       case when t.team_name = m.home_team then 'home' when t.team_name = m.away_team then 'away'
            when t.team_rank = 1 then 'home' else 'away' end as side,
       t.team_name, x[1] as pos, replace(x[2], '&amp;', '&') as player, x[3] as minutes,
       (substring(x[3] from '^([0-9]+)'))::int as min_in, (substring(x[3] from '-([0-9]+)'))::int as min_out,
       nullif(x[4], '')::numeric as rating_h1, nullif(x[5], '')::numeric as rating_h2, x[6]::numeric as rating
from t left join silver.ts_matches m on m.match_id = t.match_id;

-- Comparatif par secteurs : pour chaque zone, valeur de l'équipe à domicile face à celle des visiteurs
-- (« ~ » = zone sans joueurs, vaut la moitié des zones voisines). Les gardiens sont à part (zone_order 0 et 8).
create or replace view silver.ts_match_sectors with (security_invoker = true) as
with seg as (
  select match_id, substring(text from 'Comparatif par secteurs(.*?)Dans chaque zone') as s
  from silver.ts_match_pages
)
select seg.match_id, z.ord::int as zone_order, trim(z.x[1]) as zone,
       replace(z.x[2], '~', '')::numeric as home_value, replace(z.x[3], '~', '')::numeric as away_value,
       z.x[2] like '~%' or z.x[3] like '~%' as has_empty_zone
from seg
cross join lateral regexp_matches(seg.s, '([^0-9~]+?)\s*(~?[0-9]+)\s+vs\s+(~?[0-9]+)(?=\s|$)', 'g') with ordinality z(x, ord)
where seg.s is not null
union all
select match_id, 0, 'Gardien (domicile)', replace(substring(s from 'Gardien\s+(~?[0-9]+)'), '~', '')::numeric, null, false
from seg where s is not null
union all
select match_id, 8, 'Gardien (visiteurs)', null, replace(substring(s from '.*Gardien\s+(~?[0-9]+)'), '~', '')::numeric, false
from seg where s is not null;

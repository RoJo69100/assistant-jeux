-- Silver Hardwood (Online College Basketball, onlinecollegebasketball.org) : lecture des pages capturées
-- par userscripts/hardwood.user.js (bronze.raw_pages, game = 'hardwood', source = 'dom').
-- Le site est en HTML : chaque page arrive avec payload.text, payload.tables (headers + rows), payload.fields
-- (réglages des formulaires) et payload.html. Toutes les vues prennent la DERNIÈRE copie de chaque page.
-- Règles : outputs/hardwood/veille/connaissance.md (veille Discord du 2026-10-30) ; manuel /rules pas encore capturé.
-- Préfixe hw_. Notre équipe = celle de la page /team (« [ID #940] »), jamais une constante.

-- Dernière copie de chaque page, avec la date du jeu affichée en tête (« Game Date: Nov 14th, 2054 »).
create or replace view silver.hw_pages with (security_invoker = true) as
select distinct on (r.page_url)
       r.id as capture_id, r.captured_at, (r.captured_at at time zone 'Europe/Paris')::date as day,
       r.page_type, r.page_url,
       nullif(substring(r.page_url from '/(\d+)(?:/|$)'), '')::int as url_id,
       substring(r.payload->>'text' from 'Game Date: ([A-Za-z]+ \d+[a-z]{2}, \d{4})') as game_date_txt,
       r.payload->'tables' as tables, r.payload->'fields' as fields,
       r.payload->>'text' as text, r.payload->>'html' as html
from bronze.raw_pages r
where r.game = 'hardwood' and r.source = 'dom'
order by r.page_url, r.captured_at desc;

-- Notre équipe (page /team ou /team/<id> la plus récente).
create or replace view silver.hw_own with (security_invoker = true) as
select substring(text from '\[ID #(\d+)\]')::int as team_id,
       substring(text from 'Team: ([^\[]+?) \[ID') as team_name,
       substring(text from 'Conference: ([IV]+\.\d+)') as conference,
       substring(text from 'Conference: [IV]+\.\d+ \[(Division \d)\]') as division,
       substring(text from 'Rating: ([\d.]+)')::numeric as rating,
       substring(text from 'Overall Position: #(\d+)')::int as overall_position,
       substring(text from 'Fan Mood: ([\d.]+)')::numeric as fan_mood,
       substring(text from 'Alumni Mood: ([\d.]+)')::numeric as alumni_mood,
       substring(text from 'Prestige: (\d+)')::int as prestige,
       substring(text from 'Team Power Index: ([\d.]+)')::numeric as tpi,
       game_date_txt, captured_at
from silver.hw_pages
where page_type in ('team', 'team_id') and text ~ '\[ID #\d+\]'
order by captured_at desc
limit 1;

-- Identifiants des joueurs : liens /player/<id> présents dans le HTML de n'importe quelle page de notre équipe.
create or replace view silver.hw_player_ids with (security_invoker = true) as
select distinct on (m[2]) (m[1])::int as player_id, trim(m[2]) as name
from silver.hw_pages p,
     regexp_matches(coalesce(p.html, ''), 'href="/player/(\d+)"[^>]*>([^<]+)</a>', 'g') m
order by m[2], p.captured_at desc;

-- Effectif (page /roster/<notre id>). Les colonnes sont lues par position : l'en-tête a deux « Pos ».
-- Le nom porte « +N » quand le joueur est blessé pour N jours (« Chris Adkins +7 »).
create or replace view silver.hw_roster with (security_invoker = true) as
select p.captured_at, p.game_date_txt,
       i.player_id,
       trim(regexp_replace(r->>3, '\s*\+\d+$', '')) as name,
       r->>0 as pos, nullif(r->>2, '')::int as jersey, nullif(r->>4, '')::numeric as height_m,
       (r->>5)::int as ins, (r->>6)::int as os, (r->>7)::int as rng, (r->>8)::int as fin, (r->>9)::int as reb,
       (r->>10)::int as idef, (r->>11)::int as pdef, (r->>12)::int as iq, (r->>13)::int as pass, (r->>14)::int as hnd,
       (r->>15)::int as drv, (r->>16)::int as str, (r->>17)::int as spd, (r->>18)::int as sta,
       nullif(r->>19, '') as positions,          -- majuscule = poste maîtrisé, minuscule = poste en apprentissage (veille)
       (r->>20)::int as si, (r->>21)::int as pot, nullif(nullif(r->>22, '-'), '')::int as stars,
       r->>23 as class, (r->>23) like 'RS %' as redshirted, (r->>24) <> '' as scholarship,
       coalesce(substring(r->>3 from '\+(\d+)$')::int, 0) as injury_days,
       (r->>3) ~ '\+\d+$' as injured
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
left join silver.hw_player_ids i on i.name = trim(regexp_replace(r->>3, '\s*\+\d+$', ''))
where p.page_type = 'roster_id' and p.url_id = o.team_id and jsonb_array_length(r) >= 24;

-- Calendrier de la saison (page /schedule/<notre id>). Score = visiteur - domicile ; W/L = notre résultat.
create or replace view silver.hw_schedule with (security_invoker = true) as
select p.captured_at, g.ord as game_no,
       r->>0 as sim_time, r->>1 as game_date, r->>2 as game_type,     -- Exhibition, Non-Conference, Conference, …
       r->>3 as visitor, r->>4 as home,
       (r->>4) = split_part(o.team_name, ' ', 1) as is_home,
       case when r->>5 ~ '^[WL] ' then left(r->>5, 1) end as my_result,
       substring(r->>5 from '^[WL] (\d+) -')::int as visitor_pts,
       substring(r->>5 from '- (\d+)')::int as home_pts,
       r->>5 ~ '\(ot\)' as overtime,
       r->>5 = 'NPY' as not_played,
       nullif(replace(r->>7, ',', ''), 'NPY')::int as attendance
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') with ordinality g(r, ord)
where p.page_type = 'schedule_id' and p.url_id = o.team_id and jsonb_array_length(r) >= 8;

-- Coachs de notre équipe (page /coaches/<id>) : Off, Def, Tac (tactique), Dev (développement), Mot, Rec (recrutement), échelle 0-20.
create or replace view silver.hw_coaches with (security_invoker = true) as
select p.captured_at, r->>0 as role, r->>2 as coach, (r->>3)::int as age,
       (r->>5)::int as off, (r->>6)::int as def, (r->>7)::int as tac, (r->>8)::int as dev,
       (r->>9)::int as mot, (r->>10)::int as rec, (r->>11)::int as years,
       replace(replace(r->>13, '$', ''), 'M', '')::numeric as salary_m
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'coaches_id' and p.url_id = o.team_id and jsonb_array_length(r) >= 14;

-- Classement de la conférence (page /conference/<id>) ; première ligne de rows = sous-en-tête, ignorée.
create or replace view silver.hw_standings with (security_invoker = true) as
select p.captured_at, p.url_id as conference_page_id,
       substring(p.text from '\n([IV]+\.\d+) Conference') as conference,
       (r->>0)::int as rank, trim(r->>1) as team,
       (r->>2)::int as conf_w, (r->>3)::int as conf_l,
       (r->>11)::int as w, (r->>12)::int as l, (r->>14)::numeric as pf, (r->>15)::numeric as pa,
       r->>18 as home, r->>19 as away, r->>21 as streak,
       nullif(r->>24, '')::numeric as rpi, nullif(r->>25, '')::numeric as sos
from silver.hw_pages p
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'conference_id' and (r->>0) ~ '^\d+$';

-- Statistiques de la saison par joueur (page /statistics/<notre id>), moyennes par match.
create or replace view silver.hw_player_stats with (security_invoker = true) as
select p.captured_at, r->>0 as name, (r->>1)::int as g, (r->>2)::int as gs, (r->>3)::numeric as min,
       (r->>4)::numeric as fgm, (r->>5)::numeric as fga, nullif(r->>6, '-')::numeric as fg_pct,
       (r->>7)::numeric as tpm, (r->>8)::numeric as tpa, nullif(r->>9, '-')::numeric as tp_pct,
       (r->>10)::numeric as ftm, (r->>11)::numeric as fta, nullif(r->>12, '-')::numeric as ft_pct,
       (r->>13)::numeric as pts, (r->>17)::numeric as oreb, (r->>18)::numeric as dreb, (r->>19)::numeric as reb,
       (r->>20)::numeric as ast, (r->>21)::numeric as stl, (r->>22)::numeric as blk,
       (r->>24)::numeric as tov, (r->>25)::numeric as pf, (r->>26)::int as dq,
       nullif(r->>28, '-')::numeric as usg_pct, (r->>29)::int as inj, nullif(r->>30, '-')::numeric as plus_minus
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'statistics_id' and p.page_url ~ ('/statistics/' || o.team_id || '$')
  and jsonb_array_length(r) >= 31;

-- Recrutement : tableau des prospects suivis + bandeau (« Recruiting Round #11 / 53 », points, bourses).
create or replace view silver.hw_recruiting with (security_invoker = true) as
select p.captured_at,
       substring(p.text from 'Recruiting Round #(\d+)')::int as round,
       substring(p.text from 'Recruiting Round #\d+ / (\d+)')::int as rounds,
       substring(p.text from 'Recruiting Point\(s\): (\d+)')::int as points,
       substring(p.text from 'Recruiting Point\(s\): \d+ / (\d+) Max')::int as points_max,
       substring(p.text from '(\d+) / \d+ Scholarships Available For Prospects Next Season')::int as schol_open_next,
       substring(p.text from 'Following Season: ([0-9 -]+)') as schol_following,
       r->>0 as class, r->>2 as prospect, nullif(r->>3, '')::numeric as height_m, r->>4 as pos, r->>5 as hometown,
       (r->>6)::int as contacts, (r->>7)::int as si, (r->>8)::int as pot, nullif(r->>9, '')::int as stars,
       r->>10 as top_skills, r->>11 as hs_stats, (r->>12) <> '' as offered, r->>13 as interest, r->>14 as competition
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables) t
cross join lateral jsonb_array_elements(t->'rows') r
where p.page_type = 'recruiting_id' and p.url_id = o.team_id
  and (t->'headers'->>2) = 'Prospect' and jsonb_array_length(r) >= 15;

-- Game Tactics : bloc 0 = départ du match, blocs 1 à 5 = ajustements de mi-temps (déclencheur + seuils).
-- Pace -5..+5 ; Emphasis I (très intérieur) i ~ o O (très extérieur) ; Zone % et Pressure % (le reste = individuelle) ;
-- Extend -5..+5 (NC = inchangé) ; Substitution Mode Mass / Staggered A-B-C.
create or replace view silver.hw_tactics with (security_invoker = true) as
with f as (
  select p.captured_at, x->>'name' as name, coalesce(x->>'text', x->>'value') as v
  from silver.hw_pages p cross join silver.hw_own o, jsonb_array_elements(p.fields) x
  where p.page_type = 'game_tactics_id' and p.url_id = o.team_id
)
select max(captured_at) as captured_at, b as block,
       max(v) filter (where name = 'ttype-' || b) as trigger,
       max(v) filter (where name = 'threshold-' || b || 'l') as lower_threshold,
       max(v) filter (where name = 'threshold-' || b || 'u') as upper_threshold,
       max(v) filter (where name = 'pace-' || b) as pace,
       max(v) filter (where name = 'emphasis-' || b) as emphasis,
       max(v) filter (where name = 'zone-' || b)::int as zone_pct,
       max(v) filter (where name = 'pressure-' || b)::int as pressure_pct,
       100 - max(v) filter (where name = 'zone-' || b)::int - max(v) filter (where name = 'pressure-' || b)::int as man_pct,
       max(v) filter (where name = 'extended-' || b) as extend,
       max(v) filter (where name = 'sub_mode-' || b) as sub_mode
from f cross join generate_series(0, 5) b
group by b;

-- Game Management, par joueur, lu dans le HTML : chaque réglage est dans <span id="<réglage>_<player_id>">.
-- Green Light 0 x, 1 --, 2 -, 3 neutre, 4 +, 5 ++ ; Offensive Positioning 1 I, 2 i, 3 neutre, 4 o, 5 O ;
-- Playing Time = minutes max (1 à 15 « non recommandé ») ; Foul Trouble Hook none / slow / average / quick.
create or replace view silver.hw_management with (security_invoker = true) as
with chunks as (
  select p.captured_at, c
  from silver.hw_pages p, regexp_split_to_table(coalesce(p.html, ''), '<span id="') c
  where p.page_type = 'management'
), kv as (
  select captured_at,
         substring(c from '^([a-z_]+?)_\d+"') as setting,
         substring(c from '^[a-z_]+?_(\d+)"')::int as player_id,
         coalesce(substring(c from 'value="([^"]*)" selected'), case when c ~ '\mchecked\M' then 'on' end) as v
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

-- Coachs du club (historique des transactions) et mouvements de joueurs : à lire depuis hw_pages (transactions_id) au besoin.

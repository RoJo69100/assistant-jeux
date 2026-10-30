-- Hardwood : feuilles de match (/game/<id>), dernière copie de chaque match.
-- Le site met des espaces insécables (chr(160)) : remplacés avant les regex. Regex Postgres : pas de mélange
-- de quantificateurs gourmands et non gourmands (le premier impose son mode à tout le motif).
-- La première ligne « A 99 - B 67 » donne le visiteur puis l'équipe à domicile (même ordre que le box score).
-- On n'y voit que NOTRE tactique demandée (« Game Tactics ») ; la défense réellement jouée et l'extend sont
-- mesurés pour les deux équipes (« Defensive Tactics ») : c'est la seule lecture de la tactique adverse.

create or replace view silver.hw_games with (security_invoker = true) as
with g as (
  select p.captured_at, p.url_id as game_id,
         replace(split_part(split_part(p.text, 'HomeNewsTeamMailForumHelpSearch', 2), 'Colorful Dialog', 1), chr(160), ' ') as t,
         (select substring(r.text from '\n([^\n]+) Roster\n') from silver.hw_pages r cross join silver.hw_own o
           where r.page_type = 'roster_id' and r.url_id = o.team_id limit 1) as own_short
  from silver.hw_pages p
  where p.page_type = 'game_id'
), h as (
  select g.*, regexp_match(substring(t from '^\s*([^\n]+)'), '^(.*) (\d+) - (.*) (\d+)\s*$') as sc,
         regexp_match(t, '1st Half:\s+Offense\s+Pace ([-+]?\d+), Emphasis (\S+) - Defense\s+Man-to-Man (\d+)%, Zone (\d+)%, Pressure (\d+)%, Extend ([-+]?\d+) - Sub-Mode ([^\n]+)') as tac
  from g
)
select captured_at, game_id,
       substring(t from 'Date: ([A-Za-z]+ \d+[a-z]{2}, \d{4})') as game_date,
       substring(t from 'Game: College \[([^\]]+)\]') as game_type,
       sc[1] as visitor, sc[2]::int as visitor_pts, sc[3] as home, sc[4]::int as home_pts,
       sc[3] = own_short as is_home,
       case when own_short not in (sc[1], sc[3]) then null
            when (sc[1] = own_short) = (sc[2]::int > sc[4]::int) then 'W' else 'L' end as my_result,
       case when sc[1] = own_short then sc[2]::int - sc[4]::int else sc[4]::int - sc[2]::int end as my_margin,
       case when sc[1] = own_short then sc[3] else sc[1] end as opponent,
       substring(t from 'Player Of The Game: ([^(\n]+?) \(') as player_of_game,
       tac[1]::int as my_pace, tac[2] as my_emphasis, tac[3]::int as my_man_pct, tac[4]::int as my_zone_pct,
       tac[5]::int as my_pressure_pct, tac[6]::int as my_extend, trim(tac[7]) as my_sub_mode,
       trim(substring(t from '2nd Half:\s+([^\n]+)')) as my_second_half,
       trim(substring(t from 'Injuries\n[^\n]*?' || own_short || ':\s+([^\n]+)')) as my_injuries,
       trim(substring(t from 'Overworked\n[^\n]*?' || own_short || ':\s+([^\n]+)')) as my_overworked,
       substring(t from 'Simulated:\s+([^\n]+)') as simulated_at
from h;

-- Une ligne par équipe et par match : efficacité par zone de tir, défense réellement jouée, SI pondéré et TPI.
create or replace view silver.hw_game_teams with (security_invoker = true) as
with g as (
  select p.url_id as game_id,
         replace(split_part(split_part(p.text, 'HomeNewsTeamMailForumHelpSearch', 2), 'Colorful Dialog', 1), chr(160), ' ') as t
  from silver.hw_pages p where p.page_type = 'game_id'
), eff as (
  select game_id, trim(m[1]) as team, m
  from g, regexp_matches(t, '\n([^\n:]+):\s+At the rim \((\d+)/(\d+)[^)]*\)\s+Inside \((\d+)/(\d+)[^)]*\)\s+Mid-range \((\d+)/(\d+)[^)]*\)\s+Beyond the Arc \((\d+)/(\d+)', 'g') m
), def as (
  select game_id, trim(m[1]) as team, m
  from g, regexp_matches(t, '\n([^\n:]+):\s+Man-To-Man \(([\d.]+)%\)\s+Zone \(([\d.]+)%\)\s+Pressure \(([\d.]+)%\)\s+2nd Chance \(([\d.]+)%\)\s+Transition \(([\d.]+)%\)\s+Int\. Foul \(([\d.]+)%\)\s*\n\s*Extend:\s+Start ([-+.\d]+),\s+End of 1st Half ([-+.\d]+),\s+Start of 2nd Half ([-+.\d]+),\s+End of Regulation\s+([-+.\d]+)', 'g') m
), si as (
  select game_id, trim(m[1]) as team, m
  from g, regexp_matches(t, '\n([^\n:]+):\s+([\d.]+) / ([\d.]+)', 'g') m
)
select e.game_id, e.team,
       e.m[2]::int as rim_m, e.m[3]::int as rim_a, e.m[4]::int as inside_m, e.m[5]::int as inside_a,
       e.m[6]::int as mid_m, e.m[7]::int as mid_a, e.m[8]::int as three_m, e.m[9]::int as three_a,
       d.m[2]::numeric as def_man_pct, d.m[3]::numeric as def_zone_pct, d.m[4]::numeric as def_pressure_pct,
       d.m[5]::numeric as def_2nd_chance_pct, d.m[6]::numeric as def_transition_pct, d.m[7]::numeric as def_int_foul_pct,
       d.m[8]::numeric as extend_start, d.m[9]::numeric as extend_end_h1, d.m[10]::numeric as extend_start_h2,
       d.m[11]::numeric as extend_end,
       s.m[2]::numeric as weighted_si, s.m[3]::numeric as tpi
from eff e
left join def d using (game_id, team)
left join si s using (game_id, team);

-- Box score : une ligne par joueur et par match. Le suffixe du nom = poste joué (« C. Harkins sf »).
-- Fat = fatigue en fin de match (- aucune, Lght légère, Mod modérée, Hvy forte) ; OFG = tirs réussis/tentés par l'adversaire direct.
create or replace view silver.hw_game_box with (security_invoker = true) as
with rows as (
  select p.url_id as game_id, q.o, q.r
  from silver.hw_pages p, jsonb_array_elements(p.tables->1->'rows') with ordinality q(r, o)
  where p.page_type = 'game_id'
), tagged as (
  select *, sum(case when jsonb_array_length(r) = 1 and r->>0 <> '' then 1 else 0 end)
              over (partition by game_id order by o) as side
  from rows
), named as (
  select distinct on (game_id, side) game_id, side, r->>0 as team_full
  from tagged where jsonb_array_length(r) = 1 and r->>0 <> ''
  order by game_id, side, o
)
select game_id, side, team_full,
       nullif(r->>0, '')::int as jersey,
       regexp_replace(r->>2, '\s+(pg|sg|sf|pf|c)$', '') as player, substring(r->>2 from '\s(pg|sg|sf|pf|c)$') as pos_played,
       (r->>3)::int as min,
       split_part(r->>4, '-', 1)::int as fgm, split_part(r->>4, '-', 2)::int as fga,
       split_part(r->>5, '-', 1)::int as tpm, split_part(r->>5, '-', 2)::int as tpa,
       split_part(r->>6, '-', 1)::int as ftm, split_part(r->>6, '-', 2)::int as fta,
       (r->>7)::int as pts, (r->>8)::int as oreb, (r->>9)::int as reb, (r->>10)::int as ast,
       (r->>11)::int as stl, (r->>12)::int as blk,
       split_part(trim(r->>13), '-', 1)::int as ofg_m, split_part(trim(r->>13), '-', 2)::int as ofg_a,
       (r->>14)::int as tov, (r->>15)::int as pf, nullif(r->>16, '')::int as plus_minus,
       (r->>20)::int as fd, nullif(r->>21, '-') as fatigue
from tagged join named using (game_id, side)
where jsonb_array_length(r) >= 22 and r->>0 ~ '^\d+$';

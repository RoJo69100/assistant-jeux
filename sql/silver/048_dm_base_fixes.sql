-- Derby Manager, corrections du 2026-10-30 après le premier test sur les exports de Queen of the South.
-- 1. Entraînement de groupe : lire le mot qui suit « MOV n » (avant : « MOV 3 Positioning »).
-- 2. Money flow et School : Postgres donne à toute la regex la gourmandise du premier quantificateur ; on découpe
--    d'abord en éléments (une date ou un « Promote Release » par élément), puis on lit chaque élément.
-- 3. silver.dm_player_ids : identifiants /players/<id> lus dans le HTML de toutes les pages.

create or replace view silver.dm_training_groups with (security_invoker = true) as
with t as (
  select s.team_id, s.captured_at, tb
  from silver.dm_team_src s cross join lateral jsonb_array_elements(s.tables) tb
  where tb->'headers'->>0 ~ '^\s*Goalkeepers'
), g as (
  select team_id, captured_at, 0 as grp, tb->'headers'->>0 as raw from t
  union all
  select team_id, captured_at, row_number() over (partition by team_id order by o)::int, r->>0
  from t cross join lateral jsonb_array_elements(tb->'rows') with ordinality x(r, o)
  where jsonb_array_length(r) = 1
)
select team_id, captured_at, grp,
       substring(raw from '^\s*(\w+)') as grp_name,
       substring(raw from 'TEC (\d+)')::int as tec_lvl, substring(raw from 'DEC (\d+)')::int as dec_lvl,
       substring(raw from 'MOV (\d+)')::int as mov_lvl,
       substring(regexp_replace(raw, '\s+', ' ', 'g') from 'MOV \d+ ([A-Za-z]+(?: [A-Za-z]+)??) training') as training
from g;

create or replace view silver.dm_money_flow with (security_invoker = true) as
with p as (select team_id, captured_at, text from silver.dm_pages where page_type = 'teams_id_finances'),
blocks as (
  select team_id, captured_at, b.kind, substring(text from b.re) as body
  from p cross join (values
    ('in',       'In DATE NAME FROM PRICE (.*) -?[\d.]+M Out DATE'),
    ('out',      'Out DATE NAME TO PRICE (.*) -?[\d.]+M Extended DATE'),
    ('extended', 'Extended DATE NAME PRICE (.*) -?[\d.]+M Promoted DATE'),
    ('promoted', 'Promoted DATE NAME PRICE (.*) -?[\d.]+M\s*$')) b(kind, re)
), items as (
  select team_id, captured_at, kind, it
  from blocks cross join lateral regexp_split_to_table(coalesce(body, ''), ' (?=(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2} )') it
)
select team_id, captured_at, kind, m[1] as date_txt, trim(m[2]) as name, m[3] as pos, m[4]::int as age,
       nullif(trim(m[5]), '') as other_club, silver.dm_money(m[6]) as amount
from items cross join lateral regexp_matches(it, '^(\w{3} \d{1,2}) ([^,]+), ([A-Z/]+), (\d+)(.*) (-?[\d.]+[kM])\s*$') m;

create or replace view silver.dm_school with (security_invoker = true) as
with p as (select team_id, captured_at, text from silver.dm_pages where page_type = 'teams_id_school'),
c as (
  select team_id, captured_at, trim(ch) as ch
  from p cross join lateral regexp_split_to_table(substring(text from 'YOUTH PROSPECTS (.*)$'), ' Promote Release ?') ch
  where trim(ch) <> ''
)
select team_id, captured_at,
       trim(substring(ch from '^([^,]+),')) as name,
       substring(ch from '^[^,]+, ([A-Z/]+)') as pos,
       substring(ch from 'Until: (\w{3} \d{1,2})') as until_txt,
       substring(ch from '\((\d+) days left\)')::int as days_left,
       substring(ch from 'days left\) (.+?) \d+ years') as country,
       substring(ch from '(\d+) years')::int as age,
       substring(ch from '(\d+)cm')::int as height_cm, substring(ch from '(\d+)kg')::int as weight_kg,
       substring(ch from '(\w+) footed') as foot,
       substring(ch from 'footed (.*?) (?:Untested|Tested)') as skills_txt,
       substring(ch from '(Untested|Tested) youngster') as tested,
       substring(ch from 'with (\w+) natural fitness') as natural_fitness,
       substring(ch from 'He has (\w+) potential') as potential_level,
       substring(ch from 'potential to become an? ([\w ]+?)\.') as potential_target,
       substring(ch from 'shows an? ([\w -]+?) personality') as personality
from c;

create or replace view silver.dm_player_ids with (security_invoker = true) as
select distinct on (m[1]) m[1]::int as player_id, trim(m[2]) as name, p.team_id as seen_on_team, p.page_url
from silver.dm_pages p
cross join lateral regexp_matches(coalesce(p.html, ''),
  'href="/players/(\d+)"[^>]*>(?:<span[^>]*>[^<]*</span>)?\s*(?:\d+\. )?([^<]{3,40})</a>', 'g') m
order by m[1], p.captured_at desc;

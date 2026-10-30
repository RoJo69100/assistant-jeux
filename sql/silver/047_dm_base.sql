-- Silver Derby Manager (derbymanager.com, football) : lecture des pages capturées par userscripts/derbymanager.user.js
-- (bronze.raw_pages, game = 'derbymanager'). Conçu le 2026-10-30.
-- Deux clubs : 547 Queen of the South (Écosse, D1) et 307 Marmandes (France, D4). Chaque vue porte team_id : on ne
-- mélange jamais les deux. Le club d'une page = l'identifiant de l'URL /teams/<id> ; sinon payload.club (userscript).
-- Les cellules du site portent souvent une clé de tri collée à la valeur (« 15000::15k », « 14Useful player »,
-- « 3-DLCR ») : silver.dm_n() lit le premier nombre, les regex retirent les clés.
-- Préfixe dm_. Règles : outputs/derbymanager/veille/connaissance.md.

create or replace function silver.dm_n(t text) returns numeric
language sql immutable as $$
  select nullif(substring(replace(coalesce(t, ''), ',', '') from '^\s*([+-]?\d+(?:\.\d+)?)'), '')::numeric
$$;

-- Montant affiché « 4.0M », « 766k », « -500k », « 20,402,320 » → nombre.
create or replace function silver.dm_money(t text) returns numeric
language sql immutable as $$
  select case
    when t ~* '^\s*[+-]?[\d.,]+\s*M' then silver.dm_n(t) * 1000000
    when t ~* '^\s*[+-]?[\d.,]+\s*k' then silver.dm_n(t) * 1000
    else silver.dm_n(t) end
$$;

-- Dernière copie de chaque page (DOM), avec le club.
create or replace view silver.dm_pages with (security_invoker = true) as
select distinct on (r.page_url)
       r.id as capture_id, r.captured_at, (r.captured_at at time zone 'Europe/Paris')::date as day,
       r.page_type, r.page_url,
       coalesce(substring(r.page_url from '/teams/(\d+)')::int,
                case when r.payload->>'club' ~ '^\d+$' then (r.payload->>'club')::int end) as team_id,
       r.payload->'tables' as tables, r.payload->'fields' as fields,
       regexp_replace(r.payload->>'text', '\s+', ' ', 'g') as text, r.payload->>'html' as html
from bronze.raw_pages r
where r.game = 'derbymanager' and r.source = 'dom'
order by r.page_url, r.captured_at desc;

-- Nos deux clubs (référence fixe donnée par l'utilisateur le 2026-10-30).
create or replace view silver.dm_clubs with (security_invoker = true) as
select * from (values
  (547, 'Queen of the South', 'Écosse', 1, 'qos'),
  (307, 'Marmandes', 'France', 4, 'mar')) v(team_id, club, country, division, code);

-- Page d'équipe complète la plus récente de chaque club (/teams/<id>?view=… : le site met tous les onglets dans le DOM).
-- On garde la copie dont le tableau d'effectif a ses colonnes FRM remplies (l'onglet Squad les laisse parfois vides).
create or replace view silver.dm_team_src with (security_invoker = true) as
select distinct on (tid) tid as team_id, r.id as capture_id, r.captured_at, r.payload->'tables' as tables,
       regexp_replace(r.payload->>'text', '\s+', ' ', 'g') as text, r.payload->'fields' as fields
from (select substring(page_url from '/teams/(\d+)(?:\?|$)')::int as tid, *
      from bronze.raw_pages where game = 'derbymanager' and source = 'dom' and page_url ~ '/teams/\d+(\?|$)') r
where exists (select 1 from jsonb_array_elements(r.payload->'tables') t
              where t->'headers'->>0 = 'SEL' and t->'headers'->>1 = 'NAME'
                and exists (select 1 from jsonb_array_elements(t->'rows') x where coalesce(x->>8, '') <> ''))
order by tid, r.captured_at desc;

-- Effectif : une ligne par joueur (64 colonnes de l'écran Squad).
-- Compétences (1-20) : HAN handling, MAR marking, TAC tackling, POS positioning, AER aerial, AGI agility,
-- ANT anticipation, CRE creativity, PAS passing, BAL ball control, FIR first touch, TEC technique, ACC accuracy,
-- SHO shooting, HEA headers, REA reaction. Salaire et argent : par jour (page Finances, « Daily flow »).
create or replace view silver.dm_squad with (security_invoker = true) as
select s.team_id, s.captured_at,
       substring(r->>0 from '([A-Z]{1,4} \([A-Z]+\)|S\d)\s*$') as slot,
       substring(r->>1 from '(\d+)\.\s') ::int as shirt,
       trim(regexp_replace(r->>1, '^(\d+\s+)?\d+\.\s*', '')) as name,
       trim(regexp_replace(r->>2, '^\d+[\s-]+', '')) as pos,
       silver.dm_n(r->>3)::int as age,
       substring(r->>4 from '^(LOW|MED|HIGH)') as intensity,
       r->>5 as tr, silver.dm_n(r->>6)::int as pt, silver.dm_n(r->>7) as condition_pct,
       silver.dm_n(r->>8)::int as form, silver.dm_n(r->>9)::int as sharpness,
       silver.dm_n(r->>10)::int as bu, silver.dm_n(r->>11)::int as pbu, nullif(r->>12, '') as traits,
       silver.dm_n(r->>13)::int as fit, silver.dm_n(r->>14)::int as exp, silver.dm_n(r->>15)::int as pot,
       nullif(r->>16, '') as skill,
       silver.dm_n(r->>17)::int as han, silver.dm_n(r->>18)::int as mar, silver.dm_n(r->>19)::int as tac,
       silver.dm_n(r->>20)::int as posi, silver.dm_n(r->>21)::int as aer, silver.dm_n(r->>22)::int as agi,
       silver.dm_n(r->>23)::int as ant, silver.dm_n(r->>24)::int as cre, silver.dm_n(r->>25)::int as pas,
       silver.dm_n(r->>26)::int as bal, silver.dm_n(r->>27)::int as fir, silver.dm_n(r->>28)::int as tec,
       silver.dm_n(r->>29)::int as acc, silver.dm_n(r->>30)::int as sho, silver.dm_n(r->>31)::int as hea,
       silver.dm_n(r->>32)::int as rea,
       substring(r->>33 from '^([A-Z]+)') as sub_policy,
       silver.dm_n(r->>34)::int as sp_sho, silver.dm_n(r->>35)::int as sp_acc, silver.dm_n(r->>36)::int as sp_pas,
       nullif(substring(r->>37 from '^(.*?)Default'), '-') as sp_pen, nullif(substring(r->>38 from '^(.*?)Default'), '-') as sp_fk,
       nullif(substring(r->>39 from '^(.*?)Default'), '-') as sp_cor,
       silver.dm_n(r->>40)::int as sp_aer, silver.dm_n(r->>41)::int as sp_hea,
       nullif(substring(r->>42 from '^(.*?)Default'), '-') as sp_def, nullif(substring(r->>43 from '^(.*?)Default'), '-') as sp_att,
       silver.dm_n(r->>45)::int as xp, nullif(substring(r->>46 from '^(.*?)Default'), '-') as captain,
       silver.dm_n(r->>47)::int as apps, silver.dm_n(r->>48)::int as st_con, silver.dm_n(r->>49)::int as st_sav,
       silver.dm_n(r->>50)::int as st_tac, silver.dm_n(r->>51)::int as st_pas, silver.dm_n(r->>52)::int as assists,
       r->>53 as shots_on_target, silver.dm_n(r->>54)::int as goals, silver.dm_n(r->>55) as rating,
       nullif(r->>56, '') as cou,
       trim(regexp_replace(r->>57, '^\d+', '')) as tier, silver.dm_n(r->>57)::int as tier_rank,
       silver.dm_n(r->>58)::int as sta, round(silver.dm_n(r->>59) * 100, 1) as satisfaction_pct,
       trim(regexp_replace(r->>60, '^\d+', '')) as role, silver.dm_n(substring(r->>61 from '\d+'))::int as contract_days,
       silver.dm_n(r->>62) as salary, silver.dm_n(r->>63) as price
from silver.dm_team_src s
cross join lateral jsonb_array_elements(s.tables) t
cross join lateral jsonb_array_elements(t->'rows') r
where t->'headers'->>0 = 'SEL' and t->'headers'->>1 = 'NAME'
  and jsonb_array_length(r) >= 64 and coalesce(r->>1, '') <> '';

-- Réglages tactiques enregistrés (curseurs de l'onglet Squad : 0 = gauche, 2 = droite), formation et esprit.
create or replace view silver.dm_tactic with (security_invoker = true) as
select s.team_id, s.captured_at,
       substring(s.text from 'SPIRIT: (\d+)%')::int as spirit_pct,
       max(case when f->>'name' = 'defensive_line' then (f->>'value')::int end) as defensive_line,   -- Low 0 · 1 · 2 High
       max(case when f->>'name' = 'pass_type' then (f->>'value')::int end) as pass_preference,       -- Short 0 · 2 Direct
       max(case when f->>'name' = 'pass_focus' then (f->>'value')::int end) as pass_focus,           -- Narrow 0 · 2 Wide
       max(case when f->>'name' = 'shot_focus' then (f->>'value')::int end) as shooting,             -- On sight 0 · 2 From box
       max(case when f->>'name' = 'headers' then (f->>'value')::int end) as headers                  -- Avoid 0 · 2 Prioritise
from silver.dm_team_src s
left join lateral (
  select f from bronze.raw_pages b, jsonb_array_elements(b.payload->'fields') f
  where b.game = 'derbymanager' and b.page_url ~ ('/teams/' || s.team_id || '(\?|$)') and jsonb_array_length(b.payload->'fields') > 0
    and b.captured_at = (select max(captured_at) from bronze.raw_pages b2
                         where b2.game = 'derbymanager' and b2.page_url ~ ('/teams/' || s.team_id || '(\?|$)')
                           and jsonb_array_length(b2.payload->'fields') > 0)
) x on true
group by s.team_id, s.captured_at, s.text;

-- Entraînement : groupes (GK, DEF, MID, FWD) avec l'entraînement choisi et les niveaux TEC/DEC/MOV affichés.
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
       trim(substring(regexp_replace(raw, '\s+', ' ', 'g') from '(\w[\w ]*?) training')) as training
from g;

-- Entraînement par joueur : intensité, potentiel, TR, mentor, compétences et variation (« 13 +4 »), gains/pertes.
-- Ordre des compétences de cet écran : HAN REA TAC PAS FIR SHO POS ANT CRE TEC ACC MAR AER AGI BAL HEA.
create or replace view silver.dm_training with (security_invoker = true) as
with t as (
  select s.team_id, s.captured_at, tb
  from silver.dm_team_src s cross join lateral jsonb_array_elements(s.tables) tb
  where tb->'headers'->>0 ~ '^\s*Goalkeepers'
), r as (
  select team_id, captured_at, r, o,
         count(*) filter (where jsonb_array_length(r) = 1) over (partition by team_id order by o) as grp
  from t cross join lateral jsonb_array_elements(tb->'rows') with ordinality x(r, o)
), k(i, sk) as (values (8,'han'),(9,'rea'),(10,'tac'),(11,'pas'),(12,'fir'),(13,'sho'),(14,'posi'),(15,'ant'),
                        (16,'cre'),(17,'tec'),(18,'acc'),(19,'mar'),(20,'aer'),(21,'agi'),(22,'bal'),(23,'hea'))
select r.team_id, r.captured_at, g.grp_name, g.training as group_training,
       trim(regexp_replace(r.r->>0, '\s+[+-]?[\d.]+::.*$', '', 's')) as name,
       substring(r.r->>1 from '^(LOW|MED|HIGH)') as intensity, nullif(r.r->>2, '') as sat,
       silver.dm_n(r.r->>3)::int as pot, r.r->>4 as tr, silver.dm_n(r.r->>5)::int as mentor,
       trim(regexp_replace(r.r->>6, '^\d+-', '')) as pos, silver.dm_n(r.r->>7)::int as age,
       (select jsonb_object_agg(k.sk, silver.dm_n(r.r->>k.i)) from k) as skills,
       (select jsonb_object_agg(k.sk, substring(r.r->>k.i from '\s([+-]\d+)$')::int) from k
         where r.r->>k.i ~ '\s[+-]\d+$') as deltas,
       substring(r.r->>24 from '^([+-]?\d+)')::int as gained, substring(r.r->>24 from '/\s*([+-]?\d+)')::int as lost,
       silver.dm_n(r.r->>25) as price_change,
       silver.dm_n(substring(r.r->>0 from '([+-]?[\d.]+)::')) as value
from r
left join silver.dm_training_groups g on g.team_id = r.team_id and g.grp = r.grp
where jsonb_array_length(r.r) = 26 and r.r->>0 <> 'NAME';

-- Calendrier et résultats de la saison (tableau du club ; « (5:3) 0 : 0 » = tirs au but).
create or replace view silver.dm_fixtures with (security_invoker = true) as
select s.team_id, s.captured_at, o as ord,
       regexp_replace(r->>0, '^[\d.]+', '') as date_txt, regexp_replace(r->>1, '^[\d.]+', '') as time_txt,
       trim(regexp_replace(split_part(regexp_replace(r->>2, '\s+', ' ', 'g'), ':', 1), '\s+', ' ', 'g')) as competition,
       trim(split_part(regexp_replace(r->>2, '\s+', ' ', 'g'), ':', 2)) as round,
       silver.dm_n(r->>3)::int as attendance, r->>4 = 'H' as is_home,
       trim(regexp_replace(r->>5, '\s*\(.*\)$', '')) as opponent, substring(r->>5 from '\((.*)\)') as opp_rank,
       substring(r->>6 from '(\d+)\s*:\s*\d+\s*$')::int as gf_home_side,
       substring(r->>6 from '(\d+)\s*$')::int as ga_away_side,
       substring(r->>6 from '^\((\d+:\d+)\)') as shootout,
       nullif(r->>7, '') as my_result
from silver.dm_team_src s
cross join lateral jsonb_array_elements(s.tables) tb
cross join lateral jsonb_array_elements(tb->'rows') with ordinality x(r, o)
where jsonb_array_length(tb->'headers') = 8 and tb->'headers'->>2 ~ ':' and jsonb_array_length(r) = 8;

-- Matchs détaillés (réponse JSON /teams/<id>/matches : xG, possession, build up, tirs, formation, force).
create or replace view silver.dm_matches with (security_invoker = true) as
with src as (
  select distinct on ((payload->'body'->'team'->>'id')::int)
         (payload->'body'->'team'->>'id')::int as team_id, (payload->'body'->>'season')::int as season,
         captured_at, payload->'body'->'matches' as ms
  from bronze.raw_pages
  where game = 'derbymanager' and source = 'api' and payload->'body' ? 'matches' and payload->'body' ? 'team'
  order by (payload->'body'->'team'->>'id')::int, captured_at desc
)
select s.team_id, s.season, (m->>'id')::int as match_id, (m->>'date')::timestamptz as played_at,
       m->>'comp' as comp, m->>'compName' as comp_name, m->>'opp' as opponent, (m->>'home')::boolean as is_home,
       (m->>'gf')::int as gf, (m->>'ga')::int as ga,
       case when (m->>'gf')::int > (m->>'ga')::int then 'W' when (m->>'gf')::int < (m->>'ga')::int then 'L' else 'D' end as my_result,
       (m->>'xgf')::numeric as xgf, (m->>'xga')::numeric as xga, (m->>'xpts')::numeric as xpts,
       round((m->>'poss')::numeric * 100, 1) as poss_pct, m->>'formation' as formation,
       (m->'bu'->>0)::int as bu_a, (m->'bu'->>1)::int as bu_b, (m->'buOpp'->>0)::int as bu_opp_a, (m->'buOpp'->>1)::int as bu_opp_b,
       (m->'pass'->>0)::int as pass_a, (m->'pass'->>1)::int as pass_b, (m->>'passes')::int as passes,
       (m->'fouls'->>0)::int as fouls_for, (m->'fouls'->>1)::int as fouls_against,
       (m->'corners'->>0)::int as corners_for, (m->'corners'->>1)::int as corners_against,
       (m->>'counters')::int as counters, (m->>'countersOpp')::int as counters_opp,
       m->'strength' as strength, m->'types' as pass_types, m->'shots' as shots
from src s cross join lateral jsonb_array_elements(s.ms) m;

-- Tirs de chaque match (f = notre tir ; sq = origine : leftBuildUp, centre, counter, corner, freeKick, setPiece…).
create or replace view silver.dm_shots with (security_invoker = true) as
select m.team_id, m.match_id, m.played_at, m.opponent, (x->>'f')::boolean as ours,
       substring(x->>'m' from '\d+')::int as minute, x->>'k' as kind, x->>'r' as outcome, (x->>'bx')::boolean as in_box,
       trim(regexp_replace(x->>'by', '\s*\(.*\)$', '')) as player, substring(x->>'by' from '\((\w+)\)') as player_slot,
       x->>'sq' as sequence, x->>'src' as source, (x->>'xg')::numeric as xg
from silver.dm_matches m cross join lateral jsonb_array_elements(m.shots) x;

-- Finances (page /teams/<id>/finances) : tout est par jour.
create or replace view silver.dm_finances with (security_invoker = true) as
select p.team_id, p.captured_at,
       silver.dm_n(substring(p.text from 'MONEY ([\d,]+)')) as money,
       silver.dm_money(substring(p.text from 'SALARIES ([\d.]+[kM]?)')) as salaries_now,
       silver.dm_money(substring(p.text from 'SALARIES [\d.]+[kM]? \(([\d.]+[kM]?) /')) as salaries_committed,
       silver.dm_money(substring(p.text from 'SALARIES [\d.]+[kM]? \([\d.]+[kM]? / ([\d.]+[kM]?)\)')) as salary_cap,
       substring(p.text from 'Allowed salaries by expectation: (\d+)\w*') ::int as expectation_rank,
       substring(p.text from 'Allowed salaries by expectation: \d+\w* \((\d+)%\)')::int as expectation_pct,
       silver.dm_n(substring(p.text from 'Broadcasting rights ([\d,]+)')) as broadcasting,
       silver.dm_n(substring(p.text from 'Sponsorship deals ([\d,]+)')) as sponsorship,
       silver.dm_n(substring(p.text from 'Maintenance cost \(at \d+%\) (-?[\d,]+)')) as maintenance,
       silver.dm_n(substring(p.text from 'Team merchandise (-?[\d,]+)')) as merchandise,
       silver.dm_n(substring(p.text from 'Brand recognition (-?[\d,]+)')) as brand,
       silver.dm_n(substring(p.text from 'IFA subsidy (-?[\d,]+)')) as subsidy,
       silver.dm_n(substring(p.text from 'Youth school \([^)]*\) (-?[\d,]+)')) as youth_school,
       silver.dm_n(substring(p.text from 'Daily turnover (-?[\d,]+)')) as daily_turnover,
       silver.dm_n(substring(p.text from 'Estimated daily stadium revenue (-?[\d,]+)')) as stadium_daily,
       silver.dm_n(substring(p.text from 'Estimated daily turnover (-?[\d,]+)')) as daily_total
from silver.dm_pages p
where p.page_type = 'teams_id_finances';

-- Mouvements de la saison (page Finances, « Money flow ») : achats, ventes, prolongations, promotions de la school.
create or replace view silver.dm_money_flow with (security_invoker = true) as
with p as (select team_id, captured_at, text from silver.dm_pages where page_type = 'teams_id_finances'),
blocks as (
  select team_id, captured_at, b.kind, substring(text from b.re) as body
  from p cross join (values
    ('in',       'Money flow TRANSFERS Season \d+ In DATE NAME FROM PRICE (.*?) -?[\d.]+M Out'),
    ('out',      ' Out DATE NAME TO PRICE (.*?) -?[\d.]+M Extended'),
    ('extended', ' Extended DATE NAME PRICE (.*?) -?[\d.]+M Promoted'),
    ('promoted', ' Promoted DATE NAME PRICE (.*?) -?[\d.]+M\s*$')) b(kind, re)
)
select team_id, captured_at, kind, m[1] as date_txt, trim(m[2]) as name, m[3] as pos, m[4]::int as age,
       nullif(trim(m[5]), '') as other_club, silver.dm_money(m[6]) as amount
from blocks
cross join lateral regexp_matches(coalesce(body, ''),
  '(\w{3} \d{1,2}) ([^,]+), ([A-Z/]+), (\d+) ?(.*?) (-?[\d.]+[kM])(?= \w{3} \d{1,2} |$)', 'g') m;

-- Installations et stade (page /teams/<id>/facilities).
create or replace view silver.dm_facilities with (security_invoker = true) as
select p.team_id, p.captured_at,
       substring(p.text from 'REPUTATION (\d+)')::int as reputation,
       substring(p.text from 'FACILITIES (\d+):')::int as facilities_level,
       substring(p.text from 'FACILITIES \d+: (\w+)') as facilities_tier,
       substring(p.text from 'Maintenance (\d+)%')::int as maintenance_pct,
       silver.dm_money(substring(p.text from 'Downgrade at: (-?[\d.]+[kM]?)')) as downgrade_at,
       silver.dm_money(substring(p.text from 'Current value: (-?[\d.]+[kM]?)')) as current_value,
       silver.dm_money(substring(p.text from 'Daily change: (-?[\d.]+[kM]?)')) as daily_change,
       silver.dm_money(substring(p.text from 'Upgrade at: (-?[\d.]+[kM]?)')) as upgrade_at,
       substring(p.text from 'Capacity: (\d+)')::int as stadium_capacity,
       substring(p.text from 'Upkeep at: (\d+)%')::int as stadium_upkeep_pct,
       substring(p.text from 'Features (.*?) Facilities over time') as stadium_features
from silver.dm_pages p
where p.page_type = 'teams_id_facilities';

-- School : prospects (texte de la page /teams/<id>/school) et leurs compétences.
create or replace view silver.dm_school with (security_invoker = true) as
select p.team_id, p.captured_at, trim(m[1]) as name, m[2] as pos, m[3] as until_txt, m[4]::int as days_left,
       m[5] as country, m[6]::int as age, m[7]::int as height_cm, m[8]::int as weight_kg, m[9] as foot,
       m[10] as skills_txt, m[11] as tested, m[12] as natural_fitness, m[13] as potential_level,
       m[14] as potential_target, m[15] as personality
from silver.dm_pages p
cross join lateral regexp_matches(p.text,
  '([A-ZÀ-Ý][^,]{2,40}?), ([A-Z/]{1,5}) N/A Until: (\w{3} \d{1,2}) \((\d+) days left\) ([\w ]+?) (\d+) years \(days until birthday: \d+\) (\d+)cm, (\d+)kg, (\w+) footed (.*?) (Untested|Tested) youngster with (\w+) natural fitness\. He has (\w+) potential to become an? ([\w ]+?)\. He shows an? ([\w-]+) personality',
  'g') m
where p.page_type = 'teams_id_school';

-- Classement de la ligue (page /competitions/<ligue>/<saison>).
create or replace view silver.dm_standings with (security_invoker = true) as
select p.captured_at, substring(p.text from '([A-Z][A-Z -]+), SEASON \d+') as competition,
       substring(p.text from 'SEASON (\d+)')::int as season,
       m[1]::int as rank, trim(m[2]) as team, m[3]::int as played, m[4]::int as w, m[5]::int as d, m[6]::int as l,
       m[7]::int as gf, m[8]::int as ga, m[9]::int as gd, m[10]::int as pts, m[11] as form
from silver.dm_pages p
cross join lateral regexp_matches(substring(p.text from 'PTS FORM (.*)$'),
  '(\d+) ([A-Za-zÀ-ÿ .''-]+?) (\d+) (\d+) (\d+) (\d+) (\d+) : (\d+) ([+-]?\d+) (\d+) ((?:[WDL] ?){1,5})', 'g') m
where p.page_type = 'competitions_id';

-- Marché : joueurs à vendre (tableau 1 du marché : fourchettes de compétences « 2-9 » vues par nos scouts).
create or replace view silver.dm_market with (security_invoker = true) as
with p as (select * from silver.dm_pages where page_type in ('market', 'market_regions-tab') order by captured_at desc limit 1),
k(i, sk) as (values (12,'han'),(13,'mar'),(14,'tac'),(15,'posi'),(16,'aer'),(17,'agi'),(18,'ant'),(19,'cre'),
                    (20,'pas'),(21,'bal'),(22,'fir'),(23,'tec'),(24,'acc'),(25,'sho'),(26,'hea'),(27,'rea'))
select p.team_id as viewer_team_id, p.captured_at, r->>1 as name, r->>2 as team, nullif(r->>3, '') as decision,
       regexp_replace(r->>4, '^\d+-', '') as pos, silver.dm_n(r->>5)::int as age, nullif(r->>6, '') as country,
       silver.dm_money(regexp_replace(r->>8, '^[\d.]+::', '')) as salary, r->>9 as duration,
       trim(regexp_replace(r->>10, '^\d+', '')) as tier,
       silver.dm_money(regexp_replace(r->>11, '^([\d.]+::)+', '')) as price,
       (select jsonb_object_agg(k.sk, substring(r->>k.i from '::(\d+-\d+)$')) from k) as skill_ranges,
       (select round(avg(silver.dm_n(split_part(substring(r->>k.i from '::(\d+-\d+)$'), '-', 1))), 1) from k) as avg_min,
       (select round(avg(silver.dm_n(split_part(substring(r->>k.i from '::(\d+-\d+)$'), '-', 2))), 1) from k) as avg_max
from p cross join lateral jsonb_array_elements(p.tables) tb
cross join lateral jsonb_array_elements(tb->'rows') r
where tb->'headers'->>3 = 'DECISION' and jsonb_array_length(r) >= 28;

-- Transferts conclus (page /transfers, semaine affichée) : base de prix par âge, poste et niveau.
create or replace view silver.dm_transfers with (security_invoker = true) as
with p as (select * from silver.dm_pages where page_type = 'transfers' order by captured_at desc limit 1)
select p.captured_at, r->>0 as name, silver.dm_n(r->>1)::int as age, r->>2 as pos, r->>3 as tier,
       r->>4 as from_club, r->>5 as to_club, silver.dm_money(r->>6) as price, silver.dm_money(r->>7) as fees,
       silver.dm_money(r->>8) as salary, r->>9 as status, r->>10 as date_txt
from p cross join lateral jsonb_array_elements(p.tables) tb
cross join lateral jsonb_array_elements(tb->'rows') r
where tb->'headers'->>0 = 'NAME' and tb->'headers'->>6 = 'PRICE' and jsonb_array_length(r) = 11;

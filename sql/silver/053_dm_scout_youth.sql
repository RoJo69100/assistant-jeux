-- Derby Manager : jeunes découverts par nos scouts (Market > Scouting, onglet régions), conçu le 2026-11-02.
-- Demande : « est-ce que tu as tout mis dans des golds ? » ; l'école se compare aux jeunes découverts
-- (offrir un contrat à un jeune découvert le place à l'école, utilisateur 2026-11-02).
-- Source : bronze.raw_pages page_type 'market_regions-tab' (payload.club = notre club).
--   payload.tables[1..11] = une table par région, dans l'ordre de l'écran (England … Asia & North America),
--   colonnes S NAME POS AGE COU + 16 compétences ; S = nombre de scouts reçus (niveau de scout).
--   payload.tables[12] = liste des jeunes découverts (S NAME TEAM POS AGE COU REG STA SAL TIER PRI LISTED EXPIRES).
-- Cellules : « 1.9::1-9 » (clé de tri :: affichage), « 1-5 » ou « 6 ». Dernière capture par club (chaque capture a les 11 régions).

create or replace function silver.dm_range(c text) returns int[] language sql immutable as $$
  select case when d ~ '^\d+(-\d+)?$'
              then array[split_part(d, '-', 1)::int, coalesce(nullif(split_part(d, '-', 2), ''), split_part(d, '-', 1))::int] end
  from (select trim(case when c like '%::%' then split_part(c, '::', 2) else c end) as d) x
$$;

create or replace view silver.dm_scout_youth with (security_invoker = true) as
with cap as (
  select distinct on ((payload->>'club')::int)
         id as capture_id, captured_at, (payload->>'club')::int as team_id, payload->'tables' as t
  from bronze.raw_pages
  where game = 'derbymanager' and page_type = 'market_regions-tab' and payload->>'club' ~ '^\d+$'
    and jsonb_typeof(payload->'tables') = 'array' and jsonb_array_length(payload->'tables') >= 13
  order by (payload->>'club')::int, captured_at desc
),
reg as (
  select region, i::int as i
  from unnest(array['England','Spain','Germany','France','Italy','North Europe','Central Europe',
                    'East Europe','Africa','South America','Asia & North America']) with ordinality u(region, i)
),
lignes as (
  select c.team_id, c.capture_id, c.captured_at, reg.region, r
  from cap c cross join reg
  cross join lateral jsonb_array_elements(c.t->reg.i->'rows') r
  where jsonb_array_length(r) >= 21
),
liste as (
  select c.team_id, trim(r->>1) as name,
         nullif(regexp_replace(r->>9, '^\d+', ''), '') as tier,
         substring(r->>12 from '([A-Z][a-z]{2} \d{1,2})$') as expire
  from cap c cross join lateral jsonb_array_elements(c.t->12->'rows') r
  where jsonb_array_length(r) >= 13
)
select l.team_id, l.captured_at, l.region,
       nullif(l.r->>0, '')::int as scouts,
       trim(l.r->>1) as name,
       regexp_replace(l.r->>2, '^\d+-', '') as pos,
       nullif(l.r->>3, '')::int as age,
       nullif(l.r->>4, '') as pays,
       s.moy_min, s.moy_max, s.competences,
       li.tier, li.expire
from lignes l
cross join lateral (
  select round(avg((silver.dm_range(l.r->>k))[1]), 1) as moy_min,
         round(avg((silver.dm_range(l.r->>k))[2]), 1) as moy_max,
         string_agg(h.lbl || ' ' || trim(case when l.r->>k like '%::%' then split_part(l.r->>k, '::', 2) else l.r->>k end),
                    ' · ' order by k) as competences
  from generate_series(5, 20) k
  join (values (5,'HAN'),(6,'MAR'),(7,'TAC'),(8,'POS'),(9,'AER'),(10,'AGI'),(11,'ANT'),(12,'CRE'),
               (13,'PAS'),(14,'BAL'),(15,'FIR'),(16,'TEC'),(17,'ACC'),(18,'SHO'),(19,'HEA'),(20,'REA')) h(k2, lbl)
    on h.k2 = k
) s
left join liste li on li.team_id = l.team_id and li.name = trim(l.r->>1);

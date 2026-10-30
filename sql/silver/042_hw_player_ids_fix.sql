-- Hardwood : hw_player_ids prenait encore des noms abrégés écrits avec une espace insécable (« E.&nbsp;Corey »),
-- d'où 12 joueurs du roster sans player_id. On écarte toute forme abrégée et on décode &nbsp;.
-- hw_player_profile reprend le nom complet de hw_player_ids corrigé.

create or replace view silver.hw_player_ids with (security_invoker = true) as
select distinct on ((m[1])::int) (m[1])::int as player_id, trim(replace(m[2], '&nbsp;', ' ')) as name
from silver.hw_pages p,
     regexp_matches(coalesce(p.html, ''), 'href="/player/(\d+)"[^>]*>([^<]+)</a>', 'g') m
where replace(m[2], '&nbsp;', ' ') !~ '^\s*[A-Z]\.\s'
order by (m[1])::int, p.captured_at desc;

create or replace view silver.hw_player_profile with (security_invoker = true) as
with p as (
  select p.captured_at, p.url_id as player_id,
         (select string_agg(x::text, ' ') from jsonb_array_elements(p.tables->0->'rows') x) as flat
  from silver.hw_pages p
  where p.page_type = 'player_id'
)
select player_id, i.name, captured_at,
       substring(flat from 'Age: (\d+)')::int as age,
       substring(flat from 'Shoots: (\w+)') as shoots,
       substring(flat from 'Weight: (\d+) kgs')::int as weight_kg,
       substring(flat from 'Wingspan: ([\d.]+) m')::numeric as wingspan_m,
       substring(flat from 'Vertical: ([\d.]+) cm')::numeric as vertical_cm,
       substring(flat from 'Home Town: (.+?)  ') as hometown,
       substring(flat from 'Junior College: (.+?)  ') as junior_college,
       substring(flat from 'Projected Height: ([\d.]+) m')::numeric as projected_height_m,
       trim(substring(flat from 'Recruiting Evaluation: (.*?) Projected Height')) as evaluation
from p left join silver.hw_player_ids i using (player_id);

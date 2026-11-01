-- Hardwood : une page de vérification Cloudflare (« Un instant… », 0 tableau) capturée après la vraie page
-- devenait la dernière version de l'URL et effaçait la recrue de silver.hw_recruit_page (Lyle Tolliver, 31/10 09:50 UTC).
-- silver.hw_pages ignore désormais ces captures : la dernière vraie page de l'URL reste lue.
create or replace view silver.hw_pages as
select distinct on (page_url) id as capture_id,
       captured_at,
       (captured_at at time zone 'Europe/Paris')::date as day,
       page_type,
       page_url,
       nullif(substring(page_url, '/(\d+)(?:/|$)'), '')::integer as url_id,
       substring(payload ->> 'text', 'Game Date: ([A-Za-z]+ \d+[a-z]{2}, \d{4})') as game_date_txt,
       payload -> 'tables' as tables,
       payload -> 'fields' as fields,
       payload ->> 'text' as text,
       payload ->> 'html' as html
from bronze.raw_pages r
where game = 'hardwood' and source = 'dom'
  -- Le titre suffit (les 4 captures Cloudflare du 31/10 l'ont) ; un filtre regex sur le texte faisait expirer les vues gold.
  and coalesce(payload ->> 'title', '') !~* '^(Just a moment|Un instant)'
order by page_url, captured_at desc;

-- Hardwood : hw_coach_market ne lisait que tables->1 de /coach_results. La page change de disposition selon le coach
-- à remplacer (head : 2 tables, assistants : 1 table de 616 lignes) et silver.hw_pages ne garde que la dernière copie
-- de l'URL : l'export assistant (30/10 16:58) masquait l'export head coach. On lit donc bronze, une liste par coach à remplacer.
-- Colonnes : to_replace = « Head Coach X » ou « Assistant Coach X » ; nos propres coachs (EUREK) sont exclus.

create or replace view silver.hw_coach_market with (security_invoker = true) as
with last_per_target as (
  select distinct on (substring(r.payload->>'text' from 'To Replace: ([^\n]+)'))
         r.captured_at, r.payload, substring(r.payload->>'text' from 'To Replace: ([^\n]+)') as to_replace
  from bronze.raw_pages r
  where r.game = 'hardwood' and r.source = 'dom' and r.page_type = 'coach_results'
  order by substring(r.payload->>'text' from 'To Replace: ([^\n]+)'), r.captured_at desc
)
select l.captured_at, l.to_replace,
       c->>1 as coach, c->>2 as team, (c->>2) = 'Available' as available,
       (c->>3)::int as age, (c->>4)::int as exp,
       (c->>5)::int as off, (c->>6)::int as def, (c->>7)::int as tac, (c->>8)::int as dev,
       (c->>9)::int as mot, (c->>10)::int as rec,
       replace(replace(c->>11, '$', ''), 'M', '')::numeric as salary_m
from last_per_target l
cross join lateral jsonb_array_elements(l.payload->'tables') t
cross join lateral jsonb_array_elements(t->'rows') c
where jsonb_array_length(c) >= 12 and (c->>3) ~ '^\d+$' and (c->>2) <> 'EUREK';

-- gold.hw_coach_board : le tableau « libre » filtre maintenant sur le coach à remplacer (paramètre dans la vue : tous).

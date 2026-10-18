-- Silver BasketVibe : news de l'admin (page /news, API /news?limit=N → body.posts).
-- Une ligne par post, dernière capture gardée. Sert à la veille : lire les posts publiés après la dernière lecture.

create or replace view silver.bv_news with (security_invoker = true) as
select distinct on (p->>'id')
       (p->>'id')::uuid                  as post_id,
       (p->>'published_at')::timestamptz as published_at,
       p->>'title'                       as title,
       p->>'body_markdown'               as body,
       (p->>'has_poll')::bool            as has_poll,
       p->'poll'                         as poll,
       (p->>'comment_count')::int        as comment_count,
       a.captured_at
from silver.bv_api a
cross join lateral jsonb_array_elements(a.body->'posts') p
where a.endpoint = '/news'
order by p->>'id', a.captured_at desc;

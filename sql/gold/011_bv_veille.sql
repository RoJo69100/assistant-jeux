-- Silver / Gold BasketVibe : fil de veille (agent Veille).
-- Discord (bronze.discord_messages, export hebdomadaire de l'utilisateur) + News de l'admin (silver.bv_news).
-- L'agent ne lit que le delta : posts publiés après la date notée dans outputs/basketvibe/veille/etat.md.

create or replace view silver.bv_discord_messages with (security_invoker = true) as
select m.id, m.channel, m.author, m.posted_at,
       m.payload->>'content' as content,
       m.author ilike 'vachacz%' as is_dev,   -- développeur unique du jeu (skill basketvibe-communaute)
       m.source_file, m.inserted_at
from bronze.discord_messages m
where m.game = 'basketvibe';

create or replace view gold.bv_veille_feed with (security_invoker = true) as
select 'news' as source, n.published_at as posted_at, 'admin' as author, true as is_dev, 'news' as channel,
       n.title || E'\n' || coalesce(n.body, '') as content, n.post_id::text as ref, n.captured_at as imported_at
from silver.bv_news n
union all
select 'discord', d.posted_at, d.author, d.is_dev, d.channel, d.content, d.id::text, d.inserted_at
from silver.bv_discord_messages d
where length(coalesce(d.content, '')) >= 20;   -- ignore les messages très courts (réactions, « merci »)

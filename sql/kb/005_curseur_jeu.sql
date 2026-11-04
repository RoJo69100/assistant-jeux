-- Refonte v2, 4.3 : le curseur se repère dans le message du même jeu (un id peut exister dans deux jeux).
create or replace function public.kb_lot(p_game text, p_after text, p_limit int default 50, p_min_len int default 60,
                                         p_officiels text[] default '{}')
returns jsonb
language sql
stable
security definer
set search_path = bronze, public
as $$
  select coalesce(jsonb_agg(jsonb_build_object('id', id, 'at', posted_at, 'channel', channel, 'author', author,
                                               'text', left(c, 1500)) order by posted_at, id), '[]')
  from (select m.id::text id, m.posted_at, m.channel, m.author,
               coalesce(m.payload->>'content', m.payload->>'text', '') c
        from bronze.discord_messages m
        where m.game = p_game
          and (p_after is null or (m.posted_at, m.id::text) > (select d.posted_at, d.id::text from bronze.discord_messages d
                                                              where d.id::text = p_after and d.game = p_game limit 1))
          and (length(coalesce(m.payload->>'content', m.payload->>'text', '')) >= p_min_len
               or lower(m.author) = any(p_officiels))
        order by m.posted_at, m.id
        limit p_limit) x
$$;

create or replace function public.kb_estimer(p_min_len int default 60, p_officiels text[] default '{}')
returns jsonb
language sql
stable
security definer
set search_path = bronze, kb, public
as $$
  select coalesce(jsonb_agg(x order by x->>'game'), '[]') from (
    select jsonb_build_object('game', m.game, 'messages', count(*),
             'caracteres', sum(length(coalesce(m.payload->>'content', m.payload->>'text', ''))),
             'officiels', count(*) filter (where lower(m.author) = any(p_officiels)),
             'curseur', (select last_id from kb.ingest_cursor k where k.game = m.game and k.source = 'bronze.discord_messages')) x
    from bronze.discord_messages m
    left join lateral (select d.posted_at, d.id::text did from bronze.discord_messages d, kb.ingest_cursor k
                       where k.game = m.game and k.source = 'bronze.discord_messages' and d.id::text = k.last_id
                         and d.game = m.game
                       limit 1) c on true
    where (c.posted_at is null or (m.posted_at, m.id::text) > (c.posted_at, c.did))
      and (length(coalesce(m.payload->>'content', m.payload->>'text', '')) >= p_min_len
           or lower(m.author) = any(p_officiels))
    group by m.game) t
$$;

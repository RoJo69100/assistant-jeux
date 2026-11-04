-- Refonte v2, étape 4.3 : ingestion Discord par lots (pipelines/kb_ingest.py).
-- public.kb_lot : messages suivants après le curseur (ordre posted_at, id), filtrés en SQL (longueur minimale,
--   auteurs officiels toujours gardés) ; public.kb_estimer : volume restant par jeu, sans rien lire en LLM.
-- public.kb_import accepte en plus p->'cursor' = {source, last_id} : le curseur n'avance qu'avec l'import du lot.

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
                                                              where d.id::text = p_after limit 1))
          and (length(coalesce(m.payload->>'content', m.payload->>'text', '')) >= p_min_len
               or lower(m.author) = any(p_officiels))
        order by m.posted_at, m.id
        limit p_limit) x
$$;
revoke all on function public.kb_lot(text, text, int, int, text[]) from public, anon, authenticated;
grant execute on function public.kb_lot(text, text, int, int, text[]) to service_role;

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
    left join lateral (select d.posted_at from bronze.discord_messages d, kb.ingest_cursor k
                       where k.game = m.game and k.source = 'bronze.discord_messages' and d.id::text = k.last_id
                       limit 1) c on true
    where (c.posted_at is null or m.posted_at > c.posted_at)
      and (length(coalesce(m.payload->>'content', m.payload->>'text', '')) >= p_min_len
           or lower(m.author) = any(p_officiels))
    group by m.game) t
$$;
revoke all on function public.kb_estimer(int, text[]) from public, anon, authenticated;
grant execute on function public.kb_estimer(int, text[]) to service_role;

create or replace function public.kb_import(p jsonb)
returns jsonb
language plpgsql
security definer
set search_path = kb, public
as $$
declare n_c int; n_s int;
begin
  insert into kb.claim (game, domain, text, source_kind, source_ref, author, said_at, status, import_key, origine)
  select x->>'game', x->>'domain', x->>'text', x->>'source_kind', x->>'source_ref', x->>'author',
         (x->>'said_at')::timestamptz, x->>'status', x->>'import_key', x->'origine'
  from jsonb_array_elements(coalesce(p->'claims', '[]')) x
  on conflict (import_key) do nothing;
  get diagnostics n_c = row_count;

  insert into kb.support (claim_id, author, source_ref, said_at)
  select c.id, y->>'author', y->>'source_ref', (y->>'said_at')::timestamptz
  from jsonb_array_elements(coalesce(p->'support', '[]')) y
  join kb.claim c on c.import_key = y->>'import_key'
  where c.author is distinct from y->>'author'
  on conflict do nothing;
  get diagnostics n_s = row_count;

  if p ? 'cursor' then
    insert into kb.ingest_cursor (game, source, last_id)
    values (p->>'game', p->'cursor'->>'source', p->'cursor'->>'last_id')
    on conflict (game, source) do update set last_id = excluded.last_id, updated_at = now();
  end if;

  perform kb.recompute_confidence(p->>'game');
  return jsonb_build_object('claims', n_c, 'support', n_s,
                            'total', (select count(*) from kb.claim where game = p->>'game'));
end $$;
revoke all on function public.kb_import(jsonb) from public, anon, authenticated;
grant execute on function public.kb_import(jsonb) to service_role;

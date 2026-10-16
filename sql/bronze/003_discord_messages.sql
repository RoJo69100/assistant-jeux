-- Bronze : messages Discord, tels qu'exportés (DiscordChatExporter, format texte), jamais modifiés.
-- Un message réexporté (exports qui se chevauchent) n'est inséré qu'une fois.

create table if not exists bronze.discord_messages (
  id             bigint generated always as identity primary key,
  game           text        not null,                 -- 'basketvibe'
  guild          text        not null,                 -- 'basketvibe.com'
  channel        text        not null,                 -- 'Community / help'
  author         text        not null,
  posted_local   text        not null,                 -- horodatage brut de l'export : 'dd/mm/yyyy HH:MM'
  posted_at      timestamptz not null,                 -- posted_local interprété dans le fuseau de l'export
  payload        jsonb       not null,                 -- {content, sections: {Attachments, Reactions, ...}, raw}
  content_sha256 text        not null,                 -- hash du texte du message, hors réactions
  source_file    text        not null,
  inserted_at    timestamptz not null default now(),
  unique (game, channel, author, posted_local, content_sha256)
);

create index if not exists discord_messages_game_time on bronze.discord_messages (game, posted_at desc);

alter table bronze.discord_messages enable row level security;

drop trigger if exists discord_messages_immutable on bronze.discord_messages;
create trigger discord_messages_immutable before update or delete on bronze.discord_messages
  for each row execute function bronze.forbid_change();

-- Point d'entrée de pipelines/import_discord.py : POST /rest/v1/rpc/ingest_discord_messages
-- p_items = [{game, guild, channel, author, posted_local, posted_at, payload, source_file}, ...]
create or replace function public.ingest_discord_messages(p_token text, p_items jsonb)
returns integer
language plpgsql security definer set search_path = '' as $$
declare
  n integer;
begin
  if not exists (
    select 1 from bronze.ingest_tokens
    where token_sha256 = encode(sha256(convert_to(p_token, 'UTF8')), 'hex')
  ) then
    raise exception 'jeton invalide' using errcode = '28000';
  end if;

  if jsonb_typeof(p_items) <> 'array' or jsonb_array_length(p_items) > 500 then
    raise exception 'p_items doit être un tableau de 500 éléments maximum';
  end if;

  insert into bronze.discord_messages (game, guild, channel, author, posted_local, posted_at, payload, content_sha256, source_file)
  select i->>'game', i->>'guild', i->>'channel', i->>'author', i->>'posted_local',
         (i->>'posted_at')::timestamptz, i->'payload',
         encode(sha256(convert_to(i->'payload'->>'content', 'UTF8')), 'hex'),
         i->>'source_file'
  from jsonb_array_elements(p_items) as i
  on conflict do nothing;

  get diagnostics n = row_count;
  return n;
end $$;

revoke all on function public.ingest_discord_messages(text, jsonb) from public, authenticated;
grant execute on function public.ingest_discord_messages(text, jsonb) to anon;

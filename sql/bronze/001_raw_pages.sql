-- Bronze : JSON brut daté, jamais modifié.
-- Une ligne = une capture (réponse JSON interceptée ou instantané DOM) d'une page ouverte par l'utilisateur.

create schema if not exists bronze;

create table if not exists bronze.raw_pages (
  id             bigint generated always as identity primary key,
  game           text        not null,                 -- 'basketvibe'
  page_type      text        not null,                 -- 'roster', 'match', 'finance'... (voir userscript)
  page_url       text        not null,                 -- URL de la page ouverte
  source         text        not null,                 -- 'api' (réponse interceptée) ou 'dom' (instantané)
  source_url     text,                                 -- URL de la requête interceptée (null pour 'dom')
  captured_at    timestamptz not null,                 -- horodatage navigateur
  payload        jsonb       not null,
  payload_sha256 text        not null,
  client         text,                                 -- version du script
  inserted_at    timestamptz not null default now(),
  unique nulls not distinct (game, page_type, source, source_url, payload_sha256)  -- source_url null pour 'dom'
);

create index if not exists raw_pages_game_type_time on bronze.raw_pages (game, page_type, captured_at desc);

alter table bronze.raw_pages enable row level security;

-- Immuabilité : aucune mise à jour ni suppression.
create or replace function bronze.forbid_change() returns trigger
language plpgsql set search_path = '' as $$
begin
  raise exception 'bronze.% est en écriture seule', tg_table_name;
end $$;

drop trigger if exists raw_pages_immutable on bronze.raw_pages;
create trigger raw_pages_immutable before update or delete on bronze.raw_pages
  for each row execute function bronze.forbid_change();

-- Jetons d'ingestion (seul le hash SHA-256 est stocké).
create table if not exists bronze.ingest_tokens (
  token_sha256 text primary key,
  label        text not null,
  created_at   timestamptz not null default now()
);
alter table bronze.ingest_tokens enable row level security;

-- Point d'entrée unique du userscript : POST /rest/v1/rpc/ingest_raw_pages
-- p_items = [{game, page_type, page_url, source, source_url, captured_at, payload, client}, ...]
create or replace function public.ingest_raw_pages(p_token text, p_items jsonb)
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

  insert into bronze.raw_pages (game, page_type, page_url, source, source_url, captured_at, payload, payload_sha256, client)
  select i->>'game', i->>'page_type', i->>'page_url', i->>'source', i->>'source_url',
         (i->>'captured_at')::timestamptz, i->'payload',
         encode(sha256(convert_to((i->'payload')::text, 'UTF8')), 'hex'),
         i->>'client'
  from jsonb_array_elements(p_items) as i
  on conflict do nothing;

  get diagnostics n = row_count;
  return n;
end $$;

revoke all on schema bronze from public, anon, authenticated;
revoke all on function public.ingest_raw_pages(text, jsonb) from public;
grant execute on function public.ingest_raw_pages(text, jsonb) to anon;

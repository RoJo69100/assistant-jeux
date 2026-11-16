-- Brique « base », étape 3 (2026-11-16) : export du bronze par RPC, sans clé de service.
-- public.export_bronze(p_token, p_table, p_apres_id, p_limite) : lecture seule, deux tables seulement
-- (raw_pages, discord_messages), 5000 lignes au plus par appel, appelable avec la clé publishable (rôle anon) + un jeton.
--   p_limite >= 1 : lignes d'id > p_apres_id, par id croissant, sous forme d'un tableau JSON (une ligne = to_jsonb de la ligne) ;
--                   la réponse s'arrête avant 3 Mo de payload comprimé cumulé (au moins une ligne) : le client boucle jusqu'à un tableau vide.
--   p_limite = 0  : comptage, renvoie [{"n": count(id <= p_apres_id)}] (contrôle de la sauvegarde, le bronze étant immuable).
-- Jeton : table séparée du jeton d'ingestion (bronze.ingest_tokens), seul le hash SHA-256 est stocké, révocable (revoked_at).
-- Créer un jeton (hors dépôt) : le tirer au hasard sur le poste, ne stocker ici que son hash :
--   insert into bronze.export_tokens (token_sha256, label) values ('<sha256 hex du jeton>', 'poste-remy');
-- Révoquer : update bronze.export_tokens set revoked_at = now() where label = 'poste-remy';

create table if not exists bronze.export_tokens (
  token_sha256 text primary key,
  label        text not null,
  created_at   timestamptz not null default now(),
  revoked_at   timestamptz
);
alter table bronze.export_tokens enable row level security;
revoke all on bronze.export_tokens from public, anon, authenticated;

create or replace function public.export_bronze(p_token text, p_table text, p_apres_id bigint, p_limite integer)
returns jsonb
language plpgsql stable security definer set search_path = '' set statement_timeout = '25s' as $$
declare
  r jsonb;
  n integer := least(greatest(coalesce(p_limite, 0), 0), 5000);
begin
  if p_token is null or not exists (
    select 1 from bronze.export_tokens
    where token_sha256 = encode(sha256(convert_to(p_token, 'UTF8')), 'hex') and revoked_at is null
  ) then
    raise exception 'jeton invalide' using errcode = '28000';
  end if;
  if p_table not in ('raw_pages', 'discord_messages') then
    raise exception 'table non exportable : %', p_table using errcode = '22023';
  end if;
  if p_apres_id is null or p_apres_id < 0 then
    raise exception 'p_apres_id doit être un entier >= 0' using errcode = '22023';
  end if;

  if n = 0 then
    if p_table = 'raw_pages' then
      select jsonb_build_array(jsonb_build_object('n', count(*))) into r from bronze.raw_pages where id <= p_apres_id;
    else
      select jsonb_build_array(jsonb_build_object('n', count(*))) into r from bronze.discord_messages where id <= p_apres_id;
    end if;
  elsif p_table = 'raw_pages' then
    -- plafond d'octets (payload comprimé cumulé, au moins une ligne) : 5000 pages de 40 Ko saturent la mémoire de l'API (522 le 2026-11-16)
    select coalesce(jsonb_agg(to_jsonb(z.x) order by z.id), '[]'::jsonb) into r
    from (select y.id, y, sum(pg_column_size(y.payload)) over (order by y.id) - pg_column_size(y.payload) as avant
          from (select * from bronze.raw_pages where id > p_apres_id order by id limit n) y) z(id, x, avant)
    where z.avant < 3000000;
  else
    select coalesce(jsonb_agg(to_jsonb(z.x) order by z.id), '[]'::jsonb) into r
    from (select y.id, y, sum(pg_column_size(y.payload)) over (order by y.id) - pg_column_size(y.payload) as avant
          from (select * from bronze.discord_messages where id > p_apres_id order by id limit n) y) z(id, x, avant)
    where z.avant < 3000000;
  end if;
  return r;
end $$;

revoke all on function public.export_bronze(text, text, bigint, integer) from public, authenticated;
grant execute on function public.export_bronze(text, text, bigint, integer) to anon, service_role;

-- Refonte v2, étape 0.4 : rôle Postgres en lecture seule pour pipelines/sql.py.
-- Le mot de passe n'est PAS dans ce fichier : il est posé à part (alter role ... password) et gardé dans .env (SUPABASE_DB_URL_RO).
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'assistant_ro') then
    create role assistant_ro nologin;
  end if;
end $$;

alter role assistant_ro set default_transaction_read_only = on;
alter role assistant_ro set statement_timeout = '20s';

grant usage on schema silver, gold to assistant_ro;
grant select on all tables in schema silver to assistant_ro;
grant select on all tables in schema gold to assistant_ro;
alter default privileges in schema silver grant select on tables to assistant_ro;
alter default privileges in schema gold grant select on tables to assistant_ro;

-- bronze : métadonnées seulement, jamais le payload complet ni le contenu des messages
grant usage on schema bronze to assistant_ro;
grant select (id, game, page_type, page_url, source, source_url, captured_at, payload_sha256, client, inserted_at)
  on bronze.raw_pages to assistant_ro;
grant select (id, game, guild, channel, posted_local, posted_at, content_sha256, source_file, inserted_at)
  on bronze.discord_messages to assistant_ro;

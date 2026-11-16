-- Brique « base », étape 3 (2026-11-16) : registre de lecture des pages pour les 6 jeux.
-- core.type_page(source, page_type, source_url) : normaliseur d'adresses commun à tous les jeux (repris de gold.bv_couverture_pages, 022) :
--   capture API : chemin sans hôte ni paramètres, uuid -> <id>, /clubs/<slug>, /regions/<code>, nombres -> <n> ;
--   capture DOM : « dom:<page_type> ».
-- core.page_ignore (game, motif, raison) : types de page ignorés exprès (motif = regex sur le type de page) ; sans alerte « non lue ».
--   Table vide à la création : c'est l'utilisateur qui trie.

create or replace function core.type_page(p_source text, p_page_type text, p_source_url text) returns text
language sql immutable set search_path = '' as $$
  select case when p_source = 'dom' then 'dom:' || p_page_type
         else regexp_replace(
                regexp_replace(
                  regexp_replace(
                    regexp_replace(
                      regexp_replace(split_part(p_source_url, '?', 1), '^https?://[^/]+', ''),
                      '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<id>', 'g'),
                    '/clubs/[^/]+', '/clubs/<slug>'),
                  '/regions/[^/]+', '/regions/<code>'),
                '/[0-9]+(/|$)', '/<n>\1', 'g') end
$$;
grant execute on function core.type_page(text, text, text) to assistant_ro;

create table if not exists core.page_ignore (
  game   text not null,
  motif  text not null,
  raison text not null,
  primary key (game, motif)
);
alter table core.page_ignore enable row level security;
drop policy if exists assistant_ro_select on core.page_ignore;
create policy assistant_ro_select on core.page_ignore for select to assistant_ro using (true);
grant select on core.page_ignore to assistant_ro;

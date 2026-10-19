-- Dédoublonnage de bronze.raw_pages sur une empreinte de source_url (2026-10-19).
-- Team Soccer (forum) appelle son API avec des adresses de plusieurs milliers de caractères : l'index unique sur
-- source_url en clair refusait l'insertion (erreur 54000, ligne d'index > 1/3 de page). Même règle d'unicité,
-- l'adresse est remplacée par son md5 ; ingest_raw_pages (« on conflict do nothing ») n'a pas besoin de changer.

alter table bronze.raw_pages drop constraint raw_pages_game_page_type_source_source_url_payload_sha256_key;

create unique index raw_pages_dedup on bronze.raw_pages
  (game, page_type, source, md5(coalesce(source_url, '')), payload_sha256);

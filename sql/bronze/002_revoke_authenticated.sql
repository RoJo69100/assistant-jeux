-- Seul anon (le userscript, avec jeton) appelle l'ingestion ; Supabase accorde EXECUTE à authenticated par défaut.
revoke execute on function public.ingest_raw_pages(text, jsonb) from authenticated;

-- Refonte v2, étape 0.4 : lecture ciblée d'un morceau de payload bronze pour pipelines/sql.py --payload-path.
-- Le rôle assistant_ro n'a pas accès à bronze.raw_pages.payload en entier : seulement à un chemin JSON d'une page.
create or replace function bronze.payload_at(p_id bigint, p_path text[])
returns jsonb
language sql
stable
security definer
set search_path = ''
as $$
  select payload #> p_path from bronze.raw_pages where id = p_id
$$;

revoke all on function bronze.payload_at(bigint, text[]) from public, anon, authenticated;
grant execute on function bronze.payload_at(bigint, text[]) to assistant_ro;

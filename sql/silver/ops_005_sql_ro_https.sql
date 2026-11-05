-- Lecture SQL en HTTPS pour pipelines/sql.py quand le port 5432 est fermé (sessions cloud : le proxy ne laisse sortir que le 443).
-- Appel : GET {SUPABASE_URL}/rest/v1/rpc/sql_ro?q=... avec la clé secrète (service_role) ; anon et authenticated refusés.
-- Verrous : la fonction appartient à assistant_ro (droits de lecture), elle est STABLE (PostgREST l'exécute en transaction
-- en lecture seule, même en POST), elle refuse toute transaction en écriture, et la requête est enveloppée dans une
-- sous-requête (un WITH ... INSERT y est refusé).
-- Appliquée en deux migrations Supabase : ops_005_sql_ro_https puis ops_005b_sql_ro_revoke_anon (le changement de
-- propriétaire réattribue les droits à assistant_ro : la révocation doit se faire sous ce rôle).
create or replace function public.sql_ro(q text)
returns json
language plpgsql
stable
security definer
set search_path = ''
set statement_timeout = '20s'
as $$
declare
  r json;
begin
  if current_setting('transaction_read_only') <> 'on' then
    raise exception 'sql_ro : lecture seule, appel en GET uniquement';
  end if;
  execute format('select coalesce(json_agg(t), ''[]''::json) from (%s) t', q) into r;
  return r;
end
$$;

-- postgres doit être membre d'assistant_ro (changement de propriétaire et révocations), le temps de ces instructions.
grant assistant_ro to postgres;
grant create on schema public to assistant_ro;
alter function public.sql_ro(text) owner to assistant_ro;
revoke create on schema public from assistant_ro;
set role assistant_ro;
revoke all on function public.sql_ro(text) from public, anon, authenticated;
grant execute on function public.sql_ro(text) to service_role;
reset role;
revoke assistant_ro from postgres;

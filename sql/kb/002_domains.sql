-- Refonte v2, étape 4.4 : liste des thèmes d'un jeu pour pipelines/kb.py --domaines.
create or replace function public.kb_domains(p_game text)
returns jsonb
language sql
stable
security definer
set search_path = kb, public
as $$
  select coalesce(jsonb_agg(jsonb_build_object('domain', domain, 'n', n) order by n desc), '[]')
  from (select domain, count(*) n from kb.claim where game = p_game and status <> 'obsolete' group by 1) d
$$;
revoke all on function public.kb_domains(text) from public, anon, authenticated;
grant execute on function public.kb_domains(text) to service_role, assistant_ro;

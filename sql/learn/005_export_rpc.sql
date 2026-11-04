-- Refonte v2, étape 3.5 : lecture de learn.* pour pipelines/export_learnings_md.py quand il n'y a pas d'URL Postgres
-- (session cloud) : REST rpc avec la clé secrète, exécutable par service_role seulement. Lecture seule.

create or replace function public.learn_export(p_game text)
returns jsonb
language sql
stable
security definer
set search_path = learn, public
as $$
  select jsonb_build_object(
    'lessons', coalesce((select jsonb_agg(jsonb_build_object(
        'id', l.id, 'claim', l.claim, 'status', l.status, 'n_for', l.n_for, 'n_against', l.n_against,
        'created_at', l.created_at, 'origine', l.origine) order by l.created_at, l.id)
      from learn.lesson l where l.game = p_game), '[]'),
    'decisions', coalesce((select jsonb_agg(jsonb_build_object(
        'id', d.id, 'label', d.label, 'status', d.status, 'prediction', d.prediction,
        'decided_at', d.decided_at, 'origine', d.origine, 'verdict', o.verdict) order by d.decided_at, d.id)
      from learn.decision d left join learn.outcome o on o.decision_id = d.id where d.game = p_game), '[]'))
$$;

revoke all on function public.learn_export(text) from public, anon, authenticated;
grant execute on function public.learn_export(text) to service_role;

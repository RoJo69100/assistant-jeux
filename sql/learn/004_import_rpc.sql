-- Refonte v2, étape 3.5 : point d'entrée d'import vers learn.* (pipelines/migrer_learnings.py).
-- Appelé en REST (rpc) avec la clé secrète : exécutable par service_role seulement, jamais par anon/authenticated.
-- Idempotent : une leçon (id), une décision migrée (origine jeu + ordre) ou une erreur (ref) déjà présente est ignorée.
-- Pas de « drop policy » (règle N3).

create or replace function public.learn_import(p jsonb)
returns jsonb
language plpgsql
security definer
set search_path = learn, public
as $$
declare
  n_l int; n_d int; n_e int;
begin
  insert into learn.lesson (id, game, domain, claim, status, n_for, n_against, created_at, origine)
  select x->>'id', x->>'game', x->>'domain', x->>'claim', x->>'status',
         (x->>'n_for')::int, (x->>'n_against')::int, (x->>'created_at')::timestamptz, x->'origine'
  from jsonb_array_elements(coalesce(p->'lessons', '[]')) x
  on conflict do nothing;
  get diagnostics n_l = row_count;

  insert into learn.decision (game, domain, decided_at, label, hypothesis, prediction, eval_after, status, origine)
  select x->>'game', x->>'domain', (x->>'decided_at')::timestamptz, x->>'label', x->>'hypothesis',
         x->'prediction', (x->>'eval_after')::timestamptz, x->>'status', x->'origine'
  from jsonb_array_elements(coalesce(p->'decisions', '[]')) x
  on conflict do nothing;
  get diagnostics n_d = row_count;

  insert into learn.error (game, description, recurrence, enforcement, guard_ref, closed_at, ref)
  select x->>'game', x->>'description', 1, x->>'enforcement', x->>'guard_ref',
         (x->>'closed_at')::timestamptz, x->>'ref'
  from jsonb_array_elements(coalesce(p->'errors', '[]')) x
  on conflict do nothing;
  get diagnostics n_e = row_count;

  return jsonb_build_object('lessons', n_l, 'decisions', n_d, 'errors', n_e);
end $$;

revoke all on function public.learn_import(jsonb) from public, anon, authenticated;
grant execute on function public.learn_import(jsonb) to service_role;

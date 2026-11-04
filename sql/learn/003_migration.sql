-- Refonte v2, étape 3.5 : migration des learnings.md et des règles E du triage vers learn.*.
-- origine : la ligne d'origine (jeu, section, ordre, cellules) ; sert à régénérer learnings.md à l'identique
-- (pipelines/export_learnings_md.py). Les conseils migrés (prediction.metric = 'migre') ne sont pas évalués :
-- leur critère est en prose ; seules les décisions my_result / sql passent par evaluer_decisions.py.
-- learn.error.ref : identifiant de la règle du triage (CM-xx, R-n, A-n, Lnn) ; une ligne par règle E.
-- Pas de « drop policy » (règle N3).

alter table learn.lesson   add column if not exists origine jsonb;
alter table learn.decision add column if not exists origine jsonb;
alter table learn.error    add column if not exists ref text;
create unique index if not exists error_ref_uq on learn.error (ref) where ref is not null;
create unique index if not exists decision_origine_uq on learn.decision
  ((origine->>'jeu'), ((origine->>'ordre')::int)) where origine is not null;

create or replace view gold.decisions_a_evaluer with (security_invoker = true) as
select d.*
from learn.decision d
where d.status in ('accepted', 'done') and d.eval_after <= now()
  and d.prediction->>'metric' in ('my_result', 'sql')
  and not exists (select 1 from learn.outcome o where o.decision_id = d.id);
grant select on gold.decisions_a_evaluer to assistant_ro;

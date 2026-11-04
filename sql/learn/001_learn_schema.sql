-- Refonte v2, étape 3.1 : journal de décisions et apprentissage (plan, annexe B.2).
-- « Ne pas se répéter » devient une propriété de la base : chaque conseil = une ligne de learn.decision
-- avec une prédiction mesurable ; l'évaluateur (3.3) écrit learn.outcome et fait évoluer learn.lesson.
-- Droits : assistant_ro lit tout ; il ajoute des décisions et des résultats, change le statut et la note
-- d'une décision (journal en ajout seul : ni suppression, ni réécriture de la prédiction).
-- Pas de « drop policy » (règle N3 : confirmation invisible via le connecteur).

create schema if not exists learn;
revoke all on schema learn from public, anon, authenticated;
grant usage on schema learn to assistant_ro;

create table if not exists learn.decision (
  id                bigint generated always as identity primary key,
  game              text not null,
  team_id           text,
  domain            text not null check (domain in
                    ('composition','tactique','entrainement','academie','achat','vente','finances','infrastructure','personnel')),
  decided_at        timestamptz not null default now(),
  label             text not null,
  hypothesis        text not null,
  prediction        jsonb not null check (prediction ? 'metric' and prediction ? 'attendu'),
  eval_after        timestamptz not null,
  evidence          jsonb not null default '[]',
  strategy_snapshot jsonb,
  status            text not null default 'proposed'
                    check (status in ('proposed','accepted','rejected','done','expired')),
  user_note         text,
  lesson_id         text,
  check (eval_after > decided_at)
);

create table if not exists learn.outcome (
  decision_id bigint primary key references learn.decision(id),
  measured_at timestamptz not null default now(),
  observed    jsonb not null,
  verdict     text not null check (verdict in ('confirmed','contradicted','inconclusive')),
  note        text
);

create table if not exists learn.lesson (
  id               text primary key,
  game             text not null,
  domain           text not null,
  claim            text not null,
  check_sql        text,
  status           text not null default 'hypothesis'
                   check (status in ('hypothesis','validated','hard_rule','retired')),
  n_for            int not null default 0,
  n_against        int not null default 0,
  created_at       timestamptz not null default now(),
  promoted_at      timestamptz,
  source_decisions bigint[] not null default '{}'
);

create table if not exists learn.error (
  id           bigint generated always as identity primary key,
  game         text,
  description  text not null,
  recurrence   int not null default 1 check (recurrence >= 1),
  enforcement  text not null check (enforcement in ('hook','sql','test','prose')),
  guard_ref    text,
  opened_at    timestamptz not null default now(),
  closed_at    timestamptz,
  -- une récidive ne se ferme que si un garde-fou exécutable existe
  check (closed_at is null or recurrence < 2 or enforcement <> 'prose')
);

alter table learn.decision enable row level security;
alter table learn.outcome  enable row level security;
alter table learn.lesson   enable row level security;
alter table learn.error    enable row level security;

create policy assistant_ro_select on learn.decision for select to assistant_ro using (true);
create policy assistant_ro_insert on learn.decision for insert to assistant_ro with check (true);
create policy assistant_ro_update on learn.decision for update to assistant_ro using (true) with check (true);
create policy assistant_ro_select on learn.outcome  for select to assistant_ro using (true);
create policy assistant_ro_insert on learn.outcome  for insert to assistant_ro with check (true);
create policy assistant_ro_select on learn.lesson   for select to assistant_ro using (true);
create policy assistant_ro_select on learn.error    for select to assistant_ro using (true);

grant select on all tables in schema learn to assistant_ro;
grant insert on learn.decision, learn.outcome to assistant_ro;
grant update (status, user_note, lesson_id) on learn.decision to assistant_ro;
grant usage on sequence learn.decision_id_seq to assistant_ro;

-- Décisions à évaluer (3.3) : acceptées, date d'évaluation passée, pas encore de résultat.
create or replace view gold.decisions_a_evaluer with (security_invoker = true) as
select d.*
from learn.decision d
where d.status in ('accepted', 'done') and d.eval_after <= now()
  and not exists (select 1 from learn.outcome o where o.decision_id = d.id);
grant select on gold.decisions_a_evaluer to assistant_ro;

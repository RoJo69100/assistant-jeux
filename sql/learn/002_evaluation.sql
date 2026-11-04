-- Refonte v2, étapes 3.3 et 3.4 : évaluation des décisions et garde-fou.
-- sujet : joueur, cible ou réglage visé (garde.py y repère les revirements : acheter puis revendre le même sujet).
-- Seuils de leçon communs à tous les jeux (game = '_tous') : 3 confirmations sans contradiction → validated ;
-- 5 → hard_rule proposée ; 2 contradictions → retired + learn.error + conseil à réécrire (plan 3.3, A-7).
-- L'évaluateur (assistant_ro) met à jour les compteurs et le statut des leçons et ouvre les erreurs.
-- Pas de « drop policy » (règle N3).

alter table learn.decision add column if not exists sujet text;
grant update (sujet) on learn.decision to assistant_ro;

create policy assistant_ro_insert on learn.lesson for insert to assistant_ro with check (true);
create policy assistant_ro_update on learn.lesson for update to assistant_ro using (true) with check (true);
create policy assistant_ro_insert on learn.error  for insert to assistant_ro with check (true);
create policy assistant_ro_update on learn.error  for update to assistant_ro using (true) with check (true);
grant insert on learn.lesson, learn.error to assistant_ro;
grant update (n_for, n_against, status, promoted_at, source_decisions) on learn.lesson to assistant_ro;
grant update (recurrence, closed_at, enforcement, guard_ref) on learn.error to assistant_ro;
grant usage on sequence learn.error_id_seq to assistant_ro;

insert into core.game_params (game, key, value, source, verified_on) values
  ('_tous', 'lecon_valider', '3', 'plan refonte 3.3', '2026-11-04'),
  ('_tous', 'lecon_regle',   '5', 'plan refonte 3.3', '2026-11-04'),
  ('_tous', 'lecon_retirer', '2', 'plan refonte 3.3 ; attentes A-7', '2026-11-04')
on conflict (game, key) do update set value = excluded.value, source = excluded.source, verified_on = excluded.verified_on;

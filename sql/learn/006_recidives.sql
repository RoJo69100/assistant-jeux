-- Refonte v2, fin de phase 3 : M7 (récidives de règles par semaine) mesurable en SQL.
-- Une récidive = une ligne datée de learn.error_occurrence (écrite par l'agent retro ou à la main) ;
-- le déclencheur tient learn.error.recurrence à jour et rouvre l'erreur si elle était fermée.
-- gold.kpi_recidives : par semaine ISO, récidives totales et récidives d'erreurs couvertes par du code
-- (enforcement hook/sql/test) — cible M7 : 0 pour ces dernières.

create table if not exists learn.error_occurrence (
  id        bigint generated always as identity primary key,
  error_id  bigint not null references learn.error(id),
  seen_at   timestamptz not null default now(),
  game      text,
  source    text not null,          -- ex. outputs/retro/2026-11-04.md#3
  note      text
);
create index if not exists error_occurrence_error_idx on learn.error_occurrence (error_id, seen_at);

create or replace function learn.compter_recidive() returns trigger
language plpgsql security definer set search_path = learn, public as $$
begin
  update learn.error
     set recurrence = recurrence + 1,
         closed_at = null
   where id = new.error_id;
  return new;
end $$;

create or replace trigger error_occurrence_compte after insert on learn.error_occurrence
for each row execute function learn.compter_recidive();

alter table learn.error_occurrence enable row level security;
create policy assistant_ro_select on learn.error_occurrence for select to assistant_ro using (true);
create policy assistant_ro_insert on learn.error_occurrence for insert to assistant_ro with check (true);
grant select, insert on learn.error_occurrence to assistant_ro;
grant usage on sequence learn.error_occurrence_id_seq to assistant_ro;

create or replace view gold.kpi_recidives with (security_invoker = true) as
select date_trunc('week', o.seen_at)::date as semaine,
       count(*) as recidives,
       count(*) filter (where e.enforcement <> 'prose') as recidives_avec_code,
       count(distinct o.error_id) as erreurs_distinctes,
       string_agg(distinct 'E-' || o.error_id, ', ') filter (where e.enforcement <> 'prose') as a_corriger
from learn.error_occurrence o
join learn.error e on e.id = o.error_id
group by 1
order by 1 desc;

grant select on gold.kpi_recidives to assistant_ro;

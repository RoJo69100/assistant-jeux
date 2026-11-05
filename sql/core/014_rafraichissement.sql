-- Refonte v3, S4b : rafraîchissement automatique des vues matérialisées (core.standing, core.player_daily ; daily_alerts et
-- match_objective s'y ajoutent dans leurs migrations).
-- Décision utilisateur : pg_cron toutes les 10 minutes, avec garde « seulement si une page est arrivée dans bronze.raw_pages
-- depuis le dernier rafraîchissement » ; en plus, un appel explicite avant le que faire du soir.
-- Le job tourne sous le rôle postgres (hors limite de 8 s de l'API). L'appel explicite passe par une fonction en ÉCRITURE
-- (public.rafraichir_avant_soir) : sql_ro est en lecture seule, elle ne peut donc pas être appelée par sql.py (voir le journal).
-- La fonction ne fait que poser une demande ; un second job, chaque minute, lance le rafraîchissement demandé.

create extension if not exists pg_cron with schema pg_catalog;

create table if not exists core.rafraichi_etat (
  id            smallint primary key default 1 check (id = 1),
  last_page_id  bigint,              -- max(bronze.raw_pages.id) vu au dernier rafraîchissement
  debut_a       timestamptz,         -- début du dernier rafraîchissement (les données sont au moins aussi fraîches)
  rafraichi_a   timestamptz,         -- fin du dernier rafraîchissement
  duree_ms      integer,
  demande_a     timestamptz          -- demande explicite en attente
);
insert into core.rafraichi_etat (id) values (1) on conflict do nothing;
grant select on core.rafraichi_etat to assistant_ro;

create or replace function core.rafraichir_vues(p_force boolean default false) returns table(vue text, ms numeric)
language plpgsql security definer set search_path = '' as $$
declare
  cur bigint; e core.rafraichi_etat%rowtype; t0 timestamptz; debut timestamptz := clock_timestamp();
begin
  if not pg_try_advisory_xact_lock(7140001) then
    vue := '(déjà en cours)'; ms := 0; return next; return;
  end if;
  select max(id) into cur from bronze.raw_pages;
  select * into e from core.rafraichi_etat where id = 1;
  if not p_force and e.last_page_id is not distinct from cur then
    vue := '(aucune page nouvelle)'; ms := 0; return next; return;
  end if;

  t0 := clock_timestamp();
  refresh materialized view concurrently core.standing;
  vue := 'core.standing'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently core.player_daily;
  vue := 'core.player_daily'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

  update core.rafraichi_etat
     set last_page_id = cur, debut_a = debut, rafraichi_a = clock_timestamp(),
         duree_ms = round(extract(epoch from clock_timestamp() - debut) * 1000)
   where id = 1;
end $$;
revoke all on function core.rafraichir_vues(boolean) from public;
drop function if exists core.rafraichir_vues();   -- ancienne version sans paramètre (013)

create or replace function core.rafraichir_si_demande() returns void
language plpgsql security definer set search_path = '' as $$
declare e core.rafraichi_etat%rowtype;
begin
  select * into e from core.rafraichi_etat where id = 1;
  if e.demande_a is not null and (e.rafraichi_a is null or e.demande_a > e.debut_a) then
    perform * from core.rafraichir_vues(true);
  end if;
end $$;
revoke all on function core.rafraichir_si_demande() from public;

-- Appel explicite avant le que faire du soir : pose une demande (au plus une par minute) et dit où on en est.
-- Écrit dans core.rafraichi_etat : à appeler en POST (pipelines/rafraichir_avant_soir.py), pas par sql_ro.
create or replace function public.rafraichir_avant_soir() returns text
language plpgsql volatile security definer set search_path = '' as $$
declare e core.rafraichi_etat%rowtype;
begin
  select * into e from core.rafraichi_etat where id = 1 for update;
  if exists (select 1 from pg_locks where locktype = 'advisory' and classid = 0 and objid = 7140001 and granted) then
    return 'en cours : relance dans 30 s';
  end if;
  if e.rafraichi_a is not null and e.rafraichi_a > now() - interval '1 minute' then
    return 'à jour : rafraîchi à ' || to_char(e.rafraichi_a at time zone 'Europe/Paris', 'HH24:MI:SS');
  end if;
  if e.demande_a is not null and e.demande_a > now() - interval '1 minute' then
    return 'déjà demandé à ' || to_char(e.demande_a at time zone 'Europe/Paris', 'HH24:MI:SS') || ' : relance dans 60 s';
  end if;
  update core.rafraichi_etat set demande_a = now() where id = 1;
  return 'demandé : le job démarre dans la minute, relance dans 90 s';
end $$;
revoke all on function public.rafraichir_avant_soir() from public, anon, authenticated;
grant execute on function public.rafraichir_avant_soir() to service_role, assistant_ro;

-- Jobs (idempotents : même nom = remplacement).
select cron.schedule('rafraichir-vues', '*/10 * * * *', $$select * from core.rafraichir_vues(false)$$);
select cron.schedule('rafraichir-demande', '* * * * *', $$select core.rafraichir_si_demande()$$);
select cron.schedule('purge-cron', '17 3 * * *', $$delete from cron.job_run_details where end_time < now() - interval '3 days'$$);

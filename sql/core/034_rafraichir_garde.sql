-- Rafraîchissement des vues matérialisées : garde-fous contre la saturation (24/11/2026).
-- Faits du 24/11 : les rafraîchissements réussis duraient 256 à 297 s (22–23/11, dérive lente). Le serveur a planté à 14:27 Paris
-- (« database system was interrupted », redémarrage à 15:21) pendant un rafraîchissement ; ensuite chaque lancement a atteint
-- les 15 min du statement_timeout et le cron l'a relancé toutes les 10 min (last_page_id jamais mis à jour) : instance saturée,
-- un calcul pur de 3 M lignes prenait 10 à 19 s sans aucune autre requête active.
-- Garde-fous :
--   1. plafond de durée 8 min (statement_timeout des deux jobs ; une réussite normale prend ~5 min) ;
--   2. après un échec (timeout, annulation, redémarrage), aucun nouveau lancement pendant 60 min, demande explicite comprise ;
--   3. aucun lancement de 08:25 à 09:15 ni de 18:15 à 19:05 (Paris) : la base reste libre pour les passages de 08:40 et 18:30 ;
--      avec le plafond de 8 min, un lancement de 08:24 finit au plus tard à 08:32 ;
--   4. pas de chevauchement : verrou consultatif 7140001 (déjà en place).

create or replace function core.rafraichir_bloque(p_maintenant timestamptz default now()) returns text
language plpgsql stable security definer set search_path = '' as $$
declare h time := (p_maintenant at time zone 'Europe/Paris')::time; echec timestamptz; e core.rafraichi_etat%rowtype;
begin
  if h >= time '08:25' and h < time '09:15' then return 'créneau du passage de 08:40'; end if;
  if h >= time '18:15' and h < time '19:05' then return 'créneau du passage de 18:30'; end if;
  select max(d.end_time) into echec
    from cron.job_run_details d join cron.job j using (jobid)
   where j.command like '%rafraichir%' and d.status = 'failed'
     and (d.return_message like '%statement timeout%' or d.return_message like '%canceling statement%'
          or d.return_message like '%server restarted%')
     and d.end_time > p_maintenant - interval '60 minutes';
  select * into e from core.rafraichi_etat where id = 1;
  if echec is not null and (e.rafraichi_a is null or e.rafraichi_a < echec) then
    return 'échec à ' || to_char(echec at time zone 'Europe/Paris', 'HH24:MI') || ' : pas de relance avant '
           || to_char((echec + interval '60 minutes') at time zone 'Europe/Paris', 'HH24:MI');
  end if;
  return null;
end $$;
revoke all on function core.rafraichir_bloque(timestamptz) from public;

create or replace function core.rafraichir_vues(p_force boolean default false)
 returns table(vue text, ms numeric)
 language plpgsql security definer set search_path to ''
as $function$
declare
  cur bigint; e core.rafraichi_etat%rowtype; t0 timestamptz; debut timestamptz := clock_timestamp(); bloque text;
begin
  if not pg_try_advisory_xact_lock(7140001) then
    vue := '(déjà en cours)'; ms := 0; return next; return;
  end if;
  bloque := core.rafraichir_bloque(now());
  if bloque is not null then
    vue := '(bloqué : ' || bloque || ')'; ms := 0; return next; return;
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
  t0 := clock_timestamp();
  refresh materialized view concurrently gold.match_objective;
  vue := 'gold.match_objective'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently gold.daily_alerts;
  vue := 'gold.daily_alerts'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently gold.bv_sell_candidates;
  vue := 'gold.bv_sell_candidates'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently gold.bv_sell_replacement;
  vue := 'gold.bv_sell_replacement'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently gold.bv_matchs_autres;
  vue := 'gold.bv_matchs_autres'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

  update core.rafraichi_etat
     set last_page_id = cur, debut_a = debut, rafraichi_a = clock_timestamp(),
         duree_ms = round(extract(epoch from clock_timestamp() - debut) * 1000)
   where id = 1;
end $function$;
revoke all on function core.rafraichir_vues(boolean) from public;

-- Plafond de durée : 8 min au lieu de 15 ; les jobs restent suspendus (active = false) tant que l'instance n'est pas saine.
select cron.alter_job(jobid, command := $$set statement_timeout = '8min'; select * from core.rafraichir_vues(false)$$)
  from cron.job where jobname = 'rafraichir-vues';
select cron.alter_job(jobid, command := $$set statement_timeout = '8min'; select core.rafraichir_si_demande()$$)
  from cron.job where jobname = 'rafraichir-demande';

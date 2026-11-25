-- Rafraîchissement à mémoire bornée (25/11/2026), après le plantage du 24/11 à 14:27 Paris (pic de mémoire ≈ 2 Go selon la
-- console Supabase, plan Free, swap ≈ 400 Mo en continu). Mesures du 25/11 (EXPLAIN ANALYZE, BUFFERS, instance saine) :
--   core.standing_src 22 s · core.player_daily_src 19 s (124 611 blocs temporaires ≈ 1 Go) · gold.match_objective_src 20,5 s ·
--   gold.daily_alerts_src > 58 s (ts 26,7 s, bv 10,9 s, hw 10,7 s, exports_state 5,5 s, hn 2,8 s, sz 1,6 s) ·
--   gold.bv_sell_candidates_src > 58 s · gold.bv_sell_replacement_src 1,8 s · gold.bv_matchs_autres 4,7 s.
-- 035 rend gold.exports_state léger (0,54 s) ; ici : rattrapage de core.page_meta avant les vues, sans worker parallèle
-- (chaque worker reprend work_mem) et avec hash_mem_multiplier = 1 pendant le rafraîchissement. Le reste du coût vient des
-- vues silver qui relisent le JSON de bronze à chaque lecture.

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
  set local max_parallel_workers_per_gather = 0;
  set local hash_mem_multiplier = 1;
  t0 := clock_timestamp();
  perform core.page_meta_rattraper(5000);
  vue := 'core.page_meta'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

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

-- 18/11 : « vue gold.bv_sell_replacement illisible » dans le plan BasketVibe (délai de sql_ro, 20 s) : aucune vente évaluée.
-- Mesuré : 9,6 à 11 s pour 12 lignes (gold.bv_slot_fit relue trois fois). Même remède que 087 (bv_sell_candidates) : vue
-- d'origine renommée _src, vue matérialisée à sa place, rafraîchie par core.rafraichir_vues avec les autres.
-- Test : pipelines/test_vues_lentes.py (moins de 5 s, jamais « illisible »).

set local search_path = '';

-- 1. colonnes inchangées, aucun dépendant (pg_depend vérifié le 18/11), player_id unique et non nul
alter view gold.bv_sell_replacement rename to bv_sell_replacement_src;
create materialized view gold.bv_sell_replacement as select * from gold.bv_sell_replacement_src with data;
create unique index bv_sell_replacement_cle on gold.bv_sell_replacement (player_id);
grant select on gold.bv_sell_replacement to assistant_ro;

-- 2. rafraîchissement : la vue s'ajoute à la liste de 087
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
end $$;
revoke all on function core.rafraichir_vues(boolean) from public;

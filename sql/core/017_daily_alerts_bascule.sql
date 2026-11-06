-- Refonte v3, S4b : gold.daily_alerts matérialisée, phase 2 (bascule des noms, sans interruption de service).
-- La vue provisoire gold.daily_alerts_m, remplie en 119 s par pg_cron (phase 1), prend le nom gold.daily_alerts.
-- La vue d'origine devient gold.daily_alerts_src (non supprimée). Colonnes d'origine inchangées ; `cle` et `rafraichi_a` à la fin.
-- Contenu vérifié avant la bascule : basketvibe et sixzeroleague identiques (md5) ; derbymanager et hockeynation ne diffèrent que
-- par le compteur d'heures d'âge d'un export (« 66 h » / « 65 h »), qui avance avec l'heure.
-- Limite : les alertes dépendent de now() et current_date (âge des exports, enchères en cours) ; la vue est figée entre deux
-- rafraîchissements (nouvelle page, appel explicite avant le soir, ou demande). Un rafraîchissement complet coûte ~2 min.

set local search_path = '';

alter view gold.daily_alerts rename to daily_alerts_src;
alter materialized view gold.daily_alerts_m rename to daily_alerts;
alter index gold.daily_alerts_m_cle rename to daily_alerts_cle;
alter index gold.daily_alerts_m_jeu rename to daily_alerts_jeu;

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
  refresh materialized view concurrently gold.daily_alerts;   -- en dernier : elle lit core.player_daily, core.fixture, gold.exports_state
  vue := 'gold.daily_alerts'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

  update core.rafraichi_etat
     set last_page_id = cur, debut_a = debut, rafraichi_a = clock_timestamp(),
         duree_ms = round(extract(epoch from clock_timestamp() - debut) * 1000)
   where id = 1;
end $$;
revoke all on function core.rafraichir_vues(boolean) from public;

-- 18/11 : deux lectures du plan BasketVibe dépassaient le délai de sql_ro (20 s) : « vue vendre illisible », « matchs_autres
-- illisible » (aucune vente évaluée ; « 75 en base » au lieu de 122). Cause mesurée (explain analyze) : la vue relit
-- bronze.raw_pages (JSON brut, regex sur l'URL) dans une sous-requête corrélée, 92 fois. Même remède que 016 (match_objective) :
-- vue d'origine renommée _src, vue matérialisée à sa place, rafraîchie par core.rafraichir_vues (pg_cron toutes les 10 minutes si
-- une page est arrivée, et python -I pipelines/rafraichir_avant_aujourdhui.py avant le plan).
-- Test : pipelines/test_vues_lentes.py (moins de 5 s, jamais « illisible »).

set local search_path = '';

-- 1. gold.bv_sell_candidates : colonnes inchangées, aucun dépendant (pg_depend vérifié le 18/11)
alter view gold.bv_sell_candidates rename to bv_sell_candidates_src;
create materialized view gold.bv_sell_candidates as select * from gold.bv_sell_candidates_src with data;
create unique index bv_sell_candidates_cle on gold.bv_sell_candidates (player_id);
grant select on gold.bv_sell_candidates to assistant_ro;

-- 2. matchs d'autres clubs (finis dans silver.bv_matches, sans fixture chez nous) et jour Paris de la première capture de leur page
-- de match (null si jamais captée) : une seule lecture groupée de bronze.raw_pages au lieu d'une sous-requête par match.
create materialized view gold.bv_matchs_autres as
with pages as (
  select right(p.page_url, 36) as fixture_id, (min(p.captured_at) at time zone 'Europe/Paris')::date as premiere_jour
  from bronze.raw_pages p
  where p.game = 'basketvibe' and p.page_url ~ '^https://www[.]basketvibe[.]com/(match|friendly|cup)/[0-9a-f-]{36}$'
  group by 1
)
select distinct on (m.fixture_id) m.fixture_id::text as fixture_id, pg.premiere_jour
from silver.bv_matches m
left join pages pg on pg.fixture_id = m.fixture_id::text
where m.status = 'finished'
  and not exists (select 1 from core.fixture f where f.game = 'basketvibe' and f.fixture_id = m.fixture_id::text)
order by m.fixture_id
with data;
create unique index bv_matchs_autres_cle on gold.bv_matchs_autres (fixture_id);
grant select on gold.bv_matchs_autres to assistant_ro;

-- 3. rafraîchissement : les deux nouvelles vues s'ajoutent à la liste
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
  refresh materialized view concurrently gold.bv_matchs_autres;
  vue := 'gold.bv_matchs_autres'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

  update core.rafraichi_etat
     set last_page_id = cur, debut_a = debut, rafraichi_a = clock_timestamp(),
         duree_ms = round(extract(epoch from clock_timestamp() - debut) * 1000)
   where id = 1;
end $$;
revoke all on function core.rafraichir_vues(boolean) from public;

-- Refonte v3, S4b : gold.match_objective matérialisée. Le filtre par jeu est déjà poussé dans la vue (le plan ne lit que la branche
-- du jeu demandé), mais teamsoccer restait à 3,9 s : l'adaptateur de matchs est lu deux fois (joues + a_venir). Décision utilisateur :
-- matérialiser seulement si le filtre ne suffit pas ; c'est le cas.
-- La vue d'origine est renommée match_objective_src (non supprimée). Colonnes inchangées. Aucun dépendant (pg_depend vérifié).
-- Limite : la fenêtre « 7 jours » suit current_date ; la vue est donc figée entre deux rafraîchissements (nouvelle page ou appel explicite).

set local search_path = '';

alter view gold.match_objective rename to match_objective_src;
create materialized view gold.match_objective as select * from gold.match_objective_src with data;
create unique index match_objective_cle on gold.match_objective (game, team_id, fixture_id);
create index match_objective_jeu on gold.match_objective (game);
grant select on gold.match_objective to assistant_ro;

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
  refresh materialized view concurrently gold.match_objective;   -- après standing (season_context la lit)
  vue := 'gold.match_objective'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;

  update core.rafraichi_etat
     set last_page_id = cur, debut_a = debut, rafraichi_a = clock_timestamp(),
         duree_ms = round(extract(epoch from clock_timestamp() - debut) * 1000)
   where id = 1;
end $$;
revoke all on function core.rafraichir_vues(boolean) from public;

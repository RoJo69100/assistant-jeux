-- Refonte v3, S4 : vues rapides. core.standing et core.player_daily relisaient le JSON de bronze.raw_pages à chaque lecture
-- (standing : 9,4 à 11,1 s, player_daily : 5,4 s et 6,6 s pour teamsoccer et hardwood ; seuil visé 2 s).
-- Les autres vues core.* sont déjà sous 2 s (mesure du 2026-11-05) : non touchées.
-- Les vues d'origine sont renommées *_src (non supprimées). Les vues gold qui les lisaient sont recréées pour viser la nouvelle vue.
-- Une vue matérialisée n'a ni security_invoker ni RLS : select accordé explicitement à assistant_ro.
-- Retour arrière : voir le bloc en bas de fichier.

set local search_path = '';

alter view core.standing rename to standing_src;
create materialized view core.standing as select * from core.standing_src with data;
create unique index standing_cle on core.standing (game, team_id, season_id, day);
create index standing_jeu on core.standing (game);
grant select on core.standing to assistant_ro;

alter view core.player_daily rename to player_daily_src;
create materialized view core.player_daily as select * from core.player_daily_src with data;
create unique index player_daily_cle on core.player_daily (game, team_id, player_id, day);
create index player_daily_jeu on core.player_daily (game);
grant select on core.player_daily to assistant_ro;

-- Les vues dépendantes suivent l'objet renommé (liaison par identifiant) : on les recrée pour qu'elles lisent la vue matérialisée.
do $$
declare r record;
begin
  for r in
    select distinct dep.oid as dep_oid, dn.nspname as dep_schema, dep.relname as dep_name,
           src.relname as src_name
    from pg_depend d
    join pg_rewrite rw on rw.oid = d.objid
    join pg_class dep on dep.oid = rw.ev_class
    join pg_namespace dn on dn.oid = dep.relnamespace
    join pg_class src on src.oid = d.refobjid
    where src.relnamespace = 'core'::regnamespace
      and src.relname in ('standing_src', 'player_daily_src')
      and dep.relkind = 'v'
  loop
    execute format('create or replace view %I.%I with (security_invoker = true) as %s',
                   r.dep_schema, r.dep_name,
                   replace(pg_get_viewdef(r.dep_oid, true), r.src_name, replace(r.src_name, '_src', '')));  -- aussi les références de colonnes (player_daily_src.game)
    raise notice 'recréée : %.% (lisait core.%)', r.dep_schema, r.dep_name, r.src_name;
  end loop;
end $$;

-- Rafraîchissement : sans bloquer les lectures (index uniques ci-dessus). Durée renvoyée en millisecondes.
create or replace function core.rafraichir_vues() returns table(vue text, ms numeric)
language plpgsql security definer set search_path = '' as $$
declare t0 timestamptz;
begin
  t0 := clock_timestamp();
  refresh materialized view concurrently core.standing;
  vue := 'core.standing'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
  t0 := clock_timestamp();
  refresh materialized view concurrently core.player_daily;
  vue := 'core.player_daily'; ms := round(extract(epoch from clock_timestamp() - t0) * 1000); return next;
end $$;
revoke all on function core.rafraichir_vues() from public;

-- Retour arrière (à ne lancer que sur décision) :
--   drop materialized view core.standing; alter view core.standing_src rename to standing;
--   drop materialized view core.player_daily; alter view core.player_daily_src rename to player_daily;
--   puis recréer les vues gold dépendantes depuis leurs fichiers sql/gold/.

-- Refonte v3, S4b : gold.daily_alerts matérialisée (6,9 à 11,6 s, timeout hardwood et teamsoccer avant).
-- Décision utilisateur : colonnes `cle` (unique) et `rafraichi_a` ajoutées À LA FIN ; aucune colonne existante modifiée ni réordonnée.
-- Phase 1 (ce fichier) : la vue matérialisée est créée sous un nom provisoire (gold.daily_alerts_m), SANS données, puis remplie
-- par un job pg_cron à usage unique (le remplissage dépasse les 60 s du connecteur). La vue d'origine reste en service.
-- Phase 2 (016_daily_alerts_bascule.sql) : bascule des noms une fois la vue remplie et vérifiée.

create materialized view gold.daily_alerts_m as
select s.game, s.team_id, s.prio, s.niveau, s.domaine, s.alerte, s.rule_id, s.club,
       row_number() over (order by s.game, s.team_id, s.prio, s.domaine, s.alerte, s.rule_id, s.club)::bigint as cle,
       now() as rafraichi_a
from gold.daily_alerts s
with no data;

create unique index daily_alerts_m_cle on gold.daily_alerts_m (cle);
create index daily_alerts_m_jeu on gold.daily_alerts_m (game);
grant select on gold.daily_alerts_m to assistant_ro;

-- Remplissage initial, une seule fois (le job se retire après le remplissage ; s'il échoue il se relance chaque minute : à surveiller).
select cron.schedule('init-daily-alerts', '* * * * *',
  $$refresh materialized view gold.daily_alerts_m; select cron.unschedule('init-daily-alerts')$$);

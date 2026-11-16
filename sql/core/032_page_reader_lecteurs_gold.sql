-- Lecteurs gold manquants du registre core.page_reader (2026-11-16, brique base, étape 4).
-- Vérifiés dans les définitions en base : gold.dm_ecole_scouts filtre page_type = 'players_id' ; gold.hw_exports_state et gold.hw_today lisent
-- silver.hw_schedule (page_type schedule_id) ; gold.sz_exports_state teste ^/infrastructure/mine$, ^/teams/mine/transfers$ et ^/transfers$ ;
-- gold.ts_match_report lit silver.ts_match_ratings / ts_match_sectors, eux-mêmes lus dans silver.ts_match_pages (/match-viewer/<n>).
-- Réglages de tirs arrêtés DerbyManager (appels /players/<n>/setpiece/...) : gold.dm_setpieces est le lecteur indiqué par l'utilisateur,
-- mais la vue lit l'onglet Squad (silver.dm_squad), pas ces appels : rattachement à confirmer.
-- Hockey Nation /api/club/<id> (agenda) : aucun lecteur gold ne le cite (gold.hn_exports_state lit seulement les sous-routes) : non inséré.
insert into core.page_reader (game, motif, lecteur) values
  ('derbymanager', '^/players/<n>/setpiece/', 'gold.dm_setpieces'),
  ('derbymanager', '^dom:players_id$', 'gold.dm_ecole_scouts'),
  ('hardwood', '^dom:schedule_id$', 'gold.hw_exports_state'),
  ('hardwood', '^dom:schedule_id$', 'gold.hw_today'),
  ('sixzeroleague', '^/api/infrastructure/mine$', 'gold.sz_exports_state'),
  ('sixzeroleague', '^/api/teams/mine/transfers$', 'gold.sz_exports_state'),
  ('sixzeroleague', '^/api/transfers$', 'gold.sz_exports_state'),
  ('teamsoccer', '^dom:dashboard_match-viewer_id$', 'gold.ts_match_report'),
  ('teamsoccer', '^dom:dashboard_match-viewer_id$', 'silver.ts_match_pages')
on conflict do nothing;

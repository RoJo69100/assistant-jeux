-- Refonte v2, étape 1.4 : core.alert_rule pour Team Soccer, Six Zero League, Hardwood et Derby Manager.
-- Même méthode que Hockey Nation : la fraîcheur des exports passe par gold.exports_state (écart voulu : un écran
-- par ligne, par club pour Team Soccer) ; les autres domaines sont repris tels quels de l'ancienne vue du jeu
-- (texte et club identiques), en attendant leur portage sur core.
-- Hardwood : tout reste dans l'ancienne vue (son domaine Export lit aussi feuilles de match et pages joueur).
-- Derby Manager : pas d'ancienne vue d'alertes ; exports seulement (nouveau).

insert into core.alert_rule (game, rule_id, priority, domaine, declencheur, competition_kind, seuil_bas, seuil_haut, modele, source) values
  ('teamsoccer', 'exports', 3, 'export', 'export_perime', null, null, null, 'Export {ecran} : {statut} ({age_h} h)',
   'core.export_rule (écart voulu : remplace les 5 types d''écran de gold.ts_daily_alerts, par club)'),
  ('teamsoccer', 'blessure', 1, 'blessure', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts'),
  ('teamsoccer', 'cartons', 2, 'cartons', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts [skill teamsoccer-joueurs]'),
  ('teamsoccer', 'composition', 1, 'composition', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts (gold.ts_upcoming)'),
  ('teamsoccer', 'finances', 1, 'finances', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts (gold.ts_finance_status ; à porter avec gold.finance_health)'),
  ('teamsoccer', 'HPC', 2, 'HPC', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts (gold.ts_hpc_status)'),
  ('teamsoccer', 'académie', 2, 'académie', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts (gold.ts_academy)'),
  ('teamsoccer', 'match', 2, 'match', 'ancienne_vue', null, null, null, null, 'gold.ts_daily_alerts (match joué sans événements)'),

  ('sixzeroleague', 'exports', 3, 'export', 'export_perime', null, null, null, 'Export {ecran} : {statut} ({age_h} h)',
   'core.export_rule (écart voulu : 14 écrans au lieu de 5, même hors saison)'),
  ('sixzeroleague', 'blessure', 1, 'blessure', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts'),
  ('sixzeroleague', 'effectif', 1, 'effectif', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts (gold.sz_role_report, retraites)'),
  ('sixzeroleague', 'finances', 1, 'finances', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts (gold.sz_finance_projection)'),
  ('sixzeroleague', 'sponsor', 2, 'sponsor', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts'),
  ('sixzeroleague', 'académie', 2, 'académie', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts (silver.sz_u18)'),
  ('sixzeroleague', 'match', 2, 'match', 'ancienne_vue', null, null, null, null, 'gold.sz_daily_alerts'),

  ('hardwood', 'Composition', 1, 'Composition', 'ancienne_vue', null, null, null, null, 'gold.hw_daily_alerts (gold.hw_depth_suggest)'),
  ('hardwood', 'Personnel', 1, 'Personnel', 'ancienne_vue', null, null, null, null, 'gold.hw_daily_alerts (fenêtre des assistants)'),
  ('hardwood', 'Export', 1, 'Export', 'ancienne_vue', null, null, null, null, 'gold.hw_daily_alerts (gold.hw_exports_state)'),
  ('hardwood', 'Académie/Draft', 2, 'Académie/Draft', 'ancienne_vue', null, null, null, null, 'gold.hw_daily_alerts (points de recrutement)'),
  ('hardwood', 'Analyse', 2, 'Analyse', 'ancienne_vue', null, null, null, null, 'gold.hw_daily_alerts (Overwork)'),

  ('derbymanager', 'exports', 2, 'export', 'export_perime', null, null, null, 'Export {ecran} : {statut} ({age_h} h)',
   'core.export_rule (gold.dm_exports_etat ; nouveau : pas d''ancienne vue d''alertes)')
on conflict (game, rule_id) do update set
  priority = excluded.priority, domaine = excluded.domaine, declencheur = excluded.declencheur,
  competition_kind = excluded.competition_kind, seuil_bas = excluded.seuil_bas, seuil_haut = excluded.seuil_haut,
  modele = excluded.modele, source = excluded.source;

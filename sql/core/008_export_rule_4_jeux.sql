-- Refonte v2, étape 1.4 : core.export_rule étendue à Team Soccer, Six Zero League, Hardwood et Derby Manager.
-- champ : ce que path_re lit dans le bronze
--   path      chemin de l'appel API, hôte et paramètres retirés (source api, statut 200) — BV, HN, SZL
--   url       chemin + paramètres de l'appel API (source api, statut 200) — Team Soccer (club dans ?team_id=eq.N)
--   page_type type de page déclaré par le userscript (toute source) — Hardwood, Derby Manager (commun)
--   page_url  adresse de la page ouverte (toute source) — Derby Manager (club dans l'adresse)
-- par_equipe : une ligne par équipe à moi (dernier club_label de core.player_daily) ; {team} dans path_re = team_id.
-- corps_tableau : seulement les réponses dont le corps est un tableau (silver.ts_api).
-- titre_exclu_re : captures écartées par leur titre (pages anti-robot de Hardwood, silver.hw_pages).
-- max_age_h nul : pas d'âge limite (« après chaque match » de Derby Manager) ; à jour dès qu'une capture existe.

alter table core.export_rule add column if not exists champ text not null default 'path'
  check (champ in ('path', 'url', 'page_type', 'page_url'));
alter table core.export_rule add column if not exists source_filtre text check (source_filtre in ('api', 'dom'));
alter table core.export_rule add column if not exists par_equipe boolean not null default false;
alter table core.export_rule add column if not exists corps_tableau boolean not null default false;
alter table core.export_rule add column if not exists titre_exclu_re text;
alter table core.export_rule alter column max_age_h drop not null;

-- Team Soccer : repris de gold.ts_exports_state (sql/gold/037_ts_bv_routine.sql), écrans 1 à 6 par club.
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source, champ, par_equipe, corps_tableau) values
  ('teamsoccer', 1, 'Équipe (joueurs)', '^/rest/v1/players\?(.*&)?team_id=eq\.{team}(&|$)', 24, 'effectif, Forme, blessés', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 2, 'Composition', '^/rest/v1/match_lineups\?(.*&)?team_id=eq\.{team}(&|$)', 24, 'compo enregistrée du prochain match', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 3, 'Finances', '^/rest/v1/team_finances\?(.*&)?team_id=eq\.{team}(&|$)', 72, 'solde, capacité d''investissement', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 4, 'Stade', '^/rest/v1/stadiums\?(.*&)?team_id=eq\.{team}(&|$)', 168, 'places, prix', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 5, 'Académie', '^/rest/v1/youth_academies\?(.*&)?team_id=eq\.{team}(&|$)', 48, 'jeunes révélés', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 6, 'Haute performance', '^/rest/v1/high_performance_scouts\?(.*&)?team_id=eq\.{team}(&|$)', 168, 'scouts HPC', 'gold.ts_exports_state', 'url', true, true),
  ('teamsoccer', 7, 'Matchs (calendrier)', '^/rest/v1/matches$', 24, 'résultats, prochains matchs', 'gold.ts_exports_state', 'path', false, true),
  ('teamsoccer', 8, 'Classement', '^/rest/v1/series$', 48, 'classement des deux ligues', 'gold.ts_exports_state', 'path', false, true),
  ('teamsoccer', 9, 'Marché', '^/rest/v1/transfer_listings$', 24, 'cibles', 'gold.ts_exports_state', 'path', false, true),
  ('teamsoccer', 10, 'Mes enchères', '^/rest/v1/transfer_bids$', 24, 'enchères en cours', 'gold.ts_exports_state', 'path', false, true),
  ('teamsoccer', 11, 'Gymnase (entraînement)', '^/rest/v1/player_training_assignments$', 168, 'compétence et intensité par joueur', 'gold.ts_exports_state', 'path', false, true),
  ('teamsoccer', 12, 'Forum', '^/rest/v1/forum_posts$', 72, 'veille', 'gold.ts_exports_state', 'path', false, true)
on conflict (game, ordre) do update set
  ecran = excluded.ecran, path_re = excluded.path_re, max_age_h = excluded.max_age_h, pour_quoi = excluded.pour_quoi,
  source = excluded.source, champ = excluded.champ, par_equipe = excluded.par_equipe, corps_tableau = excluded.corps_tableau;

-- Six Zero League : repris de gold.sz_exports_state (sql/gold/036_sz_routine.sql) ; silver.sz_api retire « /api ».
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source) values
  ('sixzeroleague', 1, 'Équipe > Players', '^/api/teams/mine/players$', 24, 'effectif, blessés, compétences', 'gold.sz_exports_state'),
  ('sixzeroleague', 2, 'Équipe > Tactique', '^/api/teams/mine/tactics/default$', 24, 'sept et remplaçants enregistrés', 'gold.sz_exports_state'),
  ('sixzeroleague', 3, 'Transferts (marché)', '^/api/transfers$', 12, 'cibles, enchères en cours', 'gold.sz_exports_state'),
  ('sixzeroleague', 4, 'Mes transferts', '^/api/teams/mine/transfers$', 24, 'mes ventes et enchères', 'gold.sz_exports_state'),
  ('sixzeroleague', 5, 'Finances', '^/api/finances/mine$', 24, 'solde, sponsor, prévision', 'gold.sz_exports_state'),
  ('sixzeroleague', 6, 'Entraînement (plan)', '^/api/teams/mine/training$', 48, 'intensité et focus enregistrés', 'gold.sz_exports_state'),
  ('sixzeroleague', 7, 'Entraînement (rapport)', '^/api/teams/mine/training/report$', 48, 'progression du cycle', 'gold.sz_exports_state'),
  ('sixzeroleague', 8, 'Formation de rôle', '^/api/teams/mine/role-training$', 72, '2e rôle en cours', 'gold.sz_exports_state'),
  ('sixzeroleague', 9, 'Académie U18', '^/api/teams/mine/u18$', 72, 'prospects', 'gold.sz_exports_state'),
  ('sixzeroleague', 10, 'Infrastructures', '^/api/infrastructure/mine$', 72, 'niveaux, coûts', 'gold.sz_exports_state'),
  ('sixzeroleague', 11, 'Calendrier (League)', '^/api/seasons/current$', 24, 'étapes de la saison', 'gold.sz_exports_state'),
  ('sixzeroleague', 12, 'Ma compétition', '^/api/seasons/current/my-competition$', 24, 'classement, résultats', 'gold.sz_exports_state'),
  ('sixzeroleague', 13, 'Coupe', '^/api/cups/current$', 48, 'tableau de coupe', 'gold.sz_exports_state'),
  ('sixzeroleague', 14, 'Chat', '^/api/chat/messages$', 72, 'veille (développeur, conseils)', 'gold.sz_exports_state')
on conflict (game, ordre) do update set
  ecran = excluded.ecran, path_re = excluded.path_re, max_age_h = excluded.max_age_h, pour_quoi = excluded.pour_quoi, source = excluded.source;

-- Hardwood : repris de gold.hw_exports_state (sql/gold/043_hw_gold.sql) ; pages DOM par type, âge en jours × 24.
-- Les deux lignes calculées de l'ancienne vue (feuilles de match, pages joueur) ne sont pas des écrans : alertes Hardwood.
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source, champ, source_filtre, titre_exclu_re) values
  ('hardwood', 1, 'Roster', '^roster_id$', 24, 'effectif', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 2, 'Schedule', '^schedule_id$', 24, 'calendrier, résultats', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 3, 'Statistics', '^statistics_id$', 24, 'stats de la saison', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 4, 'Recruiting', '^recruiting_id$', 24, 'recrues suivies, points', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 5, 'Prospect Search (région)', '^prospect_results$', 72, 'nouvelles recrues', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 6, 'Conference', '^conference_id$', 24, 'classement de conférence', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 7, 'Rankings', '^rankings$', 72, 'classements nationaux', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 8, 'Development (après jeudi/dimanche)', '^development_id$', 96, 'progression', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 9, 'Depth Chart', '^depth_chart_id$', 168, 'depth chart', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 10, 'Game Tactics', '^game_tactics_id$', 168, 'tactique de match', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 11, 'Game Management', '^management$', 168, 'consignes par joueur', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 12, 'Coaches', '^coaches_id$', 168, 'coachs en poste', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)'),
  ('hardwood', 13, 'Coach Search', '^coach_results$', 168, 'coachs à recruter', 'gold.hw_exports_state', 'page_type', 'dom', '^(Just a moment|Un instant)')
on conflict (game, ordre) do update set
  ecran = excluded.ecran, path_re = excluded.path_re, max_age_h = excluded.max_age_h, pour_quoi = excluded.pour_quoi,
  source = excluded.source, champ = excluded.champ, source_filtre = excluded.source_filtre, titre_exclu_re = excluded.titre_exclu_re;

-- Derby Manager : repris de gold.dm_exports_etat (sql/gold/049_dm_gold.sql) ; « chaque jour » = 20 h, « chaque semaine » = 168 h.
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source, champ, par_equipe) values
  ('derbymanager', 1, 'Équipe (effectif + entraînement + calendrier)', '/teams/{team}(\?|$)', 20, 'chaque jour', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 2, 'Rapport des matchs (JSON)', '/teams/{team}/matches', null, 'après chaque match', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 3, 'Finances', '/teams/{team}/finances', 20, 'chaque jour', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 4, 'Installations', '/teams/{team}/facilities', 168, 'chaque semaine', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 5, 'School', '/teams/{team}/school', 20, 'chaque jour', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 6, 'Graduates', '/teams/{team}/development', 168, 'chaque semaine', 'gold.dm_exports_etat', 'page_url', true),
  ('derbymanager', 11, 'Marché', '^market', 24, 'chaque jour', 'gold.dm_exports_etat', 'page_type', false),
  ('derbymanager', 12, 'Transferts conclus', '^transfers$', 24, 'chaque jour', 'gold.dm_exports_etat', 'page_type', false),
  ('derbymanager', 13, 'Classement de la ligue', '^competitions_id$', 24, 'chaque jour', 'gold.dm_exports_etat', 'page_type', false)
on conflict (game, ordre) do update set
  ecran = excluded.ecran, path_re = excluded.path_re, max_age_h = excluded.max_age_h, pour_quoi = excluded.pour_quoi,
  source = excluded.source, champ = excluded.champ, par_equipe = excluded.par_equipe;

-- Refonte v2, étape 1.4 : écrans à exporter par jeu (données, pas du SQL par jeu), lus par gold.exports_state.
-- path_re s'applique au chemin de l'appel API capturé, hôte et paramètres retirés (ex. /api/v1/teams/<id>/overview).
-- max_age_h : âge au-delà duquel l'export est à refaire.

create table if not exists core.export_rule (
  game       text not null,
  ordre      int  not null,
  ecran      text not null,
  path_re    text not null,
  max_age_h  int  not null check (max_age_h > 0),
  pour_quoi  text not null,
  source     text not null,
  actif      boolean not null default true,
  primary key (game, ordre)
);
alter table core.export_rule enable row level security;
drop policy if exists assistant_ro_select on core.export_rule;
create policy assistant_ro_select on core.export_rule for select to assistant_ro using (true);
grant select on core.export_rule to assistant_ro;

-- BasketVibe : repris de gold.bv_exports_state (sql/gold/037_ts_bv_routine.sql).
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source) values
  ('basketvibe', 1, 'Équipe (aperçu, joueurs)', '^/api/v1/teams/[^/]+/overview$', 24, 'effectif, forme, fatigue', 'gold.bv_exports_state'),
  ('basketvibe', 2, 'Tactique', '^/api/v1/teams/[^/]+/tactics$', 24, 'cinq par quart-temps, consignes', 'gold.bv_exports_state'),
  ('basketvibe', 3, 'Amicaux (liste)', '^/api/v1/teams/[^/]+/friendlies$', 24, 'amical du jour', 'gold.bv_exports_state'),
  ('basketvibe', 4, 'Amical : tactique du match', '^/api/v1/friendlies/[^/]+/match-tactics$', 24, 'saisie de l''amical', 'gold.bv_exports_state'),
  ('basketvibe', 5, 'Match de ligue : aperçu', '^/api/v1/fixtures/[^/]+/preview$', 72, 'adversaire du prochain match', 'gold.bv_exports_state'),
  ('basketvibe', 6, 'Match de ligue : box', '^/api/v1/fixtures/[^/]+/period-box$', 72, 'stats du dernier match', 'gold.bv_exports_state'),
  ('basketvibe', 7, 'Classement', '^/api/v1/leagues/[^/]+/seasons/[^/]+/standings$', 72, 'classement', 'gold.bv_exports_state'),
  ('basketvibe', 8, 'Marché (enchères)', '^/api/v1/transfer-auctions$', 24, 'cibles', 'gold.bv_exports_state'),
  ('basketvibe', 9, 'Mes enchères', '^/api/v1/teams/[^/]+/my-transfer-auctions$', 24, 'ventes et enchères en cours', 'gold.bv_exports_state'),
  ('basketvibe', 10, 'Finances', '^/api/v1/teams/[^/]+/finance$', 168, 'semaine financière', 'gold.bv_exports_state'),
  ('basketvibe', 11, 'Entraînement', '^/api/v1/teams/[^/]+/training$', 168, 'choix de la semaine', 'gold.bv_exports_state'),
  ('basketvibe', 12, 'Académie', '^/api/v1/teams/[^/]+/academy$', 168, 'jauge, prospects', 'gold.bv_exports_state'),
  ('basketvibe', 13, 'Personnel', '^/api/v1/teams/[^/]+/personnel$', 168, 'staff', 'gold.bv_exports_state'),
  ('basketvibe', 14, 'News (devlog)', '^/api/v1/news$', 168, 'veille', 'gold.bv_exports_state')
on conflict (game, ordre) do nothing;

-- Hockey Nation : repris de gold.hn_exports_state (sql/gold/026_hn_routine.sql) ; :id = identifiant uuid.
insert into core.export_rule (game, ordre, ecran, path_re, max_age_h, pour_quoi, source) values
  ('hockeynation', 1, 'Roster PRO, FRM, U21, U17', '^/api/team/[0-9a-f-]{36}/roster$', 24, 'effectif, talents, contrats', 'gold.hn_exports_state'),
  ('hockeynation', 2, 'Office > Salary cap', '^/api/office/salary-cap-overview$', 24, 'cap space avant échange ou signature', 'gold.hn_exports_state'),
  ('hockeynation', 3, 'Trade Center > offres', '^/api/trade-center/trade-offers$', 24, 'offres reçues et envoyées', 'gold.hn_exports_state'),
  ('hockeynation', 4, 'Trade Center > recherche', '^/api/trade-center/search$', 24, 'cibles d''échange', 'gold.hn_exports_state'),
  ('hockeynation', 5, 'Lineups PRO', '^/api/team/[0-9a-f-]{36}/lineups$', 24, 'lignes enregistrées', 'gold.hn_exports_state'),
  ('hockeynation', 6, 'Training (journal)', '^/api/club/[0-9a-f-]{36}/training-log$', 24, 'entraînement PRO / FRM', 'gold.hn_exports_state'),
  ('hockeynation', 7, 'Coaching staff', '^/api/club/[0-9a-f-]{36}/coaching-staff$', 48, 'coachs en poste et réponses', 'gold.hn_exports_state'),
  ('hockeynation', 8, 'Scouting staff', '^/api/club/[0-9a-f-]{36}/scouting-staff$', 48, 'scouts embauchés', 'gold.hn_exports_state'),
  ('hockeynation', 9, 'Scouting budget', '^/api/club/[0-9a-f-]{36}/scouting-budget-overview$', 48, 'budget de scouting', 'gold.hn_exports_state'),
  ('hockeynation', 10, 'Contract talks', '^/api/club/[0-9a-f-]{36}/expiring-players$', 72, 'prolongations', 'gold.hn_exports_state'),
  ('hockeynation', 11, 'Club finances', '^/api/club/[0-9a-f-]{36}/finances$', 72, 'rachats, salaires par saison', 'gold.hn_exports_state'),
  ('hockeynation', 12, 'Draft class', '^/api/league/[0-9a-f-]{36}/draft-class$', 168, 'rapports des scouts', 'gold.hn_exports_state'),
  ('hockeynation', 13, 'Matchs (programme)', '^/api/club/[0-9a-f-]{36}/game-overview$', 24, 'résultats et prochains matchs', 'gold.hn_exports_state'),
  ('hockeynation', 14, 'Classement', '^/api/league/[0-9a-f-]{36}/standings$', 48, 'classement', 'gold.hn_exports_state')
on conflict (game, ordre) do nothing;

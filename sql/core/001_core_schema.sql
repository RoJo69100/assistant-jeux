-- Refonte v2, étape 1.1 : schémas core (contrat commun) et adapt (un adaptateur mince par jeu).
-- Les vues core.* sont des union all générées par pipelines/build_core.py depuis docs/attentes/jeux/*.yaml.
create schema if not exists core;
create schema if not exists adapt;
revoke all on schema core, adapt from public, anon, authenticated;
grant usage on schema core, adapt to assistant_ro;
alter default privileges in schema core grant select on tables to assistant_ro;
alter default privileges in schema adapt grant select on tables to assistant_ro;

-- Paramètres de règle par jeu : chaque valeur a sa source (skill, manuel, News) et sa date de vérification.
create table core.game_params (
  game        text not null,
  key         text not null,
  value       jsonb not null,
  source      text not null,
  verified_on date not null,
  primary key (game, key)
);
alter table core.game_params enable row level security;
create policy assistant_ro_select on core.game_params for select to assistant_ro using (true);
revoke all on core.game_params from public, anon, authenticated;
grant select on core.game_params to assistant_ro;

insert into core.game_params (game, key, value, source, verified_on) values
  ('basketvibe', 'equipes_par_ligue',    '12',  'basketvibe-saison/02-ligue-et-saison [M§2]', '2026-11-03'),
  ('basketvibe', 'rounds_total',         '22',  'basketvibe-saison/02-ligue-et-saison [M§2]', '2026-11-03'),
  ('basketvibe', 'points_par_victoire',  '2',   'basketvibe-saison/02-ligue-et-saison [M§2, §9.1]', '2026-11-03'),
  ('basketvibe', 'points_par_defaite',   '1',   'basketvibe-saison/02-ligue-et-saison [M§2, §9.1]', '2026-11-03'),
  ('basketvibe', 'match_nul_possible',   'false', 'basketvibe-saison/02-ligue-et-saison [M§2, §9.1]', '2026-11-03'),
  ('basketvibe', 'promo_slots',          '1',   'basketvibe-saison/02-ligue-et-saison [M§2.1] (vainqueur de la ligue fille)', '2026-11-03'),
  ('basketvibe', 'releg_slots',          '4',   'basketvibe-saison/02-ligue-et-saison [M§2.1] (places 9 à 12)', '2026-11-03'),
  ('basketvibe', 'effectif_min',         '8',   'docs/attentes/jeux/basketvibe.yaml domaines.transferts.minimum_effectif', '2026-11-03'),
  ('basketvibe', 'echelle_form',         '{"min": 1, "max": 10}',  'basketvibe-joueurs/05-forme-110 [M§5.5]', '2026-11-03'),
  ('basketvibe', 'echelle_fatigue',      '{"min": 0, "max": 100}', 'basketvibe-joueurs/06-fatigue-0100 [M§5.6]', '2026-11-03');

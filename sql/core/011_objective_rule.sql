-- Refonte v2, étape 2.2 : règles d'objectif de match, en données (lues par gold.match_objective, sql/gold/070).
-- Une règle s'applique si son jeu (nul = tous), son type de compétition (nul = tous) et sa condition collent ;
-- la plus petite priorité gagne. Conditions :
--   serie_defaites  au moins 2 défaites d'affilée (hors amicaux) [A-1]
--   titre_acquis    gold.season_context.titre_acquis
--   rien_a_jouer    gold.season_context.rien_a_jouer
--   normal          toujours vraie (règle par défaut)
-- Trous : {n_def} {rank} {n_teams} {gap_first} {left} {manquants}.
-- « former » (charte du club, étape 2.3) n'est pas encore utilisé : il viendra de core.club_strategy.

create table if not exists core.objective_rule (
  game              text,
  rule_id           text not null,
  competition_kind  text check (competition_kind in ('ligue','coupe','amical','playoff','autre')),
  condition         text not null check (condition in ('serie_defaites','titre_acquis','rien_a_jouer','normal')),
  objectif          text not null check (objectif in ('gagner','tester','former','corriger')),
  priorite          int  not null,
  raison            text not null,
  preuve_erreur     text not null,
  source            text not null,
  actif             boolean not null default true,
  primary key (rule_id)
);
alter table core.objective_rule enable row level security;
-- Pas de « drop policy » : via le connecteur Supabase, il déclenche une confirmation qui n'arrive pas à l'utilisateur
-- (2026-11-04, 3 essais perdus). Table neuve : la politique n'existe pas encore.
create policy assistant_ro_select on core.objective_rule for select to assistant_ro using (true);
grant select on core.objective_rule to assistant_ro;

insert into core.objective_rule (game, rule_id, competition_kind, condition, objectif, priorite, raison, preuve_erreur, source) values
  (null, 'serie',        null,     'serie_defaites', 'corriger', 1,
   '{n_def} défaites d''affilée : changement fort tout de suite (composition, tactique ou joueur)',
   'nouvelle défaite avec le changement appliqué : la cause corrigée n''était pas la bonne',
   'attentes A-1 ; plan refonte 2.2'),
  (null, 'titre',        'ligue',  'titre_acquis',   'tester',   2,
   'titre acquis ({gap_first} points d''avance au plus, {left} matchs restants) : tester joueurs et réglages',
   'le titre n''est pas validé en fin de saison (calcul faux ou règle de points différente)',
   'plan refonte 2.2'),
  (null, 'rien',         'ligue',  'rien_a_jouer',   'tester',   3,
   'rien à jouer (rang {rank}/{n_teams}, maintien acquis, montée hors de portée ou acquise) : tester',
   'le rang final change de palier (montée ou descente) : le calcul était faux',
   'plan refonte 2.2'),
  (null, 'amical',       'amical', 'normal',         'tester',   8,
   'amical : tester (postes, jeunes, réglages)',
   'aucune mesure tirée du test : l''amical n''a rien appris',
   'plan refonte 2.2'),
  (null, 'defaut',       null,     'normal',         'gagner',   9,
   'match à enjeu (rang {rank}/{n_teams}, {gap_first} du 1er, {left} matchs restants{manquants})',
   'défaite avec la meilleure composition disponible : le niveau ou la tactique est en cause',
   'plan refonte 2.2')
on conflict (rule_id) do update set
  game = excluded.game, competition_kind = excluded.competition_kind, condition = excluded.condition,
  objectif = excluded.objectif, priorite = excluded.priorite, raison = excluded.raison,
  preuve_erreur = excluded.preuve_erreur, source = excluded.source;

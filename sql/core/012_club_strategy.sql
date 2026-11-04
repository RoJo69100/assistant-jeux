-- Refonte v2, étape 2.3 : charte de chaque club (choix de l'utilisateur, jamais déduits).
-- Une ligne par équipe ; vide tant que l'utilisateur ne l'a pas fixée (valide_le nul = non validée, ignorée).
-- Lue par gold.match_objective (objectif « former ») ; chaque décision de learn.decision en garde un instantané.
-- Colonnes du plan 2.3 : horizon, poids_jeunes, poids_veterans, appetit_risque,
-- plafond_masse_salariale_pct_revenus, reserve_tresorerie (en périodes de salaires), vendre_pour_profit.

create table if not exists core.club_strategy (
  game                                text not null,
  team_id                             text not null,
  horizon                             text check (horizon in ('maintenant','3_saisons','long_terme')),
  poids_jeunes                        numeric(3,2) check (poids_jeunes between 0 and 1),
  poids_veterans                      numeric(3,2) check (poids_veterans between 0 and 1),
  appetit_risque                      numeric(3,2) check (appetit_risque between 0 and 1),
  plafond_masse_salariale_pct_revenus numeric(5,2) check (plafond_masse_salariale_pct_revenus > 0),
  reserve_tresorerie                  numeric(5,2) check (reserve_tresorerie >= 0),
  vendre_pour_profit                  boolean,
  valide_le                           date,
  note                                text,
  primary key (game, team_id)
);
alter table core.club_strategy enable row level security;
create policy assistant_ro_select on core.club_strategy for select to assistant_ro using (true);
grant select on core.club_strategy to assistant_ro;

-- Règles « former » : même condition que « tester », mais seulement si la charte validée a l'horizon voulu.
alter table core.objective_rule add column if not exists charte_horizons text[];
update core.objective_rule set priorite = 3 where rule_id = 'titre';
update core.objective_rule set priorite = 5 where rule_id = 'rien';
insert into core.objective_rule (game, rule_id, competition_kind, condition, charte_horizons, objectif, priorite,
                                 raison, preuve_erreur, source) values
  (null, 'titre_former', 'ligue', 'titre_acquis', '{3_saisons,long_terme}', 'former', 2,
   'titre acquis ({gap_first} points d''avance au plus, {left} matchs restants) et charte à long terme : minutes aux jeunes',
   'les jeunes alignés ne progressent pas plus que sur le banc (gains d''entraînement et de match)',
   'plan refonte 2.2 et 2.3 ; core.club_strategy'),
  (null, 'rien_former',  'ligue', 'rien_a_jouer', '{3_saisons,long_terme}', 'former', 4,
   'rien à jouer (rang {rank}/{n_teams}) et charte à long terme : minutes aux jeunes',
   'les jeunes alignés ne progressent pas plus que sur le banc (gains d''entraînement et de match)',
   'plan refonte 2.2 et 2.3 ; core.club_strategy')
on conflict (rule_id) do update set
  competition_kind = excluded.competition_kind, condition = excluded.condition, charte_horizons = excluded.charte_horizons,
  objectif = excluded.objectif, priorite = excluded.priorite, raison = excluded.raison,
  preuve_erreur = excluded.preuve_erreur, source = excluded.source;

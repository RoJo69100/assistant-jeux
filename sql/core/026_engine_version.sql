-- Étape 6c, critères V1 et V2 (docs/refonte-v3/journal-aujourdhui.md, « Versions du moteur, étape 6c »).
-- Migration additive : une table, ses lignes, une vue. Aucun drop.

-- V1 : versions du moteur de match par jeu et par compétition. end_date nulle = version en cours.
-- statut : 'annoncé' (date donnée par le développeur ou les News) ou 'déduit' (date tirée du calendrier ou d'une étude).
create table core.engine_version (
  game             text not null,
  version          text not null,
  competition_kind text not null,            -- vocabulaire de core.fixture : ligue, coupe, amical
  start_date       date not null,
  end_date         date,
  source           text not null,
  statut           text not null check (statut in ('annoncé', 'déduit')),
  primary key (game, competition_kind, start_date),
  check (end_date is null or end_date >= start_date)
);
alter table core.engine_version enable row level security;
create policy assistant_ro_select on core.engine_version for select to assistant_ro using (true);
revoke all on core.engine_version from public, anon, authenticated;
grant select on core.engine_version to assistant_ro;

insert into core.engine_version (game, version, competition_kind, start_date, end_date, source, statut) values
  ('basketvibe', 'v3', 'ligue', '2026-09-07', '2026-10-26',
   'fin : skill basketvibe-communaute 02-1 (« ligue en v3 jusqu''à la dernière journée de la saison 1, lundi 26/10 », News 2026-10-19) ; '
   'début : premier match de ligue de la saison 1 (core.fixture), règle de preanalyse-matchs-basketvibe.md § 1.1 et de '
   'etude_evenements_basketvibe.py ; conflit : le même skill dit « v3 en ligue depuis la journée 12 » (03/10, Dev 2026-09-30 / 2026-10-04)',
   'déduit'),
  ('basketvibe', 'v4', 'ligue', '2026-11-02', null,
   'skill basketvibe-communaute 02-1 (« v4 activé dans tous les types de matchs juste après la saison 1 », News 2026-10-19 ; '
   'V-20261027-2 « v4 actif en ligue, coupe et amical depuis le 27/10 ») ; 02/11 = première journée de la saison 2 (skill basketvibe-saison 03) ; '
   'fin : v5 « vers le milieu de la saison », sans date (V-20261108-5)',
   'annoncé'),
  ('basketvibe', 'v4', 'coupe', '2026-10-28', '2026-10-31',
   'skill basketvibe-communaute 02-1 (V-20261027-2 : v4 actif en coupe depuis le 27/10) ; bornes 28/10 et 31/10 = matchs de coupe détaillés '
   'de preanalyse-matchs-basketvibe.md § 1.1 et de l''étude des événements',
   'déduit'),
  ('basketvibe', 'v4', 'amical', '2026-10-11', '2026-10-27',
   'skill basketvibe-communaute 02-1 (« les amicaux depuis le 11/10 tournent déjà avec ces réglages ») ; preanalyse-matchs-basketvibe.md § 1.1 '
   '(10/10 = veille de l''annonce, en v3) ; fin = veille du v5 en amical',
   'déduit'),
  ('basketvibe', 'v5', 'amical', '2026-10-28', null,
   'skill basketvibe-communaute 02-1 (« Moteur v5 : amicaux seulement depuis le 28/10 », V-20261108-5) ; '
   'fin : aucune, déploiement dans tous les matchs sans date',
   'annoncé');

-- V2 : version du moteur de chaque match joué. Aucune ligne de version → 'non attribuée'.
create view gold.bv_match_engine_version as
select f.game, f.team_id, f.fixture_id, f.competition_kind, f.day, f.opponent, f.my_result,
       coalesce(e.version, 'non attribuée') as version, e.statut, e.start_date as version_depuis
from core.fixture f
left join core.engine_version e
  on e.game = f.game and e.competition_kind = f.competition_kind
 and f.day >= e.start_date and (e.end_date is null or f.day <= e.end_date)
where f.game = 'basketvibe' and f.played;

grant select on gold.bv_match_engine_version to assistant_ro;

-- Test : select competition_kind, version, count(*) from gold.bv_match_engine_version group by 1, 2 order by 1, 2;

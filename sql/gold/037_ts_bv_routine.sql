-- Team Soccer et BasketVibe : routine quotidienne en SQL, sans agent (2026-10-30, modèle Hockey Nation 026_hn_routine.sql).
-- Team Soccer : ts_today (prochain match de chaque club, compo enregistrée ou non) et ts_exports_state (par club).
-- BasketVibe : bv_exports_state (bv_agenda tient déjà lieu de « today », bv_saisie_* existent).

-- Prochain match de chaque club (les deux clubs, toujours), échéance de la compo (match pré-calculé 2 h avant [teamsoccer-match]).
create or replace view gold.ts_today with (security_invoker = true) as
select mt.name as club,
       (now() at time zone 'Europe/Paris')::date as today,
       u.competition, u.opponent, u.venue, u.opponent_position, u.opponent_is_bot,
       u.match_date_paris, u.lineup_deadline_paris,
       case when u.match_id is null then 'aucun match programmé'
            when u.lineup_saved then '🟩 compo enregistrée (' || coalesce(u.saved_formation, '?') || ')'
            else '🟥 compo à enregistrer avant ' || to_char(u.lineup_deadline_paris, 'DD/MM HH24:MI') end as compo
from silver.ts_my_teams mt
left join lateral (select * from gold.ts_upcoming x where x.team_id = mt.team_id order by x.match_date_paris limit 1) u on true
order by mt.name;

-- Fraîcheur des exports, par club pour les écrans d'un club, « les deux » pour les écrans communs.
create or replace view gold.ts_exports_state with (security_invoker = true) as
with need(ordre, ecran, endpoint, par_club, max_age_h, pour_quoi) as (values
  (1, 'Équipe (joueurs)', 'players', true, 24, 'effectif, Forme, blessés'),
  (2, 'Composition', 'match_lineups', true, 24, 'compo enregistrée du prochain match'),
  (3, 'Finances', 'team_finances', true, 72, 'solde, capacité d''investissement'),
  (4, 'Stade', 'stadiums', true, 168, 'places, prix'),
  (5, 'Académie', 'youth_academies', true, 48, 'jeunes révélés'),
  (6, 'Haute performance', 'high_performance_scouts', true, 168, 'scouts HPC'),
  (7, 'Matchs (calendrier)', 'matches', false, 24, 'résultats, prochains matchs'),
  (8, 'Classement', 'series', false, 48, 'classement des deux ligues'),
  (9, 'Marché', 'transfer_listings', false, 24, 'cibles'),
  (10, 'Mes enchères', 'transfer_bids', false, 24, 'enchères en cours'),
  (11, 'Gymnase (entraînement)', 'player_training_assignments', false, 168, 'compétence et intensité par joueur'),
  (12, 'Forum', 'forum_posts', false, 72, 'veille')
),
clubs as (select team_id, name from silver.ts_my_teams),
rows as (
  select n.*, c.team_id, c.name as club from need n join clubs c on n.par_club
  union all
  select n.*, null::int, 'les deux' from need n where not n.par_club
)
select r.ordre, r.club, r.ecran, r.pour_quoi,
       max(a.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(a.captured_at)) / 3600) as age_h,
       case when max(a.captured_at) is null then '🟥 jamais'
            when now() - max(a.captured_at) > make_interval(hours => r.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from rows r
left join silver.ts_api a on a.endpoint = r.endpoint and (r.team_id is null or a.q_team_id = r.team_id)
group by r.ordre, r.club, r.ecran, r.pour_quoi, r.max_age_h
order by r.ordre, r.club;

-- BasketVibe : fraîcheur des exports (amical chaque jour : tactique et amicaux à 24 h).
create or replace view gold.bv_exports_state with (security_invoker = true) as
with need(ordre, ecran, endpoint_re, max_age_h, pour_quoi) as (values
  (1, 'Équipe (aperçu, joueurs)', '^/teams/[^/]+/overview$', 24, 'effectif, forme, fatigue'),
  (2, 'Tactique', '^/teams/[^/]+/tactics$', 24, 'cinq par quart-temps, consignes'),
  (3, 'Amicaux (liste)', '^/teams/[^/]+/friendlies$', 24, 'amical du jour'),
  (4, 'Amical : tactique du match', '^/friendlies/[^/]+/match-tactics$', 24, 'saisie de l''amical'),
  (5, 'Match de ligue : aperçu', '^/fixtures/[^/]+/preview$', 72, 'adversaire du prochain match'),
  (6, 'Match de ligue : box', '^/fixtures/[^/]+/period-box$', 72, 'stats du dernier match'),
  (7, 'Classement', '^/leagues/[^/]+/seasons/[^/]+/standings$', 72, 'classement'),
  (8, 'Marché (enchères)', '^/transfer-auctions$', 24, 'cibles'),
  (9, 'Mes enchères', '^/teams/[^/]+/my-transfer-auctions$', 24, 'ventes et enchères en cours'),
  (10, 'Finances', '^/teams/[^/]+/finance$', 168, 'semaine financière'),
  (11, 'Entraînement', '^/teams/[^/]+/training$', 168, 'choix de la semaine'),
  (12, 'Académie', '^/teams/[^/]+/academy$', 168, 'jauge, prospects'),
  (13, 'Personnel', '^/teams/[^/]+/personnel$', 168, 'staff'),
  (14, 'News (devlog)', '^/news$', 168, 'veille')
)
select n.ordre, n.ecran, n.pour_quoi,
       max(a.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(a.captured_at)) / 3600) as age_h,
       case when max(a.captured_at) is null then '🟥 jamais'
            when now() - max(a.captured_at) > make_interval(hours => n.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from need n left join silver.bv_api a on a.endpoint ~ n.endpoint_re
group by n.ordre, n.ecran, n.pour_quoi, n.max_age_h
order by n.ordre;

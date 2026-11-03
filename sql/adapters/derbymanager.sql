-- Refonte v2, étape 1.2 : adaptateur Derby Manager (football, DM2) vers le contrat core (plan §1.1).
-- Deux clubs (silver.dm_clubs : 547 Queen of the South, 307 Marmandes) = deux team_id, comme dans l'adresse des pages
-- (/teams/<id>) : core.export_rule par club s'appuie dessus.
-- Argent et salaires : par jour (silver.dm_squad, page Finances « Daily flow »).
-- Compétences 1–20 (silver.dm_squad) ; forme, condition et sharpness : échelles non sourcées, brutes dans extras.
-- Matchs : réponse JSON /teams/<id>/matches (silver.dm_matches) = matchs joués seulement ; les matchs à venir
-- (silver.dm_fixtures, date en texte du jeu) ne sont pas branchés : date réelle à confirmer.

insert into core.game_params (game, key, value, source, verified_on) values
  ('derbymanager', 'echelle_competence', '{"min": 1, "max": 20}', 'silver.dm_squad (compétences 1-20)', '2026-11-04'),
  ('derbymanager', 'rounds_total',       '30', 'derbymanager-regles (saison de 30 matchs)', '2026-11-04'),
  ('derbymanager', 'match_nul_possible', 'true', 'silver.dm_standings (colonne D)', '2026-11-04')
on conflict (game, key) do nothing;

create or replace view adapt.derbymanager_player_daily with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  s.team_id::text                                   as team_id,
  c.club                                            as club_label,
  s.name                                            as player_id,      -- pas d'identifiant dans le tableau Squad
  (s.captured_at at time zone 'Europe/Paris')::date as day,
  s.name                                            as name,
  s.pos                                             as position,
  s.age                                             as age,
  s.rating::numeric                                 as rating,         -- note moyenne de la saison (colonne RATING)
  null::numeric                                     as form,           -- FRM : échelle non sourcée (extras.form)
  null::numeric                                     as fatigue,        -- condition % dans extras
  round(s.satisfaction_pct / 100, 3)                as morale,         -- satisfaction 0–100 % -> 0–1
  null::boolean                                     as injured,        -- blessure non lue dans le tableau Squad
  null::boolean                                     as suspended,
  s.salary                                          as salary,         -- par jour (extras.salary_period)
  null::date                                        as contract_end,   -- jours restants dans extras
  s.price                                           as market_value,
  false                                             as is_academy,     -- la school est dans academy_prospect
  jsonb_build_object('han', s.han, 'mar', s.mar, 'tac', s.tac, 'posi', s.posi, 'aer', s.aer, 'agi', s.agi,
                     'ant', s.ant, 'cre', s.cre, 'pas', s.pas, 'bal', s.bal, 'fir', s.fir, 'tec', s.tec,
                     'acc', s.acc, 'sho', s.sho, 'hea', s.hea, 'rea', s.rea) as skills,
  jsonb_build_object('salary_period', 'jour', 'contract_days', s.contract_days, 'form', s.form,
                     'condition_pct', s.condition_pct, 'sharpness', s.sharpness, 'fit', s.fit, 'exp', s.exp,
                     'pot', s.pot, 'tier', s.tier, 'role', s.role, 'intensity', s.intensity, 'tr', s.tr,
                     'slot', s.slot, 'shirt', s.shirt, 'apps', s.apps, 'goals', s.goals, 'assists', s.assists,
                     'captured_at', s.captured_at) as extras
from silver.dm_squad s
join silver.dm_clubs c on c.team_id = s.team_id;

create or replace view adapt.derbymanager_fixture with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  m.team_id::text                                   as team_id,
  m.match_id::text                                  as fixture_id,
  case when m.comp ilike '%league%' or m.comp in ('L', 'league') then 'ligue'
       when m.comp ilike '%friend%' then 'amical'
       when m.comp is not null then 'coupe' else 'autre' end as competition_kind,
  null::int                                         as round_no,
  30                                                as rounds_total,
  (m.played_at at time zone 'Europe/Paris')::date   as day,
  m.played_at                                       as scheduled_at,
  true                                              as played,
  m.gf                                              as my_score,
  m.ga                                              as opp_score,
  case m.my_result when 'W' then 'V' when 'D' then 'N' when 'L' then 'D' end as my_result,
  m.opponent                                        as opponent,
  m.is_home                                         as home,
  jsonb_build_object('comp', m.comp, 'comp_name', m.comp_name, 'season', m.season, 'xgf', m.xgf, 'xga', m.xga,
                     'poss_pct', m.poss_pct, 'formation', m.formation) as extras
from silver.dm_matches m
join silver.dm_clubs c on c.team_id = m.team_id;

create or replace view adapt.derbymanager_standing with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  s.team                                            as team_id,        -- pas d'identifiant dans le classement
  s.team                                            as team_label,
  exists (select 1 from silver.dm_clubs c where c.club = s.team) as is_mine,
  s.competition || ' S' || s.season                 as season_id,
  (s.captured_at at time zone 'Europe/Paris')::date as day,
  s.played                                          as round_no,
  s.rank, s.played, s.pts as points, s.w as wins, s.d as draws, s.l as losses, s.gf, s.ga,
  jsonb_build_object('gd', s.gd, 'form', s.form) as extras
from silver.dm_standings s;

create or replace view adapt.derbymanager_finance_daily with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  f.team_id::text                                   as team_id,
  (f.captured_at at time zone 'Europe/Paris')::date as day,
  f.money                                           as balance,
  null::numeric                                     as income,
  null::numeric                                     as expenses,
  f.salaries_now                                    as salaries,       -- par jour
  f.salary_cap                                      as wage_cap,
  null::numeric                                     as capacite_invest,
  jsonb_build_object('periode', 'jour', 'salaries_committed', f.salaries_committed, 'daily_turnover', f.daily_turnover,
                     'daily_total', f.daily_total, 'stadium_daily', f.stadium_daily, 'broadcasting', f.broadcasting,
                     'sponsorship', f.sponsorship, 'maintenance', f.maintenance, 'merchandise', f.merchandise,
                     'youth_school', f.youth_school, 'expectation_rank', f.expectation_rank) as extras
from silver.dm_finances f
join silver.dm_clubs c on c.team_id = f.team_id;

-- Installations (une ligne) et stade (une ligne) de la page Facilities.
create or replace view adapt.derbymanager_facility with (security_invoker = true) as
select 'derbymanager'::text as game, f.team_id::text as team_id, 'installations' as facility_id,
       (f.captured_at at time zone 'Europe/Paris')::date as day, 'Facilities ' || f.facilities_tier as name,
       'entrainement' as kind, f.facilities_level::numeric as level, null::int as capacity,
       null::numeric as upkeep,
       jsonb_build_object('tier', f.facilities_tier, 'maintenance_pct', f.maintenance_pct, 'downgrade_at', f.downgrade_at,
                          'current_value', f.current_value, 'daily_change', f.daily_change, 'upgrade_at', f.upgrade_at,
                          'reputation', f.reputation) as extras
from silver.dm_facilities f join silver.dm_clubs c on c.team_id = f.team_id
union all
select 'derbymanager', f.team_id::text, 'stade', (f.captured_at at time zone 'Europe/Paris')::date, 'Stade', 'stade',
       null, f.stadium_capacity, null,
       jsonb_build_object('upkeep_pct', f.stadium_upkeep_pct, 'features', f.stadium_features)
from silver.dm_facilities f join silver.dm_clubs c on c.team_id = f.team_id
where f.stadium_capacity is not null;

create or replace view adapt.derbymanager_academy_prospect with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  s.team_id::text                                   as team_id,
  s.name                                            as prospect_id,
  (s.captured_at at time zone 'Europe/Paris')::date as day,
  s.captured_at                                     as seen_at,
  s.name, s.pos as position, s.age,
  null::numeric as rating_min, null::numeric as rating_max,
  null::numeric as potential_min, null::numeric as potential_max,   -- potentiel en mots (extras)
  'candidat'::text                                  as status,
  null::jsonb                                       as skills,
  jsonb_build_object('days_left', s.days_left, 'until', s.until_txt, 'tested', s.tested, 'potential_level', s.potential_level,
                     'potential_target', s.potential_target, 'natural_fitness', s.natural_fitness,
                     'personality', s.personality, 'height_cm', s.height_cm, 'foot', s.foot, 'skills_txt', s.skills_txt) as extras
from silver.dm_school s
join silver.dm_clubs c on c.team_id = s.team_id;

create or replace view adapt.derbymanager_training_plan with (security_invoker = true) as
select
  'derbymanager'::text                              as game,
  t.team_id::text                                   as team_id,
  t.name                                            as player_id,
  (t.captured_at at time zone 'Europe/Paris')::date as day,
  t.name, false as is_academy,
  t.group_training                                  as focus_primary,
  null::text                                        as focus_secondary,
  case t.intensity when 'LOW' then 33 when 'MED' then 67 when 'HIGH' then 100 end::numeric as intensity,
  jsonb_build_object('intensity_label', t.intensity, 'group', t.grp_name, 'tr', t.tr, 'mentor', t.mentor,
                     'pot', t.pot, 'gained', t.gained, 'lost', t.lost) as extras
from silver.dm_training t
join silver.dm_clubs c on c.team_id = t.team_id;

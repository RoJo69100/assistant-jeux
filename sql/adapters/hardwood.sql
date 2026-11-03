-- Refonte v2, étape 1.2 : adaptateur Hardwood (basket universitaire) vers le contrat core (plan §1.1).
-- Pages DOM seulement (silver.hw_pages : dernière capture de chaque page, pages anti-robot écartées).
-- Une équipe (silver.hw_own) ; pas de finances ni de transferts dans le jeu (hardwood-regles) : finance_daily et
-- market_listing non branchés. Les recrues (lycée, JuCo, international) vont dans academy_prospect.
-- Compétences 0–20 (hardwood-regles) ; valeurs affichées ±20 % (hardwood-regles) : brutes dans skills.
-- Calendrier : la date du jeu (« Game Date ») n'est pas la date réelle ; fixture branchée plus tard (gold.hw_today
-- convertit l'heure de simulation ; à reprendre avec sa règle).

insert into core.game_params (game, key, value, source, verified_on) values
  ('hardwood', 'echelle_competence', '{"min": 0, "max": 20}', 'hardwood-regles (compétences 0-20)', '2026-11-04'),
  ('hardwood', 'bourses_max',        '13',                     'hardwood-regles (effectif : 13 bourses + walk-ons)', '2026-11-04'),
  ('hardwood', 'points_recrutement_max', '45',                 'hardwood-recrutement (plafond 45)', '2026-11-04')
on conflict (game, key) do nothing;

-- Effectif : dernière page Roster de mon équipe (un relevé = la date réelle de capture, Europe/Paris).
create or replace view adapt.hardwood_player_daily with (security_invoker = true) as
select
  'hardwood'::text                                  as game,
  o.team_id::text                                   as team_id,
  o.team_name                                       as club_label,
  coalesce(r.player_id::text, r.name)               as player_id,
  (r.captured_at at time zone 'Europe/Paris')::date as day,
  r.name                                            as name,
  r.pos                                             as position,
  null::int                                         as age,          -- classe (FR, SO, JR, SR) dans extras
  r.si::numeric                                     as rating,       -- Skill Index (hardwood-regles)
  null::numeric                                     as form,
  null::numeric                                     as fatigue,      -- fatigue par match seulement (feuille de match)
  null::numeric                                     as morale,
  r.injured                                         as injured,
  false                                             as suspended,    -- pas de suspension dans le jeu
  null::numeric                                     as salary,       -- bourses, pas de salaires
  null::date                                        as contract_end,
  null::numeric                                     as market_value,
  false                                             as is_academy,
  jsonb_build_object('ins', r.ins, 'os', r.os, 'rng', r.rng, 'fin', r.fin, 'reb', r.reb, 'idef', r.idef,
                     'pdef', r.pdef, 'iq', r.iq, 'pass', r.pass, 'hnd', r.hnd, 'drv', r.drv, 'str', r.str,
                     'spd', r.spd, 'sta', r.sta) as skills,
  jsonb_build_object('pot', r.pot, 'stars', r.stars, 'class', r.class, 'redshirted', r.redshirted,
                     'scholarship', r.scholarship, 'injury_days', r.injury_days, 'jersey', r.jersey,
                     'height_m', r.height_m, 'positions', r.positions, 'game_date', r.game_date_txt,
                     'captured_at', r.captured_at) as extras
from silver.hw_roster r
cross join silver.hw_own o;

-- Classement de ma conférence (dernière page Conference).
create or replace view adapt.hardwood_standing with (security_invoker = true) as
select
  'hardwood'::text                                  as game,
  s.team                                            as team_id,       -- pas d'identifiant d'équipe dans le tableau
  s.team                                            as team_label,
  s.team = o.team_name                              as is_mine,
  s.conference                                      as season_id,
  (s.captured_at at time zone 'Europe/Paris')::date as day,
  null::int                                         as round_no,
  s.rank                                            as rank,
  s.w + s.l                                         as played,
  null::int                                         as points,        -- classement aux victoires
  s.w                                               as wins,
  0                                                 as draws,
  s.l                                               as losses,
  s.pf::int                                         as gf,
  s.pa::int                                         as ga,
  jsonb_build_object('conf_w', s.conf_w, 'conf_l', s.conf_l, 'home', s.home, 'away', s.away,
                     'streak', s.streak, 'rpi', s.rpi, 'sos', s.sos) as extras
from silver.hw_standings s
cross join silver.hw_own o;

-- Recrues suivies (page Recruiting) : prospect_id = nom (pas d'identifiant dans le tableau).
create or replace view adapt.hardwood_academy_prospect with (security_invoker = true) as
select
  'hardwood'::text                                  as game,
  o.team_id::text                                   as team_id,
  r.prospect                                        as prospect_id,
  (r.captured_at at time zone 'Europe/Paris')::date as day,
  r.captured_at                                     as seen_at,
  r.prospect                                        as name,
  r.pos                                             as position,
  null::int                                         as age,
  r.si::numeric                                     as rating_min,    -- Skill Index affiché ±20 % (hardwood-regles)
  r.si::numeric                                     as rating_max,
  r.pot::numeric                                    as potential_min,
  r.pot::numeric                                    as potential_max,
  case when r.offered then 'offre' else 'suivi' end as status,
  null::jsonb                                       as skills,
  jsonb_build_object('class', r.class, 'stars', r.stars, 'interest', r.interest, 'competition', r.competition,
                     'contacts', r.contacts, 'hometown', r.hometown, 'top_skills', r.top_skills,
                     'round', r.round, 'rounds', r.rounds, 'points', r.points, 'points_max', r.points_max) as extras
from silver.hw_recruiting r
cross join silver.hw_own o;

-- Coachs (head + 3 assistants) : niveau = moyenne des 6 compétences 0–20, ramenée à 0–100.
create or replace view adapt.hardwood_staff with (security_invoker = true) as
select
  'hardwood'::text                                  as game,
  o.team_id::text                                   as team_id,
  c.role || ' ' || c.coach                          as staff_id,
  (c.captured_at at time zone 'Europe/Paris')::date as day,
  c.coach                                           as name,
  c.role                                            as role,
  round(100.0 * (c.off + c.def + c.tac + c.dev + c.mot + c.rec) / (6 * 20), 1) as level,
  c.salary_m * 1000000                              as salary,
  jsonb_build_object('off', c.off, 'def', c.def, 'tac', c.tac, 'dev', c.dev, 'mot', c.mot, 'rec', c.rec,
                     'age', c.age, 'years', c.years) as extras
from silver.hw_coaches c
cross join silver.hw_own o;

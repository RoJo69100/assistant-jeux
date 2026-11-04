-- Refonte v2, étape 1.2 : adaptateur Team Soccer vers le contrat core (plan §1.1).
-- Mince : renommage, échelles, competition_kind, my_result (calculé une fois ici, même règle que gold.ts_match_report).
-- Deux clubs = deux team_id (18 Chomelix Cows, 15858 Ben Ahmed Donkey) ; seuls mes clubs sont gardés.
-- Colonnes absentes du jeu ou de la collecte = null, déclarées dans docs/attentes/jeux/teamsoccer.yaml (core.limites).
-- Non sourcés, donc absents de game_params : points par victoire (3 dans silver.ts_standings, non écrit dans le guide),
-- places de montée et de descente (barrages : « détail exact non écrit dans le guide », teamsoccer-saison/02-ligue).

insert into core.game_params (game, key, value, source, verified_on) values
  ('teamsoccer', 'equipes_par_ligue',   '8',     'teamsoccer-saison/02-ligue (ligues nationales de 8 équipes)', '2026-11-03'),
  ('teamsoccer', 'rounds_total',        '14',    'teamsoccer-saison/02-ligue (14 journées en semaines 1 à 7)', '2026-11-03'),
  ('teamsoccer', 'match_nul_possible',  'true',  'teamsoccer-saison/03-coupes (tirs au but si égalité en coupe) ; nuls en ligue dans silver.ts_standings', '2026-11-03'),
  ('teamsoccer', 'effectif_min',        '16',    'teamsoccer-joueurs/12-effectif [F:2026-10-18 Admin-Dev]', '2026-11-03'),
  ('teamsoccer', 'effectif_max',        '24',    'teamsoccer-joueurs/12-effectif [F:2026-10-18 Admin-Dev]', '2026-11-03'),
  ('teamsoccer', 'age_declin',          '28',    'teamsoccer-entrainement/02-age [G:Entraînements] (28 ans : aucun point, ou perte)', '2026-11-03'),
  ('teamsoccer', 'ecran_calendrier',
   '{"path_re": "^/rest/v1/matches$", "max_age_h": 12}',
   'silver.ts_matches (endpoint matches) ; rétro 2026-11-02 soir, règle 69 (12 h)', '2026-11-03')
on conflict (game, key) do nothing;

create or replace view adapt.teamsoccer_player_daily with (security_invoker = true) as
select
  'teamsoccer'::text                          as game,
  p.team_id::text                             as team_id,
  t.name                                      as club_label,
  p.player_id::text                           as player_id,
  p.day                                       as day,
  p.name                                      as name,
  p.position                                  as position,     -- GK / DEF / MID / FWD de l'API
  p.age                                       as age,
  p.ovr                                       as rating,       -- OVR 0–100 (teamsoccer-joueurs)
  p.forme / 100.0                             as form,         -- Forme 0–100 (teamsoccer-joueurs/06)
  null::numeric                               as fatigue,      -- endurance = compétence (skills.stamina), pas d'état de fatigue
  null::numeric                               as morale,       -- moral d'équipe seulement (silver.ts_my_teams.team_morale)
  p.injury_days > 0                           as injured,
  p.suspended                                 as suspended,
  p.wage::numeric                             as salary,       -- par semaine (extras.salary_period)
  null::date                                  as contract_end, -- pas de contrat dans le jeu
  p.value::numeric                            as market_value,
  false                                       as is_academy,   -- les jeunes sont dans academy_prospect
  jsonb_build_object('goalkeeper', p.goalkeeper, 'defense', p.defense, 'ball_control', p.ball_control,
                     'passing', p.passing, 'crosses', p.crosses, 'dribbling', p.dribbling, 'heading', p.heading,
                     'finishing', p.finishing, 'stamina', p.stamina, 'pace', p.pace) as skills,
  jsonb_build_object('salary_period', 'semaine', 'nickname', p.nickname, 'nationality', p.nationality,
                     'talent', p.talent, 'form_label', p.form_label, 'injury_days', p.injury_days,
                     'yellow_cards', p.yellow_cards, 'shirt_number', p.shirt_number,
                     'official_matches', p.official_matches, 'official_goals', p.official_goals,
                     'official_assists', p.official_assists, 'official_tackles', p.official_tackles,
                     'captured_at', p.captured_at) as extras
from silver.ts_player_snapshots p
join silver.ts_my_teams t on t.team_id = p.team_id;

-- Matchs de mes clubs. barrage -> playoff ; inconnu (match admin sans compétition) -> autre.
-- my_result : sur le score ; une égalité de coupe reste D, le vainqueur aux tirs au but est dans extras.
create or replace view adapt.teamsoccer_fixture with (security_invoker = true) as
select
  'teamsoccer'::text                                   as game,
  m.my_team_id::text                                   as team_id,
  m.match_id::text                                     as fixture_id,
  case m.competition when 'ligue' then 'ligue' when 'coupe' then 'coupe' when 'amical' then 'amical'
                     when 'barrage' then 'playoff' else 'autre' end as competition_kind,
  null::int                                            as round_no,      -- numéro de journée non exporté
  case when m.competition = 'ligue' then 14 end        as rounds_total,  -- core.game_params rounds_total
  m.match_date_paris::date                             as day,
  m.match_date                                         as scheduled_at,
  m.status = 'finished' and m.home_score is not null   as played,
  case when m.status = 'finished' then case m.venue when 'domicile' then m.home_score else m.away_score end end as my_score,
  case when m.status = 'finished' then case m.venue when 'domicile' then m.away_score else m.home_score end end as opp_score,
  case when m.status <> 'finished' or m.home_score is null then null
       when m.home_score = m.away_score then 'D'
       when (m.home_score > m.away_score) = (m.venue = 'domicile') then 'W' else 'L' end as my_result,
  case m.venue when 'domicile' then m.away_team else m.home_team end as opponent,
  m.venue = 'domicile'                                 as home,
  jsonb_build_object('competition', m.competition, 'status', m.status, 'series_id', m.series_id,
                     'cup_id', m.cup_id, 'cup_round', m.cup_round, 'is_admin', m.is_admin,
                     'penalties_for', case m.venue when 'domicile' then m.home_penalties else m.away_penalties end,
                     'penalties_against', case m.venue when 'domicile' then m.away_penalties else m.home_penalties end,
                     'last_seen', m.last_seen) as extras
from silver.ts_matches m
where m.my_team_id is not null;

-- Classement : recalculé depuis les matchs joués (silver.ts_standings, sans date) ; day = dernier match de ligue joué
-- de la série. Une saison par série et par date de début : season_id = série + 1er jour de ligue vu.
create or replace view adapt.teamsoccer_standing with (security_invoker = true) as
with serie as (
  select m.series_id, min(m.match_date_paris)::date as debut,
         max(m.match_date_paris) filter (where m.status = 'finished')::date as dernier
  from silver.ts_matches m
  where m.competition = 'ligue'
  group by m.series_id
)
select
  'teamsoccer'::text                       as game,
  s.team_id::text                          as team_id,
  s.team                                   as team_label,
  s.is_mine                                as is_mine,
  s.series_id || ':' || se.debut           as season_id,
  se.dernier                               as day,
  max(s.played) over (partition by s.my_team_id)::int as round_no,
  s.position::int                          as rank,
  s.played::int                            as played,
  s.points::int                            as points,     -- 3 / 1 / 0 dans silver.ts_standings (non sourcé, voir en-tête)
  s.wins::int                              as wins,
  s.draws::int                             as draws,
  s.losses::int                            as losses,
  s.goals_for::int                         as gf,
  s.goals_against::int                     as ga,
  jsonb_build_object('my_team_id', s.my_team_id, 'series_id', s.series_id, 'goal_difference', s.goal_difference,
                     'recalcule', true) as extras
from silver.ts_standings s
join serie se on se.series_id = s.series_id;

-- Finances : un relevé par club et par jour ; lignes de la semaine en cours (extras.periode = semaine).
create or replace view adapt.teamsoccer_finance_daily with (security_invoker = true) as
select
  'teamsoccer'::text                       as game,
  f.team_id::text                          as team_id,
  f.day                                    as day,
  f.balance::numeric                       as balance,
  f.weekly_income::numeric                 as income,
  f.weekly_expenses::numeric               as expenses,
  f.wages_expenses::numeric                as salaries,
  null::numeric                            as wage_cap,      -- pas de plafond salarial
  null::numeric                            as capacite_invest,  -- calculée une fois dans le gold générique (plan 1.4)
  jsonb_build_object('periode', 'semaine', 'last_weekly_process', f.last_weekly_process,
                     'match_income', f.match_income, 'prize_income', f.prize_income,
                     'player_sales_income', f.player_sales_income, 'other_income', f.other_income,
                     'stadium_maintenance', f.stadium_maintenance, 'stadium_building', f.stadium_building,
                     'new_signings', f.new_signings, 'staff_expenses', f.staff_expenses,
                     'youth_expenses', f.youth_expenses, 'other_expenses', f.other_expenses,
                     'total_wages', f.total_wages, 'total_match_income', f.total_match_income,
                     'total_player_sales', f.total_player_sales, 'total_new_signings', f.total_new_signings,
                     'total_stadium_building', f.total_stadium_building,
                     'total_stadium_maintenance', f.total_stadium_maintenance) as extras
from silver.ts_finances f
join silver.ts_my_teams t on t.team_id = f.team_id;

-- Marché : chaque annonce vue (dernière capture) ; marché masculin -> Chomelix Cows, féminin -> Ben Ahmed Donkey.
-- price = prix demandé (banque) ou prix de départ (enchère de manager) : l'enchère en cours n'est pas exportée.
-- CTE « materialized » : ts_my_teams et ts_my_bids relisent le JSON brut ; sans elles, relus pour chaque annonce (timeout).
create or replace view adapt.teamsoccer_market_listing with (security_invoker = true) as
with mt as materialized (select name from silver.ts_my_teams),
     mb as materialized (select distinct listing_id from silver.ts_my_bids)
select
  'teamsoccer'::text                                     as game,
  case l.market when 'feminin' then '15858' else '18' end as team_id,
  l.listing_id::text                                     as listing_id,
  (l.seen_at at time zone 'Europe/Paris')::date          as day,
  l.seen_at                                              as seen_at,
  l.deadline                                             as ends_at,
  l.listing_type                                         as status,       -- bank | manager
  l.player_id::text                                      as player_id,
  l.name                                                 as name,
  l.position                                             as position,
  l.age                                                  as age,
  l.ovr                                                  as rating,
  l.asking_price::numeric                                as price,
  null::numeric                                          as starting_price,
  l.bids                                                 as bids,
  null::text                                             as seller_id,    -- nom du vendeur seulement
  l.seller                                               as seller_label,
  coalesce(l.seller in (select name from mt), false)     as is_mine,     -- vendeur absent sur certaines annonces de banque
  jsonb_build_object('goalkeeper', l.goalkeeper, 'defense', l.defense, 'ball_control', l.ball_control,
                     'passing', l.passing, 'crosses', l.crosses, 'dribbling', l.dribbling, 'heading', l.heading,
                     'finishing', l.finishing, 'stamina', l.stamina, 'pace', l.pace) as skills,
  jsonb_build_object('market', l.market, 'forme', l.forme, 'value', l.value, 'nationality', l.nationality,
                     'last_bidder_team_id', l.last_bidder_team_id,
                     'my_bid', l.listing_id in (select listing_id from mb)) as extras
from silver.ts_transfer_listings l;

-- Académie : jeunes de mes deux académies (dernier relevé) ; compétences révélées seulement (null sinon),
-- ni note ni potentiel affichés (teamsoccer-entrainement, académie des jeunes).
create or replace view adapt.teamsoccer_academy_prospect with (security_invoker = true) as
select
  'teamsoccer'::text                                     as game,
  y.team_id::text                                        as team_id,
  y.youth_id::text                                       as prospect_id,
  y.day                                                  as day,
  (y.day::timestamp at time zone 'Europe/Paris')         as seen_at,      -- jour seulement
  y.name                                                 as name,
  y.position                                             as position,
  y.age                                                  as age,
  null::numeric                                          as rating_min,
  null::numeric                                          as rating_max,
  null::numeric                                          as potential_min,
  null::numeric                                          as potential_max,
  'candidat'::text                                       as status,
  jsonb_build_object('goalkeeper', y.goalkeeper, 'defense', y.defense, 'ball_control', y.ball_control,
                     'passing', y.passing, 'crosses', y.crosses, 'dribbling', y.dribbling, 'heading', y.heading,
                     'finishing', y.finishing, 'stamina', y.stamina, 'pace', y.pace) as skills,
  jsonb_build_object('academy_id', y.academy_id, 'talent', y.talent, 'is_high_performance', y.is_high_performance,
                     'revealed_skills', y.revealed_skills, 'revealed_count', y.revealed_count,
                     'last_reveal_date', y.last_reveal_date, 'seen_at_precision', 'jour') as extras
from silver.ts_youth_players y
join silver.ts_my_teams t on t.team_id = y.team_id;

-- Personnel : l'entraîneur de chaque club (5 niveaux : 1 Faible … 5 Formidable, teamsoccer-entrainement/05).
-- level = niveau × 20 ; l'API donne un libellé anglais (« poor » = Faible = 1) ; libellé inconnu = null.
create or replace view adapt.teamsoccer_staff with (security_invoker = true) as
with releve as (
  select max(a.day) as day
  from silver.ts_api a cross join silver.ts_me me
  where a.endpoint = 'teams' and a.q_manager_id = me.manager_id
), niveau as (
  select t.*, coalesce(t.coach_level,
           case lower(t.coach_level_label) when 'poor' then 1 end) as n
  from silver.ts_my_teams t
)
select
  'teamsoccer'::text                                     as game,
  n.team_id::text                                        as team_id,
  'entraineur'::text                                     as staff_id,     -- un seul par club, sans nom ni identifiant
  r.day                                                  as day,
  'Entraîneur'::text                                     as name,
  'coach'::text                                          as role,
  n.n * 20::numeric                                      as level,
  null::numeric                                          as salary,       -- dans finances (extras.staff_expenses), pas par personne
  jsonb_build_object('niveau_1_5', n.n, 'label', n.coach_level_label) as extras
from niveau n cross join releve r;

-- Entraînement : réglage actuel des joueurs de mon effectif actuel (silver.ts_training garde le dernier par joueur).
create or replace view adapt.teamsoccer_training_plan with (security_invoker = true) as
select
  'teamsoccer'::text                                     as game,
  p.team_id::text                                        as team_id,
  t.player_id::text                                      as player_id,
  t.day                                                  as day,
  p.name                                                 as name,
  false                                                  as is_academy,
  t.training_type                                        as focus_primary,
  null::text                                             as focus_secondary,  -- une compétence par joueur
  t.intensity / 100.0                                    as intensity,        -- 0–100 % (teamsoccer-entrainement/04)
  jsonb_build_object('last_trained_type', t.last_trained_type, 'skill_progress', t.skill_progress,
                     'last_change', t.last_change, 'stamina_progress', t.stamina_progress,
                     'stamina_last_change', t.stamina_last_change, 'pace_progress', t.pace_progress,
                     'pace_last_change', t.pace_last_change, 'captured_at', t.captured_at) as extras
from silver.ts_training t
join silver.ts_players p on p.player_id = t.player_id;

-- Bâtiments : stade (places par type ; entretien = dernière ligne hebdomadaire des finances, teamsoccer-club/02)
-- et Centre de Haute Performance (TSCredits, saison en cours).
create or replace view adapt.teamsoccer_facility with (security_invoker = true) as
select
  'teamsoccer'::text                                     as game,
  s.team_id::text                                        as team_id,
  'stade'::text                                          as facility_id,
  s.day                                                  as day,
  s.name                                                 as name,
  'stade'::text                                          as kind,
  null::numeric                                          as level,        -- pas de niveau : places par type
  s.capacity                                             as capacity,
  f.stadium_maintenance::numeric                         as upkeep,       -- par semaine (extras.upkeep_period)
  jsonb_build_object('upkeep_period', 'semaine', 'upkeep_day', f.day, 'seats_standing', s.seats_standing,
                     'seats_basic', s.seats_basic, 'seats_covered', s.seats_covered, 'seats_vip', s.seats_vip) as extras
from silver.ts_stadiums s
join silver.ts_my_teams t on t.team_id = s.team_id
left join lateral (
  select x.day, x.stadium_maintenance from silver.ts_finances x
  where x.team_id = s.team_id and x.day <= s.day order by x.day desc limit 1
) f on true
union all
select
  'teamsoccer', h.team_id::text, 'centre_haute_performance', h.day, 'Centre de Haute Performance', 'academie',
  null::numeric, null::int, null::numeric,
  jsonb_build_object('season', h.season, 'status', h.status, 'total_tsc', h.total_tsc,
                     'last_payment_week', h.last_payment_week, 'options_week', h.options_week,
                     'week_options', h.week_options, 'chosen_skills', h.chosen_skills,
                     'youth_player_id', h.youth_player_id, 'account_tsc', h.account_tsc)
from (select distinct on (x.team_id) x.* from silver.ts_hpc x
      join silver.ts_my_teams t on t.team_id = x.team_id
      order by x.team_id, x.season desc) h;

grant select on adapt.teamsoccer_player_daily, adapt.teamsoccer_fixture, adapt.teamsoccer_standing,
                adapt.teamsoccer_finance_daily, adapt.teamsoccer_market_listing,
                adapt.teamsoccer_academy_prospect, adapt.teamsoccer_staff, adapt.teamsoccer_training_plan,
                adapt.teamsoccer_facility to assistant_ro;

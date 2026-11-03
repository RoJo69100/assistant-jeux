-- Refonte v2, étape 1.2 : adaptateur Hockey Nation vers le contrat core (plan §1.1).
-- Mince : renommage, échelles, competition_kind. my_result vient tel quel de silver.hn_games (R-9).
-- Quatre équipes (PRO, FRM, U21, U17) = quatre team_id ; niveau dans extras.team_level.
-- Colonnes absentes du jeu ou de la collecte = null, déclarées dans docs/attentes/jeux/hockeynation.yaml (core.limites).

insert into core.game_params (game, key, value, source, verified_on) values
  ('hockeynation', 'equipes_par_ligue',  '20',  'hockeynation-match-calendrier/01-competitions (2 conférences)', '2026-11-03'),
  ('hockeynation', 'rounds_total',       '30',  'hockeynation-match-calendrier/01-competitions (30 matchs en 35 jours)', '2026-11-03'),
  ('hockeynation', 'playoff_slots',      '8',   'hockeynation-match-calendrier/01-competitions (top 4 de chaque conférence)', '2026-11-03'),
  ('hockeynation', 'promo_slots',        '2',   'hockeynation-match-calendrier/01-competitions (les 2 finalistes)', '2026-11-03'),
  ('hockeynation', 'releg_slots',        '4',   'hockeynation-match-calendrier/01-competitions (2 derniers de chaque conférence)', '2026-11-03'),
  ('hockeynation', 'effectif_max_farm',  '30',  'hockeynation-joueurs/01-les-4-equipes [G:Teams]', '2026-11-03')
on conflict (game, key) do nothing;

create or replace view adapt.hockeynation_player_daily with (security_invoker = true) as
select
  'hockeynation'::text                        as game,
  p.team_id::text                             as team_id,
  t.city || ' ' || t.nickname                 as club_label,
  p.player_id::text                           as player_id,
  p.day                                       as day,
  p.name                                      as name,
  p.main_position                             as position,
  p.age                                       as age,
  p.rating::numeric                           as rating,      -- OVR 0–100 (hockeynation-joueurs/08)
  null::numeric                               as form,        -- pas de forme dans le jeu
  null::numeric                               as fatigue,     -- condition en match seulement, non collectée
  null::numeric                               as morale,
  null::boolean                               as injured,     -- blessures non implémentées à notre connaissance (hypothèse, joueurs/08)
  null::boolean                               as suspended,
  c.salary                                    as salary,      -- contrat actif ; U17/U21 sans contrat = null
  null::date                                  as contract_end, -- fin de contrat en numéro de saison (extras.contract_to)
  null::numeric                               as market_value,
  p.team_level in ('U17', 'U21')              as is_academy,  -- équipes de jeunes
  p.skills                                    as skills,
  jsonb_build_object(
    'team_level', p.team_level, 'xp', p.xp, 'skater', p.skater, 'positions', p.positions,
    'talents', p.talents, 'special_skills', p.special_skills, 'draft_rank', p.draft_rank,
    'contract_from', c.season_from, 'contract_to', c.season_to, 'contract_remaining', c.remaining,
    'elc', c.elc, 'frm', c.frm, 'expiring', p.expiring, 'tradable', p.tradable,
    'on_trade_block', p.on_trade_block, 'retiring', p.retiring, 'scouted_times', p.scouted_times
  )                                           as extras
from silver.hn_player_snapshots p
left join silver.hn_my_teams t on t.team_id = p.team_id
left join lateral (
  select (x->>'salary')::numeric as salary, (x->>'from')::int as season_from, (x->>'to')::int as season_to,
         (x->>'remaining')::int as remaining, (x->>'elc')::boolean as elc, (x->>'frm')::boolean as frm
  from jsonb_array_elements(p.contracts) x
  where (x->>'active')::boolean
  limit 1
) c on true;

create or replace view adapt.hockeynation_fixture with (security_invoker = true) as
with mes_matchs as (
  select g.*,
         case when g.home_is_mine then 'home' else 'away' end as my_side
  from silver.hn_games g
  where g.home_is_mine or g.away_is_mine
)
select
  'hockeynation'::text                                 as game,
  m.teams -> m.my_side ->> 'id'                        as team_id,
  m.game_id::text                                      as fixture_id,
  case m.game_type when 'League' then 'ligue' when 'Playoffs' then 'playoff'
                   when 'Friendly' then 'amical' else 'autre' end as competition_kind,
  null::int                                            as round_no,      -- numéro de journée non exporté (extras.season_day = jour de saison)
  case when m.game_type = 'League' then 30 end         as rounds_total,  -- core.game_params rounds_total
  (m.scheduled_at at time zone 'Europe/Paris')::date   as day,           -- fuseau_affichage
  m.scheduled_at                                       as scheduled_at,
  m.status = 'ended'                                   as played,
  case m.my_side when 'home' then m.home_score else m.away_score end as my_score,
  case m.my_side when 'home' then m.away_score else m.home_score end as opp_score,
  m.my_result                                          as my_result,
  case m.my_side when 'home' then m.away else m.home end             as opponent,
  m.my_side = 'home'                                   as home,
  jsonb_build_object('season_day', m.season_day, 'status', m.status, 'team_level', m.team_level,
                     'winner', m.winner) as extras
from mes_matchs m;

-- Classement : relevés qui contiennent une de mes équipes (les autres ligues sont écartées).
create or replace view adapt.hockeynation_standing with (security_invoker = true) as
with lignes as (
  select s.day, split_part(s.endpoint, '/', 3) as league_id, e
  from silver.hn_standings s, jsonb_array_elements(s.standing -> 'entries') e
),
releves as (
  select distinct l.day, l.league_id from lignes l
  join silver.hn_my_teams t on t.team_id::text = l.e ->> 'id'
)
select
  'hockeynation'::text                     as game,
  l.e ->> 'id'                             as team_id,
  coalesce(n.t ->> 'city', '') || ' ' || coalesce(n.t ->> 'nickname', '') as team_label,
  exists (select 1 from silver.hn_my_teams t where t.team_id::text = l.e ->> 'id') as is_mine,
  l.league_id                              as season_id,   -- identifiant de ligue (une ligue par saison)
  l.day                                    as day,
  max((l.e ->> 'gp')::int) over (partition by l.league_id, l.day) as round_no,
  (l.e ->> 'pos')::int                     as rank,
  (l.e ->> 'gp')::int                      as played,
  (l.e ->> 'pts')::int                     as points,
  (l.e ->> 'won')::int                     as wins,
  null::int                                as draws,       -- règle des points et des prolongations non sourcée
  (l.e ->> 'lost')::int                    as losses,
  (l.e ->> 'gf')::int                      as gf,
  (l.e ->> 'ga')::int                      as ga,
  jsonb_build_object('ot', (l.e ->> 'ot')::int, 'l10', l.e ->> 'l10', 'bot', l.e -> 'team' -> 'bot',
                     'home_won', (l.e ->> 'homeWon')::int, 'home_lost', (l.e ->> 'homeLost')::int,
                     'away_won', (l.e ->> 'awayWon')::int, 'away_lost', (l.e ->> 'awayLost')::int,
                     'conf_won', (l.e ->> 'confWon')::int, 'conf_lost', (l.e ->> 'confLost')::int) as extras
from lignes l
join releves r on r.day = l.day and r.league_id = l.league_id
left join lateral (
  select t from silver.hn_standings s2, jsonb_array_elements(s2.teams) t
  where s2.day = l.day and t ->> 'id' = l.e ->> 'id'
  limit 1
) n on true;

-- Finances : plafond salarial PRO (pas de solde dans le jeu) ; salaries = masse salariale projetée de la saison.
create or replace view adapt.hockeynation_finance_daily with (security_invoker = true) as
select
  'hockeynation'::text                     as game,
  (select t.team_id::text from silver.hn_my_teams t where t.level = 'PRO') as team_id,
  f.day                                    as day,
  null::numeric                            as balance,      -- pas de trésorerie : économie au plafond salarial
  null::numeric                            as income,
  null::numeric                            as expenses,
  f.total_projected_salary::text::numeric  as salaries,
  f.salary_cap::text::numeric              as wage_cap,     -- contrats-finances/01-plafond-salarial-pro
  null::numeric                            as capacite_invest,  -- calculée une fois dans le gold générique (plan 1.4)
  jsonb_build_object('periode', 'saison', 'season', f.season,
                     'cap_space', f.salary_cap::text::numeric - f.total_projected_salary::text::numeric,
                     'salary_cap_projection', f.salary_cap_projection) as extras
from silver.hn_finances f;

-- Marché : agents libres et trade block vus ; un joueur = une annonce par source, au dernier relevé.
-- Pas d'enchère ni de prix dans le jeu (signature au salaire, échanges) ; relevés datés au jour seulement.
create or replace view adapt.hockeynation_market_listing with (security_invoker = true) as
select distinct on (m.source, m.player_id)
  'hockeynation'::text                                   as game,
  pro.team_id::text                                      as team_id,
  m.source || ':' || m.player_id                         as listing_id,
  m.day                                                  as day,
  (m.day::timestamp at time zone 'Europe/Paris')         as seen_at,      -- jour seulement (extras.seen_at_precision)
  null::timestamptz                                      as ends_at,
  m.source                                               as status,       -- free_agent | trade_block
  m.player_id::text                                      as player_id,
  m.name                                                 as name,
  m.main_position                                        as position,
  m.age                                                  as age,
  m.rating::numeric                                      as rating,       -- OVR 0–100 (hockeynation-joueurs/08)
  null::numeric                                          as price,
  null::numeric                                          as starting_price,
  null::int                                              as bids,
  null::text                                             as seller_id,
  m.team                                                 as seller_label,
  exists (select 1 from silver.hn_my_teams t where t.city || ' ' || t.nickname = m.team) as is_mine,
  m.skills                                               as skills,
  jsonb_build_object('seen_at_precision', 'jour', 'fa_salary', m.fa_salary, 'fa_years', m.fa_years,
                     'positions', m.positions, 'talents', m.talents, 'special_skills', m.special_skills,
                     'contracts', m.contracts) as extras
from silver.hn_market_players m
cross join (select team_id from silver.hn_my_teams where level = 'PRO') pro
order by m.source, m.player_id, m.day desc;

-- Draft : classe de ma ligue seulement (ligues où une de mes équipes est classée) ; note visible = OVR,
-- potentiel non affiché (calcul dans hockeynation-potentiel-joueurs, pas dans l'adaptateur).
create or replace view adapt.hockeynation_academy_prospect with (security_invoker = true) as
with mes_ligues as (
  select distinct split_part(s.endpoint, '/', 3) as league_id
  from silver.hn_standings s, jsonb_array_elements(s.standing -> 'entries') e
  join silver.hn_my_teams t on t.team_id::text = e ->> 'id'
)
select distinct on (d.season, d.player_id)
  'hockeynation'::text                                   as game,
  pro.team_id::text                                      as team_id,
  d.season || ':' || d.player_id                         as prospect_id,
  d.day                                                  as day,
  (d.day::timestamp at time zone 'Europe/Paris')         as seen_at,      -- jour seulement
  d.name                                                 as name,
  d.main_position                                        as position,
  d.age                                                  as age,
  d.rating::numeric                                      as rating_min,   -- OVR affiché (null si non scouté)
  d.rating::numeric                                      as rating_max,
  null::numeric                                          as potential_min,
  null::numeric                                          as potential_max,
  'candidat'::text                                       as status,
  d.skills                                               as skills,
  jsonb_build_object('season', d.season, 'league_id', split_part(d.endpoint, '/', 3), 'draft_rank', d.draft_rank,
                     'skater', d.skater, 'u17_team', d.u17_team, 'from_my_u17', d.from_my_u17,
                     'scouted_times', d.scouted_times, 'can_scout', d.can_scout, 'talents', d.talents,
                     'special_skills', d.special_skills, 'seen_at_precision', 'jour') as extras
from silver.hn_draft_class d
join mes_ligues l on l.league_id = split_part(d.endpoint, '/', 3)
cross join (select team_id from silver.hn_my_teams where level = 'PRO') pro
order by d.season, d.player_id, d.day desc;

-- Personnel : coachs de mes 4 équipes (note 0–100) et scouts du club (rattachés à l'équipe PRO).
create or replace view adapt.hockeynation_staff with (security_invoker = true) as
select
  'hockeynation'::text                                   as game,
  t.team_id::text                                        as team_id,
  c.coach_id::text                                       as staff_id,
  c.day                                                  as day,
  c.name                                                 as name,
  'coach'::text                                          as role,
  c.rating::numeric                                      as level,
  null::numeric                                          as salary,       -- salaire des coachs non collecté
  jsonb_build_object('team_level', c.team_level, 'head_coach', c.head_coach, 'age', c.age, 'xp', c.xp,
                     'match_rating', c.match_rating, 'training_rating', c.training_rating,
                     'ofp', c.ofp, 'dfp', c.dfp, 'bat', c.bat, 'pp', c.pp, 'pk', c.pk,
                     'skills', c.skills, 'talents', c.talents) as extras
from silver.hn_coaches c
join silver.hn_my_teams t on t.level = c.team_level
union all
select
  'hockeynation', pro.team_id::text, s.scout_id::text, s.day, s.name, 'scout',
  null::numeric,                                                          -- pas de note de scout
  s.daily_salary::numeric,                                                -- par jour (extras.salary_period)
  jsonb_build_object('salary_period', 'jour', 'age', s.age, 'preferred_position', s.preferred_position,
                     'nation', s.nation, 'head_scout', s.head_scout)
from silver.hn_scouts s
cross join (select team_id from silver.hn_my_teams where level = 'PRO') pro;

-- Entraînement : une compétence par joueur et par jour (PRO, FRM réglables ; U21, U17 au hasard) [coachs-entrainement/04].
create or replace view adapt.hockeynation_training_plan with (security_invoker = true) as
select distinct on (t.team_id, l.player_id, l.day)
  'hockeynation'::text                                   as game,
  t.team_id::text                                        as team_id,
  l.player_id::text                                      as player_id,
  l.day                                                  as day,
  l.name                                                 as name,
  l.team_level in ('U17', 'U21')                         as is_academy,
  l.skill                                                as focus_primary,
  null::text                                             as focus_secondary,  -- une seule compétence à la fois
  null::numeric                                          as intensity,
  jsonb_build_object('team_level', l.team_level, 'skill_level', l.skill_level, 'coach_id', l.coach_id,
                     'coach_level', l.coach_level, 'training_rate', l.training_rate,
                     'reglable', l.team_level in ('PRO', 'FRM'), 'captured_at', l.captured_at) as extras
from silver.hn_training_log l
join silver.hn_my_teams t on t.level = l.team_level
order by t.team_id, l.player_id, l.day, l.captured_at desc;

grant select on adapt.hockeynation_player_daily, adapt.hockeynation_fixture,
                adapt.hockeynation_standing, adapt.hockeynation_finance_daily,
                adapt.hockeynation_market_listing, adapt.hockeynation_academy_prospect,
                adapt.hockeynation_staff, adapt.hockeynation_training_plan to assistant_ro;

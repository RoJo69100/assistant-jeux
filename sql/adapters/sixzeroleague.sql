-- Refonte v2, étape 1.2 : adaptateur Six Zero League (handball) vers le contrat core (plan §1.1).
-- Mince : renommage, échelles, competition_kind, my_result (W/D/L de silver.sz_matches -> V/N/D).
-- Une équipe (silver.sz_my_team, uuid) ; une semaine financière = 2 journées de ligue (sixzeroleague-club, Semaine financière).
-- Colonnes absentes du jeu ou de la collecte = null, déclarées dans docs/attentes/jeux/sixzeroleague.yaml (core.limites).
-- Non sourcés, donc absents de game_params : points par victoire, places de montée et de descente.

insert into core.game_params (game, key, value, source, verified_on) values
  ('sixzeroleague', 'equipes_par_ligue',  '10',   'sixzeroleague-match (ligues de 10, 5 divisions)', '2026-11-04'),
  ('sixzeroleague', 'match_nul_possible', 'true', 'silver.sz_standings (colonne draws) ; sixzeroleague-match (points, départages)', '2026-11-04'),
  ('sixzeroleague', 'ecran_calendrier',
   '{"path_re": "^/api/seasons/current$", "max_age_h": 12}',
   'silver.sz_schedule (endpoint /seasons/current) ; rétro 2026-11-02 soir, règle 69 (12 h)', '2026-11-04')
on conflict (game, key) do nothing;

-- Joueurs : un relevé par joueur et par jour (silver.sz_player_snapshots). Compétences 1–100 [W:Attributes].
create or replace view adapt.sixzeroleague_player_daily with (security_invoker = true) as
select
  'sixzeroleague'::text            as game,
  t.team_id::text                  as team_id,
  t.name                           as club_label,
  p.player_id::text                as player_id,
  p.day                            as day,
  p.name                           as name,
  p.role                           as position,      -- 7 rôles (sixzeroleague-joueurs)
  p.age                            as age,
  p.overall::numeric               as rating,        -- note globale 1–100
  null::numeric                    as form,          -- pas de forme dans le jeu (sixzeroleague-joueurs)
  null::numeric                    as fatigue,       -- endurance = compétence (skills.stamina)
  null::numeric                    as morale,        -- pas de moral exporté
  p.injured                        as injured,
  p.suspended                      as suspended,
  p.wage::numeric                  as salary,        -- par semaine financière (extras.salary_period)
  null::date                       as contract_end,  -- pas de contrat ; salaire revu entre les saisons
  null::numeric                    as market_value,  -- pas de valeur affichée
  false                            as is_academy,    -- les U18 sont dans academy_prospect
  p.attributes                     as skills,
  jsonb_build_object('salary_period', 'semaine (2 journées)', 'number', p.number, 'height_cm', p.height_cm,
                     'preferred_hand', p.preferred_hand, 'country', p.country, 'retiring', p.retiring,
                     'for_sale', p.for_sale, 'secondary_roles', p.secondary_roles, 'role_overalls', p.role_overalls,
                     'training_progress', p.training_progress, 'captured_at', p.captured_at) as extras
from silver.sz_player_snapshots p
cross join silver.sz_my_team t;

-- Matchs : saison en cours (silver.sz_schedule, matchs que je joue) + matchs exportés (silver.sz_matches, toutes saisons).
-- league -> ligue, cup -> coupe ; my_result W/D/L -> V/N/D ; played = statut 'complete' ou match exporté.
create or replace view adapt.sixzeroleague_fixture with (security_invoker = true) as
with sc as (
  select * from silver.sz_schedule where i_play and match_id is not null
),
mt as (
  select * from silver.sz_matches
)
select
  'sixzeroleague'::text                                  as game,
  t.team_id::text                                        as team_id,
  coalesce(sc.match_id, mt.match_id)::text               as fixture_id,
  case coalesce(sc.competition, mt.competition) when 'league' then 'ligue' when 'cup' then 'coupe' else 'autre' end
                                                         as competition_kind,
  coalesce(sc.round, mt.round)                           as round_no,
  null::int                                              as rounds_total,
  coalesce(mt.match_day, (sc.kickoff_paris)::date)       as day,
  sc.scheduled_at                                        as scheduled_at,
  (mt.match_id is not null or sc.status = 'complete')    as played,
  mt.goals                                               as my_score,
  mt.opp_goals                                           as opp_score,
  case mt.result when 'W' then 'V' when 'D' then 'N' when 'L' then 'D' end as my_result,
  coalesce(sc.opponent, mt.opponent)                     as opponent,
  case coalesce(sc.venue, case mt.venue when 'home' then 'domicile' when 'away' then 'extérieur' end)
       when 'domicile' then true when 'extérieur' then false end as home,
  jsonb_build_object('step_label', sc.label, 'status', sc.status, 'opponent_is_bot', coalesce(sc.opponent_is_bot, mt.opponent_is_bot),
                     'neutre', sc.venue = 'neutre', 'cup_won', sc.cup_won) as extras
from sc
full join mt on mt.match_id = sc.match_id
cross join silver.sz_my_team t
where coalesce(mt.match_day, (sc.kickoff_paris)::date) is not null;

-- Classement de ma ligue (dernière capture de /seasons/current/my-competition).
create or replace view adapt.sixzeroleague_standing with (security_invoker = true) as
select
  'sixzeroleague'::text            as game,
  s.team_id::text                  as team_id,
  s.team                           as team_label,
  coalesce(s.is_mine, false)       as is_mine,
  s.league || ' D' || s.division   as season_id,
  s.day                            as day,
  s.current_round                  as round_no,
  s.position                       as rank,
  s.played, s.points, s.wins, s.draws, s.losses,
  s.goals_for                      as gf,
  s.goals_against                  as ga,
  jsonb_build_object('division', s.division, 'total_rounds', s.total_rounds, 'is_bot', s.is_bot, 'form', s.form) as extras
from silver.sz_standings s;

-- Finances : un relevé par jour ; prévision du cycle (semaine de 2 journées).
create or replace view adapt.sixzeroleague_finance_daily with (security_invoker = true) as
select
  'sixzeroleague'::text            as game,
  t.team_id::text                  as team_id,
  f.day                            as day,
  f.balance::numeric               as balance,
  f.fc_revenue::numeric            as income,      -- prévision de la semaine en cours
  f.fc_expenses::numeric           as expenses,
  f.fc_wages::numeric              as salaries,
  null::numeric                    as wage_cap,    -- pas de plafond salarial
  null::numeric                    as capacite_invest,
  jsonb_build_object('periode', 'semaine (2 journées)', 'fc_net', f.fc_net, 'sponsor', f.sponsor,
                     'sponsor_weekly', f.sponsor_weekly, 'sponsor_win_bonus', f.sponsor_win_bonus,
                     'sponsor_can_choose', f.sponsor_can_choose, 'last_week', f.last_week, 'last_net', f.last_net) as extras
from silver.sz_finances f
cross join silver.sz_my_team t;

-- Marché : chaque annonce vue (dernière capture). is_mine = je suis le vendeur.
create or replace view adapt.sixzeroleague_market_listing with (security_invoker = true) as
select
  'sixzeroleague'::text                         as game,
  t.team_id::text                               as team_id,
  l.listing_id::text                            as listing_id,
  (l.seen_at at time zone 'Europe/Paris')::date as day,
  l.seen_at                                     as seen_at,
  null::timestamptz                             as ends_at,      -- réglé après la journée settle_after_round (extras)
  'vu'::text                                    as status,
  l.player_id::text                             as player_id,
  l.name, l.role                                as position,
  l.age,
  l.overall::numeric                            as rating,
  coalesce(l.current_bid, l.starting_price)::numeric as price,
  l.starting_price::numeric                     as starting_price,
  null::int                                     as bids,
  null::text                                    as seller_id,
  l.seller                                      as seller_label,
  coalesce(l.seller = t.name, false)            as is_mine,
  l.attributes                                  as skills,
  jsonb_build_object('wage', l.wage, 'retiring', l.retiring, 'free_agent', l.free_agent, 'seller_is_bot', l.seller_is_bot,
                     'next_bid', l.next_bid, 'highest_bidder', l.highest_bidder,
                     'settle_after_round', l.settle_after_round, 'height_cm', l.height_cm) as extras
from silver.sz_transfer_listings l
cross join silver.sz_my_team t;

-- Académie U18 : prospects de la dernière capture.
create or replace view adapt.sixzeroleague_academy_prospect with (security_invoker = true) as
select
  'sixzeroleague'::text                          as game,
  t.team_id::text                                as team_id,
  coalesce(p ->> 'id', p ->> 'name')             as prospect_id,
  u.day                                          as day,
  r.captured_at                                  as seen_at,
  p ->> 'name'                                   as name,
  p ->> 'role'                                   as position,
  (p ->> 'age')::int                             as age,
  (p ->> 'overall')::numeric                     as rating_min,
  (p ->> 'overall')::numeric                     as rating_max,
  null::numeric                                  as potential_min,
  null::numeric                                  as potential_max,
  case when u.available then 'candidat' else 'vu' end as status,
  p -> 'attributes'                              as skills,
  jsonb_build_object('rounds_until_next_pick', u.rounds_until_next_pick, 'squad_full', u.squad_full, 'brut', p) as extras
from silver.sz_u18 u
cross join lateral jsonb_array_elements(coalesce(u.prospects, '[]'::jsonb)) p
cross join silver.sz_my_team t
cross join lateral (select max(captured_at) as captured_at from silver.sz_api where endpoint = '/teams/mine/u18') r;

-- Entraînement : intensité d'équipe + focus par joueur (dernière capture).
create or replace view adapt.sixzeroleague_training_plan with (security_invoker = true) as
select
  'sixzeroleague'::text            as game,
  t.team_id::text                  as team_id,
  tp.player_id::text               as player_id,
  tp.day                           as day,
  coalesce(p.name, tp.player_id::text) as name,
  false                            as is_academy,
  coalesce(tp.focus_skill, tp.focus_group) as focus_primary,
  null::text                       as focus_secondary,
  case tp.intensity when 'light' then 33 when 'normal' then 67 when 'high' then 100 end::numeric as intensity,
  jsonb_build_object('intensity_label', tp.intensity, 'focus_group', tp.focus_group, 'focus_skill', tp.focus_skill) as extras
from silver.sz_training_plan tp
cross join silver.sz_my_team t
left join silver.sz_players p on p.player_id = tp.player_id;

-- Infrastructures : niveau actuel de chaque installation (Arena, Training Facilities, Youth Academy, Fan Shop), niveaux 1–20.
create or replace view adapt.sixzeroleague_facility with (security_invoker = true) as
select
  'sixzeroleague'::text            as game,
  t.team_id::text                  as team_id,
  i.facility                       as facility_id,
  i.day                            as day,
  i.facility                       as name,
  case when i.facility ilike '%arena%' then 'stade' when i.facility ilike '%training%' then 'entrainement'
       when i.facility ilike '%youth%' then 'academie' when i.facility ilike '%shop%' then 'commerce' else 'autre' end as kind,
  round(100.0 * i.current_level / 20, 1) as level,   -- niveaux 1–20 (sixzeroleague-club) -> 0–100
  null::int                        as capacity,
  i.weekly_maintenance::numeric    as upkeep,
  jsonb_build_object('niveau', i.current_level, 'niveau_max', 20, 'effet', i.effect_label,
                     'cout_niveau_suivant', n.upgrade_cost_from_current) as extras
from silver.sz_infrastructure_levels i
cross join silver.sz_my_team t
left join silver.sz_infrastructure_levels n on n.facility = i.facility and n.level = i.current_level + 1
where i.level = i.current_level;

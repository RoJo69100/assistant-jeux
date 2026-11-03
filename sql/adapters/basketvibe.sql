-- Refonte v2, étape 1.2 : adaptateur BasketVibe vers le contrat core (plan §1.1).
-- Mince : renommage, échelles, competition_kind. my_result vient tel quel de silver.bv_matches (R-9).
-- Colonnes absentes du jeu ou de la collecte = null, déclarées dans docs/attentes/jeux/basketvibe.yaml (core.limites).

create or replace view adapt.basketvibe_player_daily with (security_invoker = true) as
select
  'basketvibe'::text                          as game,
  p.team_id::text                             as team_id,
  'Chomelix Cow'::text                        as club_label,
  p.player_id::text                           as player_id,
  p.day                                       as day,
  p.name                                      as name,
  p.position                                  as position,
  p.age                                       as age,
  p.ps::numeric                               as rating,      -- PS, moyenne pondérée des compétences 0–99 [M§2.2]
  round((p.form - 1) / 9.0, 4)                as form,        -- 1–10 [M§5.5] -> 0–1
  round(p.fatigue / 100.0, 4)                 as fatigue,     -- 0–100 [M§5.6] -> 0–1
  null::numeric                               as morale,
  coalesce(p.injury_return_on > p.day, false) as injured,
  null::boolean                               as suspended,
  s.salary::numeric                           as salary,
  null::date                                  as contract_end,
  null::numeric                               as market_value,
  false                                       as is_academy,  -- l'effectif seulement ; les prospects sont dans core.academy_prospect
  jsonb_build_object(
    'two_point', p.two_point, 'three_point', p.three_point, 'defense', p.defense, 'passing', p.passing,
    'ball_handling', p.ball_handling, 'rebounding', p.rebounding, 'stamina', p.stamina, 'athleticism', p.athleticism
  )                                           as skills,
  jsonb_build_object(
    'form_raw', p.form, 'fatigue_raw', p.fatigue, 'experience', p.experience,
    'injury_return_on', p.injury_return_on, 'skills_visibility', p.skills_visibility,
    'training_primary', p.training_primary, 'training_secondary', p.training_secondary,
    'salary_day', s.day, 'capture_id', p.capture_id
  )                                           as extras
from silver.bv_player_daily p
left join lateral (
  select w.salary, w.day
  from silver.bv_player_salary_weekly w
  where w.player_id = p.player_id and w.day <= p.day
  order by w.day desc
  limit 1
) s on true;

create or replace view adapt.basketvibe_fixture with (security_invoker = true) as
with mine as (
  select t.team_id::text as team_id from silver.bv_my_team t
),
played as (
  -- Matchs de mon club (ligue, coupe, amical) : une ligne par fixture, la capture la plus récente.
  select distinct on (m.fixture_id) m.*
  from silver.bv_matches m
  where m.my_side is not null
  order by m.fixture_id, m.captured_at desc nulls last
),
scheduled as (
  -- Calendrier de ligue connu mais pas encore exporté comme match.
  select f.*
  from silver.bv_fixtures f
  where f.is_mine and not exists (select 1 from played p where p.fixture_id = f.fixture_id)
)
select
  'basketvibe'::text                                   as game,
  (select team_id from mine)                           as team_id,
  p.fixture_id::text                                   as fixture_id,
  case p.competition when 'league' then 'ligue' when 'cup' then 'coupe'
                     when 'friendly' then 'amical' else 'autre' end as competition_kind,
  p.round_number                                       as round_no,
  case when p.competition = 'league' then 22 end       as rounds_total,  -- core.game_params rounds_total
  p.match_day                                          as day,
  null::timestamptz                                    as scheduled_at,  -- fuseau de kickoff_time non sourcé ; connu seulement pour les amicaux programmés
  p.status = 'finished'                                as played,
  case p.my_side when 'home' then p.home_score else p.away_score end as my_score,
  case p.my_side when 'home' then p.away_score else p.home_score end as opp_score,
  p.my_result                                          as my_result,
  case p.my_side when 'home' then p.away_team else p.home_team end   as opponent,
  p.my_side = 'home'                                   as home,
  jsonb_build_object('match_id', p.match_id, 'season_id', p.season_id, 'status', p.status,
                     'kickoff_time', p.kickoff_time, 'is_walkover', p.is_walkover,
                     'overtime_periods', p.overtime_periods, 'source', 'bv_matches') as extras
from played p
union all
select
  'basketvibe', (select team_id from mine), s.fixture_id::text, 'ligue', s.round_number, 22, s.match_day,
  null::timestamptz, s.status = 'finished',
  null::int, null::int, null::text,  -- score et résultat seulement depuis bv_matches (R-9)
  case when s.home_team_id::text = (select team_id from mine) then s.away_team else s.home_team end,
  s.home_team_id::text = (select team_id from mine),
  jsonb_build_object('match_id', s.match_id, 'season_id', s.season_id, 'status', s.status, 'source', 'bv_fixtures')
from scheduled s
union all
-- Amicaux programmés : dernière capture de la liste des amicaux (kickoff_at en UTC dans l'API).
select
  'basketvibe', (select team_id from mine), x ->> 'id', 'amical', null::int, null::int,
  ((x ->> 'kickoff_at')::timestamptz at time zone 'Europe/Paris')::date,  -- fuseau_affichage (match_day = jour de l'hôte, dans extras)
  (x ->> 'kickoff_at')::timestamptz, false,
  null::int, null::int, null::text,
  case when x ->> 'home_team_id' = (select team_id from mine) then x ->> 'away_team_name' else x ->> 'home_team_name' end,
  x ->> 'home_team_id' = (select team_id from mine),
  jsonb_build_object('status', x ->> 'status', 'match_day', x ->> 'match_day', 'has_saved_match_tactics', (x ->> 'has_saved_match_tactics')::boolean,
                     'source', 'bv_api friendlies')
from (select a.body from silver.bv_api a
      where a.endpoint ~ '^/teams/[0-9a-f-]{36}/friendlies$'
      order by a.captured_at desc limit 1) a,
     jsonb_array_elements(a.body -> 'friendlies') x
where x ->> 'status' = 'scheduled'
  and not exists (select 1 from played p where p.fixture_id::text = x ->> 'id');

-- Classement : une ligne par club et par relevé de ma ligue (relevés sans mon club écartés : autre ligue).
create or replace view adapt.basketvibe_standing with (security_invoker = true) as
with releves as (
  select distinct s.season_id, s.day from silver.bv_standings_weekly s where s.is_mine
)
select
  'basketvibe'::text           as game,
  s.team_id::text              as team_id,
  s.team                       as team_label,
  s.is_mine                    as is_mine,
  s.season_id::text            as season_id,
  s.day                        as day,
  max(s.wins + s.losses) over (partition by s.season_id, s.day) as round_no,
  s.rank                       as rank,
  s.wins + s.losses            as played,
  s.points                     as points,
  s.wins                       as wins,
  0                            as draws,  -- pas de match nul [M§2]
  s.losses                     as losses,
  s.points_for                 as gf,
  s.points_against             as ga,
  jsonb_build_object('week', s.week, 'diff', s.diff, 'home_wins', s.home_wins, 'home_losses', s.home_losses,
                     'away_wins', s.away_wins, 'away_losses', s.away_losses, 'club_strength', s.club_strength,
                     'is_human', s.is_human, 'form', s.form) as extras
from silver.bv_standings_weekly s
join releves r on r.season_id = s.season_id and r.day = s.day;

-- Finances : relevé hebdomadaire ; salaries et expenses sont des montants par semaine (extras.periode).
create or replace view adapt.basketvibe_finance_daily with (security_invoker = true) as
select
  'basketvibe'::text           as game,
  f.team_id::text              as team_id,
  f.day                        as day,
  f.balance                    as balance,
  null::numeric                as income,       -- recettes non relevées sur la page finances
  (f.weekly_salaries + f.weekly_academy + f.weekly_personnel) as expenses,
  f.weekly_salaries            as salaries,
  null::numeric                as wage_cap,     -- aucun plafond salarial dans les skills BasketVibe
  null::numeric                as capacite_invest,  -- calculée une fois dans le gold générique (plan 1.4)
  jsonb_build_object('periode', 'semaine', 'week', f.week, 'popularity', f.popularity,
                     'academy', f.weekly_academy, 'personnel', f.weekly_personnel,
                     'transfer_available', f.transfer_available, 'transfer_committed', f.transfer_committed,
                     'transfer_lock', f.transfer_lock) as extras
from silver.bv_finance_weekly f;

-- Marché : chaque annonce vue (marché ou mes ventes), dernier relevé ; le statut n'est pas remis à jour après la fin.
create or replace view adapt.basketvibe_market_listing with (security_invoker = true) as
select
  'basketvibe'::text                           as game,
  me.team_id::text                             as team_id,
  t.auction_id::text                           as listing_id,
  (t.seen_at at time zone 'Europe/Paris')::date as day,
  t.seen_at                                    as seen_at,
  t.ends_at                                    as ends_at,
  t.status                                     as status,
  t.player_id::text                            as player_id,
  t.name                                       as name,
  t.position                                   as position,
  t.age                                        as age,
  t.ps::numeric                                as rating,      -- PS 0–99 [M§2.2]
  t.current_price::numeric                     as price,
  t.starting_price::numeric                    as starting_price,
  t.bid_count                                  as bids,
  t.seller_team_id::text                       as seller_id,
  t.seller_team                                as seller_label,
  t.seller_team_id is not distinct from me.team_id as is_mine,
  jsonb_build_object(
    'two_point', t.two_point, 'three_point', t.three_point, 'defense', t.defense, 'passing', t.passing,
    'ball_handling', t.ball_handling, 'rebounding', t.rebounding, 'stamina', t.stamina, 'athleticism', t.athleticism
  )                                            as skills,
  jsonb_build_object('experience', t.experience, 'height_cm', t.height_cm, 'weight_kg', t.weight_kg,
                     'nationality', t.nationality, 'seller_is_free_agent', t.seller_is_free_agent) as extras
from silver.bv_transfer_auctions t
cross join silver.bv_my_team me;

grant select on adapt.basketvibe_player_daily, adapt.basketvibe_fixture,
                adapt.basketvibe_standing, adapt.basketvibe_finance_daily,
                adapt.basketvibe_market_listing to assistant_ro;

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
  null::timestamptz                                    as scheduled_at,  -- fuseau de kickoff_time non sourcé (« fuseau de l'hôte » pour les amicaux)
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
from scheduled s;

grant select on adapt.basketvibe_player_daily, adapt.basketvibe_fixture to assistant_ro;

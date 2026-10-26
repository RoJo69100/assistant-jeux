-- B2 (rétro 2026-10-24), brut ouvert le 2026-10-25 :
-- * la ligne « orpheline » (match 30b9bec7…, 24-25 L) n'est pas un doublon de J3 (tirs 44-51 contre 46-47) :
--   c'est un match de COUPE (présent dans /cups/current et /teams/mine/events, adversaire Pailans de Garavota, 2026-10-20).
-- * match_day venait de sz_fixtures.day = jour de capture de la page compétition (2026-10-24 partout).
-- Correctif : match_day = date Paris de l'événement match_result (/teams/mine/events), NULL si absent ;
-- opponent et venue complétés par l'événement pour la coupe ; colonnes ajoutées en fin : competition, played_at.
-- Les chiffres de ligue filtrent competition = 'league'.
create or replace view silver.sz_matches with (security_invoker = true) as
with me as (select team_id from silver.sz_my_team),
t as (
  select r.match_id, r.captured_at, r.day, (x->>'teamId')::uuid as team_id, x
  from silver.sz_match_stats_raw r, jsonb_array_elements(r.body->'teams') x
),
ev as (
  select distinct on (e->'data'->>'matchId')
         (e->'data'->>'matchId')::uuid as match_id, (e->>'at')::timestamptz as played_at,
         (e->'data'->>'home')::boolean as home, e->'data'->>'opponentName' as opponent
  from silver.sz_api a, jsonb_array_elements(a.body) e
  where a.endpoint = '/teams/mine/events' and e->>'type' = 'match_result'
  order by e->'data'->>'matchId', a.captured_at desc
),
cup as (
  select distinct (tie->>'matchId')::uuid as match_id
  from silver.sz_api a, jsonb_array_elements(a.body->'rounds') r, jsonb_array_elements(r->'ties') tie
  where a.endpoint = '/cups/current' and tie->>'matchId' is not null
)
select mine.match_id, mine.captured_at, mine.day as captured_day,
       (ev.played_at at time zone 'Europe/Paris')::date as match_day, f.round,
       case when f.home_team_id = me.team_id then 'home' when f.away_team_id = me.team_id then 'away'
            when ev.home then 'home' when not ev.home then 'away' end as venue,
       coalesce(case when f.home_team_id = me.team_id then f.away_team else f.home_team end, ev.opponent) as opponent,
       case when f.home_team_id = me.team_id then f.away_is_bot else f.home_is_bot end as opponent_is_bot,
       (mine.x->>'goals')::int as goals, (opp.x->>'goals')::int as opp_goals,
       case when (mine.x->>'goals')::int > (opp.x->>'goals')::int then 'W'
            when (mine.x->>'goals')::int < (opp.x->>'goals')::int then 'L' else 'D' end as result,
       (mine.x->>'shots')::int as shots, (opp.x->>'shots')::int as opp_shots,
       (mine.x->>'shotsOnTarget')::int as shots_on_target, (opp.x->>'shotsOnTarget')::int as opp_shots_on_target,
       round(100.0 * (mine.x->>'goals')::int / nullif((mine.x->>'shots')::int, 0), 1) as shot_pct,
       round(100.0 * (opp.x->>'goals')::int / nullif((opp.x->>'shots')::int, 0), 1) as opp_shot_pct,
       (mine.x->>'saves')::int as saves, (opp.x->>'saves')::int as opp_saves,
       round(100.0 * (mine.x->>'saves')::int / nullif((opp.x->>'shotsOnTarget')::int, 0), 1) as save_pct,
       round(100.0 * (opp.x->>'saves')::int / nullif((mine.x->>'shotsOnTarget')::int, 0), 1) as opp_save_pct,
       (mine.x->>'turnovers')::int as turnovers, (opp.x->>'turnovers')::int as opp_turnovers,
       (mine.x->>'steals')::int as steals, (opp.x->>'steals')::int as opp_steals,
       (mine.x->>'blocks')::int as blocks, (opp.x->>'blocks')::int as opp_blocks,
       (mine.x->>'exclusions')::int as exclusions, (opp.x->>'exclusions')::int as opp_exclusions,
       (mine.x->>'yellowCards')::int as yellow_cards, (opp.x->>'yellowCards')::int as opp_yellow_cards,
       (mine.x->>'redCards')::int as red_cards, (opp.x->>'redCards')::int as opp_red_cards,
       (mine.x->>'sevenMeterGoals')::int as seven_m_goals, (mine.x->>'sevenMeterShots')::int as seven_m_shots,
       (opp.x->>'sevenMeterGoals')::int as opp_seven_m_goals, (opp.x->>'sevenMeterShots')::int as opp_seven_m_shots,
       (mine.x->>'possessionSeconds')::int as possession_s, (opp.x->>'possessionSeconds')::int as opp_possession_s,
       case when f.match_id is not null then 'league' when cup.match_id is not null then 'cup' end as competition,
       ev.played_at
from t mine
cross join me
join t opp on opp.match_id = mine.match_id and opp.team_id <> mine.team_id
left join silver.sz_fixtures f on f.match_id = mine.match_id
left join ev on ev.match_id = mine.match_id
left join cup on cup.match_id = mine.match_id
where mine.team_id = me.team_id;

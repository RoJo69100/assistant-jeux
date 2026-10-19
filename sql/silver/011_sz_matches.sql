-- Silver SixZero League : matchs (endpoint /matches/<id>/stats, capturé en ouvrant la page du match).
-- Une ligne par match pour mon équipe, stats par joueur, incidents (buts, exclusions 2 min, cartons, mi-temps).
-- playerId de l'API = '<teamId>-<playerId>' : on garde les 36 derniers caractères pour joindre silver.sz_players.

create or replace view silver.sz_match_stats_raw with (security_invoker = true) as
select distinct on (m.match_id)
       m.match_id, a.captured_at, a.day, a.body
from silver.sz_api a,
     lateral (select substring(a.endpoint from '^/matches/([0-9a-f-]{36})/stats$')::uuid as match_id) m
where a.endpoint ~ '^/matches/[0-9a-f-]{36}/stats$'
order by m.match_id, a.captured_at desc;

-- Un match par ligne, vu de mon équipe : stats d'équipe des deux côtés et contexte du calendrier (sz_fixtures).
create or replace view silver.sz_matches with (security_invoker = true) as
with me as (select team_id from silver.sz_my_team),
t as (
  select r.match_id, r.captured_at, r.day, (x->>'teamId')::uuid as team_id, x
  from silver.sz_match_stats_raw r, jsonb_array_elements(r.body->'teams') x
)
select mine.match_id, mine.captured_at, mine.day as captured_day,
       f.day as match_day, f.round,
       case when f.home_team_id = me.team_id then 'home' when f.away_team_id = me.team_id then 'away' end as venue,
       case when f.home_team_id = me.team_id then f.away_team else f.home_team end as opponent,
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
       (mine.x->>'possessionSeconds')::int as possession_s, (opp.x->>'possessionSeconds')::int as opp_possession_s
from t mine
cross join me
join t opp on opp.match_id = mine.match_id and opp.team_id <> mine.team_id
left join silver.sz_fixtures f on f.match_id = mine.match_id
where mine.team_id = me.team_id;

-- Stats par joueur (les deux équipes ; is_mine pour filtrer).
create or replace view silver.sz_match_players with (security_invoker = true) as
select r.match_id, r.day as captured_day,
       (p->>'teamId')::uuid as team_id, (p->>'teamId')::uuid = (select team_id from silver.sz_my_team) as is_mine,
       right(p->>'playerId', 36)::uuid as player_id, p->>'name' as name, p->>'role' as role, (p->>'number')::int as number,
       (p->>'goals')::int as goals, (p->>'shots')::int as shots,
       round(100.0 * (p->>'goals')::int / nullif((p->>'shots')::int, 0), 1) as shot_pct,
       (p->>'sevenMeterGoals')::int as seven_m_goals, (p->>'sevenMeterShots')::int as seven_m_shots,
       (p->>'saves')::int as saves, (p->>'goalsConceded')::int as goals_conceded,
       round(100.0 * (p->>'saves')::int / nullif((p->>'saves')::int + (p->>'goalsConceded')::int, 0), 1) as save_pct,
       (p->>'steals')::int as steals, (p->>'blocks')::int as blocks, (p->>'technicalFouls')::int as technical_fouls,
       (p->>'exclusions')::int as exclusions, (p->>'yellowCards')::int as yellow_cards, (p->>'redCards')::int as red_cards
from silver.sz_match_stats_raw r, jsonb_array_elements(r.body->'players') p;

-- Incidents dans l'ordre du match (clock_s en secondes depuis le coup d'envoi).
create or replace view silver.sz_match_incidents with (security_invoker = true) as
select r.match_id, (i.ord)::int as seq, (i.v->>'clockSeconds')::int as clock_s,
       i.v->>'kind' as kind, i.v->>'detail' as detail,
       (i.v->>'teamId')::uuid as team_id, (i.v->>'teamId')::uuid = (select team_id from silver.sz_my_team) as is_mine,
       right(i.v->>'playerId', 36)::uuid as player_id, i.v->>'playerName' as player_name,
       (i.v->>'homeScore')::int as home_score, (i.v->>'awayScore')::int as away_score
from silver.sz_match_stats_raw r, jsonb_array_elements(r.body->'incidents') with ordinality as i(v, ord);

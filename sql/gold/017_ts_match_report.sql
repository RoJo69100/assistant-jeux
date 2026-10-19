-- Gold Team Soccer : rapport de match (agent Match), à partir des vues silver ts_match_events / _ratings / _sectors.
-- Tout est orienté « moi » contre « adversaire ». Règles : skill teamsoccer-match (duels, secteurs), teamsoccer-joueurs (notes).

-- Une ligne par action (play_id) : qui attaquait, jusqu'où elle est allée et comment elle s'est terminée.
create or replace view gold.ts_match_plays with (security_invoker = true) as
select e.match_id, e.play_id, bool_or(e.is_mine) as is_mine, min(e.minute) as minute, max(e.phase_total) as phases,
       bool_or(e.type = 'play_resolution') as shot, bool_or(e.is_goal) as goal,
       bool_or(e.type = 'save') as saved, bool_or(e.type = 'shot_blocked') as blocked,
       bool_or(e.type in ('shot_wide', 'shot_post')) as off_target, bool_or(e.type = 'shot_post') as post,
       bool_or(e.type = 'penalty') as penalty, bool_or(e.type = 'corner') as corner,
       bool_or(e.type = 'header') as header, bool_or(e.type in ('cross', 'cross_cleared')) as cross_play,
       (array_agg(e.type order by e.seq desc))[1] as outcome,
       (array_agg(e.actor order by e.seq desc))[1] as last_actor
from silver.ts_match_events e
where e.play_id is not null
group by e.match_id, e.play_id;

-- Rapport par match : score, affluence, actions, tirs, efficacité, ballons perdus, cartons, notes moyennes
-- (notes et secteurs dépendent de la composition, pas du déroulé : voir silver.ts_match_ratings),
-- secteurs (moyenne des 7 zones de champ, gardien à part, zone la plus faible), composition enregistrée.
create or replace view gold.ts_match_report with (security_invoker = true) as
with p as (
  select match_id,
         count(*) filter (where is_mine) as my_attacks, count(*) filter (where not is_mine) as opp_attacks,
         count(*) filter (where is_mine and shot) as my_shots, count(*) filter (where not is_mine and shot) as opp_shots,
         count(*) filter (where is_mine and (goal or saved)) as my_on_target, count(*) filter (where not is_mine and (goal or saved)) as opp_on_target,
         count(*) filter (where is_mine and penalty) as my_penalties, count(*) filter (where not is_mine and penalty) as opp_penalties,
         count(*) filter (where is_mine and header) as my_headers,
         count(*) filter (where is_mine and outcome like 'play_lost%') as my_lost,
         count(*) filter (where is_mine and outcome = 'play_lost_intercept') as my_lost_intercept,
         count(*) filter (where is_mine and outcome = 'play_lost_badcontrol') as my_lost_badcontrol,
         count(*) filter (where is_mine and outcome = 'play_lost_outofbounds') as my_lost_outofbounds,
         count(*) filter (where is_mine and post) as my_posts
  from gold.ts_match_plays group by match_id
), ev as (
  select match_id, max(engine_version) as engine_version,
         max((attendance->>'spectators')::int) as spectators, max((attendance->>'fillPercent')::int) as fill_pct,
         max(attendance->>'stadiumName') as stadium,
         count(*) filter (where type = 'yellow_card' and is_mine) as my_yellows, count(*) filter (where type = 'red_card' and is_mine) as my_reds,
         count(*) filter (where type = 'foul' and is_mine) as my_fouls, count(*) filter (where type = 'substitution' and is_mine) as my_subs,
         max(jsonb_array_length(summary->'injuries')) as injuries, (array_agg(summary) filter (where summary is not null))[1] as summary,
         string_agg(case when is_goal then minute || '′ ' || coalesce(actor, '?') || case when is_mine then '' else ' (adv.)' end end, ', ' order by seq) as goals_detail
  from silver.ts_match_events group by match_id
), r as (
  select rt.match_id,
         round(avg(rt.rating) filter (where (rt.side = 'home') = (m.venue = 'domicile')), 2) as my_avg_rating,
         round(avg(rt.rating) filter (where (rt.side = 'home') <> (m.venue = 'domicile')), 2) as opp_avg_rating,
         (array_agg(rt.player || ' ' || rt.rating order by rt.rating desc) filter (where (rt.side = 'home') = (m.venue = 'domicile')))[1] as my_best,
         (array_agg(rt.player || ' (' || rt.pos || ') ' || rt.rating order by rt.rating) filter (where (rt.side = 'home') = (m.venue = 'domicile')))[1] as my_worst
  from silver.ts_match_ratings rt join silver.ts_matches m on m.match_id = rt.match_id
  group by rt.match_id
), s as (
  select sc.match_id,
         round(avg(case when m.venue = 'domicile' then sc.home_value else sc.away_value end) filter (where sc.zone_order between 1 and 7), 1) as my_sector_avg,
         round(avg(case when m.venue = 'domicile' then sc.away_value else sc.home_value end) filter (where sc.zone_order between 1 and 7), 1) as opp_sector_avg,
         max(case when m.venue = 'domicile' then sc.home_value else sc.away_value end) filter (where sc.zone_order in (0, 8)) as my_gk_sector,
         max(case when m.venue = 'domicile' then sc.away_value else sc.home_value end) filter (where sc.zone_order in (0, 8)) as opp_gk_sector,
         (array_agg(case when m.venue = 'domicile' or sc.zone not like '% / %' then split_part(sc.zone, ' / ', 1) else split_part(sc.zone, ' / ', 2) end
                    || ' ' || case when m.venue = 'domicile' then sc.home_value - sc.away_value else sc.away_value - sc.home_value end
                    order by case when m.venue = 'domicile' then sc.home_value - sc.away_value else sc.away_value - sc.home_value end)
            filter (where sc.zone_order between 1 and 7))[1] as my_weakest_zone
  from silver.ts_match_sectors sc join silver.ts_matches m on m.match_id = sc.match_id
  group by sc.match_id
)
select m.match_id, m.my_team_id, mt.name as my_team, m.match_date_paris, m.competition, m.venue,
       case when m.venue = 'domicile' then m.away_team else m.home_team end as opponent,
       coalesce(ot.is_bot, false) or (case when m.venue = 'domicile' then m.away_team else m.home_team end) = 'BOT' as opp_is_bot,
       case when m.venue = 'domicile' then m.home_score else m.away_score end as goals_for,
       case when m.venue = 'domicile' then m.away_score else m.home_score end as goals_against,
       case when m.home_score = m.away_score then 'N'
            when (m.home_score > m.away_score) = (m.venue = 'domicile') then 'V' else 'D' end as result,
       ev.goals_detail, ml.formation, ml.play_style,
       p.my_attacks, p.opp_attacks, p.my_shots, p.opp_shots, p.my_on_target, p.opp_on_target,
       round(100.0 * (case when m.venue = 'domicile' then m.home_score else m.away_score end) / nullif(p.my_shots, 0), 0) as my_conversion_pct,
       p.my_penalties, p.opp_penalties, p.my_headers, p.my_posts,
       p.my_lost, p.my_lost_intercept, p.my_lost_badcontrol, p.my_lost_outofbounds,
       ev.my_yellows, ev.my_reds, ev.my_fouls, ev.my_subs, ev.injuries,
       r.my_avg_rating, r.opp_avg_rating, r.my_best, r.my_worst,
       s.my_sector_avg, s.opp_sector_avg, s.my_gk_sector, s.opp_gk_sector, s.my_weakest_zone,
       ev.stadium, ev.spectators, ev.fill_pct, ev.engine_version
from silver.ts_matches m
join ev on ev.match_id = m.match_id
left join silver.ts_my_teams mt on mt.team_id = m.my_team_id
left join silver.ts_teams ot on ot.team_id = case when m.venue = 'domicile' then m.away_team_id else m.home_team_id end
left join p on p.match_id = m.match_id
left join r on r.match_id = m.match_id
left join s on s.match_id = m.match_id
left join silver.ts_match_lineups ml on ml.match_id = m.match_id and ml.team_id = m.my_team_id
where m.my_team_id is not null;

-- Mes joueuses et joueurs sur les matchs analysés : notes (moyenne, mini, maxi, tendance 1re → 2e mi-temps),
-- buts, implication dans les actions, ballons perdus en fin d'action. Clé : club + nom affiché.
create or replace view gold.ts_player_match_ratings with (security_invoker = true) as
with rt as (
  select rt.*, m.match_date_paris
  from silver.ts_match_ratings rt join silver.ts_matches m on m.match_id = rt.match_id
  where (rt.side = 'home') = (m.venue = 'domicile')
), ev as (
  select e.match_id, e.actor as player,
         count(*) filter (where e.is_goal) as goals,
         count(*) as involvements,
         count(*) filter (where e.type like 'play_lost%') as balls_lost
  from silver.ts_match_events e where e.is_mine and e.actor is not null
  group by e.match_id, e.actor
)
select rt.my_team_id as team_id, rt.player,
       string_agg(distinct rt.pos, '/') as positions, count(*) as matches,
       sum(coalesce(rt.min_out, 90) - coalesce(rt.min_in, 1) + 1) as minutes,
       round(avg(rt.rating), 2) as avg_rating, min(rt.rating) as min_rating, max(rt.rating) as max_rating,
       round(avg(rt.rating_h2 - rt.rating_h1), 2) as avg_h2_minus_h1,
       (array_agg(rt.rating order by rt.match_date_paris desc))[1] as last_rating,
       coalesce(sum(ev.goals), 0) as goals, coalesce(sum(ev.involvements), 0) as involvements,
       coalesce(sum(ev.balls_lost), 0) as balls_lost
from rt left join ev on ev.match_id = rt.match_id and ev.player = rt.player
group by rt.my_team_id, rt.player;

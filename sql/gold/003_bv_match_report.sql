-- Gold BasketVibe : rapport de match pour l'agent Match.
-- Une ligne par match joué (ligue et amicaux, colonne competition), les « quatre facteurs » moi vs adversaire,
-- les écarts par quart-temps, puis le détail par joueur et le focus défensif sur l'adversaire.
-- Possessions estimées : FGA − OREB + TOV + 0,44 × FTA (formule classique du basket, pas une règle du jeu).

create or replace view gold.bv_match_report with (security_invoker = true) as
with t as (
  select t.*, m.round_number, m.home_team, m.away_team, m.my_side, m.home_score, m.away_score,
         m.quarter_scores, m.overtime_periods
  from gold.bv_match_team_totals t
  join silver.bv_matches m using (fixture_id)
),
p as (
  select me.fixture_id, me.competition, me.match_day, me.round_number, me.my_result,
         case me.my_side when 'home' then me.away_team else me.home_team end as opponent,
         me.my_side as venue,
         me.quarter_scores, me.overtime_periods,
         me.pts as my_pts, coalesce(op.pts, case me.my_side when 'home' then me.away_score else me.home_score end) as opp_pts,
         me.fga + 0.44 * me.fta - me.oreb + me.tov as my_poss,
         op.fga + 0.44 * op.fta - op.oreb + op.tov as opp_poss,
         me.fgm, me.fga, me.fg3m, me.fg3a, me.ftm, me.fta, me.oreb, me.dreb, me.ast, me.tov, me.stl, me.blk, me.pf,
         op.fgm o_fgm, op.fga o_fga, op.fg3m o_fg3m, op.fg3a o_fg3a, op.ftm o_ftm, op.fta o_fta,
         op.oreb o_oreb, op.dreb o_dreb, op.ast o_ast, op.tov o_tov, op.stl o_stl, op.blk o_blk, op.pf o_pf
  from t me left join t op on op.fixture_id = me.fixture_id and op.is_mine = false  -- box score adverse parfois absent de l'API (amical du 2026-10-13)
  where me.is_mine
)
select p.fixture_id, p.competition, p.match_day, p.round_number, p.opponent, p.venue, p.my_result,
       p.my_pts, p.opp_pts, p.my_pts - p.opp_pts as margin,
       -- écart par quart-temps (positif = quart-temps gagné)
       (select array_agg(case p.venue when 'home' then (q->>'home_points')::int - (q->>'away_points')::int
                                      else (q->>'away_points')::int - (q->>'home_points')::int end
                         order by (q->>'period')::int)
        from jsonb_array_elements(p.quarter_scores) q)                         as quarter_margins,
       p.overtime_periods,
       round((p.my_poss + p.opp_poss) / 2, 1)                                  as pace,
       round(100 * p.my_pts / nullif(p.my_poss, 0), 1)                         as off_rtg,
       round(100 * p.opp_pts / nullif(p.opp_poss, 0), 1)                       as def_rtg,
       -- quatre facteurs (moi / adversaire)
       round(100.0 * (p.fgm + 0.5 * p.fg3m) / nullif(p.fga, 0), 1)             as efg_pct,
       round(100.0 * (p.o_fgm + 0.5 * p.o_fg3m) / nullif(p.o_fga, 0), 1)       as opp_efg_pct,
       round(100.0 * p.tov / nullif(p.my_poss, 0), 1)                          as tov_pct,
       round(100.0 * p.o_tov / nullif(p.opp_poss, 0), 1)                       as opp_tov_pct,
       round(100.0 * p.oreb / nullif(p.oreb + p.o_dreb, 0), 1)                 as oreb_pct,
       round(100.0 * p.o_oreb / nullif(p.o_oreb + p.dreb, 0), 1)               as opp_oreb_pct,
       round(100.0 * p.fta / nullif(p.fga, 0), 1)                              as ft_rate,
       round(100.0 * p.o_fta / nullif(p.o_fga, 0), 1)                          as opp_ft_rate,
       -- détail des tirs
       round(100.0 * (p.fgm - p.fg3m) / nullif(p.fga - p.fg3a, 0), 1)          as fg2_pct,
       round(100.0 * (p.o_fgm - p.o_fg3m) / nullif(p.o_fga - p.o_fg3a, 0), 1)  as opp_fg2_pct,
       round(100.0 * p.fg3m / nullif(p.fg3a, 0), 1)                            as fg3_pct,
       round(100.0 * p.o_fg3m / nullif(p.o_fg3a, 0), 1)                        as opp_fg3_pct,
       round(100.0 * p.fg3a / nullif(p.fga, 0), 1)                             as fg3a_share,
       round(100.0 * p.o_fg3a / nullif(p.o_fga, 0), 1)                         as opp_fg3a_share,
       round(100.0 * p.ftm / nullif(p.fta, 0), 1)                              as ft_pct,
       p.fga, p.o_fga, p.fta, p.o_fta, p.oreb, p.o_oreb, p.dreb, p.o_dreb,
       p.ast, p.o_ast, p.tov, p.o_tov, p.stl, p.o_stl, p.blk, p.o_blk, p.pf, p.o_pf
from p;

-- Ce qui sépare victoires et défaites : moyennes des facteurs par compétition et résultat.
create or replace view gold.bv_match_factors_by_result with (security_invoker = true) as
select competition, my_result, count(*) as matches,
       round(avg(margin), 1) margin, round(avg(pace), 1) pace,
       round(avg(off_rtg), 1) off_rtg, round(avg(def_rtg), 1) def_rtg,
       round(avg(efg_pct), 1) efg_pct, round(avg(opp_efg_pct), 1) opp_efg_pct,
       round(avg(tov_pct), 1) tov_pct, round(avg(opp_tov_pct), 1) opp_tov_pct,
       round(avg(oreb_pct), 1) oreb_pct, round(avg(opp_oreb_pct), 1) opp_oreb_pct,
       round(avg(ft_rate), 1) ft_rate, round(avg(opp_ft_rate), 1) opp_ft_rate,
       round(avg(fg3a_share), 1) fg3a_share, round(avg(opp_fg3a_share), 1) opp_fg3a_share,
       round(avg(fg3_pct), 1) fg3_pct, round(avg(opp_fg3_pct), 1) opp_fg3_pct
from gold.bv_match_report
group by competition, my_result
order by competition desc, my_result desc;

-- Mes joueurs, match par match : minutes, quarts-temps joués, stats, consignes jouées.
-- Les crans de consigne (0–4) sont ceux de l'API : defense_tier suit l'échelle du manuel (0 soft, 2 équilibrée, 4 agressive) [M§6.3] ;
-- le sens de role_tier / shot_tier / offensive_focus_tier (0 = passeur / 2 pts / Low ?) reste à confirmer dans le jeu.
create or replace view gold.bv_match_player_lines with (security_invoker = true) as
with quarters as (
  select fixture_id, player_id,
         array_agg(period order by period) filter (where min > 0) as periods_played
  from silver.bv_match_player_stats
  where period > 0
  group by fixture_id, player_id
),
directives as (
  select t.fixture_id, (d->>'player_id')::uuid as player_id,
         (d->>'role_tier')::int as role_tier, (d->>'shot_tier')::int as shot_tier,
         (d->>'offensive_focus_tier')::int as offensive_focus_tier, (d->>'defense_tier')::int as defense_tier
  from silver.bv_match_tactics t
  join silver.bv_my_team me on me.team_id = t.team_id
  cross join lateral jsonb_array_elements(t.player_directives) d
)
select m.fixture_id, m.competition, m.match_day, m.round_number,
       s.player_id, s.name, s.position,
       s.min, q.periods_played, s.min > 36 as over_36,
       s.pts, s.fgm, s.fga, s.fg3m, s.fg3a, s.ftm, s.fta, s.oreb, s.dreb, s.reb, s.ast, s.stl, s.blk, s.tov, s.pf,
       s.pf >= 6 as fouled_out, s.plus_minus, s.eval,
       round(s.eval / nullif(s.min, 0), 2) as eval_per_min,
       d.role_tier, d.shot_tier, d.offensive_focus_tier, d.defense_tier
from silver.bv_matches m
join silver.bv_match_player_stats s on s.fixture_id = m.fixture_id and s.period = 0 and s.is_mine
left join quarters q on q.fixture_id = s.fixture_id and q.player_id = s.player_id
left join directives d on d.fixture_id = s.fixture_id and d.player_id = s.player_id;

-- Adversaires, match par match : production de chaque joueur adverse et notre focus défensif sur lui [M§6.6].
create or replace view gold.bv_match_opp_focus with (security_invoker = true) as
with focus as (
  select t.fixture_id, (f->>'opponent_player_id')::uuid as player_id, f->>'focus' as our_focus
  from silver.bv_match_tactics t
  join silver.bv_my_team me on me.team_id = t.team_id
  cross join lateral jsonb_array_elements(t.defensive_focus) f
)
select m.fixture_id, m.competition, m.match_day, m.round_number,
       s.team as opponent, s.player_id, s.name, s.position,
       s.min, s.pts, s.fga, s.fg3a, s.fta,
       round(100.0 * s.fgm / nullif(s.fga, 0), 1) as fg_pct,
       s.ast, s.reb, s.eval,
       round(100.0 * s.fga / nullif(sum(s.fga) over (partition by m.fixture_id), 0), 1) as shot_share,
       coalesce(f.our_focus, 'normal (pas de plan)') as our_focus
from silver.bv_matches m
join silver.bv_match_player_stats s on s.fixture_id = m.fixture_id and s.period = 0 and s.is_mine = false
left join focus f on f.fixture_id = s.fixture_id and f.player_id = s.player_id;

-- BasketVibe : meilleurs joueurs adverses de la ligue, à partir des matchs que nous avons joués contre eux
-- (registre de couverture docs/couverture/basketvibe.md, ligne 7 « analyser les stats de la ligue »).
-- period 0 = total du match. Seuls les adversaires de nos matchs sont connus (chaque club de la ligue 2 fois par saison).
create or replace view gold.bv_league_top_players as
select m.season_id,
       m.competition,
       s.team,
       s.player_id,
       s.name,
       s.position,
       count(*)                                         as matches,
       round(avg(s.min), 1)                             as min_per_game,
       round(avg(s.pts), 1)                             as pts_per_game,
       round(avg(s.reb), 1)                             as reb_per_game,
       round(avg(s.ast), 1)                             as ast_per_game,
       round(avg(s.eval), 1)                            as eval_per_game,
       round(100.0 * sum(s.fgm) / nullif(sum(s.fga), 0), 1)   as fg_pct,
       round(100.0 * sum(s.fg3m) / nullif(sum(s.fg3a), 0), 1) as fg3_pct,
       round(100.0 * sum(s.fg3a) / nullif(sum(s.fga), 0), 1)  as fg3a_share,
       rank() over (partition by m.season_id, m.competition order by avg(s.eval) desc) as rank_eval
from silver.bv_match_player_stats s
join silver.bv_matches m on m.fixture_id = s.fixture_id
where s.period = 0 and not s.is_mine and s.min > 0
group by m.season_id, m.competition, s.team, s.player_id, s.name, s.position;

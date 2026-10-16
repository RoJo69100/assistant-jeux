-- Silver BasketVibe : ajoute l'équipe de chaque ligne du box score.
-- Les deux équipes sont gardées (tendances concédées, analyse de l'adversaire) ; filtrer avec is_mine.
create or replace view silver.bv_match_player_stats with (security_invoker = true) as
with src as (
  select distinct on (f.fixture_id, period)
         f.fixture_id, f.body,
         case when f.part = 'preview' then 0
              else (substring(f.query from 'period=(\d+)'))::int end as period
  from silver.bv_fixture_api f
  where f.part = 'preview' or (f.part = 'period-box' and f.query ~ 'period=\d+')
  order by f.fixture_id, period, f.captured_at desc
)
select s.fixture_id,
       s.period,
       (p->>'player_id')::uuid               as player_id,
       p->>'first_name' || ' ' || (p->>'last_name') as name,
       p->>'team_side'                       as team_side,
       p->>'position'                        as position,
       (p->>'min')::numeric                  as min,
       (p->>'pts')::int  as pts,
       (p->>'fgm')::int  as fgm,  (p->>'fga')::int  as fga,
       (p->>'fg3m')::int as fg3m, (p->>'fg3a')::int as fg3a,
       (p->>'ftm')::int  as ftm,  (p->>'fta')::int  as fta,
       (p->>'oreb')::int as oreb, (p->>'dreb')::int as dreb,
       (p->>'oreb')::int + (p->>'dreb')::int as reb,
       (p->>'ast')::int  as ast,  (p->>'stl')::int  as stl,
       (p->>'blk')::int  as blk,  (p->>'tov')::int  as tov,
       (p->>'pf')::int   as pf,
       (p->>'plus_minus')::int               as plus_minus,
       (p->>'eval')::numeric                 as eval,
       case p->>'team_side' when 'home' then m.home_team_id when 'away' then m.away_team_id end as team_id,
       case p->>'team_side' when 'home' then m.home_team    when 'away' then m.away_team    end as team,
       p->>'team_side' = m.my_side           as is_mine
from src s
cross join lateral jsonb_array_elements(s.body->'players') p
left join silver.bv_matches m on m.fixture_id = s.fixture_id;

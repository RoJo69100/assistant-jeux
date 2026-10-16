-- Gold BasketVibe : vues d'analyse, calculées en SQL à partir de silver. Mon équipe = silver.bv_my_team.

create schema if not exists gold;
revoke all on schema gold from public, anon, authenticated;

-- ---------- Bilan par poste ----------
-- Dernier relevé hebdo de mon effectif + dernier salaire connu.
create or replace view gold.bv_position_summary with (security_invoker = true) as
with roster as (
  select w.*
  from silver.bv_player_weekly w
  join silver.bv_my_team m on m.team_id::text = w.team_id
  where w.week = (select max(week) from silver.bv_player_weekly w2 where w2.team_id = w.team_id)
),
sal as (
  select distinct on (player_id) player_id, salary
  from silver.bv_player_salary_weekly
  order by player_id, week desc
)
select r.position,
       count(*)                                         as depth,
       round(avg(r.ps), 1)                              as ps_avg,
       max(r.ps)                                        as ps_max,
       (array_agg(r.name order by r.ps desc))[1]        as best,
       (array_agg(r.name order by r.ps asc))[1]         as weakest,
       round(avg(r.age), 1)                             as age_avg,
       min(r.age)                                       as age_min,
       max(r.age)                                       as age_max,
       sum(s.salary)                                    as salary_total,
       round(sum(s.salary) / nullif(sum(r.ps), 0))      as salary_per_ps,
       count(*) filter (where r.injury_return_on is not null) as injured,
       max(r.week)                                      as week
from roster r
left join sal s using (player_id)
group by r.position
order by array_position(array['PG','SG','SF','PF','C'], r.position);

-- ---------- Tendances de match ----------
-- Totaux d'équipe par match (moi et adversaire), puis moyennes sur les 5 et 10 derniers matchs analysés.
create or replace view gold.bv_match_team_totals with (security_invoker = true) as
select m.fixture_id, m.match_day, m.my_result,
       s.is_mine,
       sum(s.pts) pts, sum(s.fgm) fgm, sum(s.fga) fga, sum(s.fg3m) fg3m, sum(s.fg3a) fg3a,
       sum(s.ftm) ftm, sum(s.fta) fta, sum(s.oreb) oreb, sum(s.dreb) dreb, sum(s.reb) reb,
       sum(s.ast) ast, sum(s.tov) tov, sum(s.stl) stl, sum(s.blk) blk, sum(s.pf) pf
from silver.bv_matches m
join silver.bv_match_player_stats s using (fixture_id)
where s.period = 0 and m.my_side is not null and m.status = 'finished'
group by m.fixture_id, m.match_day, m.my_result, s.is_mine;

create or replace view gold.bv_match_trends with (security_invoker = true) as
with ranked as (
  select t.*, dense_rank() over (order by t.match_day desc, t.fixture_id) as recency
  from gold.bv_match_team_totals t
),
w as (select unnest(array[5, 10]) as last_n)
select w.last_n,
       count(distinct r.fixture_id)                                         as matches,
       count(distinct r.fixture_id) filter (where r.my_result = 'W')         as wins,
       case when r.is_mine then 'moi' else 'adversaires' end                as side,
       round(avg(r.pts), 1) pts,
       round(100.0 * sum(r.fgm) / nullif(sum(r.fga), 0), 1)                 as fg_pct,
       round(avg(r.fg3a), 1) fg3a,
       round(100.0 * sum(r.fg3m) / nullif(sum(r.fg3a), 0), 1)               as fg3_pct,
       round(avg(r.fta), 1) fta,
       round(100.0 * sum(r.ftm) / nullif(sum(r.fta), 0), 1)                 as ft_pct,
       round(avg(r.oreb), 1) oreb, round(avg(r.dreb), 1) dreb, round(avg(r.reb), 1) reb,
       round(avg(r.ast), 1) ast, round(avg(r.tov), 1) tov,
       round(avg(r.stl), 1) stl, round(avg(r.blk), 1) blk, round(avg(r.pf), 1) pf
from w
join ranked r on r.recency <= w.last_n
group by w.last_n, r.is_mine
order by w.last_n, r.is_mine desc;

-- ---------- Progression hebdo des skills ----------
-- Une ligne par joueur et par entraînement (dimanche), points gagnés par skill.
create or replace view gold.bv_skill_progress_weekly with (security_invoker = true) as
select c.run_day,
       c.player_id,
       c.name,
       max(c.age)                                                            as age,
       coalesce(sum(c.delta) filter (where c.skill = 'two_point'), 0)        as two_point,
       coalesce(sum(c.delta) filter (where c.skill = 'three_point'), 0)      as three_point,
       coalesce(sum(c.delta) filter (where c.skill = 'defense'), 0)          as defense,
       coalesce(sum(c.delta) filter (where c.skill = 'passing'), 0)          as passing,
       coalesce(sum(c.delta) filter (where c.skill = 'ball_handling'), 0)    as ball_handling,
       coalesce(sum(c.delta) filter (where c.skill = 'rebounding'), 0)       as rebounding,
       coalesce(sum(c.delta) filter (where c.skill = 'stamina'), 0)          as stamina,
       coalesce(sum(c.delta) filter (where c.skill = 'athleticism'), 0)      as athleticism,
       coalesce(sum(c.delta) filter (where c.skill <> 'form'), 0)            as total_skills,
       sum(c.delta) filter (where c.skill = 'form')                          as form_change
from silver.bv_training_changes c
group by c.run_day, c.player_id, c.name;

-- ---------- Finances ----------
-- Résultat par semaine (lundi → dimanche) à partir des transactions.
-- complete = la semaine est entièrement couverte par les transactions capturées
-- (le jeu n'en montre que 20 à la fois : exporter Finances au moins une fois par semaine).
create or replace view gold.bv_finance_weekly_result with (security_invoker = true) as
with tx as (
  select t.*, date_trunc('week', t.game_day)::date as week
  from silver.bv_finance_transactions t
  join silver.bv_my_team m on m.team_id::text = t.team_id
),
cover as (select min(created_at) as oldest from tx)
select tx.week,
       sum(tx.amount) filter (where tx.amount > 0)  as income,
       sum(tx.amount) filter (where tx.amount < 0)  as expenses,
       sum(tx.amount)                               as result,
       (select oldest from cover) < tx.week::timestamptz and tx.week + 7 <= current_date as complete
from tx
group by tx.week
order by tx.week;

-- Projection de fin de saison : solde actuel
--   + recettes billetterie restantes (moyenne par match de ligue à domicile × matchs à domicile restants)
--   + sponsor garanti restant
--   − charges hebdo (salaires + personnel + académie) × dimanches restants jusqu'à la fin de saison.
-- Non inclus : amicaux, coupes, transferts, primes (imprévisibles).
create or replace view gold.bv_finance_projection with (security_invoker = true) as
with me as (select team_id from silver.bv_my_team),
fx as (
  select count(*) filter (where f.status = 'finished' and f.home_team_id = me.team_id) as home_played,
         count(*) filter (where f.status <> 'finished' and f.home_team_id = me.team_id) as home_left,
         max(f.match_day)                                                             as season_end
  from silver.bv_fixtures f, me
  where f.is_mine
),
fin as (
  select w.* from silver.bv_finance_weekly w, me
  where w.team_id = me.team_id::text
  order by w.day desc limit 1
),
season as (
  select s.* from silver.bv_finance_seasons s, me
  where s.team_id = me.team_id::text and s.is_current
),
sponsor as (
  select s.remaining_guaranteed from silver.bv_sponsor_weekly s, me
  where s.team_id = me.team_id::text
  order by s.week desc limit 1
),
paydays as (
  select count(*) as n
  from fx, generate_series(current_date + 1, fx.season_end, interval '1 day') d
  where extract(isodow from d) = 7
)
select fin.day                                                     as as_of,
       fin.balance                                                 as balance_now,
       season.season_balance                                       as season_result_so_far,
       fx.home_played, fx.home_left, fx.season_end,
       paydays.n                                                   as paydays_left,
       round(season.league_tickets / nullif(fx.home_played, 0))    as ticket_per_home_game,
       round(season.league_tickets / nullif(fx.home_played, 0) * fx.home_left) as tickets_left,
       coalesce(sponsor.remaining_guaranteed, 0)                   as sponsor_left,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) as weekly_costs,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) * paydays.n as costs_left,
       round(fin.balance
             + season.league_tickets / nullif(fx.home_played, 0) * fx.home_left
             + coalesce(sponsor.remaining_guaranteed, 0)
             - (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) * paydays.n) as balance_end_projected
from fin, season, fx, paydays
left join sponsor on true;

-- Gold BasketVibe : corrections relevées par l'agent Finances le 2026-10-18.
-- 1. bv_finance_projection.sponsor_left lisait le « reste garanti » d'un relevé sponsor antérieur au versement du dimanche :
--    on prend maintenant base hebdomadaire × dimanches de paie restants, plafonné par le reste garanti (8 versements max [M§10.1.2]).
-- 2. bv_finance_health.homegrown_last_week prenait une fenêtre de 7 jours glissants (comptait le 11/10 le 18/10) :
--    on prend le montant versé le dernier dimanche de paie (date du dernier salary_weekly).

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
  select s.weekly_base, s.remaining_guaranteed from silver.bv_sponsor_weekly s, me
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
       least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0)) as sponsor_left,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) as weekly_costs,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) * paydays.n as costs_left,
       round(fin.balance
             + season.league_tickets / nullif(fx.home_played, 0) * fx.home_left
             + least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0))
             - (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) * paydays.n) as balance_end_projected
from fin, season, fx, paydays
left join sponsor on true;

create or replace view gold.bv_finance_health with (security_invoker = true) as
with w as (
  select f.* from silver.bv_finance_weekly f
  join silver.bv_my_team me on me.team_id::text = f.team_id
  order by f.day desc limit 1
),
sp as (select weekly_base, win_bonus from silver.bv_sponsor_weekly order by week desc limit 1),
tk as (
  select round(avg(ticket_revenue) filter (where competition = 'league' and my_side = 'home')) as ticket_home,
         round(avg(ticket_revenue) filter (where competition = 'friendly' and my_side = 'home')) as ticket_friendly
  from silver.bv_matches
),
hg as (  -- bonus homegrown versé le dernier dimanche de paie
  select coalesce(sum(amount) filter (where kind = 'sponsor_homegrown_bonus'
           and game_day = (select max(game_day) from silver.bv_finance_transactions where kind = 'salary_weekly')), 0) as homegrown_last_week
  from silver.bv_finance_transactions
)
select w.day as as_of, w.balance, w.popularity,
       w.weekly_salaries, w.weekly_personnel, w.weekly_academy,
       w.weekly_salaries + w.weekly_personnel + w.weekly_academy                 as weekly_fixed_costs,
       sp.weekly_base                                                            as sponsor_weekly,
       tk.ticket_home,
       round(tk.ticket_home * 11 / 8.0)                                          as tickets_per_week,
       tk.ticket_friendly,
       tk.ticket_friendly * 7                                                    as friendlies_per_week,
       hg.homegrown_last_week,
       sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week as recurring_income_week,
       sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week
         - (w.weekly_salaries + w.weekly_personnel + w.weekly_academy)          as weekly_result_est,
       round(100.0 * w.weekly_salaries
         / nullif(sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week, 0), 1) as salaries_pct_of_income,
       w.transfer_available, w.transfer_committed
from w cross join sp cross join tk cross join hg;

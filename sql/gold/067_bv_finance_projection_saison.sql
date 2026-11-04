-- Gold BasketVibe : correction du 2026-11-03 (refonte v2, constat de gold.finance_health).
-- bv_finance_projection comptait les matchs des deux saisons (11 joués en saison 1, 11 à venir en saison 2) et divisait
-- les billets de la saison 2 (0 au 02/11) par les matchs de la saison 1 : 0 billet projeté, solde de fin à −1 943 053.
-- Maintenant : matchs de la saison en cours seulement (dernière saison des fixtures) ; billet par match à domicile =
-- moyenne de la saison en cours, ou, avant le premier match à domicile, moyenne mesurée de tous les matchs de ligue
-- à domicile (gold.bv_finance_health.ticket_home) ; ticket_source dit laquelle.

create or replace view gold.bv_finance_projection with (security_invoker = true) as
with me as (select team_id from silver.bv_my_team),
cur as (
  select f.season_id from silver.bv_fixtures f where f.is_mine order by f.match_day desc limit 1
),
fx as (
  select count(*) filter (where f.status = 'finished' and f.home_team_id = me.team_id) as home_played,
         count(*) filter (where f.status <> 'finished' and f.home_team_id = me.team_id) as home_left,
         max(f.match_day)                                                             as season_end
  from silver.bv_fixtures f, me, cur
  where f.is_mine and f.season_id = cur.season_id
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
tk as (
  select coalesce(round(season.league_tickets / nullif(fx.home_played, 0)), h.ticket_home) as ticket,
         case when fx.home_played > 0 then 'saison en cours' else 'moyenne mesurée (aucun match à domicile cette saison)' end as source
  from season, fx, gold.bv_finance_health h
),
sponsor as (
  select s.weekly_base, s.remaining_guaranteed from silver.bv_sponsor_weekly s, me
  where s.team_id = me.team_id::text
  order by s.week desc limit 1
),
last_paid as (
  select max(game_day) filter (where kind = 'salary_weekly')             as salary_day,
         max(game_day) filter (where kind = 'academy_weekly_investment') as academy_day
  from silver.bv_finance_transactions
),
paydays as (  -- dimanches de paie restants (salaires, personnel, sponsor)
  select count(*) as n
  from fx, last_paid, generate_series(greatest(current_date, coalesce(last_paid.salary_day, current_date - 1) + 1), fx.season_end, interval '1 day') d
  where extract(isodow from d) = 7
),
academy_days as (  -- prélèvements d'académie restants (même jour de semaine que le dernier)
  select count(*) as n
  from fx, last_paid, generate_series(greatest(current_date, coalesce(last_paid.academy_day, current_date - 1) + 1), fx.season_end, interval '1 day') d
  where extract(isodow from d) = coalesce(extract(isodow from last_paid.academy_day), 4)
)
select fin.day                                                     as as_of,
       fin.balance                                                 as balance_now,
       season.season_balance                                       as season_result_so_far,
       fx.home_played, fx.home_left, fx.season_end,
       paydays.n                                                   as paydays_left,
       tk.ticket                                                   as ticket_per_home_game,
       tk.ticket * fx.home_left                                    as tickets_left,
       least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0)) as sponsor_left,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) as weekly_costs,
       (fin.weekly_salaries + fin.weekly_personnel) * paydays.n + fin.weekly_academy * academy_days.n as costs_left,
       round(fin.balance
             + tk.ticket * fx.home_left
             + least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0))
             - (fin.weekly_salaries + fin.weekly_personnel) * paydays.n
             - fin.weekly_academy * academy_days.n) as balance_end_projected,
       academy_days.n                                              as academy_days_left,
       tk.source                                                   as ticket_source
from fin, season, fx, tk, paydays, academy_days
left join sponsor on true;

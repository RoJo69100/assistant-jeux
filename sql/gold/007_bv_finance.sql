-- Gold BasketVibe : santé financière, masse salariale, capacité d'investissement (agent Finances et Personnel).
-- Règles (skill basketvibe-economie) : charges le dimanche (salaires, personnel) et le jeudi (académie) [M§1.3] ;
-- billet 50 × 8 000 places × popularité, popularité remise à 70 % en début de saison [M§10.1.1] ; amical ≈ 6 % d'un match à domicile ;
-- sponsor : base chaque dimanche, 8 versements maximum [M§10.1.2] ; homegrown 200 par minute de ligue des juniors de l'académie,
-- plafond 40 000 par semaine [M§10.1.3] ; primes de classement [M§10.1.4] ; salaires recalculés en fin de saison [M§10.2].

-- Saison en cours : cumul par catégorie (résumé du jeu) et moyenne par semaine écoulée.
create or replace view gold.bv_finance_season_rates with (security_invoker = true) as
with s as (
  select f.* from silver.bv_finance_seasons f
  join silver.bv_my_team me on me.team_id::text = f.team_id
  where f.is_current
),
cal as (  -- dimanches de paie écoulés depuis le début de la saison (1re journée de ligue)
  select min(m.match_day) as season_start,
         count(*) filter (where m.my_side = 'home' and m.competition = 'league') as home_played,
         count(*) filter (where m.competition = 'friendly' and m.my_side = 'home') as home_friendlies
  from silver.bv_matches m
)
select s.as_of, c.season_start,
       (select count(*) from generate_series(c.season_start, s.as_of, interval '1 day') d where extract(isodow from d) = 7) as paydays,
       c.home_played, c.home_friendlies,
       s.league_tickets, s.friendlies, s.cups, s.sponsor, s.rewards, s.transfers_in, s.transfers_out,
       s.salaries, s.personnel, s.academy, s.season_balance
from s cross join cal c;

-- Santé de la semaine type : recettes récurrentes contre charges fixes actuelles (E15, E16).
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
hg as (  -- bonus homegrown versé la dernière semaine connue
  select coalesce(sum(amount) filter (where kind = 'sponsor_homegrown_bonus' and game_day >= current_date - 7), 0) as homegrown_last_week
  from silver.bv_finance_transactions
)
select w.day as as_of, w.balance, w.popularity,
       w.weekly_salaries, w.weekly_personnel, w.weekly_academy,
       w.weekly_salaries + w.weekly_personnel + w.weekly_academy                 as weekly_fixed_costs,
       sp.weekly_base                                                            as sponsor_weekly,
       tk.ticket_home,
       round(tk.ticket_home * 11 / 8.0)                                          as tickets_per_week,     -- 11 matchs à domicile sur 8 semaines
       tk.ticket_friendly,
       tk.ticket_friendly * 7                                                    as friendlies_per_week,  -- un amical à domicile par jour
       hg.homegrown_last_week,
       sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week as recurring_income_week,
       sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week
         - (w.weekly_salaries + w.weekly_personnel + w.weekly_academy)          as weekly_result_est,
       round(100.0 * w.weekly_salaries
         / nullif(sp.weekly_base + round(tk.ticket_home * 11 / 8.0) + tk.ticket_friendly * 7 + hg.homegrown_last_week, 0), 1) as salaries_pct_of_income,
       w.transfer_available, w.transfer_committed
from w cross join sp cross join tk cross join hg;

-- Projection de la saison 2 (8 semaines) et capacité d'investissement (E17).
-- HYPOTHÈSES (affichées, à rappeler) : même sponsor de base qu'en saison 1 ; popularité remise à 70 % → 280 000 par match à domicile
-- au départ, puis variation selon les résultats (non modélisée) ; 11 matchs à domicile ; amical à domicile chaque jour ; masse salariale,
-- personnel et académie actuels (les salaires seront recalculés en fin de saison : en hausse si les joueurs progressent) ;
-- homegrown au niveau de la dernière semaine ; réserve de sécurité = 2 semaines de charges fixes.
create or replace view gold.bv_finance_s2_projection with (security_invoker = true) as
with h as (select * from gold.bv_finance_health),
p as (select balance_end_projected from gold.bv_finance_projection),
st as (select rank from silver.bv_standings_weekly where is_mine order by day desc limit 1)
select h.as_of,
       p.balance_end_projected                                          as balance_end_s1,
       case when st.rank = 1 then 400000 when st.rank = 2 then 300000 when st.rank = 3 then 200000
            when st.rank = 4 then 100000 when st.rank <= 8 then 50000 else 0 end as reward_if_rank_kept,
       st.rank                                                          as current_rank,
       8 * h.sponsor_weekly                                             as s2_sponsor,
       11 * 280000                                                      as s2_tickets,
       56 * h.ticket_friendly                                           as s2_friendlies,
       8 * h.homegrown_last_week                                        as s2_homegrown,
       8 * h.weekly_salaries                                            as s2_salaries,
       8 * h.weekly_personnel                                           as s2_personnel,
       8 * h.weekly_academy                                             as s2_academy,
       8 * h.sponsor_weekly + 11 * 280000 + 56 * h.ticket_friendly + 8 * h.homegrown_last_week
         - 8 * (h.weekly_salaries + h.weekly_personnel + h.weekly_academy) as s2_result,
       2 * h.weekly_fixed_costs                                          as safety_reserve,
       p.balance_end_projected
         + case when st.rank <= 8 then 50000 else 0 end
         - 2 * h.weekly_fixed_costs                                      as investable_now_end_s1
from h cross join p cross join st;

-- Personnel : postes occupés, coût et effet (E18).
create or replace view gold.bv_personnel_status with (security_invoker = true) as
select p.week, r.role, r.hired, r.slots, r.unit_cost, r.hired * r.unit_cost as weekly_cost, r.effect_per_hire, r.current_effect
from (select * from silver.bv_personnel_weekly order by week desc limit 1) p
cross join lateral (values
  ('médecin',      p.doctors,       p.doctor_slots,       10000, '−25 % de durée de blessure', p.treatment_reduction_pct || ' % de durée en moins'),
  ('kinésithérapeute', p.physios,   p.physio_slots,        5000, '−12,5 % de risque de blessure', p.prevention_reduction_pct || ' % de risque en moins'),
  ('psychologue',  p.psychologists, p.psychologist_slots, 10000, '+5 pts vers une hausse de forme le dimanche', '+' || p.form_improvement_pp || ' pts'),
  ('marketing',    p.marketers,     p.marketer_slots,     12500, '−1 pt de popularité perdue par défaite à domicile', p.popularity_mitigation_pp || ' pts en moins')
) r(role, hired, slots, unit_cost, effect_per_hire, current_effect);

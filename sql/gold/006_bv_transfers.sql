-- Gold BasketVibe : marché des transferts (agent Transferts).
-- Règles (skills basketvibe-transferts / basketvibe-economie) : taxe vendeur 5 % [M§11.1] ; salaire selon la moyenne des 8 compétences,
-- barème 40 → 14 000, 50 → 21 000, 60 → 31 000, 70 → 41 000, 80 → 54 000, 90 → 68 000, 99 → 82 280 (interpolé) [M§10.2] ;
-- 0 progression à 30 ans, déclin dès 31 [M§8.5] ; au moins 9 joueurs disponibles pour vendre [M§11.1] ; TS = moyenne des 8 meilleurs PS [M§2.2].
-- Référence de prix : transferts conclus (silver.bv_transfers). Compétences connues seulement si le joueur a été vu en vente (silver.bv_transfer_auctions).

create or replace view gold.bv_salary_scale with (security_invoker = true) as
select * from (values (0, 0), (40, 14000), (50, 21000), (60, 31000), (70, 41000), (80, 54000), (90, 68000), (99, 82280), (100, 82280)) t(avg_skill, salary);

-- Prix conclus par tranche d'âge et poste, sur les 21 derniers jours (les prix bougent vite [Com 2026-09]).
create or replace view gold.bv_market_price_ref with (security_invoker = true) as
with t as (
  select distinct on (auction_id) * from silver.bv_transfers
  where fee > 0 and entry_type = 'transfer' and settled_at >= now() - interval '21 days'
  order by auction_id
)
select case when age <= 17 then '16-17' when age <= 21 then '18-21' when age <= 25 then '22-25'
            when age <= 29 then '26-29' else '30+' end as age_band,
       position, count(*) as n,
       percentile_cont(0.25) within group (order by fee) as p25,
       percentile_cont(0.5)  within group (order by fee) as median,
       percentile_cont(0.75) within group (order by fee) as p75,
       max(settled_at)::date as last_sale
from t group by 1, 2;

-- Ventes conclues dont on connaît les compétences (vues en vente avant) : la meilleure référence de prix.
create or replace view gold.bv_market_price_known with (security_invoker = true) as
with t as (select distinct on (auction_id) * from silver.bv_transfers where fee > 0 and entry_type = 'transfer' order by auction_id),
a as (select distinct on (player_id) * from silver.bv_transfer_auctions order by player_id, seen_at desc)
select t.settled_at::date as sold_on, t.name, t.position, t.age, a.ps,
       round((a.two_point + a.three_point + a.defense + a.passing + a.ball_handling + a.rebounding + a.stamina + a.athleticism) / 8.0, 1) as avg_skill,
       a.height_cm, a.starting_price, t.fee, a.seller_is_free_agent as was_free_agent,
       round(t.fee / nullif(a.ps, 0)) as fee_per_ps
from t join a using (player_id);

-- Joueurs en vente (dernier export du marché) jugés pour mon effectif.
create or replace view gold.bv_market_candidates with (security_invoker = true) as
with a as (
  select distinct on (auction_id) * from silver.bv_transfer_auctions
  where seen_at >= (select max(seen_at) - interval '2 hours' from silver.bv_transfer_auctions)
  order by auction_id, seen_at desc
),
height_eff(cm, pg, sg, sf, pf, c) as (
  values (175, 96, 82, 69, 60, 55), (180,100, 93, 80, 71, 55), (185,100, 98, 91, 82, 63), (190,100,100, 98, 93, 74),
         (195,100,100,100, 98, 85), (200,100,100,100,100, 96), (205, 95, 98,100,100,100), (210, 83, 90, 98,100,100),
         (215, 71, 78, 93, 98,100)
),
x as (
  select a.*,
         round((a.two_point + a.three_point + a.defense + a.passing + a.ball_handling + a.rebounding + a.stamina + a.athleticism) / 8.0, 1) as avg_skill,
         least(greatest(a.height_cm, 175), 215) as h,
         (floor(least(greatest(a.height_cm, 175), 214) / 5.0) * 5)::int as h0
  from a
),
slots as (  -- PS par emplacement × efficacité de taille, comme gold.bv_slot_fit (sans la forme)
  select x.auction_id, s.slot,
         round((x.two_point * s.w2 + x.three_point * s.w3 + x.passing * s.wpa + x.ball_handling * s.wbh + x.defense * s.wde
              + x.rebounding * s.wre + x.athleticism * s.wat + x.stamina * s.wst) / 100.0
              * (case s.slot when 'PG' then e0.pg + (e1.pg - e0.pg) * (x.h - x.h0) / 5.0
                             when 'SG' then e0.sg + (e1.sg - e0.sg) * (x.h - x.h0) / 5.0
                             when 'SF' then e0.sf + (e1.sf - e0.sf) * (x.h - x.h0) / 5.0
                             when 'PF' then e0.pf + (e1.pf - e0.pf) * (x.h - x.h0) / 5.0
                             else           e0.c  + (e1.c  - e0.c)  * (x.h - x.h0) / 5.0 end) / 100, 1) as fit
  from x
  cross join (values ('PG',15,15,15,15,15, 5,10,10), ('SG',15,15,10,15,15, 5,15,10), ('SF',15,15,10,10,15,10,15,10),
                     ('PF',15,10,10,10,15,15,15,10), ('C', 15,10,10,10,15,15,15,10)) s(slot, w2, w3, wpa, wbh, wde, wre, wat, wst)
  join height_eff e0 on e0.cm = x.h0
  join height_eff e1 on e1.cm = x.h0 + 5
),
best as (select distinct on (auction_id) auction_id, slot as best_slot, fit as best_fit from slots order by auction_id, fit desc),
mine as (  -- mon meilleur et mon 2e par emplacement (sans la forme), et le 8e PS de l'effectif
  select slot, max(fit) filter (where rk = 1) as my_best_fit, max(fit) filter (where rk = 2) as my_second_fit
  from (select slot, fit, rank() over (partition by slot order by fit desc, name) rk from gold.bv_slot_fit where not coalesce(on_transfer_list, false)) z
  group by slot
),
ts8 as (select min(ps) as eighth_ps from (select ps from gold.bv_roster_now order by ps desc limit 8) z)
select x.auction_id, x.name, x.position, x.age, x.height_cm, x.ps, x.avg_skill,
       b.best_slot, b.best_fit, m.my_best_fit, m.my_second_fit,
       round(b.best_fit - m.my_second_fit, 1) as gain_vs_my_second,
       x.ps > t.eighth_ps as enters_top8,
       round((select s1.salary + (s2.salary - s1.salary) * (x.avg_skill - s1.avg_skill) / nullif(s2.avg_skill - s1.avg_skill, 0)
              from gold.bv_salary_scale s1, gold.bv_salary_scale s2
              where s1.avg_skill = (select max(avg_skill) from gold.bv_salary_scale where avg_skill <= x.avg_skill)
                and s2.avg_skill = (select min(avg_skill) from gold.bv_salary_scale where avg_skill > x.avg_skill))) as est_weekly_salary,
       case when x.age >= 31 then 'déclin' when x.age = 30 then 'plateau' else 'progression possible' end as age_status,
       x.starting_price, x.current_price, x.bid_count, x.seller_is_free_agent as free_agent,
       (x.ends_at at time zone 'Europe/Paris') as ends_paris,
       r.median as ref_median_age_pos, r.n as ref_n,
       x.two_point, x.three_point, x.defense, x.passing, x.ball_handling, x.rebounding, x.stamina, x.athleticism,
       (select count(*) + 1 from gold.bv_slot_fit f
         where f.slot = b.best_slot and f.fit > b.best_fit and not coalesce(f.on_transfer_list, false)) as would_rank_in_slot
from x
join best b using (auction_id)
left join mine m on m.slot = b.best_slot
cross join ts8 t
left join gold.bv_market_price_ref r
  on r.position = x.position
 and r.age_band = case when x.age <= 17 then '16-17' when x.age <= 21 then '18-21' when x.age <= 25 then '22-25' when x.age <= 29 then '26-29' else '30+' end
where x.status like 'live%';

-- Mes joueurs à vendre : âge, salaire, potentiel, place dans la rotation.
create or replace view gold.bv_sell_candidates with (security_invoker = true) as
with pot as (
  select distinct on (player_id) player_id, potential_est, confidence from gold.bv_potential_estimate order by player_id, week desc
),
mins as (  -- minutes en ligue sur les 4 derniers matchs de ligue
  select player_id, round(avg(min), 1) as league_min_last4
  from (select l.*, dense_rank() over (order by match_day desc) rk from gold.bv_match_player_lines l where competition = 'league') z
  where rk <= 4 group by player_id
),
slot as (select distinct on (player_id) player_id, slot as best_slot, rank_in_slot from gold.bv_slot_fit order by player_id, fit desc)
select o.player_id, o.name, o.position, o.age, o.ps, o.salary, o.salary_per_ps,
       p.potential_est, p.confidence as potential_confidence,
       o.trend_s3, o.ps_s1, o.ps_s2,
       coalesce(m.league_min_last4, 0) as league_min_last4,
       s.best_slot, s.rank_in_slot,
       r.on_transfer_list,
       case when o.age >= 31 then 'déclin chaque semaine' when o.age = 30 then 'ne progresse plus, déclin dès la saison prochaine'
            when o.age = 29 then 'dernière saison de progression' else null end as age_flag,
       (select count(*) from gold.bv_roster_now where not coalesce(on_transfer_list, false) and injury_return_on is null) as available_players
from gold.bv_player_outlook o
left join pot p using (player_id)
left join mins m using (player_id)
left join slot s using (player_id)
left join gold.bv_roster_now r using (player_id);

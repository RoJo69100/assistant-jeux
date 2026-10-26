-- Gold BasketVibe : base des transferts passés, prix de référence par PS et âge, bonnes affaires et achat-revente.
-- Demande du 2026-10-26 (mémoire project-base-transferts-bonnes-affaires) : juger un prix contre les ventes conclues,
-- chercher les annonces sous ce prix, mesurer la marge nette de revente.
-- Règles : taxe vendeur 5 % [M§11.1, skill basketvibe-transferts] ; revente impossible avant une semaine [M§11.1].
-- Source : silver.bv_transfers (historique global, sans compétences) + silver.bv_transfer_auctions (compétences vues en vente).
-- Constat du 2026-10-26 (158 ventes connues) : saut de prix à PS 50, prix qui baisse avec l'âge ; d'où des tranches PS × âge.

-- Une ligne par transfert payé ; compétences quand l'enchère a été vue ; revente quand le joueur avait déjà été acheté.
create or replace view gold.bv_transfer_history with (security_invoker = true) as
with t as (
  select distinct on (auction_id) * from silver.bv_transfers
  where fee > 0 and entry_type = 'transfer'
  order by auction_id
),
a as (select distinct on (auction_id) * from silver.bv_transfer_auctions order by auction_id, seen_at desc),
r as (
  select t.*,
         lag(t.fee)        over w as prev_fee,
         lag(t.settled_at) over w as prev_settled_at,
         lag(t.to_team_id) over w as prev_buyer_id
  from t window w as (partition by t.player_id order by t.settled_at)
)
select r.settled_at::date as sold_on, r.auction_id, r.player_id, r.name, r.position, r.age,
       case when r.age <= 21 then '≤21' when r.age <= 25 then '22-25' when r.age <= 29 then '26-29' else '30+' end as age_band,
       a.ps, (floor(a.ps / 5) * 5)::int as ps_band,
       round((a.two_point + a.three_point + a.defense + a.passing + a.ball_handling + a.rebounding + a.stamina + a.athleticism) / 8.0, 1) as avg_skill,
       a.height_cm, a.starting_price, r.fee,
       round(r.fee / nullif(a.ps, 0)) as fee_per_ps,
       r.from_team, r.to_team,
       r.from_team_id = m.team_id as sold_by_me,
       r.to_team_id   = m.team_id as bought_by_me,
       a.seller_is_free_agent as was_free_agent,
       -- revente : le vendeur est l'acheteur précédent
       r.prev_buyer_id = r.from_team_id as is_resale,
       case when r.prev_buyer_id = r.from_team_id then r.prev_fee end as bought_for,
       case when r.prev_buyer_id = r.from_team_id then round(r.fee * 0.95 - r.prev_fee) end as resale_net_margin,
       case when r.prev_buyer_id = r.from_team_id then (r.settled_at::date - r.prev_settled_at::date) end as days_held,
       a.ps is not null as skills_known
from r
left join a on a.auction_id::text = r.auction_id::text
left join silver.bv_my_team m on true;

-- Prix de référence par tranche de PS (5 points) et d'âge, sur toutes les ventes dont les compétences sont connues.
-- n < 3 : référence fragile, à ne pas utiliser seule.
create or replace view gold.bv_price_ref_ps with (security_invoker = true) as
select ps_band, age_band, count(*) as n,
       percentile_cont(0.25) within group (order by fee) as p25,
       percentile_cont(0.5)  within group (order by fee) as median,
       percentile_cont(0.75) within group (order by fee) as p75,
       max(sold_on) as last_sale
from gold.bv_transfer_history
where skills_known
group by 1, 2;

-- Achat-revente constaté sur le marché : combien de reventes, part gagnante, marge nette médiane, durée de détention.
create or replace view gold.bv_resale_stats with (security_invoker = true) as
select grouping(ps_band, age_band) as level,  -- 0 = PS × âge, 1 = PS seul, 3 = total
       ps_band, age_band, count(*) as n,
       count(*) filter (where resale_net_margin > 0) as n_gain,
       percentile_cont(0.5) within group (order by resale_net_margin) as median_net_margin,
       percentile_cont(0.5) within group (order by days_held) as median_days_held
from gold.bv_transfer_history
where is_resale
group by rollup (ps_band, age_band);

-- Annonces en cours (dernier export du marché) comparées à la référence PS × âge.
-- L'enchère n'est pas finie : price_now monte encore, discount_pct n'est qu'un signal.
-- Le chiffre qui décide est bid_ceiling_resale : enchère maximale pour revendre au bas de la fourchette (p25) sans perte, taxe de 5 % déduite.
create or replace view gold.bv_market_bargains with (security_invoker = true) as
with a as (
  select distinct on (auction_id) * from silver.bv_transfer_auctions
  where seen_at >= (select max(seen_at) - interval '2 hours' from silver.bv_transfer_auctions)
    and status like 'live%'
  order by auction_id, seen_at desc
),
x as (
  select a.*, (floor(a.ps / 5) * 5)::int as ps_band,
         case when a.age <= 21 then '≤21' when a.age <= 25 then '22-25' when a.age <= 29 then '26-29' else '30+' end as age_band,
         greatest(a.current_price, a.starting_price) as price_now
  from a
)
select x.auction_id, x.name, x.position, x.age, x.ps, x.ps_band, x.age_band,
       x.seller_team, x.seller_is_free_agent as free_agent, x.bid_count,
       x.price_now, r.n as ref_n, r.p25 as ref_p25, r.median as ref_median, r.p75 as ref_p75,
       round((1 - x.price_now / nullif(r.median, 0)) * 100) as discount_pct,
       round(r.p25 * 0.95) as bid_ceiling_resale,
       round(r.p25 * 0.95 - x.price_now) as resale_margin_p25,
       round(r.median * 0.95 - x.price_now) as resale_margin_median,
       (x.ends_at at time zone 'Europe/Paris') as ends_paris,
       coalesce(r.n, 0) >= 3 as ref_reliable
from x
left join gold.bv_price_ref_ps r on r.ps_band = x.ps_band and r.age_band = x.age_band;

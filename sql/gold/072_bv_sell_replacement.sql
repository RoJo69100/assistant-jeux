-- Étape 5f, L1 (docs/refonte-v3/journal-aujourdhui.md) : pour chaque joueur, sa force à son meilleur poste, le remplaçant
-- du même poste et l'écart, avec le salaire hebdomadaire économisé par une vente. Vue additive, lecture seule.
-- Force = fit (sans la forme) pour le poste ET pour le remplaçant : une vente est définitive, la forme change chaque jour.
-- (gold.bv_sell_candidates choisit best_slot sur fit et rank_in_slot sur fit_with_form ; incohérence non reprise ici.)
create or replace view gold.bv_sell_replacement with (security_invoker = true) as
with f as (
  select player_id, name, slot, slot_order, fit,
         coalesce(on_transfer_list, false) as on_transfer_list,
         (not coalesce(on_transfer_list, false) and injury_return_on is null) as available
  from gold.bv_slot_fit
),
best as (  -- meilleur poste : fit le plus haut, égalité départagée par l'ordre des postes PG -> C
  select distinct on (player_id) player_id, name, slot as best_slot, fit as fit_best, on_transfer_list, available
  from f order by player_id, fit desc, slot_order
),
repl as (  -- meilleur autre joueur disponible dont le fit au même poste est inférieur ou égal
  select distinct on (b.player_id) b.player_id, r.player_id as replacement_id, r.name as replacement_name, r.fit as replacement_fit
  from best b
  join f r on r.slot = b.best_slot and r.player_id <> b.player_id and r.available and r.fit <= b.fit_best
  order by b.player_id, r.fit desc, r.player_id
)
select b.player_id, b.name, b.best_slot, b.fit_best,
       r.replacement_id, r.replacement_name, r.replacement_fit,
       round(b.fit_best - r.replacement_fit, 1) as gap,
       o.salary as weekly_salary,
       b.on_transfer_list, b.available,
       (select count(*) from f where f.slot = 'PG' and f.available) as available_players
from best b
left join repl r using (player_id)
left join gold.bv_player_outlook o using (player_id);

grant select on gold.bv_sell_replacement to assistant_ro;

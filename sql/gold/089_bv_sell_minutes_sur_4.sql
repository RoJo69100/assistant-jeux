-- 18/11 : gold.bv_sell_candidates.league_min_last4 était avg(min) sur les seules lignes où le joueur apparaît (006, l. 107) : un
-- joueur à 1 match de 12 min sur les 4 derniers matchs de ligue s'affichait à 12 au lieu de 3, et la règle « hors rotation
-- ≤ 6 min » le ratait. Désormais : somme des minutes sur les 4 derniers matchs de ligue de l'équipe / 4 (0 pour un match non joué).
-- Colonnes inchangées (même nom, même type numeric) : create or replace de la vue source, puis rafraîchissement de la vue
-- matérialisée (087). Test : pipelines/test_vues_lentes.py (cas 12 min sur 4 = 3,0 ; lecture < 5 s).

set local search_path = '';

create or replace view gold.bv_sell_candidates_src with (security_invoker = true) as
with pot as (
  select distinct on (player_id) player_id, potential_est, confidence from gold.bv_potential_estimate order by player_id, week desc
),
-- MINS-DEBUT
mins as (
  select l.player_id, round(sum(l.min)::numeric / 4, 1) as league_min_last4
  from gold.bv_match_player_lines l
  where l.competition = 'league' and l.fixture_id in (
    select x.fixture_id from (select distinct fixture_id, match_day from gold.bv_match_player_lines where competition = 'league') x
    order by x.match_day desc, x.fixture_id limit 4)
  group by l.player_id
),
-- MINS-FIN
slot as (select distinct on (player_id) player_id, slot as best_slot, rank_in_slot from gold.bv_slot_fit order by player_id, fit desc)
select o.player_id, o.name, o.position, o.age, o.ps, o.salary, o.salary_per_ps,
       p.potential_est, p.confidence as potential_confidence,
       o.trend_s3, o.ps_s1, o.ps_s2,
       coalesce(m.league_min_last4, 0::numeric) as league_min_last4,
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

refresh materialized view concurrently gold.bv_sell_candidates;

-- Gold BasketVibe : alertes du jour pour le brief quotidien (skill basketvibe-aujourdhui).
-- Seuils : fatigue > 20 = sortie de la zone verte [M§5.6.1] ; forme ≤ 2 = −8 à −11 % en attaque [M§5.5] ;
-- 9 joueurs disponibles minimum pour vendre [M§11.1] ; exports attendus selon la routine (wiki/routine.md).

create or replace view gold.bv_daily_alerts with (security_invoker = true) as
with r as (select * from gold.bv_roster_now),
last_cap as (
  select page_type, max(captured_at) as last_at
  from bronze.raw_pages where game = 'basketvibe' group by page_type
),
fresh(kind, page_types, max_age_days) as (
  values ('Effectif / Entraînement', array['roster','roster_skills','roster_tiles','training','training_progress','training_recent'], 7),
         ('Finances', array['finance','finance_sponsor'], 7),
         ('Académie', array['academy'], 7),
         ('Marché des transferts', array['transfers'], 2)
)
select 1 as priority, 'blessure' as category,
       r.name || ' blessé, retour le ' || to_char(r.injury_return_on, 'DD/MM') as alert
from r where r.injury_return_on is not null
union all
select 2, 'fatigue', r.name || ' : fatigue ' || round(r.fatigue) || ' (hors zone verte)'
from r where r.fatigue > 20
union all
select 2, 'forme', r.name || ' : forme ' || r.form || ' (attaque ' || case r.form::int when 1 then '−11 %' else '−8 %' end || ')'
from r where r.form <= 2
union all
select 1, 'finances', 'Semaine type déficitaire : ' || weekly_result_est || ' par semaine'
from gold.bv_finance_health where weekly_result_est < 0
union all
select 1, 'transferts', 'Moins de 9 joueurs disponibles : vente impossible'
from (select count(*) n from r where not coalesce(r.on_transfer_list, false) and r.injury_return_on is null) z where n < 9
union all
select 3, 'export', f.kind || ' : dernier export il y a ' || coalesce(extract(day from now() - max(c.last_at))::int::text, '?') || ' jour(s)'
from fresh f left join last_cap c on c.page_type = any(f.page_types)
group by f.kind, f.max_age_days
having max(c.last_at) is null or max(c.last_at) < now() - make_interval(days => f.max_age_days)
union all
select 2, 'match', 'Dernier match exporté : ' || m.match_day || ' (' || m.competition || ', ' || m.my_result || ' ' || m.my_pts || '-' || m.opp_pts || ' contre ' || m.opponent || ')'
from (select * from gold.bv_match_report order by match_day desc limit 1) m
union all
select 2, 'match', 'Match de ligue joué non exporté : J' || f.round_number || ' du ' || to_char(f.match_day, 'DD/MM')
from silver.bv_fixtures f
where f.is_mine and f.match_day < current_date and f.match_day >= current_date - 7
  and not exists (select 1 from silver.bv_matches m where m.fixture_id = f.fixture_id);

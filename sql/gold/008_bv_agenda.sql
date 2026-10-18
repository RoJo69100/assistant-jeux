-- Gold BasketVibe : agenda des actions des 7 prochains jours (brief quotidien, « que faire aujourd'hui »).
-- Sources : calendrier de ligue (silver.bv_fixtures), amicaux programmés (dernière capture /teams/<id>/friendlies),
-- mes ventes en cours (/teams/<id>/my-transfer-auctions), rythme de la semaine (skill basketvibe-saison [M§1.3]) :
-- ligue lun/mer/sam 20:00, verrouillage 19:45 ; amical : verrouillage 15 min avant ; entraînement dimanche 04:00 (Paris) [Obs] ;
-- académie jeudi 09:00 ; routine d'export de l'utilisateur (après chaque match ; dimanche après 04:00 : Entraînement + Finances + Personnel).
-- Heures en Europe/Paris.

create or replace view gold.bv_agenda with (security_invoker = true) as
with days as (
  select d::date as day from generate_series(current_date, current_date + 6, interval '1 day') d
),
league as (
  select f.match_day as day, f.round_number,
         case when f.home_team_id = me.team_id then f.away_team else f.home_team end as opponent,
         case when f.home_team_id = me.team_id then 'domicile' else 'extérieur' end as venue
  from silver.bv_fixtures f cross join silver.bv_my_team me
  where f.is_mine and f.status = 'scheduled' and f.match_day between current_date and current_date + 6
),
fr as (
  select (x->>'kickoff_at')::timestamptz at time zone 'Europe/Paris' as kickoff,
         case when x->>'home_team_name' = me_name.name then x->>'away_team_name' else x->>'home_team_name' end as opponent,
         (x->>'has_saved_match_tactics')::bool as has_plan
  from (select body from silver.bv_api where endpoint ~ '^/teams/[0-9a-f-]{36}/friendlies$' order by captured_at desc limit 1) a
  cross join lateral jsonb_array_elements(a.body->'friendlies') x
  cross join (select coalesce((select home_team from silver.bv_matches where my_side = 'home' limit 1), '') as name) me_name
  where x->>'status' = 'scheduled'
),
sales as (
  select (x->>'ends_at')::timestamptz at time zone 'Europe/Paris' as ends,
         x->>'player_first_name' || ' ' || (x->>'player_last_name') as player,
         (x->>'bid_count')::int as bids, (x->>'display_price')::numeric as price
  from (select body from silver.bv_api where endpoint ~ '/my-transfer-auctions$' order by captured_at desc limit 1) a
  cross join lateral jsonb_array_elements(a.body->'auctions') x
  where x->>'status' like 'live%'
),
season_end as (select max(f.match_day) as last_day from silver.bv_fixtures f where f.is_mine),
ev(day, at_time, priority, category, action) as (
  -- Ligue
  select day, time '19:45', 1, 'ligue', 'Avant 19:45 : vérifier le preset de ligue et régler le focus défensif sur la page du match J' || round_number || ' contre ' || opponent || ' (' || venue || ')' from league
  union all
  select day, time '19:30', 2, 'export', 'Avant 19:45 si possible : exporter la page Preview du match J' || round_number || ' (effectif adverse à jour)' from league
  union all
  select day, time '20:50', 2, 'export', 'Après le match (~20:50) : exporter la page du match J' || round_number || ' (puis analyse de l''agent Match)' from league
  -- Amicaux
  union all
  select kickoff::date, (kickoff - interval '15 minutes')::time, 1, 'amical',
         'Avant ' || to_char(kickoff - interval '15 minutes', 'HH24:MI') || ' : preset amical sur le match contre ' || opponent
         || case when has_plan then '' else ' (au dernier export : aucun plan sauvegardé)' end
  from fr where kickoff::date between current_date and current_date + 6
  union all
  select kickoff::date, (kickoff + interval '55 minutes')::time, 3, 'export', 'Après l''amical (~' || to_char(kickoff + interval '55 minutes', 'HH24:MI') || ') : exporter la page du match' from fr
  where kickoff::date between current_date and current_date + 6
  union all
  select d.day, time '12:00', 3, 'amical', 'Aucun amical programmé ce jour : en programmer un (recette ~17 500, minutes pour les jeunes, test v4)'
  from days d where d.day > current_date and not exists (select 1 from fr where fr.kickoff::date = d.day)
    and d.day <= (select last_day from season_end) + 1
  -- Entraînement, finances, académie
  union all
  select day, time '23:00', 2, 'entraînement', 'Avant dimanche 04:00 : vérifier et sauvegarder les choix d''entraînement (fiche de l''agent Entraînement)' from days where extract(isodow from day) = 6
  union all
  select day, time '04:30', 1, 'export', 'Après 04:00 : exporter Entraînement, Finances et Personnel (routine du dimanche)' from days where extract(isodow from day) = 7
  union all
  select day, time '09:30', 3, 'export', 'Après 09:00 : exporter la page Académie (nouveau rapport du scout) ; Finances en option' from days where extract(isodow from day) = 4
  -- Mes ventes
  union all
  select ends::date, ends::time, 2, 'transfert', 'Fin de la vente de ' || player || ' (' || bids || ' enchère(s), prix affiché ' || price || ')' from sales
  where ends::date between current_date and current_date + 6
  -- Fin de saison
  union all
  select last_day, time '21:00', 1, 'saison', 'Dernier match de la saison : maintien et prime de classement se jouent ce soir' from season_end
  where last_day between current_date and current_date + 6
)
select day,
       (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from day)::int] || ' ' || to_char(day, 'DD/MM') as day_label,
       at_time, priority, category, action
from ev
order by day, at_time, priority;

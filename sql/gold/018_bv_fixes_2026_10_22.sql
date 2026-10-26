-- Gold BasketVibe : corrections du 2026-10-22.
-- 1. bv_finance_projection comptait l'académie sur les dimanches de paie, alors qu'elle est prélevée le jeudi
--    (academy_weekly_investment les 08, 15 et 22/10) : le 22/10, 100 000 déjà payés étaient recomptés
--    (costs_left 490 996 au lieu de 390 996, investable_now_end_s1 à -4 000). Relevé par l'agent Finances.
--    Maintenant : salaires + personnel × dimanches restants après le dernier prélèvement de salaires,
--    académie × jours restants du même jour de semaine que le dernier prélèvement d'académie.
-- 2. bv_agenda reconnaissait mon club dans les amicaux par son nom, pris dans un match quelconque :
--    après le renommage (« Chomelix Cow's » → « Chomelix Cow »), l'adversaire affiché était mon propre club.
--    Maintenant : comparaison par team_id ; le lieu (domicile/extérieur) est ajouté.

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
       round(season.league_tickets / nullif(fx.home_played, 0))    as ticket_per_home_game,
       round(season.league_tickets / nullif(fx.home_played, 0) * fx.home_left) as tickets_left,
       least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0)) as sponsor_left,
       (fin.weekly_salaries + fin.weekly_personnel + fin.weekly_academy) as weekly_costs,
       (fin.weekly_salaries + fin.weekly_personnel) * paydays.n + fin.weekly_academy * academy_days.n as costs_left,
       round(fin.balance
             + season.league_tickets / nullif(fx.home_played, 0) * fx.home_left
             + least(coalesce(sponsor.weekly_base, 0) * paydays.n, coalesce(sponsor.remaining_guaranteed, 0))
             - (fin.weekly_salaries + fin.weekly_personnel) * paydays.n
             - fin.weekly_academy * academy_days.n) as balance_end_projected,
       academy_days.n                                              as academy_days_left
from fin, season, fx, paydays, academy_days
left join sponsor on true;

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
         case when (x->>'home_team_id')::uuid = me.team_id then x->>'away_team_name' else x->>'home_team_name' end as opponent,
         case when (x->>'home_team_id')::uuid = me.team_id then 'domicile' else 'extérieur' end as venue,
         (x->>'has_saved_match_tactics')::bool as has_plan
  from (select body from silver.bv_api where endpoint ~ '^/teams/[0-9a-f-]{36}/friendlies$' order by captured_at desc limit 1) a
  cross join lateral jsonb_array_elements(a.body->'friendlies') x
  cross join silver.bv_my_team me
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
         'Avant ' || to_char(kickoff - interval '15 minutes', 'HH24:MI') || ' : preset amical sur le match contre ' || opponent || ' (' || venue || ')'
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

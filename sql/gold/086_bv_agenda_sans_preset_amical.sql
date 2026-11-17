-- 17/11 (décision de l'utilisateur) : l'amical est un test sans preset (docs/attentes/jeux/basketvibe.yaml : amical, preset non).
-- gold.bv_agenda n'émet plus « Avant HH:MM : preset amical sur le match contre … ». Seule différence avec la définition en base :
-- la branche « preset amical » du CTE ev est retirée ; l'export d'après l'amical et la ligne « aucun amical programmé » restent.
create or replace view gold.bv_agenda as
with days as (
    select d.d::date as day
    from generate_series(current_date::timestamptz, (current_date + 6)::timestamptz, '1 day'::interval) d(d)
), league as (
    select f.match_day as day, f.round_number,
           case when f.home_team_id = me.team_id then f.away_team else f.home_team end as opponent,
           case when f.home_team_id = me.team_id then 'domicile'::text else 'extérieur'::text end as venue
    from silver.bv_fixtures f
    cross join silver.bv_my_team me
    where f.is_mine and f.status = 'scheduled' and f.match_day >= current_date and f.match_day <= current_date + 6
), fr as (
    select ((x.value ->> 'kickoff_at')::timestamptz at time zone 'Europe/Paris') as kickoff,
           case when (x.value ->> 'home_team_id')::uuid = me.team_id then x.value ->> 'away_team_name' else x.value ->> 'home_team_name' end as opponent,
           case when (x.value ->> 'home_team_id')::uuid = me.team_id then 'domicile'::text else 'extérieur'::text end as venue,
           (x.value ->> 'has_saved_match_tactics')::boolean as has_plan
    from (select bv_api.body from silver.bv_api
          where bv_api.endpoint ~ '^/teams/[0-9a-f-]{36}/friendlies$'
          order by bv_api.captured_at desc limit 1) a
    cross join lateral jsonb_array_elements(a.body -> 'friendlies') x(value)
    cross join silver.bv_my_team me
    where (x.value ->> 'status') = 'scheduled'
), sales as (
    select ((x.value ->> 'ends_at')::timestamptz at time zone 'Europe/Paris') as ends,
           ((x.value ->> 'player_first_name') || ' ') || (x.value ->> 'player_last_name') as player,
           (x.value ->> 'bid_count')::integer as bids,
           (x.value ->> 'display_price')::numeric as price
    from (select bv_api.body from silver.bv_api
          where bv_api.endpoint ~ '/my-transfer-auctions$'
          order by bv_api.captured_at desc limit 1) a
    cross join lateral jsonb_array_elements(a.body -> 'auctions') x(value)
    where (x.value ->> 'status') like 'live%'
), season_end as (
    select max(f.match_day) as last_day from silver.bv_fixtures f where f.is_mine
), ev(day, at_time, priority, category, action) as (
    select league.day, '19:45:00'::time, 1, 'ligue'::text,
           'Avant 19:45 : vérifier le preset de ligue et régler le focus défensif sur la page du match J' || league.round_number
           || ' contre ' || league.opponent || ' (' || league.venue || ')'
    from league
    union all
    select league.day, '19:30:00'::time, 2, 'export'::text,
           'Avant 19:45 si possible : exporter la page Preview du match J' || league.round_number || ' (effectif adverse à jour)'
    from league
    union all
    select league.day, '20:50:00'::time, 2, 'export'::text,
           'Après le match (~20:50) : exporter la page du match J' || league.round_number || ' (puis analyse de l''agent Match)'
    from league
    union all
    select fr.kickoff::date, (fr.kickoff + '00:55:00'::interval)::time, 3, 'export'::text,
           'Après l''amical (~' || to_char(fr.kickoff + '00:55:00'::interval, 'HH24:MI') || ') : exporter la page du match'
    from fr
    where fr.kickoff::date >= current_date and fr.kickoff::date <= current_date + 6
    union all
    select d.day, '12:00:00'::time, 3, 'amical'::text,
           'Aucun amical programmé ce jour : en programmer un (recette ~17 500, minutes pour les jeunes, test v4)'::text
    from days d
    where d.day > current_date and not exists (select 1 from fr where fr.kickoff::date = d.day)
      and d.day <= (select season_end.last_day from season_end) + 1
    union all
    select days.day, '23:00:00'::time, 2, 'entraînement'::text,
           'Avant dimanche 04:00 : vérifier et sauvegarder les choix d''entraînement (fiche de l''agent Entraînement)'::text
    from days where extract(isodow from days.day) = 6
    union all
    select days.day, '04:30:00'::time, 1, 'export'::text,
           'Après 04:00 : exporter Entraînement, Finances et Personnel (routine du dimanche)'::text
    from days where extract(isodow from days.day) = 7
    union all
    select days.day, '09:30:00'::time, 3, 'export'::text,
           'Après 09:00 : exporter la page Académie (nouveau rapport du scout) ; Finances en option'::text
    from days where extract(isodow from days.day) = 4
    union all
    select sales.ends::date, sales.ends::time, 2, 'transfert'::text,
           'Fin de la vente de ' || sales.player || ' (' || sales.bids || ' enchère(s), prix affiché ' || sales.price || ')'
    from sales
    where sales.ends::date >= current_date and sales.ends::date <= current_date + 6
    union all
    select season_end.last_day, '21:00:00'::time, 1, 'saison'::text,
           'Dernier match de la saison : maintien et prime de classement se jouent ce soir'::text
    from season_end
    where season_end.last_day >= current_date and season_end.last_day <= current_date + 6
)
select day,
       ((array['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'])[extract(isodow from day)::integer] || ' ')
       || to_char(day::timestamptz, 'DD/MM') as day_label,
       at_time, priority, category, action
from ev
order by day, at_time, priority;

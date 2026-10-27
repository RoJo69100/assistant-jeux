-- Six Zero League : bilan d'effectif par poste et comparaison victoires / défaites (2026-10-27)
-- Règles générales « vue gold systématique » et « questions effectif à chaque passage » (CLAUDE.md, Vitesse 4-5).

-- 1. Bilan d'effectif : rang au poste, statut (titulaire / doublure / surplus), salaire, temps de jeu.
create or replace view gold.sz_effectif_bilan as
with p as (
  select * from silver.sz_players
  where as_of = (select max(as_of) from silver.sz_players)
),
jeu as (
  select mp.player_id,
         count(distinct mp.match_id)            as matchs_feuille,
         sum(mp.goals)                          as buts,
         sum(mp.shots)                          as tirs,
         sum(mp.saves)                          as arrets,
         sum(mp.exclusions)                     as exclusions
  from silver.sz_match_players mp
  where mp.is_mine
  group by mp.player_id
),
r as (
  select p.*, row_number() over (partition by p.role order by p.overall desc, p.age) as rang_poste,
         count(*) over (partition by p.role) as nb_poste
  from p
)
select r.role                                   as poste,
       r.rang_poste,
       r.name                                   as joueur,
       r.age,
       r.overall                                as note,
       r.wage                                   as salaire,
       coalesce(j.matchs_feuille, 0)            as matchs_feuille,
       coalesce(j.buts, 0)                      as buts,
       coalesce(j.tirs, 0)                      as tirs,
       round(100.0 * j.buts / nullif(j.tirs, 0), 1) as pct_tir,
       coalesce(j.arrets, 0)                    as arrets,
       coalesce(j.exclusions, 0)                as exclusions,
       case when r.rang_poste = 1 then 'titulaire'
            when r.rang_poste = 2 then 'doublure'
            else 'surplus' end                  as statut,
       r.injured                                as blesse,
       r.retiring                               as retraite,
       r.for_sale                               as en_vente,
       sum(r.wage) over ()                      as masse_salariale,
       count(*) over ()                         as effectif,
       r.as_of
from r
left join jeu j on j.player_id = r.player_id
order by array_position(array['GK','CB','LB','RB','LW','RW','P'], r.role), r.rang_poste;

-- 2. Victoires contre défaites : moyennes par résultat (W / D / L) et écart victoire − défaite.
create or replace view gold.sz_vd_comparatif as
with m as (
  select distinct on (match_id) * from silver.sz_matches
  where result in ('W','D','L')
  order by match_id, captured_at desc
),
agg as (
  select result,
         count(*)                                         as matchs,
         round(avg(goals), 1)                             as buts,
         round(avg(opp_goals), 1)                         as buts_contre,
         round(avg(shots), 1)                             as tirs,
         round(avg(opp_shots), 1)                         as tirs_contre,
         round(100.0 * sum(goals) / nullif(sum(shots), 0), 1)         as pct_tir,
         round(100.0 * sum(opp_goals) / nullif(sum(opp_shots), 0), 1) as pct_tir_contre,
         round(avg(save_pct), 1)                          as pct_arrets,
         round(avg(opp_save_pct), 1)                      as pct_arrets_contre,
         round(avg(turnovers), 1)                         as pertes,
         round(avg(opp_steals), 1)                        as interceptions_contre,
         round(avg(steals), 1)                            as interceptions,
         round(avg(exclusions), 1)                        as exclusions,
         round(avg(opp_exclusions), 1)                    as exclusions_contre,
         round(avg(opp_seven_m_shots), 1)                 as sept_m_concedes,
         round(avg(seven_m_shots), 1)                     as sept_m_obtenus,
         round(avg(possession_s) / 60.0, 1)               as possession_min,
         sum(case when venue = 'home' then 1 else 0 end)  as domicile,
         sum(case when opponent_is_bot then 1 else 0 end) as contre_bots
  from m group by result
)
select result as resultat, matchs, buts, buts_contre, tirs, tirs_contre, pct_tir, pct_tir_contre,
       pct_arrets, pct_arrets_contre, pertes, interceptions, interceptions_contre,
       exclusions, exclusions_contre, sept_m_obtenus, sept_m_concedes, possession_min, domicile, contre_bots
from agg
union all
select 'W-L', null,
       w.buts - l.buts, w.buts_contre - l.buts_contre, w.tirs - l.tirs, w.tirs_contre - l.tirs_contre,
       w.pct_tir - l.pct_tir, w.pct_tir_contre - l.pct_tir_contre,
       w.pct_arrets - l.pct_arrets, w.pct_arrets_contre - l.pct_arrets_contre,
       w.pertes - l.pertes, w.interceptions - l.interceptions, w.interceptions_contre - l.interceptions_contre,
       w.exclusions - l.exclusions, w.exclusions_contre - l.exclusions_contre,
       w.sept_m_obtenus - l.sept_m_obtenus, w.sept_m_concedes - l.sept_m_concedes,
       w.possession_min - l.possession_min, null, null
from agg w, agg l where w.result = 'W' and l.result = 'L';

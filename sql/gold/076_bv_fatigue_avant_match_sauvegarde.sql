-- Phase 0 du plan du jour (instantané du 12/11) : « Sors … » était calculé depuis l'écran de coupe non sauvegardé.
-- Ajoute à gold.bv_fatigue_avant_match (075) l'indicateur de sauvegarde de l'écran (gold.bv_saisie_joueurs.sauvegarde_match,
-- issu de has_saved_match_tactics) et le repli `ecran_par_defaut` : les 14 joueurs du match à 48 min et agressivité 3.
-- Colonnes ajoutées en fin de vue (create or replace view le permet). Lecture seule.
create or replace view gold.bv_fatigue_avant_match with (security_invoker = true) as
with s as (
  select kind, match_day, opponent, joueur, fixture_id, sauvegarde_match,
         nullif(substring(minutes from '^[0-9]+'), '')::int as minutes,
         agress - 1 as defense_tier
  from gold.bv_saisie_joueurs
  where kind in ('ligue', 'coupe') and match_day >= current_date
),
d as (
  select kind, match_day, opponent,
         (count(*) = 14 and bool_and(minutes = 48 and defense_tier = 2)) as ecran_par_defaut
  from s group by kind, match_day, opponent
),
r as (
  select seuil_bas as zone_verte from core.alert_rule where game = 'basketvibe' and rule_id = 'fatigue' and actif
)
select s.kind, s.match_day, s.opponent, s.joueur, p.name, s.minutes, s.defense_tier, p.sat_fatigue,
       r.zone_verte, (p.sat_fatigue > r.zone_verte) as depasse, s.fixture_id,
       s.sauvegarde_match, d.ecran_par_defaut
from s
cross join r
join d using (kind, match_day, opponent)
left join gold.bv_fatigue_plan p
  on p.name like '% ' || s.joueur and p.minutes = s.minutes and p.defense_tier = s.defense_tier
where s.minutes > 0;

grant select on gold.bv_fatigue_avant_match to assistant_ro;

-- Test : coupe du 12/11 contre Stare Kotlety, écran non sauvegardé : sauvegarde_match = false sur chaque ligne.
-- select kind, match_day, opponent, bool_or(sauvegarde_match), bool_or(ecran_par_defaut) from gold.bv_fatigue_avant_match group by 1,2,3;

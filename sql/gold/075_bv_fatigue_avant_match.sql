-- Étape 5h, N3 (docs/refonte-v3/journal-aujourdhui.md) : fatigue projetée de chaque joueur qui doit jouer un match
-- de ligue ou de coupe à venir, d'après la saisie du match (gold.bv_saisie_joueurs : minutes, agressivité) et
-- gold.bv_fatigue_plan (fatigue stabilisée au samedi, rythme lun/mer/sam ; les amicaux n'y sont pas comptés).
-- Zone verte = seuil_bas de la règle `fatigue` de core.alert_rule (aucun seuil écrit ici). Vue additive, lecture seule.
-- Jointure par nom : gold.bv_saisie_joueurs n'expose que le nom de famille ; bv_fatigue_plan.name = « Prénom Nom ».
create or replace view gold.bv_fatigue_avant_match with (security_invoker = true) as
with s as (
  select kind, match_day, opponent, joueur, fixture_id,
         nullif(substring(minutes from '^[0-9]+'), '')::int as minutes,
         agress - 1 as defense_tier
  from gold.bv_saisie_joueurs
  where kind in ('ligue', 'coupe') and match_day >= current_date
),
r as (
  select seuil_bas as zone_verte from core.alert_rule where game = 'basketvibe' and rule_id = 'fatigue' and actif
)
select s.kind, s.match_day, s.opponent, s.joueur, p.name, s.minutes, s.defense_tier, p.sat_fatigue,
       r.zone_verte, (p.sat_fatigue > r.zone_verte) as depasse, s.fixture_id
from s
cross join r
left join gold.bv_fatigue_plan p
  on p.name like '% ' || s.joueur and p.minutes = s.minutes and p.defense_tier = s.defense_tier
where s.minutes > 0;

grant select on gold.bv_fatigue_avant_match to assistant_ro;

-- Test : J4 du 09/11 contre Naked Spartans, 10 joueurs à 24 min, cran 2 : fatigue 11,0 à 14,1, aucun dépassement (zone verte 20).
-- select joueur, minutes, defense_tier, sat_fatigue, zone_verte, depasse from gold.bv_fatigue_avant_match order by sat_fatigue desc;

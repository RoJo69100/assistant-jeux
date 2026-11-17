-- P2 du plan v4 (13/11) : vues lues par pipelines/etat_jour.py (état calculé par événement). Lecture seule.
-- « Âge d'export » : aucune colonne last_seen_at n'existe en base (vérifié le 17/11 dans information_schema) ; l'âge vient de
-- silver.bv_api.captured_at, dont les identifiants de page sont ceux de core.fixture.fixture_id (ligue, coupe, amical).

-- 1. Un match (ligue, coupe, amical) de J-7 à J+3 : calendrier, statut « fini » (core.fixture.played), verrou, aperçu et page
--    du match capturés, saisie sauvegardée (gold.bv_saisie_joueurs.sauvegarde_match, par fixture_id).
create or replace view gold.bv_etat_match with (security_invoker = true) as
with f as (
  select f.fixture_id, f.competition_kind, f.day, f.opponent, f.home, f.played, f.my_result,
         f.scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris,
         (f.extras ->> 'verrou_at')::timestamptz at time zone 'Europe/Paris' as verrou_paris
  from core.fixture f
  where f.game = 'basketvibe'
    and f.day between (now() at time zone 'Europe/Paris')::date - 7 and (now() at time zone 'Europe/Paris')::date + 3
),
cap as (
  select substring(a.endpoint from '/([0-9a-f]{8}-[0-9a-f-]{27})/') as fixture_id,
         max(a.captured_at) filter (where a.endpoint ~ '/preview$') as apercu_at,
         max(a.captured_at) filter (where a.endpoint ~ '/period-box$') as page_at
  from silver.bv_api a
  where a.endpoint ~ '^/(fixtures|friendlies|cup-fixtures)/[0-9a-f-]{36}/(preview|period-box)$'
  group by 1
),
s as (
  select fixture_id, bool_or(sauvegarde_match) as sauvegarde, max(export_paris) as saisie_export_paris,
         count(*) filter (where nullif(substring(minutes from '^[0-9]+'), '')::int > 0) as joueurs_saisis
  from gold.bv_saisie_joueurs
  group by fixture_id
)
select f.fixture_id, f.competition_kind, f.day, f.opponent, f.home, f.played, f.my_result, f.coup_envoi_paris, f.verrou_paris,
       cap.apercu_at at time zone 'Europe/Paris' as apercu_paris,
       cap.page_at at time zone 'Europe/Paris' as page_paris,
       s.sauvegarde, s.saisie_export_paris, s.joueurs_saisis
from f
left join cap on cap.fixture_id = f.fixture_id
left join s on s.fixture_id = f.fixture_id;

grant select on gold.bv_etat_match to assistant_ro;

-- 2. Blessure comparée à la date de chaque match à venir (J à J+3), par player_id : indisponible si le retour est postérieur au jour du match.
create or replace view gold.bv_blessures_match with (security_invoker = true) as
select r.player_id, r.name, r.injury_return_on, f.fixture_id, f.competition_kind, f.day,
       (r.injury_return_on > f.day) as indisponible
from gold.bv_roster_now r
join core.fixture f
  on f.game = 'basketvibe' and not f.played
 and f.day between (now() at time zone 'Europe/Paris')::date and (now() at time zone 'Europe/Paris')::date + 3
where r.injury_return_on is not null;

grant select on gold.bv_blessures_match to assistant_ro;

-- Test : select competition_kind, day, opponent, played, apercu_paris, page_paris, sauvegarde from gold.bv_etat_match order by day;

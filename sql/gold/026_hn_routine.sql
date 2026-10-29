-- Hockey Nation : routine quotidienne en SQL, sans agent (2026-10-29, mise à niveau sur BasketVibe).
-- hn_today (jour de saison + événements), hn_exports_state (fraîcheur des exports), hn_saisie_lignes (lignes PRO A/B/C enregistrées,
-- poste par poste, avec les trous), hn_daily_alerts (réécrite : offres reçues, plafond en direct, exports périmés, lignes à refaire).

-- Jour de saison. Le jour 1 se déduit de la fermeture de la fenêtre I (jour 35, /trade-center/trade-window) [G:Calendar].
-- À revoir à l'ouverture de la fenêtre II (jour 51) : le timestamp changera.
create or replace view gold.hn_today with (security_invoker = true) as
with s as (select * from silver.hn_season limit 1),
d as (select s.season, s.phase, (s.trade_window_ts at time zone 'Europe/Paris')::date - 34 as day1, s.next_event, s.next_event_at,
             s.draft_at, s.last_capture from s)
select d.season, d.phase, d.day1, (now() at time zone 'Europe/Paris')::date as today,
       (now() at time zone 'Europe/Paris')::date - d.day1 + 1 as season_day,
       (select string_agg('J' || c.day || ' (' || to_char(d.day1 + c.day - 1, 'DD/MM') || ') : ' || c.event, ' ; ' order by c.day)
        from gold.hn_calendar c where c.day between (now() at time zone 'Europe/Paris')::date - d.day1 + 1
                                            and (now() at time zone 'Europe/Paris')::date - d.day1 + 1) as today_events,
       (select 'J' || c.day || ' (' || to_char(d.day1 + c.day - 1, 'DD/MM') || ') : ' || c.event
        from gold.hn_calendar c where c.day > (now() at time zone 'Europe/Paris')::date - d.day1 + 1 order by c.day limit 1) as next_calendar_event,
       d.next_event, d.next_event_at at time zone 'Europe/Paris' as next_event_paris,
       (d.last_capture at time zone 'Europe/Paris') as last_capture_paris
from d;

-- Fraîcheur des exports utiles à la décision. max_age_h = âge au-delà duquel l'export est à refaire (config hockeynation.yaml, exports).
create or replace view gold.hn_exports_state with (security_invoker = true) as
with need(ordre, ecran, route, max_age_h, pour_quoi) as (values
  (1, 'Roster PRO, FRM, U21, U17', '/team/:id/roster', 24, 'effectif, talents, contrats'),
  (2, 'Office > Salary cap', '/office/salary-cap-overview', 24, 'cap space avant échange ou signature'),
  (3, 'Trade Center > offres', '/trade-center/trade-offers', 24, 'offres reçues et envoyées'),
  (4, 'Trade Center > recherche', '/trade-center/search', 24, 'cibles d''échange'),
  (5, 'Lineups PRO', '/team/:id/lineups', 24, 'lignes enregistrées'),
  (6, 'Training (journal)', '/club/:id/training-log', 24, 'entraînement PRO / FRM'),
  (7, 'Coaching staff', '/club/:id/coaching-staff', 48, 'coachs en poste et réponses'),
  (8, 'Scouting staff', '/club/:id/scouting-staff', 48, 'scouts embauchés'),
  (9, 'Scouting budget', '/club/:id/scouting-budget-overview', 48, 'budget de scouting'),
  (10, 'Contract talks', '/club/:id/expiring-players', 72, 'prolongations'),
  (11, 'Club finances', '/club/:id/finances', 72, 'rachats, salaires par saison'),
  (12, 'Draft class', '/league/:id/draft-class', 168, 'rapports des scouts'),
  (13, 'Matchs (programme)', '/club/:id/game-overview', 24, 'résultats et prochains matchs'),
  (14, 'Classement', '/league/:id/standings', 48, 'classement')
)
select n.ordre, n.ecran, n.pour_quoi,
       max(a.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(a.captured_at)) / 3600) as age_h,
       case when max(a.captured_at) is null then '🟥 jamais'
            when now() - max(a.captured_at) > make_interval(hours => n.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from need n left join silver.hn_api a on a.route = n.route
group by n.ordre, n.ecran, n.pour_quoi, n.max_age_h
order by n.ordre;

-- Lignes PRO enregistrées dans le jeu (dernier export), dans l'ordre de l'écran, avec le contrôle de chaque case :
-- joueur parti (absent du roster PRO = le jeu met un amateur, −5 % par amateur), hors poste (−20 %), contre-emploi.
create or replace view gold.hn_saisie_lignes with (security_invoker = true) as
with l as (select * from silver.hn_lineups),
pro as (select * from silver.hn_players where team_level = 'PRO'),
ord(line, ord_line) as (values ('L1',1),('L2',2),('L3',3),('L4',4),('G',5),('PP1',6),('PP2',7),('PK4-1',8),('PK4-2',9),
                                ('PK3-1',10),('PK3-2',11),('4V4-1',12),('4V4-2',13),('EXT',14)),
sord(slot, ord_slot) as (values ('LW',1),('C',2),('RW',3),('LD',4),('RD',5),('D',6),('ANY',7),('FW',8),('FW1',9),('FW2',10),('SG',11),('BG',12))
select l.lineup, l.line, l.slot, coalesce(o.ord_line, 99) * 100 + coalesce(so.ord_slot, 99) as ordre,
       coalesce(p.name, '⚠ parti (' || left(l.player_id::text, 8) || ')') as joueur,
       p.main_position as poste_joueur, p.rating, p.endu as endurance,
       case when p.player_id is null then '🟥 absent du roster PRO'
            when l.slot in ('LW','C','RW','LD','RD') and not (p.positions ? l.slot) then '🟧 hors poste (−20 %)'
            when l.slot = 'D' and not (p.positions ?| array['LD','RD']) then '🟧 hors poste (−20 %)'
            when l.slot = 'FW' or l.slot like 'FW_' then case when p.positions ?| array['LW','C','RW'] then 'ok' else '🟧 D en attaque' end
            else 'ok' end as controle,
       f.verdict as fit, l.day as enregistre_le
from l
left join pro p on p.player_id = l.player_id
left join ord o on o.line = l.line
left join sord so on so.slot = l.slot
left join gold.hn_player_fit f on f.player_id = l.player_id and f.is_main;

-- Alertes Hockey Nation, rouge d'abord. Le brief du jour et le registre fait-… passent avant ces alertes.
create or replace view gold.hn_daily_alerts with (security_invoker = true) as
with s as (select * from silver.hn_season order by season desc limit 1)
select 1 as prio, '🟥 URGENT' as niveau, 'draft' as domaine,
       'Pré-instructions de draft avant ' || to_char(s.draft_deadline_at at time zone 'Europe/Paris', 'DD/MM HH24:MI') || ' (Paris)' as alerte
from s where s.draft_deadline_at > now() and s.draft_deadline_at < now() + interval '48 hours'
union all
select 1, '🟥 URGENT', 'transferts',
       'Offre reçue de ' || offering_team || ' : ils donnent ' || they_give || ' contre ' || they_get || ' (relevé du ' || to_char(captured_at at time zone 'Europe/Paris', 'DD/MM HH24:MI') || ')'
from silver.hn_trade_offers where direction = 'reçue' and needs_acceptance
union all
select 1, '🟥 URGENT', 'tactique',
       'Lineup ' || lineup || ' : ' || count(*) || ' case(s) avec un joueur parti (amateur en match), export du ' || to_char(max(enregistre_le), 'DD/MM')
from gold.hn_saisie_lignes where controle like '🟥%' group by lineup
union all
select 2, '🟧 IMPORTANT', 'tactique',
       'Lineup ' || lineup || ' : ' || count(*) || ' case(s) hors poste'
from gold.hn_saisie_lignes where controle like '🟧%' group by lineup
union all
select 2, '🟧 IMPORTANT', 'contrats',
       'Cap space S' || (select season from s) || ' : ' || round(cap_space / 1e6, 2) || ' M$ (relevé du ' || to_char(captured_at at time zone 'Europe/Paris', 'DD/MM') || ')'
from silver.hn_cap_now where cap_space < 2000000
union all
select 2, '🟧 IMPORTANT', 'scouting',
       'Scouts : ' || num_scouts || ' sur ' || max_scouts || ' possibles (relevé du ' || to_char(day, 'DD/MM') || ')'
from (select * from silver.hn_scouting_budget order by day desc limit 1) b where num_scouts < max_scouts
union all
select 2, '🟧 IMPORTANT', 'export', 'Export ' || ecran || ' : ' || statut || coalesce(' (' || age_h || ' h)', '')
from gold.hn_exports_state where statut <> '🟩 à jour'
union all
select 3, '🟩 SUIVI', 'U21', name || ' (' || age || ' ans, ' || rating || ') : pas de contrat, part à 22 ans'
from silver.hn_players where team_level = 'U21' and age >= 21 and salary is null and not coalesce(frm, false) and next_salary is null
union all
select 3, '🟩 SUIVI', 'effectif', name || ' joue ' || position || ' à contre-emploi (talents ' || talent_strongest::text || ')'
from gold.hn_player_fit where is_main and verdict = 'contre-emploi' and team_level in ('PRO', 'FRM');

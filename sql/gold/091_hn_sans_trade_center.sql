-- 2026-11-25, consigne de l'utilisateur (Hockey Nation) : « je ne veux plus jamais avoir à exporter le Trade Center ».
-- Les écrans Trade Center > offres et > recherche sortent de gold.hn_exports_state (donc des exports demandés, des alertes
-- « exports périmés » de gold.hn_daily_alerts et des listes d'exports de plus de 7 jours) et de core.export_rule (inactifs).
-- La date de fermeture de la fenêtre reste en config (docs/attentes/jeux/hockeynation.yaml, rythme.fenetre_echanges).
create or replace view gold.hn_exports_state with (security_invoker = true) as
with need(ordre, ecran, route, max_age_h, pour_quoi) as (values
  (1, 'Roster PRO, FRM, U21, U17', '/team/:id/roster', 24, 'effectif, talents, contrats'),
  (2, 'Office > Salary cap', '/office/salary-cap-overview', 24, 'cap space avant échange ou signature'),
  (5, 'Lineups PRO', '/team/:id/lineups', 24, 'lignes enregistrées'),
  (6, 'Training (journal)', '/club/:id/training-log', 24, 'entraînement PRO / FRM'),
  (7, 'Coaching staff', '/club/:id/coaching-staff', 48, 'coachs en poste et réponses'),
  (8, 'Scouting staff', '/club/:id/scouting-staff', 48, 'scouts embauchés'),
  (9, 'Scouting budget', '/club/:id/scouting-budget-overview', 48, 'budget de scouting'),
  (10, 'Contract talks', '/club/:id/expiring-players', 72, 'prolongations'),
  (11, 'Club finances', '/club/:id/finances', 72, 'rachats, salaires par saison'),
  (12, 'Draft class', '/league/:id/draft-class', 168, 'rapports des scouts'),
  (13, 'Matchs (programme)', '/club/:id/game-overview', 24, 'résultats et prochains matchs'),
  (14, 'Classement', '/league/:id/standings', 48, 'classement'))
select n.ordre, n.ecran, n.pour_quoi,
  (max(a.captured_at) at time zone 'Europe/Paris') as dernier_paris,
  round(extract(epoch from now() - max(a.captured_at)) / 3600) as age_h,
  case when max(a.captured_at) is null then '🟥 jamais'
       when now() - max(a.captured_at) > make_interval(hours => n.max_age_h) then '🟧 à refaire'
       else '🟩 à jour' end as statut
from need n left join silver.hn_api a on a.route = n.route
group by n.ordre, n.ecran, n.pour_quoi, n.max_age_h
order by n.ordre;

update core.export_rule set actif = false where game = 'hockeynation' and ordre in (3, 4);

-- Team Soccer : agenda du soir et alertes du jour, pour les deux clubs (skill teamsoccer-aujourdhui, checklist F, 2026-10-20).
-- L'utilisateur n'agit que le soir après 19:00 (Paris) : toute action dont la limite tombe avant 19:00 se fait la veille au soir.
-- Composition à enregistrer au moins 2 h avant le coup d'envoi (match pré-calculé) [skill teamsoccer-match].
-- Rythme : lundi 00:05 clôture financière et remise à zéro de la limite d'achat, vendredi ~00:00–01:00 UTC entraînement,
-- 3 révélations d'académie par jour (01:00 UTC), un amical par semaine [skill teamsoccer-saison].
-- Les jours de match viennent des données (silver.ts_matches), pas de la règle « mardi et samedi » : Ben Ahmed joue le lundi et le jeudi [Obs].

-- Gold : agenda de ce soir et de demain soir, une ligne par action.
create or replace view gold.ts_agenda with (security_invoker = true) as
with t as (select (now() at time zone 'Europe/Paris')::date as today),
m as (
  select u.*, u.lineup_deadline_paris::date as dl_day,
         case when u.lineup_deadline_paris::time >= time '19:00' then u.lineup_deadline_paris::date
              else u.lineup_deadline_paris::date - 1 end as prep_day,
         case u.competition when 'ligue' then 'ligue' when 'coupe' then 'coupe' when 'amical' then 'amical'
              when 'barrage' then 'barrage' else 'match de type inconnu' end as tag
  from gold.ts_upcoming u
),
days as (select today as day from t union all select today + 1 from t),
amical_done as (
  select my_team_id as team_id, date_trunc('week', match_date_paris)::date as week
  from silver.ts_matches where competition = 'amical' group by 1, 2
),
ev(day, team, priority, category, action) as (
  -- Composition de chaque match, à enregistrer le soir où la limite (coup d'envoi − 2 h) est encore atteignable.
  select m.prep_day, m.team, case when m.lineup_saved then 3 else 1 end, 'composition',
         case when m.prep_day < m.match_date_paris::date then 'Pour ' || case when m.match_date_paris::date = m.prep_day + 1 then 'demain' else to_char(m.match_date_paris, 'DD/MM') end
              else 'Ce soir' end
         || ' (' || m.tag || ', ' || coalesce(m.venue, '?') || ', contre ' || coalesce(m.opponent, '?')
         || case when m.opponent_is_bot then ', bot' when m.opponent_is_bot = false then ', humain' else '' end || ') : '
         || case when m.lineup_saved then 'composition déjà enregistrée (' || coalesce(m.saved_formation, '?') || '), à revoir seulement si Forme ou blessure ont changé'
                 else 'enregistrer la composition (agent Tactique)' end
         || case when m.tag = 'match de type inconnu' then ' ; vérifier dans la page Matchs de quoi il s''agit' else '' end
  from m
  union all
  -- Export de chaque match joué le jour même (le soir).
  select m.match_date_paris::date, m.team, 2, 'export',
         'Exporter la page du match (' || m.tag || ' contre ' || coalesce(m.opponent, '?') || '), puis agent Match'
  from m where m.tag <> 'amical'
  union all
  -- Lundi : semaine financière close à 00:05, limite d'achat remise à zéro, fenêtre de paiement HPC.
  select d.day, 'les deux clubs', 1, 'finances',
         'Lundi : exporter Finances et Stade (semaine close), contrôler l''entretien du stade (bug déjà vu), puis agent Finances ; limite d''achat remise à zéro ; paiement HPC possible'
  from days d where extract(isodow from d.day) = 1
  union all
  -- Vendredi : entraînement de la nuit, nouvelles compétences et Forme.
  select d.day, 'les deux clubs', 1, 'entrainement',
         'Vendredi : exporter Effectif et Entraînement (entraînement de la nuit), puis agent Entraînement'
  from days d where extract(isodow from d.day) = 5
  union all
  -- Chaque soir : révélations d'académie (ce soir, seulement les clubs qui en ont encore).
  select (select today from t), a.team, 2, 'académie',
         'Révéler ' || max(a.team_reveals_left_today) || ' compétence(s) à l''académie, puis exporter la page Académie'
  from gold.ts_academy a group by a.team having max(a.team_reveals_left_today) > 0
  union all
  select (select today from t) + 1, 'les deux clubs', 2, 'académie',
         'Révéler les compétences du jour à l''académie (3 par club), puis exporter la page Académie'
  union all
  -- Amical de la semaine, si aucun n'est encore joué ni prévu (impossible tant que le club est en Coupe Nationale [skill teamsoccer-saison]).
  select d.day, mt.name, 3, 'amical',
         'Pas encore d''amical cette semaine : en lancer un si le club n''est plus en Coupe Nationale (tests de postes ou de jeunes)'
  from days d cross join silver.ts_my_teams mt
  where d.day = (select today from t)
    and not exists (select 1 from amical_done a where a.team_id = mt.team_id and a.week = date_trunc('week', d.day)::date)
    and not exists (select 1 from m where m.team_id = mt.team_id and m.tag = 'amical' and date_trunc('week', m.match_date_paris) = date_trunc('week', d.day))
)
select ev.day,
       (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from ev.day)::int] || ' ' || to_char(ev.day, 'DD/MM') as day_label,
       ev.team, ev.priority, ev.category, ev.action
from ev, t
where ev.day between t.today and t.today + 1
order by ev.day, ev.priority, ev.team;

-- Gold : alertes du jour (blessures et cartons, compositions manquantes, finances, HPC, académie, exports en retard).
create or replace view gold.ts_daily_alerts with (security_invoker = true) as
with last_cap(kind, endpoint, max_age) as (
  values ('Effectif (players)', 'players', interval '24 hours'),
         ('Matchs (calendrier)', 'matches', interval '24 hours'),
         ('Marché (transfer_listings)', 'transfer_listings', interval '24 hours'),
         ('Académie', 'youth_academy_players', interval '24 hours'),
         ('Finances', 'team_finances', interval '7 days')
),
caps as (
  select l.kind, l.max_age, max(a.captured_at) as last_at
  from last_cap l left join silver.ts_api a on a.endpoint = l.endpoint
  group by l.kind, l.max_age
),
in_season as (select exists (select 1 from silver.ts_matches where status = 'scheduled' and match_date > now()) as yes)
select 1 as priority, mt.name as team, 'blessure' as category,
       p.name || ' (' || p.position || ') ' || case when p.injury_days > 0 then 'blessé, ' || p.injury_days || ' j' else 'suspendu' end
         || ' au relevé du ' || to_char(p.as_of, 'DD/MM') as alert
from silver.ts_players p join silver.ts_my_teams mt on mt.team_id = p.team_id
where p.injury_days > 0 or p.suspended
union all
select 2, mt.name, 'cartons', p.name || ' (' || p.position || ') a 2 jaunes : un de plus = suspendu [skill teamsoccer-joueurs]'
from silver.ts_players p join silver.ts_my_teams mt on mt.team_id = p.team_id
where p.yellow_cards = 2 and not p.suspended
union all
select 1, u.team, 'composition',
       'Composition non enregistrée : ' || u.competition || ' contre ' || coalesce(u.opponent, '?') || ' le ' || to_char(u.match_date_paris, 'DD/MM HH24:MI')
         || ' (limite ' || to_char(u.lineup_deadline_paris, 'DD/MM HH24:MI') || ')'
from gold.ts_upcoming u
where not u.lineup_saved and u.lineup_deadline_paris < (now() at time zone 'Europe/Paris') + interval '36 hours'
union all
select 1, f.team, 'finances', 'Solde négatif : ' || f.balance || ' $ (ni achat, ni stade, ni entraîneur) [skill teamsoccer-club]'
from gold.ts_finance_status f where f.alert_negative
union all
select 1, f.team, 'finances', 'Entretien du stade facturé ' || f.stadium_maintenance || ' $ au lieu de ' || f.maintenance_expected || ' $ : écrire au forum pour remboursement'
from gold.ts_finance_status f where f.maintenance_gap > 0
union all
select 2, h.team, 'HPC', 'Haute Performance : il manque ' || h.tsc_needed || ' TSC pour atteindre 50 (compte : ' || h.account_tsc || ', lundis restants : ' || coalesce(h.mondays_left::text, '?') || ')'
from gold.ts_hpc_status h where h.tsc_needed > 0
union all
select 2, a.team, 'académie', 'Révélations du jour non faites : ' || max(a.team_reveals_left_today) || ' sur 3'
from gold.ts_academy a group by a.team having max(a.team_reveals_left_today) > 0
union all
select 2, mt.name, 'match', 'Match joué non exporté : ' || m.competition || ' du ' || to_char(m.match_date_paris, 'DD/MM') || ' contre ' || coalesce(case when m.venue = 'domicile' then m.away_team else m.home_team end, '?')
from silver.ts_matches m join silver.ts_my_teams mt on mt.team_id = m.my_team_id
where m.competition not in ('amical', 'autre') and m.match_date < now() - interval '2 hours' and m.match_date > now() - interval '8 days'
  and not exists (select 1 from silver.ts_match_events e where e.match_id = m.match_id)
union all
select 3, null, 'export', c.kind || ' : dernier export le ' || coalesce(to_char(c.last_at at time zone 'Europe/Paris', 'DD/MM HH24:MI'), 'jamais')
from caps c cross join in_season s
where s.yes and (c.last_at is null or c.last_at < now() - c.max_age);

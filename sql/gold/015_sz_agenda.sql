-- SixZero League : calendrier officiel, agenda du soir et alertes du jour (skill sixzeroleague-aujourdhui, checklist F, 2026-10-19).
-- Source du calendrier : /seasons/current (steps : chaque journée de ligue et tour de coupe avec scheduledAt), adversaires :
-- silver.sz_fixtures (ligue) et /cups/current (coupe, terrain neutre [W:Competitions]).
-- L'utilisateur n'agit que le soir après 19:00 (Paris) : un match avant 19:00 se prépare la veille au soir.
-- Cycle réglé chaque soir après le match de 21:00 (Paris) [Dev chat] ; annonces closes au coup d'envoi suivant [Dev chat].

-- Silver : calendrier de la saison, une ligne par étape (journée de ligue ou tour de coupe), avec mon match s'il existe.
create or replace view silver.sz_schedule with (security_invoker = true) as
with s as (select captured_at, body from silver.sz_api where endpoint = '/seasons/current' order by captured_at desc limit 1),
st as (
  select (x->>'stepIndex')::int as step_index, x->>'label' as label, x->>'competitionType' as competition,
         (x->>'roundNumber')::int as round, (x->>'scheduledAt')::timestamptz as scheduled_at, x->>'status' as status,
         s.captured_at
  from s, jsonb_array_elements(s.body->'steps') x
),
cup as (
  select r.ord::int as round, t->>'status' as tie_status, (t->>'matchId')::uuid as match_id,
         case when (t->>'homeTeamId')::uuid = me.team_id then t->>'awayTeamName' else t->>'homeTeamName' end as opponent,
         (t->>'winnerTeamId')::uuid = me.team_id as won
  from (select body from silver.sz_api where endpoint = '/cups/current' order by captured_at desc limit 1) c
  cross join silver.sz_my_team me
  cross join lateral jsonb_array_elements(c.body->'rounds') with ordinality r(v, ord)
  cross join lateral jsonb_array_elements(r.v->'ties') t
  where me.team_id in ((t->>'homeTeamId')::uuid, (t->>'awayTeamId')::uuid)
)
select st.step_index, st.label, st.competition, st.round, st.scheduled_at,
       st.scheduled_at at time zone 'Europe/Paris' as kickoff_paris, st.status, st.captured_at,
       coalesce(f.match_id, cup.match_id) as match_id,
       case when st.competition = 'league' then case when f.home_team_id = me.team_id then f.away_team else f.home_team end
            else cup.opponent end as opponent,
       case when st.competition = 'cup' then 'neutre' when f.home_team_id = me.team_id then 'domicile' when f.match_id is not null then 'extérieur' end as venue,
       case when f.home_team_id = me.team_id then f.away_is_bot else f.home_is_bot end as opponent_is_bot,
       cup.tie_status, cup.won as cup_won,
       (f.match_id is not null or (cup.match_id is not null)) as i_play
from st
cross join silver.sz_my_team me
left join silver.sz_fixtures f on st.competition = 'league' and f.is_mine and f.round = st.round
left join cup on st.competition = 'cup' and cup.round = st.round;

-- Gold : agenda d'aujourd'hui et de demain, heures de Paris, seulement les actions faisables le soir.
create or replace view gold.sz_agenda with (security_invoker = true) as
with m as (
  select *, kickoff_paris::date as kday, kickoff_paris::time as ktime,
         case when competition = 'league' then 'J' || round else 'Coupe T' || round end as tag
  from silver.sz_schedule
  where i_play and status <> 'complete' and kickoff_paris::date between current_date and current_date + 1
),
evenings as (select distinct kday as day from m where ktime >= time '19:00'),
ev(day, at_time, priority, category, action) as (
  -- Préparer chaque match : avant le coup d'envoi s'il est le soir, sinon la veille au soir.
  select case when ktime >= time '19:00' then kday else kday - 1 end,
         case when ktime >= time '19:00' then (kickoff_paris - interval '15 minutes')::time else time '22:15' end,
         1, 'tactique',
         case when ktime >= time '19:00' then 'Avant ' || to_char(kickoff_paris, 'HH24:MI') else 'Ce soir, pour demain ' || to_char(kickoff_paris, 'HH24:MI') || ' (tu ne seras pas là)' end
         || ' : tactique par défaut (Équipe → Tactique) pour ' || tag || ' contre ' || coalesce(opponent, '?')
         || ' (' || coalesce(venue, '?') || case when opponent_is_bot then ', bot' when opponent_is_bot = false then ', humain' else '' end || ')'
  from m
  union all
  -- Exporter chaque match une fois joué (le soir au plus tôt).
  select kday, greatest((kickoff_paris + interval '1 hour')::time, time '19:00'), 2, 'export',
         'Exporter la page du match ' || tag || ' contre ' || coalesce(opponent, '?') || ' (puis agent Match)'
  from m
  union all
  -- Chaque soir de match à 21:00 : exports avant le coup d'envoi, puis après le règlement du cycle.
  select day, time '20:30', 2, 'export', 'Avant 21:00 : exporter Équipe (Players, Tactique) et Transferts (annonces closes au coup d''envoi), puis agents Tactique et Transferts' from evenings
  union all
  select day, time '22:00', 1, 'cycle', 'Après le match de 21:00 (cycle réglé) : exporter Finances et Entraînement, puis agents Entraînement et Finances ; entraînement à saisir avant le prochain cycle' from evenings
)
select day,
       (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from day)::int] || ' ' || to_char(day, 'DD/MM') as day_label,
       at_time, priority, category, action
from ev
where day >= current_date
order by day, at_time, priority;

-- Gold : alertes du jour (blessés, profondeur, finances, sponsor, académie, exports en retard ou manquants).
create or replace view gold.sz_daily_alerts with (security_invoker = true) as
with last_cap(kind, endpoint_re, max_age) as (
  values ('Joueurs (Équipe → Players)', '^/teams/mine/players$', interval '24 hours'),
         ('Transferts', '^/transfers$', interval '12 hours'),
         ('Finances', '^/finances/mine$', interval '24 hours'),
         ('Entraînement (rapport)', '^/teams/mine/training/report$', interval '24 hours'),
         ('Calendrier (League)', '^/seasons/current$', interval '24 hours')
),
caps as (
  select l.kind, l.max_age, max(a.captured_at) as last_at
  from last_cap l left join silver.sz_api a on a.endpoint ~ l.endpoint_re
  group by l.kind, l.max_age
),
in_season as (select exists (select 1 from silver.sz_schedule where status <> 'complete') as yes)
select 1 as priority, 'blessure' as category,
       p.name || ' (' || p.role || ') ' || case when p.injured then 'blessé' else 'suspendu' end || ' au relevé du ' || to_char(p.as_of, 'DD/MM') as alert
from silver.sz_players p where p.injured or p.suspended
union all
select 1, 'effectif', r.slot || ' : ' || r.name || ' sans remplaçant naturel (blessure = joueur hors poste)'
from gold.sz_role_report r where r.rank_in_slot = 1 and r.no_natural_backup
union all
select 2, 'effectif', p.name || ' (' || p.role || ', ' || p.age || ' ans) a annoncé sa retraite : encore une saison, invendable'
from silver.sz_players p where p.retiring
union all
select 1, 'finances', 'Prévision du cycle déficitaire : ' || fc_net || ' € ; fin de saison sans victoire : ' || end_balance_no_wins || ' €'
from gold.sz_finance_projection where fc_net < 0 or end_balance_no_wins < 0
union all
select 2, 'sponsor', 'Choix du sponsor ouvert (agent Finances)' from gold.sz_finance_projection where sponsor_can_choose
union all
select 2, 'académie', 'Prospects U18 disponibles (agent Académie)' from silver.sz_u18 where available
union all
select 3, 'export', c.kind || ' : dernier export le ' || coalesce(to_char(c.last_at at time zone 'Europe/Paris', 'DD/MM HH24:MI'), 'jamais')
from caps c cross join in_season s
where s.yes and (c.last_at is null or c.last_at < now() - c.max_age)
union all
select 2, 'match', 'Match joué non exporté : ' || case when s.competition = 'league' then 'J' else 'Coupe T' end || s.round || ' contre ' || coalesce(s.opponent, '?')
from silver.sz_schedule s
where s.i_play and s.match_id is not null and s.scheduled_at < now() - interval '1 hour'
  and not exists (select 1 from silver.sz_match_stats_raw r where r.match_id = s.match_id)
union all
select 3, 'match', 'Dernier match exporté : J' || m.round || ' ' || m.result || ' ' || m.goals || '-' || m.opp_goals || ' contre ' || m.opponent
from (select * from silver.sz_matches order by match_day desc nulls last, round desc nulls last limit 1) m;

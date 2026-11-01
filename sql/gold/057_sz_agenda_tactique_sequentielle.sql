-- SixZero League : agenda corrigé (2026-11-01, remarque de l'utilisateur).
-- 1) La tactique d'un match ne se saisit qu'une fois le match précédent joué (J2 impossible avant J1) : la ligne « tactique »
--    de Jn est datée après le coup d'envoi de J(n-1) [déclaré par l'utilisateur 2026-11-01] ; J1 (pas de match avant) reste la veille.
-- 2) L'entraînement du soir de match est une action très importante (priorité 1) : exporter le rapport, agent Entraînement, plan saisi avant le cycle de 21:00.
create or replace view gold.sz_agenda with (security_invoker = true) as
with m as (
  select s.*, s.kickoff_paris::date as kday, s.kickoff_paris::time as ktime,
         case when s.competition = 'league' then 'J' || s.round else 'Coupe T' || s.round end as tag,
         p.kickoff_paris as prev_kickoff
  from silver.sz_schedule s
  left join silver.sz_schedule p on s.competition = 'league' and p.competition = 'league' and p.round = s.round - 1
  where s.i_play and s.status <> 'complete' and s.kickoff_paris::date between current_date and current_date + 1
),
evenings as (select distinct kday as day from m where ktime >= time '19:00'),
ev(day, at_time, priority, category, action) as (
  -- Tactique de Jn : après le match précédent (saisie impossible avant) ; J1 / coupe : avant le coup d'envoi, la veille si le match est avant 19:00.
  select case when prev_kickoff is not null then prev_kickoff::date when ktime >= time '19:00' then kday else kday - 1 end,
         case when prev_kickoff is not null and prev_kickoff::date < kday then (prev_kickoff + interval '75 minutes')::time
              when prev_kickoff is not null then least(greatest((prev_kickoff + interval '75 minutes')::time, time '19:00'), (kickoff_paris - interval '15 minutes')::time)
              when ktime >= time '19:00' then (kickoff_paris - interval '15 minutes')::time else time '22:15' end,
         1, 'tactique',
         case when prev_kickoff is not null then 'Une fois J' || (round - 1) || ' joué' else 'Avant le coup d''envoi' end
         || ' : tactique (Équipe → Tactique) pour ' || tag || ' contre ' || coalesce(opponent, '?') || ' le ' || to_char(kickoff_paris, 'DD/MM HH24:MI')
         || ' (' || coalesce(venue, '?') || case when opponent_is_bot then ', bot' when opponent_is_bot = false then ', humain' else '' end || ')'
         || case when prev_kickoff is not null and prev_kickoff::date < kday then ' : tu ne seras pas là le lendemain' else '' end
  from m
  where competition = 'league'
  union all
  -- Exporter chaque match une fois joué (le soir au plus tôt).
  select kday, greatest((kickoff_paris + interval '1 hour')::time, time '19:00'), 2, 'export',
         'Exporter la page du match ' || tag || ' contre ' || coalesce(opponent, '?') || ' (puis agent Match)'
  from m
  union all
  -- Chaque soir de match à 21:00 : exports avant le coup d'envoi.
  select day, time '20:30', 2, 'export', 'Avant 21:00 : exporter Équipe (Players, Tactique) et Transferts (annonces closes au coup d''envoi), puis agents Tactique et Transferts' from evenings
  union all
  -- Entraînement : très important, rapport exporté puis plan saisi avant le cycle.
  select day, time '19:30', 1, 'entraînement', 'TRÈS IMPORTANT : exporter l''Entraînement (rapport), agent Entraînement, puis saisir le plan avant le cycle de 21:00' from evenings
  union all
  select day, time '22:00', 1, 'cycle', 'Après le match de 21:00 (cycle réglé) : exporter Finances, puis agent Finances' from evenings
)
select day,
       (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from day)::int] || ' ' || to_char(day, 'DD/MM') as day_label,
       at_time, priority, category, action
from ev
where day >= current_date
order by day, at_time, priority;

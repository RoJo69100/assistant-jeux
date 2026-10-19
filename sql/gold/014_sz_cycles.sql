-- SixZero League : relevé par cycle, bilan par rôle, progression par cycle, finances par cycle (checklist C, 2026-10-19).
-- Cycle (« semaine » du jeu) = 2 journées de ligue, réglé chaque soir après le match de 21:00 (Paris) [W:Finances, Dev chat].
-- weekNumber repart à 1 à chaque saison : un cycle est identifié par son applied_at, pas par son numéro.

-- Silver : rapports d'entraînement, un rang par cycle (applied_at) et par point franchi ; match_share ajouté.
create or replace view silver.sz_training_changes with (security_invoker = true) as
select distinct on ((a.body->>'appliedAt'), (p->>'playerId'), (c->>'skill'))
       (a.body->>'weekNumber')::int as week_number, (a.body->>'appliedAt')::timestamptz as applied_at,
       (p->>'playerId')::uuid as player_id, p->>'name' as name, p->>'role' as role,
       c->>'skill' as skill, (c->>'before')::int as value_before, (c->>'after')::int as value_after,
       (p->>'overallBefore')::int as overall_before, (p->>'overallAfter')::int as overall_after,
       (c->>'matchShare')::numeric as match_share
from silver.sz_api a, jsonb_array_elements(a.body->'players') p, jsonb_array_elements(p->'changes') c
where a.endpoint = '/teams/mine/training/report'
order by (a.body->>'appliedAt'), (p->>'playerId'), (c->>'skill'), a.captured_at desc;

-- Silver : relevé des joueurs par cycle. Un relevé (sz_player_snapshots) est rattaché au dernier cycle réglé avant lui.
create or replace view silver.sz_player_cycles with (security_invoker = true) as
with cycles as (select distinct applied_at, week_number from silver.sz_training_changes)
select s.day, s.captured_at, c.week_number as after_week, c.applied_at as after_cycle,
       s.player_id, s.name, s.role, s.age, s.overall, s.wage, s.injured, s.suspended, s.retiring,
       s.attributes, s.role_overalls, s.training_progress
from silver.sz_player_snapshots s
left join lateral (select * from cycles c where c.applied_at <= s.captured_at order by c.applied_at desc limit 1) c on true;

-- Gold : bilan par rôle. Joueurs sans pénalité à chaque rôle (gold.sz_lineup_natural), compétences clés du rôle
-- [W:Attributes, skill sixzeroleague-joueurs], profondeur disponible et salaire par point de note.
create or replace view gold.sz_role_report with (security_invoker = true) as
with keys(slot, skills) as (values
  ('GK', array['reflexes','oneOnOne','positioning','handling','distribution']),
  ('CB', array['passing','technique','offTheBall','shooting']),
  ('LB', array['shooting','jumping','technique','passing']),
  ('RB', array['shooting','jumping','technique','passing']),
  ('LW', array['speed','agility','shooting','ballControl']),
  ('RW', array['speed','agility','shooting','ballControl']),
  ('P',  array['strength','ballControl','offTheBall','shooting'])
),
n as (select l.*, count(*) filter (where not l.unavailable) over (partition by l.slot) as available_depth from gold.sz_lineup_natural l)
select n.ord, n.slot, n.rank_in_slot, n.name, n.primary_role, n.rating, n.age, p.wage,
       round(p.wage::numeric / nullif(n.rating, 0), 1) as wage_per_point,
       n.unavailable, n.available_depth, n.available_depth < 2 as no_natural_backup,
       (select round(avg((p2.attributes->>k)::int), 1) from unnest(keys.skills) k) as key_skills_avg,
       (select jsonb_object_agg(k, (p2.attributes->>k)::int) from unnest(keys.skills) k) as key_skills,
       p.retiring, p.as_of
from n
join keys on keys.slot = n.slot
join silver.sz_players p on p.player_id = n.player_id
join lateral (select attributes from silver.sz_player_snapshots s where s.player_id = n.player_id order by s.captured_at desc limit 1) p2 on true
order by n.ord, n.rank_in_slot;

-- Gold : progression par cycle et par joueur (points franchis, dont compétences clés de son rôle principal).
create or replace view gold.sz_training_progress with (security_invoker = true) as
with keys(role, skills) as (values
  ('GK', array['reflexes','oneonone','positioning','handling','distribution']),
  ('CB', array['passing','technique','offtheball','shooting']),
  ('LB', array['shooting','jumping','technique','passing']),
  ('RB', array['shooting','jumping','technique','passing']),
  ('LW', array['speed','agility','shooting','ballcontrol']),
  ('RW', array['speed','agility','shooting','ballcontrol']),
  ('P',  array['strength','ballcontrol','offtheball','shooting'])
)
select c.applied_at, c.week_number, c.player_id, c.name, c.role,
       sum(c.value_after - c.value_before) as points,
       coalesce(sum(c.value_after - c.value_before) filter (where lower(replace(c.skill, ' ', '')) = any(k.skills)), 0) as key_points,
       max(c.overall_after) - max(c.overall_before) as overall_gain,
       string_agg(c.skill || ' ' || c.value_before || '→' || c.value_after, ', ' order by c.skill) as detail
from silver.sz_training_changes c
left join keys k on k.role = c.role
group by c.applied_at, c.week_number, c.player_id, c.name, c.role
order by c.applied_at desc, points desc;

-- Gold : résultat de chaque cycle réglé (lastReport) et projection de fin de saison (9 cycles par saison, hypothèse de 013).
create or replace view gold.sz_finance_cycles with (security_invoker = true) as
select distinct on (f.last_report->>'appliedAt')
       (f.last_report->>'appliedAt')::timestamptz as applied_at, f.last_week as week_number,
       (f.last_report->>'openingBalance')::int as opening_balance, (f.last_report->>'closingBalance')::int as closing_balance,
       (f.last_report->>'revenue')::int as revenue, (f.last_report->>'expenses')::int as expenses,
       (f.last_report->>'wages')::int as wages, f.last_net as net,
       (f.last_report->>'ticketRevenue')::int + coalesce((f.last_report->>'arenaTicketBonus')::int, 0) as tickets,
       (f.last_report->>'fanShopRevenue')::int as fan_shop,
       (f.last_report->>'sponsorRevenue')::int + (f.last_report->>'sponsorWinBonus')::int as sponsor,
       (f.last_report->>'leaguePrizeRevenue')::int + (f.last_report->>'cupPrizeRevenue')::int as prizes,
       (f.last_report->>'facilityMaintenance')::int as maintenance,
       (f.last_report->>'infrastructureSpend')::int as infrastructure_spend,
       (f.last_report->>'transferNet')::int as transfer_net,
       f.last_report->'weeksApplied' as weeks_applied
from silver.sz_finances f
where f.last_report is not null
order by f.last_report->>'appliedAt', f.day desc;

-- Projection : solde actuel + prévision du cycle en cours × cycles restants (sans prime de victoire, sans coupe, sans transfert),
-- puis avec les primes de victoire au rythme actuel de la ligue (silver.sz_standings).
create or replace view gold.sz_finance_projection with (security_invoker = true) as
with f as (select * from silver.sz_finances order by day desc limit 1),
st as (select played, wins from silver.sz_standings where is_mine),
r as (select f.*, 9 - (f.forecast->>'weekNumber')::int + 1 as cycles_left from f)
select r.day, r.balance, (r.forecast->>'weekNumber')::int as current_week, r.cycles_left,
       r.fc_revenue, r.fc_expenses, r.fc_wages, r.fc_net,
       round(100.0 * r.fc_wages / nullif(r.fc_revenue, 0), 1) as wages_pct_revenue,
       r.balance + r.fc_net * r.cycles_left as end_balance_no_wins,
       round(coalesce(st.wins::numeric / nullif(st.played, 0), 0.5) * 2 * r.cycles_left) as expected_wins_left,
       r.balance + r.fc_net * r.cycles_left
         + round(coalesce(st.wins::numeric / nullif(st.played, 0), 0.5) * 2 * r.cycles_left) * (r.forecast->>'sponsorWinBonusPerWin')::int as end_balance_with_wins,
       r.sponsor, r.sponsor_can_choose
from r left join st on true;

-- Hockey Nation : correctifs du 2026-10-25 (brief lecteur-exports du jour).
-- 1) silver.hn_players ne garde que les joueurs présents dans le dernier relevé de leur équipe (9 fantômes le 2026-10-25) ;
--    les absents passent dans silver.hn_players_gone (échangé, libéré, retraité, monté d'équipe sans relevé).
-- 2) silver.hn_draft_class gagne la saison de la classe (paramètre ?season= de l'appel ; à défaut, saison en cours).
-- 3) Nouvelles lectures : offres de prolongation, missions et candidatures de scouts, candidatures de coachs, notes d'équipes de la ligue.

create or replace view silver.hn_players with (security_invoker = true) as
with cur as (
  select distinct on (body->>'id') (body->>'id')::uuid as team_id, captured_at
  from silver.hn_api
  where route = '/team/:id/roster' and (body->>'own')::bool
  order by body->>'id', captured_at desc
), last as (
  select distinct on (s.player_id) s.* from silver.hn_player_snapshots s order by s.player_id, s.day desc, s.captured_at desc
)
select l.player_id, l.name, l.team_level, l.team_id, l.age, l.rating, l.xp, l.skater, l.main_position, l.positions,
       n.name as nation, l.draft_rank,
       silver.hn_skill(l.skills, 'SKA') as ska, silver.hn_skill(l.skills, 'END') as endu, silver.hn_skill(l.skills, 'PWR') as pwr,
       silver.hn_skill(l.skills, 'SHO') as sho, silver.hn_skill(l.skills, 'PAS') as pas, silver.hn_skill(l.skills, 'DEF') as def,
       silver.hn_skill(l.skills, 'CHK') as chk, silver.hn_skill(l.skills, 'DSC') as dsc, silver.hn_skill(l.skills, 'FOF') as fof,
       silver.hn_skill(l.skills, 'REF') as ref, silver.hn_skill(l.skills, 'POS') as pos, silver.hn_skill(l.skills, 'PAD') as pad,
       silver.hn_skill(l.skills, 'BLO') as blo, silver.hn_skill(l.skills, 'GLO') as glo, silver.hn_skill(l.skills, 'STK') as stk,
       (select count(*) from jsonb_array_elements(l.skills) s where (s->>'max')::bool) as skills_maxed,
       (select count(*) from jsonb_array_elements(l.skills) s where (s->>'dec')::bool) as skills_declining,
       (select count(*) from jsonb_array_elements(l.skills) s) as skills_total,
       l.talent_strongest, l.talent_weakest, l.special_skills, l.special_skill_count,
       c.salary as salary, c.to_season as contract_to, c.remaining as contract_years_left, c.elc, c.frm,
       nx.salary as next_salary, nx.to_season as next_contract_to,
       l.has_pro_contract, l.expiring, l.tradable, l.on_trade_block, l.retiring, l.day as as_of
from last l
join cur on cur.team_id = l.team_id and cur.captured_at = l.captured_at
left join silver.hn_nations n on n.nation_id = l.nation_id
left join lateral (
  select (x->>'salary')::bigint as salary, (x->>'to')::int as to_season, (x->>'remaining')::int as remaining,
         (x->>'elc')::bool as elc, (x->>'frm')::bool as frm
  from jsonb_array_elements(coalesce(l.contracts, '[]'::jsonb)) x where (x->>'active')::bool limit 1) c on true
left join lateral (
  select (x->>'salary')::bigint as salary, (x->>'to')::int as to_season
  from jsonb_array_elements(coalesce(l.contracts, '[]'::jsonb)) x where not coalesce((x->>'active')::bool, false) order by (x->>'from')::int limit 1) nx on true;

-- Joueurs vus dans nos équipes mais absents du dernier relevé de leur équipe.
create or replace view silver.hn_players_gone with (security_invoker = true) as
with cur as (
  select distinct on (body->>'id') (body->>'id')::uuid as team_id, captured_at
  from silver.hn_api
  where route = '/team/:id/roster' and (body->>'own')::bool
  order by body->>'id', captured_at desc
), last as (
  select distinct on (s.player_id) s.* from silver.hn_player_snapshots s order by s.player_id, s.day desc, s.captured_at desc
)
select l.player_id, l.name, l.team_level as last_team_level, l.age, l.rating, l.main_position, l.day as last_seen
from last l
left join cur on cur.team_id = l.team_id and cur.captured_at = l.captured_at
where cur.team_id is null;

-- Classe de draft : la saison s'ajoute en dernière colonne (S26 et S27 étaient mélangées).
create or replace view silver.hn_draft_class with (security_invoker = true) as
select distinct on (p->>'id') a.day, a.endpoint, (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name,
       (p->>'age')::int as age, (p->>'draftRank')::int as draft_rank, (p->>'rating')::int as rating,
       coalesce((p->>'skater')::bool, not coalesce((p->>'goalie')::bool, false)) as skater, p->'positions'->>0 as main_position,
       (p->>'nationId')::uuid as nation_id, p->'team'->>'city' || ' ' || (p->'team'->>'nickname') as u17_team,
       coalesce((p->'team'->>'own')::bool, false) as from_my_u17,
       (p->>'scoutedTimes')::int as scouted_times, (p->>'canScout')::bool as can_scout,
       p->'talents' as talents, p->'skills' as skills, (p->>'specialSkillCount')::int as special_skill_count,
       p->'specialSkills' as special_skills, p->'tournamentSkaterStats' as stats,
       coalesce(substring(a.query from 'season=(\d+)')::int, (select season from silver.hn_season)) as season
from silver.hn_api a, jsonb_array_elements(a.body->'draftees') p
where a.route = '/league/:id/draft-class'
order by p->>'id', a.captured_at desc;

-- Offres de prolongation en cours (une par joueur, dernier état) et historique des propositions.
create or replace view silver.hn_extension_offers with (security_invoker = true) as
select distinct on (a.endpoint) a.day, a.captured_at,
       substring(a.endpoint from '/player/([0-9a-f-]{36})/')::uuid as player_id, p.name,
       a.body->>'status' as status, a.body->>'mood' as agent_mood,
       (a.body->>'salary')::bigint as salary, (a.body->>'years')::int as years, a.body->'logs' as logs
from silver.hn_api a
left join silver.hn_players p on p.player_id = substring(a.endpoint from '/player/([0-9a-f-]{36})/')::uuid
where a.route in ('/player/:id/new-extension-offer', '/player/:id/contract-extension-talks')
order by a.endpoint, a.captured_at desc;

-- Missions de scouting en cours (dernier relevé).
create or replace view silver.hn_scouting_assignments with (security_invoker = true) as
select a.day, (m->>'id')::uuid as assignment_id, (m->>'scoutId')::uuid as scout_id, s.name as scout,
       (m->>'leagueId')::uuid as league_id, (m->>'duration')::int as duration_days,
       (m->>'daysElapsed')::int as days_elapsed, (m->>'daysLeft')::int as days_left
from (select * from silver.hn_api where route = '/club/:id/scouting-assignments' order by captured_at desc limit 1) a,
     jsonb_array_elements(a.body) m
left join silver.hn_scouts s on s.scout_id = (m->>'scoutId')::uuid;

-- Candidatures de scouts (dernier relevé).
create or replace view silver.hn_scout_applications with (security_invoker = true) as
select a.day, (a.body->>'canHire')::bool as can_hire, (x->'scout'->>'id')::uuid as scout_id,
       x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as name, (x->'scout'->>'age')::int as age,
       x->'scout'->>'position' as preferred_position, n.name as nation
from (select * from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
     jsonb_array_elements(a.body->'applications') x
left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid;

-- Candidatures de coachs (anciens joueurs du club, dernier relevé).
create or replace view silver.hn_coach_applications with (security_invoker = true) as
select a.day, (a.body->>'canHire')::bool as can_hire, (x->'coach'->>'id')::uuid as coach_id,
       x->'coach'->>'firstname' || ' ' || (x->'coach'->>'lastname') as name, (x->'coach'->>'age')::int as age,
       (x->'coach'->>'xp')::int as xp, (x->'coach'->>'rating')::int as rating,
       silver.hn_skill(x->'coach'->'skills', 'OFP') as ofp, silver.hn_skill(x->'coach'->'skills', 'DFP') as dfp,
       silver.hn_skill(x->'coach'->'skills', 'BAT') as bat, silver.hn_skill(x->'coach'->'skills', 'PP') as pp,
       silver.hn_skill(x->'coach'->'skills', 'PK') as pk,
       x->'coach'->'skills' as skills, x->'coach'->'talents' as talents, x->'coach'->'specialSkills' as special_skills
from (select * from silver.hn_api where route = '/club/:id/coach-applications' order by captured_at desc limit 1) a,
     jsonb_array_elements(a.body->'formerPlayers') x;

-- Notes des équipes de la ligue (offense, défense, physique, gardien, coaching), dernier relevé par ligue.
create or replace view silver.hn_league_team_ratings with (security_invoker = true) as
select a.day, (a.body->>'id')::uuid as league_id, (t->>'id')::uuid as team_id,
       t->>'city' || ' ' || (t->>'nickname') as team, coalesce((t->>'bot')::bool, false) as bot,
       (t->'ratings'->>'offense')::int as offense, (t->'ratings'->>'defense')::int as defense,
       (t->'ratings'->>'physical')::int as physical, (t->'ratings'->>'goaltending')::int as goaltending,
       (t->'ratings'->>'coaching')::int as coaching
from (select distinct on (endpoint) * from silver.hn_api where route = '/league/:id/team-ratings' order by endpoint, captured_at desc) a,
     jsonb_array_elements(a.body->'groups') g, jsonb_array_elements(g->'teams') t;

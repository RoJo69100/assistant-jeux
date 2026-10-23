-- Silver Hockey Nation (hockey sur glace, hockey-nation.com) : lecture des réponses API capturées (bronze.raw_pages, game = 'hockeynation').
-- Règles : skills hockeynation-* (guide officiel lu le 2026-10-23, « Last updated on September 30, 2026 »).
-- Nos 4 équipes : PRO, FRM (farm), U21, U17 (`own` = true dans l'API). Compétences des joueurs 0–10 [G:Players].
-- Codes de compétence joueur : SKA Skating, END Endurance, PWR Power, SHO Shooting, PAS Passing, DEF Defending, CHK Checking,
-- DSC Discipline, FOF Faceoffs (attaquants) ; gardiens : REF Reflexes, END, POS Positioning, PAD Pads, BLO Blocker, GLO Glove, STK Stick.
-- Coachs : mêmes codes pour l'entraînement + OFP Offensive Play, DFP Defensive Play, BAT Puck Battling, PP Power Play, PK Penalty Kill.

create or replace view silver.hn_api with (security_invoker = true) as
select r.id as capture_id, r.captured_at,
       (r.captured_at at time zone 'Europe/Paris')::date as day,
       regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+/api', '') as endpoint,
       regexp_replace(regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+/api', ''),
                      '[0-9a-f]{8}-[0-9a-f-]{27}', ':id', 'g') as route,
       nullif(split_part(r.source_url, '?', 2), '') as query,
       coalesce(r.payload->'body'->'data', r.payload->'body') as body
from bronze.raw_pages r
where r.game = 'hockeynation' and r.source = 'api' and coalesce((r.payload->>'status')::int, 200) = 200;

-- Saison en cours, phase (pre / regular / post), jours de paie, prochain événement, draft.
create or replace view silver.hn_season with (security_invoker = true) as
select
  (select (body->>'seasonNumber')::int from silver.hn_api where route = '/season-current' order by captured_at desc limit 1) as season,
  (select body->>'phase' from silver.hn_api where route = '/season-phase' order by captured_at desc limit 1) as phase,
  (select body from silver.hn_api where route = '/season-payday' order by captured_at desc limit 1) as payday,
  (select body->>'name' from silver.hn_api where route = '/office/next-event' order by captured_at desc limit 1) as next_event,
  (select (body->>'startDate')::timestamptz from silver.hn_api where route = '/office/next-event' order by captured_at desc limit 1) as next_event_at,
  (select (body->>'deadlineAt')::timestamptz from silver.hn_api where route = '/draft-center/draft' order by captured_at desc limit 1) as draft_deadline_at,
  (select (body->>'scheduledAt')::timestamptz from silver.hn_api where route = '/draft-center/draft' order by captured_at desc limit 1) as draft_at,
  (select (body->>'draftPicksOwnedCount')::int from silver.hn_api where route = '/draft-center/draft' order by captured_at desc limit 1) as draft_picks_owned,
  (select (body->>'timestamp')::timestamptz from silver.hn_api where route = '/trade-center/trade-window' order by captured_at desc limit 1) as trade_window_ts,
  (select max(captured_at) from silver.hn_api) as last_capture;

-- Nations (id → nom, rang, palier) et libellés des compétences, depuis /api/world.
create or replace view silver.hn_nations with (security_invoker = true) as
select distinct on (n->>'id') (n->>'id')::uuid as nation_id, n->>'name' as name, n->>'abbr' as abbr,
       (n->>'rank')::int as world_rank, (n->>'tier')::int as tier, (n->>'tierU21')::int as tier_u21
from silver.hn_api a, jsonb_array_elements(a.body->'nations') n
where a.route = '/world'
order by n->>'id', a.captured_at desc;

-- Nos équipes (PRO, FRM, U21, U17) : une ligne par équipe, dernier relevé.
create or replace view silver.hn_my_teams with (security_invoker = true) as
select distinct on (body->>'id') (body->>'id')::uuid as team_id, body->>'level' as level, body->>'city' as city, body->>'nickname' as nickname
from silver.hn_api
where route = '/team/:id/roster' and (body->>'own')::bool
order by body->>'id', captured_at desc;

-- Fonction utilitaire : niveau d'une compétence dans le tableau skills [{id, lvl, max, dec, hidden}].
create or replace function silver.hn_skill(skills jsonb, code text) returns int
language sql immutable as $$
  select (s->>'lvl')::int from jsonb_array_elements(coalesce(skills, '[]'::jsonb)) s where s->>'id' = code limit 1
$$;

-- Joueurs de nos 4 équipes : un relevé par joueur et par jour (compétences 0–10, talents, contrats, poste).
create or replace view silver.hn_player_snapshots with (security_invoker = true) as
select distinct on (p->>'id', a.day)
       a.day, a.captured_at, (a.body->>'id')::uuid as team_id, a.body->>'level' as team_level,
       (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name, p->>'lastname' as lastname,
       (p->>'age')::int as age, (p->>'rating')::int as rating, (p->>'xp')::int as xp,
       coalesce((p->>'skater')::bool, not coalesce((p->>'goalie')::bool, false)) as skater,
       p->'positions' as positions, p->'positions'->>0 as main_position,
       (p->>'nationId')::uuid as nation_id, (p->>'draftRank')::int as draft_rank,
       p->'skills' as skills, p->'talents' as talents, p->'talents'->'strongest' as talent_strongest, p->'talents'->>'weakest' as talent_weakest,
       p->'specialSkills' as special_skills, (p->>'specialSkillCount')::int as special_skill_count,
       p->'contracts' as contracts, (p->>'hasProContract')::bool as has_pro_contract,
       (p->>'expiring')::bool as expiring, (p->>'tradable')::bool as tradable, (p->>'onTradeBlock')::bool as on_trade_block,
       (p->>'retiring')::bool as retiring, (p->>'scoutedTimes')::int as scouted_times
from silver.hn_api a, jsonb_array_elements(a.body->'players') p
where a.route = '/team/:id/roster' and (a.body->>'own')::bool
order by p->>'id', a.day, a.captured_at desc;

-- Dernier relevé de chaque joueur, compétences à plat + contrat actif et suivant.
create or replace view silver.hn_players with (security_invoker = true) as
with last as (
  select distinct on (player_id) * from silver.hn_player_snapshots order by player_id, day desc, captured_at desc
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
left join silver.hn_nations n on n.nation_id = l.nation_id
left join lateral (
  select (x->>'salary')::bigint as salary, (x->>'to')::int as to_season, (x->>'remaining')::int as remaining,
         (x->>'elc')::bool as elc, (x->>'frm')::bool as frm
  from jsonb_array_elements(coalesce(l.contracts, '[]'::jsonb)) x where (x->>'active')::bool limit 1) c on true
left join lateral (
  select (x->>'salary')::bigint as salary, (x->>'to')::int as to_season
  from jsonb_array_elements(coalesce(l.contracts, '[]'::jsonb)) x where not coalesce((x->>'active')::bool, false) order by (x->>'from')::int limit 1) nx on true;

-- Finances du club PRO : plafond salarial, salaires projetés, buyouts.
create or replace view silver.hn_finances with (security_invoker = true) as
select distinct on (a.day) a.day, a.captured_at, (a.body->>'currentSeasonNum')::int as season,
       a.body->'salaryCap' as salary_cap, a.body->'salaryCapProjection' as salary_cap_projection,
       a.body->'totalProjectedSalary' as total_projected_salary, a.body->'salaries' as salaries,
       a.body->'buyouts' as buyouts, a.body->'rosterContracts' as roster_contracts,
       a.body->'nonRosterContracts' as non_roster_contracts, a.body->'onTheMoveContracts' as on_the_move_contracts
from silver.hn_api a
where a.route = '/club/:id/finances'
order by a.day, a.captured_at desc;

-- Contrats qui expirent (PRO) et pourparlers en cours (agent, humeur, proposition).
create or replace view silver.hn_expiring with (security_invoker = true) as
select distinct on (p->>'id') a.day, a.route, (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name,
       (p->>'age')::int as age, (p->>'rating')::int as rating, p->'positions'->>0 as main_position,
       p->'agent'->>'lastname' as agent, p->'contractTalk'->>'status' as talk_status, p->'contractTalk'->>'mood' as agent_mood,
       (p->'contractTalk'->>'salary')::bigint as asked_salary, (p->'contractTalk'->>'years')::int as asked_years,
       p->'contracts' as contracts
from silver.hn_api a, jsonb_array_elements(a.body) p
where a.route in ('/club/:id/expiring-players', '/club/:id/expiring-prospects', '/club/:id/contract-talks-farm-players')
order by p->>'id', a.captured_at desc;

-- Coachs de nos équipes : compétences d'entraînement (6) et de match (OFP DFP BAT PP PK), talents, compétences spéciales.
create or replace view silver.hn_coaches with (security_invoker = true) as
select distinct on (c->>'id') a.day, k.key as team_level, (c->>'id')::uuid as coach_id,
       c->>'firstname' || ' ' || (c->>'lastname') as name, (c->>'age')::int as age, (c->>'xp')::int as xp,
       coalesce((c->'job'->>'head')::bool, false) as head_coach, (c->'job'->>'from')::int as at_club_since_season,
       (c->>'rating')::int as rating, (c->>'matchRating')::int as match_rating, (c->>'trainingRating')::int as training_rating,
       silver.hn_skill(c->'skills', 'OFP') as ofp, silver.hn_skill(c->'skills', 'DFP') as dfp, silver.hn_skill(c->'skills', 'BAT') as bat,
       silver.hn_skill(c->'skills', 'PP') as pp, silver.hn_skill(c->'skills', 'PK') as pk,
       c->'skills' as skills, c->'talents' as talents, c->'specialSkills' as special_skills, (c->>'nationId')::uuid as nation_id
from silver.hn_api a, jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
where a.route = '/club/:id/coaching-staff'
order by c->>'id', a.captured_at desc;

-- Coachs libres (marché des coachs, /coach-center/search).
create or replace view silver.hn_free_coaches with (security_invoker = true) as
select distinct on (c->>'id') a.day, (c->>'id')::uuid as coach_id, c->>'firstname' || ' ' || (c->>'lastname') as name,
       (c->>'age')::int as age, (c->>'xp')::int as xp, (c->>'rating')::int as rating,
       (c->>'matchRating')::int as match_rating, (c->>'trainingRating')::int as training_rating,
       silver.hn_skill(c->'skills', 'OFP') as ofp, silver.hn_skill(c->'skills', 'DFP') as dfp, silver.hn_skill(c->'skills', 'BAT') as bat,
       silver.hn_skill(c->'skills', 'PP') as pp, silver.hn_skill(c->'skills', 'PK') as pk,
       c->'skills' as skills, c->'talents' as talents, c->'specialSkills' as special_skills,
       (c->>'canOffer')::bool as can_offer, (c->>'nationId')::uuid as nation_id
from silver.hn_api a, jsonb_array_elements(a.body) c
where a.route = '/coach-center/search'
order by c->>'id', a.captured_at desc;

-- Journal d'entraînement : compétence entraînée, coach choisi, vitesse (trainingRate), par équipe.
create or replace view silver.hn_training_log with (security_invoker = true) as
select a.day, a.captured_at, t->>'teamLevel' as team_level, (t->'player'->>'id')::uuid as player_id,
       t->'player'->>'firstname' || ' ' || (t->'player'->>'lastname') as name, (t->'player'->>'age')::int as age,
       t->>'skill' as skill, (t->>'level')::int as skill_level, (t->>'coachId')::uuid as coach_id,
       (t->>'coachLevel')::int as coach_level, (t->>'trainingRate')::int as training_rate
from silver.hn_api a, jsonb_array_elements(a.body) t
where a.route = '/club/:id/training-log';

-- Lignes de l'équipe PRO (A, B, C) : une ligne par poste.
create or replace view silver.hn_lineups with (security_invoker = true) as
select distinct on (l->>'id', ln.key, pos.key) a.day, l->>'id' as lineup, ln.key as line, pos.key as slot,
       (pos.value #>> '{}')::uuid as player_id, l->'gameplan' as gameplan
from silver.hn_api a, jsonb_array_elements(a.body) l, jsonb_each(l->'lines') ln, jsonb_each(ln.value) pos
where a.route = '/team/:id/lineups' and jsonb_typeof(pos.value) = 'string'
order by l->>'id', ln.key, pos.key, a.captured_at desc;

-- Matchs de nos équipes (calendrier terminé et à venir).
create or replace view silver.hn_games with (security_invoker = true) as
select distinct on (g->>'id') (g->>'id')::uuid as game_id, g->>'type' as game_type, (g->>'day')::int as season_day,
       (g->>'scheduledAt')::timestamptz as scheduled_at, g->>'status' as status,
       g->'teams'->'home'->>'city' || ' ' || (g->'teams'->'home'->>'nickname') as home,
       g->'teams'->'away'->>'city' || ' ' || (g->'teams'->'away'->>'nickname') as away,
       (g->>'homeScore')::int as home_score, (g->>'awayScore')::int as away_score, g->'winner' as winner,
       coalesce((g->'teams'->'home'->>'own')::bool, false) as home_is_mine, coalesce((g->'teams'->'away'->>'own')::bool, false) as away_is_mine,
       g->'teams' as teams, a.captured_at
from silver.hn_api a, jsonb_array_elements(a.body) g
where a.route in ('/team/:id/schedule', '/club/:id/game-overview')
order by g->>'id', a.captured_at desc;

-- Détail d'un match : résumé, feuille de match, événements (JSON brut, à analyser par l'agent Match).
create or replace view silver.hn_game_detail with (security_invoker = true) as
select distinct on (a.body->>'id') (a.body->>'id')::uuid as game_id, a.captured_at,
       a.body->'result' as result, a.body->'summary' as summary, a.body->'periods' as periods, a.body->'boxscore' as boxscore,
       a.body->'stars' as stars, a.body->'coaches' as coaches, a.body->'teams' as teams, a.body->'events' as events,
       a.body->'players' as players, (a.body->>'scheduledAt')::timestamptz as scheduled_at
from silver.hn_api a
where a.route = '/game/:id'
order by a.body->>'id', a.captured_at desc;

-- Classement de la ligue.
create or replace view silver.hn_standings with (security_invoker = true) as
select distinct on (a.endpoint) a.day, a.endpoint, a.body->'standing' as standing, a.body->'teams' as teams, a.body->'groups' as groups
from silver.hn_api a
where a.route = '/league/:id/standings'
order by a.endpoint, a.captured_at desc;

-- Échanges récents (Trade Tracker) : un échange par ligne, actifs offerts et reçus en JSON.
create or replace view silver.hn_trades with (security_invoker = true) as
select distinct on (t->>'id') (t->>'id')::uuid as trade_id, (t->>'createdAt')::timestamptz as created_at,
       (t->>'resolvedAt')::timestamptz as resolved_at, (t->>'processedAt')::timestamptz as processed_at,
       t->'teams'->'offering'->>'city' || ' ' || (t->'teams'->'offering'->>'nickname') as offering_team,
       t->'teams'->'receiving'->>'city' || ' ' || (t->'teams'->'receiving'->>'nickname') as receiving_team,
       t->'assets'->'offering' as assets_offering, t->'assets'->'receiving' as assets_receiving,
       t->'salaryImpact' as salary_impact, (t->>'votesApproved')::int as votes_approved,
       (t->>'votesRejectedOffering')::int as votes_rejected_offering, (t->>'votesRejectedReceiving')::int as votes_rejected_receiving
from silver.hn_api a, jsonb_array_elements(a.body) t
where a.route = '/trade-center/trade-tracker'
order by t->>'id', a.captured_at desc;

-- Joueurs disponibles : agents libres et joueurs mis sur le marché des échanges.
create or replace view silver.hn_market_players with (security_invoker = true) as
select distinct on (a.route, p->>'id') a.day, case a.route when '/free-agent-center/search' then 'free_agent' else 'trade_block' end as source,
       (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name, (p->>'age')::int as age,
       (p->>'rating')::int as rating, p->'positions'->>0 as main_position, p->'positions' as positions,
       (p->>'faSalary')::bigint as fa_salary, (p->>'faYears')::int as fa_years,
       p->'team'->>'city' || ' ' || (p->'team'->>'nickname') as team, p->'skills' as skills, p->'talents' as talents,
       p->'specialSkills' as special_skills, (p->>'specialSkillCount')::int as special_skill_count, p->'contracts' as contracts,
       (p->>'nationId')::uuid as nation_id
from silver.hn_api a, jsonb_array_elements(a.body) p
where a.route in ('/free-agent-center/search', '/trade-center/search', '/office/shortlist')
order by a.route, p->>'id', a.captured_at desc;

-- Draft : classe de draft (100 joueurs de 17 ans d'une ligue), nos choix, préférences, scouts et budget.
create or replace view silver.hn_draft_class with (security_invoker = true) as
select distinct on (p->>'id') a.day, a.endpoint, (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name,
       (p->>'age')::int as age, (p->>'draftRank')::int as draft_rank, (p->>'rating')::int as rating,
       coalesce((p->>'skater')::bool, not coalesce((p->>'goalie')::bool, false)) as skater, p->'positions'->>0 as main_position,
       (p->>'nationId')::uuid as nation_id, p->'team'->>'city' || ' ' || (p->'team'->>'nickname') as u17_team,
       coalesce((p->'team'->>'own')::bool, false) as from_my_u17,
       (p->>'scoutedTimes')::int as scouted_times, (p->>'canScout')::bool as can_scout,
       p->'talents' as talents, p->'skills' as skills, (p->>'specialSkillCount')::int as special_skill_count,
       p->'specialSkills' as special_skills, p->'tournamentSkaterStats' as stats
from silver.hn_api a, jsonb_array_elements(a.body->'draftees') p
where a.route = '/league/:id/draft-class'
order by p->>'id', a.captured_at desc;

create or replace view silver.hn_draft_picks with (security_invoker = true) as
select distinct on (p->>'id') a.day, (p->>'id')::uuid as pick_id, (p->>'round')::int as round, (p->>'rank')::int as overall_rank,
       (p->>'leagueId')::uuid as league_id, p->'team'->>'city' || ' ' || (p->'team'->>'nickname') as original_team,
       p->'preference' as preference
from silver.hn_api a, jsonb_array_elements(a.body) p
where a.route in ('/club/:id/draft-picks', '/draft-center/draft-pick-preferences')
order by p->>'id', (a.route = '/draft-center/draft-pick-preferences') desc, a.captured_at desc;

create or replace view silver.hn_scouts with (security_invoker = true) as
select distinct on (s->>'id') a.day, (s->>'id')::uuid as scout_id, s->>'firstname' || ' ' || (s->>'lastname') as name,
       (s->>'age')::int as age, s->>'position' as preferred_position, n.name as nation,
       coalesce((s->'job'->>'head')::bool, false) as head_scout, (s->'job'->'contract'->>'salary')::int as daily_salary
from silver.hn_api a, jsonb_array_elements(a.body) s
left join silver.hn_nations n on n.nation_id = (s->>'nationId')::uuid
where a.route = '/club/:id/scouting-staff'
order by s->>'id', a.captured_at desc;

create or replace view silver.hn_scouting_budget with (security_invoker = true) as
select distinct on (a.day) a.day, (a.body->>'numScouts')::int as num_scouts, (a.body->>'maxScouts')::int as max_scouts,
       (a.body->>'budgetLeft')::bigint as budget_left, (a.body->>'seasonBudget')::bigint as season_budget,
       (a.body->'projections'->>'budgetNextSeason')::bigint as budget_next_season, (a.body->>'headScoutHired')::bool as head_scout_hired
from silver.hn_api a
where a.route = '/club/:id/scouting-budget-overview'
order by a.day, a.captured_at desc;

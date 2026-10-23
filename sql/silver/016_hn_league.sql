-- Silver Hockey Nation : autres clubs (effectifs, staffs, fiches coach), exports du 2026-10-23.
-- Correction : silver.hn_coaches ne garde que nos 4 équipes (les staffs adverses exportés le 2026-10-23 y entraient).

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
  and (a.body->'team'->>'id')::uuid in (select team_id from silver.hn_my_teams)
order by c->>'id', a.captured_at desc;

-- Staffs de tous les clubs exportés (le nôtre et les adversaires), dernier relevé par coach.
create or replace view silver.hn_club_staff with (security_invoker = true) as
select distinct on (c->>'id') a.day, (a.body->'team'->>'id')::uuid as club_id,
       a.body->'team'->>'city' || ' ' || (a.body->'team'->>'nickname') as club,
       (a.body->'team'->>'id')::uuid in (select team_id from silver.hn_my_teams) as own,
       k.key as team_level, (c->>'id')::uuid as coach_id, c->>'firstname' || ' ' || (c->>'lastname') as name,
       (c->>'age')::int as age, (c->>'xp')::int as xp, coalesce((c->'job'->>'head')::bool, false) as head_coach,
       (c->>'rating')::int as rating, (c->>'matchRating')::int as match_rating, (c->>'trainingRating')::int as training_rating,
       silver.hn_skill(c->'skills', 'OFP') as ofp, silver.hn_skill(c->'skills', 'DFP') as dfp, silver.hn_skill(c->'skills', 'BAT') as bat,
       silver.hn_skill(c->'skills', 'PP') as pp, silver.hn_skill(c->'skills', 'PK') as pk,
       c->'talents' as talents, c->'specialSkills' as special_skills, (c->>'nationId')::uuid as nation_id
from silver.hn_api a, jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
where a.route = '/club/:id/coaching-staff'
order by c->>'id', a.captured_at desc;

-- Fiches coach ouvertes une à une (/coach/:id) : nos coachs, ceux des adversaires et du marché.
create or replace view silver.hn_coach_profiles with (security_invoker = true) as
select distinct on (a.body->>'id') a.day, (a.body->>'id')::uuid as coach_id,
       a.body->>'firstname' || ' ' || (a.body->>'lastname') as name, (a.body->>'age')::int as age, (a.body->>'xp')::int as xp,
       (a.body->'team'->>'id')::uuid as team_id, a.body->'team'->>'city' || ' ' || (a.body->'team'->>'nickname') as team,
       a.body->'team'->>'level' as team_level, coalesce((a.body->'team'->>'own')::bool, false) as own,
       (a.body->>'rating')::int as rating, (a.body->>'matchRating')::int as match_rating, (a.body->>'trainingRating')::int as training_rating,
       silver.hn_skill(a.body->'skills', 'OFP') as ofp, silver.hn_skill(a.body->'skills', 'DFP') as dfp, silver.hn_skill(a.body->'skills', 'BAT') as bat,
       silver.hn_skill(a.body->'skills', 'PP') as pp, silver.hn_skill(a.body->'skills', 'PK') as pk,
       a.body->'skills' as skills, a.body->'talents' as talents, a.body->'specialSkills' as special_skills, (a.body->>'nationId')::uuid as nation_id
from silver.hn_api a
where a.route = '/coach/:id'
order by a.body->>'id', a.captured_at desc;

-- Joueurs de tous les effectifs exportés (nos 4 équipes et les adversaires), dernier relevé, contrat actif à plat.
create or replace view silver.hn_league_players with (security_invoker = true) as
select distinct on (p->>'id') a.day, (a.body->>'id')::uuid as team_id, a.body->>'city' || ' ' || (a.body->>'nickname') as team,
       a.body->>'level' as team_level, coalesce((a.body->>'own')::bool, false) as own,
       (p->>'id')::uuid as player_id, p->>'firstname' || ' ' || (p->>'lastname') as name, (p->>'age')::int as age,
       (p->>'rating')::int as rating, (p->>'xp')::int as xp,
       coalesce((p->>'skater')::bool, not coalesce((p->>'goalie')::bool, false)) as skater,
       p->'positions' as positions, p->'positions'->>0 as main_position, (p->>'nationId')::uuid as nation_id,
       p->'skills' as skills, p->'talents'->'strongest' as talent_strongest, p->'talents'->>'weakest' as talent_weakest,
       p->'specialSkills' as special_skills, (p->>'specialSkillCount')::int as special_skill_count,
       c.salary, c.to_season as contract_to, c.remaining as contract_years_left, p->'contracts' as contracts,
       (p->>'tradable')::bool as tradable, (p->>'onTradeBlock')::bool as on_trade_block, (p->>'expiring')::bool as expiring
from silver.hn_api a, jsonb_array_elements(a.body->'players') p
left join lateral (
  select (x->>'salary')::bigint as salary, (x->>'to')::int as to_season, (x->>'remaining')::int as remaining
  from jsonb_array_elements(coalesce(p->'contracts', '[]'::jsonb)) x where (x->>'active')::bool limit 1) c on true
where a.route = '/team/:id/roster'
order by p->>'id', a.captured_at desc;

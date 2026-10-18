-- Silver SixZero League (handball) : lecture des réponses API capturées (bronze.raw_pages, game = 'sixzeroleague').
-- Règles du jeu : skills sixzeroleague-*. Cycle du jeu : tout se règle toutes les 2 journées de ligue [W:Finances].
-- Confidentialité : ne jamais exposer ownerUsername (e-mail des autres managers, masqué par le script depuis la 0.1.3).

create or replace view silver.sz_api with (security_invoker = true) as
select r.id as capture_id, r.captured_at,
       (r.captured_at at time zone 'Europe/Paris')::date as day,
       regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+/api', '') as endpoint,
       nullif(split_part(r.source_url, '?', 2), '') as query,
       r.payload->'body' as body
from bronze.raw_pages r
where r.game = 'sixzeroleague' and r.source = 'api' and (r.payload->>'status')::int = 200;

create or replace view silver.sz_my_team with (security_invoker = true) as
select (body->>'id')::uuid as team_id, body->>'name' as name, (body->>'rating')::numeric as rating, body->>'country' as country
from silver.sz_api where endpoint = '/teams/mine'
order by captured_at desc limit 1;

-- Joueurs : un relevé par joueur et par jour de capture (compétences, progression fractionnaire, note par rôle).
create or replace view silver.sz_player_snapshots with (security_invoker = true) as
select distinct on ((p->>'id'), a.day)
       a.day, a.captured_at,
       (p->>'id')::uuid as player_id, p->>'name' as name, p->>'role' as role, (p->>'number')::int as number,
       (p->>'age')::int as age, (p->>'height')::int as height_cm, p->>'preferredHand' as preferred_hand, p->>'country' as country,
       (p->>'overall')::int as overall, (p->>'wage')::int as wage,
       (p->>'injured')::bool as injured, (p->>'suspended')::bool as suspended, (p->>'retiring')::bool as retiring, (p->>'forSale')::bool as for_sale,
       p->'secondaryRoles' as secondary_roles,
       p->'attributes' as attributes, p->'trainingProgress' as training_progress, p->'roleOveralls' as role_overalls,
       p->'careerStats' as career_stats
from silver.sz_api a, jsonb_array_elements(a.body) p
where a.endpoint = '/teams/mine/players'
order by (p->>'id'), a.day, a.captured_at desc;

-- Dernier relevé de chaque joueur, compétences à plat (échelle 1–100 [W:Attributes]).
create or replace view silver.sz_players with (security_invoker = true) as
select distinct on (s.player_id)
       s.player_id, s.name, s.role, s.number, s.age, s.height_cm, s.preferred_hand, s.overall, s.wage,
       s.injured, s.suspended, s.retiring, s.for_sale, s.secondary_roles,
       (s.attributes->>'workEthic')::int    as work_ethic,
       (s.attributes->>'agility')::int      as agility,      (s.attributes->>'speed')::int        as speed,
       (s.attributes->>'strength')::int     as strength,     (s.attributes->>'jumping')::int      as jumping,
       (s.attributes->>'stamina')::int      as stamina,
       (s.attributes->>'passing')::int      as passing,      (s.attributes->>'shooting')::int     as shooting,
       (s.attributes->>'ballControl')::int  as ball_control, (s.attributes->>'offTheBall')::int   as off_the_ball,
       (s.attributes->>'technique')::int    as technique,
       (s.attributes->>'marking')::int      as marking,      (s.attributes->>'blocking')::int     as blocking,
       (s.attributes->>'anticipation')::int as anticipation, (s.attributes->>'duels')::int        as duels,
       (s.attributes->>'recovery')::int     as recovery,
       (s.attributes->>'reflexes')::int     as reflexes,     (s.attributes->>'oneOnOne')::int     as one_on_one,
       (s.attributes->>'handling')::int     as handling,     (s.attributes->>'distribution')::int as distribution,
       (s.attributes->>'positioning')::int  as positioning,
       s.role_overalls, s.training_progress, s.career_stats, s.day as as_of
from silver.sz_player_snapshots s
order by s.player_id, s.day desc, s.captured_at desc;

-- Tactique par défaut : les 7 de chaque match et un remplaçant par rôle [W:Match, Injuries].
create or replace view silver.sz_tactics with (security_invoker = true) as
select a.day, a.body->>'attackFormation' as attack_formation, a.body->>'defenseFormation' as defense_formation,
       (a.body->>'autoFilled')::bool as auto_filled, a.body->'defenseSpots' as defense_spots,
       x.kind, x.item->>'simulationRole' as slot, (x.item->>'playerId')::uuid as player_id
from (select * from silver.sz_api where endpoint = '/teams/mine/tactics/default' order by captured_at desc limit 1) a
cross join lateral (
  select 'titulaire' as kind, e as item from jsonb_array_elements(a.body->'assignments') e
  union all select 'remplaçant', e from jsonb_array_elements(a.body->'substitutes') e
) x;

-- Plan d'entraînement : intensité d'équipe et focus par joueur [W:Training].
create or replace view silver.sz_training_plan with (security_invoker = true) as
select a.day, a.body->>'intensity' as intensity,
       (p->>'playerId')::uuid as player_id, p->>'group' as focus_group, p->>'skill' as focus_skill
from (select * from silver.sz_api where endpoint = '/teams/mine/training' order by captured_at desc limit 1) a
cross join lateral jsonb_array_elements(a.body->'players') p;

-- Rapports d'entraînement : chaque point franchi, par cycle.
create or replace view silver.sz_training_changes with (security_invoker = true) as
select distinct on ((a.body->>'weekNumber'), (p->>'playerId'), (c->>'skill'))
       (a.body->>'weekNumber')::int as week_number, (a.body->>'appliedAt')::timestamptz as applied_at,
       (p->>'playerId')::uuid as player_id, p->>'name' as name, p->>'role' as role,
       c->>'skill' as skill, (c->>'before')::int as value_before, (c->>'after')::int as value_after,
       (p->>'overallBefore')::int as overall_before, (p->>'overallAfter')::int as overall_after
from silver.sz_api a, jsonb_array_elements(a.body->'players') p, jsonb_array_elements(p->'changes') c
where a.endpoint = '/teams/mine/training/report'
order by (a.body->>'weekNumber'), (p->>'playerId'), (c->>'skill'), a.captured_at desc;

-- Formation à un 2e rôle [W:Training].
create or replace view silver.sz_role_training with (security_invoker = true) as
select a.day, (a.body->>'facilityLevel')::int as facility_level, (a.body->>'weeklyFee')::int as weekly_fee,
       (s->>'slot')::int as slot, (s->>'unlocked')::bool as unlocked, (s->>'unlockLevel')::int as unlock_level,
       s->'occupant'->>'playerName' as player, s->'occupant'->>'primaryRole' as primary_role, s->'occupant'->>'role' as learning_role,
       (s->'occupant'->>'roundsCompleted')::int as rounds_completed, (s->'occupant'->>'totalRounds')::int as total_rounds
from (select * from silver.sz_api where endpoint = '/teams/mine/role-training' order by captured_at desc limit 1) a
cross join lateral jsonb_array_elements(a.body->'slots') s;

-- Finances : un relevé par jour (solde, sponsor, prévision du cycle, dernier rapport) [W:Finances, Sponsors].
create or replace view silver.sz_finances with (security_invoker = true) as
select distinct on (a.day)
       a.day, (a.body->>'balance')::int as balance,
       a.body->'sponsor'->'current'->>'name' as sponsor, (a.body->'sponsor'->'current'->>'weekly')::int as sponsor_weekly,
       (a.body->'sponsor'->'current'->>'leagueWinBonus')::int as sponsor_win_bonus, (a.body->'sponsor'->>'canChoose')::bool as sponsor_can_choose,
       a.body->'sponsor'->'offers' as sponsor_offers,
       (a.body->'forecast'->>'revenue')::int as fc_revenue, (a.body->'forecast'->>'expenses')::int as fc_expenses,
       (a.body->'forecast'->>'net')::int as fc_net, (a.body->'forecast'->>'wages')::int as fc_wages,
       (a.body->'forecast'->>'homeFixtures')::int as fc_home_fixtures, a.body->'forecast' as forecast,
       (a.body->'lastReport'->>'weekNumber')::int as last_week, (a.body->'lastReport'->>'net')::int as last_net,
       a.body->'lastReport' as last_report, a.body->'sinceLastReport' as since_last_report
from silver.sz_api a where a.endpoint = '/finances/mine'
order by a.day, a.captured_at desc;

-- Infrastructures : chaque niveau de chaque installation (dernière capture), effet chiffré tiré du libellé [W:Infrastructure].
create or replace view silver.sz_infrastructure_levels with (security_invoker = true) as
select a.day, f->>'type' as facility, (f->>'level')::int as current_level,
       (l->>'level')::int as level, l->>'effectLabel' as effect_label,
       nullif(regexp_replace(substring(l->>'effectLabel' from '([0-9][0-9,]*)'), ',', '', 'g'), '')::int as effect_value,
       (l->>'weeklyMaintenance')::int as weekly_maintenance,
       (l->>'upgradeCostFromCurrent')::int as upgrade_cost_from_current, l->>'unlock' as unlock
from (select * from silver.sz_api where endpoint = '/infrastructure/mine' order by captured_at desc limit 1) a
cross join lateral jsonb_array_elements(a.body->'facilities') f
cross join lateral jsonb_array_elements(f->'levels') l;

-- Compétition : classement et calendrier de ma ligue (dernière capture) [W:Competitions].
create or replace view silver.sz_standings with (security_invoker = true) as
select a.day, a.body->>'name' as league, (a.body->>'division')::int as division, (a.body->>'currentRound')::int as current_round,
       (a.body->>'totalRounds')::int as total_rounds,
       (s->>'position')::int as position, (s->>'teamId')::uuid as team_id, t->>'name' as team, (t->>'isBot')::bool as is_bot,
       (s->>'played')::int as played, (s->>'wins')::int as wins, (s->>'draws')::int as draws, (s->>'losses')::int as losses,
       (s->>'points')::int as points, (s->>'goalsFor')::int as goals_for, (s->>'goalsAgainst')::int as goals_against,
       (s->>'goalDifference')::int as goal_difference, s->>'form' as form,
       (s->>'teamId')::uuid = (select team_id from silver.sz_my_team) as is_mine
from (select * from silver.sz_api where endpoint = '/seasons/current/my-competition' order by captured_at desc limit 1) a
cross join lateral jsonb_array_elements(a.body->'standings') s
left join lateral (select x from jsonb_array_elements(a.body->'teams') x where x->>'teamId' = s->>'teamId') tt(t) on true;

create or replace view silver.sz_fixtures with (security_invoker = true) as
select a.day, (f->>'round')::int as round, (f->>'matchId')::uuid as match_id, f->>'status' as status,
       f->>'homeTeamName' as home_team, f->>'awayTeamName' as away_team,
       (f->>'homeTeamId')::uuid as home_team_id, (f->>'awayTeamId')::uuid as away_team_id,
       (f->>'homeScore')::int as home_score, (f->>'awayScore')::int as away_score,
       (f->>'homeTeamIsBot')::bool as home_is_bot, (f->>'awayTeamIsBot')::bool as away_is_bot,
       me.team_id in ((f->>'homeTeamId')::uuid, (f->>'awayTeamId')::uuid) as is_mine
from (select * from silver.sz_api where endpoint = '/seasons/current/my-competition' order by captured_at desc limit 1) a
cross join lateral jsonb_array_elements(a.body->'rounds') r
cross join lateral jsonb_array_elements(r->'fixtures') f
cross join silver.sz_my_team me;

-- Marché des transferts : chaque annonce vue, dernière capture (compétences visibles quand le joueur est en vente [W:Transfers]).
create or replace view silver.sz_transfer_listings with (security_invoker = true) as
select distinct on (l->>'id')
       a.captured_at as seen_at, (l->>'id')::uuid as listing_id, (l->>'playerId')::uuid as player_id,
       l->>'name' as name, l->>'role' as role, (l->>'age')::int as age, (l->>'height')::int as height_cm, l->>'preferredHand' as preferred_hand,
       (l->>'overall')::int as overall, (l->>'wage')::int as wage, (l->>'retiring')::bool as retiring,
       (l->>'startingPrice')::int as starting_price, (l->>'currentBid')::int as current_bid, (l->>'nextBid')::int as next_bid,
       (l->>'isFreeAgent')::bool as free_agent, (l->>'sellerIsBot')::bool as seller_is_bot, l->>'sellerTeamName' as seller,
       l->>'highestBidderName' as highest_bidder, l->'attributes' as attributes,
       (a.body->>'settleAfterRound')::int as settle_after_round
from silver.sz_api a, jsonb_array_elements(a.body->'listings') l
where a.endpoint = '/transfers'
order by (l->>'id'), a.captured_at desc;

-- Académie U18 [W:U18].
create or replace view silver.sz_u18 with (security_invoker = true) as
select a.day, (a.body->>'available')::bool as available, (a.body->>'squadFull')::bool as squad_full,
       (a.body->>'roundsUntilNextPick')::int as rounds_until_next_pick, a.body->'prospects' as prospects
from silver.sz_api a where a.endpoint = '/teams/mine/u18'
order by a.captured_at desc limit 1;

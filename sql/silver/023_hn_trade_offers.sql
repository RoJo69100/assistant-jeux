-- Hockey Nation : offres d'échange en cours (envoyées et reçues) et plafond en direct (2026-10-29).
-- Avant : l'export Trade Center (/trade-center/trade-offers) n'était lu par aucune vue ; seul le Trade Tracker (échanges conclus de la ligue) l'était.

-- Offres en cours : une ligne par offre, dernier relevé. direction = 'reçue' si l'équipe qui reçoit est la nôtre.
create or replace view silver.hn_trade_offers with (security_invoker = true) as
with last as (
  select a.captured_at, a.body from silver.hn_api a
  where a.route = '/trade-center/trade-offers' order by a.captured_at desc limit 1
)
select (t->>'id')::uuid as offer_id, (t->>'createdAt')::timestamptz as created_at, l.captured_at,
       case when (t->'teams'->'receiving'->>'own')::bool then 'reçue' else 'envoyée' end as direction,
       t->'teams'->'offering'->>'city' || ' ' || (t->'teams'->'offering'->>'nickname') as offering_team,
       t->'teams'->'receiving'->>'city' || ' ' || (t->'teams'->'receiving'->>'nickname') as receiving_team,
       (select string_agg(coalesce(x->'player'->>'firstname' || ' ' || (x->'player'->>'lastname') || ' (' || (x->'player'->'positions'->>0)
                 || ' ' || (x->'player'->>'age') || ' ans, ' || (x->'player'->>'rating') || ', ' || coalesce(x->'player'->'team'->>'level', '?') || ')',
                 'pick T' || (x->'draftPick'->>'round') || ' S' || (x->'draftPick'->>'season')), ', ')
        from jsonb_array_elements(t->'assets'->'offering') x) as they_give,
       (select string_agg(coalesce(x->'player'->>'firstname' || ' ' || (x->'player'->>'lastname') || ' (' || (x->'player'->'positions'->>0)
                 || ' ' || (x->'player'->>'age') || ' ans, ' || (x->'player'->>'rating') || ', ' || coalesce(x->'player'->'team'->>'level', '?') || ')',
                 'pick T' || (x->'draftPick'->>'round') || ' S' || (x->'draftPick'->>'season')), ', ')
        from jsonb_array_elements(t->'assets'->'receiving') x) as they_get,
       (t->'salaryImpact'->'receiving'->>'salaryChange')::bigint as salary_change_receiving,
       (t->>'needsAcceptance')::bool as needs_acceptance, (t->>'votesApproved')::int as votes_approved,
       t->'assets' as assets
from last l, jsonb_array_elements(l.body) t;

-- Plafond PRO en direct (Office > Salary cap), plus frais que /club/:id/finances.
create or replace view silver.hn_cap_now with (security_invoker = true) as
select a.captured_at, (a.body->>'salaryCap')::bigint as salary_cap,
       (a.body->>'projectedSeasonSalary')::bigint as projected_salary, (a.body->>'projectedCapSpace')::bigint as cap_space
from silver.hn_api a
where a.route = '/office/salary-cap-overview'
order by a.captured_at desc limit 1;

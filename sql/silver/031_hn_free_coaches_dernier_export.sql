-- Hockey Nation : le marché des coachs ne garde que le dernier export (2026-10-30).
-- Avant : DISTINCT ON sur tous les exports, donc un coach parti du marché restait « libre »
-- (Graf, Vrábel proposés le 30/10 alors qu'ils n'étaient plus dans l'export de 13:30 UTC).
-- Un export = toutes les captures des 30 minutes qui précèdent la plus récente.
create or replace view silver.hn_free_coaches as
select distinct on ((c.value ->> 'id'))
    a.day,
    (c.value ->> 'id')::uuid as coach_id,
    (c.value ->> 'firstname') || ' ' || (c.value ->> 'lastname') as name,
    (c.value ->> 'age')::integer as age,
    (c.value ->> 'xp')::integer as xp,
    (c.value ->> 'rating')::integer as rating,
    (c.value ->> 'matchRating')::integer as match_rating,
    (c.value ->> 'trainingRating')::integer as training_rating,
    silver.hn_skill(c.value -> 'skills', 'OFP') as ofp,
    silver.hn_skill(c.value -> 'skills', 'DFP') as dfp,
    silver.hn_skill(c.value -> 'skills', 'BAT') as bat,
    silver.hn_skill(c.value -> 'skills', 'PP') as pp,
    silver.hn_skill(c.value -> 'skills', 'PK') as pk,
    c.value -> 'skills' as skills,
    c.value -> 'talents' as talents,
    c.value -> 'specialSkills' as special_skills,
    (c.value ->> 'canOffer')::boolean as can_offer,
    (c.value ->> 'nationId')::uuid as nation_id
from silver.hn_api a, lateral jsonb_array_elements(a.body) c(value)
where a.route = '/coach-center/search'
  and a.captured_at >= (select max(captured_at) - interval '30 minutes'
                        from silver.hn_api where route = '/coach-center/search')
order by (c.value ->> 'id'), a.captured_at desc;

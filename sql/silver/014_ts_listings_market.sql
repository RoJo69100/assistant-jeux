-- Team Soccer : marché masculin et marché féminin séparés (2026-10-27).
-- La page Transferts charge deux listes : region_id = 200 (Women's TS League : vendeurs « Ladies », Ben Ahmed Donkey)
-- et region_id ≠ 200 (équipes premières : Chomelix Cows). Sans cette colonne, Ben Ahmed recevait des cibles masculines.
create or replace view silver.ts_transfer_listings as
select distinct on (((l.value ->> 'id')::integer)) a.captured_at as seen_at,
    (l.value ->> 'id')::integer as listing_id,
    l.value ->> 'listing_type' as listing_type,
    (l.value ->> 'asking_price')::bigint as asking_price,
    (l.value ->> 'bids')::integer as bids,
    (l.value ->> 'last_bidder_team_id')::integer as last_bidder_team_id,
    (l.value ->> 'deadline')::timestamptz as deadline,
    (l.value -> 'seller_team') ->> 'name' as seller,
    ((l.value -> 'player') ->> 'player_id')::integer as player_id,
    trim(both from concat_ws(' ', (l.value -> 'player') ->> 'first_name', (l.value -> 'player') ->> 'last_name')) as name,
    (l.value -> 'player') ->> 'position' as "position",
    ((l.value -> 'player') ->> 'age')::integer as age,
    (l.value -> 'player') ->> 'nationality' as nationality,
    ((l.value -> 'player') ->> 'rating')::numeric as ovr,
    ((l.value -> 'player') ->> 'fitness')::numeric as forme,
    ((l.value -> 'player') ->> 'value')::bigint as value,
    ((l.value -> 'player') ->> 'goalkeeper')::numeric as goalkeeper,
    ((l.value -> 'player') ->> 'defense')::numeric as defense,
    ((l.value -> 'player') ->> 'ball_control')::numeric as ball_control,
    ((l.value -> 'player') ->> 'passing')::numeric as passing,
    ((l.value -> 'player') ->> 'crosses')::numeric as crosses,
    ((l.value -> 'player') ->> 'dribbling')::numeric as dribbling,
    ((l.value -> 'player') ->> 'heading')::numeric as heading,
    ((l.value -> 'player') ->> 'finishing')::numeric as finishing,
    ((l.value -> 'player') ->> 'stamina')::numeric as stamina,
    ((l.value -> 'player') ->> 'pace')::numeric as pace,
    case when a.query ~ 'region_id=eq\.200' then 'feminin' when a.query ~ 'region_id' then 'masculin' end as market
from silver.ts_api a, lateral jsonb_array_elements(a.body) l(value)
where a.endpoint = 'transfer_listings' and l.value ? 'player' and jsonb_typeof(l.value -> 'player') = 'object'
order by ((l.value ->> 'id')::integer), a.captured_at desc;

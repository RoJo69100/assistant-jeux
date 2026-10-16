-- Silver BasketVibe : marché, finances, personnel, académie, classement.
-- Relevés datés par semaine (lundi) quand la donnée est un état ; dédoublonnés par id quand c'est un événement.

-- ---------- Marché ----------
-- Enchères vues sur le marché (/transfer-auctions), dernier état connu de chaque enchère.
create or replace view silver.bv_transfer_auctions with (security_invoker = true) as
select distinct on (x->>'id')
       (x->>'id')::uuid                       as auction_id,
       x->>'status'                           as status,
       (x->>'ends_at')::timestamptz           as ends_at,
       (x->>'player_id')::uuid                as player_id,
       x->>'player_first_name' || ' ' || (x->>'player_last_name') as name,
       x->>'player_position'                  as position,
       (x->>'player_age')::int                as age,
       (x->>'player_strength')::numeric       as ps,
       (x->>'player_experience')::int         as experience,
       (x->>'player_height_cm')::int          as height_cm,
       (x->>'player_weight_kg')::int          as weight_kg,
       x->>'player_nationality_code'          as nationality,
       (x->'player_skills'->>'two_point')::int     as two_point,
       (x->'player_skills'->>'three_point')::int   as three_point,
       (x->'player_skills'->>'defense')::int       as defense,
       (x->'player_skills'->>'passing')::int       as passing,
       (x->'player_skills'->>'ball_handling')::int as ball_handling,
       (x->'player_skills'->>'rebounding')::int    as rebounding,
       (x->'player_skills'->>'stamina')::int       as stamina,
       (x->'player_skills'->>'athleticism')::int   as athleticism,
       (x->>'starting_price')::numeric        as starting_price,
       (x->>'display_price')::numeric         as current_price,
       (x->>'bid_count')::int                 as bid_count,
       (x->>'seller_team_id')::uuid           as seller_team_id,
       x->>'seller_team_name'                 as seller_team,
       (x->>'seller_is_free_agent')::bool     as seller_is_free_agent,
       a.captured_at                          as seen_at
from silver.bv_api a, jsonb_array_elements(a.body->'auctions') x
where a.endpoint = '/transfer-auctions'
order by x->>'id', a.captured_at desc;

-- Transferts conclus (historique global, de la ligue, du club, d'un joueur) : référence de prix.
create or replace view silver.bv_transfers with (security_invoker = true) as
select distinct on (x->>'auction_id')
       x->>'auction_id'                       as auction_id,
       coalesce(x->>'entry_type', 'transfer') as entry_type,
       (x->>'settled_at')::timestamptz        as settled_at,
       (x->>'fee')::numeric                   as fee,
       (x->>'player_id')::uuid                as player_id,
       x->>'player_first_name' || ' ' || (x->>'player_last_name') as name,
       x->>'player_position'                  as position,
       (x->>'player_age')::int                as age,
       nullif(x->>'from_team_id', '')::uuid   as from_team_id,
       nullif(x->>'from_team_name', '')       as from_team,
       nullif(x->>'to_team_id', '')::uuid     as to_team_id,
       x->>'to_team_name'                     as to_team
from silver.bv_api a, jsonb_array_elements(a.body->'transfers') x
where a.endpoint ~ '(^/transfer-history$|^/teams/[0-9a-f-]{36}/transfer-history$|^/leagues/[0-9a-f-]{36}/recent-transfers$|^/players/[0-9a-f-]{36}/transfer-history$)'
order by x->>'auction_id', a.captured_at desc;

-- ---------- Finances ----------
-- État des finances, dernier relevé de chaque semaine.
create or replace view silver.bv_finance_weekly with (security_invoker = true) as
select distinct on (a.team_id, date_trunc('week', a.day))
       date_trunc('week', a.day)::date               as week,
       a.day,
       a.team_id,
       (a.body->>'balance')::numeric                 as balance,
       (a.body->>'popularity')::numeric              as popularity,
       (a.body->>'weekly_salary_total')::numeric     as weekly_salaries,
       (a.body->>'weekly_academy_investment')::numeric as weekly_academy,
       (a.body->>'weekly_medical_staff_cost')::numeric as weekly_personnel,
       (a.body->>'transfer_available')::numeric      as transfer_available,
       (a.body->>'transfer_committed')::numeric      as transfer_committed,
       (a.body->>'transfer_lock')::bool              as transfer_lock
from silver.bv_api a
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/finance$'
order by a.team_id, date_trunc('week', a.day), a.captured_at desc;

-- Transactions (les 20 plus récentes à chaque capture), dédoublonnées.
create or replace view silver.bv_finance_transactions with (security_invoker = true) as
select distinct on (x->>'id')
       (x->>'id')::uuid                       as transaction_id,
       a.team_id,
       (x->>'created_at')::timestamptz        as created_at,
       (x->>'virtual_day')::date              as game_day,
       x->>'kind'                             as kind,
       (x->>'amount')::numeric                as amount,
       (x->>'balance_after')::numeric         as balance_after,
       x->>'ticket_match_kind'                as match_kind,
       x->>'opponent_team_name'               as opponent
from silver.bv_api a, jsonb_array_elements(a.body->'recent_transactions') x
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/finance$'
order by x->>'id', a.captured_at desc;

-- Bilan par saison (cumul depuis le début de saison), dernier relevé.
create or replace view silver.bv_finance_seasons with (security_invoker = true) as
select distinct on (a.team_id, x->>'season_id')
       a.team_id,
       (x->>'season_id')::uuid                as season_id,
       (x->>'season_index')::int              as season_index,
       (x->>'is_current')::bool               as is_current,
       (x->>'league_tickets')::numeric        as league_tickets,
       (x->>'friendlies')::numeric            as friendlies,
       (x->>'cups')::numeric                  as cups,
       (x->>'sponsor')::numeric               as sponsor,
       (x->>'rewards')::numeric               as rewards,
       (x->>'transfers_in')::numeric          as transfers_in,
       (x->>'transfers_out')::numeric         as transfers_out,
       (x->>'salaries')::numeric              as salaries,
       (x->>'personnel')::numeric             as personnel,
       (x->>'academy')::numeric               as academy,
       (x->>'season_balance')::numeric        as season_balance,
       a.day                                  as as_of
from silver.bv_api a, jsonb_array_elements(a.body->'season_summaries') x
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/finance$'
order by a.team_id, x->>'season_id', a.captured_at desc;

-- Contrat sponsor en cours, dernier relevé de chaque semaine.
create or replace view silver.bv_sponsor_weekly with (security_invoker = true) as
select distinct on (a.team_id, date_trunc('week', a.day))
       date_trunc('week', a.day)::date               as week,
       a.team_id,
       a.body->>'phase'                              as phase,
       (a.body->>'choice_pending')::bool             as choice_pending,
       a.body->'active_contract'->>'brand_id'        as brand,
       a.body->'active_contract'->>'variant'         as variant,
       (a.body->'active_contract'->>'weekly_base')::numeric             as weekly_base,
       (a.body->'active_contract'->>'win_bonus_per_league_win')::numeric as win_bonus,
       (a.body->'active_contract'->>'remaining_guaranteed_base')::numeric as remaining_guaranteed,
       (a.body->'active_contract'->>'current_league_rank')::int          as league_rank,
       a.body->'offers'                              as offers
from silver.bv_api a
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/sponsor$'
order by a.team_id, date_trunc('week', a.day), a.captured_at desc;

-- ---------- Personnel ----------
create or replace view silver.bv_personnel_weekly with (security_invoker = true) as
select distinct on (a.team_id, date_trunc('week', a.day))
       date_trunc('week', a.day)::date               as week,
       a.team_id,
       (a.body->>'weekly_cost')::numeric             as weekly_cost,
       (a.body->>'weekly_cost_cap')::numeric         as weekly_cost_cap,
       (a.body->>'doctors_hired')::int               as doctors,
       (a.body->>'doctor_slots')::int                as doctor_slots,
       (a.body->>'physiotherapists_hired')::int      as physios,
       (a.body->>'physiotherapist_slots')::int       as physio_slots,
       (a.body->>'psychologists_hired')::int         as psychologists,
       (a.body->>'psychologist_slots')::int          as psychologist_slots,
       (a.body->>'marketers_hired')::int             as marketers,
       (a.body->>'marketer_slots')::int              as marketer_slots,
       (a.body->>'treatment_reduction_pct')::numeric       as treatment_reduction_pct,
       (a.body->>'prevention_reduction_pct')::numeric      as prevention_reduction_pct,
       (a.body->>'form_improvement_shift_pp')::numeric     as form_improvement_pp,
       (a.body->>'popularity_loss_mitigation_pp')::numeric as popularity_mitigation_pp
from silver.bv_api a
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/personnel$'
order by a.team_id, date_trunc('week', a.day), a.captured_at desc;

-- ---------- Académie ----------
create or replace view silver.bv_academy_weekly with (security_invoker = true) as
select distinct on (a.team_id, date_trunc('week', a.day))
       date_trunc('week', a.day)::date               as week,
       a.team_id,
       (a.body->>'academy_score')::numeric           as academy_score,
       (a.body->>'weekly_investment')::numeric       as weekly_investment,
       (a.body->>'weekly_investment_max')::numeric   as weekly_investment_max,
       (a.body->>'scout_report_at')::timestamptz     as scout_report_at,
       (a.body->>'next_scout_report_due_ymd')::date  as next_scout_report
from silver.bv_api a
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/academy$'
order by a.team_id, date_trunc('week', a.day), a.captured_at desc;

-- Prospects de chaque rapport du scout, avec la fourchette (min-max) de chaque skill.
create or replace view silver.bv_academy_candidates with (security_invoker = true) as
select distinct on (a.body->>'scout_report_at', x->>'slot')
       (a.body->>'scout_report_at')::timestamptz     as scout_report_at,
       a.team_id,
       (x->>'slot')::int                             as slot,
       x->>'first_name' || ' ' || (x->>'last_name')  as name,
       x->>'position'                                as position,
       (x->>'age')::int                              as age,
       (x->>'height_cm')::int                        as height_cm,
       (x->>'weight_kg')::int                        as weight_kg,
       (x->'skill_brackets'->'two_point'->>'min')::int     as two_point_min,
       (x->'skill_brackets'->'two_point'->>'max')::int     as two_point_max,
       (x->'skill_brackets'->'three_point'->>'min')::int   as three_point_min,
       (x->'skill_brackets'->'three_point'->>'max')::int   as three_point_max,
       (x->'skill_brackets'->'defense'->>'min')::int       as defense_min,
       (x->'skill_brackets'->'defense'->>'max')::int       as defense_max,
       (x->'skill_brackets'->'passing'->>'min')::int       as passing_min,
       (x->'skill_brackets'->'passing'->>'max')::int       as passing_max,
       (x->'skill_brackets'->'ball_handling'->>'min')::int as ball_handling_min,
       (x->'skill_brackets'->'ball_handling'->>'max')::int as ball_handling_max,
       (x->'skill_brackets'->'rebounding'->>'min')::int    as rebounding_min,
       (x->'skill_brackets'->'rebounding'->>'max')::int    as rebounding_max,
       (x->'skill_brackets'->'stamina'->>'min')::int       as stamina_min,
       (x->'skill_brackets'->'stamina'->>'max')::int       as stamina_max,
       (x->'skill_brackets'->'athleticism'->>'min')::int   as athleticism_min,
       (x->'skill_brackets'->'athleticism'->>'max')::int   as athleticism_max
from silver.bv_api a, jsonb_array_elements(a.body->'scout_candidates') x
where a.endpoint ~ '^/teams/[0-9a-f-]{36}/academy$'
order by a.body->>'scout_report_at', x->>'slot', a.captured_at desc;

-- ---------- Classement et calendrier ----------
create or replace view silver.bv_standings_weekly with (security_invoker = true) as
select distinct on ((x->>'team_id'), date_trunc('week', a.day))
       date_trunc('week', a.day)::date               as week,
       a.day,
       (a.body->>'season_id')::uuid                  as season_id,
       (x->>'rank')::int                             as rank,
       (x->>'team_id')::uuid                         as team_id,
       x->>'team_name'                               as team,
       (x->>'wins')::int                             as wins,
       (x->>'losses')::int                           as losses,
       (x->>'points')::int                           as points,
       (x->>'pf')::int                               as points_for,
       (x->>'pa')::int                               as points_against,
       (x->>'diff')::int                             as diff,
       (x->>'home_wins')::int                        as home_wins,
       (x->>'home_losses')::int                      as home_losses,
       (x->>'away_wins')::int                        as away_wins,
       (x->>'away_losses')::int                      as away_losses,
       (x->>'club_strength')::numeric                as club_strength,
       (x->>'is_human')::bool                        as is_human,
       x->'form'                                     as form,
       (x->>'team_id')::uuid = m.team_id             as is_mine
from silver.bv_api a
cross join lateral jsonb_array_elements(a.body->'standings') x
left join silver.bv_my_team m on true
where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/standings$'
order by (x->>'team_id'), date_trunc('week', a.day), a.captured_at desc;

-- Calendrier de la saison (tous les matchs de la ligue), dernier état connu.
create or replace view silver.bv_fixtures with (security_invoker = true) as
with src as (
  select a.captured_at, a.body
  from silver.bv_api a
  where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$'
),
labels as (
  select distinct on (l->>'team_id') (l->>'team_id')::uuid as team_id, l->>'team_name' as team_name
  from src, jsonb_array_elements(src.body->'team_labels') l
  order by l->>'team_id', src.captured_at desc
)
select distinct on (f->>'id')
       (f->>'id')::uuid                       as fixture_id,
       (f->>'match_id')::uuid                 as match_id,
       (src.body->>'season_id')::uuid         as season_id,
       (f->>'round_number')::int              as round_number,
       (f->>'match_day')::date                as match_day,
       f->>'status'                           as status,
       (f->>'home_team_id')::uuid             as home_team_id,
       h.team_name                            as home_team,
       (f->>'away_team_id')::uuid             as away_team_id,
       w.team_name                            as away_team,
       (f->>'home_score')::int                as home_score,
       (f->>'away_score')::int                as away_score,
       m.team_id in ((f->>'home_team_id')::uuid, (f->>'away_team_id')::uuid) as is_mine
from src
cross join lateral jsonb_array_elements(src.body->'fixtures') f
left join labels h on h.team_id = (f->>'home_team_id')::uuid
left join labels w on w.team_id = (f->>'away_team_id')::uuid
left join silver.bv_my_team m on true
order by f->>'id', src.captured_at desc;

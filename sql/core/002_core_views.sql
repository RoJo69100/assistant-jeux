-- Généré par pipelines/build_core.py depuis docs/attentes/jeux/*.yaml : ne pas modifier à la main.

create or replace view core.player_daily with (security_invoker = true) as
select game, team_id, club_label, player_id, day, name, position, age, rating, form, fatigue, morale, injured, suspended, salary, contract_end, market_value, is_academy, skills, extras from adapt.basketvibe_player_daily
union all
select game, team_id, club_label, player_id, day, name, position, age, rating, form, fatigue, morale, injured, suspended, salary, contract_end, market_value, is_academy, skills, extras from adapt.hockeynation_player_daily
union all
select game, team_id, club_label, player_id, day, name, position, age, rating, form, fatigue, morale, injured, suspended, salary, contract_end, market_value, is_academy, skills, extras from adapt.teamsoccer_player_daily;
grant select on core.player_daily to assistant_ro;

create or replace view core.fixture with (security_invoker = true) as
select game, team_id, fixture_id, competition_kind, round_no, rounds_total, day, scheduled_at, played, my_score, opp_score, my_result, opponent, home, extras from adapt.basketvibe_fixture
union all
select game, team_id, fixture_id, competition_kind, round_no, rounds_total, day, scheduled_at, played, my_score, opp_score, my_result, opponent, home, extras from adapt.hockeynation_fixture
union all
select game, team_id, fixture_id, competition_kind, round_no, rounds_total, day, scheduled_at, played, my_score, opp_score, my_result, opponent, home, extras from adapt.teamsoccer_fixture;
grant select on core.fixture to assistant_ro;

create or replace view core.standing with (security_invoker = true) as
select game, team_id, team_label, is_mine, season_id, day, round_no, rank, played, points, wins, draws, losses, gf, ga, extras from adapt.basketvibe_standing
union all
select game, team_id, team_label, is_mine, season_id, day, round_no, rank, played, points, wins, draws, losses, gf, ga, extras from adapt.hockeynation_standing
union all
select game, team_id, team_label, is_mine, season_id, day, round_no, rank, played, points, wins, draws, losses, gf, ga, extras from adapt.teamsoccer_standing;
grant select on core.standing to assistant_ro;

create or replace view core.finance_daily with (security_invoker = true) as
select game, team_id, day, balance, income, expenses, salaries, wage_cap, capacite_invest, extras from adapt.basketvibe_finance_daily
union all
select game, team_id, day, balance, income, expenses, salaries, wage_cap, capacite_invest, extras from adapt.hockeynation_finance_daily
union all
select game, team_id, day, balance, income, expenses, salaries, wage_cap, capacite_invest, extras from adapt.teamsoccer_finance_daily;
grant select on core.finance_daily to assistant_ro;

create or replace view core.market_listing with (security_invoker = true) as
select game, team_id, listing_id, day, seen_at, ends_at, status, player_id, name, position, age, rating, price, starting_price, bids, seller_id, seller_label, is_mine, skills, extras from adapt.basketvibe_market_listing
union all
select game, team_id, listing_id, day, seen_at, ends_at, status, player_id, name, position, age, rating, price, starting_price, bids, seller_id, seller_label, is_mine, skills, extras from adapt.hockeynation_market_listing
union all
select game, team_id, listing_id, day, seen_at, ends_at, status, player_id, name, position, age, rating, price, starting_price, bids, seller_id, seller_label, is_mine, skills, extras from adapt.teamsoccer_market_listing;
grant select on core.market_listing to assistant_ro;

create or replace view core.academy_prospect with (security_invoker = true) as
select game, team_id, prospect_id, day, seen_at, name, position, age, rating_min, rating_max, potential_min, potential_max, status, skills, extras from adapt.basketvibe_academy_prospect
union all
select game, team_id, prospect_id, day, seen_at, name, position, age, rating_min, rating_max, potential_min, potential_max, status, skills, extras from adapt.hockeynation_academy_prospect
union all
select game, team_id, prospect_id, day, seen_at, name, position, age, rating_min, rating_max, potential_min, potential_max, status, skills, extras from adapt.teamsoccer_academy_prospect;
grant select on core.academy_prospect to assistant_ro;

create or replace view core.staff with (security_invoker = true) as
select game, team_id, staff_id, day, name, role, level, salary, extras from adapt.basketvibe_staff
union all
select game, team_id, staff_id, day, name, role, level, salary, extras from adapt.hockeynation_staff
union all
select game, team_id, staff_id, day, name, role, level, salary, extras from adapt.teamsoccer_staff;
grant select on core.staff to assistant_ro;

create or replace view core.training_plan with (security_invoker = true) as
select game, team_id, player_id, day, name, is_academy, focus_primary, focus_secondary, intensity, extras from adapt.basketvibe_training_plan
union all
select game, team_id, player_id, day, name, is_academy, focus_primary, focus_secondary, intensity, extras from adapt.hockeynation_training_plan
union all
select game, team_id, player_id, day, name, is_academy, focus_primary, focus_secondary, intensity, extras from adapt.teamsoccer_training_plan;
grant select on core.training_plan to assistant_ro;

create or replace view core.facility with (security_invoker = true) as
select game, team_id, facility_id, day, name, kind, level, capacity, upkeep, extras from adapt.teamsoccer_facility;
grant select on core.facility to assistant_ro;

create or replace view core.season with (security_invoker = true) as
select game, season_id, day1, days_total, phase, extras from adapt.hockeynation_season;
grant select on core.season to assistant_ro;

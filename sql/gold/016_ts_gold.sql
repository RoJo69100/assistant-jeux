-- Gold Team Soccer : vues d'analyse et d'alerte, pour chacun des deux clubs (team_id).
-- Règles citées : skills teamsoccer-joueurs, -club, -saison, -entrainement.

-- Calendrier de la saison par club : fin de la ligue, fin de saison estimée (semaine 8 barrages, semaine 9 repos
-- [skill teamsoccer-saison]), lundis de traitement financier restants, matchs de ligue à domicile restants.
create or replace view gold.ts_season_calendar with (security_invoker = true) as
select mt.team_id, mt.name, mt.division,
       max(m.match_date_paris) filter (where m.competition = 'ligue')::date as last_league_day,
       (max(m.match_date_paris) filter (where m.competition = 'ligue'))::date + 15 as season_end_est,
       (select count(*) from generate_series(current_date + 1, (max(m.match_date_paris) filter (where m.competition = 'ligue'))::date + 15, interval '1 day') d
        where extract(isodow from d) = 1) as mondays_left,
       count(*) filter (where m.competition = 'ligue' and m.status = 'scheduled') as league_left,
       count(*) filter (where m.competition = 'ligue' and m.status = 'scheduled' and m.venue = 'domicile') as home_league_left
from silver.ts_my_teams mt
left join silver.ts_matches m on m.my_team_id = mt.team_id
group by mt.team_id, mt.name, mt.division;

-- Bilan par poste (zone GB / DEF / MIL / ATT) : profondeur, OVR, Forme, âge, coût [skill teamsoccer-joueurs].
create or replace view gold.ts_squad_report with (security_invoker = true) as
select p.team_id, mt.name as team, p.zone, count(*) as players,
       round(avg(p.ovr), 1) as avg_ovr, max(p.ovr) as best_ovr,
       (array_agg(p.name order by p.ovr desc))[1] as best_player,
       round(avg(p.forme), 0) as avg_forme, min(p.forme) as min_forme,
       round(avg(p.age), 1) as avg_age, count(*) filter (where p.age <= 21) as u21, count(*) filter (where p.age >= 29) as age_29_plus,
       count(*) filter (where p.injury_days > 0) as injured, count(*) filter (where p.suspended) as suspended,
       count(*) filter (where p.yellow_cards >= 2) as on_two_yellows,
       sum(p.wage) as weekly_wages, sum(p.value) as total_value, max(p.as_of) as as_of
from silver.ts_players p join silver.ts_my_teams mt on mt.team_id = p.team_id
group by p.team_id, mt.name, p.zone;

-- Progression entre deux relevés d'un même joueur (utile après l'entraînement du vendredi) :
-- écarts d'OVR, de Forme, de valeur et de chaque compétence, avec le réglage d'entraînement actuel.
create or replace view gold.ts_player_progress with (security_invoker = true) as
with s as (
  select s.*, lag(s.day) over w as prev_day, lag(s.ovr) over w as prev_ovr, lag(s.forme) over w as prev_forme,
         lag(s.value) over w as prev_value,
         lag(s.goalkeeper) over w as p_gk, lag(s.defense) over w as p_def, lag(s.ball_control) over w as p_bc,
         lag(s.passing) over w as p_pas, lag(s.crosses) over w as p_cro, lag(s.dribbling) over w as p_dri,
         lag(s.heading) over w as p_hea, lag(s.finishing) over w as p_fin, lag(s.stamina) over w as p_sta, lag(s.pace) over w as p_pac
  from silver.ts_player_snapshots s
  window w as (partition by s.player_id order by s.day)
)
select s.team_id, s.player_id, s.name, s.age, s.prev_day, s.day,
       s.ovr - s.prev_ovr as d_ovr, s.forme - s.prev_forme as d_forme, s.value - s.prev_value as d_value,
       s.goalkeeper - s.p_gk as d_goalkeeper, s.defense - s.p_def as d_defense, s.ball_control - s.p_bc as d_ball_control,
       s.passing - s.p_pas as d_passing, s.crosses - s.p_cro as d_crosses, s.dribbling - s.p_dri as d_dribbling,
       s.heading - s.p_hea as d_heading, s.finishing - s.p_fin as d_finishing, s.stamina - s.p_sta as d_stamina, s.pace - s.p_pac as d_pace,
       t.training_type, t.intensity, s.forme
from s left join silver.ts_training t on t.player_id = s.player_id
where s.prev_day is not null;

-- Finances : dernier relevé, contrôle de l'entretien (6 % de la recette à guichets fermés [skill teamsoccer-club]),
-- et projection de fin de saison (salaires + entretien chaque lundi, billetterie des matchs de ligue à domicile
-- restants selon l'affluence de la division et du rang actuel). Approximation : ni primes, ni ventes, ni coupes.
create or replace view gold.ts_finance_status with (security_invoker = true) as
with f as (select distinct on (team_id) * from silver.ts_finances order by team_id, day desc, captured_at desc),
st as (
  select s.team_id, s.capacity,
         s.seats_standing * 7.5 + s.seats_basic * 15 + s.seats_covered * 27.5 + s.seats_vip * 75 as full_gate
  from silver.ts_stadiums s
),
rk as (select my_team_id as team_id, position from silver.ts_standings where is_mine),
w as (select team_id, sum(wage) as wage_bill from silver.ts_players group by team_id)
select f.team_id, mt.name as team, f.day as as_of, f.balance, f.last_weekly_process,
       f.weekly_income, f.weekly_expenses, f.weekly_income - f.weekly_expenses as week_net,
       w.wage_bill, f.wages_expenses, f.stadium_maintenance,
       round(st.full_gate * 0.06) as maintenance_expected,
       f.stadium_maintenance - round(st.full_gate * 0.06) as maintenance_gap,
       st.full_gate, coalesce(rk.position, 4) as rank_used, mt.division,
       greatest(0, (array[100, 90, 85, 80, 75, 70, 65, 60])[coalesce(rk.position, 4)] - 10 * (mt.division - 1)) / 100.0 as attendance_rate,
       c.mondays_left, c.home_league_left,
       round(st.full_gate * greatest(0, (array[100, 90, 85, 80, 75, 70, 65, 60])[coalesce(rk.position, 4)] - 10 * (mt.division - 1)) / 100.0) as gate_per_home_match,
       f.balance
         - c.mondays_left * (w.wage_bill + round(st.full_gate * 0.06))
         + c.home_league_left * round(st.full_gate * greatest(0, (array[100, 90, 85, 80, 75, 70, 65, 60])[coalesce(rk.position, 4)] - 10 * (mt.division - 1)) / 100.0)
         as projected_season_end,
       f.balance < 0 as alert_negative
from f
join silver.ts_my_teams mt on mt.team_id = f.team_id
left join st on st.team_id = f.team_id
left join rk on rk.team_id = f.team_id
left join w on w.team_id = f.team_id
left join gold.ts_season_calendar c on c.team_id = f.team_id;

-- Rentabilité du stade : matchs à domicile pour rembourser une place de chaque type, au rang et à la division actuels
-- (prix d'achat ÷ (recette × affluence × 0,94), le 0,94 retirant l'entretien de 6 % [skill teamsoccer-club]).
create or replace view gold.ts_stadium_payback with (security_invoker = true) as
select s.team_id, mt.name as team, x.seat_type, x.seats, x.max_seats, x.max_seats - x.seats as room_left,
       x.price, x.revenue, fs.attendance_rate,
       round(x.price / nullif(x.revenue * fs.attendance_rate * 0.94, 0), 1) as home_matches_to_repay,
       fs.home_league_left,
       round(x.price / nullif(x.revenue * fs.attendance_rate * 0.94, 0), 1) <= fs.home_league_left as repaid_this_season
from silver.ts_stadiums s
join silver.ts_my_teams mt on mt.team_id = s.team_id
left join gold.ts_finance_status fs on fs.team_id = s.team_id
cross join lateral (values
  ('debout', s.seats_standing, 50000, 80, 7.5),
  ('basique', s.seats_basic, 20000, 150, 15),
  ('couverte', s.seats_covered, 9500, 300, 27.5),
  ('VIP', s.seats_vip, 500, 1500, 75)
) x(seat_type, seats, max_seats, price, revenue);

-- Académie : un jeune par ligne, compétences révélées, et révélations encore possibles aujourd'hui (1 par jour [U:2026-11-04]).
create or replace view gold.ts_academy with (security_invoker = true) as
select y.team_id, mt.name as team, y.youth_id, y.name, y.age, y.position, y.talent, y.revealed_count,
       (select round(avg((to_jsonb(y)->>k)::numeric), 1) from jsonb_array_elements_text(y.revealed_skills) k) as avg_revealed,
       (select max((to_jsonb(y)->>k)::numeric) from jsonb_array_elements_text(y.revealed_skills) k) as best_revealed,
       (select string_agg(k, ', ') from unnest(array['goalkeeper', 'defense', 'ball_control', 'passing', 'crosses', 'dribbling',
                                                      'heading', 'finishing', 'stamina', 'pace']) k
        where not y.revealed_skills ? k) as hidden_skills,
       case when a.daily_reveal_date = (now() at time zone 'Atlantic/Canary')::date then greatest(0, 1 - a.daily_reveal_count) else 1 end
         as team_reveals_left_today,
       y.day as as_of
from silver.ts_youth_players y
join silver.ts_my_teams mt on mt.team_id = y.team_id
left join silver.ts_youth_academies a on a.team_id = y.team_id
where not coalesce(y.is_high_performance, false);

-- Centre de Haute Performance : TSC investis cette saison, TSC du compte, reste à verser pour atteindre 50
-- (sinon remboursés en fin de saison [F:2026-10-10 PIPO68]) et lundis restants pour le faire.
create or replace view gold.ts_hpc_status with (security_invoker = true) as
select h.team_id, mt.name as team, h.season, h.status, h.total_tsc, h.account_tsc,
       greatest(0, 50 - h.total_tsc) as tsc_needed, h.account_tsc >= greatest(0, 50 - h.total_tsc) as can_complete,
       h.last_payment_week, h.options_week, h.week_options, h.chosen_skills, c.mondays_left, h.day as as_of
from silver.ts_hpc h
join silver.ts_my_teams mt on mt.team_id = h.team_id
left join gold.ts_season_calendar c on c.team_id = h.team_id
where h.season = (select max(season) from silver.ts_hpc);

-- Prochains matchs de chaque club : adversaire, son classement d'équipe et son rang, composition déjà enregistrée ou non
-- (le match est calculé 2 h avant le coup d'envoi [skill teamsoccer-match]).
create or replace view gold.ts_upcoming with (security_invoker = true) as
select m.my_team_id as team_id, mt.name as team, m.match_id, m.match_date_paris, m.competition, m.venue,
       case when m.venue = 'domicile' then m.away_team_id else m.home_team_id end as opponent_id,
       case when m.venue = 'domicile' then m.away_team else m.home_team end as opponent,
       o.team_rating as opponent_rating, mt.team_rating as my_rating, o.is_bot as opponent_is_bot,
       sd.position as opponent_position, sd.points as opponent_points,
       ml.match_id is not null as lineup_saved, ml.formation as saved_formation,
       m.match_date_paris - interval '2 hours' as lineup_deadline_paris
from silver.ts_matches m
join silver.ts_my_teams mt on mt.team_id = m.my_team_id
left join silver.ts_teams o on o.team_id = case when m.venue = 'domicile' then m.away_team_id else m.home_team_id end
left join silver.ts_standings sd on sd.my_team_id = m.my_team_id and sd.team_id = o.team_id
left join silver.ts_match_lineups ml on ml.team_id = m.my_team_id and ml.match_id = m.match_id
where m.status = 'scheduled' and m.match_date > now();

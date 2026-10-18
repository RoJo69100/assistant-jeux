-- Gold BasketVibe : aides à la tactique (agent Tactique).
-- Règles utilisées (skills basketvibe-joueurs / basketvibe-tactique) :
--   PS par emplacement = compétences × poids du poste [M§2.2] (poids indicatifs selon le dev [Dev 2026-09-17]) ;
--   efficacité selon la taille et l'emplacement, interpolée linéairement entre les lignes de 5 cm [M§6.2.1] ;
--   forme [M§5.5] ; fatigue : gain = min × 0,19 × agressivité × (1,5 − 0,008 × endurance), récupération 0,5 + 10 % par nuit [M§5.6] ;
--   pénalité de fatigue en attaque v3 [M§5.6.2] et v4 [News 2026-10-17].
-- Vérifié le 2026-10-18 : la simulation reproduit le tableau §5.6.4 du manuel (ex. endurance 99, soft : 0 / 3 / 7 / 12).

-- Dernier relevé de chaque joueur de mon effectif (valeurs précises si disponibles).
create or replace view gold.bv_roster_now with (security_invoker = true) as
select distinct on (w.player_id)
       w.player_id, w.name, w.position, w.age, w.form, w.fatigue, w.experience, w.ps,
       p.height_cm, p.weight_kg, p.on_transfer_list, w.injury_return_on,
       coalesce(w.two_point_exact,     w.two_point)     as two_point,
       coalesce(w.three_point_exact,   w.three_point)   as three_point,
       coalesce(w.defense_exact,       w.defense)       as defense,
       coalesce(w.passing_exact,       w.passing)       as passing,
       coalesce(w.ball_handling_exact, w.ball_handling) as ball_handling,
       coalesce(w.rebounding_exact,    w.rebounding)    as rebounding,
       coalesce(w.stamina_exact,       w.stamina)       as stamina,
       coalesce(w.athleticism_exact,   w.athleticism)   as athleticism,
       w.week, w.day
from silver.bv_player_weekly w
join silver.bv_my_team me on me.team_id::text = w.team_id
join silver.bv_players p on p.player_id = w.player_id and p.team_id = me.team_id::text
order by w.player_id, w.week desc, w.day desc;

-- Chaque joueur sur chacun des 5 emplacements.
create or replace view gold.bv_slot_fit with (security_invoker = true) as
with weights(slot, ord, w2, w3, wpa, wbh, wde, wre, wat, wst) as (
  values ('PG',1,15,15,15,15,15, 5,10,10), ('SG',2,15,15,10,15,15, 5,15,10), ('SF',3,15,15,10,10,15,10,15,10),
         ('PF',4,15,10,10,10,15,15,15,10), ('C', 5,15,10,10,10,15,15,15,10)
),
height_eff(cm, pg, sg, sf, pf, c) as (
  values (175, 96, 82, 69, 60, 55), (180,100, 93, 80, 71, 55), (185,100, 98, 91, 82, 63), (190,100,100, 98, 93, 74),
         (195,100,100,100, 98, 85), (200,100,100,100,100, 96), (205, 95, 98,100,100,100), (210, 83, 90, 98,100,100),
         (215, 71, 78, 93, 98,100)
),
form_off(form, pct) as (values (1,-11),(2,-8),(3,-5),(4,-4),(5,-1),(6,1),(7,4),(8,7),(9,11),(10,15)),
r as (
  select r.*, least(greatest(r.height_cm, 175), 215) as h,
         (floor(least(greatest(r.height_cm, 175), 214) / 5.0) * 5)::int as h0
  from gold.bv_roster_now r
),
eff as (
  select r.player_id, w.slot, w.ord,
         round((r.two_point * w.w2 + r.three_point * w.w3 + r.passing * w.wpa + r.ball_handling * w.wbh
              + r.defense * w.wde + r.rebounding * w.wre + r.athleticism * w.wat + r.stamina * w.wst) / 100.0, 1) as slot_ps,
         case w.slot when 'PG' then a.pg + (b.pg - a.pg) * (r.h - r.h0) / 5.0
                     when 'SG' then a.sg + (b.sg - a.sg) * (r.h - r.h0) / 5.0
                     when 'SF' then a.sf + (b.sf - a.sf) * (r.h - r.h0) / 5.0
                     when 'PF' then a.pf + (b.pf - a.pf) * (r.h - r.h0) / 5.0
                     else            a.c  + (b.c  - a.c)  * (r.h - r.h0) / 5.0 end as height_eff
  from r
  cross join weights w
  join height_eff a on a.cm = r.h0
  join height_eff b on b.cm = r.h0 + 5
)
select r.player_id, r.name, r.position, r.age, r.height_cm, e.slot, e.ord as slot_order,
       e.slot_ps, round(e.height_eff, 1) as height_eff,
       round(e.slot_ps * e.height_eff / 100, 1) as fit,
       r.form, f.pct as form_off_pct, r.fatigue,
       round(e.slot_ps * e.height_eff / 100 * (1 + f.pct / 100.0), 1) as fit_with_form,
       rank() over (partition by e.slot order by e.slot_ps * e.height_eff / 100 * (1 + f.pct / 100.0) desc) as rank_in_slot,
       r.on_transfer_list, r.injury_return_on
from r
join eff e on e.player_id = r.player_id
left join form_off f on f.form = r.form::int;

-- Fatigue stabilisée avant un match de ligue du samedi (rythme lun / mer / sam), par joueur, minutes et agressivité défensive.
-- defense_tier 0–4 = soft, ×0,875, équilibrée, ×1,325, agressive [M§5.6, §6.3]. Amicaux non comptés (≈ 1/10, §1.2).
create or replace view gold.bv_fatigue_plan with (security_invoker = true) as
with recursive
scen as (
  select r.player_id, r.name, r.stamina, m.minutes, a.defense_tier, a.mult,
         m.minutes * 0.19 * a.mult * (1.5 - 0.008 * r.stamina) as gain
  from gold.bv_roster_now r
  cross join (values (12), (24), (36), (48)) m(minutes)
  cross join (values (0, 0.75), (1, 0.875), (2, 1.0), (3, 1.325), (4, 1.65)) a(defense_tier, mult)
),
-- 3 matchs par semaine, 8 semaines : n = 0 lundi, 1 mercredi, 2 samedi, ... ; nuits après le match : 2, 3, 2
sim(player_id, minutes, defense_tier, n, pre) as (
  select player_id, minutes, defense_tier, 0, 0::numeric from scen
  union all
  select s.player_id, s.minutes, s.defense_tier, s.n + 1,
         (select greatest(0, case when s.n % 3 = 1 then 0.9 * (0.9 * (0.9 * (s.pre + c.gain) - 0.5) - 0.5) - 0.5
                                  else 0.9 * (0.9 * (s.pre + c.gain) - 0.5) - 0.5 end)
          from scen c where c.player_id = s.player_id and c.minutes = s.minutes and c.defense_tier = s.defense_tier)
  from sim s where s.n < 23
),
settled as (
  select player_id, minutes, defense_tier, pre as sat_fatigue from sim where n = 23  -- samedi de la 8e semaine
)
select c.player_id, c.name, round(c.stamina, 1) as stamina, c.minutes, c.defense_tier,
       round(s.sat_fatigue, 1) as sat_fatigue,
       -- pénalité en attaque au coup d'envoi (interpolation linéaire entre les points d'ancrage)
       round(case when s.sat_fatigue <= 20 then -3 * s.sat_fatigue / 20
                  when s.sat_fatigue <= 40 then -3 - 7 * (s.sat_fatigue - 20) / 20
                  when s.sat_fatigue <= 60 then -10 - 10 * (s.sat_fatigue - 40) / 20
                  else -20 - 20 * (s.sat_fatigue - 60) / 40 end, 1) as off_penalty_v3,
       round(case when s.sat_fatigue <= 20 then -4 * s.sat_fatigue / 20
                  when s.sat_fatigue <= 40 then -4 - 11 * (s.sat_fatigue - 20) / 20
                  when s.sat_fatigue <= 60 then -15 - 15 * (s.sat_fatigue - 40) / 20
                  when s.sat_fatigue <= 80 then -30 - 20 * (s.sat_fatigue - 60) / 20
                  else -50 end, 1) as penalty_v4
from scen c
join settled s using (player_id, minutes, defense_tier);

-- Prochains adversaires : classement, force (TS), humain ou bot, nos confrontations passées et leurs meilleurs scoreurs contre nous.
create or replace view gold.bv_next_opponents with (security_invoker = true) as
with nxt as (
  select f.fixture_id, f.round_number, f.match_day,
         case when f.home_team_id = me.team_id then 'home' else 'away' end as venue,
         case when f.home_team_id = me.team_id then f.away_team_id else f.home_team_id end as opp_id,
         case when f.home_team_id = me.team_id then f.away_team else f.home_team end as opponent
  from silver.bv_fixtures f
  cross join silver.bv_my_team me
  where f.is_mine and f.status = 'scheduled'
),
st as (
  select distinct on (team_id) team_id, rank, wins, losses, diff, club_strength, is_human, is_mine
  from silver.bv_standings_weekly order by team_id, day desc
),
past as (
  select o.opp_id,
         string_agg(r.match_day || ' ' || r.competition || ' ' || r.my_result || ' ' || r.my_pts || '-' || r.opp_pts, ' ; ' order by r.match_day) as meetings
  from (select distinct opp_id, opponent from nxt) o
  join gold.bv_match_report r on r.opponent = o.opponent
  group by o.opp_id
),
scorers as (
  select x.opp_id, string_agg(x.name || ' (' || x.position || ', ' || x.pts || ' pts, ' || x.shot_share || ' % des tirs, focus ' || x.our_focus || ')', ' ; ' order by x.pts desc) as top_scorers
  from (
    select o.opp_id, s.name, s.position, round(avg(s.pts), 1) as pts, round(avg(s.shot_share), 1) as shot_share,
           string_agg(distinct s.our_focus, '/') as our_focus,
           rank() over (partition by o.opp_id order by avg(s.pts) desc) as rk
    from (select distinct opp_id, opponent from nxt) o
    join gold.bv_match_opp_focus s on s.opponent = o.opponent
    group by o.opp_id, s.player_id, s.name, s.position
  ) x
  where x.rk <= 3
  group by x.opp_id
)
select n.round_number, n.match_day, n.venue, n.opponent,
       st.rank as opp_rank, st.wins as opp_wins, st.losses as opp_losses, st.diff as opp_diff,
       st.club_strength as opp_ts, mine.club_strength as my_ts, st.is_human as opp_is_human,
       p.meetings, s.top_scorers, n.fixture_id, n.opp_id
from nxt n
left join st on st.team_id = n.opp_id
left join st mine on mine.is_mine
left join past p on p.opp_id = n.opp_id
left join scorers s on s.opp_id = n.opp_id
order by n.match_day;

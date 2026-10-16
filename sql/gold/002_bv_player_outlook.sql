-- Gold BasketVibe : fiche de synthèse et projection sur 3 saisons de chaque joueur de mon effectif.
-- Règles utilisées (manuel, lu le 2026-10-16) :
--   §8.2  principale +1,0 / secondaire +0,5 par semaine (avant multiplicateurs) → 2/3 des gains sur la principale
--   §8.2  âge : pleine vitesse ~16–18 ; à 25 ans +0,7 contre +1,15 à 18 (facteur 0,61) ; 0 à 30 ans
--   §8.5  déclin par saison (8 compétences) : 31 → 8, 33 → 16, 35 → 32, 38 → 40 ; retraite après la saison des 38 ans
--   §8.3  ~8 entraînements par saison ; potentiel 5 : ~13 points/saison à 16 ans
--   §2.2  poids des compétences dans le PS par poste
-- HYPOTHÈSES (pas dans le manuel) : facteur d'âge interpolé linéairement entre 18, 25 et 30 ;
--   déclin interpolé pour 32, 34, 36, 37 ; ralentissement au-dessus de 70 (§8.4) ignoré ;
--   vitesse actuelle = points affichés gagnés / semaines observées depuis la 1re apparition du joueur dans recent-runs.
--   (1re apparition = 1re ligne, forme comprise ; un joueur sans aucun changement les premières semaines est un peu surestimé).

create or replace view gold.bv_age_factor with (security_invoker = true) as
select * from (values
  (16, 1.00), (17, 1.00), (18, 1.00), (19, 0.94), (20, 0.89), (21, 0.83), (22, 0.78),
  (23, 0.72), (24, 0.67), (25, 0.61), (26, 0.49), (27, 0.37), (28, 0.24), (29, 0.12)
) as t(age, factor);

create or replace view gold.bv_age_decline with (security_invoker = true) as
select * from (values
  (31, 8), (32, 12), (33, 16), (34, 24), (35, 32), (36, 35), (37, 38), (38, 40)
) as t(age, tsp_loss);

create or replace view gold.bv_ps_weight with (security_invoker = true) as
select * from (values
  ('two_point',     0.15, 0.15, 0.15, 0.15, 0.15),
  ('three_point',   0.15, 0.15, 0.15, 0.10, 0.10),
  ('passing',       0.15, 0.10, 0.10, 0.10, 0.10),
  ('ball_handling', 0.15, 0.15, 0.10, 0.10, 0.10),
  ('defense',       0.15, 0.15, 0.15, 0.15, 0.15),
  ('rebounding',    0.05, 0.05, 0.10, 0.15, 0.15),
  ('athleticism',   0.10, 0.15, 0.15, 0.15, 0.15),
  ('stamina',       0.10, 0.10, 0.10, 0.10, 0.10)
) as t(skill, pg, sg, sf, pf, c);

create or replace view gold.bv_player_outlook with (security_invoker = true) as
with me as (select team_id from silver.bv_my_team),
roster as (
  select w.*
  from silver.bv_player_weekly w, me
  where w.team_id = me.team_id::text
    and w.week = (select max(week) from silver.bv_player_weekly w2 where w2.team_id = w.team_id)
),
ov as (
  select distinct on (player_id) player_id, p
  from silver.bv_player_overview
  order by player_id, day desc, captured_at desc
),
obs as (
  select c.player_id,
         min(c.run_day)                                   as first_seen,
         coalesce(sum(c.delta) filter (where c.skill <> 'form'), 0) as pts
  from silver.bv_training_changes c
  group by c.player_id
),
sal as (
  select distinct on (player_id) player_id, salary
  from silver.bv_player_salary_weekly order by player_id, week desc
),
season as (
  select max(match_day) as season_end from silver.bv_fixtures where is_mine
),
base as (
  select r.player_id, r.name, r.position, r.age, r.ps, r.form, r.fatigue, r.experience,
         r.injury_return_on, r.training_primary, r.training_secondary,
         coalesce(r.two_point_exact, r.two_point) + coalesce(r.three_point_exact, r.three_point)
       + coalesce(r.defense_exact, r.defense) + coalesce(r.passing_exact, r.passing)
       + coalesce(r.ball_handling_exact, r.ball_handling) + coalesce(r.rebounding_exact, r.rebounding)
       + coalesce(r.stamina_exact, r.stamina) + coalesce(r.athleticism_exact, r.athleticism) as tsp,
         s.salary,
         (ov.p->>'is_academy_junior')::bool                          as academy_junior,
         (ov.p->'season'->>'games_played')::int                      as games,
         round((ov.p->'season'->'averages'->>'min')::numeric, 1)     as min_per_game,
         round((ov.p->'season'->'averages'->>'pts')::numeric, 1)     as pts_per_game,
         round((ov.p->'season'->'averages'->>'eval')::numeric, 1)    as eval_per_game,
         -- semaines observées : de la 1re apparition du joueur au dernier entraînement connu
         case when o.first_seen is null then 0
              else (select count(distinct run_day) from silver.bv_training_changes c2
                    where c2.run_day >= o.first_seen) end           as weeks_observed,
         coalesce(o.pts, 0)                                          as pts_observed,
         (select count(*) from season, generate_series(current_date + 1, season.season_end, interval '1 day') d
          where extract(isodow from d) = 7)                          as weeks_left_season
  from roster r
  left join ov using (player_id)
  left join obs o using (player_id)
  left join sal s using (player_id)
),
rate as (
  select b.*,
         coalesce(af.factor, 0)                                      as age_factor,
         case when b.age >= 30 then 0
              when b.weeks_observed >= 3 then b.pts_observed::numeric / b.weeks_observed
              -- repli : potentiel 5 typique (§8.3, ~13 pts/saison à 16 ans) × facteur d'âge
              else 13.0 / 8 * coalesce(af.factor, 0) end             as weekly_gain,
         case when b.age >= 30 then 'règle (âge)'
              when b.weeks_observed >= 5 then 'moyenne'
              when b.weeks_observed >= 3 then 'faible'
              else 'très faible (potentiel 5 supposé)' end           as confidence,
         -- part d'un point gagné qui va au PS : 2/3 principale + 1/3 secondaire, pondérés par poste
         round(2.0/3 * case b.position when 'PG' then wp.pg when 'SG' then wp.sg when 'SF' then wp.sf when 'PF' then wp.pf else wp.c end
             + 1.0/3 * case b.position when 'PG' then ws.pg when 'SG' then ws.sg when 'SF' then ws.sf when 'PF' then ws.pf else ws.c end, 4) as ps_per_point
  from base b
  left join gold.bv_age_factor af on af.age = b.age
  left join gold.bv_ps_weight wp on wp.skill = b.training_primary
  left join gold.bv_ps_weight ws on ws.skill = b.training_secondary
),
proj as (
  select r.*, g.*
  from rate r
  cross join lateral (
    select
      -- progression (va surtout aux compétences entraînées) et déclin (réparti sur les 8) cumulés sur 1, 2, 3 saisons
      sum(grow) filter (where k <= 1) as grow_s1, sum(decl) filter (where k <= 1) as decl_s1,
      sum(grow) filter (where k <= 2) as grow_s2, sum(decl) filter (where k <= 2) as decl_s2,
      sum(grow)                       as grow_s3, sum(decl)                       as decl_s3
    from (
      select k,
             case when r.age + k >= 30 or r.age_factor = 0 then 0
                  else 8 * r.weekly_gain * coalesce(f.factor, 0) / r.age_factor end as grow,
             case when r.age + k >= 31 then coalesce(d.tsp_loss, 40) else 0 end   as decl
      from generate_series(1, 3) k
      left join gold.bv_age_factor f on f.age = r.age + k
      left join gold.bv_age_decline d on d.age = r.age + k
    ) y
  ) g
)
select player_id, name, position, age, ps, round(tsp, 1) as tsp, salary,
       round(salary / nullif(ps, 0)) as salary_per_ps,
       form, fatigue, experience, injury_return_on, academy_junior,
       games, min_per_game, pts_per_game, eval_per_game,
       training_primary, training_secondary,
       weeks_observed, pts_observed, round(weekly_gain, 2) as weekly_gain, confidence,
       weeks_left_season,
       round(tsp + weekly_gain * weeks_left_season, 0)                              as tsp_end_season,
       round(tsp + weekly_gain * weeks_left_season + grow_s1 - decl_s1, 0)          as tsp_s1,
       round(tsp + weekly_gain * weeks_left_season + grow_s2 - decl_s2, 0)          as tsp_s2,
       round(tsp + weekly_gain * weeks_left_season + grow_s3 - decl_s3, 0)          as tsp_s3,
       round(ps + (weekly_gain * weeks_left_season + grow_s1) * ps_per_point - decl_s1 / 8.0, 1) as ps_s1,
       round(ps + (weekly_gain * weeks_left_season + grow_s2) * ps_per_point - decl_s2 / 8.0, 1) as ps_s2,
       round(ps + (weekly_gain * weeks_left_season + grow_s3) * ps_per_point - decl_s3 / 8.0, 1) as ps_s3,
       age + 1 as age_s1, age + 2 as age_s2, age + 3 as age_s3,
       case when age + 3 > 38 then 'retraite avant S+3'
            when age + 3 >= 31 then 'déclin'
            when age + 3 >= 30 then 'plateau'
            else 'progression' end as trend_s3
from proj;

-- Gold BasketVibe : entraînement et potentiel (agent Entraînement).
-- Règles (skill basketvibe-entrainement) :
--   gain = base (principale 1,0 / secondaire 0,5) × multiplicateur de potentiel × multiplicateur de niveau × multiplicateur d'âge [M§8.2] ;
--   potentiel 1–10 → 0,45 0,65 0,83 1,00 1,15 1,35 1,50 1,60 1,85 2,20 [M§8.3] ;
--   niveau (valeur précise avant l'entraînement) : < 70 ×1 ; 75 ×0,88 ; 80 ×0,75 ; 85 ×0,63 ; 90 ×0,50 ; 95 ×0,21 ; 99 ×0 [M§8.4] ;
--   âge : ×1 à 16–18 ans ; à 25 ans 0,7 / 1,15 = 0,609 (potentiel 5 : +0,7 contre +1,15 à 18) [M§8.2] ; 0 à 30 ans [M§8.5].
-- Hors de 16–18 et 25 ans, le facteur d'âge vient de gold.bv_age_factor (HYPOTHÈSE : interpolation linéaire).
-- Vérifié le 2026-10-18 : sur l'entraînement du 18/10, les gains précis tombent sur le tableau (Bernard 17 ans +2,20 = potentiel 10 ;
-- Leclerc / Baron 16 ans +1,60 = 8 ; Lecomte 16 ans +1,15 = 5 ; Gimenez 25 ans 0,82 / 0,609 = 1,35 = 6 ; Bonnet 25 ans 0,91 / 0,609 = 1,50 = 7),
-- et la secondaire vaut exactement la moitié de la principale.

create or replace view gold.bv_level_mult with (security_invoker = true) as
select * from (values (0, 1.0), (70, 1.0), (75, 0.88), (80, 0.75), (85, 0.63), (90, 0.50), (95, 0.21), (99, 0.0), (100, 0.0)) t(v, mult);

create or replace view gold.bv_potential_mult with (security_invoker = true) as
select * from (values (1, 0.45), (2, 0.65), (3, 0.83), (4, 1.00), (5, 1.15), (6, 1.35), (7, 1.50), (8, 1.60), (9, 1.85), (10, 2.20)) t(potential, mult);

-- Gains précis par joueur et compétence, entre deux relevés hebdomadaires consécutifs (un entraînement entre les deux).
create or replace view gold.bv_training_gains_exact with (security_invoker = true) as
with w as (
  select w.*, lag(w.week) over (partition by w.player_id order by w.week) as prev_week
  from silver.bv_player_weekly w
  join silver.bv_my_team me on me.team_id::text = w.team_id
),
pairs as (
  select b.player_id, b.name, a.age, b.week, a.injury_return_on as injured_before,
         a.training_primary, a.training_secondary,
         s.skill, s.v_before, s.v_after
  from w b
  join w a on a.player_id = b.player_id and a.week = b.prev_week
  cross join lateral (values
    ('two_point',     a.two_point_exact,     b.two_point_exact),
    ('three_point',   a.three_point_exact,   b.three_point_exact),
    ('defense',       a.defense_exact,       b.defense_exact),
    ('passing',       a.passing_exact,       b.passing_exact),
    ('ball_handling', a.ball_handling_exact, b.ball_handling_exact),
    ('rebounding',    a.rebounding_exact,    b.rebounding_exact),
    ('stamina',       a.stamina_exact,       b.stamina_exact),
    ('athleticism',   a.athleticism_exact,   b.athleticism_exact)
  ) s(skill, v_before, v_after)
  where b.week - b.prev_week = 7          -- semaines consécutives seulement
)
select p.*, round(p.v_after - p.v_before, 3) as gain,
       rank() over (partition by p.player_id, p.week order by p.v_after - p.v_before desc, p.skill) as gain_rank
from pairs p;

-- Estimation du potentiel : principale = compétence au plus fort gain de la semaine.
create or replace view gold.bv_potential_estimate with (security_invoker = true) as
with g as (
  select player_id, name, age, week, injured_before,
         max(skill)   filter (where gain_rank = 1) as primary_skill,
         max(gain)    filter (where gain_rank = 1) as primary_gain,
         max(v_before) filter (where gain_rank = 1) as primary_before,
         max(skill)   filter (where gain_rank = 2) as secondary_skill,
         max(gain)    filter (where gain_rank = 2) as secondary_gain,
         max(v_before) filter (where gain_rank = 2) as secondary_before,
         max(training_primary) as declared_primary
  from gold.bv_training_gains_exact
  group by player_id, name, age, week, injured_before
),
lvl as (  -- multiplicateur de niveau interpolé sur la valeur avant entraînement
  select g.*,
         (select l1.mult + (l2.mult - l1.mult) * (least(g.primary_before, 100) - l1.v) / nullif(l2.v - l1.v, 0)
          from gold.bv_level_mult l1, gold.bv_level_mult l2
          where l1.v = (select max(v) from gold.bv_level_mult where v <= least(g.primary_before, 99.99))
            and l2.v = (select min(v) from gold.bv_level_mult where v >  least(g.primary_before, 99.99))) as primary_level_mult
  from g
),
f as (
  select l.*,
         case when l.age between 16 and 18 then 1.0
              when l.age = 25 then round(0.7 / 1.15, 4)
              when l.age >= 30 then 0
              else (select factor from gold.bv_age_factor a where a.age = l.age) end as age_factor,
         case when l.age between 16 and 18 or l.age = 25 then 'règle (manuel)'
              when l.age >= 30 then 'sans objet (≥ 30 ans)'
              else 'hypothèse (âge interpolé)' end as age_factor_source
  from lvl l
),
r as (
  select f.*,
         round(f.primary_gain / nullif(f.primary_level_mult * f.age_factor, 0), 3) as implied_mult,
         round(f.secondary_gain / nullif(f.primary_gain, 0), 2)                     as secondary_ratio
  from f
)
select r.player_id, r.name, r.age, r.week, r.primary_skill, r.declared_primary,
       round(r.primary_before, 2) as primary_before, r.primary_gain, r.secondary_skill, r.secondary_gain, r.secondary_ratio,
       round(r.primary_level_mult, 3) as primary_level_mult, r.age_factor, r.age_factor_source, r.implied_mult,
       case when r.implied_mult is not null then
       (select p.potential from gold.bv_potential_mult p order by abs(p.mult - r.implied_mult) limit 1) end as potential_est,
       (select round(min(abs(p.mult - r.implied_mult)), 3) from gold.bv_potential_mult p) as distance_to_table,
       case when r.injured_before is not null then 'nulle (blessé)'
            when r.age >= 30 then 'sans objet'
            when r.primary_gain is null or r.primary_gain <= 0 then 'nulle (pas de gain)'
            when r.age_factor_source = 'règle (manuel)' and abs(r.secondary_ratio - 0.5) <= 0.05
                 and (select min(abs(p.mult - r.implied_mult)) from gold.bv_potential_mult p) <= 0.03 then 'élevée'
            when r.age_factor_source = 'règle (manuel)' then 'moyenne'
            when r.age <= 24 then 'moyenne (âge interpolé)'
            else 'faible (âge interpolé, 26–29 ans)' end as confidence
from r;

-- Options d'entraînement : chaque compétence de chaque joueur, avec son poids dans le PS du poste et son multiplicateur de niveau.
create or replace view gold.bv_training_options with (security_invoker = true) as
with r as (
  select distinct on (w.player_id) w.*
  from silver.bv_player_weekly w
  join silver.bv_my_team me on me.team_id::text = w.team_id
  order by w.player_id, w.week desc
),
s as (
  select r.player_id, r.name, r.age, r.position, r.training_primary, r.training_secondary, x.skill, x.v
  from r cross join lateral (values
    ('two_point', coalesce(r.two_point_exact, r.two_point)), ('three_point', coalesce(r.three_point_exact, r.three_point)),
    ('defense', coalesce(r.defense_exact, r.defense)), ('passing', coalesce(r.passing_exact, r.passing)),
    ('ball_handling', coalesce(r.ball_handling_exact, r.ball_handling)), ('rebounding', coalesce(r.rebounding_exact, r.rebounding)),
    ('stamina', coalesce(r.stamina_exact, r.stamina)), ('athleticism', coalesce(r.athleticism_exact, r.athleticism))
  ) x(skill, v)
)
select s.player_id, s.name, s.age, s.position, s.skill, round(s.v, 2) as value,
       case s.position when 'PG' then w.pg when 'SG' then w.sg when 'SF' then w.sf when 'PF' then w.pf else w.c end as ps_weight,
       round((select l1.mult + (l2.mult - l1.mult) * (least(s.v, 100) - l1.v) / nullif(l2.v - l1.v, 0)
              from gold.bv_level_mult l1, gold.bv_level_mult l2
              where l1.v = (select max(v) from gold.bv_level_mult where v <= least(s.v, 99.99))
                and l2.v = (select min(v) from gold.bv_level_mult where v >  least(s.v, 99.99))), 3) as level_mult,
       s.skill = s.training_primary as is_primary, s.skill = s.training_secondary as is_secondary
from s
join gold.bv_ps_weight w on w.skill = s.skill;

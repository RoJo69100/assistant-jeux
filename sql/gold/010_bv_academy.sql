-- Gold BasketVibe : académie (agent Académie).
-- Règles (skill basketvibe-academie, manuel §4.2) :
--   jauge : courbes du manuel depuis 0 % à 100 000 / semaine (20, 37, 52, 64, 74, 82, 89, 94, 97, 99, 100) et à 50 000
--   (12, 23, 33, 42, 50, 58, 65, 71, 76, 80, 83, 85, 87, 88, 89) ; 0 investi = −5 par semaine ; signer ≈ divise la jauge par 2 ;
--   probabilités du potentiel caché selon la jauge au moment du rapport (tableau, interpolé linéairement entre les lignes de 10 %) ;
--   tests 25 000 → catégorie Low (1–3) / Decent (4–7) / High (8–10).
-- HYPOTHÈSE : depuis une jauge quelconque, la semaine suivante suit la même courbe (position fractionnaire sur la courbe depuis 0 %).
-- Vérification : depuis 50 % à 100 000, la courbe donne 63, 73, 82, 89, 94, 97, 99, 100 comme le manuel (à ±1).

create or replace view gold.bv_academy_curve with (security_invoker = true) as
select * from (values
  (100000, 0, 0), (100000, 1, 20), (100000, 2, 37), (100000, 3, 52), (100000, 4, 64), (100000, 5, 74), (100000, 6, 82),
  (100000, 7, 89), (100000, 8, 94), (100000, 9, 97), (100000, 10, 99), (100000, 11, 100),
  (50000, 0, 0), (50000, 1, 12), (50000, 2, 23), (50000, 3, 33), (50000, 4, 42), (50000, 5, 50), (50000, 6, 58), (50000, 7, 65),
  (50000, 8, 71), (50000, 9, 76), (50000, 10, 80), (50000, 11, 83), (50000, 12, 85), (50000, 13, 87), (50000, 14, 88), (50000, 15, 89)
) t(investment, step, score);

-- Projection de la jauge sur 8 semaines selon l'investissement (100 000, 50 000, 0), depuis la jauge actuelle et après une signature.
create or replace view gold.bv_academy_gauge_projection with (security_invoker = true) as
with now_ as (select academy_score as s from silver.bv_academy_weekly order by week desc limit 1),
start as (select 'sans signature' as scenario, s from now_ union all select 'après une signature', round(s / 2.0, 1) from now_),
pos as (  -- position fractionnaire de la jauge sur chaque courbe
  select st.scenario, st.s, c.investment,
         (select c1.step + (st.s - c1.score)::numeric / nullif(c2.score - c1.score, 0)
          from gold.bv_academy_curve c1 join gold.bv_academy_curve c2 on c2.investment = c1.investment and c2.step = c1.step + 1
          where c1.investment = c.investment and st.s >= c1.score and st.s < c2.score) as p,
         (select max(step) from gold.bv_academy_curve where investment = c.investment) as last_step
  from start st cross join (select distinct investment from gold.bv_academy_curve) c
),
w as (select generate_series(1, 8) as week)
select pos.scenario, pos.investment, w.week,
       round(case when pos.p is null then (select max(score) from gold.bv_academy_curve where investment = pos.investment)  -- déjà au plafond
                  when pos.p + w.week >= pos.last_step then (select max(score) from gold.bv_academy_curve where investment = pos.investment)
                  else (select c1.score + (c2.score - c1.score) * ((pos.p + w.week) - floor(pos.p + w.week))
                        from gold.bv_academy_curve c1 join gold.bv_academy_curve c2 on c2.investment = c1.investment and c2.step = c1.step + 1
                        where c1.investment = pos.investment and c1.step = floor(pos.p + w.week)::int) end, 1) as score
from pos cross join w
union all
select st.scenario, 0, w.week, greatest(0, st.s - 5 * w.week) from start st cross join w
order by 1, 2 desc, 3;

-- Probabilités du potentiel selon la jauge (tableau du manuel).
create or replace view gold.bv_academy_potential_table with (security_invoker = true) as
select * from (values
  (0,   12.5, 16.8, 23.1, 20.3, 14.7,  9.1,  3.5,  0.0,  0.0,  0.0),
  (10,   8.5, 14.4, 21.5, 22.2, 16.6, 11.0,  5.3,  0.6,  0.0,  0.0),
  (20,   5.2, 12.1, 19.1, 23.4, 18.4, 12.8,  7.2,  1.7,  0.0,  0.0),
  (30,   2.7,  9.7, 16.8, 23.1, 20.3, 14.7,  9.1,  3.5,  0.0,  0.0),
  (40,   1.1,  7.4, 14.4, 21.5, 22.2, 16.6, 11.0,  5.3,  0.6,  0.0),
  (50,   0.2,  5.0, 12.1, 19.1, 23.4, 18.4, 12.8,  7.2,  1.7,  0.0),
  (60,   0.0,  2.7,  9.7, 16.8, 23.1, 20.3, 14.7,  9.1,  3.5,  0.0),
  (70,   0.0,  1.1,  7.4, 14.4, 21.5, 22.2, 16.6, 11.0,  5.3,  0.6),
  (80,   0.0,  0.2,  5.0, 12.1, 19.1, 23.4, 18.4, 12.8,  7.2,  1.7),
  (90,   0.0,  0.0,  2.7,  9.7, 16.8, 23.1, 20.3, 14.7,  9.1,  3.5),
  (99,   0.0,  0.0,  1.1,  7.4, 14.4, 21.5, 22.2, 16.6, 11.0,  5.9),
  (100,  0.0,  0.0,  0.0,  3.9, 10.9, 18.0, 23.4, 19.4, 13.8, 10.7)
) t(score, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10);

-- Résumé des probabilités pour une jauge donnée (interpolation entre lignes) : jauge actuelle et jauges projetées.
create or replace view gold.bv_academy_potential_odds with (security_invoker = true) as
with g as (
  select 'jauge actuelle' as label, academy_score as s from (select academy_score from silver.bv_academy_weekly order by week desc limit 1) z
  union all select 'jauge à ' || x, x from (values (60), (80), (90), (100)) v(x)
),
r as (
  select g.label, g.s, a.score as s0, b.score as s1,
         case when b.score = a.score then 0 else (g.s - a.score)::numeric / (b.score - a.score) end as f,
         a.p1 a1, a.p2 a2, a.p3 a3, a.p4 a4, a.p5 a5, a.p6 a6, a.p7 a7, a.p8 a8, a.p9 a9, a.p10 a10,
         b.p1 b1, b.p2 b2, b.p3 b3, b.p4 b4, b.p5 b5, b.p6 b6, b.p7 b7, b.p8 b8, b.p9 b9, b.p10 b10
  from g
  join gold.bv_academy_potential_table a on a.score = (select max(score) from gold.bv_academy_potential_table where score <= g.s)
  join gold.bv_academy_potential_table b on b.score = (select min(score) from gold.bv_academy_potential_table where score >= g.s)
)
select label, s as academy_score,
       round((a1+a2+a3) + f*((b1+b2+b3)-(a1+a2+a3)), 1)                         as p_low_1_3,
       round((a4+a5+a6+a7) + f*((b4+b5+b6+b7)-(a4+a5+a6+a7)), 1)                as p_decent_4_7,
       round((a8+a9+a10) + f*((b8+b9+b10)-(a8+a9+a10)), 1)                      as p_high_8_10,
       round((1*a1+2*a2+3*a3+4*a4+5*a5+6*a6+7*a7+8*a8+9*a9+10*a10) / 100
             + f*((1*b1+2*b2+3*b3+4*b4+5*b5+6*b6+7*b7+8*b8+9*b9+10*b10) - (1*a1+2*a2+3*a3+4*a4+5*a5+6*a6+7*a7+8*a8+9*a9+10*a10)) / 100, 2) as expected_potential
from r;

-- Prospects du dernier rapport du scout : TSP (fourchette), PS estimé au poste, taille.
create or replace view gold.bv_academy_prospects with (security_invoker = true) as
with c as (
  select * from silver.bv_academy_candidates
  where scout_report_at = (select max(scout_report_at) from silver.bv_academy_candidates)
)
select c.scout_report_at, c.slot, c.name, c.position, c.age, c.height_cm, c.weight_kg,
       c.two_point_min + c.three_point_min + c.defense_min + c.passing_min + c.ball_handling_min + c.rebounding_min + c.stamina_min + c.athleticism_min as tsp_min,
       c.two_point_max + c.three_point_max + c.defense_max + c.passing_max + c.ball_handling_max + c.rebounding_max + c.stamina_max + c.athleticism_max as tsp_max,
       round(((c.two_point_min + c.two_point_max) * w.two_point + (c.three_point_min + c.three_point_max) * w.three_point
            + (c.defense_min + c.defense_max) * w.defense + (c.passing_min + c.passing_max) * w.passing
            + (c.ball_handling_min + c.ball_handling_max) * w.ball_handling + (c.rebounding_min + c.rebounding_max) * w.rebounding
            + (c.stamina_min + c.stamina_max) * w.stamina + (c.athleticism_min + c.athleticism_max) * w.athleticism) / 2.0, 1) as ps_mid,
       c.two_point_min, c.two_point_max, c.three_point_min, c.three_point_max, c.defense_min, c.defense_max,
       c.passing_min, c.passing_max, c.ball_handling_min, c.ball_handling_max, c.rebounding_min, c.rebounding_max,
       c.stamina_min, c.stamina_max, c.athleticism_min, c.athleticism_max
from c
cross join lateral (
  select max(case skill when 'two_point' then v end) two_point, max(case skill when 'three_point' then v end) three_point,
         max(case skill when 'defense' then v end) defense, max(case skill when 'passing' then v end) passing,
         max(case skill when 'ball_handling' then v end) ball_handling, max(case skill when 'rebounding' then v end) rebounding,
         max(case skill when 'stamina' then v end) stamina, max(case skill when 'athleticism' then v end) athleticism
  from (select pw.skill, case c.position when 'PG' then pw.pg when 'SG' then pw.sg when 'SF' then pw.sf when 'PF' then pw.pf else pw.c end as v
        from gold.bv_ps_weight pw) z
) w;

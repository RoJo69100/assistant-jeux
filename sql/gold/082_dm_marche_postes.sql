-- DerbyManager : joueurs du marché comparés à notre dernier titulaire de la ligne.
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view gold.dm_marche_postes with (security_invoker = true) as
WITH m AS (
         SELECT mk.viewer_team_id,
            mk.captured_at,
            mk.name,
            mk.team,
            mk.decision,
            mk.pos,
            mk.age,
            mk.country,
            mk.salary,
            mk.duration,
            mk.tier,
            mk.price,
            mk.skill_ranges,
            mk.avg_min,
            mk.avg_max,
            ( SELECT jsonb_object_agg(e.k, (silver.dm_n(split_part(e.v, '-'::text, 1)) + silver.dm_n(split_part(e.v, '-'::text, 2))) / 2.0) AS jsonb_object_agg
                   FROM jsonb_each_text(mk.skill_ranges) e(k, v)
                  WHERE e.v ~ '-'::text) AS mid,
            ( SELECT jsonb_object_agg(e.k, silver.dm_n(split_part(e.v, '-'::text, 1))) AS jsonb_object_agg
                   FROM jsonb_each_text(mk.skill_ranges) e(k, v)
                  WHERE e.v ~ '-'::text) AS lo
           FROM silver.dm_market mk
        ), n AS (
         SELECT m.viewer_team_id,
            m.captured_at,
            m.name,
            m.team,
            m.decision,
            m.pos,
            m.age,
            m.country,
            m.salary,
            m.duration,
            m.tier,
            m.price,
            m.skill_ranges,
            m.avg_min,
            m.avg_max,
            m.mid,
            m.lo,
                CASE
                    WHEN m.pos ~ '^GK'::text THEN 1
                    WHEN m.pos ~ '^D'::text THEN 2
                    WHEN m.pos ~ '^M'::text THEN 3
                    ELSE 4
                END AS ligne,
                CASE
                    WHEN m.pos ~ '^GK'::text THEN (((m.mid ->> 'han'::text)::numeric) + ((m.mid ->> 'posi'::text)::numeric) + ((m.mid ->> 'agi'::text)::numeric) + ((m.mid ->> 'aer'::text)::numeric) + ((m.mid ->> 'rea'::text)::numeric)) / 5::numeric
                    WHEN m.pos ~ '^D'::text THEN (((m.mid ->> 'mar'::text)::numeric) + ((m.mid ->> 'tac'::text)::numeric) + ((m.mid ->> 'posi'::text)::numeric) + ((m.mid ->> 'ant'::text)::numeric) + ((m.mid ->> 'aer'::text)::numeric)) / 5::numeric
                    WHEN m.pos ~ '^M'::text THEN (((m.mid ->> 'pas'::text)::numeric) + ((m.mid ->> 'cre'::text)::numeric) + ((m.mid ->> 'fir'::text)::numeric) + ((m.mid ->> 'tec'::text)::numeric) + ((m.mid ->> 'ant'::text)::numeric) + ((m.mid ->> 'bal'::text)::numeric)) / 6::numeric
                    ELSE (((m.mid ->> 'sho'::text)::numeric) + ((m.mid ->> 'acc'::text)::numeric) + ((m.mid ->> 'fir'::text)::numeric) + ((m.mid ->> 'agi'::text)::numeric) + ((m.mid ->> 'hea'::text)::numeric) + ((m.mid ->> 'tec'::text)::numeric)) / 6::numeric
                END AS note_mid,
                CASE
                    WHEN m.pos ~ '^GK'::text THEN (((m.lo ->> 'han'::text)::numeric) + ((m.lo ->> 'posi'::text)::numeric) + ((m.lo ->> 'agi'::text)::numeric) + ((m.lo ->> 'aer'::text)::numeric) + ((m.lo ->> 'rea'::text)::numeric)) / 5::numeric
                    WHEN m.pos ~ '^D'::text THEN (((m.lo ->> 'mar'::text)::numeric) + ((m.lo ->> 'tac'::text)::numeric) + ((m.lo ->> 'posi'::text)::numeric) + ((m.lo ->> 'ant'::text)::numeric) + ((m.lo ->> 'aer'::text)::numeric)) / 5::numeric
                    WHEN m.pos ~ '^M'::text THEN (((m.lo ->> 'pas'::text)::numeric) + ((m.lo ->> 'cre'::text)::numeric) + ((m.lo ->> 'fir'::text)::numeric) + ((m.lo ->> 'tec'::text)::numeric) + ((m.lo ->> 'ant'::text)::numeric) + ((m.lo ->> 'bal'::text)::numeric)) / 6::numeric
                    ELSE (((m.lo ->> 'sho'::text)::numeric) + ((m.lo ->> 'acc'::text)::numeric) + ((m.lo ->> 'fir'::text)::numeric) + ((m.lo ->> 'agi'::text)::numeric) + ((m.lo ->> 'hea'::text)::numeric) + ((m.lo ->> 'tec'::text)::numeric)) / 6::numeric
                END AS note_min
           FROM m
        ), nous AS (
         SELECT dm_poste_scores.team_id,
            dm_poste_scores.ligne,
            max(dm_poste_scores.note_poste) AS meilleur,
            (array_agg(dm_poste_scores.note_poste ORDER BY dm_poste_scores.note_poste DESC))[LEAST(
                CASE dm_poste_scores.ligne
                    WHEN 1 THEN 1
                    WHEN 2 THEN 5
                    WHEN 3 THEN 4
                    ELSE 1
                END, count(*)::integer)] AS dernier_titulaire
           FROM gold.dm_poste_scores
          GROUP BY dm_poste_scores.team_id, dm_poste_scores.ligne
        )
 SELECT c.team_id,
    c.club,
    n.name,
    n.team AS vendeur,
    n.pos,
    n.age,
    n.tier,
    n.price,
    n.salary,
    n.decision,
    round(n.note_min, 1) AS note_min,
    round(n.note_mid, 1) AS note_milieu,
    u.meilleur AS notre_meilleur,
    u.dernier_titulaire,
    round(n.note_mid - u.dernier_titulaire, 1) AS gain_milieu,
    round(n.note_min - u.dernier_titulaire, 1) AS gain_sur
   FROM n
     CROSS JOIN silver.dm_clubs c
     JOIN nous u ON u.team_id = c.team_id AND u.ligne = n.ligne;

grant select on gold.dm_marche_postes to assistant_ro;

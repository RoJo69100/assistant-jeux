-- DerbyManager : joueurs scoutés de la page /market (fourchettes de compétences).
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view silver.dm_scouted with (security_invoker = true) as
WITH p AS (
         SELECT dm_pages.capture_id,
            dm_pages.captured_at,
            dm_pages.day,
            dm_pages.page_type,
            dm_pages.page_url,
            dm_pages.team_id,
            dm_pages.tables,
            dm_pages.fields,
            dm_pages.text,
            dm_pages.html
           FROM silver.dm_pages
          WHERE dm_pages.page_url = 'https://www.derbymanager.com/market'::text
        ), k(i, sk) AS (
         VALUES (5,'han'::text), (6,'mar'::text), (7,'tac'::text), (8,'posi'::text), (9,'aer'::text), (10,'agi'::text), (11,'ant'::text), (12,'cre'::text), (13,'pas'::text), (14,'bal'::text), (15,'fir'::text), (16,'tec'::text), (17,'acc'::text), (18,'sho'::text), (19,'hea'::text), (20,'rea'::text)
        )
 SELECT p.captured_at,
    tb.ord AS tableau,
    r.value ->> 1 AS name,
    regexp_replace(r.value ->> 2, '^\d+-'::text, ''::text) AS pos,
    silver.dm_n(r.value ->> 3)::integer AS age,
    r.value ->> 4 AS country,
    ( SELECT jsonb_object_agg(k.sk, "substring"(r.value ->> k.i, '::(\d+(?:-\d+)?)$'::text)) AS jsonb_object_agg
           FROM k) AS skill_ranges,
    ( SELECT round(avg((silver.dm_n(split_part("substring"(r.value ->> k.i, '::(\d+(?:-\d+)?)$'::text), '-'::text, 1)) + silver.dm_n(split_part("substring"(r.value ->> k.i, '::(\d+(?:-\d+)?)$'::text), '-'::text, 2))) / 2.0), 1) AS round
           FROM k) AS moy16_mid,
    ( SELECT round(avg(silver.dm_n(split_part("substring"(r.value ->> k.i, '::(\d+(?:-\d+)?)$'::text), '-'::text, 2)) - silver.dm_n(split_part("substring"(r.value ->> k.i, '::(\d+(?:-\d+)?)$'::text), '-'::text, 1))), 1) AS round
           FROM k) AS largeur_moy
   FROM p
     CROSS JOIN LATERAL jsonb_array_elements(p.tables) WITH ORDINALITY tb(t, ord)
     CROSS JOIN LATERAL jsonb_array_elements(tb.t -> 'rows'::text) r(value)
  WHERE tb.ord >= 2 AND ((tb.t -> 'headers'::text) ->> 1) = 'NAME'::text AND ((tb.t -> 'headers'::text) ->> 2) = 'POS'::text AND jsonb_array_length(r.value) = 21;

grant select on silver.dm_scouted to assistant_ro;

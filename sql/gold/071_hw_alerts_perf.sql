-- Hardwood : gold.hw_daily_alerts expirait (statement timeout 8 s du rôle authenticator).
-- Mesures du 2026-11-07 : hw_depth_suggest 10,1 s (la CTE cand était recalculée à chaque pas de la récursion),
-- appelée deux fois par hw_daily_alerts, de même que hw_exports_state (2,3 s).
-- Correctifs : cand MATERIALIZED (10,1 s -> 2,1 s) ; dans hw_daily_alerts, chaque sous-vue n'est lue qu'une fois
-- (CTE MATERIALIZED) ; points de recrutement lus sur le dernier relevé seulement (avant : DISTINCT sur tout
-- l'historique, une vieille capture à 40+ points relançait l'alerte).

create or replace view gold.hw_depth_suggest with (security_invoker = true) as
WITH RECURSIVE slots AS (
  SELECT row_number() OVER (ORDER BY d.d, p_1.o) AS k, d.d AS depth, p_1.pos,
         CASE WHEN p_1.pos = ANY (ARRAY['PF'::text, 'C'::text]) THEN 'Grand'::text ELSE p_1.pos END AS grp
  FROM (VALUES ('PG'::text,1), ('C'::text,2), ('PF'::text,3), ('SF'::text,4), ('SG'::text,5)) p_1(pos, o),
       generate_series(1, 3) d(d)
), cand AS MATERIALIZED (
  SELECT n.player_id, n.name, n.grp, n.note, sl.pos AS slot_pos,
         n.note + 0.5 + COALESCE(s.plus_minus, 0::numeric) / 20.0 AS adj
  FROM gold.hw_player_group_notes n
  JOIN silver.hw_roster r ON r.player_id = n.player_id
  CROSS JOIN (VALUES ('PG'::text), ('SG'::text), ('SF'::text), ('PF'::text), ('C'::text)) sl(pos)
  LEFT JOIN silver.hw_management m ON m.player_id = n.player_id
  LEFT JOIN silver.hw_player_stats s ON s.name = ((left(r.name, 1) || '. '::text) || substr(r.name, strpos(r.name, ' '::text) + 1))
  WHERE NOT r.injured AND COALESCE(m.red_shirt, 'non'::text) <> 'oui'::text AND n.height_ok
    AND n.grp = CASE WHEN sl.pos = ANY (ARRAY['PF'::text, 'C'::text]) THEN 'Grand'::text ELSE sl.pos END
    AND COALESCE(r.positions, ''::text) ~ (('(^|\s)'::text || sl.pos) || '(\s|$)'::text)
), pick(k, used, depth, pos, player_id, name, note, mastery) AS (
  SELECT 0::bigint, ARRAY[]::integer[], NULL::integer, NULL::text, NULL::integer, NULL::text, NULL::numeric, NULL::text
  UNION ALL
  SELECT s.k, p_1.used || c.player_id, s.depth, s.pos, c.player_id, c.name, c.note, 'maîtrisé'::text
  FROM pick p_1
  JOIN slots s ON s.k = (p_1.k + 1)
  LEFT JOIN LATERAL (
    SELECT c_1.player_id, c_1.name, c_1.grp, c_1.note, c_1.slot_pos, c_1.adj
    FROM cand c_1
    WHERE c_1.slot_pos = s.pos AND (c_1.player_id <> ALL (array_remove(p_1.used, NULL::integer)))
    ORDER BY c_1.adj DESC
    LIMIT 1) c ON true
), saved AS (
  SELECT dc.depth, dc.pos, dc.short_name, dc.injured FROM silver.hw_depth_chart dc
)
SELECT p.depth, p.pos, p.name AS propose, p.note, p.mastery,
       sv.short_name || CASE WHEN sv.injured THEN ' (blessé)'::text ELSE ''::text END AS actuel,
       CASE
         WHEN p.name IS NULL AND p.depth = 1 THEN '🟥 aucun boursier valide'::text
         WHEN p.name IS NULL THEN '— vide (un joueur peut doubler deux postes)'::text
         WHEN COALESCE(sv.short_name, '-'::text) = '-'::text THEN '🟧 à saisir'::text
         WHEN sv.short_name <> ((left(p.name, 1) || '. '::text) || substr(p.name, strpos(p.name, ' '::text) + 1)) OR sv.injured THEN '🟧 à changer'::text
         ELSE '✔'::text
       END AS controle
FROM pick p
LEFT JOIN saved sv ON sv.depth = p.depth AND sv.pos = p.pos
WHERE p.k > 0
ORDER BY p.depth, CASE p.pos WHEN 'PG' THEN 1 WHEN 'SG' THEN 2 WHEN 'SF' THEN 3 WHEN 'PF' THEN 4 ELSE 5 END;

create or replace view gold.hw_daily_alerts with (security_invoker = true) as
WITH ds AS MATERIALIZED (SELECT * FROM gold.hw_depth_suggest),
     ex AS MATERIALIZED (SELECT quoi, statut FROM gold.hw_exports_state),
     rec AS (
       SELECT points, points_max FROM silver.hw_recruiting
       WHERE captured_at = (SELECT max(captured_at) FROM silver.hw_recruiting)
       LIMIT 1)
SELECT prio, niveau, categorie, alerte
FROM (
  SELECT 1 AS prio, '🟥 URGENT'::text AS niveau, 'Composition'::text AS categorie,
         'Depth chart : ' || ds.pos || ' rang ' || ds.depth || ' = ' || ds.actuel || ', mettre ' || ds.propose AS alerte
  FROM ds WHERE ds.controle = '🟧 à changer' AND ds.depth = 1
  UNION ALL
  SELECT 1, '🟥 URGENT', 'Personnel',
         'Dernier jour pour changer un assistant (conférence dans ' || t.jours_avant_conference || ' j) : voir gold.hw_coach_board'
  FROM gold.hw_today t WHERE t.jours_avant_conference BETWEEN 0 AND 2
  UNION ALL
  SELECT 1, '🟥 URGENT', 'Export', ex.quoi || ' : ' || ex.statut FROM ex WHERE ex.statut LIKE '🟥%'
  UNION ALL
  SELECT 2, '🟧 IMPORTANT', 'Académie/Draft',
         'Points de recrutement ' || rec.points || '/' || rec.points_max || ' : au-delà de 45 ils sont perdus, les dépenser'
  FROM rec WHERE rec.points >= rec.points_max - 5
  UNION ALL
  SELECT 2, '🟧 IMPORTANT', 'Composition',
         'Depth chart : ' || ds.pos || ' rang ' || ds.depth || ' = ' || COALESCE(ds.actuel, 'vide') || ', mettre ' || ds.propose
  FROM ds WHERE ds.controle IN ('🟧 à changer', '🟧 à saisir') AND ds.depth > 1
  UNION ALL
  SELECT 2, '🟧 IMPORTANT', 'Analyse', 'Overwork au dernier match : ' || x.my_overworked
  FROM (SELECT my_overworked FROM gold.hw_season_games ORDER BY game_day DESC LIMIT 1) x
  WHERE COALESCE(x.my_overworked, 'none') NOT IN ('none', '')
  UNION ALL
  SELECT 3, '🟩 SUIVI', 'Export', ex.quoi || ' : ' || ex.statut FROM ex WHERE ex.statut LIKE '🟧%'
) a
ORDER BY prio, categorie;

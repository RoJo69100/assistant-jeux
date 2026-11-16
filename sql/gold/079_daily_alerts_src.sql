-- Alertes du jour : règles core.alert_rule + anciennes vues par jeu (source de gold.daily_alerts).
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view gold.daily_alerts_src with (security_invoker = true) as
WITH r AS (
         SELECT alert_rule.game,
            alert_rule.rule_id,
            alert_rule.priority,
            alert_rule.domaine,
            alert_rule.declencheur,
            alert_rule.competition_kind,
            alert_rule.seuil_bas,
            alert_rule.seuil_haut,
            alert_rule.modele,
            alert_rule.source,
            alert_rule.actif
           FROM core.alert_rule
          WHERE alert_rule.actif
        ), ech AS (
         SELECT game_params.game,
            game_params.key,
            (game_params.value ->> 'min'::text)::numeric AS lo,
            (game_params.value ->> 'max'::text)::numeric AS hi
           FROM core.game_params
          WHERE game_params.key = ANY (ARRAY['echelle_fatigue'::text, 'echelle_form'::text])
        ), dernier AS (
         SELECT player_daily.game,
            player_daily.team_id,
            max(player_daily.day) AS day
           FROM core.player_daily
          GROUP BY player_daily.game, player_daily.team_id
        ), roster AS (
         SELECT p.game,
            p.team_id,
            p.club_label,
            p.player_id,
            p.day,
            p.name,
            p."position",
            p.age,
            p.rating,
            p.form,
            p.fatigue,
            p.morale,
            p.injured,
            p.suspended,
            p.salary,
            p.contract_end,
            p.market_value,
            p.is_academy,
            p.skills,
            p.extras,
            ef.lo + p.fatigue * (ef.hi - ef.lo) AS fatigue_jeu,
            fo.lo + p.form * (fo.hi - fo.lo) AS form_jeu
           FROM core.player_daily p
             JOIN dernier d USING (game, team_id, day)
             LEFT JOIN ech ef ON ef.game = p.game AND ef.key = 'echelle_fatigue'::text
             LEFT JOIN ech fo ON fo.game = p.game AND fo.key = 'echelle_form'::text
        ), al AS (
         SELECT p.game,
            p.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('name', p.name, 'retour', ', retour le '::text || to_char(((p.extras ->> 'injury_return_on'::text)::date)::timestamp with time zone, 'DD/MM'::text)) AS v
           FROM roster p
             JOIN r ON r.game = p.game AND r.declencheur = 'joueur_blesse'::text
          WHERE p.injured
        UNION ALL
         SELECT p.game,
            p.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('name', p.name, 'valeur', round(x.val)) AS jsonb_build_object
           FROM roster p
             JOIN r ON r.game = p.game AND (r.declencheur = ANY (ARRAY['joueur_fatigue'::text, 'joueur_forme'::text]))
             CROSS JOIN LATERAL ( SELECT
                        CASE r.declencheur
                            WHEN 'joueur_fatigue'::text THEN p.fatigue_jeu
                            ELSE p.form_jeu
                        END AS val) x
          WHERE (r.seuil_bas IS NULL OR x.val > r.seuil_bas) AND (r.seuil_haut IS NULL OR x.val <= r.seuil_haut)
        UNION ALL
         SELECT d.game,
            d.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('n', d.n) AS jsonb_build_object
           FROM ( SELECT p.game,
                    p.team_id,
                    count(*) AS n
                   FROM roster p
                  WHERE NOT p.injured AND NOT (EXISTS ( SELECT 1
                           FROM core.market_listing m
                          WHERE m.game = p.game AND m.player_id = p.player_id AND m.is_mine AND m.status ~~ 'live%'::text AND m.ends_at > now()))
                  GROUP BY p.game, p.team_id) d
             JOIN r ON r.game = d.game AND r.declencheur = 'effectif_dispo'::text
          WHERE d.n::numeric <= r.seuil_haut
        UNION ALL
         SELECT e.game,
            e.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('ecran', e.ecran, 'statut', e.statut, 'age_h', e.age_h) AS jsonb_build_object
           FROM gold.exports_state e
             JOIN r ON r.game = e.game AND r.declencheur = 'export_perime'::text
          WHERE e.statut <> '🟩 à jour'::text
        UNION ALL
         SELECT f.game,
            f.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('kind', f.competition_kind, 'round', ('J'::text || f.round_no) || ' '::text, 'day', to_char(f.day::timestamp with time zone, 'DD/MM'::text), 'opponent', f.opponent) AS jsonb_build_object
           FROM core.fixture f
             JOIN r ON r.game = f.game AND r.declencheur = 'match_sans_resultat'::text AND r.competition_kind = f.competition_kind
          WHERE f.my_result IS NULL AND f.day < CURRENT_DATE AND f.day >= (CURRENT_DATE - r.seuil_haut::integer)
        UNION ALL
         SELECT f.game,
            f.team_id,
            r.rule_id,
            r.priority,
            r.domaine,
            r.modele,
            jsonb_build_object('day', to_char(f.day::timestamp with time zone, 'DD/MM'::text), 'kind', f.competition_kind, 'result', f.my_result, 'score', (f.my_score || '-'::text) || f.opp_score, 'opponent', f.opponent) AS jsonb_build_object
           FROM ( SELECT DISTINCT ON (fixture.game) fixture.game,
                    fixture.team_id,
                    fixture.fixture_id,
                    fixture.competition_kind,
                    fixture.round_no,
                    fixture.rounds_total,
                    fixture.day,
                    fixture.scheduled_at,
                    fixture.played,
                    fixture.my_score,
                    fixture.opp_score,
                    fixture.my_result,
                    fixture.opponent,
                    fixture.home,
                    fixture.extras
                   FROM core.fixture
                  WHERE fixture.my_result IS NOT NULL
                  ORDER BY fixture.game, fixture.day DESC, fixture.scheduled_at DESC NULLS LAST) f
             JOIN r ON r.game = f.game AND r.declencheur = 'dernier_match'::text
        ), anciennes AS (
         SELECT 'basketvibe'::text AS game,
            a.priority AS prio,
            a.category AS domaine,
            a.alert AS alerte,
            NULL::text AS club
           FROM gold.bv_daily_alerts a
        UNION ALL
         SELECT 'hockeynation'::text AS text,
            a.prio,
            a.domaine,
            a.alerte,
            NULL::text AS text
           FROM gold.hn_daily_alerts a
        UNION ALL
         SELECT 'teamsoccer'::text AS text,
            a.priority,
            a.category,
            a.alert,
            a.team
           FROM gold.ts_daily_alerts a
        UNION ALL
         SELECT 'sixzeroleague'::text AS text,
            a.priority,
            a.category,
            a.alert,
            NULL::text AS text
           FROM gold.sz_daily_alerts a
        UNION ALL
         SELECT 'hardwood'::text AS text,
            a.prio,
            a.categorie,
            a.alerte,
            NULL::text AS text
           FROM gold.hw_daily_alerts a
        ), equipes AS (
         SELECT DISTINCT ON (player_daily.game, player_daily.team_id) player_daily.game,
            player_daily.team_id,
            player_daily.club_label
           FROM core.player_daily
          ORDER BY player_daily.game, player_daily.team_id, player_daily.day DESC
        )
 SELECT al.game,
    al.team_id,
    al.priority AS prio,
    (ARRAY['🟥 URGENT'::text, '🟧 IMPORTANT'::text, '🟩 SUIVI'::text])[al.priority] AS niveau,
    al.domaine,
    core.remplir(al.modele, al.v) AS alerte,
    al.rule_id,
    q.club_label AS club
   FROM al
     LEFT JOIN equipes q ON q.game = al.game AND q.team_id = al.team_id
UNION ALL
 SELECT a.game,
    NULL::text AS team_id,
    a.prio,
    (ARRAY['🟥 URGENT'::text, '🟧 IMPORTANT'::text, '🟩 SUIVI'::text])[a.prio] AS niveau,
    a.domaine,
    a.alerte,
    r.rule_id,
    a.club
   FROM anciennes a
     JOIN r ON r.game = a.game AND r.declencheur = 'ancienne_vue'::text AND r.domaine = a.domaine;

grant select on gold.daily_alerts_src to assistant_ro;

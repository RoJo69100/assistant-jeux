-- Objectif de match : règle core.objective_rule retenue par match à venir (source de gold.match_objective).
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view gold.match_objective_src with (security_invoker = true) as
WITH joues AS (
         SELECT fixture.game,
            fixture.team_id,
            fixture.my_result,
            row_number() OVER (PARTITION BY fixture.game, fixture.team_id ORDER BY (COALESCE(fixture.scheduled_at, fixture.day::timestamp with time zone)) DESC) AS k
           FROM core.fixture
          WHERE fixture.played AND fixture.my_result IS NOT NULL AND fixture.competition_kind <> 'amical'::text
        ), serie AS (
         SELECT joues.game,
            joues.team_id,
            COALESCE(min(joues.k) FILTER (WHERE joues.my_result <> 'L'::text), max(joues.k) + 1) - 1 AS n_def
           FROM joues
          GROUP BY joues.game, joues.team_id
        ), a_venir AS (
         SELECT f.game,
            f.team_id,
            f.fixture_id,
            f.competition_kind,
            f.round_no,
            f.rounds_total,
            f.day,
            f.scheduled_at,
            f.played,
            f.my_score,
            f.opp_score,
            f.my_result,
            f.opponent,
            f.home,
            f.extras
           FROM core.fixture f
          WHERE NOT f.played AND f.day >= CURRENT_DATE AND f.day <= (CURRENT_DATE + 6)
        ), cand AS (
         SELECT v.game,
            v.team_id,
            v.fixture_id,
            v.day,
            v.scheduled_at,
            v.competition_kind,
            v.opponent,
            v.home,
            COALESCE(s.n_def, 0::bigint) AS n_def,
            c.rank,
            c.n_teams,
            c.gap_to_first,
            c.rounds_left,
            c.parametres_manquants,
            r.rule_id,
            r.objectif,
            r.priorite,
            r.raison,
            r.preuve_erreur,
            row_number() OVER (PARTITION BY v.game, v.team_id, v.fixture_id ORDER BY r.priorite, r.rule_id) AS choix
           FROM a_venir v
             LEFT JOIN serie s ON s.game = v.game AND s.team_id = v.team_id
             LEFT JOIN gold.season_context c ON c.game = v.game AND c.team_id = v.team_id
             LEFT JOIN core.club_strategy cs ON cs.game = v.game AND cs.team_id = v.team_id AND cs.valide_le IS NOT NULL
             JOIN core.objective_rule r ON r.actif AND (r.charte_horizons IS NULL OR (cs.horizon = ANY (r.charte_horizons))) AND (r.game IS NULL OR r.game = v.game) AND (r.competition_kind IS NULL OR r.competition_kind = v.competition_kind) AND
                CASE r.condition
                    WHEN 'serie_defaites'::text THEN v.competition_kind <> 'amical'::text AND COALESCE(s.n_def, 0::bigint) >= 2
                    WHEN 'titre_acquis'::text THEN COALESCE(c.titre_acquis, false)
                    WHEN 'rien_a_jouer'::text THEN COALESCE(c.rien_a_jouer, false)
                    ELSE true
                END
        )
 SELECT game,
    team_id,
    fixture_id,
    day,
    scheduled_at,
    competition_kind,
    opponent,
    home,
    objectif,
    replace(replace(replace(replace(replace(replace(raison, '{n_def}'::text, n_def::text), '{rank}'::text, COALESCE(rank::text, '?'::text)), '{n_teams}'::text, COALESCE(n_teams::text, '?'::text)), '{gap_first}'::text, COALESCE(gap_to_first::text, '?'::text)), '{left}'::text, COALESCE(rounds_left::text, '?'::text)), '{manquants}'::text,
        CASE
            WHEN COALESCE(parametres_manquants, 'contexte de saison absent'::text) = ''::text THEN ''::text
            ELSE ' ; contexte incomplet : '::text || COALESCE(parametres_manquants, 'contexte de saison absent'::text)
        END) AS raison,
    preuve_erreur,
    n_def AS defaites_d_affilee,
    rule_id
   FROM cand
  WHERE choix = 1
  ORDER BY game, day, scheduled_at;

grant select on gold.match_objective_src to assistant_ro;

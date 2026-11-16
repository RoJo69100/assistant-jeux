-- DerbyManager : joueurs de l'effectif avec note de poste, verdict et intensité conseillée.
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view gold.dm_joueurs with (security_invoker = true) as
WITH ids AS (
         SELECT dm_player_ids.player_id,
            dm_player_ids.name
           FROM silver.dm_player_ids
        ), tp AS (
         SELECT t.team_id,
            t.player_id,
            i.name,
            t.tips,
            array_to_string(t.tips, ' | '::text) AS tt
           FROM silver.dm_player_tips t
             JOIN ids i USING (player_id)
        ), e AS (
         SELECT p.team_id,
            p.club,
            p.name,
            p.pos,
            p.age,
            p.tier,
            p.role,
            p.slot,
            p.price,
            p.salary,
            p.contract_days,
            p.pot,
            p.note_gk,
            p.note_def,
            p.note_mil,
            p.note_att,
            p.note_poste,
            p.ligne,
            x.tt,
            s.tr,
            s.form,
            s.sharpness,
            s.condition_pct,
            s.pt,
            s.intensity,
            s.fit,
            s.exp,
            s.skill,
            s.bu,
            s.pbu,
            s.satisfaction_pct AS effet_ts_pct,
            s.sta,
            silver.dm_n(split_part(s.tr, '/'::text, 1))::integer AS jours_sans_match,
            silver.dm_n(split_part(s.tr, '/'::text, 2))::integer AS tr_exigence,
            row_number() OVER (PARTITION BY p.team_id, p.ligne ORDER BY p.note_poste DESC) AS rang_ligne
           FROM gold.dm_poste_scores p
             JOIN silver.dm_squad s ON s.team_id = p.team_id AND s.name = p.name
             LEFT JOIN tp x ON x.team_id = p.team_id AND x.name = p.name
        )
 SELECT team_id,
    club,
        CASE ligne
            WHEN 1 THEN 'GK'::text
            WHEN 2 THEN 'D'::text
            WHEN 3 THEN 'M'::text
            ELSE 'F'::text
        END AS ligne,
    rang_ligne,
    name,
    pos,
    age,
    note_poste,
        CASE
            WHEN note_poste >= 14::numeric THEN 'fort'::text
            WHEN note_poste >= 12::numeric THEN 'moyen'::text
            ELSE 'faible'::text
        END AS niveau_equipe,
    tier,
    skill AS etoiles_equipe,
    pot AS pot_0_3,
    exp AS exp_0_3,
    fit AS fitness_0_3,
    bu,
    pbu,
    condition_pct AS condition,
    form AS forme,
    "substring"(tt, 'Form is (\w+ and \w+ \w+)'::text) AS forme_txt,
    "substring"(tt, '(Confident|Reliable|Inconsistent|Volatile|Doubtful|Nervous|Uncertain)[^|]*'::text) AS coeur_txt,
    sharpness AS coeur_1_4,
    pt AS temps_jeu_satisf_pct,
    role AS statut_contrat,
    "substring"(tt, '(Leader|Regular|Outsider):'::text) AS statut_vestiaire,
    effet_ts_pct,
    intensity,
    jours_sans_match,
    tr_exigence,
    jours_sans_match > tr_exigence AS ne_s_entraine_pas,
    "substring"(tt, '(Nearing his growth limit at this club\.|Is close to his growth limit at this club\.|Could use better training facilities and mentors\.|Unhappy with training facilities and mentors\.|Furious with training facilities and mentors\.|His training isn''t a priority anymore\.|Has no training-related complaints)'::text) AS entrainement_txt,
    tt ~ 'Provides mentoring'::text AS mentor,
    "substring"(tt, '(Bruised[^|]*|Injured[^|]*)'::text) AS blessure,
    tt ~ 'One yellow away from red'::text AS un_jaune_du_rouge,
    tt ~ 'Wants to retire'::text AS veut_retraite,
    "substring"(tt, '(Individualistic|Team player|Easygoing|Balanced|Slow-burner|Fast-burner|Determined|Territorial|Hard working|Relentless|Influential)[^|]*'::text) AS personnalite,
    "substring"(tt, '((Hard-working|Tenacious|Influential|Determined|Relentless) leader)'::text) AS trait_leader,
    contract_days,
    salary,
    price,
        CASE
            WHEN condition_pct < 80::numeric THEN 'repos (condition < 80 %)'::text
            WHEN ligne = 1 AND rang_ligne = 1 OR ligne = 2 AND rang_ligne <= 5 OR ligne = 3 AND rang_ligne <= 4 OR ligne = 4 AND rang_ligne = 1 THEN 'titulaire 541'::text
            WHEN age <= 21 AND pot >= 2 THEN 'jeune à faire jouer (amical, DEV)'::text
            WHEN ligne = 1 AND rang_ligne >= 3 OR ligne = 2 AND rang_ligne >= 8 OR ligne = 3 AND rang_ligne >= 7 OR ligne = 4 AND rang_ligne >= 3 THEN 'surplus : vendre'::text
            ELSE 'remplaçant'::text
        END AS verdict,
        CASE
            WHEN condition_pct < 80::numeric THEN 'LOW'::text
            WHEN age >= 30 THEN 'LOW'::text
            WHEN age <= 23 AND pot >= 2 THEN 'HIGH'::text
            ELSE 'MED'::text
        END AS intensite_conseillee
   FROM e;

grant select on gold.dm_joueurs to assistant_ro;

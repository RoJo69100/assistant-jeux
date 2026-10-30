-- Derby Manager : infobulles du jeu, verdict joueur par joueur, plan d'entraînement. Conçu le 2026-10-30.
-- Les infobulles (data-bs-title) de la page d'équipe donnent le sens exact des colonnes et l'état de chaque joueur :
-- forme (« Form is superb and growing slow »), cœur = sharpness (Confident / Reliable / Inconsistent / Volatile),
-- satisfaction de temps de jeu, statut de vestiaire (Leader / Regular / Outsider), plaintes d'entraînement,
-- mentor, retraite, blessure, cartons, personnalité, trait de capitaine.
-- Créées par execute_sql (pas de DROP) : gold.dm_joueurs (première version, remplacée) reste en base à supprimer.

create or replace view silver.dm_player_tips with (security_invoker = true) as
with src as (
  select s.team_id, s.captured_at, b.payload->>'html' as html
  from silver.dm_team_src s join bronze.raw_pages b on b.id = s.capture_id
), seg as (
  select team_id, captured_at, x as seg,
         coalesce(substring(x from '^[^>]*player-id="(\d+)"'), substring(x from 'href="/players/(\d+)"'))::int as player_id
  from src cross join lateral regexp_split_to_table(src.html, '<tr[ >]') x
)
select team_id, max(captured_at) as captured_at, player_id, array_agg(distinct t[1]) as tips
from seg cross join lateral regexp_matches(seg, 'data-bs-title="([^"]{3,200})"', 'g') t
where player_id is not null
group by team_id, player_id;

-- Verdict : 541 (GK 1, D 5, M 4, F 1). Ordre des règles : blessé > condition < 80 % > Key/First team sous 50 % de
-- temps de jeu (doit jouer) > titulaire > veut sa retraite > surplus (au-delà de titulaires + 2, plus de 21 ans) > jeune.
-- ne_s_entraine_pas : jours depuis le dernier match (TR « a/b ») > exigence b ⇒ aucun entraînement jusqu'au prochain match.
-- intensite_conseillee [H] : LOW si blessé, condition < 80 %, 30 ans+ ou « training isn't a priority » ; HIGH si ≤ 23 ans et POT ≥ 2.
create or replace view gold.dm_verdict_joueurs with (security_invoker = true) as
with ids as (select player_id, name from silver.dm_player_ids),
tp as (
  select t.team_id, i.name, array_to_string(t.tips, ' | ') as tt
  from silver.dm_player_tips t join ids i using (player_id)
),
e as (
  select p.*, x.tt, s.tr, s.form, s.sharpness, s.condition_pct, s.pt, s.intensity, s.fit, s.exp, s.skill, s.bu, s.pbu,
         s.satisfaction_pct as effet_ts_pct,
         silver.dm_n(split_part(s.tr, '/', 1))::int as jours_sans_match,
         silver.dm_n(split_part(s.tr, '/', 2))::int as tr_exigence,
         row_number() over (partition by p.team_id, p.ligne order by p.note_poste desc) as rang_ligne
  from gold.dm_poste_scores p
  join silver.dm_squad s on s.team_id = p.team_id and s.name = p.name
  left join tp x on x.team_id = p.team_id and x.name = p.name
)
select e.team_id, e.club,
       case e.ligne when 1 then 'GK' when 2 then 'D' when 3 then 'M' else 'F' end as ligne,
       e.rang_ligne, e.name, e.pos, e.age, e.note_poste,
       case when e.note_poste >= 14 then 'fort' when e.note_poste >= 12 then 'moyen' else 'faible' end as niveau_equipe,
       e.tier, e.skill as etoiles_equipe, e.pot as pot_0_3, e.exp as exp_0_3, e.fit as fitness_0_3, e.bu, e.pbu,
       e.condition_pct as condition, e.form as forme,
       substring(e.tt from 'Form is (\w+ and growing \w+)') as forme_txt,
       substring(e.tt from '(Confident|Reliable|Inconsistent|Volatile) - ') as coeur_txt,
       e.pt as temps_jeu_satisf_pct, e.role as statut_contrat,
       case e.role when 'Key' then 75 when 'First team' then 60 when 'Rotation' then 40 else 25 end as temps_jeu_attendu_pct,
       substring(e.tt from '(Leader|Regular|Outsider): ') as statut_vestiaire, e.effet_ts_pct,
       e.intensity, e.jours_sans_match, e.tr_exigence,
       e.jours_sans_match > e.tr_exigence as ne_s_entraine_pas,
       substring(e.tt from '(Nearing his growth limit at this club|Is close to his growth limit at this club|Could use better training facilities and mentors|Unhappy with training facilities and mentors|Furious with training facilities and mentors|His training isn''t a priority anymore|Has no training-related complaints)') as entrainement_txt,
       (e.tt ~ 'Provides mentoring') as mentor,
       substring(e.tt from '(Bruised for \d+ match[^|]*|Injured[^|]*)') as blessure,
       (e.tt ~ 'One yellow away from red') as un_jaune_du_rouge,
       (e.tt ~ 'Wants to retire') as veut_retraite,
       substring(e.tt from '(Individualistic|Team player|Easygoing|Balanced|Slow-burner|Fast-burner|Hard working|Relentless|Territorial|Determined|Influential): ') as personnalite,
       substring(e.tt from '((?:Hard-working|Tenacious|Influential|Determined|Relentless) leader)') as trait_capitaine,
       e.contract_days, e.salary, e.price,
       case
         when e.tt ~ 'Bruised|Injured' then 'blessé : banc'
         when e.condition_pct < 80 then 'repos (condition < 80 %)'
         when e.role in ('Key', 'First team') and e.pt < 50 then 'doit jouer (temps de jeu)'
         when e.ligne = 1 and e.rang_ligne = 1 or e.ligne = 2 and e.rang_ligne <= 5 or e.ligne = 3 and e.rang_ligne <= 4 or e.ligne = 4 and e.rang_ligne = 1 then 'titulaire 541'
         when e.tt ~ 'Wants to retire' then 'part à la retraite : laisser finir'
         when (e.ligne = 1 and e.rang_ligne >= 3 and e.age > 21) or (e.ligne = 2 and e.rang_ligne >= 8 and e.age > 21) or (e.ligne = 3 and e.rang_ligne >= 7 and e.age > 21) or (e.ligne = 4 and e.rang_ligne >= 3 and e.age > 21) then 'surplus : vendre'
         when e.age <= 21 and e.pot >= 2 then 'jeune : amical + banc DEV'
         else 'remplaçant' end as verdict,
       case when e.tt ~ 'Bruised|Injured' or e.condition_pct < 80 or e.age >= 30 or e.tt ~ 'training isn''t a priority' then 'LOW'
            when e.age <= 23 and e.pot >= 2 then 'HIGH'
            else 'MED' end as intensite_conseillee
from e;

-- Plan d'entraînement : par groupe, moyenne de chaque compétence clé ; conseille = la plus basse
-- (développeur : « train skills that are low/moderate for majority », 1→2 facile, 19→20 dur).
create or replace view gold.dm_entrainement_plan with (security_invoker = true) as
with g as (select team_id, grp_name, training, tec_lvl, dec_lvl, mov_lvl from silver.dm_training_groups),
j as (
  select e.*, case when e.pos ~ '^GK' then 'Goalkeepers' when e.pos ~ '^D' then 'Defenders' when e.pos ~ '^M' then 'Midfielders' else 'Forwards' end as grp_name
  from gold.dm_effectif e
),
sk(code, nom, categorie, cle_gk, cle_d, cle_m, cle_f) as (values
  ('han','Handling','Tactic',true,false,false,false), ('rea','Reaction','Tactic',true,false,false,false),
  ('tac','Tackling','Tactic',false,true,true,false), ('pas','Passing','Tactic',false,false,true,false),
  ('fir','First Touch','Tactic',false,false,true,true), ('sho','Shooting','Tactic',false,false,false,true),
  ('posi','Positioning','Decisions',true,true,false,false), ('ant','Anticipation','Decisions',false,true,true,false),
  ('cre','Creativity','Decisions',false,false,true,false), ('tec','Technique','Decisions',false,false,true,true),
  ('acc','Accuracy','Decisions',false,false,false,true),
  ('mar','Marking','Movement',false,true,false,false), ('aer','Aerial','Movement',true,true,false,false),
  ('agi','Agility','Movement',true,false,false,true), ('bal','Ball Control','Movement',false,false,true,false),
  ('hea','Headers','Movement',false,false,false,true)
),
moy as (
  select j.team_id, j.grp_name, sk.code, sk.nom, sk.categorie,
         case j.grp_name when 'Goalkeepers' then sk.cle_gk when 'Defenders' then sk.cle_d when 'Midfielders' then sk.cle_m else sk.cle_f end as cle,
         round(avg((to_jsonb(j) ->> sk.code)::numeric), 1) as moyenne, count(*) as joueurs
  from j cross join sk
  group by 1, 2, 3, 4, 5, 6
)
select m.team_id, m.grp_name as groupe, g.training as actuel, g.tec_lvl, g.dec_lvl, g.mov_lvl,
       m.nom as competence, m.categorie, m.moyenne, m.joueurs,
       rank() over (partition by m.team_id, m.grp_name order by m.moyenne) = 1 as conseille
from moy m left join g on g.team_id = m.team_id and g.grp_name = m.grp_name
where m.cle;

-- Hardwood : fiches des recrues, en deux temps (demande de l'utilisateur, 2026-10-30).
--   1. gold.hw_recrues_a_ouvrir : les prospects du board dont la page joueur n'est pas encore en base (à ouvrir).
--   2. gold.hw_recrue_fiches : une ligne par recrue ouverte, note /5 au meilleur poste, comparable à gold.hw_roster_notes.
-- Mêmes barèmes que 045_hw_notes.sql :
--   note_now     = (niveau SI + adéquation des compétences clés actuelles) / 2 — même échelle que nos boursiers.
--   note_plafond = (avenir + adéquation au plafond) / 2. Plafond d'une compétence clé = milieu de la fourchette de la phrase du scout
--                  (silver.hw_ref_scout_phrases), jamais sous la valeur actuelle ; sans phrase = valeur actuelle (« non dit »).
-- Valeurs affichées des recrues : ±20 % (hardwood-regles). Verdict et seuils [H] : à confronter aux engagements et aux matchs.

-- Fiche joueur la plus récente des joueurs qui ne sont pas chez nous, compétences lues dans le tableau 0.
create or replace view silver.hw_recruit_page with (security_invoker = true) as
with last as (
  select distinct on (p.url_id) p.url_id as player_id, p.captured_at, p.tables->0 as t
  from silver.hw_pages p
  where p.page_type = 'player_id'
    and p.url_id not in (select player_id from silver.hw_roster where player_id is not null)
  order by p.url_id, p.captured_at desc
), flat as (
  select l.*, (select string_agg(x::text, ' ') from jsonb_array_elements(l.t->'rows') x) as txt
  from last l
), sk as (
  select l.player_id,
         jsonb_object_agg(trim(trailing ':' from trim(c.label)), nullif(regexp_replace(c.val, '\D', '', 'g'), '')::int) as skills
  from last l
  cross join lateral jsonb_array_elements(l.t->'rows') r
  cross join lateral (values (r->>1, r->>2), (r->>3, r->>4)) c(label, val)
  where jsonb_array_length(r) >= 3 and coalesce(c.label, '') <> '' and c.val ~ '^\s*\d'  -- « Potential » est sur une ligne de 3
  group by l.player_id
)
select f.player_id, f.captured_at,
       trim(split_part(f.t->'headers'->>0, '[', 1)) as name,
       substring(f.txt from 'Position\(s\): ([A-Za-z ]+?)\s*"') as positions,
       substring(f.txt from 'Class: (.+?)\s{2,}') as class_long,
       substring(f.txt from 'Height: ([\d.]+) m')::numeric as height_m,
       substring(f.txt from 'Projected Height: ([\d.]+) m')::numeric as projected_height_m,
       (sk.skills->>'Skill Index')::int as si, (sk.skills->>'Potential')::int as pot,
       (sk.skills->>'Inside Shot')::int as ins, (sk.skills->>'Outside Shot')::int as os,
       (sk.skills->>'Shooting Range')::int as rng, (sk.skills->>'Finishing')::int as fin,
       (sk.skills->>'Rebounding')::int as reb, (sk.skills->>'Interior Defense')::int as idef,
       (sk.skills->>'Perimeter Defense')::int as pdef, (sk.skills->>'Basketball IQ')::int as iq,
       (sk.skills->>'Passing')::int as pass, (sk.skills->>'Ball Handling')::int as hnd,
       (sk.skills->>'Driving')::int as drv, (sk.skills->>'Strength')::int as str,
       (sk.skills->>'Speed')::int as spd, (sk.skills->>'Stamina')::int as sta,
       trim(substring(f.txt from 'Recruiting Evaluation: (.*?) Projected Height')) as evaluation,
       substring(f.txt from 'College List: ([^"]*)') as college_list
from flat f join sk using (player_id);

-- Phrases du scout de chaque recrue, reconnues ou non par la table de référence.
create or replace view silver.hw_recruit_phrases with (security_invoker = true) as
select p.player_id, trim(ph) as phrase, r.skill, r.min_val, r.max_val, r.note
from silver.hw_recruit_page p
cross join lateral regexp_split_to_table(p.evaluation, '\.\s*') ph
left join silver.hw_ref_scout_phrases r on r.phrase = trim(ph)
where trim(ph) <> '';

-- Notes par recrue et par groupe de postes (PG, SG, SF, Grand), actuelles et au plafond.
create or replace view gold.hw_recruit_group_notes with (security_invoker = true) as
with cap as (
  select player_id,
         max((min_val + max_val) / 2.0) filter (where skill = 'ins')  as c_ins,
         max((min_val + max_val) / 2.0) filter (where skill = 'os')   as c_os,
         max((min_val + max_val) / 2.0) filter (where skill = 'reb')  as c_reb,
         max((min_val + max_val) / 4.0) filter (where skill = 'id_pd') as c_def,
         max((min_val + max_val) / 2.0) filter (where skill = 'pdef') as c_pdef,
         max((min_val + max_val) / 2.0) filter (where skill = 'idef') as c_idef,
         max((min_val + max_val) / 2.0) filter (where skill = 'iq')   as c_iq,
         max((min_val + max_val) / 2.0) filter (where skill = 'pass') as c_pass,
         max((min_val + max_val) / 2.0) filter (where skill = 'hnd')  as c_hnd,
         max((min_val + max_val) / 2.0) filter (where skill = 'spd')  as c_spd,
         bool_or(phrase in ('Is a troubled kid and may not be college material',
                            'Isn''t much of a student and may not qualify academically',
                            'May choose to play overseas instead of going to college')) as risque_5050,
         bool_or(phrase = 'Is eager to commit early') as engage_tot,
         string_agg(phrase, ' · ') filter (where skill is null) as phrases_hors_ref
  from silver.hw_recruit_phrases group by player_id
), v as (
  select p.*, c.risque_5050, c.engage_tot, c.phrases_hors_ref,
         -- plafond par compétence clé : milieu de la phrase, jamais sous l'actuel
         greatest(p.ins, coalesce(c.c_ins, p.ins)) as x_ins, greatest(p.os, coalesce(c.c_os, p.os)) as x_os,
         greatest(p.reb, coalesce(c.c_reb, p.reb)) as x_reb, greatest(p.iq, coalesce(c.c_iq, p.iq)) as x_iq,
         greatest(p.pass, coalesce(c.c_pass, p.pass)) as x_pass, greatest(p.hnd, coalesce(c.c_hnd, p.hnd)) as x_hnd,
         greatest(p.spd, coalesce(c.c_spd, p.spd)) as x_spd,
         greatest((p.idef + p.pdef) / 2.0,
                  coalesce(c.c_def, (coalesce(c.c_idef, p.idef) + coalesce(c.c_pdef, p.pdef)) / 2.0)) as x_def,
         c.c_ins, c.c_os, c.c_reb, c.c_iq, c.c_pass, c.c_hnd, c.c_spd,
         coalesce(c.c_def, c.c_idef, c.c_pdef) as c_def_any
  from silver.hw_recruit_page p left join cap c using (player_id)
), g(grp, ord, slots) as (values ('PG', 1, 1), ('SG', 2, 1), ('SF', 3, 1), ('Grand', 4, 2)),
k as (
  select v.*, g.grp, g.ord, g.slots,
         case g.grp when 'PG' then (iq + pass + hnd + spd) / 4.0 when 'SG' then (os + spd) / 2.0
                    when 'SF' then (os + (idef + pdef) / 2.0 + spd) / 3.0 else (ins + reb) / 2.0 end as cles,
         case g.grp when 'PG' then (x_iq + x_pass + x_hnd + x_spd) / 4.0 when 'SG' then (x_os + x_spd) / 2.0
                    when 'SF' then (x_os + x_def + x_spd) / 3.0 else (x_ins + x_reb) / 2.0 end as cles_plafond,
         case g.grp when 'PG' then (c_iq is null)::int + (c_pass is null)::int + (c_hnd is null)::int + (c_spd is null)::int
                    when 'SG' then (c_os is null)::int + (c_spd is null)::int
                    when 'SF' then (c_os is null)::int + (c_def_any is null)::int + (c_spd is null)::int
                    else (c_ins is null)::int + (c_reb is null)::int end as cles_non_dites
  from v cross join g
), n as (
  select k.*,
         case when si >= 140 then 5 when si >= 125 then 4 when si >= 110 then 3 when si >= 95 then 2 else 1 end as niveau,
         case when cles >= 15 then 5 when cles >= 13 then 4 when cles >= 11 then 3 when cles >= 9 then 2 else 1 end as adequation,
         case when cles_plafond >= 15 then 5 when cles_plafond >= 13 then 4 when cles_plafond >= 11 then 3
              when cles_plafond >= 9 then 2 else 1 end as adequation_plafond,
         case when pot >= 13 then 5 when pot = 12 then 4 when pot = 11 then 3 when pot = 10 then 2 else 1 end as avenir
  from k
)
select player_id, name, grp, ord, slots, positions, si, pot, coalesce(projected_height_m, height_m) as height_m,
       round(cles, 1) as cles, round(cles_plafond, 1) as cles_plafond, cles_non_dites,
       niveau, adequation, round((niveau + adequation) / 2.0, 1) as note_now,
       avenir, adequation_plafond, round((avenir + adequation_plafond) / 2.0, 1) as note_plafond,
       case when coalesce(positions, '') ~ (case grp when 'Grand' then '(^|\s)(PF|C)(\s|$)' else '(^|\s)' || grp || '(\s|$)' end) then 'maîtrisé'
            when coalesce(positions, '') ~* (case grp when 'Grand' then '(^|\s)(pf|c)(\s|$)' else '(^|\s)' || grp || '(\s|$)' end) then 'apprentissage'
            else 'jamais' end as mastery,
       coalesce(projected_height_m, height_m) >= 1.95 or grp <> 'Grand' as height_ok,
       coalesce(risque_5050, false) as risque_5050, coalesce(engage_tot, false) as engage_tot, phrases_hors_ref,
       ins, os, rng, fin, reb, idef, pdef, iq, pass, hnd, drv, str, spd, sta
from n;

-- Fiche finale : meilleur poste jouable (listé dans Positions, taille OK), comparaison à nos boursiers qui restent l'an prochain.
-- Verdict [H] : offrir = plafond ≥ 4 et au plus 2 × places (PG/SG/SF 1, Grand 2) boursiers restants mieux notés aujourd'hui ;
--               réserve = plafond ≥ 3,5 ; rejeter sinon (ou aucun poste jouable). Risque 50/50 signalé, pas éliminatoire.
create or replace view gold.hw_recrue_fiches with (security_invoker = true) as
with best as (
  select distinct on (player_id) *
  from gold.hw_recruit_group_notes
  where mastery <> 'jamais' and height_ok
  order by player_id, note_plafond desc, note_now desc, (mastery = 'maîtrisé') desc, ord
), stay as (
  select groupe, note from gold.hw_roster_notes where not part_fin_saison
), b as (
  select distinct on (prospect) prospect, class, state, region, stars, teams_interested, teams_high, our_interest, we_offered, contacts
  from gold.hw_recruit_board order by prospect, contacts nulls last
), f as (
  select p.player_id, p.name, coalesce(bt.grp, '—') as poste, bt.mastery, p.positions, b.class, b.state, b.region, b.stars,
         coalesce(bt.height_m, coalesce(p.projected_height_m, p.height_m)) as height_m, p.si, p.pot,
         bt.cles, bt.cles_plafond, bt.cles_non_dites, bt.note_now, bt.note_plafond, bt.slots,
         (select count(*) from stay s where s.groupe = bt.grp and s.note > bt.note_now) as boursiers_devant,
         (select max(s.note) from stay s where s.groupe = bt.grp) as meilleure_note_poste,
         b.teams_interested, b.teams_high, b.our_interest, b.we_offered, b.contacts,
         coalesce(bt.risque_5050, false) as risque_5050, coalesce(bt.engage_tot, false) as engage_tot, bt.phrases_hors_ref,
         p.evaluation, p.captured_at
  from silver.hw_recruit_page p
  left join best bt using (player_id)
  left join b on b.prospect = p.name
)
select case when poste = '—' then '— rejeter (aucun poste jouable : taille ou postes)'
            when note_plafond >= 4 and boursiers_devant < 2 * slots then '🟥 offrir'
            when note_plafond >= 3.5 then '🟧 réserve'
            else '— rejeter (plafond < 3,5)' end
       || case when risque_5050 then ' · risque 50/50' else '' end as verdict,
       name, poste, mastery, positions, class, state, stars, height_m, si, pot,
       note_now, note_plafond, cles, cles_plafond, cles_non_dites, boursiers_devant, meilleure_note_poste,
       teams_interested, teams_high, our_interest, we_offered, contacts, engage_tot, phrases_hors_ref, evaluation, player_id, captured_at
from f
order by case when poste = '—' then 3 when note_plafond >= 4 and boursiers_devant < 2 * slots then 0
              when note_plafond >= 3.5 then 1 else 2 end,
         note_plafond desc nulls last, note_now desc nulls last;

-- Étape 1 : prospects engageables du board dont la page joueur n'est pas en base, dans l'ordre du board.
create or replace view gold.hw_recrues_a_ouvrir with (security_invoker = true) as
select b.verdict, b.rang, b.prospect, b.class, b.pos, b.height_m, b.state, b.si, b.pot, b.stars, b.top_skills,
       b.teams_interested, b.teams_high
from gold.hw_recruit_board b
where b.engageable_cette_saison
  and b.verdict in ('cible', 'cible hors région', 'secondaire')
  and not exists (select 1 from silver.hw_recruit_page p where p.name = b.prospect)
order by case b.verdict when 'cible' then 1 when 'cible hors région' then 2 else 3 end, b.rang;

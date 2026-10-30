-- Hardwood : pages joueur, développement, depth chart, recherche de prospects, coachs libres, classement RPI,
-- et tables de référence corrigées avec le document d'aide de l'utilisateur (data/manual/hardwoord/Aide docs.txt, 2026-10-30).
-- Walk-ons : leurs pages joueur ne sont PAS exportées (décision de l'utilisateur, 2026-10-30) ; le roster suffit.

-- Fiche joueur (/player/<id>) : attributs physiques et évaluation du scout (phrases qui fixent les plafonds).
create or replace view silver.hw_player_profile with (security_invoker = true) as
with p as (
  select p.captured_at, p.url_id as player_id, p.tables->0->'rows' as r,
         (select string_agg(x::text, ' ') from jsonb_array_elements(p.tables->0->'rows') x) as flat
  from silver.hw_pages p
  where p.page_type = 'player_id'
)
select player_id, i.name, captured_at,
       substring(flat from 'Age: (\d+)')::int as age,
       substring(flat from 'Shoots: (\w+)') as shoots,
       substring(flat from 'Weight: (\d+) kgs')::int as weight_kg,
       substring(flat from 'Wingspan: ([\d.]+) m')::numeric as wingspan_m,
       substring(flat from 'Vertical: ([\d.]+) cm')::numeric as vertical_cm,
       substring(flat from 'Home Town: (.+?)  ') as hometown,
       substring(flat from 'Junior College: (.+?)  ') as junior_college,
       substring(flat from 'Projected Height: ([\d.]+) m')::numeric as projected_height_m,
       trim(substring(flat from 'Recruiting Evaluation: (.*?) Projected Height')) as evaluation
from p left join silver.hw_player_ids i using (player_id);

-- Progression (/development/<notre id>) : valeur + flèche après chaque compétence (↑ = montée à la dernière mise à jour du coaching).
create or replace view silver.hw_development with (security_invoker = true) as
select p.captured_at, r->>0 as class, r->>1 as pos, r->>2 as name, (r->>3)::int as age,
       (r->>33)::int as si, (r->>34) = '↑' as si_up,
       array_remove(array[
         case when r->>6  = '↑' then 'IS' end,  case when r->>8  = '↑' then 'OS' end,
         case when r->>10 = '↑' then 'Rng' end, case when r->>12 = '↑' then 'Fin' end,
         case when r->>14 = '↑' then 'Reb' end, case when r->>16 = '↑' then 'IDef' end,
         case when r->>18 = '↑' then 'PDef' end, case when r->>20 = '↑' then 'IQ' end,
         case when r->>22 = '↑' then 'Pass' end, case when r->>24 = '↑' then 'Hnd' end,
         case when r->>26 = '↑' then 'Drv' end, case when r->>28 = '↑' then 'Str' end,
         case when r->>30 = '↑' then 'Spd' end, case when r->>32 = '↑' then 'Sta' end], null) as skills_up
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'development_id' and p.url_id = o.team_id and jsonb_array_length(r) >= 35;

-- Depth chart enregistré (/depth_chart/<notre id>) : table 0 = plan par défaut. Noms abrégés (« E. Corey »), « +N » = blessé.
create or replace view silver.hw_depth_chart with (security_invoker = true) as
select p.captured_at, (r->>0)::int as depth, x.pos,
       trim(regexp_replace(r->>x.col, '\s*\+\d+$', '')) as short_name,
       (r->>x.col) ~ '\+\d+$' as injured
from silver.hw_pages p
cross join silver.hw_own o
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
cross join (values ('PG', 2), ('SG', 5), ('SF', 8), ('PF', 11), ('C', 14)) x(pos, col)
where p.page_type = 'depth_chart_id' and p.url_id = o.team_id and coalesce(r->>x.col, '') <> '';

-- Recherche de prospects (/prospect_results) : liste des universités intéressées, ✔ = bourse offerte.
create or replace view silver.hw_prospects with (security_invoker = true) as
select p.captured_at, (r->>0)::int as search_rank, r->>1 as class, r->>3 as prospect,
       nullif(r->>4, '')::numeric as height_m, r->>5 as pos, r->>6 as hometown,
       trim(split_part(r->>6, ',', 2)) as state,
       (r->>7)::int as si, (r->>8)::int as pot, nullif(r->>9, '')::int as stars,
       r->>10 as top_skills, r->>11 as hs_stats, r->>12 as college_list,
       coalesce(array_length(regexp_split_to_array(nullif(r->>12, ''), '\),\s*'), 1), 0) as teams_interested,
       substring(r->>12 from 'Eureka \( ?✔? ?([A-Za-z+]+)\)') as our_interest,
       (r->>12) ~ 'Eureka \( ?✔' as we_offered,
       (select count(*) from regexp_matches(coalesce(r->>12, ''), '\(\s*✔?\s*High', 'g')) as teams_high
from silver.hw_pages p
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'prospect_results' and jsonb_array_length(r) >= 13;

-- Coachs (/coach_results) : table 0 = nos assistants, table 1 = candidats (« Available » = libre).
create or replace view silver.hw_coach_market with (security_invoker = true) as
select p.captured_at, substring(p.text from 'To Replace: ([^\n]+)') as to_replace,
       r->>1 as coach, r->>2 as team, (r->>2) = 'Available' as available,
       (r->>3)::int as age, (r->>4)::int as exp,
       (r->>5)::int as off, (r->>6)::int as def, (r->>7)::int as tac, (r->>8)::int as dev,
       (r->>9)::int as mot, (r->>10)::int as rec,
       replace(replace(r->>11, '$', ''), 'M', '')::numeric as salary_m
from silver.hw_pages p
cross join lateral jsonb_array_elements(p.tables->1->'rows') r
where p.page_type = 'coach_results' and jsonb_array_length(r) >= 12 and (r->>3) ~ '^\d+$';

-- Classement national RPI (/rankings) : 50 premiers de notre division.
create or replace view silver.hw_rankings with (security_invoker = true) as
select p.captured_at, (r->>0)::int as rank, r->>1 as team, r->>2 as conference,
       (r->>3)::int as w, (r->>4)::int as l, nullif(r->>7, '')::numeric as rpi, nullif(r->>8, '')::numeric as sos,
       r->>13 as q1, r->>14 as q2, r->>15 as q3, r->>16 as q4,
       nullif(r->>18, '')::numeric as rating, nullif(r->>19, '')::int as prestige, nullif(r->>21, '')::numeric as tpi
from silver.hw_pages p
cross join lateral jsonb_array_elements(p.tables->0->'rows') r
where p.page_type = 'rankings' and (r->>0) ~ '^\d+$';

-- Référence : phrases du scout → fourchette de la compétence au plafond. Source : tableau épinglé sur Discord,
-- recopié par l'utilisateur (Aide docs.txt). Remplace les valeurs non vérifiées du 2026-10-30 (plusieurs étaient fausses :
-- « good shooter » 13-19 au lieu de 13-16, « sluggish » 0-6 au lieu de 0-9, « below average ball handler » 0-2 au lieu de 0-12…).
-- target 'id_pd' = somme IDef + PDef.
create table if not exists silver.hw_ref_scout_phrases (
  phrase text primary key, skill text not null, min_val int, max_val int, note text
);
truncate silver.hw_ref_scout_phrases;
insert into silver.hw_ref_scout_phrases (phrase, skill, min_val, max_val, note) values
 ('Could be a dominating post player', 'ins', 18, 20, null),
 ('Could be a very good post player', 'ins', 15, 18, null),
 ('Could be a good post player', 'ins', 13, 17, null),
 ('Above average post moves', 'ins', 11, 14, null),
 ('Could be an excellent shooter', 'os', 15, 20, null),
 ('Could be a good shooter', 'os', 13, 16, null),
 ('Could be an above average shooter', 'os', 11, 17, null),
 ('Does not have much of a shooting touch', 'os', null, null, 'plafond bas, valeur non publiée'),
 ('Could really be a long-range shooter', 'rng', 10, 20, null),
 ('Can be a monster on the boards', 'reb', 15, 20, null),
 ('Can be a decent rebounder', 'reb', 13, 16, null),
 ('Can never be a good rebounder', 'reb', 0, 8, null),
 ('Can be a really smart player', 'iq', 14, 20, null),
 ('Can be a smart player', 'iq', 13, 18, null),
 ('Can be prone to a lot of mental mistakes', 'iq', 0, 7, null),
 ('Can be a great all-around defensive player', 'id_pd', 22, 36, 'somme IDef + PDef'),
 ('Can be a good all-around defensive player', 'id_pd', 14, 31, 'somme IDef + PDef'),
 ('Will never be a good perimeter defender', 'pdef', 0, 10, null),
 ('Will never be a good interior defender', 'idef', 0, 10, null),
 ('Can be a skilled passer with exceptional court vision', 'pass', 14, 20, null),
 ('Can be a skilled passer', 'pass', 12, 16, null),
 ('Can be a really good ball handler', 'hnd', 15, 20, null),
 ('Can be a decent ball handler', 'hnd', 11, 16, null),
 ('Will be a below average ball handler', 'hnd', 0, 12, null),
 ('Will be quick as lightning', 'spd', 19, 20, null),
 ('Will be very quick', 'spd', 15, 18, null),
 ('Can be a speedy player', 'spd', 12, 16, null),
 ('Will always be a bit sluggish', 'spd', 0, 9, null),
 ('Is a troubled kid and may not be college material', 'other', null, null, '~50/50 : s''engage ou ne joue jamais en université (fin HS SR)'),
 ('Isn''t much of a student and may not qualify academically', 'other', null, null, '~50/50 : s''engage ou part en JuCo (fin HS SR)'),
 ('May choose to play overseas instead of going to college', 'other', null, null, 'international seulement, ~50/50'),
 ('Is eager to commit early', 'other', null, null, 's''engage dans la 1re moitié de saison s''il a des contacts'),
 ('Would prefer to play close to home', 'other', null, null, 'bonus de région plus fort'),
 ('Has no preference to play close to home', 'other', null, null, 'pas de bonus de région'),
 ('Will flourish in a fast pace offense', 'other', null, null, 'Pace positif'),
 ('Excellent all-around player', 'other', null, null, null),
 ('Good all-around player', 'other', null, null, null);

-- Référence : potentiel → plafond de SI (Aide docs.txt, identique à public.hardwood_ref_potential_caps ; pot 4-8 extrapolés 14 × pot).
create table if not exists silver.hw_ref_potential_caps (pot int primary key, cap_min int, cap_max int, source text);
truncate silver.hw_ref_potential_caps;
insert into silver.hw_ref_potential_caps
select p, 14 * p, 14 * p + 13, case when p between 9 and 17 then 'Aide docs (tableau Discord)' else 'extrapolé 14 × pot [H]' end
from generate_series(3, 20) p;

-- Référence : compétences clés par poste (Aide docs.txt, image 5). Taille : PF et C « grand », SF plus grand que SG et PG.
create table if not exists silver.hw_ref_position_keys (pos text primary key, ord int, keys text[], height_min_m numeric, source text);
truncate silver.hw_ref_position_keys;
insert into silver.hw_ref_position_keys values
 ('PG', 1, array['iq', 'pass', 'hnd', 'spd'], null, 'Aide docs'),
 ('SG', 2, array['os', 'spd'], null, 'Aide docs'),
 ('SF', 3, array['os', 'def', 'spd'], 1.90, 'Aide docs (def = moyenne IDef/PDef ; taille [H])'),
 ('PF', 4, array['ins', 'reb'], 1.98, 'Aide docs (taille [H])'),
 ('C',  5, array['ins', 'reb'], 2.03, 'Aide docs (taille [H])');

-- Les tables public.hardwood_* (créées hors dépôt, utilisées par public.hardwood_view_player_analysis) ne sont pas touchées ;
-- leurs fourchettes de phrases sont fausses par endroits : les vues hw_* lisent silver.hw_ref_* seulement.

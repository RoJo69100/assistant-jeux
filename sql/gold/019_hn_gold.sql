-- Hockey Nation : vues gold (2026-10-23).
-- Sources : silver.hn_* (sql/silver/015_hn_base.sql) ; règles [G:Rubrique] = guide officiel lu le 2026-10-23.

-- Compétences clés par poste. Hypothèse tirée des définitions du guide [G:Players] :
-- attaquants = Tir, Passe, Patinage (+ Mises au jeu pour le centre, « Forwards only ») ;
-- défenseurs = Défense (« crucial to prevent scoring chances »), Mise en échec, Patinage ;
-- gardiens = Réflexes, Placement, Jambières, Bloqueur, Mitaine.
-- Règle de l'utilisateur (2026-10-23) : un ailier dont les talents forts sont DEF et CHK ne nous intéresse pas.
create or replace view gold.hn_position_keys with (security_invoker = true) as
select * from (values
  ('C','SHO'),('C','PAS'),('C','SKA'),('C','FOF'),
  ('LW','SHO'),('LW','PAS'),('LW','SKA'),
  ('RW','SHO'),('RW','PAS'),('RW','SKA'),
  ('LD','DEF'),('LD','CHK'),('LD','SKA'),
  ('RD','DEF'),('RD','CHK'),('RD','SKA'),
  ('G','REF'),('G','POS'),('G','PAD'),('G','BLO'),('G','GLO')
) v(position, skill);

-- Adéquation talents / poste, une ligne par joueur et par poste qu'il peut tenir.
-- talents_cles = nombre de talents forts (2 au plus) parmi les compétences clés du poste ;
-- faible_cle = son talent le plus faible est une compétence clé du poste.
create or replace view gold.hn_player_fit with (security_invoker = true) as
with p as (
  select pl.player_id, pl.name, pl.team_level, pl.age, pl.rating, pl.main_position, pl.positions,
         pl.talent_strongest, pl.talent_weakest, pl.special_skill_count, pl.salary, pl.contract_to
  from silver.hn_players pl
), pos as (
  select p.*, x.position, x.ord = 1 as is_main
  from p, jsonb_array_elements_text(p.positions) with ordinality x(position, ord)
)
select pos.player_id, pos.name, pos.team_level, pos.age, pos.rating, pos.position, pos.is_main,
       pos.talent_strongest, pos.talent_weakest,
       (select count(*) from jsonb_array_elements_text(pos.talent_strongest) t
         where exists (select 1 from gold.hn_position_keys k where k.position = pos.position and k.skill = t)) as talents_cles,
       exists (select 1 from gold.hn_position_keys k where k.position = pos.position and k.skill = pos.talent_weakest) as faible_cle,
       case
         when (select count(*) from jsonb_array_elements_text(pos.talent_strongest) t
                where exists (select 1 from gold.hn_position_keys k where k.position = pos.position and k.skill = t)) = 2
              and not exists (select 1 from gold.hn_position_keys k where k.position = pos.position and k.skill = pos.talent_weakest) then 'idéal'
         when (select count(*) from jsonb_array_elements_text(pos.talent_strongest) t
                where exists (select 1 from gold.hn_position_keys k where k.position = pos.position and k.skill = t)) >= 1 then 'correct'
         else 'contre-emploi'
       end as verdict,
       pos.special_skill_count, pos.salary, pos.contract_to
from pos;

-- Tableau de draft : toutes les classes exportées, talents lus contre le poste principal.
create or replace view gold.hn_draft_board with (security_invoker = true) as
select substring(d.endpoint from '/league/([^/]+)/')::uuid as league_id, d.draft_rank, d.name, d.main_position, d.age,
       d.rating, d.scouted_times, d.from_my_u17, d.u17_team,
       d.talents->'strongest' as talent_strongest, d.talents->>'weakest' as talent_weakest,
       case when d.talents is null then null else
         (select count(*) from jsonb_array_elements_text(d.talents->'strongest') t
           where exists (select 1 from gold.hn_position_keys k where k.position = d.main_position and k.skill = t)) end as talents_cles,
       case when d.talents is null then null else
         exists (select 1 from gold.hn_position_keys k where k.position = d.main_position and k.skill = d.talents->>'weakest') end as faible_cle,
       d.special_skill_count,
       (select count(*) from jsonb_array_elements(d.skills) s where s ? 'lvl') as skills_visible,
       case when d.from_my_u17 or d.scouted_times >= 3 then 'tout connu'
            when d.scouted_times = 2 then 'talents + 3-5 compétences'
            when d.scouted_times = 1 then 'note + talents'
            else 'non repéré' end as scouting_state,
       d.day
from silver.hn_draft_class d;

-- Engagements salariaux par saison future (contrats actifs et déjà signés) contre le plafond projeté.
-- Rachats [G:Finances, Buyouts] : salaries[0] = saison en cours, [1] = suivante.
create or replace view gold.hn_cap_outlook with (security_invoker = true) as
with s as (select max(season) as season from silver.hn_season),
f as (select * from silver.hn_finances order by day desc limit 1),
c as (
  select ps.player_id, ps.name, (x->>'from')::int as from_s, (x->>'to')::int as to_s, (x->>'salary')::bigint as salary,
         coalesce((x->>'frm')::bool, false) as frm
  from (select distinct on (player_id) * from silver.hn_player_snapshots order by player_id, day desc, captured_at desc) ps,
       jsonb_array_elements(coalesce(ps.contracts, '[]'::jsonb)) x
), seasons as (select s.season + k as season, k from s, generate_series(1, 4) k)
select se.season,
       case when se.k = 1 then (f.salary_cap_projection->>'value')::bigint end as cap_projected,
       sum(c.salary) filter (where not c.frm) as committed,
       count(*) filter (where not c.frm) as contracts,
       (select coalesce(sum((b->'salaries'->>se.k)::bigint), 0) from jsonb_array_elements(coalesce(f.buyouts, '[]'::jsonb)) b) as buyouts,
       case when se.k = 1 then (f.salary_cap_projection->>'value')::bigint - coalesce(sum(c.salary) filter (where not c.frm), 0)
            - (select coalesce(sum((b->'salaries'->>se.k)::bigint), 0) from jsonb_array_elements(coalesce(f.buyouts, '[]'::jsonb)) b) end as cap_space
from seasons se cross join f
left join c on se.season between c.from_s and c.to_s
group by se.season, se.k, f.salary_cap_projection, f.buyouts
order by se.season;

-- Coachs : les nôtres et le marché. match_sum = OFP+DFP+BAT+PP+PK [G:Coaches, Match Skills] ;
-- le head coach compte double en match. Plafonds : U17 note 54, U21 note 69 [G:Coaches].
create or replace view gold.hn_coach_board with (security_invoker = true) as
select 'club' as source, c.team_level, c.head_coach, c.name, c.age, c.xp, c.rating, c.match_rating, c.training_rating,
       c.ofp, c.dfp, c.bat, c.pp, c.pk, coalesce(c.ofp,0)+coalesce(c.dfp,0)+coalesce(c.bat,0)+coalesce(c.pp,0)+coalesce(c.pk,0) as match_sum,
       c.talents->'strongest' as talent_strongest, c.talents->>'weakest' as talent_weakest,
       (select count(*) from jsonb_array_elements(c.skills) s where not coalesce((s->>'max')::bool, false)) as skills_open,
       null::bool as can_offer, 65 - c.age as years_to_retire, c.day
from silver.hn_coaches c
union all
select 'marché', null, null, f.name, f.age, f.xp, f.rating, f.match_rating, f.training_rating,
       f.ofp, f.dfp, f.bat, f.pp, f.pk, coalesce(f.ofp,0)+coalesce(f.dfp,0)+coalesce(f.bat,0)+coalesce(f.pp,0)+coalesce(f.pk,0),
       f.talents->'strongest', f.talents->>'weakest',
       (select count(*) from jsonb_array_elements(f.skills) s where not coalesce((s->>'max')::bool, false)),
       f.can_offer, 65 - f.age, f.day
from silver.hn_free_coaches f;

-- Calendrier de saison [G:Calendar] et fenêtres utiles à la gestion.
create or replace view gold.hn_calendar with (security_invoker = true) as
select * from (values
  (1, 'Début de saison : âge +1, draftés en U21, U17 de 15 ans, fenêtre d''échanges I et agents libres ouvertes, plafond annoncé en hausse ou en baisse'),
  (3, 'Premières réponses des coachs ; Free Agent Frenzy (offres jusqu''à 1 h avant)'),
  (4, 'Début des missions de scouting (jusqu''au jour 63)'),
  (8, '1re journée de saison régulière ; 1er jour de paie'),
  (10, 'Mise à jour des demandes des agents libres'),
  (20, 'Mise à jour des demandes des agents libres ; Championnat du monde'),
  (28, 'Fourchette du plafond de la saison suivante'),
  (30, 'Mise à jour des demandes des agents libres'),
  (35, 'Fermeture fenêtre I et agents libres (21:00 CET) : effectifs gelés, dernières embauches de coachs, dernières activations de contrat'),
  (42, 'Dernière journée de saison régulière ; dernier jour de paie'),
  (44, 'Début des playoffs'),
  (49, 'Début de l''Import Draft (1 joueur de 14 ans révélé par jour pendant 6 jours)'),
  (51, 'Ouverture fenêtre II'),
  (57, 'Plafond officiel de la saison suivante'),
  (61, 'Fermeture fenêtre II (21:00 CET)'),
  (63, 'Dernier jour : Youth Draft (pré-instructions 1 h avant), report du budget de scouting')
) v(day, event);

-- Alertes Hockey Nation, rouge d'abord. Le brief du jour et le registre fait-… passent avant ces alertes.
create or replace view gold.hn_daily_alerts with (security_invoker = true) as
with s as (select * from silver.hn_season order by season desc limit 1)
select 1 as prio, '🟥 URGENT' as niveau, 'draft' as domaine,
       'Pré-instructions de draft avant ' || to_char(s.draft_deadline_at at time zone 'Europe/Paris', 'DD/MM HH24:MI') || ' (Paris)' as alerte
from s where s.draft_deadline_at > now() and s.draft_deadline_at < now() + interval '48 hours'
union all
select 2, '🟧 IMPORTANT', 'contrats', 'Cap space projeté S' || season || ' : ' || round(cap_space / 1e6, 2) || ' M$'
from gold.hn_cap_outlook where cap_space is not null and cap_space < 2000000
union all
select 2, '🟧 IMPORTANT', 'scouting', 'Scouts : ' || num_scouts || ' sur ' || max_scouts || ' possibles'
from (select * from silver.hn_scouting_budget order by day desc limit 1) b where num_scouts < max_scouts
union all
select 3, '🟩 SUIVI', 'U21', name || ' (' || age || ' ans, ' || rating || ') : pas de contrat, part à 22 ans'
from silver.hn_players where team_level = 'U21' and age >= 21 and salary is null and not coalesce(frm, false) and next_salary is null
union all
select 3, '🟩 SUIVI', 'effectif', name || ' joue ' || position || ' à contre-emploi (talents ' || talent_strongest::text || ')'
from gold.hn_player_fit where is_main and verdict = 'contre-emploi' and team_level in ('PRO', 'FRM');

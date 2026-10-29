-- Hockey Nation (2026-10-29, colère de l'utilisateur) :
-- 1) silver.hn_declared : faits déclarés par l'utilisateur et pas encore dans un export (scouts embauchés, joueurs bloqués, offres de coachs).
--    On l'alimente à chaque « j'ai fait X » : toutes les vues se recalculent seules.
-- 2) gold.hn_scout_board : TOUS les scouts (embauchés + candidats) avec top poste+nation / poste / nation / total / nouveaux joueurs couverts.
-- 3) Règles de coachs [U] : U17 = note ≤ 54 ET expérience ≤ Average (4) ; U21 = note ≤ 69 ET expérience ≤ Very Good (7). Échelle d'expérience
--    déduite des spéciales débloquées (Strobel 8 = Excellent, 3 spéciales visibles) : hypothèse [H].
--    U17 : on cherche 2 compétences de match parmi les 2 talents forts + la plus grande marge de progression.

create table if not exists silver.hn_declared (
  kind text not null,          -- scout_hired | joueur_bloque | coach_offre
  name text not null,
  detail text,
  declared_on date not null default current_date,
  primary key (kind, name)
);
insert into silver.hn_declared (kind, name, detail, declared_on) values
  ('scout_hired', 'Rob Gardner', 'RW USA, embauché le 29/10, pas encore exporté', date '2026-10-29'),
  ('scout_hired', 'Frank Löffler', 'LD Allemagne, embauché le 29/10, pas encore exporté', date '2026-10-29'),
  ('joueur_bloque', 'Carpentier', 'ne peut pas bouger (reste PRO)', date '2026-10-29'),
  ('joueur_bloque', 'Jasiński', 'ne peut pas bouger (reste PRO) — correction de l''utilisateur', date '2026-10-29'),
  ('coach_offre', 'Florian Strobel', 'PRO assistant à la place de Wolfgang Baier (offre envoyée)', date '2026-10-29')
on conflict (kind, name) do update set detail = excluded.detail, declared_on = excluded.declared_on;

-- Classe de draft de la saison en cours, dans notre ligue.
create or replace view gold.hn_classe_draft with (security_invoker = true) as
select b.draft_rank as rang, b.name as joueur, b.main_position as pos, n.name as nation, b.scouted_times as rapports, b.rating as note, b.from_my_u17 as notre_u17
from gold.hn_draft_board b
left join silver.hn_draft_class d on d.name = b.name and d.draft_rank = b.draft_rank
left join silver.hn_nations n on n.nation_id = d.nation_id
where b.season = (select max(season) from gold.hn_draft_board)
  and b.league_id = (select league_id from gold.hn_draft_board where from_my_u17 group by league_id order by count(*) desc limit 1);

-- Scouts en poste = dernier export + scouts déclarés embauchés pas encore exportés.
create or replace view gold.hn_scouts_effectifs with (security_invoker = true) as
with apps as (
  select x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as scout, (x->'scout'->>'age')::int as age,
         x->'scout'->>'position' as pos, n.name as nation
  from (select body from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
       jsonb_array_elements(a.body->'applications') x
  left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid
), cur as (
  select name as scout, preferred_position as pos, nation, coalesce(head_scout, false) as chef, 'embauché' as statut
  from silver.hn_scouts where day = (select max(day) from silver.hn_scouts)
)
select * from cur
union all
select a.scout, a.pos, a.nation, false, 'embauché (déclaré)'
from apps a join silver.hn_declared d on d.kind = 'scout_hired' and d.name = a.scout
where a.scout not in (select scout from cur);

create or replace view gold.hn_scout_board with (security_invoker = true) as
with h as (select * from gold.hn_scouts_effectifs),
apps as (
  select x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as scout, (x->'scout'->>'age')::int as age,
         x->'scout'->>'position' as pos, n.name as nation
  from (select body from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
       jsonb_array_elements(a.body->'applications') x
  left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid
), s as (
  select statut, scout, null::int as age, pos, nation from h
  union all
  select 'candidat', a.scout, a.age, a.pos, a.nation from apps a where a.scout not in (select scout from h)
)
select s.statut, s.scout, s.age, s.pos as poste, s.nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos and c.nation = s.nation) as top_poste_nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos) as tous_poste,
       (select count(*) from gold.hn_classe_draft c where c.nation = s.nation) as tous_nation,
       (select count(*) from gold.hn_classe_draft c where c.pos = s.pos or c.nation = s.nation) as total_couvert,
       -- candidat : joueurs que personne d'embauché ne couvre ; embauché : joueurs que lui seul couvre
       (select count(*) from gold.hn_classe_draft c
         where (c.pos = s.pos or c.nation = s.nation)
           and not exists (select 1 from h where h.scout <> s.scout and (h.pos = c.pos or h.nation = c.nation))) as nouveaux_ou_uniques,
       case when s.statut <> 'candidat' then 'en poste'
            when s.pos = 'G' then 'non : limite de draft G = 0'
            when (select count(*) from gold.hn_classe_draft c
                  where (c.pos = s.pos or c.nation = s.nation)
                    and not exists (select 1 from h where h.pos = c.pos or h.nation = c.nation)) = 0 then 'non : rien de nouveau'
            else 'oui' end as decision
from s
order by (s.statut = 'candidat'), 10 desc, 6 desc, 3;

create or replace view gold.hn_scout_priority with (security_invoker = true) as
select scout, age, poste, nation, top_poste_nation, tous_poste, tous_nation, nouveaux_ou_uniques as nouveaux_joueurs_couverts, decision as embaucher
from gold.hn_scout_board where statut = 'candidat'
order by (decision = 'oui') desc, nouveaux_ou_uniques desc, top_poste_nation desc, age;

create or replace view gold.hn_scout_coverage with (security_invoker = true) as
select scout, poste, nation, top_poste_nation, tous_poste, tous_nation, total_couvert from gold.hn_scout_board where statut <> 'candidat'
union all
select 'TOUS (joueurs distincts)', null, null, null, null, null,
       (select count(*) from gold.hn_classe_draft c where exists (select 1 from gold.hn_scouts_effectifs h where h.pos = c.pos or h.nation = c.nation));

create or replace view gold.hn_scout_targets with (security_invoker = true) as
select h.scout, h.chef,
       case when c.pos = h.pos and c.nation = h.nation then 'A poste + nation' when c.pos = h.pos then 'B poste' else 'C nation' end as categorie,
       c.rang, c.joueur, c.pos as poste, c.nation, c.rapports, c.note, c.notre_u17
from gold.hn_scouts_effectifs h join gold.hn_classe_draft c on c.pos = h.pos or c.nation = h.nation
where c.rapports < 3
order by h.scout, 3, c.rapports, c.rang;

-- Coachs candidats du marché avec leurs droits par équipe et leur marge de progression.
create or replace view gold.hn_coach_candidats with (security_invoker = true) as
with fc as (select name, can_offer from silver.hn_free_coaches where day = (select max(day) from silver.hn_free_coaches))
select p.coach, p.age, p.xp, p.note, p.match_sum, p.match_min, p.match_max, p.match_max - p.match_sum as marge,
       p.saisons_avant_retraite, p.speciales, p.talents_forts, p.talent_faible,
       (select count(*) from jsonb_array_elements_text(p.talents_forts) t
         where t in ('Offensive Play', 'Defensive Play', 'Puck Battling', 'Power Play', 'Penalty Kill')) as talents_forts_de_match,
       (p.note <= 54 and p.xp <= 4) as ok_u17,
       (p.note <= 69 and p.xp <= 7) as ok_u21,
       exists (select 1 from silver.hn_declared d where d.kind = 'coach_offre' and d.name = p.coach) as offre_envoyee
from gold.hn_coach_potential p
where not p.en_poste and coalesce((select can_offer from fc where fc.name = p.coach limit 1), true);

-- Options par poste : mêmes règles qu'avant + expérience (U17 ≤ 4, U21 ≤ 7), sans les coachs déjà offerts.
drop view if exists gold.hn_coach_options;
create view gold.hn_coach_options with (security_invoker = true) as
with fs as (
  select (x->'coach'->>'id') as coach_id, coalesce((x->'coach'->>'firstSeason')::bool, false) as first_season
  from (select body from silver.hn_api where route = '/coach-center/active-jobs' order by captured_at desc limit 1) a, jsonb_array_elements(a.body) x
), staff as (
  select k.key as team_level, c->>'id' as coach_id, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age,
         coalesce((c->'job'->>'head')::bool, false) as head,
         silver.hn_skill(c->'skills','OFP') + silver.hn_skill(c->'skills','DFP') + silver.hn_skill(c->'skills','BAT')
           + silver.hn_skill(c->'skills','PP') + silver.hn_skill(c->'skills','PK') as match_sum
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
)
select s.team_level, s.head, s.coach, s.age, s.match_sum,
       b.coach as meilleur_candidat, b.age as age_candidat, b.xp as xp_candidat, b.match_sum as somme_candidat,
       (b.match_sum - s.match_sum) * case when s.head then 2 else 1 end as gain_equipe,
       b.saisons_avant_retraite,
       (select string_agg(d.name || ' : ' || d.detail, ' ; ') from silver.hn_declared d where d.kind = 'coach_offre' and d.detail like '%' || s.coach || '%') as offre_en_cours
from staff s
left join fs on fs.coach_id = s.coach_id
left join lateral (
  select m.* from gold.hn_coach_candidats m
  where m.match_sum > s.match_sum and not m.offre_envoyee and m.age < 65
    and (s.team_level <> 'U17' or m.ok_u17) and (s.team_level <> 'U21' or m.ok_u21)
  order by m.match_sum desc, m.age limit 1
) b on true
where not coalesce(fs.first_season, false)
order by s.team_level, s.head desc, gain_equipe desc nulls last;

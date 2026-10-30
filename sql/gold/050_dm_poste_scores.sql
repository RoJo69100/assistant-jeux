-- Derby Manager : note par poste (compétences clés) pour nos joueurs et pour le marché. Conçu le 2026-10-30.
-- Compétences clés [H] tirées des règles du développeur (skill derbymanager-tactique, connaissance.md) :
--   GK : handling, positioning, agility, aerial, reaction (« for goalkeepers there are only 5 skills involved », 2025-06-03)
--   D  : marking, tackling, positioning, anticipation, aerial (PBU = anticipation, positioning, tackling, 2025-08-04)
--   M  : passing, creativity, first touch, technique, anticipation, ball control (BU = creativity, dribbling, first touch)
--   F  : shooting, accuracy, first touch, agility, headers, technique
-- À confronter aux matchs (notes de match, tirs) ; pondération égale faute de formule publiée.
-- gold.dm_marche_postes (049 bis) a un défaut (somme nulle dès qu'une compétence manque) : utiliser gold.dm_marche_notes.

create or replace view gold.dm_poste_scores with (security_invoker = true) as
with s as (select * from gold.dm_effectif)
select s.team_id, s.club, s.name, s.pos, s.age, s.tier, s.role, s.slot, s.price, s.salary, s.contract_days, s.pot,
       round((s.han + s.posi + s.agi + s.aer + s.rea) / 5.0, 1) as note_gk,
       round((s.mar + s.tac + s.posi + s.ant + s.aer) / 5.0, 1) as note_def,
       round((s.pas + s.cre + s.fir + s.tec + s.ant + s.bal) / 6.0, 1) as note_mil,
       round((s.sho + s.acc + s.fir + s.agi + s.hea + s.tec) / 6.0, 1) as note_att,
       case when s.pos ~ '^GK' then round((s.han + s.posi + s.agi + s.aer + s.rea) / 5.0, 1)
            when s.pos ~ '^D' then round((s.mar + s.tac + s.posi + s.ant + s.aer) / 5.0, 1)
            when s.pos ~ '^M' then round((s.pas + s.cre + s.fir + s.tec + s.ant + s.bal) / 6.0, 1)
            else round((s.sho + s.acc + s.fir + s.agi + s.hea + s.tec) / 6.0, 1) end as note_poste,
       s.ligne
from s;

-- Marché : note au poste au milieu et au bas de la fourchette vue par nos scouts, contre notre dernier titulaire
-- de la même ligne (GK 1er, D 5e, M 4e, F 1er : 5-4-1). gain_sur = gain garanti (bas de fourchette).
create or replace view gold.dm_marche_notes with (security_invoker = true) as
with m as (
  select mk.*,
    case when pos ~ '^GK' then 1 when pos ~ '^D' then 2 when pos ~ '^M' then 3 else 4 end as ligne,
    case when pos ~ '^GK' then array['han','posi','agi','aer','rea']
         when pos ~ '^D' then array['mar','tac','posi','ant','aer']
         when pos ~ '^M' then array['pas','cre','fir','tec','ant','bal']
         else array['sho','acc','fir','agi','hea','tec'] end as cles
  from silver.dm_market mk
), n as (
  select m.*,
    (select avg((silver.dm_n(split_part(v, '-', 1)) + silver.dm_n(split_part(v, '-', 2))) / 2.0)
       from jsonb_each_text(m.skill_ranges) e(k, v) where k = any(m.cles) and v ~ '\d-\d') as note_mid,
    (select avg(silver.dm_n(split_part(v, '-', 1)))
       from jsonb_each_text(m.skill_ranges) e(k, v) where k = any(m.cles) and v ~ '\d-\d') as note_min,
    (select count(*) from jsonb_each_text(m.skill_ranges) e(k, v) where k = any(m.cles) and v ~ '\d-\d') as cles_vues
  from m
), nous as (
  select team_id, ligne, max(note_poste) as meilleur,
         (array_agg(note_poste order by note_poste desc))[least(case ligne when 1 then 1 when 2 then 5 when 3 then 4 else 1 end, count(*)::int)] as dernier_titulaire
  from gold.dm_poste_scores group by team_id, ligne
)
select c.team_id, c.club, n.name, n.team as vendeur, n.pos, n.age, n.tier, n.price, n.salary, n.decision,
       n.cles_vues, round(n.note_min, 1) as note_min, round(n.note_mid, 1) as note_milieu,
       u.meilleur as notre_meilleur, u.dernier_titulaire,
       round(n.note_mid - u.dernier_titulaire, 1) as gain_milieu, round(n.note_min - u.dernier_titulaire, 1) as gain_sur
from n cross join silver.dm_clubs c
join nous u on u.team_id = c.team_id and u.ligne = n.ligne;

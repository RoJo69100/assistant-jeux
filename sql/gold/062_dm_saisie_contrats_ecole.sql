-- Derby Manager : trois vues de saisie et de décision, conçues le 2026-11-02 (Opus).
-- Demande : « est-ce que tu as tout mis dans des golds ? ça devrait être plus simple maintenant ».
-- But : la composition enregistrée, les contrats et l'école se lisent en une requête, sans agent.

-- 1. Saisie de l'écran Squad, dans l'ordre de l'écran : GK, ligne D (gauche → droite), M, F, puis S1-S5.
--    Pour chaque titulaire : note au poste, condition, forme, blessure, consignes de set pieces enregistrées,
--    et le meilleur joueur de la même ligne hors des 16 (alternative) si sa note est plus haute.
--    Ligne 0 = curseurs enregistrés (silver.dm_tactic). Options Pressing/Counters/… : absentes de la base.
create or replace view gold.dm_saisie_squad with (security_invoker = true) as
with q as (
  select s.team_id, s.name, s.pos, s.slot, s.sub_policy,
         substring(s.slot from '^([A-Z]{1,4}) \(') as poste,
         substring(s.slot from '\(([A-Z]+)\)') as role
  from silver.dm_squad s
),
o as (
  select q.*,
         case when q.slot ~ '^S\d' then 100 + substring(q.slot from '\d')::int
              else array_position(array['GK','DL','DLC','DC','DRC','DR','ML','MLC','MC','MRC','MR','FL','FLC','FC','FRC','FR'], q.poste)
         end as ordre
  from q where q.slot is not null
),
v as (select * from gold.dm_verdict_joueurs),
sp as (select * from gold.dm_setpieces),
alt as (
  select distinct on (v.team_id, v.ligne) v.team_id, v.ligne, v.name, v.note_poste
  from v left join o on o.team_id = v.team_id and o.name = v.name
  where o.name is null and v.blessure is null
  order by v.team_id, v.ligne, v.note_poste desc nulls last
),
t as (
  select distinct on (team_id) team_id, defensive_line, pass_preference, pass_focus, shooting, headers
  from silver.dm_tactic order by team_id, captured_at desc
)
select c.club, o.team_id, o.ordre,
       case when o.ordre > 100 then o.slot else o.poste end as poste,
       o.role, o.name, o.pos, v.note_poste, v.condition, v.forme, v.blessure,
       case when o.ordre > 100 then substring(o.sub_policy from '^(RAT|CON|AUTO|DEV|IMP|EMR)') end as statut_entree,
       nullif(concat_ws(' ', case when sp.pen_regle is not null then 'PEN' end, case when sp.fk_regle is not null then 'FK' end,
                        case when sp.cor_regle is not null then 'COR' end, case when sp.def_regle is not null then 'DEF ' || sp.def_regle end,
                        case when sp.att_regle is not null then 'ATT ' || sp.att_regle end, case when sp.cap_regle is not null then 'CAP' end), '') as set_pieces,
       case when o.ordre < 100 and alt.note_poste > v.note_poste then alt.name end as alternative,
       case when o.ordre < 100 and alt.note_poste > v.note_poste then alt.note_poste end as note_alternative
from o
join silver.dm_clubs c using (team_id)
left join v on v.team_id = o.team_id and v.name = o.name
left join sp on sp.team_id = o.team_id and sp.name = o.name
left join alt on alt.team_id = o.team_id and alt.ligne = v.ligne
union all
select c.club, t.team_id, 0, 'Curseurs', null,
       'DL ' || t.defensive_line || ' · PP ' || t.pass_preference || ' · PF ' || t.pass_focus || ' · SH ' || t.shooting || ' · HE ' || t.headers,
       null, null, null, null, null, null, null, null, null
from t join silver.dm_clubs c using (team_id);

-- 2. Contrats : prolonger, lister, laisser partir. Un joueur par ligne, contrat le plus court d'abord.
--    Règles : listable si contrat < 85 j (strict) ; libération gratuite ≤ 70 j sous un seuil de valeur (seuil inconnu) ;
--    prolongation = 5 % du prix (Vargas −240 000 pour 4,8 M le 2026-11-02) ; la mise en vente de Bodian a été refusée
--    à 20 joueurs dont un listé (19 → 18) : ventes_possibles = effectif − 19 [hypothèse, seuil réel inconnu].
--    Le statut « déjà listé » et la demande de salaire ne sont pas en base (page Contrat à exporter).
create or replace view gold.dm_contrats with (security_invoker = true) as
select v.club, v.team_id, v.name, v.pos, v.ligne, v.rang_ligne, v.age, v.note_poste, v.statut_contrat,
       v.temps_jeu_satisf_pct, v.contract_days, v.salary, v.price,
       round(v.price * 0.05) as frais_prolongation,
       v.contract_days < 85 as listable,
       v.contract_days <= 70 as liberable_70j,
       case when v.contract_days <= 7 then 'URGENT : prolonger ou laisser partir'
            when v.contract_days <= 30 then 'prolonger ce cycle'
            when v.contract_days < 85 then 'listable'
            else 'non listable' end as echeance,
       v.mentor, v.verdict,
       count(*) over (partition by v.team_id) as effectif,
       greatest(count(*) over (partition by v.team_id) - 19, 0) as ventes_possibles,
       f.marge_salaire_jour
from gold.dm_verdict_joueurs v
left join gold.dm_finances_bilan f on f.team_id = v.team_id
order by v.team_id, v.contract_days;

-- 3. École contre jeunes découverts : un jeune par ligne, par club.
--    École : silver.dm_school (compétences exactes, potentiel). Découverts : silver.dm_scout_youth (fourchettes),
--    potentiel lu sur la fiche joueur exportée (bronze players_id, titre « DM - G. Onaga »).
--    valeur_cible = médiane de prix 24-27 ans du tier visé (gold.dm_prix_reference) : ordre des tiers déduit des prix [hypothèse].
create or replace view gold.dm_ecole_scouts with (security_invoker = true) as
with ecole as (
  select distinct on (team_id, name) * from silver.dm_school order by team_id, name, captured_at desc
),
derniere_ecole as (select team_id, max(captured_at) as cap from silver.dm_school group by 1),
fiche as (
  select distinct on (substring(payload->>'title' from '^DM - (.+)$'))
         substring(payload->>'title' from '^DM - (.+)$') as name, captured_at,
         regexp_replace(payload->>'text', '\s+', ' ', 'g') as txt
  from bronze.raw_pages
  where game = 'derbymanager' and page_type = 'players_id' and payload->>'text' like '%youngster%'
  order by substring(payload->>'title' from '^DM - (.+)$'), captured_at desc
),
noms as (select * from (values ('Handling'),('Marking'),('Tackling'),('Positioning'),('Passing'),('Ball control'),('First touch'),
                                ('Shooting'),('Headers'),('Reaction'),('Anticipation'),('Aerial'),('Agility'),('Technique'),
                                ('Creativity'),('Accuracy')) n(nom)),
tout as (
  select e.team_id, 'école' as source, null::text as region, e.name, e.pos, e.age, e.days_left as jours_ecole, null::int as scouts,
         m.moy as moy_min, m.moy as moy_max, e.potential_level as potentiel, e.potential_target as cible, e.personality as personnalite,
         null::text as expire
  from ecole e join derniere_ecole d on d.team_id = e.team_id and d.cap = e.captured_at
  cross join lateral (
    select round(avg(substring(e.skills_txt from '(?i)' || n.nom || ' (?:[+-]\d+ )?(\d+)')::int), 1) as moy from noms n
  ) m
  union all
  select y.team_id, 'découvert', y.region, y.name, y.pos, y.age, null, y.scouts,
         coalesce(fm.moy, y.moy_min), coalesce(fm.moy, y.moy_max),
         substring(f.txt from 'He has (\w+) potential'), substring(f.txt from 'potential to become an? ([\w ]+?)\.'),
         substring(f.txt from 'shows an? ([\w -]+?) personality'), y.expire
  from silver.dm_scout_youth y
  left join fiche f on f.name = y.name
  left join lateral (
    select round(avg(substring(f.txt from n.nom || ' (\d+)')::int), 1) as moy from noms n
  ) fm on f.name is not null
)
select c.club, t.team_id, t.source, t.region, t.name, t.pos, t.age, t.jours_ecole, t.scouts,
       t.moy_min, t.moy_max, t.potentiel, t.cible, t.personnalite, t.expire,
       p.mediane as valeur_cible,
       rank() over (partition by t.team_id order by p.mediane desc nulls last, t.moy_max desc nulls last) as rang
from tout t
join silver.dm_clubs c using (team_id)
left join gold.dm_prix_reference p
  on p.ages = '24-27' and lower(p.tier) = lower(t.cible)
order by t.team_id, rang;

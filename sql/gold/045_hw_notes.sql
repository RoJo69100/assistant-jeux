-- Hardwood : notes /5 par joueur et par poste, comparables entre postes (demande de l'utilisateur, 2026-10-30).
-- Postes regroupés : PG, SG, SF, Grand (PF et C sont traités pareil : mêmes compétences clés IS + Reb).
-- Note = (niveau + adéquation) / 2, par demi-points.
--   niveau     : SI >= 140 -> 5 ; >= 125 -> 4 ; >= 110 -> 3 ; >= 95 -> 2 ; sinon 1.
--   adéquation : moyenne des compétences clés du poste (Aide docs) >= 15 -> 5 ; >= 13 -> 4 ; >= 11 -> 3 ; >= 9 -> 2 ; sinon 1.
--     PG : IQ, Pass, Hnd, Spd · SG : OS, Spd · SF : OS, défense (moyenne IDef/PDef), Spd · Grand : IS, Reb.
--   avenir     : potentiel >= 13 -> 5 ; 12 -> 4 ; 11 -> 3 ; 10 -> 2 ; sinon 1.
-- Seuils [H] : à confronter aux matchs. Walk-ons exclus (décision de l'utilisateur).

create or replace view gold.hw_player_group_notes with (security_invoker = true) as
with g(grp, ord) as (values ('PG', 1), ('SG', 2), ('SF', 3), ('Grand', 4)),
k as (
  select r.player_id, r.name, g.grp, g.ord, r.positions, r.si, r.pot, r.height_m,
         case g.grp
           when 'PG' then (r.iq + r.pass + r.hnd + r.spd) / 4.0
           when 'SG' then (r.os + r.spd) / 2.0
           when 'SF' then (r.os + (r.idef + r.pdef) / 2.0 + r.spd) / 3.0
           else (r.ins + r.reb) / 2.0 end as cles
  from silver.hw_roster r cross join g
  where r.scholarship
)
select player_id, name, grp, ord, round(cles, 1) as cles, si, pot,
       case when si >= 140 then 5 when si >= 125 then 4 when si >= 110 then 3 when si >= 95 then 2 else 1 end as niveau,
       case when cles >= 15 then 5 when cles >= 13 then 4 when cles >= 11 then 3 when cles >= 9 then 2 else 1 end as adequation,
       (case when si >= 140 then 5 when si >= 125 then 4 when si >= 110 then 3 when si >= 95 then 2 else 1 end
        + case when cles >= 15 then 5 when cles >= 13 then 4 when cles >= 11 then 3 when cles >= 9 then 2 else 1 end) / 2.0 as note,
       case when pot >= 13 then 5 when pot = 12 then 4 when pot = 11 then 3 when pot = 10 then 2 else 1 end as avenir,
       case when coalesce(positions, '') ~ (case grp when 'Grand' then '(^|\s)(PF|C)(\s|$)' else '(^|\s)' || grp || '(\s|$)' end) then 'maîtrisé'
            when coalesce(positions, '') ~ (case grp when 'Grand' then '(^|\s)(pf|c)(\s|$)' else '(^|\s)' || lower(grp) || '(\s|$)' end) then 'apprentissage'
            else 'jamais' end as mastery,
       height_m >= 1.95 or grp <> 'Grand' as height_ok
from k;

-- Équipe d'aujourd'hui et de l'an prochain : poste principal du joueur, notes, résultats, classe N+1 et départ.
create or replace view gold.hw_roster_notes with (security_invoker = true) as
select case n.grp when 'Grand' then 'Grand' else n.grp end as groupe, n.ord, r.name, r.pos as poste_jeu, r.class, r.height_m,
       n.si, n.pot, n.cles, n.niveau, n.adequation, n.note, n.avenir, n.mastery,
       r.class in ('SR', 'RS SR') as part_fin_saison,
       case r.class when 'FR' then 'SO' when 'SO' then 'JR' when 'JR' then 'SR' when 'RS FR' then 'RS SO' when 'RS SO' then 'RS JR'
                    when 'RS JR' then 'RS SR' else null end as classe_n1,
       r.injury_days, s.g, s.min, s.pts, s.plus_minus
from silver.hw_roster r
join gold.hw_player_group_notes n on n.player_id = r.player_id
  and n.grp = case when r.pos in ('PF', 'C') then 'Grand' else r.pos end
left join silver.hw_player_stats s on s.name = left(r.name, 1) || '. ' || substr(r.name, strpos(r.name, ' ') + 1)
where r.scholarship;

-- Depth chart proposé : remplissage dans l'ordre du moteur (PG, C, PF, SF, SG), PF et C puisent dans le même groupe « Grand ».
-- Classement = note + 0,5 si poste maîtrisé + plus-minus par match / 20 (les résultats comptent : un titulaire à +18 ne cède pas
-- sa place à un joueur sans minute pour 0,5 point de note). Blessés et redshirts cochés exclus.
create or replace view gold.hw_depth_suggest with (security_invoker = true) as
with recursive slots as (
  select row_number() over (order by d, o) as k, d as depth, pos,
         case when pos in ('PF', 'C') then 'Grand' else pos end as grp
  from (values ('PG', 1), ('C', 2), ('PF', 3), ('SF', 4), ('SG', 5)) p(pos, o), generate_series(1, 3) d
), cand as (
  -- Les notes regroupent PF et C, mais le jeu garde deux postes : on ne place un joueur que sur un poste qu'il maîtrise
  -- (majuscule dans « Positions »), jamais en apprentissage (malus hors poste non chiffré).
  select n.player_id, n.name, n.grp, n.note, sl.pos as slot_pos,
         n.note + 0.5 + coalesce(s.plus_minus, 0) / 20.0 as adj
  from gold.hw_player_group_notes n
  join silver.hw_roster r on r.player_id = n.player_id
  cross join (values ('PG'), ('SG'), ('SF'), ('PF'), ('C')) sl(pos)
  left join silver.hw_management m on m.player_id = n.player_id
  left join silver.hw_player_stats s on s.name = left(r.name, 1) || '. ' || substr(r.name, strpos(r.name, ' ') + 1)
  where not r.injured and coalesce(m.red_shirt, 'non') <> 'oui' and n.height_ok
    and n.grp = case when sl.pos in ('PF', 'C') then 'Grand' else sl.pos end
    and coalesce(r.positions, '') ~ ('(^|\s)' || sl.pos || '(\s|$)')
), pick (k, used, depth, pos, player_id, name, note, mastery) as (
  select 0::bigint, array[]::int[], null::int, null::text, null::int, null::text, null::numeric, null::text
  union all
  select s.k, p.used || c.player_id, s.depth, s.pos, c.player_id, c.name, c.note, 'maîtrisé'
  from pick p
  join slots s on s.k = p.k + 1
  left join lateral (
    select * from cand c where c.slot_pos = s.pos and c.player_id <> all (array_remove(p.used, null))
    order by c.adj desc limit 1) c on true
), saved as (
  select dc.depth, dc.pos, dc.short_name, dc.injured from silver.hw_depth_chart dc
)
select p.depth, p.pos, p.name as propose, p.note, p.mastery,
       sv.short_name || case when sv.injured then ' (blessé)' else '' end as actuel,
       case when p.name is null and p.depth = 1 then '🟥 aucun boursier valide'
            when p.name is null then '— vide (un joueur peut doubler deux postes)'
            when coalesce(sv.short_name, '-') = '-' then '🟧 à saisir'
            when sv.short_name <> left(p.name, 1) || '. ' || substr(p.name, strpos(p.name, ' ') + 1) or sv.injured then '🟧 à changer'
            else '✔' end as controle
from pick p
left join saved sv on sv.depth = p.depth and sv.pos = p.pos
where p.k > 0
order by p.depth, case p.pos when 'PG' then 1 when 'SG' then 2 when 'SF' then 3 when 'PF' then 4 else 5 end;

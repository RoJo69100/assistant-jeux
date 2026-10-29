-- Hockey Nation (2026-10-29) : tactique PRO, toujours le même rendu.
-- 1) silver.hn_lineups ne lit plus que le DERNIER export (une case vidée dans le jeu restait remplie par un ancien export).
-- 2) gold.hn_tactique_cible = la lineup voulue (lignes, paires D, gardiens, PP, PK, 3 hommes, 4v4, EXT, rôles) ;
--    gold.hn_tactique_plan = le plan de jeu voulu ; gold.hn_tactique_journal = chaque changement et sa raison.
-- 3) gold.hn_tactique_rendu (tout, dans l'ordre de l'écran, avec l'écart au jeu), gold.hn_tactique_effectif_poste
--    (tous les joueurs par poste et leurs rôles), gold.hn_tactique_controle (contrôles avant rendu).
-- Pour changer la lineup : UPDATE gold.hn_tactique_cible + une ligne dans gold.hn_tactique_journal (jamais de nouvelle table).

create or replace view silver.hn_lineups as
select distinct on ((l.value ->> 'id'), ln.key, pos.key)
       a.day, (l.value ->> 'id') as lineup, ln.key as line, pos.key as slot,
       ((pos.value #>> '{}'))::uuid as player_id, (l.value -> 'gameplan') as gameplan
from silver.hn_api a, lateral jsonb_array_elements(a.body) l(value),
     lateral jsonb_each(l.value -> 'lines') ln(key, value), lateral jsonb_each(ln.value) pos(key, value)
where a.route = '/team/:id/lineups' and jsonb_typeof(pos.value) = 'string'
  and a.captured_at = (select max(captured_at) from silver.hn_api where route = '/team/:id/lineups')
order by (l.value ->> 'id'), ln.key, pos.key, a.captured_at desc;

create table if not exists gold.hn_tactique_cible (
  lineup text not null default 'A', line text not null, slot text not null, ordre int not null,
  player_id uuid, joueur text, motif text, maj date not null default current_date,
  primary key (lineup, line, slot)
);
create table if not exists gold.hn_tactique_plan (
  lineup text not null default 'A', parametre text not null, valeur int, libelle text, statut text,
  maj date not null default current_date, primary key (lineup, parametre)
);
create table if not exists gold.hn_tactique_journal (
  id serial primary key, jour date not null default current_date, version text not null,
  changement text not null, raison text, test text, resultat text
);
alter table gold.hn_tactique_cible enable row level security;
alter table gold.hn_tactique_plan enable row level security;
alter table gold.hn_tactique_journal enable row level security;

truncate gold.hn_tactique_cible;
with v(line, slot, ordre, nom, motif) as (values
  ('L1','LW',101,'Soma Yokoyama','END 9, seuil L1 7+'),
  ('L1','C',102,'Alexander de Bruin','C idéal, END 8'),
  ('L1','RW',103,'Perry Spinka','END 7, CHK 10 / SKA 9'),
  ('L1','LD',104,'Joakim Seppälä','meilleur LD (73), END 4 : point faible reconnu'),
  ('L1','RD',105,'Jukka Nokelainen','END 9 : porte la paire D1'),
  ('L2','LW',201,'Darryl Bélanger','END 5 (tolérance −1) ; Conte END 4 reste en L3 : test'),
  ('L2','C',202,'Vladislav Papež','C idéal, END 6, FOF 8'),
  ('L2','RW',203,'Terrence Stone','END 8, 2 postes LW/RW'),
  ('L2','LD',204,'Gerard Burns','DEF 9, END 5'),
  ('L2','RD',205,'Thomas Marquardt','END 7, DEF 8'),
  ('L3','LW',301,'Antonio Conte','FOF 10, CHK 9, END 4'),
  ('L3','C',302,'Slava Blednov','74, FOF 10 : mises au jeu avec Conte'),
  ('L3','RW',303,'Paul Lubowitz','SHO 9 / PAS 8, END 4'),
  ('L3','LD',304,'Poul Munk','PWR 8, END 4'),
  ('L3','RD',305,'Vít Kabát','DEF 9 / PAS 8, END 2 : D3 joue peu'),
  ('L4','LW',401,'Jimi Hakkarainen','19 ans, SKA 10, END 2 : peu de minutes'),
  ('L4','C',402,'Mason Flink','C/RW, 70'),
  ('L4','RW',403,'Kosuke Kaneda','12e attaquant (54), seul RW/LW libre'),
  ('G','SG',501,'Vasiliy Kovalev','G1 71, END 4 : fatigué après 4 départs d''affilée'),
  ('G','BG',502,'Jean-Marc Lauper','G2 69, END 6 : débute le 5e match'),
  ('PP1','C',601,'Alexander de Bruin','SHO 9 SKA 8'),
  ('PP1','LW',602,'Darryl Bélanger','SHO 9 PAS 7'),
  ('PP1','RW',603,'Paul Lubowitz','SHO 9 PAS 8'),
  ('PP1','D',604,'Joakim Seppälä','SKA 10'),
  ('PP1','ANY',605,'Slava Blednov','FOF 10 : un preneur de mises au jeu 7+ par unité PP ; DEF 8 contre les buts en infériorité'),
  ('PP2','C',701,'Vladislav Papež','PAS 8, FOF 8'),
  ('PP2','LW',702,'Jimi Hakkarainen','SKA 10 PAS 8, END 2 mais PP courte'),
  ('PP2','RW',703,'Mason Flink','SHO 7 PAS 7'),
  ('PP2','D',704,'Thomas Marquardt','PAS 7'),
  ('PP2','ANY',705,'Soma Yokoyama','PAS 9, END 9'),
  ('PK4-1','FW1',801,'Perry Spinka','CHK 10 SKA 9 PWR 8'),
  ('PK4-1','FW2',802,'Terrence Stone','END 8'),
  ('PK4-1','LD',803,'Gerard Burns','DEF 9'),
  ('PK4-1','RD',804,'Thomas Marquardt','DEF 8 PWR 8'),
  ('PK4-2','FW1',811,'Mason Flink','CHK 8'),
  ('PK4-2','FW2',812,'Antonio Conte','CHK 9'),
  ('PK4-2','LD',813,'Poul Munk','PWR 8 CHK 7'),
  ('PK4-2','RD',814,'Jukka Nokelainen','SKA 8, END 9'),
  ('PK3-1','FW',821,'Perry Spinka',null),
  ('PK3-1','LD',822,'Gerard Burns',null),
  ('PK3-1','RD',823,'Thomas Marquardt',null),
  ('PK3-2','FW',831,'Mason Flink',null),
  ('PK3-2','LD',832,'Poul Munk',null),
  ('PK3-2','RD',833,'Jukka Nokelainen',null),
  ('4V4-1','FW1',901,'Alexander de Bruin','SHO 9 SKA 8'),
  ('4V4-1','FW2',902,'Soma Yokoyama','PAS 9, END 9'),
  ('4V4-1','LD',903,'Joakim Seppälä','SKA 10'),
  ('4V4-1','RD',904,'Jukka Nokelainen','SKA 8, END 9'),
  ('4V4-2','FW1',911,'Vladislav Papež','PAS 8'),
  ('4V4-2','FW2',912,'Terrence Stone','PAS 7 SHO 7'),
  ('4V4-2','LD',913,'Gerard Burns','PAS 7'),
  ('4V4-2','RD',914,'Vít Kabát','SHO 8 PAS 8'),
  ('EXT','FW1',1001,'Paul Lubowitz','SHO 9 PAS 8 (fin de match : END sans importance)'),
  ('EXT','FW2',1002,'Darryl Bélanger','SHO 9 PAS 7'),
  ('ROLE','CAP',1101,'Slava Blednov','expérience 10, la plus haute du club'),
  ('ROLE','A1',1102,'Joakim Seppälä','expérience 9'),
  ('ROLE','A2',1103,'Alexander de Bruin','expérience 8')
)
insert into gold.hn_tactique_cible (lineup, line, slot, ordre, player_id, joueur, motif)
select 'A', v.line, v.slot, v.ordre, p.player_id::uuid, v.nom, v.motif
from v left join silver.hn_players p on p.name = v.nom and p.team_level = 'PRO';

truncate gold.hn_tactique_plan;
insert into gold.hn_tactique_plan (lineup, parametre, valeur, libelle, statut) values
 ('A','tempo',1,'rythme : 0 / 1 / 2 (libellés non lus)','à confirmer : écran Plan de jeu'),
 ('A','mentality',2,'mentalité (Discord : offensive = plus de tirs, défensive = moins ; 2 lu comme offensive [H])','à confirmer'),
 ('A','aggression',0,'agressivité (Discord : basse en PP, sinon buts encaissés en infériorité)','gardé : 21 V en ligue S26'),
 ('A','pullGoalie1',1,'retrait du gardien, 1er seuil','à confirmer'),
 ('A','pullGoalie2',2,'retrait du gardien, 2e seuil','à confirmer'),
 ('A','shiftLength',1,'durée des présences (Discord : courtes = adapté aux END bas, temps de glace plus équilibré)','test possible : 0 si les libellés confirment « courtes »'),
 ('A','puckPressure',1,'pression sur le palet (Discord : forte = CHK / PWR)','à confirmer');

insert into gold.hn_tactique_journal (version, changement, raison, test)
values ('v1 2026-10-29', 'Lineup créée sur l''effectif PRO du 2026-10-29 (23 joueurs, Hakkarainen et Kaneda en L4, Nokelainen D1)',
        'END d''abord en L1/L2 (Yokoyama 9, de Bruin 8, Spinka 7 ; Stone 8) ; PP = SHO+PAS+SKA avec un FOF 7+ par unité ; PK = DEF+CHK+SKA+PWR sans Seppälä (déjà D1 + PP1 + 4v4)',
        'Après les 10 premiers matchs de ligue (S27, 1er match 2026-11-01) : PK ≥ 80 %, PP ≥ 23 %, mises au jeu ≥ 54,8 % ; sinon réécrire l''unité fautive');

-- Rendu : un tableau, toujours le même, dans l'ordre de l'écran du jeu.
create or replace view gold.hn_tactique_rendu with (security_invoker = true) as
with p as (select * from silver.hn_players where team_level = 'PRO'),
saisi as (select line, slot, player_id from silver.hn_lineups where lineup = 'A')
select c.ordre,
       case when c.line in ('L1','L2','L3','L4') then 'Lignes et paires D'
            when c.line = 'G' then 'Gardiens' when c.line like 'PP%' then 'Power play'
            when c.line like 'PK4%' then 'Infériorité 4 hommes' when c.line like 'PK3%' then 'Infériorité 3 hommes'
            when c.line like '4V4%' then '4 contre 4' when c.line = 'EXT' then 'Gardien retiré'
            else 'Rôles' end as bloc,
       c.line, c.slot, c.joueur, p.rating as note, p.endu as endurance, p.fof,
       case when c.line = 'ROLE' then null
            when c.slot in ('LW','C','RW','LD','RD','G') or c.slot in ('SG','BG') then
              case when c.slot in ('SG','BG') and p.positions ? 'G' then 'ok'
                   when p.positions ? c.slot then 'ok' else 'hors poste (−20 %)' end
            when c.slot = 'D' then case when p.positions ?| array['LD','RD'] then 'ok' else 'hors poste (−20 %)' end
            when c.slot in ('FW','FW1','FW2') then case when p.positions ?| array['LW','C','RW'] then 'ok' else 'D en attaque' end
            else 'ok' end as poste,
       case when c.line like 'PP%' or c.line = 'EXT' then coalesce(p.sho,0) + coalesce(p.pas,0) + case when c.line = 'EXT' then 0 else coalesce(p.ska,0) end
            when c.line like 'PK%' then coalesce(p.def,0) + coalesce(p.chk,0) + coalesce(p.ska,0) + coalesce(p.pwr,0)
            when c.line like '4V4%' then coalesce(p.ska,0) + coalesce(p.pas,0) + coalesce(p.sho,0)
            else p.rating end as valeur,
       case when c.line like 'PP%' or c.line = 'EXT' then 'SHO+PAS' || case when c.line = 'EXT' then '' else '+SKA' end
            when c.line like 'PK%' then 'DEF+CHK+SKA+PWR' when c.line like '4V4%' then 'SKA+PAS+SHO'
            else 'note' end as critere,
       (select string_agg(s->>'id', ', ') from jsonb_array_elements(p.special_skills) s) as speciales,
       c.motif,
       case when c.line = 'ROLE' then 'à saisir (non lisible dans l''export)'
            when s.player_id is null then '🟥 case vide dans le jeu : saisir'
            when s.player_id = c.player_id then 'déjà saisi'
            else '🟧 à changer : le jeu a ' || coalesce((select name from p p2 where p2.player_id::text = s.player_id::text), 'un joueur parti') end as dans_le_jeu
from gold.hn_tactique_cible c
left join p on p.player_id::text = c.player_id::text
left join saisi s on s.line = c.line and s.slot = c.slot
where c.lineup = 'A';

-- Tous les joueurs PRO par poste : où ils jouent, ou réserve.
create or replace view gold.hn_tactique_effectif_poste with (security_invoker = true) as
select case p.main_position when 'C' then 1 when 'LW' then 2 when 'RW' then 3 when 'LD' then 4 when 'RD' then 5 else 6 end as ordre_poste,
       p.main_position as poste, (select string_agg(x, '/') from jsonb_array_elements_text(p.positions) x) as postes_jouables, p.name as joueur, p.age, p.rating as note, p.endu as endurance, p.fof,
       p.sho, p.pas, p.ska, p.def, p.chk, p.pwr,
       (select string_agg(s->>'id', ', ') from jsonb_array_elements(p.special_skills) s) as speciales,
       coalesce((select string_agg(c.line || ' ' || c.slot, ' · ' order by c.ordre) from gold.hn_tactique_cible c where c.player_id::text = p.player_id::text and c.lineup = 'A' and c.line not in ('ROLE')), 'RÉSERVE') as roles,
       (select count(*) from gold.hn_tactique_cible c where c.player_id::text = p.player_id::text and c.lineup = 'A' and c.line not in ('ROLE')) as nb_roles
from silver.hn_players p where p.team_level = 'PRO';

-- Contrôles avant rendu (chaque ligne doit être 'ok').
create or replace view gold.hn_tactique_controle with (security_invoker = true) as
select 'joueur introuvable dans le PRO' as controle, count(*)::text as valeur, case when count(*) = 0 then 'ok' else 'ERREUR' end as etat
  from gold.hn_tactique_cible c where c.player_id is null
union all
select 'hors poste', count(*)::text, case when count(*) = 0 then 'ok' else 'à justifier' end from gold.hn_tactique_rendu where poste not in ('ok')
union all
select 'même joueur deux fois dans un type d''unité (PP, PK4, PK3, 4V4, lignes)', count(*)::text, case when count(*) = 0 then 'ok' else 'ERREUR' end
  from (select case when line like 'L%' then 'L' when line like 'PP%' then 'PP' when line like 'PK4%' then 'PK4' when line like 'PK3%' then 'PK3' when line like '4V4%' then '4V4' end as t, player_id
        from gold.hn_tactique_cible where lineup = 'A' and line in ('L1','L2','L3','L4','PP1','PP2','PK4-1','PK4-2','PK3-1','PK3-2','4V4-1','4V4-2')
        group by 1, 2 having count(*) > 1) d
union all
select 'joueurs distincts dans les lignes et gardiens (20 attendus)', count(distinct player_id)::text, case when count(distinct player_id) = 20 then 'ok' else 'ERREUR' end
  from gold.hn_tactique_cible where lineup = 'A' and line in ('L1','L2','L3','L4','G')
union all
select 'cases du jeu différentes de la cible', count(*)::text, case when count(*) = 0 then 'ok' else 'à saisir' end
  from gold.hn_tactique_rendu where dans_le_jeu like '🟥%' or dans_le_jeu like '🟧%';

-- Plan de jeu : cible contre jeu.
create or replace view gold.hn_tactique_plan_rendu with (security_invoker = true) as
select t.parametre, t.valeur as cible, (select (gameplan->>t.parametre)::int from silver.hn_lineups where lineup = 'A' limit 1) as dans_le_jeu,
       t.libelle, t.statut
from gold.hn_tactique_plan t where t.lineup = 'A'
order by array_position(array['tempo','mentality','aggression','pullGoalie1','pullGoalie2','shiftLength','puckPressure'], t.parametre);

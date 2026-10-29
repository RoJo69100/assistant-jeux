-- Hockey Nation (2026-10-29) : tactique v2.
-- 1) Kaneda part en FRM : Jasiński prend le L4 RW.
-- 2) Capitaine / assistants : attributs cachés (leadership), non lisibles : choix par expérience, sans écart au jeu.
-- 3) Plan de jeu : libellés réels donnés par l'utilisateur (échelles 0/1/2 lues dans l'ordre des libellés [H]).
-- 4) Style d'équipe : présences courtes (11 patineurs sur 18 à END <= 5).
update gold.hn_tactique_cible c
set player_id = p.player_id::uuid, joueur = p.name, maj = current_date,
    motif = '18 ans, RW/C, PAS 10 : prend la place de Kaneda (parti en FRM)'
from silver.hn_players p
where c.lineup = 'A' and c.line = 'L4' and c.slot = 'RW' and p.name = 'Gabriel Jasiński' and p.team_level = 'PRO';

update gold.hn_tactique_cible set motif = motif || ' (leadership caché, non lisible : choix par expérience)'
where line = 'ROLE' and motif not like '%leadership%';

do $$
declare d text;
begin
  d := pg_get_viewdef('gold.hn_tactique_rendu'::regclass);
  d := replace(d, 'à saisir (non lisible dans l''export)', 'non lisible (attribut caché)');
  execute 'create or replace view gold.hn_tactique_rendu with (security_invoker = true) as ' || d;
end $$;

update gold.hn_tactique_plan set valeur = 0, maj = current_date,
  statut = 'changé le 2026-10-29 : test (11 patineurs sur 18 à END 5 ou moins (6 à END 4 ou moins))'
where lineup = 'A' and parametre = 'shiftLength';

update gold.hn_tactique_plan set maj = current_date, libelle = case parametre
  when 'tempo' then 'Tempo : slow 0 / normal 1 / fast 2. Rapide = plus et meilleures chances, mais défense exposée et pertes de palet.'
  when 'mentality' then 'Mentalité : defensive 0 / balanced 1 / offensive 2. Offensive = plus de chances, moins responsable en défense.'
  when 'aggression' then 'Agressivité : calm 0 / normal 1 / aggressive 2. Plus de mises en échec, plus de pénalités.'
  when 'puckPressure' then 'Pression sur le palet : light 0 / normal 1 / heavy 2. Plus de vols de palet, mais risque de ne plus bloquer les tirs.'
  when 'shiftLength' then 'Durée des présences : short 0 (35-40 s) / normal 1 (41-49 s) / long 2 (50-55 s). Court = moins de temps de glace, moins de condition perdue.'
  when 'pullGoalie1' then 'Gardien retiré à 1 but de retard (2 dernières minutes) : never 0 / sometimes 1 (50 %, standard) / always 2.'
  when 'pullGoalie2' then 'Gardien retiré à 2 buts de retard (3 dernières minutes) : never 0 / sometimes 1 / always 2.'
  end
where lineup = 'A';

update gold.hn_tactique_plan set statut = 'gardé (21 V en ligue S26)'
where lineup = 'A' and parametre in ('tempo','mentality','aggression','puckPressure','pullGoalie1','pullGoalie2');

drop view if exists gold.hn_tactique_plan_rendu;
create view gold.hn_tactique_plan_rendu with (security_invoker = true) as
with j as (select gameplan from silver.hn_lineups where lineup = 'A' limit 1)
select t.parametre, t.valeur as cible, (j.gameplan->>t.parametre)::int as dans_le_jeu,
       (case t.parametre
          when 'tempo' then (array['slow','normal','fast'])[t.valeur + 1]
          when 'mentality' then (array['defensive','balanced','offensive'])[t.valeur + 1]
          when 'aggression' then (array['calm','normal','aggressive'])[t.valeur + 1]
          when 'puckPressure' then (array['light','normal','heavy'])[t.valeur + 1]
          when 'shiftLength' then (array['short','normal','long'])[t.valeur + 1]
          else (array['never','sometimes','always'])[t.valeur + 1] end) as choix,
       t.libelle, t.statut
from gold.hn_tactique_plan t cross join j where t.lineup = 'A'
order by array_position(array['mentality','puckPressure','tempo','aggression','shiftLength','pullGoalie1','pullGoalie2'], t.parametre);

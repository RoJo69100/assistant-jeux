-- Hockey Nation : vues gold, deuxième lot (2026-10-23) — compétences spéciales, adversaires, lignes probables, échanges, progression.
-- Sources : silver.hn_* (015_hn_base.sql, 016_hn_league.sql) ; règles [G:Players], [G:Coaches] = guide officiel (« Last updated on September 30, 2026 »),
-- lu dans bronze.raw_pages id 12572 (page Guide exportée le 2026-10-23).

-- Compétences spéciales [G:Players, Special Skills ; G:Coaches, Special Skills]. Texte du guide, traduit.
-- Seules celles du head coach jouent en match [G:Coaches]. synergie = ce qui démultiplie la compétence chez nous.
create or replace view gold.hn_special_skills with (security_invoker = true) as
select * from (values
  ('agitator','patineur','Agitator','-1 en Discipline au meilleur patineur adverse (tant qu''il est sur la glace)','chaque match',null),
  ('assist-king','patineur','Assist King','+1 en Passe après chaque passe décisive (max +3)','situation',null),
  ('buzzer-beater','patineur','Buzzer Beater','+3 en Tir dans la dernière minute de chaque période','chaque match',null),
  ('crowd-pleaser','patineur','Crowd Pleaser','+1 à une compétence au hasard à domicile','domicile','coach Elite Crowd Pleaser'),
  ('egg-breaker','patineur','Egg Breaker','+1 à toutes les compétences tant que le score est 0-0','situation',null),
  ('equalizer','patineur','Equalizer','Annule une compétence spéciale d''un adversaire (début de match)','chaque match','annulé par un coach adverse Master Equalizer'),
  ('human-shield','patineur','Human Shield','Plus de tirs bloqués','chaque match',null),
  ('inspire','patineur','Inspire','+1 au hasard aux coéquipiers SANS compétence spéciale quand il est sur la glace (un seul Inspire actif par joueur)','chaque match','coéquipiers sans compétence spéciale'),
  ('late-bloomer','patineur','Late Bloomer','Compétence spéciale débloquée à 25 ans','à 25 ans',null),
  ('mr-game-five','patineur','Mr Game Five','+1 à toutes les compétences au match 5 des playoffs','playoffs',null),
  ('on-fire','patineur','On Fire','+1 en Tir après chaque but (max +3)','situation',null),
  ('overtime-hero','patineur','Overtime Hero','+2 compétences au hasard en prolongation (hors tirs au but)','prolongation','coach Overtime Period'),
  ('patriot','patineur','Patriot','+1 au hasard à un compatriote en début de match (un bonus Patriot par joueur et par match)','chaque match','compatriotes dans le cinq'),
  ('penalty-killer','patineur','Penalty Killer','+1 en Patinage, Puissance, Défense, Mise en échec en infériorité','infériorité',null),
  ('playoff-beard','patineur','Playoff Beard','+1 à deux compétences au hasard en playoffs','playoffs',null),
  ('powerplay-specialist','patineur','Powerplay Specialist','+1 en Tir et Passe en supériorité','supériorité',null),
  ('rivalry','patineur','Rivalry','+1 à trois compétences au hasard contre le rival','contre le rival',null),
  ('second-wind','patineur','Second Wind','Condition pleine si mené ou à égalité à 10 min de la fin','situation',null),
  ('shootout-specialist','patineur','Shootout Specialist','Plus de chances de marquer en tirs au but et penalty','tirs au but',null),
  ('tactician','patineur','Tactician','L''équipe qui a le plus de Tacticians sur la glace : +1 au hasard à ses patineurs','chaque match','coach Master Tactician (départage)'),
  ('team-player','patineur','Team Player','+1 à deux compétences au hasard quand un autre Team Player est sur la glace','chaque match','un 2e Team Player dans la même ligne'),
  ('telepathy','patineur','Telepathy','Copie une compétence spéciale d''un patineur adverse (début de match)','chaque match',null),
  ('wrecking-ball','patineur','Wrecking Ball','Double les chances de grosse mise en échec ; la victime perd 1-3 % de condition non récupérable','chaque match',null),
  ('brick-wall','gardien','Brick Wall','+1 à toutes les compétences après 20 arrêts de suite ; un but annule le bonus','situation',null),
  ('crowd-pleaser','gardien','Crowd Pleaser','+1 à une compétence au hasard à domicile','domicile','coach Elite Crowd Pleaser'),
  ('equalizer','gardien','Equalizer','Annule une compétence spéciale d''un adversaire (début de match)','chaque match','annulé par un coach adverse Master Equalizer'),
  ('goalie-tandem','gardien','Goalie Tandem','Si titulaire et remplaçant l''ont : +2 à une compétence où l''autre excelle','chaque match','les 2 gardiens doivent l''avoir'),
  ('goalie-telepathy','gardien','Goalie Telepathy','Copie la compétence spéciale du gardien adverse (début de match)','chaque match',null),
  ('late-bloomer','gardien','Late Bloomer','Compétence spéciale débloquée à 25 ans','à 25 ans',null),
  ('mr-game-five','gardien','Mr Game Five','+1 à toutes les compétences au match 5 des playoffs','playoffs',null),
  ('overtime-hero','gardien','Overtime Hero','+2 compétences au hasard en prolongation (hors tirs au but)','prolongation','coach Overtime Period'),
  ('patriot','gardien','Patriot','+1 au hasard à un compatriote en début de match','chaque match','compatriotes'),
  ('playoff-beard','gardien','Playoff Beard','+1 à deux compétences au hasard en playoffs','playoffs',null),
  ('rivalry','gardien','Rivalry','+1 à trois compétences au hasard contre le rival','contre le rival',null),
  ('second-wind','gardien','Second Wind','Condition pleine si mené ou à égalité à 10 min de la fin','situation',null),
  ('shootout-stopper','gardien','Shootout Stopper','Plus de chances d''arrêter tirs au but et penalties','tirs au but',null),
  ('bracket-boss','coach','Bracket Boss','Deux joueurs au hasard : +1 à une compétence en playoffs de ligue','playoffs',null),
  ('bulldozer','coach','Bulldozer','Les adversaires perdent 2 % de condition non récupérable en plus sur une grosse mise en échec','chaque match','joueurs Wrecking Ball, Puissance élevée'),
  ('commander','coach','Commander','Notre capitaine : +1 à une compétence au hasard','chaque match','capitaine (Leadership + expérience)'),
  ('elite-crowd-pleaser','coach','Elite Crowd Pleaser','Jusqu''à trois Crowd Pleasers : +1 à une compétence de plus à domicile','domicile','joueurs Crowd Pleaser'),
  ('eye-for-talent','coach','Eye For Talent','Notre meilleur joueur de 25 ans ou moins : +1 à une compétence au hasard','chaque match','un jeune bien noté'),
  ('master-agitator','coach','Master Agitator','-1 en Discipline au meilleur patineur adverse','chaque match','plus de pénalités adverses → notre supériorité (PP)'),
  ('master-equalizer','coach','Master Equalizer','Annule une compétence Equalizer d''un adversaire','chaque match','adversaires avec Equalizer'),
  ('master-patriot','coach','Master Patriot','+1 au hasard à deux compatriotes du coach en début de match (un bonus Patriot par joueur)','chaque match','joueurs de la nation du coach'),
  ('master-tactician','coach','Master Tactician','Départage les Tacticians quand au moins un Tactician est sur la glace','chaque match','joueurs Tactician'),
  ('meditation','coach','Meditation','20 % de chances de regagner 1 % de condition en plus aux entractes','chaque match',null),
  ('first-period','coach','First Period','Trois joueurs au hasard : +1 à une compétence en 1re période','chaque match',null),
  ('second-period','coach','Second Period','Trois joueurs au hasard : +1 à une compétence en 2e période','chaque match',null),
  ('third-period','coach','Third Period','Trois joueurs au hasard : +1 à une compétence en 3e période','chaque match',null),
  ('overtime-period','coach','Overtime Period','Les Overtime Heroes : +1 à une compétence de plus en prolongation','prolongation','joueurs Overtime Hero'),
  ('shining-star','coach','Shining Star','Notre meilleur joueur : +1 à une compétence au hasard','chaque match',null)
) v(skill_id, porteur, nom, effet, quand, synergie);

-- Adéquation talents / poste pour tous les effectifs exportés (même règle que gold.hn_player_fit).
-- score_poste = note + 3 par talent fort clé − 3 si le talent faible est clé : hypothèse de tri (2026-10-23), à recaler après le premier match.
create or replace view gold.hn_league_player_fit with (security_invoker = true) as
select p.player_id, p.name, p.team_id, p.team, p.team_level, p.own, p.age, p.rating, x.position, x.ord = 1 as is_main,
       p.talent_strongest, p.talent_weakest, f.talents_cles, f.faible_cle,
       case when f.talents_cles = 2 and not f.faible_cle then 'idéal' when f.talents_cles >= 1 then 'correct' else 'contre-emploi' end as verdict,
       p.rating + 3 * f.talents_cles - case when f.faible_cle then 3 else 0 end as score_poste,
       p.special_skills, p.special_skill_count, p.skater, p.nation_id, p.salary, p.contract_to, p.contracts
from silver.hn_league_players p
cross join lateral jsonb_array_elements_text(p.positions) with ordinality x(position, ord)
cross join lateral (
  select (select count(*) from jsonb_array_elements_text(coalesce(p.talent_strongest, '[]'::jsonb)) t
           join gold.hn_position_keys k on k.position = x.position and k.skill = t)::int as talents_cles,
         exists (select 1 from gold.hn_position_keys k where k.position = x.position and k.skill = p.talent_weakest) as faible_cle
) f;

-- Lignes probables par équipe : 4 C, 4 LW, 4 RW, 2 LD, 2 RD, 2 G (consigne de l'utilisateur, 2026-10-23).
-- Le GM ne règle pas les lignes FRM, U21, U17 : cette vue dit qui devrait jouer, à confronter aux lignes réelles après le premier match.
-- 1) meilleurs au poste principal (score_poste), 2) trous comblés par un poste secondaire, 3) le reste en réserve, 4) trou restant = « manque ».
create or replace view gold.hn_depth_chart with (security_invoker = true) as
with need(position, n, ord) as (values ('C',4,1),('LW',4,2),('RW',4,3),('LD',2,4),('RD',2,5),('G',2,6)),
f as (select * from gold.hn_league_player_fit),
teams as (select distinct team, team_level, own from f),
p1 as (
  select f.*, row_number() over (partition by f.team, f.position order by f.score_poste desc, f.rating desc) as rk
  from f where f.is_main
),
sel1 as (select p1.* from p1 join need on need.position = p1.position where p1.rk <= need.n),
short as (
  select t.team, need.position, need.n - count(s.player_id) as missing
  from teams t cross join need left join sel1 s on s.team = t.team and s.position = need.position
  group by t.team, need.position, need.n having need.n - count(s.player_id) > 0
),
cand as (
  select distinct on (f.player_id) f.*, sh.missing
  from f join short sh on sh.team = f.team and sh.position = f.position
  where not f.is_main and f.player_id not in (select player_id from sel1)
  order by f.player_id, f.score_poste desc
),
sel2 as (
  select c.* from (select cand.*, row_number() over (partition by team, position order by score_poste desc) as rk2 from cand) c
  where c.rk2 <= c.missing
),
picked as (
  select team, team_level, own, position, player_id, name, age, rating, verdict, score_poste, talent_strongest, talent_weakest, 'poste principal' as origine from sel1
  union all
  select team, team_level, own, position, player_id, name, age, rating, verdict, score_poste, talent_strongest, talent_weakest, 'poste secondaire' from sel2
),
counts as (
  select t.team, t.team_level, t.own, need.position, need.n, need.ord, count(pk.player_id) as got
  from teams t cross join need left join picked pk on pk.team = t.team and pk.position = need.position
  group by t.team, t.team_level, t.own, need.position, need.n, need.ord
)
select pk.team, pk.team_level, pk.own, 'titulaire' as statut, pk.position, n.ord,
       row_number() over (partition by pk.team, pk.position order by pk.score_poste desc) as rang,
       pk.name, pk.age, pk.rating, pk.verdict, pk.score_poste, pk.origine, pk.talent_strongest, pk.talent_weakest
from picked pk join need n on n.position = pk.position
union all
select c.team, c.team_level, c.own, 'manque', c.position, c.ord, g.k, null, null, null, null, null, 'aucun joueur', null, null
from counts c cross join lateral generate_series(c.got + 1, c.n) g(k)
union all
select f.team, f.team_level, f.own, 'réserve', f.position, n.ord, null, f.name, f.age, f.rating, f.verdict, f.score_poste, 'poste principal', f.talent_strongest, f.talent_weakest
from f join need n on n.position = f.position
where f.is_main and f.player_id not in (select player_id from picked);

-- Compétences spéciales des coachs (débloquées), tous les coachs vus : notre staff, staffs adverses, fiches, marché.
-- actif_en_match = head coach [G:Coaches]. porteurs_pro_chez_nous = joueurs de notre PRO qui profitent de la compétence.
create or replace view gold.hn_coach_specials with (security_invoker = true) as
with coaches as (
  select distinct on (coach_id) * from (
    select 1 as prio, 'staff' as source, s.coach_id, s.name, s.age, s.xp, s.club as team, s.team_level, s.own, s.head_coach,
           s.rating, s.match_rating, coalesce(s.ofp,0)+coalesce(s.dfp,0)+coalesce(s.bat,0)+coalesce(s.pp,0)+coalesce(s.pk,0) as match_sum,
           s.special_skills, s.nation_id, s.day
    from silver.hn_club_staff s
    union all
    select 2, 'fiche', c.coach_id, c.name, c.age, c.xp, c.team, c.team_level, c.own, null,
           c.rating, c.match_rating, coalesce(c.ofp,0)+coalesce(c.dfp,0)+coalesce(c.bat,0)+coalesce(c.pp,0)+coalesce(c.pk,0),
           c.special_skills, c.nation_id, c.day
    from silver.hn_coach_profiles c
    union all
    select 3, 'marché', f.coach_id, f.name, f.age, f.xp, null, null, false, null,
           f.rating, f.match_rating, coalesce(f.ofp,0)+coalesce(f.dfp,0)+coalesce(f.bat,0)+coalesce(f.pp,0)+coalesce(f.pk,0),
           f.special_skills, f.nation_id, f.day
    from silver.hn_free_coaches f
  ) u order by coach_id, prio, day desc
),
pro as (select * from silver.hn_league_players where own and team_level = 'PRO'),
sk as (
  select c.*, s->>'id' as skill_id
  from coaches c, jsonb_array_elements(coalesce(c.special_skills, '[]'::jsonb)) s
  where s->>'id' <> 'unrevealed' and coalesce((s->>'unlocked')::bool, true)
)
select coalesce(sk.team, 'marché') as team, sk.team_level, sk.own, sk.head_coach, sk.name as coach, sk.age, 65 - sk.age as years_to_retire,
       sk.xp, sk.rating, sk.match_rating, sk.match_sum, sk.skill_id, r.nom, r.effet, r.quand,
       coalesce(sk.head_coach, false) as actif_en_match,
       case sk.skill_id
         when 'elite-crowd-pleaser' then (select count(*) from pro where pro.special_skills @> '[{"id":"crowd-pleaser"}]')
         when 'master-tactician' then (select count(*) from pro where pro.special_skills @> '[{"id":"tactician"}]')
         when 'overtime-period' then (select count(*) from pro where pro.special_skills @> '[{"id":"overtime-hero"}]')
         when 'master-patriot' then (select count(*) from pro where pro.nation_id = sk.nation_id)
         when 'eye-for-talent' then (select count(*) from pro where pro.age <= 25)
       end as porteurs_pro_chez_nous,
       r.synergie, sk.source, sk.day
from sk left join gold.hn_special_skills r on r.skill_id = sk.skill_id and r.porteur = 'coach';

-- Comparaison des clubs PRO exportés (nous, Leszno Bulls = référence, finalistes) : effectif, adéquation, head coach.
create or replace view gold.hn_club_compare with (security_invoker = true) as
with p as (
  select lp.*, row_number() over (partition by lp.team_id order by lp.rating desc) as rk
  from silver.hn_league_players lp where lp.team_level = 'PRO'
),
fit as (
  select team, count(*) filter (where verdict = 'idéal') as ideal, count(*) filter (where verdict = 'contre-emploi') as contre_emploi
  from gold.hn_league_player_fit where is_main and team_level = 'PRO' group by team
),
hc as (
  select distinct on (club) club, name as head_coach, match_rating,
         coalesce(ofp,0)+coalesce(dfp,0)+coalesce(bat,0)+coalesce(pp,0)+coalesce(pk,0) as hc_match_sum,
         (select string_agg(x->>'id', ', ') from jsonb_array_elements(coalesce(special_skills, '[]'::jsonb)) x where x->>'id' <> 'unrevealed') as hc_specials
  from silver.hn_club_staff where team_level = 'PRO' and head_coach order by club, day desc
),
staff as (
  select club, sum(coalesce(ofp,0)+coalesce(dfp,0)+coalesce(bat,0)+coalesce(pp,0)+coalesce(pk,0)) as staff_match_sum
  from silver.hn_club_staff where team_level = 'PRO' group by club
)
select p.team, bool_or(p.own) as own, count(*) as joueurs, round(avg(p.rating) filter (where p.rk <= 20), 1) as note_top20,
       max(p.rating) as note_max, round(avg(p.age), 1) as age_moyen,
       count(*) filter (where p.main_position = 'C') as c, count(*) filter (where p.main_position = 'LW') as lw,
       count(*) filter (where p.main_position = 'RW') as rw, count(*) filter (where p.main_position = 'LD') as ld,
       count(*) filter (where p.main_position = 'RD') as rd, count(*) filter (where p.main_position = 'G') as g,
       sum(coalesce(p.special_skill_count, 0)) as specials, sum(p.salary) as masse_salariale,
       max(fit.ideal) as ideal, max(fit.contre_emploi) as contre_emploi,
       max(hc.head_coach) as head_coach, max(hc.hc_match_sum) as hc_match_sum, max(hc.hc_specials) as hc_specials,
       max(staff.staff_match_sum) as staff_match_sum
from p
left join fit on fit.team = p.team
left join hc on hc.club = p.team
left join staff on staff.club = p.team
group by p.team;

-- Valeur d'un échange : joueur par joueur (nos équipes et adversaires exportés), avant/après sur le cap space de la saison suivante.
-- cap_space_apres : + salaire si on le cède (contrat PRO), − salaire si on l'acquiert [G:Finances]. Contrats FRM hors plafond.
create or replace view gold.hn_trade_value with (security_invoker = true) as
with s as (select max(season) as season from silver.hn_season),
cap as (select cap_space from gold.hn_cap_outlook where cap_space is not null order by season limit 1)
select f.team, f.team_level, f.own, f.name, f.age, f.rating, f.position, f.verdict, f.talents_cles, f.talent_strongest, f.talent_weakest,
       (select string_agg(coalesce(r.nom, x->>'id'), ', ')
          from jsonb_array_elements(coalesce(f.special_skills, '[]'::jsonb)) x
          left join gold.hn_special_skills r on r.skill_id = x->>'id' and r.porteur = case when f.skater then 'patineur' else 'gardien' end) as specials,
       f.salary, f.contract_to, n.salaire_saison_suivante,
       cap.cap_space as cap_space_avant,
       cap.cap_space + case when f.own then coalesce(n.salaire_saison_suivante, 0) else -coalesce(n.salaire_saison_suivante, 0) end as cap_space_apres
from gold.hn_league_player_fit f
cross join s cross join cap
left join lateral (
  select (x->>'salary')::bigint as salaire_saison_suivante
  from jsonb_array_elements(coalesce(f.contracts, '[]'::jsonb)) x
  where s.season + 1 between (x->>'from')::int and (x->>'to')::int and not coalesce((x->>'frm')::bool, false)
  limit 1) n on true
where f.is_main;

-- Progression par joueur (nos équipes) entre le premier et le dernier relevé.
create or replace view gold.hn_player_progress with (security_invoker = true) as
with s as (
  select player_id, name, team_level, day, rating, age, skills,
         row_number() over (partition by player_id order by day) as rn_first,
         row_number() over (partition by player_id order by day desc) as rn_last
  from silver.hn_player_snapshots
)
select l.name, l.team_level, l.age, f.day as from_day, l.day as to_day, l.day - f.day as days,
       f.rating as rating_from, l.rating as rating_to, l.rating - f.rating as rating_delta,
       (select coalesce(sum((b->>'lvl')::int), 0) from jsonb_array_elements(l.skills) b)
         - (select coalesce(sum((a->>'lvl')::int), 0) from jsonb_array_elements(f.skills) a) as skill_points_delta,
       (select string_agg(b->>'id' || ' ' || (a->>'lvl') || '→' || (b->>'lvl'), ', ')
          from jsonb_array_elements(l.skills) b join jsonb_array_elements(f.skills) a on a->>'id' = b->>'id'
          where (b->>'lvl')::int <> (a->>'lvl')::int) as changes
from s f join s l on l.player_id = f.player_id and l.rn_last = 1
where f.rn_first = 1 and l.day > f.day;

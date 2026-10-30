-- Hardwood : vues gold (une vue = un tableau prêt, zéro agent). Conçu le 2026-10-30.
-- Walk-ons : jamais dans le depth chart proposé ni dans les exports demandés (décision de l'utilisateur, 2026-10-30 :
-- « on n'exporte pas les walk-ons, inutiles »). Ils restent visibles dans hw_effectif (colonne walk_on) pour mémoire.
-- Heures : matchs simulés à 9:00 heure du Pacifique ; on convertit en Europe/Paris.

-- 1. Note de chaque joueur à chaque poste (compétences clés de silver.hw_ref_position_keys, Aide docs).
--    cles = moyenne des compétences clés (0-20) ; score = 0,6 × cles + 0,4 × SI/14 (niveau général : « le talent compte
--    le plus », Aide docs ; pondération [H] à confronter aux matchs). Maîtrise lue dans « Positions ».
create or replace view gold.hw_player_pos_scores with (security_invoker = true) as
with k as (
  select r.*, k.pos as kpos, k.ord, k.height_min_m,
         case k.pos
           when 'PG' then (r.iq + r.pass + r.hnd + r.spd) / 4.0
           when 'SG' then (r.os + r.spd) / 2.0
           when 'SF' then (r.os + (r.idef + r.pdef) / 2.0 + r.spd) / 3.0
           else (r.ins + r.reb) / 2.0 end as cles
  from silver.hw_roster r cross join silver.hw_ref_position_keys k
)
select r.player_id, r.name, r.kpos as pos, r.ord, r.height_m, r.scholarship, r.injured, r.injury_days,
       round(r.cles, 1) as cles, round(0.6 * r.cles + 0.4 * r.si / 14.0, 1) as score,
       case when coalesce(r.positions, '') ~ ('(^|\s)' || r.kpos || '(\s|$)') then 'maîtrisé'
            when coalesce(r.positions, '') ~ ('(^|\s)' || lower(r.kpos) || '(\s|$)') then 'apprentissage'
            else 'jamais' end as mastery,
       r.height_min_m is null or r.height_m >= r.height_min_m as height_ok
from k r;

-- 2. Adéquation : meilleur poste, note au poste actuel, contre-emploi (écart ≥ 2 points).
create or replace view gold.hw_player_fit with (security_invoker = true) as
with s as (select * from gold.hw_player_pos_scores),
best as (
  select distinct on (player_id) player_id, pos as best_pos, score as best_score
  from s where height_ok order by player_id, score desc, ord
)
select r.player_id, r.name, r.pos as current_pos, r.positions,
       cur.score as current_score, b.best_pos, b.best_score,
       case when b.best_score - cur.score >= 2 then 'contre-emploi : ' || b.best_pos
            when b.best_pos <> r.pos then 'aussi ' || b.best_pos else 'bon poste' end as fit,
       (select string_agg(x.pos || ' ' || x.score, ' · ' order by x.ord) from s x where x.player_id = r.player_id) as scores
from silver.hw_roster r
left join s cur on cur.player_id = r.player_id and cur.pos = r.pos
left join best b on b.player_id = r.player_id;

-- 3. Effectif complet : compétences, poste, potentiel (plafond de SI), stats, blessure, redshirt, départ, progression.
create or replace view gold.hw_effectif with (security_invoker = true) as
select r.name, r.pos, r.class, not r.scholarship as walk_on, r.height_m, pr.weight_kg, pr.wingspan_m,
       r.si, r.pot, c.cap_min as si_cap_min, c.cap_max as si_cap_max, c.cap_max - r.si as marge_max, r.stars,
       f.fit, f.current_score, f.best_pos, f.best_score, r.positions,
       r.injury_days, m.red_shirt, m.max_minutes, m.green_light, m.off_positioning, m.foul_hook,
       st.g, st.gs, st.min, st.pts, st.reb, st.ast, st.tov, st.fg_pct, st.tp_pct, st.plus_minus,
       r.class in ('SR', 'RS SR') as part_fin_saison,
       d.skills_up as progres_derniere_maj,
       pr.evaluation, r.player_id
from silver.hw_roster r
left join gold.hw_player_fit f using (player_id)
left join silver.hw_ref_potential_caps c on c.pot = r.pot
left join silver.hw_management m using (player_id)
left join silver.hw_player_profile pr using (player_id)
left join silver.hw_development d on d.name = r.name
left join silver.hw_player_stats st
       on st.name = left(r.name, 1) || '. ' || substr(r.name, strpos(r.name, ' ') + 1);

-- 4. Depth chart proposé : boursiers valides seulement (ni blessés, ni redshirt coché, ni walk-ons).
--    Remplissage glouton dans l'ordre du moteur (PG, C, PF, SF, SG), titulaires puis 2e et 3e rideau.
--    Note retenue = score + 1 si poste maîtrisé, − 2 si jamais joué (malus hors poste réel non chiffré [H]).
create or replace view gold.hw_depth_suggest with (security_invoker = true) as
with recursive slots as (
  select row_number() over (order by d, o) as k, d as depth, pos
  from (values ('PG', 1), ('C', 2), ('PF', 3), ('SF', 4), ('SG', 5)) p(pos, o), generate_series(1, 3) d
), cand as (
  select s.player_id, s.name, s.pos, s.score, s.mastery,
         s.score + case s.mastery when 'maîtrisé' then 1 when 'jamais' then -2 else 0 end as adj
  from gold.hw_player_pos_scores s
  left join silver.hw_management m using (player_id)
  where s.scholarship and not s.injured and coalesce(m.red_shirt, 'non') <> 'oui' and s.height_ok
), pick (k, used, depth, pos, player_id, name, score, mastery) as (
  select 0::bigint, array[]::int[], null::int, null::text, null::int, null::text, null::numeric, null::text
  union all
  select s.k, p.used || c.player_id, s.depth, s.pos, c.player_id, c.name, c.score, c.mastery
  from pick p
  join slots s on s.k = p.k + 1
  left join lateral (
    select * from cand c where c.pos = s.pos and c.player_id <> all (array_remove(p.used, null))
    order by c.adj desc, c.score desc limit 1) c on true
), saved as (
  select dc.depth, dc.pos, dc.short_name, dc.injured from silver.hw_depth_chart dc
)
select p.depth, p.pos, p.name as propose, p.score, p.mastery,
       sv.short_name || case when sv.injured then ' (blessé)' else '' end as actuel,
       case when p.name is null and p.depth = 1 then '🟥 aucun boursier valide'
            when p.name is null then '— vide (un joueur peut doubler deux postes)'
            when coalesce(sv.short_name, '-') = '-' then '🟧 à saisir'
            when sv.short_name <> left(p.name, 1) || '. ' || substr(p.name, strpos(p.name, ' ') + 1) or sv.injured then '🟧 à changer'
            else '✔' end as controle,
       (select w.name || ' ' || w.score from gold.hw_player_pos_scores w
         where not w.scholarship and w.pos = p.pos and not w.injured and w.score > coalesce(p.score, 0) + 2
         order by w.score desc limit 1) as walk_on_meilleur
from pick p
left join saved sv on sv.depth = p.depth and sv.pos = p.pos
where p.k > 0
order by p.depth, case p.pos when 'PG' then 1 when 'SG' then 2 when 'SF' then 3 when 'PF' then 4 else 5 end;

-- 5. Saison match par match : notre tactique, efficacité par zone (nous / eux), défense réellement jouée, SI pondéré.
create or replace view gold.hw_season_games with (security_invoker = true) as
select g.game_id, to_date(regexp_replace(g.game_date, '(\d+)(st|nd|rd|th)', '\1'), 'Month DD, YYYY') as game_day, g.game_type, g.opponent, g.is_home, g.my_result, g.my_margin,
       g.my_pace, g.my_emphasis, g.my_man_pct, g.my_zone_pct, g.my_pressure_pct, g.my_extend, g.my_sub_mode,
       round(100.0 * us.rim_m / nullif(us.rim_a, 0)) as rim_pct, us.rim_a,
       round(100.0 * us.inside_m / nullif(us.inside_a, 0)) as in_pct, us.inside_a,
       round(100.0 * us.mid_m / nullif(us.mid_a, 0)) as mid_pct, us.mid_a,
       round(100.0 * us.three_m / nullif(us.three_a, 0)) as three_pct, us.three_a,
       round(100.0 * op.rim_m / nullif(op.rim_a, 0)) as opp_rim_pct, op.rim_a as opp_rim_a,
       round(100.0 * op.inside_m / nullif(op.inside_a, 0)) as opp_in_pct,
       round(100.0 * op.mid_m / nullif(op.mid_a, 0)) as opp_mid_pct,
       round(100.0 * op.three_m / nullif(op.three_a, 0)) as opp_three_pct, op.three_a as opp_three_a,
       op.def_man_pct as opp_man, op.def_zone_pct as opp_zone, op.def_pressure_pct as opp_press, op.extend_start as opp_extend,
       us.weighted_si as my_wsi, op.weighted_si as opp_wsi, us.tpi as my_tpi, op.tpi as opp_tpi,
       g.my_injuries, g.my_overworked
from silver.hw_games g
left join silver.hw_game_teams us on us.game_id = g.game_id and us.team <> g.opponent
left join silver.hw_game_teams op on op.game_id = g.game_id and op.team = g.opponent
where g.my_result is not null;

-- 6. Victoires contre défaites, toute la saison (exhibitions à part).
create or replace view gold.hw_vd_compare with (security_invoker = true) as
select case when game_type = 'Exhibition' then 'exhibition' else 'officiel' end as phase, my_result,
       count(*) as matchs, round(avg(my_margin), 1) as ecart,
       round(avg(rim_pct)) as rim_pct, round(avg(in_pct)) as in_pct, round(avg(mid_pct)) as mid_pct,
       round(avg(three_pct)) as three_pct, round(avg(three_a), 1) as three_a,
       round(avg(opp_three_pct)) as opp_three_pct, round(avg(opp_rim_pct)) as opp_rim_pct,
       round(avg(opp_wsi - my_wsi), 1) as ecart_wsi_adverse, round(avg(opp_press), 1) as opp_press
from gold.hw_season_games
group by 1, 2;

-- 7. Recrues : recherche de prospects + nos suivis. Région USA Central (Illinois, Indiana, Missouri, Ohio, West Virginia).
--    Verdict : cible = région, pot ≥ 12, au plus 1 équipe à High, ≤ 3 étoiles ; dur = 2 équipes ou plus à High ou 4-5 étoiles ;
--    futur = pas encore engageable. besoin = poste d'un boursier qui part en fin de saison. rang = ordre dans le verdict.
create or replace view gold.hw_recruit_board with (security_invoker = true) as
with p as (
  select prospect, class, pos, height_m, state, si, pot, stars, top_skills, teams_interested, teams_high,
         our_interest, we_offered, null::int as contacts
  from silver.hw_prospects
  union all
  select prospect, class, pos, height_m, trim(split_part(hometown, ',', 2)), si, pot, stars, top_skills,
         nullif(substring(competition from '^(\d+) Team'), '')::int, null, interest, offered, contacts
  from silver.hw_recruiting
), u as (
  select distinct on (prospect) * from p order by prospect, contacts nulls last
), own as (select schol_open_next, points, points_max, round from silver.hw_recruiting limit 1),
leaving as (select distinct pos from silver.hw_roster where scholarship and class in ('SR', 'RS SR')),
v as (
  select u.*, u.state in ('Illinois', 'Indiana', 'Missouri', 'Ohio', 'West Virginia') as region,
         case when u.class not in ('HS SR', 'JC SO') then 'futur'
              when u.stars >= 4 then 'dur (4-5 étoiles en D3)'
              when coalesce(u.teams_high, 0) >= 2 then 'dur'
              when u.pot >= 12 and coalesce(u.teams_high, 0) <= 1
                   and u.state in ('Illinois', 'Indiana', 'Missouri', 'Ohio', 'West Virginia') then 'cible'
              when u.pot >= 12 and coalesce(u.teams_high, 0) = 0 then 'cible hors région'
              when u.pot >= 11 then 'secondaire'
              else 'écarter (pot ≤ 10)' end as verdict
  from u
)
select row_number() over (partition by v.verdict order by (v.pos in (select pos from leaving)) desc, v.pot desc, v.si desc) as rang,
       v.verdict, v.prospect, v.class, v.pos, v.pos in (select pos from leaving) as besoin, v.height_m, v.state, v.region,
       v.si, v.pot, c.cap_max as si_cap_max, v.stars, v.top_skills,
       v.teams_interested, v.teams_high, v.our_interest, v.we_offered, v.contacts,
       v.class in ('HS SR', 'JC SO') as engageable_cette_saison,
       own.schol_open_next, own.points, own.points_max, own.round
from v cross join own
left join silver.hw_ref_potential_caps c on c.pot = v.pot;

-- 8. Coachs : notre staff contre les meilleurs libres. Note = Off + Def + Tac + Dev + Mot + Rec ; déclin du head coach 55-70 ans.
create or replace view gold.hw_coach_board with (security_invoker = true) as
with ours as (
  select role, coach, age, off, def, tac, dev, mot, rec, off + def + tac + dev + mot + rec as total, salary_m
  from silver.hw_coaches
), free as (
  select 'Libre' as role, coach, age, off, def, tac, dev, mot, rec, off + def + tac + dev + mot + rec as total, salary_m
  from silver.hw_coach_market where available
)
select * from (select 'nous' as groupe, * from ours) a
union all
select * from (select 'libre (meilleur total, < 55 ans)', * from free where age < 55 order by total desc limit 5) b
union all
select * from (select 'libre (meilleur Rec, < 55 ans)', * from free where age < 55 order by rec desc, total desc limit 5) c
union all
select * from (select 'libre (meilleur Dev, < 55 ans)', * from free where age < 55 order by dev desc, total desc limit 5) d;

-- 9. Aujourd'hui : prochain match (heure de Paris), bilan, phase, recrutement.
create or replace view gold.hw_today with (security_invoker = true) as
with s as (
  select *, to_date(substring(sim_time from '^\w+ (\w+ \d+)') || ' ' || extract(year from captured_at), 'Mon DD YYYY') as real_day
  from silver.hw_schedule
), nxt as (select * from s where not_played order by game_no limit 1)
select (now() at time zone 'Europe/Paris')::date as jour,
       (select game_date_txt from silver.hw_own) as date_du_jeu,
       nxt.game_type as prochain_type, case when nxt.is_home then 'vs ' || nxt.visitor else '@ ' || nxt.home end as prochain_adversaire,
       to_char(((nxt.real_day + time '09:00') at time zone 'America/Los_Angeles') at time zone 'Europe/Paris', 'DD/MM HH24:MI') as prochain_paris,
       (select count(*) filter (where my_result = 'W') || '-' || count(*) filter (where my_result = 'L') from s where game_type <> 'Exhibition') as bilan,
       (select count(*) filter (where my_result = 'W') || '-' || count(*) filter (where my_result = 'L') from s where game_type = 'Conference') as bilan_conf,
       (select min(real_day) from s where game_type = 'Conference') as debut_conference,
       (select min(real_day) from s where game_type = 'Conference') - (now() at time zone 'Europe/Paris')::date as jours_avant_conference,
       (select round || '/' || rounds from silver.hw_recruiting limit 1) as tour_recrutement,
       (select points || '/' || points_max from silver.hw_recruiting limit 1) as points_recrutement,
       (select schol_open_next from silver.hw_recruiting limit 1) as bourses_libres
from nxt;

-- 10. État des exports : fraîcheur de chaque page utile. Pages joueur = boursiers seulement (walk-ons exclus).
create or replace view gold.hw_exports_state with (security_invoker = true) as
with need(page_type, quoi, max_jours, ord) as (values
  ('roster_id', 'Roster', 1, 1), ('schedule_id', 'Schedule', 1, 2), ('statistics_id', 'Statistics', 1, 3),
  ('recruiting_id', 'Recruiting', 1, 4), ('prospect_results', 'Prospect Search (région)', 3, 5),
  ('conference_id', 'Conference', 1, 6), ('rankings', 'Rankings', 3, 7),
  ('development_id', 'Development (après jeudi/dimanche)', 4, 8),
  ('depth_chart_id', 'Depth Chart', 7, 9), ('game_tactics_id', 'Game Tactics', 7, 10), ('management', 'Game Management', 7, 11),
  ('coaches_id', 'Coaches', 7, 12), ('coach_results', 'Coach Search', 7, 13)
), last as (select page_type, max(captured_at) as last from silver.hw_pages group by 1)
select n.quoi, to_char(l.last at time zone 'Europe/Paris', 'DD/MM HH24:MI') as dernier,
       case when l.last is null then '🟥 jamais'
            when l.last < now() - make_interval(days => n.max_jours) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from need n left join last l using (page_type)
union all
select 'Feuilles de match (' || (select count(*) from silver.hw_schedule where my_result is not null) || ' joués)',
       (select count(*) from silver.hw_games)::text || ' en base',
       case when (select count(*) from silver.hw_games) < (select count(*) from silver.hw_schedule where my_result is not null)
            then '🟥 manque le dernier match' else '🟩 à jour' end
union all
select 'Pages joueur (boursiers, sans walk-ons)',
       (select count(*) from silver.hw_player_profile)::text || ' / ' || (select count(*) from silver.hw_roster where scholarship)::text,
       case when exists (select 1 from silver.hw_roster r where r.scholarship
                         and not exists (select 1 from silver.hw_player_profile p where p.player_id = r.player_id))
            then '🟧 boursier sans page' else '🟩 à jour' end;

-- 11. Alertes du jour (rouge d'abord). Jamais reprises telles quelles : le registre fait-… et les exports du jour passent avant.
create or replace view gold.hw_daily_alerts with (security_invoker = true) as
select * from (
  select 1 as prio, '🟥 URGENT' as niveau, 'Composition' as categorie,
         'Depth chart : ' || pos || ' rang ' || depth || ' = ' || actuel || ', mettre ' || propose as alerte
  from gold.hw_depth_suggest where controle = '🟧 à changer' and depth = 1
  union all
  select 1, '🟥 URGENT', 'Personnel',
         'Dernier jour pour changer un assistant (conférence dans ' || jours_avant_conference || ' j) : voir gold.hw_coach_board'
  from gold.hw_today where jours_avant_conference between 0 and 2
  union all
  select 1, '🟥 URGENT', 'Export', quoi || ' : ' || statut from gold.hw_exports_state where statut like '🟥%'
  union all
  select 2, '🟧 IMPORTANT', 'Académie/Draft',
         'Points de recrutement ' || points || '/' || points_max || ' : au-delà de 45 ils sont perdus, les dépenser'
  from (select distinct points, points_max from silver.hw_recruiting) x where points >= points_max - 5
  union all
  select 2, '🟧 IMPORTANT', 'Composition',
         'Depth chart : ' || pos || ' rang ' || depth || ' = ' || coalesce(actuel, 'vide') || ', mettre ' || propose
  from gold.hw_depth_suggest where controle in ('🟧 à changer', '🟧 à saisir') and depth > 1
  union all
  select 2, '🟧 IMPORTANT', 'Analyse', 'Overwork au dernier match : ' || my_overworked
  from (select my_overworked from gold.hw_season_games order by game_day desc limit 1) x
  where coalesce(my_overworked, 'none') not in ('none', '')
  union all
  select 3, '🟩 SUIVI', 'Export', quoi || ' : ' || statut from gold.hw_exports_state where statut like '🟧%'
) a
order by prio, categorie;

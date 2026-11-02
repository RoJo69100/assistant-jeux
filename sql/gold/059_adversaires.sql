-- Vues « adversaires » par jeu (plan de conception, étape 0c : l'agent `tactique` absorbe l'étude de
-- l'adversaire). BasketVibe a déjà gold.bv_next_opponents, gold.bv_saisie_adversaires, gold.bv_match_opp_focus.
-- Même forme partout : nos 3 prochains matchs (par club / équipe), l'adversaire, son rang et son bilan,
-- sa forme, et nos résultats contre lui cette saison (my_result de la base, jamais le score brut).
-- Derby Manager : le calendrier exporté ne contient que des matchs joués → une ligne par adversaire de ligue.
-- Lecture : select * from gold.<p>_adversaires limit 30;

-- Six Zero League
create or replace view gold.sz_adversaires with (security_invoker = true) as
with f as (
    select distinct on (match_id) * from silver.sz_fixtures order by match_id, day desc
), st as (
    select * from silver.sz_standings where day = (select max(day) from silver.sz_standings)
), moi as (select team_id from st where is_mine limit 1),
prochains as (
    select f.round, f.match_id,
           case when f.home_team_id = (select team_id from moi) then f.away_team_id else f.home_team_id end as adv_id,
           case when f.home_team_id = (select team_id from moi) then f.away_team else f.home_team end as adversaire,
           f.home_team_id = (select team_id from moi) as domicile,
           row_number() over (order by f.round) as n
    from f where f.is_mine and f.status = 'pending'
)
select p.round as journee, p.adversaire, p.domicile, s.position as rang_adv, s.is_bot as bot,
       s.wins || '-' || s.draws || '-' || s.losses as bilan_vnd, s.points, s.goals_for as bp, s.goals_against as bc,
       s.form as forme_adv,
       (select string_agg('J' || f.round || ' ' || f.home_score || '-' || f.away_score, ', ' order by f.round)
          from f where f.is_mine and f.status = 'finished'
           and p.adv_id in (f.home_team_id, f.away_team_id)) as nos_confrontations
from prochains p left join st s on s.team_id = p.adv_id
where p.n <= 3;

-- Team Soccer (les deux clubs)
create or replace view gold.ts_adversaires with (security_invoker = true) as
with m as (
    select * from silver.ts_matches where my_team_id is not null
      and my_team_id in (home_team_id, away_team_id)
), club as (select my_team_id, team as club from silver.ts_standings where is_mine),
prochains as (
    select m.my_team_id, m.match_date_paris, m.competition,
           case when m.home_team_id = m.my_team_id then m.away_team_id else m.home_team_id end as adv_id,
           case when m.home_team_id = m.my_team_id then m.away_team else m.home_team end as adversaire,
           m.home_team_id = m.my_team_id as domicile,
           row_number() over (partition by m.my_team_id order by m.match_date_paris) as n
    from m where m.status = 'scheduled'
)
select c.club, p.match_date_paris as date_paris, p.competition, p.adversaire, p.domicile,
       s.position as rang_adv, s.wins || '-' || s.draws || '-' || s.losses as bilan_vnd, s.points,
       s.goals_for as bp, s.goals_against as bc,
       (select string_agg(case when x.home_team_id = x.my_team_id then x.home_score || '-' || x.away_score
                               else x.away_score || '-' || x.home_score end
                          || case when x.home_team_id = x.my_team_id then ' (dom.)' else ' (ext.)' end, ', '
                          order by x.match_date_paris)
          from m x where x.my_team_id = p.my_team_id and x.status = 'finished'
           and p.adv_id in (x.home_team_id, x.away_team_id)) as nos_scores_pour_contre
from prochains p
left join club c on c.my_team_id = p.my_team_id
left join silver.ts_standings s on s.my_team_id = p.my_team_id and s.team_id = p.adv_id
where p.n <= 3;

-- Hockey Nation (par équipe PRO / FRM / U21 / U17). `winner` est un id d'équipe : pas de bilan de l'adversaire
-- tant que la correspondance id → nom n'est pas en silver ; rang et bilan : silver.hn_standings (JSON).
create or replace view gold.hn_adversaires with (security_invoker = true) as
with g as (
    select distinct on (game_id) * from silver.hn_games order by game_id, captured_at desc
), prochains as (
    select g.team_level, g.scheduled_at, g.game_type,
           case when g.home_is_mine then g.away else g.home end as adversaire,
           g.home_is_mine as domicile,
           row_number() over (partition by g.team_level order by g.scheduled_at) as n
    from g where (g.home_is_mine or g.away_is_mine) and g.status = 'upcoming'
)
select p.team_level as equipe, to_char(p.scheduled_at at time zone 'Europe/Paris', 'YYYY-MM-DD HH24:MI') as date_paris,
       p.game_type, p.adversaire, p.domicile,
       (select count(*) from g x where x.status = 'ended' and p.adversaire in (x.home, x.away)) as matchs_adv_en_base,
       (select string_agg(x.my_result, '' order by x.scheduled_at desc)
          from (select * from g y where y.status = 'ended' and p.adversaire in (y.home, y.away) and (y.home_is_mine or y.away_is_mine)
                order by y.scheduled_at desc limit 5) x) as nos_resultats_contre_lui
from prochains p where p.n <= 3;

-- Hardwood
create or replace view gold.hw_adversaires with (security_invoker = true) as
with s as (
    select distinct on (game_no) * from silver.hw_schedule order by game_no, captured_at desc
), st as (
    select distinct on (team) * from silver.hw_standings order by team, captured_at desc
), prochains as (
    select s.game_no, s.game_date, s.game_type,
           case when s.is_home then s.visitor else s.home end as adversaire, s.is_home as domicile,
           row_number() over (order by s.game_no) as n
    from s where s.not_played
)
select p.game_no as match_no, p.game_date, p.game_type, p.adversaire, p.domicile,
       t.conference, t.rank as rang_conf_adv, t.w || '-' || t.l as bilan_vd, t.conf_w || '-' || t.conf_l as bilan_conf,
       t.pf, t.pa, t.streak, t.rpi, t.sos,
       (select string_agg(x.my_result || ' ' || x.my_margin, ', ' order by x.game_date)
          from silver.hw_games x where x.opponent = p.adversaire) as nos_resultats_ecart
from prochains p left join st t on t.team = p.adversaire
where p.n <= 3;

-- Derby Manager (pas de calendrier à venir exporté : un adversaire de ligue par ligne, par club)
create or replace view gold.dm_adversaires with (security_invoker = true) as
with st as (
    select distinct on (competition, team) * from silver.dm_standings order by competition, team, captured_at desc
), m as (select * from silver.dm_matches)
select c.club, s.competition, s.rank as rang_adv, s.team as adversaire,
       s.w || '-' || s.d || '-' || s.l as bilan_vnd, s.pts, s.gf as bp, s.ga as bc, s.form as forme_adv,
       (select string_agg(x.my_result || ' ' || x.gf || '-' || x.ga, ', ' order by x.played_at)
          from m x where x.team_id = c.team_id and x.opponent = s.team) as nos_resultats,
       (select round(avg(x.xga), 2) from m x where x.team_id = c.team_id and x.opponent = s.team) as xg_concede_moy
from st s join silver.dm_clubs c on true
where exists (select 1 from m x where x.team_id = c.team_id and x.opponent = s.team);

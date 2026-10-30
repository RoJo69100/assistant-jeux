-- Derby Manager : vues gold (une vue = un tableau prêt, zéro agent). Conçu le 2026-10-30.
-- Toujours par club (team_id 547 Queen of the South, 307 Marmandes) : jamais de total mélangé.
-- Montants : par jour (salaires, recettes) ; prix et argent en unités du jeu.

-- 1. État des exports : chaque page attendue, par club, avec son âge. « manquant » = jamais reçue.
create or replace view gold.dm_exports_etat with (security_invoker = true) as
with attendu(ordre, page, motif, quand) as (values
  (1, 'Équipe (effectif + entraînement + calendrier)', '/teams/%s(\?|$)', 'chaque jour'),
  (2, 'Rapport des matchs (JSON)',                     '/teams/%s/matches', 'après chaque match'),
  (3, 'Finances',                                       '/teams/%s/finances', 'chaque jour'),
  (4, 'Installations',                                  '/teams/%s/facilities', 'chaque semaine'),
  (5, 'School',                                         '/teams/%s/school', 'chaque jour'),
  (6, 'Graduates',                                      '/teams/%s/development', 'chaque semaine')
), cap as (
  select c.team_id, c.club, a.ordre, a.page, a.quand, max(r.captured_at) as derniere
  from silver.dm_clubs c cross join attendu a
  left join bronze.raw_pages r on r.game = 'derbymanager' and r.page_url ~ format(a.motif, c.team_id)
  group by c.team_id, c.club, a.ordre, a.page, a.quand
)
select team_id, club, ordre, page, quand, derniere,
       round(extract(epoch from now() - derniere) / 3600) as age_h,
       case when derniere is null then 'manquant'
            when quand = 'chaque jour' and now() - derniere > interval '20 hours' then 'en retard'
            when quand = 'chaque semaine' and now() - derniere > interval '7 days' then 'en retard'
            else 'à jour' end as etat
from cap
union all
select null, 'commun', 10 + o, p, 'chaque jour', d, round(extract(epoch from now() - d) / 3600),
       case when d is null then 'manquant' when now() - d > interval '24 hours' then 'en retard' else 'à jour' end
from (values (1, 'Marché', (select max(captured_at) from bronze.raw_pages where game = 'derbymanager' and page_type like 'market%')),
             (2, 'Transferts conclus', (select max(captured_at) from bronze.raw_pages where game = 'derbymanager' and page_type = 'transfers')),
             (3, 'Classement de la ligue', (select max(captured_at) from bronze.raw_pages where game = 'derbymanager' and page_type = 'competitions_id'))) v(o, p, d);

-- 2. Effectif : une ligne par joueur, dans l'ordre des postes, avec la composition enregistrée (slot).
create or replace view gold.dm_effectif with (security_invoker = true) as
select s.team_id, c.club, s.slot, s.shirt, s.name, s.pos, s.age, s.tier, s.role,
       s.intensity, s.condition_pct, s.form, s.sharpness, s.fit, s.exp, s.pot, s.skill, s.tr,
       s.satisfaction_pct, s.contract_days, s.salary, s.price,
       s.apps, s.goals, s.assists, s.rating, s.bu, s.pbu,
       round((s.han + s.mar + s.tac + s.posi + s.aer + s.agi + s.ant + s.cre + s.pas + s.bal + s.fir + s.tec + s.acc + s.sho + s.hea + s.rea) / 16.0, 1) as moy16,
       s.han, s.mar, s.tac, s.posi, s.aer, s.agi, s.ant, s.cre, s.pas, s.bal, s.fir, s.tec, s.acc, s.sho, s.hea, s.rea,
       case when s.pos ~ '^GK' then 1 when s.pos ~ '^D' then 2 when s.pos ~ '^M' then 3 else 4 end as ligne
from silver.dm_squad s join silver.dm_clubs c using (team_id)
order by s.team_id, ligne, s.price desc;

-- 3. Matchs de la saison : résultat (gf/ga de la base, jamais le score brut domicile-extérieur), xG, possession, tirs.
create or replace view gold.dm_matchs with (security_invoker = true) as
select m.team_id, c.club, m.season, m.match_id, (m.played_at at time zone 'Europe/Paris')::date as jour,
       case m.comp when 'L' then 'Ligue' when 'C' then 'Coupe' when 'F' then 'Amical' else m.comp end as compet,
       m.opponent, case when m.is_home then 'D' else 'E' end as lieu, m.gf, m.ga, m.my_result,
       m.xgf, m.xga, round(m.xgf - m.xga, 2) as xg_diff, m.xpts, m.poss_pct, m.formation,
       (select count(*) from silver.dm_shots x where x.match_id = m.match_id and x.team_id = m.team_id and x.ours) as tirs_pour,
       (select count(*) from silver.dm_shots x where x.match_id = m.match_id and x.team_id = m.team_id and not x.ours) as tirs_contre,
       m.counters, m.counters_opp, m.corners_for, m.corners_against, m.fouls_for, m.fouls_against,
       m.strength->'us' as force_nous, m.strength->'them' as force_eux
from silver.dm_matches m join silver.dm_clubs c using (team_id);

-- 4. Bilan de saison par compétition et par formation (toute la saison, jamais un match seul).
create or replace view gold.dm_saison_bilan with (security_invoker = true) as
select team_id, club, compet, formation, count(*) as j,
       count(*) filter (where my_result = 'W') as v, count(*) filter (where my_result = 'D') as n,
       count(*) filter (where my_result = 'L') as d, sum(gf) as bp, sum(ga) as bc,
       round(avg(xgf), 2) as xg_pour_moy, round(avg(xga), 2) as xg_contre_moy, round(sum(xpts), 1) as xpts,
       round(avg(poss_pct), 1) as poss_moy, round(avg(tirs_pour), 1) as tirs_pour_moy, round(avg(tirs_contre), 1) as tirs_contre_moy
from gold.dm_matchs
group by grouping sets ((team_id, club, compet, formation), (team_id, club, compet), (team_id, club))
order by team_id, compet nulls first, formation nulls first;

-- 5. D'où viennent les tirs (pour / contre) : origine de l'action, dans ou hors surface, buts, xG.
create or replace view gold.dm_tirs_profil with (security_invoker = true) as
select s.team_id, c.club, case when s.ours then 'pour' else 'contre' end as camp,
       coalesce(s.source, s.sequence) as origine, count(*) as tirs,
       count(*) filter (where s.in_box) as dans_surface, count(*) filter (where s.kind = 'header') as tetes,
       count(*) filter (where s.outcome = 'goal') as buts, round(sum(s.xg), 2) as xg,
       round(100.0 * count(*) filter (where s.outcome = 'goal') / nullif(count(*), 0), 1) as conversion_pct
from silver.dm_shots s join silver.dm_clubs c using (team_id)
group by s.team_id, c.club, s.ours, coalesce(s.source, s.sequence)
order by s.team_id, camp desc, tirs desc;

-- 6. Finances : argent, flux du jour, marge salariale, capacité d'investissement.
-- capacite_invest = argent disponible (le flux quotidien est positif) ; marge_salaire = plafond − salaires engagés (par jour).
create or replace view gold.dm_finances_bilan with (security_invoker = true) as
select f.team_id, c.club, f.captured_at, f.money, f.daily_total as flux_jour_estime, f.daily_turnover as flux_jour_hors_stade,
       f.salaries_now, f.salaries_committed, f.salary_cap, f.salary_cap - f.salaries_committed as marge_salaire_jour,
       f.expectation_rank, f.expectation_pct, f.broadcasting, f.sponsorship, f.merchandise, f.brand, f.subsidy,
       f.maintenance, f.youth_school, f.stadium_daily,
       greatest(f.money, 0) as capacite_invest,
       x.facilities_level, x.upgrade_at, x.current_value as facilities_value, x.daily_change as facilities_daily_change,
       x.reputation, x.stadium_capacity
from silver.dm_finances f join silver.dm_clubs c using (team_id)
left join silver.dm_facilities x using (team_id);

-- 7. Entraînement : progression par joueur (compétences gagnées/perdues, variations), groupe et entraînement choisi.
create or replace view gold.dm_entrainement with (security_invoker = true) as
select t.team_id, c.club, t.grp_name as groupe, t.group_training as entrainement_groupe, t.name, t.pos, t.age,
       t.intensity, t.pot, t.tr, t.mentor, t.gained, t.lost, coalesce(t.gained, 0) + coalesce(t.lost, 0) as solde,
       t.deltas, t.price_change, t.value,
       case when coalesce(t.gained, 0) + coalesce(t.lost, 0) < 0 then 'régresse'
            when coalesce(t.gained, 0) = 0 then 'stagne' else 'progresse' end as tendance
from silver.dm_training t join silver.dm_clubs c using (team_id)
order by t.team_id, solde desc;

-- 8. Base de prix des transferts conclus : par niveau (tier) et tranche d'âge.
create or replace view gold.dm_prix_reference with (security_invoker = true) as
select tier,
       case when age <= 19 then '≤19' when age <= 23 then '20-23' when age <= 27 then '24-27' when age <= 30 then '28-30' else '31+' end as ages,
       count(*) as n,
       percentile_cont(0.25) within group (order by price) as p25,
       percentile_cont(0.5) within group (order by price) as mediane,
       percentile_cont(0.75) within group (order by price) as p75,
       round(avg(salary)) as salaire_moy
from silver.dm_transfers
where price > 0 and status not in ('School')
group by 1, 2
order by 1, 2;

-- 9. Marché : chaque joueur à vendre, compétences au milieu de la fourchette vue par nos scouts, comparé au meilleur
-- joueur de notre effectif au même poste (moyenne des 16 compétences). gain = écart de moyenne.
create or replace view gold.dm_marche_cibles with (security_invoker = true) as
with m as (
  select mk.*, (select round(avg((silver.dm_n(split_part(v, '-', 1)) + silver.dm_n(split_part(v, '-', 2))) / 2.0), 1)
                from jsonb_each_text(mk.skill_ranges) e(k, v) where v is not null) as moy16_mid,
         left(regexp_replace(mk.pos, '[^A-Z]', '', 'g'), 1) as ligne_code
  from silver.dm_market mk
), nous as (
  select team_id, left(pos, 1) as ligne_code, max(moy16) as meilleur, avg(moy16) as moyenne
  from gold.dm_effectif group by team_id, left(pos, 1)
)
select c.team_id, c.club, m.name, m.team as vendeur, m.pos, m.age, m.tier, m.price, m.salary, m.decision,
       m.avg_min, m.avg_max, m.moy16_mid, round(n.meilleur, 1) as notre_meilleur, round(n.moyenne, 1) as notre_moyenne,
       round(m.moy16_mid - n.moyenne, 1) as gain_vs_moyenne
from m cross join silver.dm_clubs c
left join nous n on n.team_id = c.team_id and n.ligne_code = m.ligne_code
where exists (select 1 from gold.dm_effectif e where e.team_id = c.team_id)
order by c.team_id, gain_vs_moyenne desc nulls last;

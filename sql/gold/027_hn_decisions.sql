-- Hockey Nation : vues de décision (2026-10-29, demande de l'utilisateur : « stocke ça dans une gold, qu'on requête vite »).
-- hn_potential() + hn_player_potential (classification de tous nos joueurs), hn_scout_priority (scouts à embaucher),
-- hn_coach_options (meilleur remplaçant du marché par poste de coach), hn_buyout_calc (rachat ou échange : effet sur le plafond).

-- Potentiel d'un joueur (skill hockeynation-potentiel-joueurs, règle [U] du 2026-10-25 calée sur Kabát 68 → 73 / 90).
-- skills = [{id, lvl, max}], talents = {strongest: [a, b], weakest: c}. Un point de compétence = un point de note.
create or replace function gold.hn_potential(skills jsonb, talents jsonb, rating int, out pot_min int, out pot_max int)
language sql immutable as $$
  with s as (
    select x->>'id' as id, (x->>'lvl')::int as lvl, coalesce((x->>'max')::bool, false) as mx,
           (talents->'strongest') ? (x->>'id') as strong, talents->>'weakest' = x->>'id' as weak
    from jsonb_array_elements(coalesce(skills, '[]'::jsonb)) x
  ), p as (
    select
      -- C : plafond fort = plus bas des deux talents forts (10 s'ils ne sont pas plafonnés)
      coalesce((select min(case when mx then lvl else 10 end) from s where strong), 10) as c,
      -- M : plafond faible = niveau du talent faible (+1 s'il n'est pas plafonné)
      coalesce((select case when mx then lvl else lvl + 1 end from s where weak), 0) as m
  ), lv as (
    select s.*,
           case when s.mx then s.lvl when s.weak then s.lvl + 1 when s.strong then s.lvl else greatest(s.lvl, p.m) end as lvl_min,
           case when s.mx then s.lvl when s.weak then null else greatest(s.lvl, p.c) end as lvl_max_other
    from s, p
  ), w as (
    select greatest(lv.lvl, coalesce((select min(o.lvl_max_other) from lv o where not o.weak), 10) - 1) as weak_max
    from lv where lv.weak and not lv.mx
  )
  select rating + coalesce(sum(lvl_min - lvl), 0)::int,
         rating + coalesce(sum(coalesce(lvl_max_other, (select weak_max from w), lvl) - lvl), 0)::int
  from lv
$$;

-- Classification de tous nos joueurs (PRO, FRM, U21, U17) : talents contre poste + potentiel + verdict + futur.
-- Verdict : Fort ≥ 74 de minimum, Solide 68-73, Moyen 58-67, Nul < 58 ; ↑ si maximum ≥ minimum + 15 et 23 ans ou moins.
-- Futur (hypothèse) : PRO = min ≥ 64 ou (≤ 23 ans, min ≥ 55, max ≥ 80) ; FRM = min ≥ 52 ou (≤ 23 ans, max ≥ 75) ; sinon VIRER.
create or replace view gold.hn_player_potential with (security_invoker = true) as
with last as (select distinct on (player_id) * from silver.hn_player_snapshots order by player_id, day desc, captured_at desc),
p as (
  select l.team_level, l.name, l.main_position as poste, l.age, l.rating, l.endu, f.verdict as fit,
         l.talent_strongest, l.talent_weakest, l.special_skills, (gold.hn_potential(l.skills, l.talents, l.rating)).*,
         l.player_id, l.day as as_of
  from (select *, silver.hn_skill(skills, 'END') as endu from last) l
  left join gold.hn_player_fit f on f.player_id = l.player_id and f.is_main
  where l.team_level in ('PRO', 'FRM', 'U21', 'U17')
)
select team_level, name, poste, age, rating, pot_min, pot_max,
       case when pot_min >= 74 then 'Fort' when pot_min >= 68 then 'Solide' when pot_min >= 58 then 'Moyen' else 'Nul' end
         || case when pot_max >= pot_min + 15 and age <= 23 then ' ↑' else '' end as classe,
       case when pot_min >= 64 or (age <= 23 and pot_min >= 55 and pot_max >= 80) then 'PRO'
            when pot_min >= 52 or (age <= 23 and pot_max >= 75) then 'FRM' else 'VIRER' end as futur,
       fit, talent_strongest, talent_weakest, endu,
       (select string_agg(x->>'id', ', ') from jsonb_array_elements(coalesce(special_skills, '[]'::jsonb)) x) as speciales,
       player_id, as_of
from p;

-- Scouts à embaucher : candidats du jour classés par joueurs NON repérés de notre classe de draft (notre ligue, saison de la draft)
-- au même poste et de la même nation, en ne comptant que ce que nos scouts actuels ne couvrent pas déjà (poste ET nation).
-- Les gardiens sont exclus tant que la limite de draft G = 0 (pré-instructions du 2026-10-25).
create or replace view gold.hn_scout_priority with (security_invoker = true) as
with lg as (select league_id from gold.hn_draft_board where from_my_u17 group by league_id order by count(*) desc limit 1),
cls as (
  select b.main_position as pos, n.name as nation, b.scouted_times
  from gold.hn_draft_board b
  join silver.hn_draft_class d on d.name = b.name and d.draft_rank = b.draft_rank
  left join silver.hn_nations n on n.nation_id = d.nation_id
  where b.league_id = (select league_id from lg) and b.season = (select max(season) from gold.hn_draft_board)
), mine as (select preferred_position as pos, nation from silver.hn_scouts where day = (select max(day) from silver.hn_scouts)),
apps as (
  select x->'scout'->>'firstname' || ' ' || (x->'scout'->>'lastname') as scout, (x->'scout'->>'age')::int as age,
         x->'scout'->>'position' as pos, n.name as nation
  from (select body from silver.hn_api where route = '/office/scout-applications' order by captured_at desc limit 1) a,
       jsonb_array_elements(a.body->'applications') x
  left join silver.hn_nations n on n.nation_id = (x->'scout'->>'nationId')::uuid
)
select * from (
select a.scout, a.age, a.pos as poste, a.nation,
       case when a.pos in (select pos from mine) then 0 else (select count(*) from cls where cls.pos = a.pos and cls.scouted_times = 0) end as poste_non_couvert,
       case when a.nation in (select nation from mine) then 0 else (select count(*) from cls where cls.nation = a.nation and cls.scouted_times = 0) end as nation_non_couverte,
       case when a.pos = 'G' then 'non : limite de draft G = 0'
            when a.pos in (select pos from mine) and a.nation in (select nation from mine) then 'non : déjà couvert'
            else 'oui' end as embaucher,
       (select num_scouts || ' / ' || max_scouts || ', budget restant ' || budget_left from silver.hn_scouting_budget order by day desc limit 1) as etat_scouts
from apps a) t
order by (embaucher = 'oui') desc, poste_non_couvert + nation_non_couverte desc, age;

-- Coachs : pour chaque coach en poste (dernier export), le meilleur coach libre du marché du jour qui augmente la somme de match
-- (OFP+DFP+BAT+PP+PK ; le head compte double [G:Coaches]). Plafonds de note : U17 54, U21 69 [G:Coaches]. Retraite à 65 ans.
create or replace view gold.hn_coach_options with (security_invoker = true) as
with staff as (
  select k.key as team_level, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age,
         coalesce((c->'job'->>'head')::bool, false) as head, (c->>'rating')::int as rating,
         silver.hn_skill(c->'skills','OFP') + silver.hn_skill(c->'skills','DFP') + silver.hn_skill(c->'skills','BAT')
           + silver.hn_skill(c->'skills','PP') + silver.hn_skill(c->'skills','PK') as match_sum
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
), market as (
  select name, age, rating, ofp, dfp, bat, pp, pk, ofp + dfp + bat + pp + pk as match_sum
  from silver.hn_free_coaches where day = (select max(day) from silver.hn_free_coaches) and coalesce(can_offer, true)
)
select s.team_level, s.head, s.coach, s.age, s.match_sum,
       b.name as meilleur_candidat, b.age as age_candidat, b.match_sum as somme_candidat,
       b.ofp || '-' || b.dfp || '-' || b.bat || '-' || b.pp || '-' || b.pk as ofp_dfp_bat_pp_pk,
       (b.match_sum - s.match_sum) * case when s.head then 2 else 1 end as gain_equipe,
       65 - s.age as saisons_avant_retraite
from staff s
left join lateral (
  select m.* from market m
  where m.match_sum > s.match_sum
    and (s.team_level <> 'U17' or m.rating <= 54) and (s.team_level <> 'U21' or m.rating <= 69)
    and m.age < 65
  order by m.match_sum desc, m.age limit 1
) b on true
order by s.team_level, s.head desc, gain_equipe desc nulls last;

-- Rachat ou échange : effet sur le plafond de la saison en cours pour chaque joueur PRO.
-- Rachat [G:Finances] : pénalité = ½ du salaire restant, étalée sur les saisons restantes → soulage ½ salaire par saison.
-- Interdit pour un agent libre signé cette saison (liste : signings-tracker) et sous 2 gardiens (sauf plafond dépassé).
create or replace view gold.hn_buyout_calc with (security_invoker = true) as
with s as (select max(season) as season from silver.hn_season),
fa as (
  select distinct x->'player'->>'id' as player_id
  from silver.hn_api a, jsonb_array_elements(a.body) x
  where a.route = '/free-agent-center/signings-tracker' and coalesce((x->'team'->>'own')::bool, x->'team'->>'nickname' = 'Cows')
), cap as (select cap_space from silver.hn_cap_now)
select p.name, p.main_position as poste, p.age, p.rating, p.salary, p.contract_to,
       p.contract_to - s.season + 1 as saisons_restantes,
       (p.salary * (p.contract_to - s.season + 1) / 2) as rachat_total,
       p.salary / 2 as rachat_par_saison,
       p.salary / 2 as soulage_rachat, p.salary as soulage_echange,
       (select cap_space from cap) as cap_space_actuel,
       (select cap_space from cap) + p.salary / 2 as cap_space_si_rachat,
       (select cap_space from cap) + p.salary as cap_space_si_echange,
       case when p.player_id::text in (select player_id from fa) then 'non : agent libre signé cette saison'
            when p.main_position = 'G' and (select count(*) from silver.hn_players where team_level = 'PRO' and main_position = 'G') <= 2
                 then 'possible seulement plafond dépassé, il faut un autre gardien'
            else 'oui' end as rachat_possible,
       p.on_trade_block as sur_liste_echange
from silver.hn_players p, s
where p.team_level = 'PRO' and p.salary is not null and not coalesce(p.frm, false)
order by p.salary desc;

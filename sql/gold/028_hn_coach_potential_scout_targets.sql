-- Hockey Nation (2026-10-29, demande de l'utilisateur) : potentiel des coachs, joueurs à repérer par scout, coachs non remplaçables,
-- potentiel des joueurs limité aux rosters actuels. Remplace les définitions de gold.hn_coach_options et gold.hn_player_potential de 027.

-- Potentiel d'un coach : mêmes règles que pour un joueur (plafonds M et C, skill hockeynation-potentiel-joueurs), appliquées aux 5 compétences
-- de match (OFP DFP BAT PP PK). Talents lus dans les drapeaux strongest / weakest des compétences. Un coach dont tout est plafonné n'a
-- plus de marge (min = max : Strobel 33, Graf 29). Pour un coach sans aucun plafond connu le maximum est théorique (jusqu'à 50).
create or replace function gold.hn_coach_pot(skills jsonb)
returns table(id text, lvl int, lvl_min int, lvl_max int)
language sql immutable as $$
  with s as (
    select x->>'id' as id, (x->>'lvl')::int as lvl, coalesce((x->>'max')::bool, false) as mx,
           coalesce((x->>'strongest')::int, 0) = 1 as strong, coalesce((x->>'weakest')::int, 0) = 1 as weak
    from jsonb_array_elements(coalesce(skills, '[]'::jsonb)) x
  ), p as (
    select coalesce((select min(case when mx then lvl else 10 end) from s where strong), 10) as c,
           coalesce((select case when mx then lvl else lvl + 1 end from s where weak), 0) as m
  ), lv as (
    select s.*, case when s.mx then s.lvl when s.weak then s.lvl + 1 when s.strong then s.lvl else greatest(s.lvl, p.m) end as lvl_min,
           case when s.mx then s.lvl when s.weak then null else greatest(s.lvl, p.c) end as lvl_max_other
    from s, p
  ), w as (
    select greatest(lv.lvl, coalesce((select min(o.lvl_max_other) from lv o where not o.weak), 10) - 1) as weak_max
    from lv where lv.weak and not lv.mx
  )
  select lv.id, lv.lvl, lv.lvl_min, coalesce(lv.lvl_max_other, (select weak_max from w), lv.lvl) from lv
$$;

create or replace view gold.hn_coach_potential with (security_invoker = true) as
with own as (
  select k.key as team_level, true as en_poste, c as c
  from (select body from silver.hn_api where route = '/club/:id/coaching-staff' order by captured_at desc limit 1) a,
       jsonb_each(a.body->'staff') k, jsonb_array_elements(k.value) c
), mkt as (
  select 'marché'::text as team_level, false as en_poste, c as c
  from (select distinct on (x->>'id') x as c from silver.hn_api a, jsonb_array_elements(a.body) x
        where a.route = '/coach-center/search' and a.captured_at > now() - interval '36 hours'
        order by x->>'id', a.captured_at desc) m
), all_c as (select * from own union all select * from mkt)
select team_level, en_poste, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age, (c->>'xp')::int as xp,
       (c->>'rating')::int as note, coalesce((c->'job'->>'head')::bool, false) as head, (c->'job'->>'from')::int as arrive_saison,
       (select sum(lvl) from gold.hn_coach_pot(c->'skills') where id in ('OFP','DFP','BAT','PP','PK')) as match_sum,
       (select sum(lvl_min) from gold.hn_coach_pot(c->'skills') where id in ('OFP','DFP','BAT','PP','PK')) as match_min,
       (select sum(lvl_max) from gold.hn_coach_pot(c->'skills') where id in ('OFP','DFP','BAT','PP','PK')) as match_max,
       65 - (c->>'age')::int as saisons_avant_retraite,
       (select string_agg(coalesce(x->>'id', '?') || case when (x->>'unlocked')::bool then '' else ' (caché)' end, ', ') from jsonb_array_elements(c->'specialSkills') x) as speciales,
       c->'talents'->>'weakest' as talent_faible, c->'talents'->'strongest' as talents_forts
from all_c;

-- Joueurs de notre classe de draft (ligue de la saison en cours) à faire repérer par chacun de nos scouts embauchés :
-- A = même poste ET même nation (missions les plus courtes), B = même poste, C = même nation. Moins de 3 rapports, rapports croissants puis rang.
create or replace view gold.hn_scout_targets with (security_invoker = true) as
with sc as (select name as scout, preferred_position as pos, nation, head_scout from silver.hn_scouts where day = (select max(day) from silver.hn_scouts)),
cls as (
  select b.draft_rank as rang, b.name as joueur, b.main_position as poste, n.name as nation, b.scouted_times as rapports,
         b.rating as note, b.talent_strongest, b.talent_weakest, b.from_my_u17 as notre_u17
  from gold.hn_draft_board b
  left join silver.hn_draft_class d on d.name = b.name and d.draft_rank = b.draft_rank
  left join silver.hn_nations n on n.nation_id = d.nation_id
  where b.season = (select max(season) from gold.hn_draft_board)
    and b.league_id = (select league_id from gold.hn_draft_board where from_my_u17 group by league_id order by count(*) desc limit 1)
)
select sc.scout, sc.head_scout as chef,
       case when cls.poste = sc.pos and cls.nation = sc.nation then 'A poste + nation'
            when cls.poste = sc.pos then 'B poste' else 'C nation' end as categorie,
       cls.rang, cls.joueur, cls.poste, cls.nation, cls.rapports, cls.note, cls.notre_u17
from sc join cls on cls.poste = sc.pos or cls.nation = sc.nation
where cls.rapports < 3
order by sc.scout, 3, cls.rapports, cls.rang;

-- Options de coachs : un coach arrivé cette saison ne se remplace pas [U, 2026-10-29] (Németh, Gschwend, Fellner, Ahn).
create or replace view gold.hn_coach_options with (security_invoker = true) as
with staff as (
  select k.key as team_level, c->>'firstname' || ' ' || (c->>'lastname') as coach, (c->>'age')::int as age,
         coalesce((c->'job'->>'head')::bool, false) as head, (c->>'rating')::int as rating,
         (c->'job'->>'from')::int as arrive_saison,
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
where s.arrive_saison < (select max(season) from silver.hn_season)
order by s.team_level, s.head desc, gain_equipe desc nulls last;

-- Potentiel de tous nos joueurs : seulement ceux encore dans nos rosters (pas les partis ni les draftés).
create or replace view gold.hn_player_potential with (security_invoker = true) as
with last as (select distinct on (player_id) * from silver.hn_player_snapshots order by player_id, day desc, captured_at desc),
p as (
  select l.team_level, l.name, l.main_position as poste, l.age, l.rating, l.endu, f.verdict as fit,
         l.talent_strongest, l.talent_weakest, l.special_skills, (gold.hn_potential(l.skills, l.talents, l.rating)).*,
         l.player_id, l.day as as_of
  from (select *, silver.hn_skill(skills, 'END') as endu from last) l
  join silver.hn_players cur on cur.player_id = l.player_id and cur.team_level = l.team_level
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

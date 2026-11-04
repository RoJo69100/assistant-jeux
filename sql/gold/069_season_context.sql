-- Refonte v2, étape 2.1 : contexte de saison de chacune de mes équipes, tous jeux (core.standing + core.game_params).
-- Dernier classement connu où mon équipe figure ; toute la ligue de ce relevé sert aux calculs.
-- Paramètres (core.game_params) : rounds_total, points_par_victoire, promo_slots, releg_slots, playoff_slots.
-- Règle du plan : un paramètre non sourcé (absent) → drapeau nul, jamais d'hypothèse silencieuse.
-- Bornes (égalités comptées contre moi, départage inconnu) :
--   max_pts(équipe)   = points + (rounds_total − joués) × points_par_victoire
--   titre_acquis      = mes points > max_pts de toutes les autres
--   elimine_titre     = mon max_pts < points du premier
--   promo_acquise     = nombre d'autres avec max_pts ≥ mes points < promo_slots
--   playoff_acquis    = idem avec playoff_slots
--   maintien_acquis   = nombre d'autres avec max_pts < mes points ≥ releg_slots
--   relegue_acquis    = nombre d'autres avec points > mon max_pts ≥ équipes − releg_slots
--   rien_a_jouer      = maintien acquis et (titre acquis ou perdu) et (montée acquise, impossible ou sans objet)

create or replace view gold.season_context with (security_invoker = true) as
with p as (
  select game,
         max(case when key = 'rounds_total' then value::text::int end)        as rounds_total,
         max(case when key = 'points_par_victoire' then value::text::int end) as ppv,
         max(case when key = 'promo_slots' then value::text::int end)         as promo_slots,
         max(case when key = 'releg_slots' then value::text::int end)         as releg_slots,
         max(case when key = 'playoff_slots' then value::text::int end)       as playoff_slots
  from core.game_params group by game
),
moi as (  -- dernier relevé de chaque équipe à moi
  select distinct on (game, team_id) game, team_id, team_label, season_id, day
  from core.standing where is_mine
  order by game, team_id, day desc
),
ligue as (
  select m.team_id as my_team_id, s.*, p.rounds_total, p.ppv, p.promo_slots, p.releg_slots, p.playoff_slots,
         s.points + (p.rounds_total - s.played) * p.ppv as max_pts,
         count(*) over (partition by m.game, m.team_id) as n_teams,
         max(s.points) over (partition by m.game, m.team_id) as pts_first
  from moi m
  join core.standing s on s.game = m.game and s.season_id = m.season_id and s.day = m.day
  left join p on p.game = m.game
),
me as (select * from ligue where is_mine and team_id = my_team_id),
agg as (
  select me.game, me.my_team_id,
         max(o.max_pts)                                          as max_autres,
         count(*) filter (where o.max_pts >= me.points)          as menaces,
         count(*) filter (where o.max_pts < me.points)           as surement_derriere,
         count(*) filter (where o.points > me.max_pts)           as surement_devant,
         max(o.points) filter (where o.rank = me.n_teams - me.releg_slots + 1) as pts_1er_relegable,
         bool_and(o.points is not null and o.played is not null) as complet
  from me join ligue o on o.game = me.game and o.my_team_id = me.my_team_id and o.team_id <> me.team_id
  group by me.game, me.my_team_id
)
select
  me.game, me.team_id, me.team_label, me.season_id, me.day as as_of,
  me.played                         as round_no,
  me.rounds_total,
  me.rounds_total - me.played       as rounds_left,
  me.n_teams::int                   as n_teams,
  me.rank, me.points,
  me.pts_first - me.points          as gap_to_first,
  me.points - a.pts_1er_relegable   as gap_to_relegation,   -- > 0 : au-dessus de la 1re place relégable
  (me.rounds_total - me.played) * me.ppv as points_restants_max,
  case when a.complet and me.max_pts is not null then me.points > a.max_autres end                       as titre_acquis,
  case when a.complet and me.max_pts is not null then me.max_pts < me.pts_first end                      as elimine_titre,
  case when a.complet and me.max_pts is not null and me.promo_slots is not null then a.menaces < me.promo_slots end   as promo_acquise,
  case when a.complet and me.max_pts is not null and me.promo_slots is not null then a.surement_devant >= me.promo_slots end as promo_impossible,
  case when a.complet and me.max_pts is not null and me.playoff_slots is not null then a.menaces < me.playoff_slots end as playoff_acquis,
  case when a.complet and me.max_pts is not null and me.releg_slots is not null then a.surement_derriere >= me.releg_slots end as maintien_acquis,
  case when a.complet and me.max_pts is not null and me.releg_slots is not null then a.surement_devant >= me.n_teams - me.releg_slots end as relegue_acquis,
  case when a.complet and me.max_pts is not null and me.releg_slots is not null then
         a.surement_derriere >= me.releg_slots
         and (me.points > a.max_autres or me.max_pts < me.pts_first)
         and (me.promo_slots is null or a.menaces < me.promo_slots or a.surement_devant >= me.promo_slots)
  end                                                                                                    as rien_a_jouer,
  concat_ws(', ',
    case when me.rounds_total is null then 'rounds_total' end,
    case when me.ppv is null then 'points_par_victoire' end,
    case when me.releg_slots is null then 'releg_slots' end,
    case when not a.complet then 'points ou matchs joués manquants' end) as parametres_manquants
from me join agg a on a.game = me.game and a.my_team_id = me.my_team_id;

grant select on gold.season_context to assistant_ro;

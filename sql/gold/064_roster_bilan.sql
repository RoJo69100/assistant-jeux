-- Refonte v2, étape 1.4 : bilan d'effectif pour tous les jeux, sur core.player_daily et core.game_params.
-- Une ligne par joueur du dernier relevé de chaque équipe ; totaux d'équipe et seuils répétés sur chaque ligne.
-- Statistiques de match propres à un jeu : restent dans gold.sz_effectif_bilan / gold.ts_effectif_bilan.

insert into core.game_params (game, key, value, source, verified_on) values
  ('basketvibe',   'age_declin', '31', 'basketvibe-entrainement/05-apres-30-ans (toutes les compétences baissent chaque dimanche)', '2026-11-03'),
  ('hockeynation', 'age_declin', '32', 'hockeynation-joueurs/06-age (déclin possible dès 32 ans, compétences plafonnées)', '2026-11-03')
on conflict (game, key) do nothing;

create or replace view gold.roster_bilan with (security_invoker = true) as
with dernier as (
  select game, team_id, max(day) as day
  from core.player_daily
  where day <= (now() at time zone 'Europe/Paris')::date
  group by game, team_id
),
p as (
  select pd.* from core.player_daily pd join dernier d using (game, team_id, day)
),
prm as (
  select game,
         max((value #>> '{}')::int) filter (where key = 'effectif_min') as effectif_min,
         max((value #>> '{}')::int) filter (where key = 'effectif_max') as effectif_max,
         max((value #>> '{}')::int) filter (where key = 'age_declin')   as age_declin
  from core.game_params group by game
)
select p.game, p.team_id, p.club_label, p.day as as_of,
       p.position, rank() over (partition by p.game, p.team_id, p.position order by p.rating desc nulls last) as rang_poste,
       p.player_id, p.name, p.age, p.rating, p.salary, p.injured, p.is_academy,
       coalesce(p.age >= prm.age_declin, false) as en_declin,
       count(*) over w                     as effectif,
       sum(p.salary) over w                as masse_salariale,
       round(avg(p.age) over w, 1)         as age_moyen,
       round(avg(p.rating) over w, 1)      as rating_moyen,
       count(*) filter (where p.injured) over w as blesses,
       prm.effectif_min, prm.effectif_max, prm.age_declin,
       case when count(*) over w < prm.effectif_min then 'sous le minimum'
            when count(*) over w > prm.effectif_max then 'au-dessus du maximum'
            else null end                  as alerte_effectif
from p
left join prm on prm.game = p.game
window w as (partition by p.game, p.team_id);

grant select on gold.roster_bilan to assistant_ro;

-- Refonte v2, étape 1.4 : agenda générique (strangler de gold.bv_agenda, puis des autres jeux).
-- Une seule vue pour tous les jeux : core.fixture + core.market_listing + core.agenda_rule.
-- Heures en Europe/Paris (fuseau_affichage) ; fenêtre aujourd'hui + 6 jours, comme gold.bv_agenda.
-- Écart voulu avec gold.bv_agenda : une règle « avant le coup d'envoi » tombe le jour de l'heure calculée
-- (amical de 00:00 : preset la veille à 23:45, l'ancienne vue le datait du jour du match).
-- 2026-11-03 : déclencheur jour_saison (core.season, Hockey Nation) ; at_time nulle si la règle n'a pas d'heure.
-- 2026-11-04 : Team Soccer (sql/core/010) — soir_min, avant_coup_envoi, fait_cle, trous {quand} {formation},
-- déclencheur ancienne_vue (gold.ts_agenda : académie, amical).

create or replace view gold.agenda with (security_invoker = true) as
with fen as (
  select d::date as day from generate_series(current_date, current_date + 6, interval '1 day') d
),
r as (
  select * from core.agenda_rule where actif
),
fin as (
  select game, team_id, max(day) as last_day from core.fixture where competition_kind = 'ligue' group by 1, 2
),
ev as (
  -- match : heure fixe le jour du match, ou coup d'envoi + décalage ; avant soir_min → la veille à soir_min ;
  -- fait_cle vraie dans extras → priorité et modèle « déjà fait »
  select f.game, f.team_id, r.rule_id,
         case when fait.v then r.priorite_si_fait else r.priority end as priority, r.category,
         case when fait.v then r.modele_si_fait else r.modele end as modele,
         x.at_ts,
         f.round_no::text as round, f.opponent,
         case when f.home then 'domicile' else 'extérieur' end as venue,
         case when coalesce((f.extras ->> 'has_saved_match_tactics')::boolean, false) then ''
              else ' (au dernier export : aucun plan sauvegardé)' end as sans_plan,
         null::text as player, null::text as bids, null::text as price,
         case when x.at_ts::date < f.day then
                case when f.day = x.at_ts::date + 1 then 'Pour demain' else 'Pour ' || to_char(f.day, 'DD/MM') end
              else 'Ce soir' end as quand,
         coalesce(f.extras ->> 'saved_formation', '?') as formation
  from core.fixture f
  join r on r.game = f.game and r.declencheur = 'match' and r.competition_kind = f.competition_kind
  cross join lateral (select case when r.heure is not null then f.day + r.heure
                                  else (f.scheduled_at at time zone 'Europe/Paris') + r.decalage end as t0) t0
  cross join lateral (select case when r.soir_min is not null and t0.t0::time < r.soir_min
                                  then (t0.t0::date - 1) + r.soir_min else t0.t0 end as at_ts) x
  cross join lateral (select r.fait_cle is not null and coalesce((f.extras ->> r.fait_cle)::boolean, false) as v) fait
  where not f.played
    and f.day between current_date and current_date + 6 + case when r.soir_min is not null then 1 else 0 end
    and (r.heure is not null or f.scheduled_at is not null)
    and (not r.avant_coup_envoi or f.scheduled_at > now())
  union all
  -- jour de la semaine
  select r.game, null, r.rule_id, r.priority, r.category, r.modele, fen.day + r.heure,
         null, null, null, null, null, null, null, null, null
  from fen join r on r.declencheur = 'jour_semaine' and r.isodow = extract(isodow from fen.day)
  union all
  -- jour futur sans match du type, jusqu'au lendemain du dernier match de ligue
  select r.game, fin.team_id, r.rule_id, r.priority, r.category, r.modele, fen.day + r.heure,
         null, null, null, null, null, null, null, null, null
  from fen
  join r on r.declencheur = 'jour_sans_match'
  join fin on fin.game = r.game
  where fen.day > current_date
    and fen.day <= fin.last_day + 1
    and not exists (select 1 from core.fixture f
                    where f.game = r.game and f.competition_kind = r.competition_kind and f.day = fen.day)
  union all
  -- fin d'une de mes ventes
  select m.game, m.team_id, r.rule_id, r.priority, r.category, r.modele,
         (m.ends_at at time zone 'Europe/Paris') + r.decalage,
         null, null, null, null, m.name, m.bids::text, m.price::text, null, null
  from core.market_listing m
  join r on r.game = m.game and r.declencheur = 'vente'
  where m.is_mine and m.status like 'live%'
    and (m.ends_at at time zone 'Europe/Paris')::date between current_date and current_date + 6
  union all
  -- dernier match de ligue connu
  select fin.game, fin.team_id, r.rule_id, r.priority, r.category, r.modele, fin.last_day + r.heure,
         null, null, null, null, null, null, null, null, null
  from fin join r on r.game = fin.game and r.declencheur = 'fin_saison'
  where fin.last_day between current_date and current_date + 6
  union all
  -- jour de saison (saison en cours : jour 1 le plus récent)
  select s.game, null, r.rule_id, r.priority, r.category, r.modele,
         (s.day1 + r.jour_saison - 1) + coalesce(r.heure, time '00:00'),
         null, null, null, null, null, null, null, null, null
  from (select distinct on (game) * from core.season order by game, day1 desc) s
  join r on r.game = s.game and r.declencheur = 'jour_saison'
  union all
  -- reprise d'une ancienne vue, par catégorie (Team Soccer : académie et amical, pas encore dans core)
  select r.game, mt.team_id::text, r.rule_id, a.priority, a.category, a.action, a.day::timestamp,
         null, null, null, null, null, null, null, null, null
  from gold.ts_agenda a
  join r on r.game = 'teamsoccer' and r.declencheur = 'ancienne_vue' and r.ancienne_vue = 'gold.ts_agenda'
        and r.category = a.category
  left join silver.ts_my_teams mt on mt.name = a.team
)
select
  ev.game,
  ev.team_id,
  ev.at_ts::date                                         as day,
  (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from ev.at_ts)::int]
    || ' ' || to_char(ev.at_ts, 'DD/MM')                 as day_label,
  case when ar.heure is null and ar.decalage is null then null
       else ev.at_ts::time end                           as at_time,     -- nulle : événement du jour sans heure sourcée
  ev.priority,
  ev.category,
  replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(ev.modele,
    '{quand}', coalesce(ev.quand, '')), '{formation}', coalesce(ev.formation, '')),
    '{round}', coalesce(ev.round, '')), '{opponent}', coalesce(ev.opponent, '')),
    '{venue}', coalesce(ev.venue, '')), '{hhmi}', to_char(ev.at_ts, 'HH24:MI')),
    '{sans_plan}', coalesce(ev.sans_plan, '')), '{player}', coalesce(ev.player, '')),
    '{bids}', coalesce(ev.bids, '')), '{price}', coalesce(ev.price, '')) as action,
  ev.rule_id
from ev
join core.agenda_rule ar on ar.game = ev.game and ar.rule_id = ev.rule_id
where ev.at_ts::date between current_date and current_date + 6
order by ev.game, day, at_time nulls first, ev.priority;

grant select on gold.agenda to assistant_ro;

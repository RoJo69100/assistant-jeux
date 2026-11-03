-- Refonte v2, étape 1.4 : agenda générique (strangler de gold.bv_agenda, puis des autres jeux).
-- Une seule vue pour tous les jeux : core.fixture + core.market_listing + core.agenda_rule.
-- Heures en Europe/Paris (fuseau_affichage) ; fenêtre aujourd'hui + 6 jours, comme gold.bv_agenda.
-- Écart voulu avec gold.bv_agenda : une règle « avant le coup d'envoi » tombe le jour de l'heure calculée
-- (amical de 00:00 : preset la veille à 23:45, l'ancienne vue le datait du jour du match).

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
  -- match : heure fixe le jour du match, ou coup d'envoi + décalage
  select f.game, f.team_id, r.rule_id, r.priority, r.category, r.modele,
         case when r.heure is not null then f.day + r.heure
              else (f.scheduled_at at time zone 'Europe/Paris') + r.decalage end as at_ts,
         f.round_no::text as round, f.opponent,
         case when f.home then 'domicile' else 'extérieur' end as venue,
         case when coalesce((f.extras ->> 'has_saved_match_tactics')::boolean, false) then ''
              else ' (au dernier export : aucun plan sauvegardé)' end as sans_plan,
         null::text as player, null::text as bids, null::text as price
  from core.fixture f
  join r on r.game = f.game and r.declencheur = 'match' and r.competition_kind = f.competition_kind
  where not f.played
    and f.day between current_date and current_date + 6
    and (r.heure is not null or f.scheduled_at is not null)
  union all
  -- jour de la semaine
  select r.game, null, r.rule_id, r.priority, r.category, r.modele, fen.day + r.heure,
         null, null, null, null, null, null, null
  from fen join r on r.declencheur = 'jour_semaine' and r.isodow = extract(isodow from fen.day)
  union all
  -- jour futur sans match du type, jusqu'au lendemain du dernier match de ligue
  select r.game, fin.team_id, r.rule_id, r.priority, r.category, r.modele, fen.day + r.heure,
         null, null, null, null, null, null, null
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
         null, null, null, null, m.name, m.bids::text, m.price::text
  from core.market_listing m
  join r on r.game = m.game and r.declencheur = 'vente'
  where m.is_mine and m.status like 'live%'
    and (m.ends_at at time zone 'Europe/Paris')::date between current_date and current_date + 6
  union all
  -- dernier match de ligue connu
  select fin.game, fin.team_id, r.rule_id, r.priority, r.category, r.modele, fin.last_day + r.heure,
         null, null, null, null, null, null, null
  from fin join r on r.game = fin.game and r.declencheur = 'fin_saison'
  where fin.last_day between current_date and current_date + 6
)
select
  ev.game,
  ev.team_id,
  ev.at_ts::date                                         as day,
  (array['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche'])[extract(isodow from ev.at_ts)::int]
    || ' ' || to_char(ev.at_ts, 'DD/MM')                 as day_label,
  ev.at_ts::time                                         as at_time,
  ev.priority,
  ev.category,
  replace(replace(replace(replace(replace(replace(replace(replace(ev.modele,
    '{round}', coalesce(ev.round, '')), '{opponent}', coalesce(ev.opponent, '')),
    '{venue}', coalesce(ev.venue, '')), '{hhmi}', to_char(ev.at_ts, 'HH24:MI')),
    '{sans_plan}', coalesce(ev.sans_plan, '')), '{player}', coalesce(ev.player, '')),
    '{bids}', coalesce(ev.bids, '')), '{price}', coalesce(ev.price, '')) as action,
  ev.rule_id
from ev
where ev.at_ts::date between current_date and current_date + 6
order by ev.game, day, at_time, ev.priority;

grant select on gold.agenda to assistant_ro;

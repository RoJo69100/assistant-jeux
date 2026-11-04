-- Refonte v2, étape 1.4 : alertes du jour pour tous les jeux, depuis core.alert_rule (strangler de gold.<jeu>_daily_alerts).
-- Effectif = dernier relevé de chaque équipe ; valeurs remises dans l'échelle du jeu (core.game_params echelle_*).
-- Les domaines « ancienne_vue » sont repris tels quels de l'ancienne vue du jeu, en attendant leur portage.
-- Parité : pipelines/alertes_parite.py.
-- 2026-11-04 : Team Soccer, Six Zero League, Hardwood (anciennes vues) et Derby Manager ; colonne club en fin de vue
-- (club_label de core.player_daily, ou équipe de l'ancienne vue : Team Soccer a deux clubs).

create or replace view gold.daily_alerts with (security_invoker = true) as
with r as (
  select * from core.alert_rule where actif
),
ech as (
  select game, key, (value ->> 'min')::numeric as lo, (value ->> 'max')::numeric as hi
  from core.game_params where key in ('echelle_fatigue', 'echelle_form')
),
dernier as (
  select game, team_id, max(day) as day from core.player_daily group by 1, 2
),
roster as (
  select p.*,
         ef.lo + p.fatigue * (ef.hi - ef.lo) as fatigue_jeu,
         fo.lo + p.form * (fo.hi - fo.lo)    as form_jeu
  from core.player_daily p
  join dernier d using (game, team_id, day)
  left join ech ef on ef.game = p.game and ef.key = 'echelle_fatigue'
  left join ech fo on fo.game = p.game and fo.key = 'echelle_form'
),
al as (
  select p.game, p.team_id, r.rule_id, r.priority, r.domaine, r.modele,
         jsonb_build_object('name', p.name,
           'retour', ', retour le ' || to_char((p.extras ->> 'injury_return_on')::date, 'DD/MM')) as v
  from roster p join r on r.game = p.game and r.declencheur = 'joueur_blesse'
  where p.injured
  union all
  select p.game, p.team_id, r.rule_id, r.priority, r.domaine, r.modele,
         jsonb_build_object('name', p.name, 'valeur', round(x.val))
  from roster p
  join r on r.game = p.game and r.declencheur in ('joueur_fatigue', 'joueur_forme')
  cross join lateral (select case r.declencheur when 'joueur_fatigue' then p.fatigue_jeu else p.form_jeu end as val) x
  where (r.seuil_bas is null or x.val > r.seuil_bas) and (r.seuil_haut is null or x.val <= r.seuil_haut)
  union all
  select d.game, d.team_id, r.rule_id, r.priority, r.domaine, r.modele, jsonb_build_object('n', d.n)
  from (select p.game, p.team_id, count(*) as n
        from roster p
        where not p.injured
          and not exists (select 1 from core.market_listing m
                          where m.game = p.game and m.player_id = p.player_id and m.is_mine
                            and m.status like 'live%' and m.ends_at > now())
        group by 1, 2) d
  join r on r.game = d.game and r.declencheur = 'effectif_dispo'
  where d.n <= r.seuil_haut
  union all
  select e.game, e.team_id, r.rule_id, r.priority, r.domaine, r.modele,
         jsonb_build_object('ecran', e.ecran, 'statut', e.statut, 'age_h', e.age_h)
  from gold.exports_state e join r on r.game = e.game and r.declencheur = 'export_perime'
  where e.statut <> '🟩 à jour'
  union all
  select f.game, f.team_id, r.rule_id, r.priority, r.domaine, r.modele,
         jsonb_build_object('kind', f.competition_kind, 'round', 'J' || f.round_no || ' ',
                            'day', to_char(f.day, 'DD/MM'), 'opponent', f.opponent)
  from core.fixture f
  join r on r.game = f.game and r.declencheur = 'match_sans_resultat' and r.competition_kind = f.competition_kind
  where f.my_result is null and f.day < current_date and f.day >= current_date - r.seuil_haut::int
  union all
  select f.game, f.team_id, r.rule_id, r.priority, r.domaine, r.modele,
         jsonb_build_object('day', to_char(f.day, 'DD/MM'), 'kind', f.competition_kind, 'result', f.my_result,
                            'score', f.my_score || '-' || f.opp_score, 'opponent', f.opponent)
  from (select distinct on (game) * from core.fixture where my_result is not null
        order by game, day desc, scheduled_at desc nulls last) f
  join r on r.game = f.game and r.declencheur = 'dernier_match'
),
anciennes as (
  select 'basketvibe'::text as game, a.priority as prio, a.category as domaine, a.alert as alerte, null::text as club
  from gold.bv_daily_alerts a
  union all
  select 'hockeynation', a.prio, a.domaine, a.alerte, null from gold.hn_daily_alerts a
  union all
  select 'teamsoccer', a.priority, a.category, a.alert, a.team from gold.ts_daily_alerts a
  union all
  select 'sixzeroleague', a.priority, a.category, a.alert, null from gold.sz_daily_alerts a
  union all
  select 'hardwood', a.prio, a.categorie, a.alerte, null from gold.hw_daily_alerts a
),
equipes as (
  select distinct on (game, team_id) game, team_id, club_label
  from core.player_daily order by game, team_id, day desc
)
select al.game, al.team_id, al.priority as prio,
       (array['🟥 URGENT', '🟧 IMPORTANT', '🟩 SUIVI'])[al.priority] as niveau,
       al.domaine, core.remplir(al.modele, al.v) as alerte, al.rule_id,
       q.club_label as club
from al
left join equipes q on q.game = al.game and q.team_id = al.team_id
union all
select a.game, null, a.prio, (array['🟥 URGENT', '🟧 IMPORTANT', '🟩 SUIVI'])[a.prio], a.domaine, a.alerte, r.rule_id, a.club
from anciennes a join r on r.game = a.game and r.declencheur = 'ancienne_vue' and r.domaine = a.domaine;

grant select on gold.daily_alerts to assistant_ro;

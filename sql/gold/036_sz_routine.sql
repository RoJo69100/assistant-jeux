-- Six Zero League : routine quotidienne en SQL, sans agent (2026-10-30, mise à niveau sur le modèle Hockey Nation, 026_hn_routine.sql).
-- sz_today (étape de saison du jour + prochaine), sz_exports_state (fraîcheur des exports), sz_saisie_tactique (tactique par défaut
-- enregistrée, poste par poste, avec contrôle de chaque case et meilleure option naturelle).

-- Jour de saison : étape en cours (ou dernière passée) et prochaine étape, d'après /seasons/current.
create or replace view gold.sz_today with (security_invoker = true) as
with s as (select * from silver.sz_schedule),
cur as (select * from s where kickoff_paris::date <= (now() at time zone 'Europe/Paris')::date order by step_index desc limit 1),
nxt as (select * from s where status <> 'complete' and kickoff_paris > (now() at time zone 'Europe/Paris') order by step_index limit 1),
nxt_match as (select * from s where i_play and status <> 'complete' order by step_index limit 1)
select (now() at time zone 'Europe/Paris')::date as today,
       cur.label || ' (' || cur.competition || ', ' || to_char(cur.kickoff_paris, 'DD/MM HH24:MI') || ', ' || cur.status || ')' as etape_du_jour,
       nxt.label || ' (' || to_char(nxt.kickoff_paris, 'DD/MM HH24:MI') || ')' as prochaine_etape,
       case when nxt_match.step_index is null then 'aucun match programmé'
            else case when nxt_match.competition = 'league' then 'J' else 'Coupe T' end || nxt_match.round || ' contre ' || coalesce(nxt_match.opponent, '?')
                 || ' (' || coalesce(nxt_match.venue, '?') || ', ' || to_char(nxt_match.kickoff_paris, 'DD/MM HH24:MI') || ')' end as prochain_match,
       cur.competition in ('off_season', 'handover') as intersaison,
       (select max(captured_at) at time zone 'Europe/Paris' from s) as calendrier_releve_paris
from (select 1) x left join cur on true left join nxt on true left join nxt_match on true;

-- Fraîcheur des exports utiles à la décision (max_age_h : au-delà, l'export est à refaire).
create or replace view gold.sz_exports_state with (security_invoker = true) as
with need(ordre, ecran, endpoint_re, max_age_h, pour_quoi) as (values
  (1, 'Équipe > Players', '^/teams/mine/players$', 24, 'effectif, blessés, compétences'),
  (2, 'Équipe > Tactique', '^/teams/mine/tactics/default$', 24, 'sept et remplaçants enregistrés'),
  (3, 'Transferts (marché)', '^/transfers$', 12, 'cibles, enchères en cours'),
  (4, 'Mes transferts', '^/teams/mine/transfers$', 24, 'mes ventes et enchères'),
  (5, 'Finances', '^/finances/mine$', 24, 'solde, sponsor, prévision'),
  (6, 'Entraînement (plan)', '^/teams/mine/training$', 48, 'intensité et focus enregistrés'),
  (7, 'Entraînement (rapport)', '^/teams/mine/training/report$', 48, 'progression du cycle'),
  (8, 'Formation de rôle', '^/teams/mine/role-training$', 72, '2e rôle en cours'),
  (9, 'Académie U18', '^/teams/mine/u18$', 72, 'prospects'),
  (10, 'Infrastructures', '^/infrastructure/mine$', 72, 'niveaux, coûts'),
  (11, 'Calendrier (League)', '^/seasons/current$', 24, 'étapes de la saison'),
  (12, 'Ma compétition', '^/seasons/current/my-competition$', 24, 'classement, résultats'),
  (13, 'Coupe', '^/cups/current$', 48, 'tableau de coupe'),
  (14, 'Chat', '^/chat/messages$', 72, 'veille (développeur, conseils)')
)
select n.ordre, n.ecran, n.pour_quoi,
       max(a.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(a.captured_at)) / 3600) as age_h,
       case when max(a.captured_at) is null then '🟥 jamais'
            when now() - max(a.captured_at) > make_interval(hours => n.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from need n left join silver.sz_api a on a.endpoint ~ n.endpoint_re
group by n.ordre, n.ecran, n.pour_quoi, n.max_age_h
order by n.ordre;

-- Tactique par défaut enregistrée (dernier export), dans l'ordre de l'écran : contrôle de chaque case
-- (joueur parti, blessé/suspendu, hors poste) et meilleure option sans pénalité disponible (gold.sz_lineup_natural).
create or replace view gold.sz_saisie_tactique with (security_invoker = true) as
with slots(slot, ord) as (values ('GK',1), ('CB',2), ('LB',3), ('RB',4), ('LW',5), ('RW',6), ('P',7)),
best as (select slot, name, rating from gold.sz_lineup_natural where rank_in_slot = 1 and not unavailable)
select t.kind as role_tactique, t.slot as poste, (case when t.kind = 'titulaire' then 0 else 10 end) + s.ord as ordre,
       coalesce(p.name, '⚠ parti (' || left(t.player_id::text, 8) || ')') as joueur,
       p.role as role_joueur, (p.role_overalls->>t.slot)::int as note_au_poste,
       case when p.player_id is null then '🟥 absent de l''effectif'
            when p.injured then '🟥 blessé'
            when p.suspended then '🟥 suspendu'
            when not (p.role = t.slot or coalesce(p.secondary_roles ? t.slot, false)) then '🟧 hors poste'
            else 'ok' end as controle,
       b.name as meilleur_naturel, b.rating as note_meilleur,
       case when b.name is not null and b.name <> coalesce(p.name, '') and t.kind = 'titulaire'
                 and b.rating > coalesce((p.role_overalls->>t.slot)::int, 0) then '🟧 ' || b.name || ' meilleur (+' || (b.rating - coalesce((p.role_overalls->>t.slot)::int, 0)) || ')'
            else '' end as suggestion,
       t.attack_formation, t.defense_formation, t.day as enregistre_le
from silver.sz_tactics t
join slots s on s.slot = t.slot
left join silver.sz_players p on p.player_id = t.player_id
left join best b on b.slot = t.slot
order by ordre;

-- Gold, tous jeux : calendrier maître (2026-11-02, rétro du soir : « vues d'agenda qui affichent leur fraîcheur »,
-- règle apprise 69 : contrôler le calendrier lui-même avant tout plan du jour).
--
-- gold.calendrier_fraicheur : une ligne par jeu et par équipe — date de la dernière capture du calendrier, âge en heures,
--   et `perime` = capture de plus de 12 h OU un match prévu dont le coup d'envoi est passé depuis la capture
--   (le calendrier ne sait pas encore qu'il a été joué). Périmé = première action « exporte le calendrier ».
-- gold.calendrier_maitre : mes matchs non joués dont le coup d'envoi tombe entre maintenant et la fin de demain (Paris) :
--   un match de demain se prépare aujourd'hui (horizon « aujourd'hui seulement »). Jointe à la fraîcheur.
--
-- Sources (colonnes relues dans les fichiers de définition, règle 72) :
--   basketvibe    silver.bv_fixtures (ligue, match_day ; 20:00 Paris, verrouillage 19:45 — commentaire de 008_bv_agenda)
--                 + dernière capture /teams/<id>/friendlies (kickoff_at, verrouillage 15 min avant).
--                 Coupes non incluses : la liste /teams/<id>/cup-fixtures n'est pas lue en silver.
--   sixzeroleague silver.sz_schedule (scheduled_at, status <> 'complete', i_play).
--   teamsoccer    gold.ts_upcoming (deux clubs, limite = coup d'envoi − 2 h, lineup_saved) ; fraîcheur = silver.ts_matches.last_seen.
--   hockeynation  silver.hn_games (scheduled_at, my_result null, équipe = team_level).
--   hardwood      silver.hw_schedule, heure comme gold.hw_today (jour réel + 09:00 America/Los_Angeles).
--   derbymanager  silver.dm_fixtures : date et heure en texte, format non vérifié en base (Supabase non lu à la conception) :
--                 rendues brutes (date_texte), coup d'envoi null, toujours classées « à vérifier ». Prochain = plus petit `ord`
--                 sans résultat (ordre de la page supposé chronologique : à contrôler au premier export).

create or replace view gold.calendrier_fraicheur with (security_invoker = true) as
with cap(jeu, equipe, capture) as (
  select 'basketvibe', 'BasketVibe', max(a.captured_at)
  from silver.bv_api a where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$'
  union all
  select 'sixzeroleague', 'Six Zero League', max(captured_at) from silver.sz_schedule
  union all
  select 'teamsoccer', mt.name, max(m.last_seen)
  from silver.ts_matches m join silver.ts_my_teams mt on mt.team_id = m.my_team_id group by mt.name
  union all
  select 'hockeynation', 'Hockey Nation', max(captured_at) from silver.hn_games
  union all
  select 'hardwood', 'Hardwood', max(captured_at) from silver.hw_schedule
  union all
  select 'derbymanager', c.club, max(f.captured_at)
  from silver.dm_fixtures f join silver.dm_clubs c on c.team_id = f.team_id group by c.club
),
passes(jeu, equipe, kickoff) as (   -- matchs prévus dont l'heure est passée : le calendrier ne le sait pas encore
  select 'basketvibe', 'BasketVibe', ((f.match_day + time '20:00') at time zone 'Europe/Paris')
  from silver.bv_fixtures f where f.is_mine and f.status = 'scheduled'
  union all
  select 'sixzeroleague', 'Six Zero League', s.scheduled_at from silver.sz_schedule s where s.i_play and s.status <> 'complete'
  union all
  select 'teamsoccer', mt.name, m.match_date
  from silver.ts_matches m join silver.ts_my_teams mt on mt.team_id = m.my_team_id where m.status = 'scheduled'
  union all
  select 'hockeynation', 'Hockey Nation', g.scheduled_at
  from silver.hn_games g where (g.home_is_mine or g.away_is_mine) and g.my_result is null
)
select c.jeu, c.equipe,
       c.capture at time zone 'Europe/Paris' as capture_paris,
       round(extract(epoch from now() - c.capture) / 3600.0, 1) as age_h,
       c.capture is null
         or c.capture < now() - interval '12 hours'
         or exists (select 1 from passes p where p.jeu = c.jeu and p.equipe = c.equipe
                    and p.kickoff > c.capture and p.kickoff < now()) as perime
from cap c;

create or replace view gold.calendrier_maitre with (security_invoker = true) as
with fin as (select ((((now() at time zone 'Europe/Paris')::date + 2)::timestamp) at time zone 'Europe/Paris') as limite),
bv_fr as (
  select (x->>'kickoff_at')::timestamptz as kickoff,
         case when x->>'home_team_name' = me_name.name then x->>'away_team_name' else x->>'home_team_name' end as opponent,
         (x->>'has_saved_match_tactics')::bool as saisie
  from (select body from silver.bv_api where endpoint ~ '^/teams/[0-9a-f-]{36}/friendlies$' order by captured_at desc limit 1) a
  cross join lateral jsonb_array_elements(a.body->'friendlies') x
  cross join (select coalesce((select home_team from silver.bv_matches where my_side = 'home' limit 1), '') as name) me_name
  where x->>'status' = 'scheduled'
),
hw as (
  select *, to_date(substring(sim_time from '^\w+ (\w+ \d+)') || ' ' || extract(year from captured_at), 'Mon DD YYYY') as real_day
  from silver.hw_schedule where not_played
),
dm as (
  select distinct on (f.team_id) f.*, c.club
  from silver.dm_fixtures f join silver.dm_clubs c on c.team_id = f.team_id
  where f.my_result is null
  order by f.team_id, f.ord
),
m(jeu, equipe, competition, adversaire, lieu, kickoff, limite_saisie, saisie_faite, date_texte) as (
  select 'basketvibe', 'BasketVibe', 'ligue J' || f.round_number,
         case when f.home_team_id = me.team_id then f.away_team else f.home_team end,
         case when f.home_team_id = me.team_id then 'domicile' else 'extérieur' end,
         ((f.match_day + time '20:00') at time zone 'Europe/Paris'),
         ((f.match_day + time '19:45') at time zone 'Europe/Paris'), null::bool, null::text
  from silver.bv_fixtures f cross join silver.bv_my_team me
  where f.is_mine and f.status = 'scheduled'
  union all
  select 'basketvibe', 'BasketVibe', 'amical', opponent, null, kickoff, kickoff - interval '15 minutes', saisie, null from bv_fr
  union all
  select 'sixzeroleague', 'Six Zero League', s.competition || ' ' || s.label, s.opponent, s.venue, s.scheduled_at, s.scheduled_at, null, null
  from silver.sz_schedule s where s.i_play and s.status <> 'complete'
  union all
  select 'teamsoccer', u.team, u.competition, u.opponent, u.venue,
         u.match_date_paris at time zone 'Europe/Paris', u.lineup_deadline_paris at time zone 'Europe/Paris', u.lineup_saved, null
  from gold.ts_upcoming u
  union all
  select 'hockeynation', coalesce(g.team_level, 'Hockey Nation'), g.game_type,
         case when g.home_is_mine then g.away else g.home end,
         case when g.home_is_mine then 'domicile' else 'extérieur' end, g.scheduled_at, g.scheduled_at, null, null
  from silver.hn_games g where (g.home_is_mine or g.away_is_mine) and g.my_result is null
  union all
  select 'hardwood', 'Hardwood', h.game_type, case when h.is_home then h.visitor else h.home end,
         case when h.is_home then 'domicile' else 'extérieur' end,
         (h.real_day + time '09:00') at time zone 'America/Los_Angeles', (h.real_day + time '09:00') at time zone 'America/Los_Angeles', null, null
  from hw
  union all
  select 'derbymanager', dm.club, dm.competition || ' ' || dm.round, dm.opponent,
         case when dm.is_home then 'domicile' else 'extérieur' end, null, null, null, dm.date_txt || ' ' || dm.time_txt
  from dm
)
select m.jeu, m.equipe, m.competition, m.adversaire, m.lieu,
       m.kickoff at time zone 'Europe/Paris' as coup_envoi_paris,
       m.limite_saisie at time zone 'Europe/Paris' as limite_saisie_paris,
       m.saisie_faite, m.date_texte,
       fr.capture_paris as calendrier_capture_paris, fr.age_h as calendrier_age_h, fr.perime as calendrier_perime,
       case when fr.perime then 'exporte le calendrier d''abord'
            when m.kickoff is null then 'à vérifier : date non convertie'
            when m.saisie_faite then 'saisie déjà enregistrée'
            else 'à saisir aujourd''hui' end as etat
from m
cross join fin
left join gold.calendrier_fraicheur fr   -- Hockey Nation : un seul calendrier pour les 4 équipes
       on fr.jeu = m.jeu and fr.equipe = case when m.jeu = 'hockeynation' then 'Hockey Nation' else m.equipe end
where m.kickoff is null
   or (m.kickoff > now() and m.kickoff < fin.limite)
order by m.kickoff nulls last, m.jeu, m.equipe;

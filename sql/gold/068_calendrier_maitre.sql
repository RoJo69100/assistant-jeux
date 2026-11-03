-- Refonte v2, étape 1.4 : calendrier maître générique, sur core.fixture et core.game_params.
-- Remplace sql/gold/061_calendrier_maitre.sql, écrit le 2026-11-02 sans être appliqué (les vues n'existaient pas en base
-- le 2026-11-03) : pas d'ancienne vue, donc pas de parité ; contrôlé contre silver le 2026-11-03.
-- Règle apprise 69 (rétro 2026-11-02 soir) : contrôler le calendrier lui-même avant tout plan du jour.
--
-- gold.calendrier_fraicheur : une ligne par jeu — dernière capture de l'écran calendrier (core.game_params
--   ecran_calendrier : chemin d'API et âge max), âge en heures, `perime` = capture trop vieille OU un de mes matchs
--   (hors amicaux) non joué dont le jour ou le coup d'envoi est passé (le calendrier ne sait pas encore qu'il a été joué). Périmé = « exporte le calendrier ».
-- gold.calendrier_maitre : mes matchs non joués d'aujourd'hui et de demain (Paris) : un match de demain se prépare
--   aujourd'hui (inviolable 3). Coup d'envoi nul quand le jeu ne le donne pas (BV ligue : fuseau non sourcé).

insert into core.game_params (game, key, value, source, verified_on) values
  ('basketvibe', 'ecran_calendrier',
   '{"path_re": "^/api/v1/leagues/[^/]+/seasons/[^/]+/fixtures$", "max_age_h": 12}',
   'sql/gold/061_calendrier_maitre.sql (silver.bv_fixtures) ; rétro 2026-11-02 soir, règle 69 (12 h)', '2026-11-03'),
  ('hockeynation', 'ecran_calendrier',
   '{"path_re": "^/api/club/[0-9a-f-]{36}/game-overview$", "max_age_h": 12}',
   'core.export_rule HN 13 (Matchs, programme) ; rétro 2026-11-02 soir, règle 69 (12 h)', '2026-11-03')
on conflict (game, key) do nothing;

create or replace view gold.calendrier_fraicheur with (security_invoker = true) as
with p as (
  select game, value ->> 'path_re' as path_re, (value ->> 'max_age_h')::int as max_age_h
  from core.game_params where key = 'ecran_calendrier'
),
cap as (
  select p.game, max(r.captured_at) as capture
  from p
  left join bronze.raw_pages r
    on r.game = p.game and r.source = 'api'
   and coalesce((r.payload ->> 'status')::int, 200) = 200
   and regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', '') ~ p.path_re
  group by p.game
),
passe as (
  select game, count(*) as n, string_agg(distinct to_char(day, 'DD/MM'), ', ') as jours
  from core.fixture
  where not played and competition_kind <> 'amical'
    and (day < current_date or scheduled_at < now())
  group by game
)
select p.game, c.capture at time zone 'Europe/Paris' as capture_paris,
       round(extract(epoch from now() - c.capture) / 3600) as age_h, p.max_age_h,
       coalesce(x.n, 0) as matchs_passes_non_joues, x.jours,
       c.capture is null or now() - c.capture > make_interval(hours => p.max_age_h) or x.n > 0 as perime
from p
left join cap c using (game)
left join passe x using (game);

create or replace view gold.calendrier_maitre with (security_invoker = true) as
select f.game, f.team_id, f.competition_kind, f.round_no, f.opponent,
       case when f.home then 'domicile' when not f.home then 'extérieur' end as lieu,
       f.day, f.scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris,
       fr.capture_paris, fr.age_h, fr.perime
from core.fixture f
left join gold.calendrier_fraicheur fr using (game)
where not f.played
  and f.day between current_date and current_date + 1
  and (f.scheduled_at is null or f.scheduled_at >= now())
order by f.game, f.day, f.scheduled_at nulls last;

grant select on gold.calendrier_fraicheur, gold.calendrier_maitre to assistant_ro;

-- Calendrier, étape 5c (docs/refonte-v3/journal-aujourdhui.md, critère J3) : les pages calendrier reçues en bronze
-- donnent à core.fixture le jour, le coup d'envoi en UTC (fuseau lu dans la page, jamais supposé), le statut,
-- le score, les équipes, la compétition et l'identifiant du match.
-- Configuration lisible, sans code par jeu :
--   core.calendrier_page  : une ligne par type de page (motif d'URL, chemin du tableau ou de l'objet, compétition,
--                           minutes de verrou avant le coup d'envoi avec la source de la règle, statuts « joué »).
--   core.calendrier_champ : le tableau « champ de la page -> colonne » (chemin JSON, ou motif d'URL pour l'identifiant).
-- Un autre jeu n'ajoute que des lignes dans ces deux tables ; son adaptateur lit silver.calendrier (game = '<jeu>').
-- Additif : create table if not exists, create or replace view, insert … on conflict do nothing. Aucun drop.

create table if not exists core.calendrier_page (
  game            text    not null,
  source          text    not null,           -- nom court du type de page
  url_motif       text    not null,           -- regex sur bronze.raw_pages.source_url
  racine          text[],                     -- chemin du tableau de matchs dans le payload
  objet           text[],                     -- ou chemin de l'objet unique (page d'un match)
  competition_kind text   not null,           -- ligue | coupe | amical (vocabulaire de core.fixture)
  statuts_joues   text[]  not null,           -- valeurs du statut qui veulent dire « joué »
  verrou_minutes  int     not null,           -- verrou de la tactique = coup d'envoi - n minutes
  verrou_source   text    not null,           -- règle sourcée (skill)
  primary key (game, source),
  check (racine is not null or objet is not null)
);

create table if not exists core.calendrier_champ (
  game      text not null,
  source    text not null,
  colonne   text not null check (colonne in ('fixture_id', 'match_id', 'jour', 'heure_utc', 'heure_locale', 'fuseau',
                                             'statut', 'tour', 'dom_id', 'ext_id', 'dom_nom', 'ext_nom',
                                             'score_dom', 'score_ext', 'competition_nom')),
  chemin    text[],                            -- chemin JSON dans l'élément (ou l'objet)
  url_motif text,                              -- sinon : regex à un groupe sur source_url
  primary key (game, source, colonne),
  check (chemin is not null or url_motif is not null)
);

alter table core.calendrier_page  enable row level security;
alter table core.calendrier_champ enable row level security;
do $$ begin
  if not exists (select 1 from pg_policies where schemaname = 'core' and tablename = 'calendrier_page' and policyname = 'assistant_ro_select') then
    create policy assistant_ro_select on core.calendrier_page for select to assistant_ro using (true);
  end if;
  if not exists (select 1 from pg_policies where schemaname = 'core' and tablename = 'calendrier_champ' and policyname = 'assistant_ro_select') then
    create policy assistant_ro_select on core.calendrier_champ for select to assistant_ro using (true);
  end if;
end $$;
grant select on core.calendrier_page, core.calendrier_champ to assistant_ro;

insert into core.calendrier_page (game, source, url_motif, racine, objet, competition_kind, statuts_joues, verrou_minutes, verrou_source) values
  ('basketvibe', 'amicaux',        '/api/v1/teams/[0-9a-f-]{36}/friendlies(\?|$)',      '{body,friendlies}',   null,     'amical', '{finished}', 15, 'basketvibe-saison 01-rythme [M§1.3] : verrou 15 min avant'),
  ('basketvibe', 'coupe',          '/api/v1/teams/[0-9a-f-]{36}/cup-fixtures(\?|$)',    '{body,cup_fixtures}', null,     'coupe',  '{finished}',  0, 'basketvibe-saison 05-coupes V-20261108-1 : verrouillée au coup d''envoi'),
  ('basketvibe', 'ligue',          '/api/v1/teams/[0-9a-f-]{36}/league-fixtures(\?|$)', '{body,fixtures}',     null,     'ligue',  '{finished}', 15, 'basketvibe-saison 01-rythme [M§1.3] : verrou 15 min avant'),
  ('basketvibe', 'apercu_ligue',   '/api/v1/fixtures/[0-9a-f-]{36}/preview(\?|$)',      null,                  '{body}', 'ligue',  '{finished}', 15, 'basketvibe-saison 01-rythme [M§1.3] : verrou 15 min avant'),
  ('basketvibe', 'apercu_amical',  '/api/v1/friendlies/[0-9a-f-]{36}/preview(\?|$)',    null,                  '{body}', 'amical', '{finished}', 15, 'basketvibe-saison 01-rythme [M§1.3] : verrou 15 min avant'),
  ('basketvibe', 'apercu_coupe',   '/api/v1/cup-fixtures/[0-9a-f-]{36}/preview(\?|$)',  null,                  '{body}', 'coupe',  '{finished}',  0, 'basketvibe-saison 05-coupes V-20261108-1 : verrouillée au coup d''envoi')
on conflict do nothing;

insert into core.calendrier_champ (game, source, colonne, chemin, url_motif) values
  -- liste des amicaux : kickoff_at est un instant ISO avec son fuseau (suffixe Z)
  ('basketvibe', 'amicaux', 'fixture_id', '{id}', null),
  ('basketvibe', 'amicaux', 'match_id',   '{match_id}', null),
  ('basketvibe', 'amicaux', 'jour',       '{match_day}', null),
  ('basketvibe', 'amicaux', 'heure_utc',  '{kickoff_at}', null),
  ('basketvibe', 'amicaux', 'statut',     '{status}', null),
  ('basketvibe', 'amicaux', 'dom_id',     '{home_team_id}', null),
  ('basketvibe', 'amicaux', 'ext_id',     '{away_team_id}', null),
  ('basketvibe', 'amicaux', 'dom_nom',    '{home_team_name}', null),
  ('basketvibe', 'amicaux', 'ext_nom',    '{away_team_name}', null),
  ('basketvibe', 'amicaux', 'score_dom',  '{home_score}', null),
  ('basketvibe', 'amicaux', 'score_ext',  '{away_score}', null),
  -- liste des matchs de coupe : heure locale + fuseau donnés par la page
  ('basketvibe', 'coupe', 'fixture_id',      '{id}', null),
  ('basketvibe', 'coupe', 'match_id',        '{match_id}', null),
  ('basketvibe', 'coupe', 'jour',            '{match_day}', null),
  ('basketvibe', 'coupe', 'heure_locale',    '{kickoff_time_local}', null),
  ('basketvibe', 'coupe', 'fuseau',          '{kickoff_timezone}', null),
  ('basketvibe', 'coupe', 'statut',          '{status}', null),
  ('basketvibe', 'coupe', 'tour',            '{round_number}', null),
  ('basketvibe', 'coupe', 'dom_id',          '{home_team_id}', null),
  ('basketvibe', 'coupe', 'ext_id',          '{away_team_id}', null),
  ('basketvibe', 'coupe', 'dom_nom',         '{home_team_name}', null),
  ('basketvibe', 'coupe', 'ext_nom',         '{away_team_name}', null),
  ('basketvibe', 'coupe', 'score_dom',       '{home_score}', null),
  ('basketvibe', 'coupe', 'score_ext',       '{away_score}', null),
  ('basketvibe', 'coupe', 'competition_nom', '{cup_name}', null),
  -- liste des matchs de ligue de mon équipe : pas d'heure dans la page (elle vient de l'aperçu)
  ('basketvibe', 'ligue', 'fixture_id', '{id}', null),
  ('basketvibe', 'ligue', 'match_id',   '{match_id}', null),
  ('basketvibe', 'ligue', 'jour',       '{match_day}', null),
  ('basketvibe', 'ligue', 'statut',     '{status}', null),
  ('basketvibe', 'ligue', 'tour',       '{round_number}', null),
  ('basketvibe', 'ligue', 'dom_id',     '{home_team_id}', null),
  ('basketvibe', 'ligue', 'ext_id',     '{away_team_id}', null),
  ('basketvibe', 'ligue', 'score_dom',  '{home_score}', null),
  ('basketvibe', 'ligue', 'score_ext',  '{away_score}', null)
on conflict do nothing;

-- Aperçu d'un match (ligue, amical, coupe) : même format ; kickoff_time + league_timezone (fuseau de l'hôte).
insert into core.calendrier_champ (game, source, colonne, chemin, url_motif)
select 'basketvibe', s.source, c.colonne, c.chemin::text[], c.url_motif
from (values ('apercu_ligue'), ('apercu_amical'), ('apercu_coupe')) s(source)
cross join (values
  ('fixture_id',   null,                 '/(?:fixtures|friendlies|cup-fixtures)/([0-9a-f-]{36})/preview'),
  ('match_id',     '{match_id}',         null),
  ('jour',         '{match_day}',        null),
  ('heure_locale', '{kickoff_time}',     null),
  ('fuseau',       '{league_timezone}',  null),
  ('statut',       '{kind}',             null),
  ('tour',         '{round_number}',     null),
  ('dom_id',       '{home_team,id}',     null),
  ('ext_id',       '{away_team,id}',     null),
  ('dom_nom',      '{home_team,name}',   null),
  ('ext_nom',      '{away_team,name}',   null),
  ('score_dom',    '{home_score}',       null),
  ('score_ext',    '{away_score}',       null)
) c(colonne, chemin, url_motif)
on conflict do nothing;

-- Une ligne par match connu d'une page calendrier ; chaque champ = sa dernière valeur non nulle (toutes pages
-- confondues) ; joue = une page au moins dit « joué » ; coup_envoi_utc = instant ISO de la page, sinon
-- jour + heure locale dans le fuseau lu dans la page ; sans fuseau lu : null (jamais supposé).
create or replace view silver.calendrier with (security_invoker = true) as
with brut as (
  select p.game, p.source, p.competition_kind, p.statuts_joues, p.verrou_minutes, p.verrou_source,
         r.captured_at, r.source_url, e.elem
  from core.calendrier_page p
  join bronze.raw_pages r on r.game = p.game and r.source_url ~ p.url_motif
  cross join lateral jsonb_array_elements(
    case when p.racine is not null and jsonb_typeof(r.payload #> p.racine) = 'array' then r.payload #> p.racine
         when p.objet is not null and jsonb_typeof(r.payload #> p.objet) = 'object' then jsonb_build_array(r.payload #> p.objet)
         else '[]'::jsonb end) e(elem)
),
lu as (
  select b.game, b.source, b.competition_kind, b.statuts_joues, b.verrou_minutes, b.verrou_source, b.captured_at, c.*
  from brut b
  cross join lateral (
    select max(v) filter (where colonne = 'fixture_id')      as fixture_id,
           max(v) filter (where colonne = 'match_id')        as match_id,
           max(v) filter (where colonne = 'jour')            as jour,
           max(v) filter (where colonne = 'heure_utc')       as heure_utc,
           max(v) filter (where colonne = 'heure_locale')    as heure_locale,
           max(v) filter (where colonne = 'fuseau')          as fuseau,
           max(v) filter (where colonne = 'statut')          as statut,
           max(v) filter (where colonne = 'tour')            as tour,
           max(v) filter (where colonne = 'dom_id')          as dom_id,
           max(v) filter (where colonne = 'ext_id')          as ext_id,
           max(v) filter (where colonne = 'dom_nom')         as dom_nom,
           max(v) filter (where colonne = 'ext_nom')         as ext_nom,
           max(v) filter (where colonne = 'score_dom')       as score_dom,
           max(v) filter (where colonne = 'score_ext')       as score_ext,
           max(v) filter (where colonne = 'competition_nom') as competition_nom
    from (select f.colonne,
                 case when f.chemin is not null then b.elem #>> f.chemin
                      else substring(b.source_url from f.url_motif) end as v
          from core.calendrier_champ f
          where f.game = b.game and f.source = b.source) x
  ) c
),
pret as (
  select l.*,
         case when l.heure_utc is not null then l.heure_utc::timestamptz
              when l.jour is not null and l.heure_locale is not null and l.fuseau is not null
                then (l.jour || ' ' || l.heure_locale)::timestamp at time zone l.fuseau end as coup_envoi
  from lu l
  where l.fixture_id is not null
)
select game, fixture_id,
       (array_agg(competition_kind order by captured_at desc))[1]                                         as competition_kind,
       (array_agg(competition_nom order by captured_at desc) filter (where competition_nom is not null))[1] as competition_nom,
       (array_agg(match_id order by captured_at desc) filter (where match_id is not null))[1]             as match_id,
       (array_agg(jour::date order by captured_at desc) filter (where jour is not null))[1]               as jour,
       (array_agg(coup_envoi order by captured_at desc) filter (where coup_envoi is not null))[1]         as coup_envoi_utc,
       (array_agg(coalesce(fuseau, 'UTC (ISO)') order by captured_at desc) filter (where coup_envoi is not null))[1] as fuseau_lu,
       (array_agg(source order by captured_at desc) filter (where coup_envoi is not null))[1]            as source_heure,
       (array_agg(statut order by captured_at desc) filter (where statut is not null))[1]                 as statut,
       coalesce(bool_or(statut = any (statuts_joues)), false)                                             as joue,
       (array_agg(nullif(tour, '0')::int order by captured_at desc) filter (where nullif(tour, '0') is not null))[1] as tour,
       (array_agg(dom_id order by captured_at desc) filter (where dom_id is not null))[1]                 as dom_id,
       (array_agg(ext_id order by captured_at desc) filter (where ext_id is not null))[1]                 as ext_id,
       (array_agg(dom_nom order by captured_at desc) filter (where dom_nom is not null))[1]               as dom_nom,
       (array_agg(ext_nom order by captured_at desc) filter (where ext_nom is not null))[1]               as ext_nom,
       (array_agg(score_dom::int order by captured_at desc) filter (where score_dom is not null))[1]      as score_dom,
       (array_agg(score_ext::int order by captured_at desc) filter (where score_ext is not null))[1]      as score_ext,
       (array_agg(verrou_minutes order by captured_at desc))[1]                                           as verrou_minutes,
       (array_agg(verrou_source order by captured_at desc))[1]                                            as verrou_source,
       max(captured_at)                                                                                   as derniere_capture
from pret
group by game, fixture_id;

grant select on silver.calendrier to assistant_ro;

-- Test (J4) : la ligue J4 du 09/11 doit sortir à 19:00 UTC (20:00 Europe/Paris), la coupe du 12/11 à 19:00 UTC.
-- select fixture_id, competition_kind, jour, coup_envoi_utc, fuseau_lu, statut, joue from silver.calendrier
-- where game = 'basketvibe' and jour in ('2026-11-09', '2026-11-12');

-- Registre d'état, R4 (docs/refonte-v3/journal-aujourdhui.md) : quelles pages reçues en bronze sont lues ?
-- Type de page = pour une capture API le chemin sans hôte ni paramètres, identifiants remplacés
-- (uuid -> <id>, nombre -> <n>, club -> <slug>, région -> <code>) ; pour une page DOM « dom:<page_type> ».
-- core.page_reader : motif (regex sur le type de page) -> vue qui le lit. Semée à la main à partir des motifs
-- d'endpoint des vues silver.bv_* au 2026-11-09 (pg_get_viewdef) ; deux lecteurs gold (agenda) y figurent aussi.
-- Un type reçu sans ligne ici sort « page reçue, non lue » ; lu par gold seulement : « lue par gold seulement ».

create table if not exists core.page_reader (
  game    text not null,
  motif   text not null,
  lecteur text not null,
  primary key (game, motif, lecteur)
);
alter table core.page_reader enable row level security;
drop policy if exists assistant_ro_select on core.page_reader;
create policy assistant_ro_select on core.page_reader for select to assistant_ro using (true);
grant select on core.page_reader to assistant_ro;

insert into core.page_reader (game, motif, lecteur) values
  ('basketvibe', '^/api/v1/teams/<id>/academy$', 'silver.bv_academy_weekly'),
  ('basketvibe', '^/api/v1/teams/<id>/academy$', 'silver.bv_academy_candidates'),
  ('basketvibe', '^/api/v1/teams/<id>/finance$', 'silver.bv_finance_weekly'),
  ('basketvibe', '^/api/v1/teams/<id>/finance$', 'silver.bv_finance_seasons'),
  ('basketvibe', '^/api/v1/teams/<id>/finance$', 'silver.bv_finance_transactions'),
  ('basketvibe', '^/api/v1/(fixtures|friendlies|cup-fixtures)/<id>/', 'silver.bv_fixture_api'),
  ('basketvibe', '^/api/v1/leagues/<id>/seasons/<id>/fixtures$', 'silver.bv_fixtures'),
  ('basketvibe', '^/api/v1/auth/me$', 'silver.bv_my_team'),
  ('basketvibe', '^/api/v1/news$', 'silver.bv_news'),
  ('basketvibe', '^/api/v1/teams/<id>/personnel$', 'silver.bv_personnel_weekly'),
  ('basketvibe', '^dom:personnel$', 'silver.bv_personnel_weekly'),
  ('basketvibe', '^dom:roster_tiles$', 'silver.bv_player_salary_weekly'),
  ('basketvibe', '^/api/v1/teams/<id>/overview$', 'silver.bv_player_overview'),
  ('basketvibe', '^/api/v1/teams/<id>/training$', 'silver.bv_player_training'),
  ('basketvibe', '^/api/v1/teams/<id>/sponsor$', 'silver.bv_sponsor_weekly'),
  ('basketvibe', '^/api/v1/leagues/<id>/seasons/<id>/standings$', 'silver.bv_standings_weekly'),
  ('basketvibe', '^/api/v1/teams/<id>/training/recent-runs$', 'silver.bv_training_changes'),
  ('basketvibe', '^/api/v1/transfer-auctions$', 'silver.bv_transfer_auctions'),
  ('basketvibe', '^/api/v1/(transfer-history|teams/<id>/transfer-history|leagues/<id>/recent-transfers|players/<id>/transfer-history)$', 'silver.bv_transfers'),
  ('basketvibe', '^/api/v1/teams/<id>/my-transfer-auctions$', 'gold.bv_agenda'),
  ('basketvibe', '^/api/v1/teams/<id>/friendlies$', 'gold.bv_agenda')
on conflict do nothing;

create or replace view gold.bv_couverture_pages with (security_invoker = true) as
with recu as (
  select case when r.source = 'dom' then 'dom:' || r.page_type
              else regexp_replace(
                     regexp_replace(
                       regexp_replace(
                         regexp_replace(
                           regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', ''),
                           '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<id>', 'g'),
                         '/clubs/[^/]+', '/clubs/<slug>'),
                       '/regions/[^/]+', '/regions/<code>'),
                     '/[0-9]+(/|$)', '/<n>\1', 'g') end as type_page,
         r.source, r.captured_at
  from bronze.raw_pages r
  where r.game = 'basketvibe' and r.captured_at > now() - interval '30 days'
),
agg as (
  select type_page, min(source) as source, count(*) as nombre, max(captured_at) as derniere
  from recu group by type_page
)
select * from (
select a.type_page, a.source, a.nombre,
       a.derniere at time zone 'Europe/Paris' as derniere_arrivee_paris,
       case when exists (select 1 from core.page_reader p
                         where p.game = 'basketvibe' and p.lecteur like 'silver.%' and a.type_page ~ p.motif)
            then 'oui' else 'non' end as lu_par_silver,
       (select string_agg(p.lecteur, ', ' order by p.lecteur) from core.page_reader p
        where p.game = 'basketvibe' and a.type_page ~ p.motif) as lecteurs,
       case when not exists (select 1 from core.page_reader p where p.game = 'basketvibe' and a.type_page ~ p.motif)
                 then 'page reçue, non lue'
            when not exists (select 1 from core.page_reader p
                             where p.game = 'basketvibe' and p.lecteur like 'silver.%' and a.type_page ~ p.motif)
                 then 'lue par gold seulement' end as alerte
from agg a
) t
order by (t.lu_par_silver = 'oui'), t.nombre desc;

grant select on gold.bv_couverture_pages to assistant_ro;

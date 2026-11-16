-- Brique « base » (2026-11-16) : taille de la base et de bronze, croissance, ligne du plan du jour.
-- Plan Supabase Free : 500 Mo de base (limite publiée du plan ; le plan « free » est confirmé par l'API de l'organisation,
-- la limite elle-même n'est pas lisible en base : à vérifier dans Settings > Usage du tableau de bord).
-- Croissance = estimation : lignes ajoutées sur 7 jours (inserted_at) x taille moyenne par ligne (table + index + TOAST),
-- pour bronze.raw_pages et bronze.discord_messages, seules tables qui grossissent au rythme des captures.
-- Pas d'historique de taille en base : une mesure réelle demanderait un relevé quotidien.

create or replace view gold.base_taille with (security_invoker = true) as
with ajout as (
  select 'raw_pages'::text as src,
         count(*) as n,
         count(*) filter (where inserted_at > now() - interval '7 days') as n7,
         pg_total_relation_size('bronze.raw_pages') as octets
  from bronze.raw_pages
  union all
  select 'discord_messages', count(*),
         count(*) filter (where inserted_at > now() - interval '7 days'),
         pg_total_relation_size('bronze.discord_messages')
  from bronze.discord_messages
),
mesure as (
  select pg_database_size(current_database()) / 1048576.0 as base_mo,
         (select sum(pg_total_relation_size(c.oid)) from pg_class c join pg_namespace n on n.oid = c.relnamespace
           where n.nspname = 'bronze' and c.relkind in ('r', 'm')) / 1048576.0 as bronze_mo,
         pg_total_relation_size('bronze.raw_pages') / 1048576.0 as raw_pages_mo,
         (select sum(case when n > 0 then n7 / 7.0 * octets / n else 0 end) from ajout) / 1048576.0 as croissance_mo_j,
         500::numeric as limite_mo
)
select round(base_mo, 0) as base_mo, round(bronze_mo, 0) as bronze_mo, round(raw_pages_mo, 0) as raw_pages_mo,
       round(croissance_mo_j, 1) as croissance_mo_j, limite_mo,
       round(100 * base_mo / limite_mo, 0) as pct_limite,
       case when croissance_mo_j > 0 then floor((limite_mo - base_mo) / croissance_mo_j) end as jours_avant_limite,
       'Base : ' || round(base_mo, 0)::int || ' Mo sur ' || limite_mo::int || ' (plan gratuit), croissance ~'
         || replace(round(croissance_mo_j, 1)::text, '.', ',') || ' Mo/jour sur 7 jours' as ligne
from mesure;

grant select on gold.base_taille to assistant_ro;

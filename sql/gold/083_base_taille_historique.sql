-- Brique « base », étape 2 (2026-11-16) : historique quotidien de la taille de la base, rempli par pg_cron.
-- gold.base_taille_jour : une ligne par jour de Paris (taille de la base, de bronze, par schéma).
-- core.releve_taille_base() : insère ou met à jour la ligne du jour ; job pg_cron « releve-taille-base » à 02:07 UTC chaque jour.
-- gold.base_taille (remplace 078) : la croissance vient de l'historique dès qu'il a 3 jours de relevé sur les 7 derniers
-- (pente entre le premier et le dernier relevé), sinon de l'estimation d'avant (lignes ajoutées sur 7 jours x taille moyenne).
-- La ligne du plan passe en « ⚠ Base à X % de la limite » à partir de 70 %. Limite : 500 Mo (plan Free, à vérifier dans Settings > Usage).

create table if not exists gold.base_taille_jour (
  jour       date primary key,            -- jour de Paris
  base_mo    numeric not null,            -- pg_database_size
  bronze_mo  numeric not null,            -- tables du schéma bronze (index et TOAST compris)
  par_schema jsonb   not null,            -- {schéma: Mo} des tables et vues matérialisées ; « autre » = reste (catalogues, WAL, index hors tables)
  releve_a   timestamptz not null default now()
);
alter table gold.base_taille_jour enable row level security;
drop policy if exists assistant_ro_select on gold.base_taille_jour;
create policy assistant_ro_select on gold.base_taille_jour for select to assistant_ro using (true);
grant select on gold.base_taille_jour to assistant_ro;

create or replace function core.releve_taille_base() returns void
language plpgsql security definer set search_path = '' as $$
declare
  b numeric := pg_database_size(current_database()) / 1048576.0;
  s jsonb;
  br numeric;
begin
  select coalesce(jsonb_object_agg(sch, mo), '{}'::jsonb), coalesce(max(mo) filter (where sch = 'bronze'), 0)
    into s, br
  from (select n.nspname as sch, round(sum(pg_total_relation_size(c.oid)) / 1048576.0, 1) as mo
        from pg_class c join pg_namespace n on n.oid = c.relnamespace
        where c.relkind in ('r', 'm') and n.nspname not in ('pg_catalog', 'information_schema', 'pg_toast')
        group by n.nspname) x;
  s := s || jsonb_build_object('autre', round(b - coalesce((select sum(v::numeric) from jsonb_each_text(s) e(k, v)), 0), 1));
  insert into gold.base_taille_jour (jour, base_mo, bronze_mo, par_schema)
  values ((now() at time zone 'Europe/Paris')::date, round(b, 1), br, s)
  on conflict (jour) do update
    set base_mo = excluded.base_mo, bronze_mo = excluded.bronze_mo, par_schema = excluded.par_schema, releve_a = now();
end $$;
revoke all on function core.releve_taille_base() from public, anon, authenticated;

select cron.schedule('releve-taille-base', '7 2 * * *', 'select core.releve_taille_base()');

create or replace view gold.base_taille with (security_invoker = true) as
with ajout as (
  select count(*) as n, count(*) filter (where inserted_at > now() - interval '7 days') as n7,
         pg_total_relation_size('bronze.raw_pages') as octets
  from bronze.raw_pages
  union all
  select count(*), count(*) filter (where inserted_at > now() - interval '7 days'),
         pg_total_relation_size('bronze.discord_messages')
  from bronze.discord_messages
),
hist as (
  select count(*) as n_jours,
         (array_agg(base_mo order by jour))[1] as mo_debut, (array_agg(base_mo order by jour desc))[1] as mo_fin,
         min(jour) as j_debut, max(jour) as j_fin
  from gold.base_taille_jour
  where jour >= (now() at time zone 'Europe/Paris')::date - 7
),
mesure as (
  select pg_database_size(current_database()) / 1048576.0 as base_mo,
         (select sum(pg_total_relation_size(c.oid)) from pg_class c join pg_namespace n on n.oid = c.relnamespace
           where n.nspname = 'bronze' and c.relkind in ('r', 'm')) / 1048576.0 as bronze_mo,
         pg_total_relation_size('bronze.raw_pages') / 1048576.0 as raw_pages_mo,
         (select sum(case when n > 0 then n7 / 7.0 * octets / n else 0 end) from ajout) / 1048576.0 as estimation_mo_j,
         h.n_jours, case when h.n_jours >= 3 and h.j_fin > h.j_debut then (h.mo_fin - h.mo_debut) / (h.j_fin - h.j_debut) end as historique_mo_j,
         500::numeric as limite_mo
  from hist h
),
choix as (
  select m.*, coalesce(historique_mo_j, estimation_mo_j) as croissance_mo_j,
         case when historique_mo_j is not null then 'historique' else 'estimation' end as source_croissance
  from mesure m
)
select round(base_mo, 0) as base_mo, round(bronze_mo, 0) as bronze_mo, round(raw_pages_mo, 0) as raw_pages_mo,
       round(croissance_mo_j, 1) as croissance_mo_j, limite_mo,
       round(100 * base_mo / limite_mo, 0) as pct_limite,
       case when croissance_mo_j > 0 then floor((limite_mo - base_mo) / croissance_mo_j) end as jours_avant_limite,
       case when 100 * base_mo / limite_mo >= 70
            then '⚠ Base à ' || round(100 * base_mo / limite_mo, 0)::int || ' % de la limite ('
                 || round(base_mo, 0)::int || ' Mo sur ' || limite_mo::int || ', plan gratuit), croissance '
                 || case when source_croissance = 'estimation' then '~' else '' end
                 || replace(round(croissance_mo_j, 1)::text, '.', ',') || ' Mo/jour sur 7 jours'
            else 'Base : ' || round(base_mo, 0)::int || ' Mo sur ' || limite_mo::int || ' (plan gratuit), croissance '
                 || case when source_croissance = 'estimation' then '~' else '' end
                 || replace(round(croissance_mo_j, 1)::text, '.', ',') || ' Mo/jour sur 7 jours'
       end as ligne,
       source_croissance, n_jours as jours_historique   -- colonnes ajoutées en fin de vue (create or replace)
from choix;

grant select on gold.base_taille to assistant_ro;

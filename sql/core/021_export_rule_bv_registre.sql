-- Registre d'état, R1 + R2 + R3 (docs/refonte-v3/journal-aujourdhui.md) : une seule liste d'écrans BasketVibe.
-- core.export_rule porte les 14 écrans ; gold.bv_exports_state en est redéfinie, mêmes colonnes, mêmes lignes.
-- R2 : l'arrivée est lue dans bronze.raw_pages (toute page reçue, statut 200), plus dans silver.bv_api.
-- R3 : un écran « optionnel si vide » sans page récente est « 🟩 optionnel », jamais « à refaire ».
-- page_dom : écran dont le texte de la page (source 'dom') suffit quand l'API n'est plus capturée
-- (Personnel depuis le 25/10, lu par silver.bv_personnel_weekly).

alter table core.export_rule add column if not exists optionnel_si_vide boolean not null default false;
alter table core.export_rule add column if not exists page_dom text;

update core.export_rule set optionnel_si_vide = true
where game = 'basketvibe' and ecran = 'Mes enchères';
update core.export_rule set page_dom = 'personnel'
where game = 'basketvibe' and ecran = 'Personnel';

create or replace view gold.bv_exports_state with (security_invoker = true) as
with vu as (
  select e.ordre, e.ecran, e.pour_quoi, e.max_age_h, e.optionnel_si_vide,
         greatest(
           (select max(r.captured_at) from bronze.raw_pages r
            where r.game = 'basketvibe' and r.source = 'api'
              and coalesce((r.payload ->> 'status')::int, 200) = 200
              and regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', '') ~ e.path_re),
           (select max(r.captured_at) from bronze.raw_pages r
            where r.game = 'basketvibe' and r.source = 'dom' and r.page_type = e.page_dom)
         ) as dernier
  from core.export_rule e
  where e.game = 'basketvibe' and e.actif
)
select v.ordre, v.ecran, v.pour_quoi,
       v.dernier at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - v.dernier) / 3600) as age_h,
       case when v.dernier is null and v.optionnel_si_vide then '🟩 optionnel'
            when v.dernier is null then '🟥 jamais'
            when v.max_age_h is not null and now() - v.dernier > make_interval(hours => v.max_age_h)
                 then case when v.optionnel_si_vide then '🟩 optionnel' else '🟧 à refaire' end
            else '🟩 à jour' end as statut
from vu v
order by v.ordre;

grant select on gold.bv_exports_state to assistant_ro;

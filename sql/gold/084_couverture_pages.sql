-- Brique « base », étape 3 (2026-11-16) : gold.couverture_pages = gold.bv_couverture_pages (core/022) généralisée aux 6 jeux.
-- Une ligne par (jeu, type de page) reçu depuis 30 jours : nombre, dernière arrivée (heure de Paris), lecteurs (core.page_reader),
-- raison d'ignorance (core.page_ignore). Alerte : « page reçue, non lue » (aucun lecteur, non ignorée) ou « lue par gold seulement ».
-- gold.bv_couverture_pages reste, filtrée sur BasketVibe, avec ses colonnes d'origine.

create or replace view gold.couverture_pages with (security_invoker = true) as
with recu as (
  select r.game, core.type_page(r.source, r.page_type, r.source_url) as type_page, r.source, r.captured_at
  from bronze.raw_pages r
  where r.captured_at > now() - interval '30 days'
),
agg as (
  select game, type_page, min(source) as source, count(*) as nombre, max(captured_at) as derniere
  from recu group by game, type_page
)
select a.game, a.type_page, a.source, a.nombre,
       a.derniere at time zone 'Europe/Paris' as derniere_arrivee_paris,
       case when exists (select 1 from core.page_reader p
                         where p.game = a.game and p.lecteur like 'silver.%' and a.type_page ~ p.motif)
            then 'oui' else 'non' end as lu_par_silver,
       (select string_agg(p.lecteur, ', ' order by p.lecteur) from core.page_reader p
        where p.game = a.game and a.type_page ~ p.motif) as lecteurs,
       (select string_agg(i.raison, ' ; ' order by i.raison) from core.page_ignore i
        where i.game = a.game and a.type_page ~ i.motif) as ignoree,
       case when exists (select 1 from core.page_ignore i where i.game = a.game and a.type_page ~ i.motif)
                 then null
            when not exists (select 1 from core.page_reader p where p.game = a.game and a.type_page ~ p.motif)
                 then 'page reçue, non lue'
            when not exists (select 1 from core.page_reader p
                             where p.game = a.game and p.lecteur like 'silver.%' and a.type_page ~ p.motif)
                 then 'lue par gold seulement' end as alerte
from agg a;

create or replace view gold.bv_couverture_pages with (security_invoker = true) as
select type_page, source, nombre, derniere_arrivee_paris, lu_par_silver, lecteurs, alerte
from gold.couverture_pages
where game = 'basketvibe'
order by (lu_par_silver = 'oui'), nombre desc;

grant select on gold.couverture_pages, gold.bv_couverture_pages to assistant_ro;

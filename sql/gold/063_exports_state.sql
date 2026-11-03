-- Refonte v2, étape 1.4 : fraîcheur des exports pour tous les jeux, depuis core.export_rule et le bronze.
-- Remplace à terme gold.<jeu>_exports_state (parité : pipelines/exports_parite.py).

create or replace view gold.exports_state with (security_invoker = true) as
with captures as (
  select r.game, r.captured_at,
         regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', '') as path
  from bronze.raw_pages r
  where r.source = 'api'
    and coalesce((r.payload ->> 'status')::int, 200) = 200
    and r.game in (select distinct game from core.export_rule where actif)
)
select e.game, e.ordre, e.ecran, e.pour_quoi,
       max(c.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(c.captured_at)) / 3600) as age_h,
       case when max(c.captured_at) is null then '🟥 jamais'
            when now() - max(c.captured_at) > make_interval(hours => e.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut
from core.export_rule e
left join captures c on c.game = e.game and c.path ~ e.path_re
where e.actif
group by e.game, e.ordre, e.ecran, e.pour_quoi, e.max_age_h;

grant select on gold.exports_state to assistant_ro;

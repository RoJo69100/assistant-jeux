-- Refonte v2, étape 1.4 : fraîcheur des exports pour tous les jeux, depuis core.export_rule et le bronze.
-- Remplace à terme gold.<jeu>_exports_state (parité : pipelines/exports_parite.py).
-- 2026-11-04 : champ lu (path, url, page_type, page_url), règles par équipe (team_id, club en fin de vue),
-- corps en tableau, titres exclus, âge limite facultatif (core/008_export_rule_4_jeux.sql).

create or replace view gold.exports_state with (security_invoker = true) as
with equipes as (
  select distinct on (game, team_id) game, team_id, club_label
  from core.player_daily
  order by game, team_id, day desc
),
regles as (
  select e.*, null::text as team_id, null::text as club, e.path_re as re
  from core.export_rule e where e.actif and not e.par_equipe
  union all
  select e.*, t.team_id, t.club_label, replace(e.path_re, '{team}', t.team_id)
  from core.export_rule e join equipes t on t.game = e.game
  where e.actif and e.par_equipe
),
captures as (
  select r.game, r.captured_at, r.source, r.page_type, r.page_url,
         regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', '') as path,
         regexp_replace(r.source_url, '^https?://[^/]+', '')                     as url,
         case when r.source = 'api' then coalesce((r.payload ->> 'status')::int, 200) end as status,
         case when r.source = 'api' then jsonb_typeof(r.payload -> 'body') end           as body_type,
         case when r.source = 'dom' then r.payload ->> 'title' end                        as title
  from bronze.raw_pages r
  where r.game in (select distinct game from core.export_rule where actif)
)
select e.game, e.ordre, e.ecran, e.pour_quoi,
       max(c.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(c.captured_at)) / 3600) as age_h,
       case when max(c.captured_at) is null then '🟥 jamais'
            when e.max_age_h is not null and now() - max(c.captured_at) > make_interval(hours => e.max_age_h) then '🟧 à refaire'
            else '🟩 à jour' end as statut,
       e.team_id, e.club
from regles e
left join captures c
  on c.game = e.game
 and case e.champ
       when 'path'      then c.source = 'api' and c.status = 200 and c.path ~ e.re
       when 'url'       then c.source = 'api' and c.status = 200 and c.url ~ e.re
       when 'page_type' then c.page_type ~ e.re
       when 'page_url'  then c.page_url ~ e.re
     end
 and (not e.corps_tableau or c.body_type = 'array')
 and (e.source_filtre is null or c.source = e.source_filtre)
 and (e.titre_exclu_re is null or coalesce(c.title, '') !~* e.titre_exclu_re)
group by e.game, e.ordre, e.ecran, e.pour_quoi, e.max_age_h, e.team_id, e.club;

grant select on gold.exports_state to assistant_ro;

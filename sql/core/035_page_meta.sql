-- Métadonnées légères des pages (25/11/2026) : gold.exports_state ne relit plus le JSON de bronze.raw_pages.
-- Mesure du 25/11 (EXPLAIN ANALYZE, instance saine) : gold.exports_state 5,5 s et 410 572 blocs lus en cache pour 88 lignes,
-- parce que chaque passage détoastait le payload des ~16 000 pages (status, type du corps, titre) ; la vue est lue par
-- gold.daily_alerts_src (rafraîchissement) et par chaque passage quotidien.
-- core.page_meta garde une ligne par page, extraite une seule fois ; bronze.raw_pages reste immuable (aucun déclencheur sur
-- l'ingestion). Les pages pas encore rattrapées sont lues en direct (id au-delà du dernier rattrapé), la vue reste donc exacte
-- entre deux rattrapages.

create table if not exists core.page_meta (
  page_id     bigint primary key,
  game        text not null,
  captured_at timestamptz,
  source      text,
  page_type   text,
  page_url    text,
  path        text,
  url         text,
  status      integer,
  body_type   text,
  title       text
);
create index if not exists page_meta_game on core.page_meta (game);
grant select on core.page_meta to assistant_ro;

-- Rattrapage par lots (mémoire bornée) : les pages absentes de core.page_meta, les plus anciennes d'abord.
create or replace function core.page_meta_rattraper(p_lot integer default 2000) returns integer
language plpgsql security definer set search_path = '' as $$
declare n integer;
begin
  insert into core.page_meta (page_id, game, captured_at, source, page_type, page_url, path, url, status, body_type, title)
  select r.id, r.game, r.captured_at, r.source, r.page_type, r.page_url,
         regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', ''),
         regexp_replace(r.source_url, '^https?://[^/]+', ''),
         case when r.source = 'api' then coalesce((r.payload ->> 'status')::integer, 200) end,
         case when r.source = 'api' then jsonb_typeof(r.payload -> 'body') end,
         case when r.source = 'dom' then r.payload ->> 'title' end
    from bronze.raw_pages r
   where not exists (select 1 from core.page_meta m where m.page_id = r.id)
   order by r.id
   limit p_lot
  on conflict (page_id) do nothing;
  get diagnostics n = row_count;
  return n;
end $$;
revoke all on function core.page_meta_rattraper(integer) from public;

create or replace view gold.exports_state with (security_invoker = true) as
with equipes as (
  select distinct on (player_daily.game, player_daily.team_id) player_daily.game, player_daily.team_id, player_daily.club_label
  from core.player_daily
  order by player_daily.game, player_daily.team_id, player_daily.day desc
), regles as (
  select e_1.game, e_1.ordre, e_1.ecran, e_1.path_re, e_1.max_age_h, e_1.pour_quoi, e_1.source, e_1.actif, e_1.champ,
         e_1.source_filtre, e_1.par_equipe, e_1.corps_tableau, e_1.titre_exclu_re,
         null::text as team_id, null::text as club, e_1.path_re as re
  from core.export_rule e_1
  where e_1.actif and not e_1.par_equipe
  union all
  select e_1.game, e_1.ordre, e_1.ecran, e_1.path_re, e_1.max_age_h, e_1.pour_quoi, e_1.source, e_1.actif, e_1.champ,
         e_1.source_filtre, e_1.par_equipe, e_1.corps_tableau, e_1.titre_exclu_re,
         t.team_id, t.club_label, replace(e_1.path_re, '{team}', t.team_id) as replace
  from core.export_rule e_1
  join equipes t on t.game = e_1.game
  where e_1.actif and e_1.par_equipe
), jeux as (
  select distinct export_rule.game from core.export_rule where export_rule.actif
), pages as (
  select m.game, m.captured_at, m.source, m.page_type, m.page_url, m.path, m.url, m.status, m.body_type, m.title
  from core.page_meta m
  where m.game in (select game from jeux)
  union all  -- pages arrivées depuis le dernier rattrapage : lues en direct (peu de lignes, par la clé primaire)
  select r.game, r.captured_at, r.source, r.page_type, r.page_url,
         regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+', ''),
         regexp_replace(r.source_url, '^https?://[^/]+', ''),
         case when r.source = 'api' then coalesce((r.payload ->> 'status')::integer, 200) end,
         case when r.source = 'api' then jsonb_typeof(r.payload -> 'body') end,
         case when r.source = 'dom' then r.payload ->> 'title' end
  from bronze.raw_pages r
  where r.id > (select coalesce(max(page_id), 0) from core.page_meta)
    and r.game in (select game from jeux)
), captures as (  -- une ligne par page distincte (dernière capture) : moins de lignes à confronter aux expressions régulières
  select game, source, page_type, page_url, path, url, status, body_type, title, max(captured_at) as captured_at
  from pages
  group by game, source, page_type, page_url, path, url, status, body_type, title
)
select e.game, e.ordre, e.ecran, e.pour_quoi,
       max(c.captured_at) at time zone 'Europe/Paris' as dernier_paris,
       round(extract(epoch from now() - max(c.captured_at)) / 3600::numeric) as age_h,
       case
         when max(c.captured_at) is null then '🟥 jamais'
         when e.max_age_h is not null and now() - max(c.captured_at) > make_interval(hours => e.max_age_h) then '🟧 à refaire'
         else '🟩 à jour'
       end as statut,
       e.team_id, e.club
from regles e
left join captures c on c.game = e.game
  and case e.champ
        when 'path' then c.source = 'api' and c.status = 200 and c.path ~ e.re
        when 'url' then c.source = 'api' and c.status = 200 and c.url ~ e.re
        when 'page_type' then c.page_type ~ e.re
        when 'page_url' then c.page_url ~ e.re
        else null::boolean
      end
  and (not e.corps_tableau or c.body_type = 'array')
  and (e.source_filtre is null or c.source = e.source_filtre)
  and (e.titre_exclu_re is null or coalesce(c.title, '') !~* e.titre_exclu_re)
group by e.game, e.ordre, e.ecran, e.pour_quoi, e.max_age_h, e.team_id, e.club;
grant select on gold.exports_state to assistant_ro;

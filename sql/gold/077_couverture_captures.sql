-- Brique « collecte » (2026-11-16) : couverture des captures, tous jeux, depuis bronze.raw_pages.
-- Numéro 077 : la série gold va jusqu'à 076 (028 est déjà pris par 028_hn_coach_potential_scout_targets).
--
-- gold.couverture_captures : dernière capture par jeu et par page_type.
-- gold.derniere_capture    : dernière capture par jeu + la ligne du plan « Dernière capture il y a X h ».
-- gold.bv_captures_manquantes : BasketVibe, ce que la collecte n'a pas reçu :
--   * matchs joués (core.fixture) des 14 derniers jours sans box, sans quarts (period-box) ou sans play-by-play ;
--     « box » = copie de la page du match (source dom) ; « quarts » et « play-by-play » = appels de l'API du match (silver.bv_fixture_api) ;
--   * clubs dont le dernier instantané d'effectif (silver.bv_club_roster, est_derniere) a plus de 7 jours.
--   Remplace la ligne « Dernier match exporté » retirée du plan au commit fa74723 (elle lisait le calendrier, pas la page exportée).

create or replace view gold.couverture_captures with (security_invoker = true) as
select r.game, r.page_type,
       max(r.captured_at) at time zone 'Europe/Paris'                        as derniere_paris,
       round(extract(epoch from now() - max(r.captured_at)) / 3600)           as age_h,
       count(*) filter (where r.captured_at > now() - interval '30 days')    as n_30j,
       count(*)                                                               as n_total
from bronze.raw_pages r
group by r.game, r.page_type;

create or replace view gold.derniere_capture with (security_invoker = true) as
select g.game, g.derniere_paris, g.age_h,
       'Dernière capture il y a ' || case when g.age_h < 1 then 'moins d''1 h' else g.age_h::int || ' h' end as ligne
from (select r.game,
             max(r.captured_at) at time zone 'Europe/Paris'                       as derniere_paris,
             floor(extract(epoch from now() - max(r.captured_at)) / 3600)         as age_h
      from bronze.raw_pages r group by r.game) g;

create or replace view gold.bv_captures_manquantes with (security_invoker = true) as
with api as (
  select fixture_id::text as fid, bool_or(part = 'period-box') as quarts, bool_or(part = 'play-by-play') as pbp
  from silver.bv_fixture_api group by 1
),
box as (
  select distinct right(page_url, 36) as fid
  from bronze.raw_pages
  where game = 'basketvibe' and source = 'dom' and page_url ~ '/(match|friendly|cup)/[0-9a-f-]{36}$'
)
select 'match'::text as kind, f.fixture_id::text as ref, f.opponent as libelle, f.day, f.competition_kind,
       concat_ws(', ', case when box.fid is null then 'box' end,
                       case when not coalesce(api.quarts, false) then 'quarts' end,
                       case when not coalesce(api.pbp, false) then 'play-by-play' end) as manque,
       null::numeric as age_j
from core.fixture f
left join api on api.fid = f.fixture_id::text
left join box on box.fid = f.fixture_id::text
where f.game = 'basketvibe' and f.played
  and f.day >= (now() at time zone 'Europe/Paris')::date - 14
  and (box.fid is null or not coalesce(api.quarts, false) or not coalesce(api.pbp, false))
union all
select 'club', c.club_slug, max(c.team_name), null::date, null::text, 'effectif',
       round(extract(epoch from now() - max(c.captured_at)) / 86400, 1)
from silver.bv_club_roster c
where c.est_derniere
group by c.club_slug
having max(c.captured_at) < now() - interval '7 days';

grant select on gold.couverture_captures, gold.derniere_capture, gold.bv_captures_manquantes to assistant_ro;

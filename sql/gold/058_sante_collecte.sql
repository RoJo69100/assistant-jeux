-- gold.sante_collecte : ce qui n'arrive plus ou arrive vide, tous jeux (étape 0b du plan de conception,
-- remplace l'agent « sante-collecte » prévu). Une ligne par jeu × page_type vu dans les 60 derniers jours.
-- Lecture : select game, page_type, statut, jours_depuis, ecart_med_jours, taille_dernier, taille_med
--           from gold.sante_collecte where statut <> 'ok' [and game = '<jeu>'] order by game, statut limit 30;
-- Statuts :
--   arrete   rien depuis plus de max(2 × écart médian entre deux jours d'export, 2 jours), au moins 3 jours d'export
--   vide     le dernier export fait moins de 20 % de la taille médiane de son type de page
--   rare     moins de 3 jours d'export en 60 jours : pas de rythme mesurable
--   ok       le reste
-- Jours comptés à l'heure de Paris. Un type de page volontairement abandonné reste « arrete » : le noter dans la
-- config du jeu (docs/attentes/jeux/<jeu>.yaml), pas le cacher ici.

create or replace view gold.sante_collecte with (security_invoker = true) as
with p as (
    select game, page_type, captured_at, octet_length(payload::text) as taille,
           (captured_at at time zone 'Europe/Paris')::date as jour
    from bronze.raw_pages
    where captured_at > now() - interval '60 days'
), jours as (
    select game, page_type, jour,
           jour - lag(jour) over (partition by game, page_type order by jour) as ecart
    from (select distinct game, page_type, jour from p) d
), rythme as (
    select game, page_type, count(*) as jours_export,
           percentile_cont(0.5) within group (order by ecart) as ecart_med_jours
    from jours group by game, page_type
), s as (
    select game, page_type, count(*) as n_60j,
           count(*) filter (where captured_at > now() - interval '7 days') as n_7j,
           max(captured_at) as dernier,
           (array_agg(taille order by captured_at desc))[1] as taille_dernier,
           percentile_cont(0.5) within group (order by taille)::int as taille_med
    from p group by game, page_type
)
select s.game, s.page_type,
       case
           when r.jours_export < 3 then 'rare'
           when (now() at time zone 'Europe/Paris')::date - (s.dernier at time zone 'Europe/Paris')::date
                > greatest(2 * coalesce(r.ecart_med_jours, 1), 2) then 'arrete'
           when s.taille_dernier < 0.2 * s.taille_med then 'vide'
           else 'ok'
       end as statut,
       (now() at time zone 'Europe/Paris')::date - (s.dernier at time zone 'Europe/Paris')::date as jours_depuis,
       r.ecart_med_jours, r.jours_export, s.n_7j, s.n_60j,
       to_char(s.dernier at time zone 'Europe/Paris', 'YYYY-MM-DD HH24:MI') as dernier_paris,
       s.taille_dernier, s.taille_med
from s join rythme r using (game, page_type);

comment on view gold.sante_collecte is 'Santé de la collecte par jeu et type de page : arrete / vide / rare / ok (sql/gold/058_sante_collecte.sql)';

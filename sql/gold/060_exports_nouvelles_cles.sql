-- gold.exports_nouvelles_cles : clés JSON apparues récemment dans un type de page déjà connu, tous jeux
-- (étape 0d du plan de conception, 2026-11-02 : remplace la « détection des nouveautés » de l'agent lecteur-exports).
-- Une ligne par jeu × page_type × clé vue pour la première fois dans les 3 derniers jours, alors que ce page_type
-- existait déjà avant (sinon tout le type est nouveau : voir gold.sante_collecte, statut « rare »).
-- Clés lues : premier niveau du payload, payload.body, payload.body.data (formats des userscripts).
-- Lecture : select game, page_type, cle, premiere_paris, n, exemple
--           from gold.exports_nouvelles_cles where game = '<jeu>' order by page_type, cle limit 30;
-- Chaque clé listée = nouveauté : l'ajouter à docs/fiches/<jeu>/commun.md § Options observées (effet selon les skills,
-- sinon « effet inconnu : tester une option à la fois »).

create or replace view gold.exports_nouvelles_cles with (security_invoker = true) as
with r as (
    select game, page_type, captured_at, payload
    from bronze.raw_pages
    where captured_at > now() - interval '30 days'
), k as (
    select r.game, r.page_type, c.cle, r.captured_at, c.valeur
    from r
    cross join lateral (
        select 'payload.' || e.key as cle, e.value as valeur
        from jsonb_each(case when jsonb_typeof(r.payload) = 'object' then r.payload else '{}'::jsonb end) e
        union all
        select 'body.' || e.key, e.value
        from jsonb_each(case when jsonb_typeof(r.payload -> 'body') = 'object' then r.payload -> 'body' else '{}'::jsonb end) e
        union all
        select 'body.data.' || e.key, e.value
        from jsonb_each(case when jsonb_typeof(r.payload -> 'body' -> 'data') = 'object' then r.payload -> 'body' -> 'data' else '{}'::jsonb end) e
    ) c
), premiere as (
    select game, page_type, cle, min(captured_at) as premiere, count(*) as n,
           (array_agg(left(valeur::text, 80) order by captured_at desc))[1] as exemple
    from k group by game, page_type, cle
), type_debut as (
    select game, page_type, min(captured_at) as debut from r group by game, page_type
)
select p.game, p.page_type, p.cle,
       to_char(p.premiere at time zone 'Europe/Paris', 'YYYY-MM-DD HH24:MI') as premiere_paris,
       p.n, p.exemple
from premiere p join type_debut t using (game, page_type)
where p.premiere > now() - interval '3 days'
  and t.debut < p.premiere - interval '1 hour';

comment on view gold.exports_nouvelles_cles is 'Clés JSON nouvelles (3 derniers jours) dans un type de page déjà connu, tous jeux (sql/gold/060_exports_nouvelles_cles.sql)';

-- Six Zero League : réglages de la tactique par défaut ENREGISTRÉE (dernier export), dans l'ordre de l'écran.
-- Créée le 2026-10-31 : j'avais écrit « direction mixed » (vieux brief) alors que l'écran était en right-center
-- (silver.sz_tactics ne porte pas la direction ni l'agressivité). À lire AVANT tout rendu de composition.
-- Usage : select * from gold.sz_saisie_reglages order by ordre;
create or replace view gold.sz_saisie_reglages with (security_invoker = true) as
with d as (
  select body, captured_at from silver.sz_api
  where endpoint = '/teams/mine/tactics/default' order by captured_at desc limit 1
)
select v.ordre, v.reglage, v.valeur, d.captured_at as export_le
from d cross join lateral (values
  (1, 'Formation d''attaque', d.body->>'attackFormation'),
  (2, 'Formation de défense', d.body->>'defenseFormation'),
  (3, 'Places de défense', (select string_agg(k || ' ' || ((d.body->'defenseSpots')->>k), ', ' order by k)
                            from jsonb_object_keys(d.body->'defenseSpots') k)),
  (4, 'Direction d''attaque', d.body->>'attackDirection'),
  (5, 'Agressivité', d.body->>'aggression'),
  (6, 'Ordres de match', coalesce(nullif(jsonb_array_length(d.body->'orders'), 0)::text, 'aucun'))
) as v(ordre, reglage, valeur);

-- BasketVibe : ce que le chat dit de l'académie (salon #academy + mots-clés dans tous les salons, en plusieurs langues).
-- Consigne « export d'académie » : docs/decisions/cartes/basketvibe/academie.md § Après chaque export d'académie.
-- Les anciens noms de salons (« Community / academy ») et les doublons d'export sont fusionnés.
create or replace view gold.bv_academy_chat as
select distinct on (posted_at, author, left(content, 80))
       posted_at,
       channel,
       author,
       is_dev,
       content
from silver.bv_discord_messages
where channel ilike '%academy%'
   or content ~* '(academy|academia|akademi|scout|prospect|junior|júnior|juniores|giovani|jovens|mladi|rapport d.acad|jauge)'
order by posted_at, author, left(content, 80), channel;

-- Derby Manager : le tableau des matchs de la page d'équipe n'a pas d'en-tête.
-- Le userscript prend donc la PREMIÈRE ligne (le prochain match) comme `headers`,
-- et silver.dm_fixtures la perdait (constaté le 2026-11-02 : amical du 3 novembre
-- contre Royal Engineers absent, la vue commençait au 4 novembre).
-- Correctif : le tableau retenu (8 colonnes, 3e cellule « Compétition: Tour ») a
-- toujours une ligne de données en `headers` ; on la remet en tête des lignes.
-- Heure : la cellule colle une clé de tri « jours depuis 1970 » à l'heure
-- (« 20760.58333333333214:00 ») ; l'ancien regexp mangeait les chiffres de l'heure
-- (« :00 »). L'heure et la date se lisent désormais dans la clé (0,5833 j = 14:00),
-- exposées aussi en `coup_envoi` (heure affichée par le jeu, fuseau non vérifié).
create or replace view silver.dm_fixtures with (security_invoker = true) as
select s.team_id, s.captured_at, o as ord,
       regexp_replace(r->>0, '^[\d.]+', '') as date_txt,
       to_char(timestamp '1970-01-01' + substring(r->>0 from '^\d+(?:\.\d+)?')::numeric * interval '1 day'
               + interval '30 seconds', 'HH24:MI') as time_txt,
       trim(regexp_replace(split_part(regexp_replace(r->>2, '\s+', ' ', 'g'), ':', 1), '\s+', ' ', 'g')) as competition,
       trim(split_part(regexp_replace(r->>2, '\s+', ' ', 'g'), ':', 2)) as round,
       silver.dm_n(r->>3)::int as attendance, r->>4 = 'H' as is_home,
       trim(regexp_replace(r->>5, '\s*\(.*\)$', '')) as opponent, substring(r->>5 from '\((.*)\)') as opp_rank,
       substring(r->>6 from '(\d+)\s*:\s*\d+\s*$')::int as gf_home_side,
       substring(r->>6 from '(\d+)\s*$')::int as ga_away_side,
       substring(r->>6 from '^\((\d+:\d+)\)') as shootout,
       nullif(r->>7, '') as my_result,
       date_trunc('minute', timestamp '1970-01-01' + substring(r->>0 from '^\d+(?:\.\d+)?')::numeric * interval '1 day'
                  + interval '30 seconds') as coup_envoi
from silver.dm_team_src s
cross join lateral jsonb_array_elements(s.tables) tb
cross join lateral jsonb_array_elements(jsonb_build_array(tb->'headers') || (tb->'rows')) with ordinality x(r, o)
where jsonb_array_length(tb->'headers') = 8 and tb->'headers'->>2 ~ ':' and jsonb_array_length(r) = 8;

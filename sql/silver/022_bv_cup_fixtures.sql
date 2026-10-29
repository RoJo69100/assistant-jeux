-- Silver BasketVibe : les matchs de coupe (API /cup-fixtures/<id>/...) rejoignent les vues de match.
-- Même format que la ligue et les amicaux (preview, period-box, play-by-play, match-tactics) ; seul le préfixe d'URL change.
-- Colonne `competition` : 'league', 'friendly' ou 'cup'. Mêmes colonnes, même ordre que 007.
-- Effet : silver.bv_matches, silver.bv_match_player_stats, gold.bv_match_report et les vues qui en dépendent
-- voient les coupes ; les vues de tendance et de finances filtrent déjà competition = 'league' / 'friendly'.
-- Les routes /teams/<id>/cup-fixtures (liste) et /cup-editions/... (tableau) ne sont pas des matchs : exclues par le motif.

create or replace view silver.bv_fixture_api with (security_invoker = true) as
select a.*,
       (substring(a.endpoint from '^/(?:fixtures|friendlies|cup-fixtures)/([0-9a-f-]{36})/'))::uuid as fixture_id,
       substring(a.endpoint from '^/(?:fixtures|friendlies|cup-fixtures)/[0-9a-f-]{36}/(.+)$') as part,
       case when a.endpoint like '/friendlies/%' then 'friendly'
            when a.endpoint like '/cup-fixtures/%' then 'cup'
            else 'league' end as competition
from silver.bv_api a
where a.endpoint ~ '^/(fixtures|friendlies|cup-fixtures)/[0-9a-f-]{36}/';

-- Test : la coupe contre Maccabi (28/10, V 121-94) doit sortir avec my_result = 'W'.
-- select competition, match_day, home_team, away_team, home_score, away_score, my_result
-- from silver.bv_matches where competition = 'cup' order by match_day;

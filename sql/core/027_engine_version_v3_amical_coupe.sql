-- Étape 6c-bis, critères W1 et W2 (docs/refonte-v3/journal-aujourdhui.md, « Versions du moteur, étape 6c-bis »).
-- Migration additive : 2 lignes insérées, 1 ligne mise à jour (coupe v4). Aucun drop, aucun autre objet.

-- W1 : amical v3 et coupe v3 de la saison 1.
insert into core.engine_version (game, version, competition_kind, start_date, end_date, source, statut) values
  ('basketvibe', 'v3', 'amical', '2026-09-07', '2026-10-10',
   'préanalyse § 1.1 et étude des événements (10/10 = veille de l''annonce, amical en v3 ; début = premier match de la saison 1)',
   'déduit'),
  ('basketvibe', 'v3', 'coupe', '2026-09-07', '2026-10-27',
   'skill basketvibe-communaute 02-1 (v4 actif en coupe depuis le 27/10, donc v3 avant) ; début = premier match de la saison 1',
   'déduit');

-- W2 : la ligne coupe v4 commence le 27/10 et n'a plus de fin (le 31/10 était la borne des matchs détaillés, pas celle de la version).
update core.engine_version
   set start_date = '2026-10-27',
       end_date   = null,
       source     = 'skill basketvibe-communaute 02-1 (V-20261027-2 : v4 actif en ligue, coupe et amical depuis le 27/10) ; '
                    'fin : aucune (la borne du 31/10 de la première version de la ligne était celle des matchs détaillés)'
 where game = 'basketvibe' and version = 'v4' and competition_kind = 'coupe' and start_date = '2026-10-28';

-- Test : select competition_kind, version, count(*) from gold.bv_match_engine_version group by 1, 2 order by 1, 2;

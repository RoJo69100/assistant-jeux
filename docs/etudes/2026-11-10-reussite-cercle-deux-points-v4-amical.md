# Réussite au cercle et compétence Deux points, v4 amical (2026-11-10)

**Question** : dans le groupe v4 amical, nos tirs au cercle réussissent-ils plus souvent quand le tireur a un Deux points plus élevé ?
**Mesure** : probabilité linéaire, réussite 0/1 ~ Deux points / 10 ; pente en points de % pour +10 points de Deux points.

| groupe | n tirs | n matchs | estimé | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|
| v4 amical | 313 | 12 | +6,81 pts de % / +10 Deux points | [+3,92 ; +8,88] | bootstrap par grappes de matchs, 2 000 tirages, centiles, graine 20261110 | association présente |

- Périmètre : 16 matchs terminés à nous (11 au 27 octobre), 1 294 tirs à nous (fg2, fg3, miss_fg ; sans block ni lancers francs), 835 tirs à 2.
- Y0 = 220 (`shot_y < 220` = cercle), exactitude 97,7 % sur 487 tirs à 2 étiquetés (maximum unique). Au-dessus de 85 % : les 348 tirs à 2 non étiquetés sont classés (160 au cercle), aucun exclu.
- Tirs au cercle : 442 dans 16 matchs ; 129 sans relevé Deux points au jour ou à la veille (dont 4 matchs entiers, du 11 au 15 octobre, avant le premier relevé du 16), exclus. Reste 313 tirs, 12 matchs, 14 joueurs ; Deux points de 34 à 75 ; 246 valeurs à une décimale ; réussite 63,9 %.

**Sources** : `python -I pipelines/etudes/reussite_cercle_deux_points_v4_amical.py` ; recoupement des comptes de tirs par `sql.py` (jointure bv_match_events / bv_matches, 487 + 141 + 348 + 318 = 1 294).

**Limites**
- Dans ce groupe, tous les tirs à 2 étiquetés sont des réussis et tous les ratés sont non étiquetés. Y0 est donc calé sur des réussis seulement, et tous les ratés au cercle viennent de la règle `shot_y`. Hypothèse : la géométrie `shot_y` est la même pour réussis et ratés ; un export de ratés étiquetés (présents dans d'autres groupes) la confirmerait.
- Association, pas cause. Confusion probable : le tireur (les meilleurs en Deux points sont aussi souvent les intérieurs, plus près du panier, et athlétiques) et la colinéarité avec les autres compétences ; adversaires d'amical variés.
- 4 matchs sur 16 perdus faute de relevé, plus des tirs isolés sans relevé : échantillon non aléatoire.

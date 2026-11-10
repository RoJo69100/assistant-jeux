# Réussite au cercle selon la compétence Deux points, v4 amical (2026-11-10)

**Question** : dans le groupe v4 amical, de combien de points de pourcentage la réussite des tirs au cercle de nos joueurs varie-t-elle pour +10 points de Deux points ? Modèle de probabilité linéaire (réussite 0/1 ~ Deux points / 10).

| groupe | n tirs | n matchs | Y0 (exactitude) | pente (pts de % / +10 DP) | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|---|
| v4 amical | 313 | 12 | 220 (97,74 % sur 487 tirs à 2 étiquetés) | +6,81 | [+3,92 ; +8,88] | bootstrap par grappes de matchs, 2 000 tirages, graine 20261110, centiles | association présente |

Filtrage : 16 matchs terminés à nous ; 1 294 tirs (459 à 3 points) ; 835 tirs à 2, dont 487 étiquetés (282 cercle, 205 mi-distance) et 348 non étiquetés classés par shot_y (160 cercle, 188 mi-distance, 0 sans shot_y) ; 442 tirs au cercle, dont 129 exclus faute de relevé Deux points au jour ou à la veille (4 matchs perdus). Deux points à une décimale pour 246 tirs sur 313 ; 14 joueurs, Deux points de 34 à 75.

**Source** : `python -I pipelines/etudes/tirs_cercle_deux_points_v4_amical.py` ; contrôle `sql.py` sur les tirs du joueur 505000bf.

## Limites
- **Étiquettes biaisées** : en v4 amical, aucun raté n'a de `shot_zone` (la clé n'apparaît qu'avec `shot_coords_version`, absente de ce groupe). Les 487 tirs étiquetés sont tous des réussis, et les 348 ratés sont tous classés par shot_y. Le seuil Y0 et ses 97,7 % d'exactitude sont mesurés sur des réussis seulement. Si un raté au cercle est enregistré à une autre coordonnée qu'un réussi, la classification est fausse pour les ratés, et la pente change avec elle.
- **Confusion probable** : l'identité du joueur et le type de tir (dunks, rebonds offensifs convertis par les intérieurs les mieux notés). Il n'y a que 14 joueurs, donc l'effet est surtout un effet entre joueurs. Exemple : 505000bf (Deux points 65) a 26 réussis sur 26 dans l'échantillon. Il a 7 ratés classés au cercle, mais tous dans des matchs sans relevé de compétence. L'exclusion par relevé n'est donc pas neutre.
- Y0 reste fixe dans le bootstrap : son incertitude n'est pas propagée.
- Hypothèse : les ratés au cercle ont le même shot_y que les réussis au cercle. Les ratés étiquetés `paint`/`mid` des groupes plus récents permettraient de la confirmer ou de l'infirmer.

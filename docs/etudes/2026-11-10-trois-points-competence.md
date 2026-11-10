# Réussite à 3 points et compétence Trois points (BasketVibe, 2026-11-10)

**Question** : variation de la probabilité de réussite d'un tir à 3 points de nos joueurs par +10 points de compétence Trois points.
**Mesure** : unité = tir à 3 points tenté par un de nos joueurs (réussi `fg3` ou raté `miss_fg` à 3 points, contrés exclus) ; exposition = compétence Trois points du relevé du jour ou de la veille (`three_point_exact` si présent, sinon `three_point`) ; pente d'un modèle linéaire de probabilité, en points de pourcentage par +10. Effet minimal qui compterait : 3 points de pourcentage par +10.
**« Sur l'ensemble de nos matchs »** mélangerait les versions du moteur : découpé par groupe, aucun chiffre global.

| groupe | n tirs (avec relevé / total) | n matchs | estimé /+10 | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|
| v3 ligue | 127 / 734 | 5 | +6,2 pts | - | - | indéterminé : n trop petit (< 8 matchs) |
| v3 amical | 0 / 30 | 0 | - | - | - | donnée absente (aucun relevé de compétences) |
| v4 ligue | 125 / 125 | 4 | +2,3 pts | - | - | indéterminé : n trop petit (< 8 matchs) |
| v4 coupe | 55 / 55 | 2 | -1,9 pts | - | - | indéterminé : n trop petit (< 8 matchs) |
| v4 amical | 355 / 459 | 12 | +1,9 pts | [-5,6 ; +8,5] | bootstrap par grappes de matchs, 2000 tirages, graine 20261110 | indéterminé : n trop petit |
| v5 amical | 423 / 423 | 12 | +1,2 pts | [-1,5 ; +4,0] | bootstrap par grappes de matchs, 2000 tirages, graine 20261110 | indéterminé : n trop petit |

n requis (approximation : erreur type = largeur de l'IC / 3,92, supposée proportionnelle à 1/racine du nombre de matchs, puissance 50 %) :
- v5 amical (erreur type ≈ 1,4 pt) : à l'estimé actuel (+1,2), environ 12 × (1,96 × 1,4 / 1,2)² ≈ 63 matchs. La borne haute (+4,0) indique déjà qu'un effet supérieur à 4 pts/+10 est peu compatible avec ce groupe.
- v4 amical (erreur type ≈ 3,6 pts) : environ 66 matchs pour un effet de 3 pts, environ 165 à l'estimé actuel (+1,9).

## Sources
- `python -I pipelines/etudes/trois_points_competence.py 2000 20261110` (script `pipelines/etudes/trois_points_competence.py`, s'appuie sur `charger()`/`preparer()` de `pipelines/etude_evenements_basketvibe.py`).
- Recoupement `sql.py` : tirs à 3 points nôtres en amical après le 10/10 : 459 tirs, 16 matchs (v4 amical) ; 423 tirs, 97 réussis, 12 matchs (v5 amical) ; cohérent avec le script (réussite brute v5 0,229).

## Limites
- Association, pas cause. Confusion principale : la compétence varie presque uniquement **entre** joueurs (intra-joueur : étendue de 0 à 4 points) ; la pente mêle donc la compétence et tout ce qui distingue les joueurs (poste, distance des tirs, consignes de tir, minutes, compétences colinéaires). La variante intra-joueur calculée par le script est inexploitable (variance quasi nulle).
- En amical, adversaires de niveau variable ; un joueur porte 133 des 423 tirs en v5 amical et pèse lourd.
- Modèle linéaire de probabilité : pente moyenne sur l'étendue observée (23 à 72), pas une courbe.
- Relevés à l'entier pour une partie des tirs (v4 ligue : aucun à une décimale).
- Hypothèse : la compétence affichée est celle utilisée par le moteur le jour du match ; serait infirmée si le relevé de la veille diffère du jour pour des joueurs en progression.

## Export demandé
Pour comprendre le Match Engine, j'ai besoin de : exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match, parce que les tirs à 3 points de v3 ligue (607 sur 734) et de v3 amical (30 sur 30) n'ont pas de relevé `three_point` du jour ou de la veille.

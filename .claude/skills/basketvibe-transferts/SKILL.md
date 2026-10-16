---
name: basketvibe-transferts
description: Règles BasketVibe du marché des transferts — mise en vente (durée, taxe de 5 %, délai d'une semaine, minimum de 8 disponibles), libération, enchères (enchère maximale automatique, paliers, prolongation anti-snipe, phase finale à l'aveugle, prix final), joueurs libres, tests de potentiel, visibilité des compétences. À charger pour acheter, vendre, fixer une enchère maximale ou juger un prix.
---

# BasketVibe — transferts

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide (lu le 2026-10-16). **[Obs]** = nos données.

## Vendre [M§11.1]
- Mise en vente depuis la fiche du joueur, avec un prix minimum facultatif. **Enchère d'environ 2 jours**, impossible à annuler.
- Le vendeur reçoit **95 % du prix final** (taxe de 5 %) ; l'acheteur paie 100 %.
- Joueur acheté (ou joueur libre signé) : **une semaine au club** avant de pouvoir le revendre. Ne s'applique pas aux joueurs de départ ni aux juniors de l'académie.
- **Au moins 8 joueurs disponibles en permanence** (actifs et pas en vente). Pour vendre ou libérer, il faut en avoir 9 avant l'action.
- Sans enchère : le joueur reste au club.
- Libérer un joueur : il quitte l'effectif et la masse salariale, sans indemnité, et n'est pas remis automatiquement sur le marché.

## Acheter [M§11.3]
- Le marché mondial montre tous les joueurs en vente (clubs et joueurs libres), par pages de 20. Pour chaque joueur : pays, taille, poids, expérience, **les 8 compétences exactes**, PS, temps restant, prix de départ, prix actuel.
- Joueur en vente : compétences exactes, PS et salaire visibles pendant l'enchère [M§4, §2.2].
- **Enchère maximale automatique** : on fixe un maximum secret et le jeu enchérit pour nous du minimum nécessaire. Palier minimum : de 250 jusqu'à 10 000, puis 1 000, 5 000, 10 000, et 5 % au-delà d'un million.
- Le meneur peut modifier son maximum, mais pas sous le prix actuel.
- **Anti-snipe** : une enchère dans les 3 dernières minutes repousse la fin de 3 minutes (répétable).
- **Phase finale à l'aveugle** : si l'enchère est encore ouverte 15 minutes après l'heure de fin initiale, le prix affiché se fige pendant 5 minutes. Chaque club soumet une offre finale secrète. Le meneur ne peut pas descendre sous son maximum.
- **Prix final** : le plus petit des deux montants entre le maximum du gagnant et ce qu'il faut pour battre le deuxième maximum.
- La somme de tes maximums en cours ne peut pas dépasser ton solde ; un maximum en tête bloque l'argent jusqu'à la fin de l'enchère [M§10.3].
- **Tests (25 000)**, une fois par club et par mise en vente : potentiel révélé en catégorie Low, Decent ou High pendant l'enchère.
- Après achat, la fiche du joueur montre aussi ses progressions passées dans d'autres clubs humains [M§4].

## Joueurs libres [M§11.4]
- **3 nouveaux par jour de match.** Enchère de départ à **10 000**, d'environ 2 jours, mêmes règles.
- Généralement **24–33 ans**, compétences moyennes ; aucun historique de match dans ce monde.
- Sans enchère : ils quittent le marché. L'argent ne va à aucun autre club.

## Points de règle utiles pour juger un achat
- Le salaire dépend de la **moyenne des 8 compétences** (barème dans basketvibe-economie). Un joueur fort coûte donc aussi en salaire chaque semaine [M§10.2].
- Valeur sportive : le PS dépend du poste (poids dans basketvibe-joueurs), mais en match seuls comptent l'emplacement et la taille [M§2.2, §6.2].
- Âge : 0 progression à partir de 30 ans, déclin à partir de 31, retraite à la fin de la saison des 38 ans [M§8.5].
- TS = moyenne des 8 meilleurs PS : une recrue ne fait monter le TS que si elle entre dans ce top 8 [M§2.2].

## Lecture de nos données
- `silver.bv_transfer_auctions` : joueurs vus sur le marché (compétences, PS, prix de départ et actuel, nombre d'enchères).
- `silver.bv_transfers` : transferts conclus (prix, âge, poste, clubs) issus de l'historique global, de la ligue et du club.
- [Obs 2026-10-16] Historique global : 1 231 transferts au total. On ne remonte pas le passé : on accumule chaque lundi (page 1 de l'historique global + marché). À terme, croiser `bv_transfer_auctions` (compétences) et `bv_transfers` (prix payé) sur `player_id` donnera la référence de prix.

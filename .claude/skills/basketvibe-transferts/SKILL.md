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
- **Tests (25 000)** : payés **une fois par club et par joueur** tant que l'enchère est ouverte ; une remise en vente ne refacture pas ; le résultat (Low / Decent / High, jamais le nombre exact) **reste sur le profil**, même après la vente ou un changement de club [M§11, lu 2026-10-23 via résumé, pas mot pour mot]. Il faut un solde positif qui couvre les frais. Un test sur un joueur de son propre club n'est plus nécessaire : le potentiel s'affiche (voir basketvibe-communaute) [News 2026-10-20]. ⚠️ Remplace « une fois par club et par mise en vente » (lecture du 2026-10-16).
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

## À surveiller / avis (hors règles du manuel)
- **Taxe dégressive à l'étude** : idée **proposée par un joueur** (« feature request »), que le dev dit devoir trancher : 1re semaine bloquée, puis 20 % la 2e semaine, 15 % la 3e… jusqu'à 5 % ; non décidée, ne pas en tenir compte avant une News [Dev 2026-10-22, economy ; message relu en base le 2026-10-23]. Pas de limite du nombre de transferts [Dev, aucune annonce]. Le dev pourrait aussi relever le prix du test de potentiel si l'argent circule trop [Dev 2026-10-19, general, d'après la veille ; non recoupé mot pour mot].
- Un joueur « 2 étoiles » de potentiel 7 progresse presque comme un 8 (×1,50 contre ×1,60 [M§8.3], −6 %) mais se vend nettement moins cher : cible d'achat à valeur [Com 2026-10-14, dcarra, italia ; calcul sur M§8.3] (avis). Le scouting sur le marché rend les 3 étoiles très chers et les 2 étoiles moins chers [Com 2026-10-16, sakota0, portugal] (avis).
- Prix constatés dans nos données (`gold.bv_market_price_known`, 89 ventes du 2026-10-16 au 2026-10-22, lu le 2026-10-23) : maximum **2 894 063** (SF 17 ans, PS 49,7, départ 2 500 000, le 21/10) ; 3 ventes ≥ 2 M, toutes de 16–17 ans ; 18 ventes ≥ 1 M. Les records de 3,5 M cités par la communauté (voir basketvibe-communaute §6) **ne sont pas dans cette vue** (fenêtre trop courte).

## Lecture de nos données
- `silver.bv_transfer_auctions` : joueurs vus sur le marché (compétences, PS, prix de départ et actuel, nombre d'enchères).
- `silver.bv_transfers` : transferts conclus (prix, âge, poste, clubs) issus de l'historique global, de la ligue et du club.
- [Obs 2026-10-16] Historique global : 1 231 transferts au total. On ne remonte pas le passé : on accumule chaque lundi (page 1 de l'historique global + marché). À terme, croiser `bv_transfer_auctions` (compétences) et `bv_transfers` (prix payé) sur `player_id` donnera la référence de prix.

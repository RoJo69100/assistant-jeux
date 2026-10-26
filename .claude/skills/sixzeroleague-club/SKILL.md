---
name: sixzeroleague-club
description: Règles Six Zero League (handball) du club — finances (solde, semaine de 2 journées, billetterie, salaires fixés entre les saisons), sponsor (3 offres, fixe, prime de victoire, prime de signature, changement une fois par saison), marché des transferts (frais, paliers, minimum, libération, règlement toutes les 2 journées), infrastructures (Arena, Training Facilities, Youth Academy, Fan Shop, niveaux 1–20, entretien, rentabilité), onglets de l'équipe. À charger pour toute question d'argent, d'achat, de vente ou d'investissement.
---

# Six Zero League — club : finances, sponsor, transferts, infrastructures

Sources : **[W:Rubrique]** = wiki officiel, lu le 2026-10-18 (voir sixzeroleague-match). Monnaie : euros entiers.

## Finances [W:Finances]
| Élément | Valeur |
|---|---|
| Solde de départ | 25 000 € |
| Semaine financière | 2 journées de ligue terminées (même cycle que l'entraînement, les blessures et les transferts) |
| Billetterie de base | 900 € par match à domicile (× multiplicateur de division ; l'Arena ajoute de l'argent [W:Infrastructure]) |
- Le rapport hebdomadaire totalise recettes et dépenses ; il ne tourne que pendant une saison de ligue.
- **Recettes** : billetterie des matchs à domicile, sponsor, transferts nets (si on a plus vendu qu'acheté), boutique (Fan Shop), primes [W:Competitions].
- **Dépenses** : **salaires (le poste principal)**, fixés selon le niveau de chaque joueur et **modifiés seulement entre les saisons** (les progrès de l'entraînement augmentent la masse salariale de la saison suivante) ; transferts nets, frais de mise en vente, entretien des infrastructures, formation de rôle.
- Un club neuf a des salaires un peu au-dessus de sa billetterie : **perte hebdomadaire jusqu'à la signature d'un sponsor**. Être à court d'argent n'a pas encore de pénalité, mais un solde sain permet d'acheter et d'absorber la hausse des salaires.

## Sponsor [W:Sponsors]
- Un sponsor principal, choisi parmi **3 offres** (onglet Finances du Club), chacune avec ses montants.
- Une offre paie : un **fixe hebdomadaire**, une **prime par victoire de ligue** dans la semaine, et une **prime de signature** versée aussitôt. Les 3 offres équilibrent ces montants différemment, sans étiquette « sûre » ou « risquée ».
- **Premier sponsor : à signer à tout moment**, même en cours de saison. Changer ensuite : **une fois par saison, entre deux saisons seulement**.
- Montants multipliés par la division ; entre deux saisons, les offres sont calculées pour la division de la saison suivante, et un contrat existant est réévalué si le club change de division.

## Marché des transferts [W:Transfers]
| Élément | Valeur |
|---|---|
| Marché | Unique et mondial ; on peut acheter et vendre même hors saison |
| Prix de départ minimum | 1 000 € |
| Frais de mise en vente | 500 €, **prélevés tout de suite, non remboursés** si le joueur n'est pas vendu |
| Frais de libération | 500 € |
| Palier d'enchère | 1 000 € |
| Effectif | 7 minimum, 30 maximum |
| Règlement | **Toutes les 2 journées de ligue**, pour toutes les annonces en même temps |
- Vendre : bouton Sell sur la fiche, prix de départ. En vente, le joueur porte un badge € et **ses compétences deviennent visibles de tous**. Un joueur qui a annoncé sa retraite ne peut pas être vendu.
- Libérer : départ définitif, 500 € ; petite chance qu'il réapparaisse comme joueur libre à 0 € (perdu si personne n'enchérit). Un joueur retraité ne revient jamais.
- Enchères : la 1re = prix de départ ; chaque suivante +1 000 € et prend la tête. Impossible d'enchérir sur son joueur ou contre soi-même. **Pas d'enchère maximale automatique** décrite : chaque enchère est manuelle.
- Impossible de vendre ou libérer pendant un match de ligue de son équipe (enchérir reste possible).
- Règlement : le plus offrant paie et prend le joueur ; une annonce invendue revient au club (un joueur libre invendu disparaît). Marché brièvement fermé pendant le règlement. Historique dans l'onglet Transfer history.

## Infrastructures [W:Infrastructure]
| Installation | Effet |
|---|---|
| **Arena** | Ajoute de l'argent à la billetterie de chaque match à domicile, de plus en plus avec le niveau |
| **Training Facilities** | Augmentent la progression hebdomadaire de l'effectif ; ouvrent les emplacements de formation de rôle (niveaux 5, 10, 15, 20) |
| **Youth Academy** | Meilleurs prospects U18 et meilleur scouting ; à partir du niveau 5, petite chance de prospect étranger |
| **Fan Shop** | Revenu chaque semaine, selon le classement en ligue (plus haut = plus d'argent) |
- Niveaux 1 (départ) à 20. Niveau 1 : entretien gratuit. Au-dessus, entretien payé sur le cycle de 2 journées (ligne Maintenance).
- **Arena et Fan Shop sont les deux seules qui rapportent** : le revenu monte avec le niveau, mais le coût d'amélioration monte plus vite. Les premiers niveaux se remboursent en quelques mois, les derniers en années. **Chaque carte affiche le nombre de semaines pour rembourser l'amélioration suivante.**
- Amélioration : coût payé tout de suite, très croissant ; rétrogradation possible dès le niveau 2. Démolir coûte aussi et n'est jamais remboursé (seule raison : réduire un entretien qu'on ne peut plus payer). À tout moment, en saison ou non.
- Coûts et entretien multipliés par la division, comme les revenus : une installation coûte toujours la même part de ce qu'on gagne.

## Onglets de l'équipe [W:Team]
Players (effectif, fiche de chaque joueur) · Tactics (composition par défaut : les 7 de chaque match, et un remplaçant par rôle [W:Injuries]) · Training (intensité et focus) · U18 (académie) · Transfer history.

## [Obs] Nos données
- Le 2026-10-18 : solde affiché 7 177 € (en-tête des pages). API : `/api/finances/mine`, `/api/infrastructure/mine`, `/api/transfers` (marché), `/api/teams/mine/transfers`.

## [Veille 2026-10-26] Mises à jour (V-20261026-17, -18)
- Rendement du Training Facilities : **×1,30 au niveau 6, ×1,36 au 7, ×1,42 au 8, ×1,54 au 10, ×2,14 au 20 : +0,06 par niveau** (linéaire) ; emplacements de formation de rôle : 1 aux niveaux 6 à 8, 2 au niveau 10, 4 au niveau 20. ⚠️ Le +0,04 par niveau de Gazelle (D:L250-251, « si je ne me trompe pas ») est contredit par nos données (+0,06). [Obs SQL 2026-10-26, `silver.sz_infrastructure_levels.effect_label` ; V-20261026-17]
- Arena niveau 20 : **+10 050 € par match à domicile** en 5e division (×1) ; Fan Shop niveau 9 : +938 à 2 144 €/semaine selon la place, niveau 10 : +1 120 à 2 560 (coût 5 400, entretien 230). **`upgrade_cost_from_current` est cumulé** : depuis le niveau 5, la Youth Academy coûte 5 200 (niv. 6), 11 400 (7), 18 900 (8), 27 900 (9), 38 600 (10) au total ; entretien par cycle 130, 175, 230, 295, 370, 455. À confirmer à l'écran Infrastructure. [Obs SQL 2026-10-26 ; Dev chat D:L246-249 : Arena maximale > 9 999 ; V-20261026-18]

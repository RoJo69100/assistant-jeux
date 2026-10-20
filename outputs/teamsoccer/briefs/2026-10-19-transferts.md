# Team Soccer — Transferts, brief du 2026-10-19 (soir)

Données : annonces relevées le 2026-10-19 19:07-19:08 UTC (`silver.ts_transfer_listings`, 72 annonces : 67 banque, 5 manager) ; effectif et finances du 2026-10-19 (`silver.ts_players`, `gold.ts_finance_status`, `gold.ts_squad_report`). Heures en Paris (UTC+2).

## En tête : actions

| # | Club | Action | Quand |
|---|---|---|---|
| 1 | Les deux | **Aucun achat possible** : les deux soldes sont négatifs (règle : pas d'achat à solde négatif [skill club : Finances] [F:2026-10-14 PIPO68]). | — |
| 2 | Chomelix Cows | Vendre **Louis Lefebvre** (ATT, 28 ans, OVR 58) à la banque : +838 166 $ | ce soir |
| 3 | Ben Ahmed Donkey | Vendre **Kavya Hayashi** (DEF, 28 ans, OVR 62) à la banque : +488 743 $ | ce soir (ou attendre, voir plus bas) |
| 4 | Ben Ahmed Donkey | Surveiller **Tommaso Barbieri** (MID, 22 ans, OVR 63), fin 2026-10-22 16:21 : n'enchérir que si le solde le permet à ce moment. | avant le 22/10 16:21 |

Date limite utile : l'enchère Barbieri (22/10 16:21). Rien d'autre ne presse.

## Faits (SQL)

- Soldes [`gold.ts_finance_status`, as_of 2026-10-19] : Chomelix **−185 283 $** (semaine −48 755 $, masse salariale 170 253 $, fin de saison projetée +878 706 $) ; Ben Ahmed **−112 482 $** (semaine +1 226 $, masse salariale 95 596 $, projection +413 078 $). Les deux alertes `alert_negative` sont vraies.
- Effectifs [`gold.ts_squad_report`] : Chomelix **23** joueurs (ATT 6, DEF 6, GB 4, MIL 7), Ben Ahmed **22** (ATT 6, DEF 8, GB 4, MIL 4). Limite 24, enchères comprises [skill joueurs : Effectif].
- Marché [`silver.ts_transfer_listings`] : sur 67 annonces banque, le prix demandé = la valeur (ratio moyen 1,00 pour DEF, FWD, GK ; 1,04 pour MID). Exception : Thorgan De Bruyne (MID 20 ans, OVR 74) demandé 2 034 483 $ pour une valeur de 1 044 012 $ (ratio 1,95, 7 offres, fin 21/10 13:29). Les 5 annonces manager démarrent à 1 à 41 % de la valeur, 2 ont 1 offre.
- **Ventes comparables closes : 0** (nos données ne contiennent que des annonces ouvertes, un seul relevé). Toute enchère maximale ci-dessous est donc fondée sur la valeur de la fiche, pas sur un prix de clôture observé.
- `silver.ts_my_bids` : 7 annonces (ids 391 à 872) pour Chomelix, absentes du relevé du jour (ids actuels 5228-5299). Probablement anciennes ; je ne peux pas dire si elles comptent dans la limite hebdomadaire. À vérifier dans « Your offers » du Marché.

## Règles utilisées

- Vente banque : immédiate, au prix de la fiche, sans commission. Enchère du manager : 72 h, départ ≤ valeur, vendeur reçoit 90 % [skill club : Marché] [F:2026-10-18 Admin-Dev].
- Achat : 1 par semaine (enchères en tête comptées), remise à zéro lundi 00:00 Canaries ; effectif ≤ 24 ; revente interdite 7 semaines [G:Limites hebdomadaires de transferts].
- Nouveau joueur : Forme 85 au départ [skill joueurs : Forme]. La Forme affichée dans l'annonce (30 à 100) n'est donc pas un critère d'achat.
- Salaire ≈ 1 % de la valeur par semaine [skill joueurs : Valeur et salaire, Obs]. Un solde bas coûte des points de moral [skill club : Finances].
- Valeur de la fiche : change au plus tous les 7 jours [G:Valeur des joueurs].

## Achat : annonces intéressantes (avis)

Aucun achat avant retour du solde au positif. Annonces à suivre, par besoin :

**Ben Ahmed — milieu (besoin C-006 : un vrai MC, Conduite ≥ 70, OVR ≥ 64).** Seulement 4 milieux dans l'effectif, dont le meilleur a OVR 64.
- **Tommaso Barbieri** (liste 5288, banque, MID 22 ans, OVR 63, Contrôle 75, Conduite 69, Endurance 72, Vitesse 72, Défense 62), prix 534 534 $ (= valeur), 0 offre, fin 22/10 16:21. Il remplacerait Uchenna Kumar (OVR 63, 24 ans, valeur 385 868 $, 3 matchs). Légèrement sous le critère de C-006 (Conduite 69, OVR 63). Prix pas bon marché : des milieux OVR 63-64 de l'effectif valent 386 000 à 405 000 $ (`silver.ts_players`), soit environ 30 % de moins. Verdict : **prix correct à cher, intérêt modéré**.
  - **Enchère maximale conseillée : 534 534 $ (la valeur, sans prime)**. Base : prix de la fiche, 0 vente comparable close. Confiance faible. Coût total : 534 534 $ + salaire ≈ 5 345 $/semaine (1 % de la valeur) soit environ 37 000 $ sur les 7 semaines restantes de saison, soit ≈ 572 000 $.
  - Le solde prévu fin de saison (+413 078 $) ne finance pas cet achat seul ; il faudrait la vente de Hayashi (+488 743 $) et un solde positif au moment de l'enchère. Inconnu : si un joueur masculin peut rejoindre l'équipe féminine (rien dans les skills) ; à vérifier sur la page Marché avant d'y compter.
- Thorgan De Bruyne (MID 20 ans, OVR 74, Conduite 93) : **cher** (2 034 483 $ pour une valeur de 1 044 012 $), 7 offres. Ne pas suivre.
- Simone Rossi (MID 29 ans, OVR 64, valeur 1 367 407 $) : cher pour OVR 64 et 29 ans. Ne pas suivre.

**Ben Ahmed — défense** : Valentina Ferreira (DEF 19 ans, OVR 80, Défense 100, Contrôle 100) à 1 600 026 $, fin 22/10 17:07 : +16 OVR sur le meilleur défenseur actuel (64). Intérêt sportif réel, mais 1,6 M$ hors de portée (salaire ≈ 16 000 $/semaine, x2,5 le salaire moyen) ; achat unique de la semaine mieux employé sur un milieu (C-006). Pas d'enchère conseillée.

**Chomelix** : aucun besoin clair. Gardiens du marché : OVR 52 au maximum (9 annonces) contre 60 chez Romain Thomas. Défense : Ounahi 90 déjà. Rien à acheter.

## Vente (avis)

Règle de calcul : la banque paie 100 % de la valeur tout de suite ; l'enchère du manager rapporte 90 % du prix final, donc ne bat la banque que si le prix final dépasse 111 % de la valeur. Aucune vente manager close observée (0 comparable), et nos 5 annonces manager vues démarrent à 1-41 % de la valeur. Pour des joueurs à 500 000 à 840 000 $, **banque**.

| Club | Joueur | Âge / OVR | Valeur | Salaire/sem | Gain net (banque) | Effet masse salariale | Raison |
|---|---|---|---|---|---|---|---|
| Chomelix | **Louis Lefebvre** (ATT) | 28 / 58 | 838 166 $ | 8 382 $ | **+838 166 $** | 170 253 → 161 871 $ (−4,9 %) | 5e attaquant (Moreau 70, Bonnet 67, David 65, É. Roux 63 devant), 0 match officiel, valeur au plus haut ; ramène le solde à ≈ +652 883 $ |
| Ben Ahmed | **Kavya Hayashi** (DEF) | 28 / 62 | 488 743 $ | 4 887 $ | **+488 743 $** | 95 596 → 90 709 $ (−5,1 %) | 8 défenseurs pour 4 postes, 2 matchs ; ramène le solde à ≈ +376 261 $ |

- Effectif après vente : Chomelix 22 (min 16), Ben Ahmed 21. Pas de contrainte de revente (les 7 semaines ne visent que les joueurs achetés).
- Bon moment : **maintenant**, car la banque paie immédiatement et le solde négatif bloque les achats et pèse sur le moral. Aucune raison de garder Lefebvre pour une fin de saison : il ne joue pas. La valeur peut changer au plus tous les 7 jours ; je n'ai pas la date de la dernière révision, donc je ne peux pas prédire sa direction.
- Pour Ben Ahmed : Hayashi ne vaut le coup de la vente que si on veut acheter (Barbieri) ; sinon garde-la. La projection de fin de saison est positive (+413 078 $) et la semaine est à +1 226 $, mais la date du retour au positif n'est pas calculée.
- Non conseillé : vendre Pierre Leroy (DEF, 32 ans, 349 144 $), le remplaçant défensif nommé dans C-003 ; ni les jeunes de 14-16 ans (valeurs 188 000 à 511 000 $), progression non évaluée ici (skill entraînement non listé dans la fiche).

## Limites de ce brief

- Un seul relevé : pas d'historique de prix, pas de vente close ; enchères maximales à confiance faible.
- Le retour au positif du solde n'est pas daté (pas de vue qui le calcule) ; l'effet de la billetterie sur le solde est reporté au traitement du lundi 00:05.
- Export utile avant le 22/10 : page Marché (rafraîchir les annonces closes et « Your offers »), pour obtenir de vrais comparables.

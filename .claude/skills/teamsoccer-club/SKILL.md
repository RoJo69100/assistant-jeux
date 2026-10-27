---
name: teamsoccer-club
description: Règles Team Soccer (football) du club — finances (1 000 000 $ au départ, semaine close le lundi 00:05, recettes et dépenses, solde négatif), salaires, stade (80 000 places, 4 types de places, prix d'achat, prix des billets, entretien de 6 %), affluence selon division et classement, marché (vente à la banque, enchères de manager de 72 h avec 10 % de commission, enchères de la banque, limite d'un achat par semaine, revente bloquée 7 semaines), équipes secondaires et Premium. À charger pour toute question d'argent, de stade, d'achat ou de vente.
---

# Team Soccer — finances, stade, marché

Sources : voir teamsoccer-joueurs (**[G]** guide officiel capté le 2026-10-19, **[F]** forum global, **[P]** page du jeu, **[Obs]** nos données). Monnaie : $ (la page Stade affiche €, même monnaie).

## Finances [G:Finances] [P:Finances]
- 1 000 000 $ au départ (et à chaque nouveau club). La semaine financière est **remise à zéro chaque lundi à 00:05** (heure du site).
- **Recettes** : billetterie des matchs à domicile (et amicaux), ventes de joueurs, primes de compétitions, autres. Le guide : « on ne gagne des $ que de 2 façons : vendre des joueurs à la banque et la billetterie » (les primes s'y ajoutent depuis la saison 2). Pas de sponsor : refusé par l'admin [F:2026-05-05 Admin-Dev].
- **Dépenses** : salaires (`Wages`), entretien du stade, achats, construction du stade, personnel (entraîneur), autres.
- **Solde négatif** : pas de faillite ni de renvoi ; on ne peut simplement plus acheter de joueur, agrandir le stade ni améliorer l'entraîneur tant que l'argent manque [F:2026-05-05 Admin-Dev] [F:2026-10-14 PIPO68]. Mais un solde bas coûte des points de moral (cercle jaune, voir teamsoccer-match).
- **Salaires** : environ 1 % de la valeur du joueur par semaine [Obs], ligne principale des dépenses.
- Bugs d'entretien constatés : le traitement du lundi a facturé l'ancienne formule (capacité × 5 $) au lieu de 6 % ; remboursé et +500 000 $ à tous le 2026-10-13, réapparu et remboursé le 2026-10-19 [F:2026-10-13, 2026-10-19 PIPO68]. **Contrôler la ligne « stadium maintenance » chaque lundi.**
- [Obs] Au 2026-10-19 : Ben Ahmed Donkey (féminine) solde −112 482 $, dépenses de la semaine 115 620 $ (salaires 95 596, entretien 20 024), bilan cumulé −852 719 $. L'autre club : −185 283 $.

## Stade [G:Stades et spectateurs] [P:Stade]
| Type | Prix d'achat par place | Recette par match et par place occupée | Maximum |
|---|---|---|---|
| Debout (stands) | 80 $ | 7,50 $ | 50 000 |
| Places basiques | 150 $ | 15 $ | 20 000 |
| Places couvertes | 300 $ | 27,50 $ | 9 500 |
| VIP | 1 500 $ | 75 $ | 500 |
- Capacité maximale 80 000. Chaque type a son propre plafond [F:2026-07-17 PIPO68].
- **Prix des billets** : ceux-ci depuis le 2026-09-18 (« Important change in ticket prices ») ; avant : 10 $ uniques (BETA) puis 15/30/55/150 (juin). Amicaux : un quart du prix (1,875 / 3,75 / 6,875 / 18,75 $) [G].
- **Entretien = 6 % de la recette potentielle d'un match à guichets fermés**, prélevé chaque semaine [F:2026-10-13 PIPO68] [Obs : 6 % × 333 725 $ = 20 024 $]. Le chiffre des Finances en fin de saison est un cumul [F:2026-09-29 PIPO68].
- **Rentabilité d'une place** (déduction) : prix ÷ (recette × taux d'affluence × 0,94) en matchs à domicile. Debout, basique, couverte : ~10,7 / 10 / 10,9 matchs à 100 % d'affluence ; VIP : 20. En division V au 5e rang (35 %), environ trois fois plus. Une saison compte 7 matchs de ligue à domicile (plus les amicaux à domicile, à un quart du prix).

### Affluence [G:Stades et spectateurs]
Pourcentage de la capacité rempli selon la division et le rang au classement (ligue de 8) :
| Rang | Div I | Div II | Div III | Div IV | Div V |
|---|---|---|---|---|---|
| 1 | 100 | 90 | 80 | 70 | 60 |
| 2 | 90 | 80 | 70 | 60 | 50 |
| 3 | 85 | 75 | 65 | 55 | 45 |
| 4 | 80 | 70 | 60 | 50 | 40 |
| 5 | 75 | 65 | 55 | 45 | 35 |
| 6 | 70 | 60 | 50 | 40 | 30 |
| 7 | 65 | 55 | 45 | 35 | 25 |
| 8 | 60 | 50 | 40 | 30 | 20 |
- Le même pourcentage s'applique à chaque type de place [F:2026-09-01 PIPO68]. Exemple de l'admin : 2 500 places, Div I, 3e → 85 % → 2 125 spectateurs [F:2026-05-13 Admin-Dev].
- Idole ou Magique dans l'effectif : affluence ×1,5 à domicile (voir teamsoccer-joueurs).
- **Coupes officielles** (terrain neutre) : billetterie partagée 50/50. **Amicaux** : prix amicaux, partagés 50/50. Seuls les matchs dans son stade rapportent la recette hebdomadaire.
- Le « fan club » est le nombre de managers qui suivent ou visitent le club : aucun lien avec l'affluence [F:2026-09-07].

## Marché des transferts
### Vendre : deux systèmes depuis le 2026-10-18 [F:2026-10-18 Admin-Dev] [G:Valeur des joueurs]
1. **Vente à la banque TeamSoccer** : immédiate, **au prix de la fiche**, sans commission. La banque remet ensuite le joueur aux enchères ; s'il ne trouve pas preneur, il disparaît du jeu.
2. **Enchère du manager** (bouton « Mettre aux enchères ») : **72 heures**, prix de départ fixé par le vendeur **au plus égal à la valeur de la fiche**. Sans enchère, le joueur revient gratuitement. Vendu : l'acheteur paie l'enchère finale, le vendeur reçoit **90 %** (10 % de commission). Impossible d'annuler une fois une offre reçue ; ni le vendeur ni ses autres clubs ne peuvent enchérir.
- Ventes illimitées pour tous [F:2026-09-11 Admin-Dev].

### Acheter [G:Limites hebdomadaires de transferts] [F:2026-10-18 Admin-Dev]
- Enchères sur la page Marché (« Your offers » regroupe les joueurs suivis). **+2 minutes de prolongation** si une offre arrive à la fin.
- **Limite d'achat** : compte de 30 jours ou moins = illimité ; au-delà, **1 achat par semaine, les enchères en tête comptent**. Remise à zéro le lundi 00:00 (heure Atlantique/Canaries).
- **Revente interdite pendant 7 semaines** après un achat. Effectif entre 16 et 24, enchères en cours comprises ; budget suffisant exigé (solde négatif = pas d'achat).
- Joueurs libres : ajoutés par le site à intervalles réguliers depuis le 2026-07-18, au prix réel [F:2026-07-18, 2026-07-19 Admin-Dev].
- En vente, les compétences du joueur sont visibles (on peut juger son OVR et sa valeur avant d'enchérir).
- [P:Marché] Au 2026-10-19 : environ 55 annonces ; prix de départ de 50 645 $ (OVR 31, 16 ans) à 2 034 483 $ (OVR 85, 20 ans).

## Équipes secondaires et Premium [G:Vente de clubs] [F:2026-05-31, 2026-10-19]
- Un club de base (invendable) ; équipes secondaires achetables (pays ou ligues différents), chacune avec **sa propre économie**, revendables à la banque contre des TSCredits (1 TSC pour 20 000 $).
- L'abonnement Premium annuel donne une équipe féminine (Women's TS League) et l'accès à la Superligue Utopia ; même date d'expiration que le Premium.
- Premium : flèches de progression, vitrine de trophées, changement d'horaire des matchs, 5 compositions par défaut, tournois personnalisés.
- Compte inactif 45 jours → le club devient BOT [F:2026-08-29 PIPO68].
- V-20261019-2 : équipe supplémentaire achetée à part dans la boutique [FAQ Team Soccer, export du 2026-10-19] ; la section Premium liste les pays disponibles, avec « Renouveler +1 an » : abonnement annuel par pays [F:2026-06-29 Admin-Dev]. Tout renouvellement Premium garde la même date d'expiration sur l'équipe première et l'équipe féminine [FAQ]. Prix absents de nos sources. Annonces Premium : mode texte des compétences (101, 2026-09-14), générateur de défis amicaux avec amical contre un BOT (113, 2026-10-07).
- V-20261019-10 (marché) : plafond de 24 joueurs : à 24 aucune signature ; à 16 aucune vente. Refus d'achat fréquents : achat de la semaine utilisé, effectif qui atteindrait 25 avec les enchères actives, budget insuffisant. Une offre de dernière seconde prolonge l'enchère [FAQ]. ⚠️ L'annonce 99 (2026-09-10) parle de « acheter et vendre un joueur par semaine » ; la FAQ et Admin-Dev [F:2026-09-11] disent que les ventes sont illimitées : garder « ventes illimitées ».

## [Obs] Nos données
- API : `team_finances` (lignes de la semaine et cumuls), `stadiums` (places par type), `transfer_listings` (prix, offres, échéance, type d'annonce), `players.value` et `players.wage`.

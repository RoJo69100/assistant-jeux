# Priorités pour faire progresser les clubs

Sources : skills teamsoccer-joueurs, -match, -entrainement, -club, -saison ; briefs du 2026-10-19 et 2026-10-20. L'ordre est un **avis** : du moins cher au plus cher, et de l'effet le plus sûr au moins sûr.

## 1. La Forme avant tout (gratuit, effet certain)
- Chaque action d'un joueur est multipliée par **0,70 + 0,30 × Forme / 100** : Forme 100 → ×1,00 ; 80 → ×0,94 ; 60 → ×0,88 ; 46 → ×0,84 [F:2026-06-27 Admin-Dev]. Elle fixe aussi le plafond de fatigue en match [F:2026-10-18 Admin-Dev].
- Elle ne bouge **qu'à l'entraînement du vendredi**, jamais en match [F:2026-06-30] :

| Intensité | 100 % | 90 % | 80 % | 70 % | 60 % | 50 % | ≤ 40 % |
|---|---|---|---|---|---|---|---|
| Forme | −10 | −6 | −4 | −2 | 0 | +6 | +10 |

  (30 ans et + : −2 de plus à 80–100 %.)
- **Avis** : 60 % est le point neutre ; un joueur sous 70 de Forme passe à 40 % une semaine ; les jeunes qui ne jouent pas peuvent monter à 80–100 %. C'est l'arbitrage central du jeu [F:2026-10-12 Mikizar].
- Remplacements programmés : un remplaçant entre avec tout son plafond, utile en fin de match [F:2026-10-18].

## 2. Le moral du manager (gratuit, jusqu'à +10 points de compétences)
5 cercles de 3 points, remis à zéro le lundi [G:MC] [F:2026-09-14] :
- 🔴 se connecter chaque jour (5 jours = 3) ;
- 🟠 jouer des matchs dans la semaine (amical compris, max 3) ;
- 🟡 trésorerie > 200 000 $ (1), > 1 500 000 $ (2), > 2 500 000 $ (3) ;
- 🔵 composition enregistrée + entraînement assigné + une action de marché ou d'académie ;
- 🟢 rang dans le pays.

[Obs 2026-10-20] Ben Ahmed (87 521 $) a **0 au cercle jaune** ; Chomelix (1 062 583 $) a 1. Les vrais cercles ne sont pas encore exportés (checklist B20).

## 3. Une trésorerie positive
- Pas de faillite, mais un solde négatif bloque achats, stade et entraîneur [F:2026-05-05 Admin-Dev].
- Salaire ≈ **1 % de la valeur par semaine** [Obs] : la masse salariale est la grosse dépense. Revenus : billetterie à domicile, ventes, primes [G].
- **Vendre à la banque** : immédiat, au prix de la fiche, sans commission. **Enchère du manager** : 72 h, 90 % pour le vendeur [F:2026-10-18 Admin-Dev]. **Avis** : la banque pour un joueur moyen, l'enchère pour un joueur recherché (jeune et fort).
- **Les coupes rapportent** : jusqu'à 800 000 $ en Consolation ou Masters, 500 000 $ en Coupe Nationale [G]. Les aligner sérieusement.
- Contrôler l'entretien chaque lundi (`gold.ts_finance_status.maintenance_gap`).
- [Obs 2026-10-20] Chomelix : 1 062 583 $, fin de saison projetée ~1,78 M$. Ben Ahmed : 87 521 $, ~0,61 M$ (`gold.ts_finance_status`, sans primes).

## 4. L'entraînement : bien choisir la compétence
- Une compétence et une intensité par joueur, appliquées le vendredi ; gain selon âge, intensité et niveau d'entraîneur, sans hasard [F:2026-06-19 Admin-Dev].
- Entraîner les **compétences clés du sous-rôle** (voir [profils-postes.md](profils-postes.md)) : seules les 4 compétences du calcul entrent dans l'OVR [G].
- **Le physique ne monte plus tout seul** depuis fin septembre 2026 : Endurance et Vitesse s'entraînent comme le reste [F:2026-10-09 PIPO68]. Le physique est « l'attribut le plus important » [F:2026-05-01 Admin-Dev]. **Endurance ≤ 30 : seul l'entraînement d'Endurance est possible** [P:Entraînement].
- Conseil de l'admin (avant les changements de septembre) : technique vers 70 %, une ou deux semaines physiques à 100 % de temps en temps [F:2026-05-09].
- **Entraîneur** : niveau 2 à 1 000 000 $, puis 4, 10 et 25 M$, un niveau à la fois [F:2026-09-18]. Nos deux clubs sont au niveau 1. Brief finances du 19/10 : Chomelix peut monter au niveau 2 **après la clôture du 02/11**, si le solde est confirmé.
- La progression réelle se mesure dans `gold.ts_player_progress` à partir du 2e relevé du vendredi (checklist C27).

## 5. Le stade : seulement quand il y a de la marge
- Une place se rembourse en ~10–11 matchs à domicile à 100 % d'affluence (VIP : 20) ; l'affluence dépend de la division et du rang [G:Stades]. Calcul par club : `gold.ts_stadium_payback`.
- [Obs 2026-10-20] Chomelix (Div I, 3e, 85 %) et Ben Ahmed (Div III, 1er, 80 %) : 5 matchs de ligue à domicile restants, donc aucune place remboursée cette saison.
- **Avis** : acheter des places de préférence en **début de saison** (7 matchs à domicile à venir) et quand l'entraîneur et l'effectif sont financés. Places basiques : meilleur ratio prix/recette.
- Un joueur Idole ou Magique dans l'effectif : affluence ×1,5 [F:2026-05-18].

## 6. L'académie : la relève gratuite
- 3 révélations par jour : commencer par les 4 compétences de poste (Gardien, Défense, Conduite, Finition) pour repérer vite un bon jeune (**avis**).
- Le niveau de l'académie monte avec le nombre de jeunes **complétés** (0, 10, 20, 35, 50, 70) et fixe le total de compétences des nouveaux jeunes (250 puis 300… 500) [F:2026-10-18 Admin-Dev]. **Avis** : compléter vite des jeunes, même moyens, puis les libérer ou les vendre, fait monter le niveau.
- Monter un jeune exige une place dans l'effectif (24 au maximum, enchères en cours comprises).
- Les talents (7 %, Magique 3 %) ne se voient qu'après la montée [F:2026-09-22].

## 7. Le marché : un achat par semaine
- 1 achat par semaine (enchères en tête comprises), revente interdite 7 semaines [G] (une revente immédiate a été vue le 19/10 : point à trancher par la Veille).
- **Avis** : n'acheter que pour un trou de l'effectif (Chomelix : gardien ; Ben Ahmed : milieux avec Conduite), avec un solde positif après réserve de deux semaines de coûts fixes.

## 8. HPC : décision de l'utilisateur
50 TSC à investir dans la saison, sinon remboursés [F:2026-10-10]. Au 2026-10-20 : 45 TSC sur le compte, 0 investi. Monnaie Premium : je ne décide pas à ta place.

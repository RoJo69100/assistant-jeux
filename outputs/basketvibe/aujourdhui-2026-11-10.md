<!-- généré le 2026-11-10 15:52 -->
## Bloc 0 — Exports d'abord

- donnée manquante : exporte Amical : tactique du match (53 h) → bloc 2
- donnée manquante : exporte l'aperçu du match de ligue du 11/11 → bloc 3
- donnée manquante : exporte l'aperçu du match de coupe du 12/11 → bloc 3
- donnée manquante : exporte l'onglet Équipes de la ligue (dernier export il y a 600 h) → blocs 5 et 6
- donnée manquante : exporte l'onglet Joueurs de la ligue (dernier export il y a 600 h) → blocs 5 et 6
- donnée manquante : exporte l'onglet Blessés de la ligue (dernier export il y a 600 h) → blocs 5 et 6
- donnée manquante : exporte l'onglet Transferts de la ligue (dernier export il y a 600 h) → blocs 5 et 6
- Marché : 1 capture, 20 annonces vues depuis 24 h (dernière le 09/11) → bloc 4
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés d'un match vue côté adversaire (si le jeu l'affiche), parce que le `defensive_focus` adverse est absent : 0 ligne adverse sur 53 dans `silver.bv_match_tactics`, toutes les captures `match-tactics-used` ont `viewer_is_primary` = true. Hypothèse : cette page existe. Si le jeu ne la montre pas, la question 1c est hors d'atteinte. (étude du 10/11) → bloc 6
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Équipe (effectif) des clubs de tête du classement, parce que les compétences de leurs joueurs manquent : `silver.bv_player_overview` ne contient que notre équipe, et les aperçus de match ne donnent au mieux que des fourchettes (`skill_brackets`). Hypothèse : cette page montre les compétences d'un club adverse. (étude du 10/11) → bloc 6
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Entraînement chaque semaine, juste avant et juste après l'entraînement, parce que les compétences à une décimale (`*_exact`) manquent dans les relevés hebdomadaires du 01/11 et du 08/11 (0 gain calculé sur 128 et 112 lignes de `gold.bv_training_gains_exact`). Hypothèse sur le moment de l'entraînement, non vérifiée ici. (étude du 10/11) → bloc 6

## Bloc 1 — À faire aujourd'hui, puis demain

**Aujourd'hui**

| Priorité | Catégorie | Action |
|---|---|---|
| 🟧 IMPORTANT | Transferts | Acheter un SF de note ≥ 61,0 : aucune annonce au poste SF dans le Marché du 09/11 (annonces encore ouvertes de l'export) → bloc 4 |
| 🟧 IMPORTANT | Transferts | Vendre Catalin Ungureanu : économie 19 030 par semaine, remplaçant Maël Bernard au poste C, écart 0,8 → bloc 4 |
| 🟩 SUIVI | Analyse | Analyse : Dernier match exporté : 10/11 (amical, W 141-117 contre Opper Cards) → bloc 7 |
| 🟩 SUIVI | Académie/Draft | Académie, rapport du 05/11 : 3 prospects ; valeur d'un High inconnue → bloc 9 |

**Demain (préparé aujourd'hui)**

| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Amical contre Launceston Ligers (mer. 11/11) : saisis le test E1 niveau A : agressivité 3 à l'écran (cran 2, équilibrée) sur tous les joueurs → bloc 2 |


## Bloc 2 — Composition de l'amical

Amical contre Launceston Ligers (mer. 11/11), heure limite du verrou 07:45

composition de l'amical en préparation

## Bloc 3 — Composition de la ligue ou de la coupe

Ligue J5 contre BC KIT (mer. 11/11)

donnée manquante : exporte l'aperçu du match de ligue du 11/11 (bloc 3)

Coupe contre Stare Kotlety (jeu. 12/11), heure limite du verrou 20:00

donnée manquante : exporte l'aperçu du match de coupe du 12/11 (bloc 3)


## Bloc 4 — Transferts

**Table des prix (ventes conclues, par tranche d'âge et palier de note de 5)**

| Âge | Note (dès) | Ventes | Prix bas (p25) | Médian | Prix haut (p75) | Dernière vente |
|---|---|---|---|---|---|---|
| ≤21 | 25 | 3 | 1 625 | 1 750 | 5 875 | 07/11 |
| ≤21 | 30 | 6 | 438 | 1 875 | 14 188 | 07/11 |
| ≤21 | 35 | 37 | 1 500 | 13 500 | 77 000 | 08/11 |
| ≤21 | 40 | 66 | 64 500 | 277 500 | 841 250 | 08/11 |
| ≤21 | 45 | 37 | 440 000 | 721 000 | 1 543 500 | 08/11 |
| ≤21 | 50 | 9 | 1 680 000 | 3 675 000 | 5 788 125 | 07/11 |
| 22-25 | 35 | 2 | 1 050 | 1 100 | 1 150 | 08/11 |
| 22-25 | 40 | 20 | 251 | 4 375 | 31 000 | 07/11 |
| 22-25 | 45 | 32 | 10 187 | 93 888 | 201 249 | 08/11 |
| 22-25 | 50 | 17 | 500 000 | 700 000 | 910 000 | 07/11 |
| 22-25 | 55 | 22 | 1 151 875 | 1 462 043 | 1 831 580 | 07/11 |
| 22-25 | 60 | 5 | 2 333 333 | 2 500 000 | 2 635 500 | 07/11 |
| 26-29 | 35 | 8 | 75 | 625 | 3 250 | 04/11 |
| 26-29 | 40 | 20 | 1 | 875 | 13 813 | 08/11 |
| 26-29 | 45 | 43 | 751 | 10 000 | 70 000 | 08/11 |
| 26-29 | 50 | 54 | 250 000 | 507 502 | 707 500 | 07/11 |
| 26-29 | 55 | 65 | 770 000 | 999 000 | 1 300 000 | 08/11 |
| 26-29 | 60 | 21 | 1 113 525 | 1 500 000 | 1 818 390 | 07/11 |
| 30+ | 35 | 1 | 1 | 1 | 1 | 05/11 |
| 30+ | 40 | 7 | 376 | 1 000 | 1 000 | 08/11 |
| 30+ | 45 | 35 | 1 000 | 10 250 | 32 500 | 08/11 |
| 30+ | 50 | 16 | 27 750 | 61 000 | 85 750 | 04/11 |

**Qui acheter (annonces du Marché qui se terminent dans les 24 h)**

aucune annonce du Marché ne se termine dans les 24 h (export du 09/11, 20 annonces)

**Qui vendre (joueurs vendables et s'ils sont nécessaires)**

| Nom | Poste | Âge | Note | Salaire hebdomadaire | Rang au poste | Minutes (4 derniers matchs de ligue) | Remplaçant | Écart de force | Prix attendu (médiane de la case) | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Catalin Ungureanu | C | 27 | 48,5 | 19 030 | 6 (C) | 12,0 | Maël Bernard | 0,8 | 10 000 | vendable |
| Anselmo Albano | PF | 27 | 47,8 | 17 668 | 10 (PF) | 3,0 | Min-jun Dang | 0,5 | 10 000 | vendable |
| Maël Bernard | C | 18 | 47,8 | 17 303 | 5 (C) | 0,0 | Anselmo Albano | 0,1 | 721 000 | vendable |
| Nolan Baron | PG | 17 | 44,5 | 16 691 | 7 (PG) | 0,0 | Jonathan Durand | 0,3 | 277 500 | vendable |
| Léo Lefebvre | PF | 29 | 63,1 | 31 803 | 1 (PF) | 35,1 | Hadrien Gimenez | 4,2 | 1 500 000 | nécessaire (écart de force 4,2 supérieur à la tolérance 1,0) |
| Hadrien Gimenez | SF | 26 | 60,0 | 28 328 | 1 (SG) | 36,0 | Oscar Richard | 4,3 | 1 500 000 | nécessaire (écart de force 4,3 supérieur à la tolérance 1,0) |
| Oscar Richard | PG | 25 | 56,4 | 25 605 | 2 (PG) | 36,0 | Léo Lefebvre | 4,5 | 1 462 043 | nécessaire (écart de force 4,5 supérieur à la tolérance 1,0) |
| Armand Fournier | C | 28 | 52,5 | 22 846 | 3 (C) | 36,0 | Oscar Richard | 2,3 | 507 502 | nécessaire (écart de force 2,3 supérieur à la tolérance 1,0) |
| Min-jun Dang | SG | 30 | 49,9 | 20 663 | 5 (SG) | 12,0 | Naël Boyer | 2,5 | 10 250 | nécessaire (écart de force 2,5 supérieur à la tolérance 1,0) |
| Thibault Bonnet | SG | 26 | 51,8 | 20 330 | 4 (SG) | 36,0 | Min-jun Dang | 1,7 | 507 502 | nécessaire (écart de force 1,7 supérieur à la tolérance 1,0) |
| Noé Legrand | PF | 23 | 49,4 | 19 227 | 4 (C) | 19,0 | Catalin Ungureanu | 1,4 | 93 888 | nécessaire (écart de force 1,4 supérieur à la tolérance 1,0) |
| Naël Boyer | PG | 20 | 48,2 | 18 252 | 5 (PG) | 12,0 | Nolan Baron | 3,9 | 721 000 | nécessaire (écart de force 3,9 supérieur à la tolérance 1,0) |
| Jonathan Durand | SF | 25 | 43,6 | 15 928 | 10 (SG) | 3,0 | Sacha Leclerc | 2,3 | 4 375 | nécessaire (écart de force 2,3 supérieur à la tolérance 1,0) |
| Sacha Leclerc | SG | 17 | 42,3 | 13 767 | 11 (SG) | 0,0 | Nolan Baron | 1,3 | 277 500 | nécessaire (écart de force 1,3 supérieur à la tolérance 1,0) |

**Enchères, achats et ventes déjà proposés**

- Acheter un SF de note ≥ 61,0 : aucune annonce au poste SF dans le Marché du 09/11 (annonces encore ouvertes de l'export) — poste SF : profondeur 2, PS moyen 51.8
- Vendre Catalin Ungureanu : économie 19 030 par semaine, remplaçant Maël Bernard au poste C, écart 0,8 — force au poste 48,4 contre 47,6, tolérance 1,0 (core.game_params.vente_tolerance_force)


## Bloc 5 — Les meilleurs et les failles du jeu

carte de faisabilité du 10/11 : 3a force du club et victoires : faisable maintenant ; 3b pourquoi les premiers le sont (compétences, tactique) : bloquée par : exporte la page Équipe des clubs de tête

## Bloc 6 — Match Engine

matchs ajoutés : 16 (ligue 1, amical 1 ; autres clubs 14) · 88 en base · étude à jour au 10/11, 0 pas encore étudiés
Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés d'un match vue côté adversaire (si le jeu l'affiche), parce que le `defensive_focus` adverse est absent : 0 ligne adverse sur 53 dans `silver.bv_match_tactics`, toutes les captures `match-tactics-used` ont `viewer_is_primary` = true. Hypothèse : cette page existe. Si le jeu ne la montre pas, la question 1c est hors d'atteinte. (étude du 10/11)
Pour comprendre le Match Engine, j'ai besoin de : exporte la page Équipe (effectif) des clubs de tête du classement, parce que les compétences de leurs joueurs manquent : `silver.bv_player_overview` ne contient que notre équipe, et les aperçus de match ne donnent au mieux que des fourchettes (`skill_brackets`). Hypothèse : cette page montre les compétences d'un club adverse. (étude du 10/11)
Pour comprendre le Match Engine, j'ai besoin de : exporte la page Entraînement chaque semaine, juste avant et juste après l'entraînement, parce que les compétences à une décimale (`*_exact`) manquent dans les relevés hebdomadaires du 01/11 et du 08/11 (0 gain calculé sur 128 et 112 lignes de `gold.bv_training_gains_exact`). Hypothèse sur le moment de l'entraînement, non vérifiée ici. (étude du 10/11)
Avancement des expériences : E1 : 0 vérifié sur 4 ; E5 : 0 vérifié sur 3 ; E2 : 0 vérifié sur 3 ; E3 : 0 vérifié sur 7 ; E4 : 0 vérifié sur 16
prochaine hypothèse : E1 — agressivité défensive, uniforme sur nos cinq

## Bloc 7 — Analyse détaillée

défaite du 09/11 : analyse non faite, lancée dans ce passage
- Analyse : Dernier match exporté : 10/11 (amical, W 141-117 contre Opper Cards)

## Bloc 8 — Économie

carte de faisabilité du 10/11 : 2 prix : PS et âge : faisable maintenant ; 2 prix : poste : dans 334 jours ; 4a rendement d'un achat-revente (marché) : faisable maintenant ; 4b usage de notre argent et rendement : bloquée par : une seule équipe observée (aucun export connu ne la lève)
- finances : seuil non atteint (résultat hebdo estimé +98 367, la réduction de charges commence sous 0)

## Bloc 9 — Académie, personnel, entraînement

carte de faisabilité du 10/11 : 5a entraînement principal contre secondaire : faisable maintenant ; 5b personnel : bloquée par : une seule configuration observée (aucun export ne la lève) ; 5c académie : bloquée par : un seul niveau d'investissement observé (aucun export ne la lève)
- Académie, rapport du 05/11 : 3 prospects ; valeur d'un High inconnue — donnée manquante : core.game_params.academie_valeur_high

## Bloc 10 — À valider par l'utilisateur

- à valider par écrit : Vendre Catalin Ungureanu : économie 19 030 par semaine, remplaçant Maël Bernard au poste C, écart 0,8
- effectif, vendre pour profit : règle non écrite — à valider (seuil de déclenchement non validé)
- Personnel (médecin 2/2, kinésithérapeute 4/4, psychologue 2/2, marketing 0/2, semaine du 2026-11-02) : règle de personnel non tranchée, à valider


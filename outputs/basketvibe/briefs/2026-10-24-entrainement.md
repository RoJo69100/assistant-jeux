# Brief Entraînement BasketVibe — 2026-10-24 (export Entraînement de 20:10 UTC)

Briefs amont lus : `2026-10-24-effectif.md` (et `2026-10-18-entrainement.md` pour le delta). Données : `gold.bv_training_options` (choix saisis, relevé du 24/10 20:10), `gold.bv_potential_estimate` (semaine du 18/10), `silver.bv_player_daily` (24/10). Skills : basketvibe-entrainement [M§8.2–8.5], basketvibe-joueurs [M§2.2].
Prochain passage : **dim. 25/10 04:00 (Paris)**, dernier entraînement de la saison 1 ; +1 an au changement de saison (nuit du 26 au 27).

## FICHE DE SAISIE — 17 joueurs

**Seulement 2 changements** (les 14 autres joueurs de moins de 30 ans sont déjà saisis comme au brief du 18/10, vérifié sur le relevé de 20:10). Rouge d'abord.

| Priorité | Joueur | Âge | Principale (valeur) | Secondaire (valeur) | Verdict | Gain attendu |
|---|---|---|---|---|---|---|
| 🟥 URGENT | **Min-jun Dang** (SG) | 29 | Rebond 41,0 → **Défense 43,0** | Passe 39,0 → **Trois points 44,0** | **changer** | PS : +0,225 × gain de principale au lieu de +0,10 × (voir note Dang) |
| 🟧 IMPORTANT | **Anselmo Albano** (PF) | 26 | Défense 53,25 → **Rebond 50,88** | Athlétisme 46,75 → **Défense 53,25** | **changer** | gain non mesuré (arrivé après le 18/10) ; même poids PS (0,15) |
| 🟩 SUIVI | Oscar Richard | 24 | Passe 62,77 | Défense 43,06 | garder | principale ≈ +1,06, secondaire ≈ +0,53 |
| 🟩 SUIVI | Thibault Bonnet | 25 | Défense 40,83 | Dribble 33,20 | garder | ≈ +0,91 / +0,46 |
| 🟩 SUIVI | Hadrien Gimenez | 25 | Deux points 58,75 | Trois points 55,41 | garder | ≈ +0,82 / +0,41 |
| 🟩 SUIVI | Léo Lefebvre | 28 | Défense 63,75 | Athlétisme 62,39 | garder | ≈ +0,39 / +0,19 |
| 🟩 SUIVI | Armand Fournier | 27 | Rebond 61,02 | Défense 56,57 | garder | ≈ +0,57 / +0,29 |
| 🟩 SUIVI | Naël Boyer | 19 | Passe 46,13 | Dribble 55,84 | garder | ≈ +1,14 / +0,57 |
| 🟩 SUIVI | Soan Henry | 26 | Trois points 37,00 | Deux points 41,00 | garder | ≈ +0,50 / +0,25 |
| 🟩 SUIVI | Jonathan Durand | 24 | Deux points 40,07 | Défense 35,81 | garder | ≈ +0,81 / +0,41 |
| 🟩 SUIVI | Noé Legrand | 22 | Rebond 53,09 | Défense 47,55 | garder | ≈ +1,30 / +0,65 |
| 🟩 SUIVI | Elias Klein | 28 | Rebond 35,81 | Défense 66,26 | garder | ≈ +0,26 / +0,13 (dernier à 28 ans) |
| 🟩 SUIVI | Maël Bernard | 17 | Rebond 61,00 | Athlétisme 52,50 | garder | ≈ +2,20 / +1,10 |
| 🟩 SUIVI | Nolan Baron | 16 | Passe 53,00 | Défense 40,60 | garder | ≈ +1,60 / +0,80 |
| 🟩 SUIVI | Sacha Leclerc | 16 | Trois points 39,20 | Défense 41,60 | garder | ≈ +1,60 / +0,80 |
| 🟩 SUIVI | Loris Lecomte | 16 | Défense 36,30 | Athlétisme 33,15 | garder | ≈ +1,15 / +0,58 |
| 🟩 SUIVI | Nael Fontaine | 30 | (indifférent) | (indifférent) | rien à saisir | 0 : 30 ans [M§8.5] |

Gains attendus = gains mesurés le 18/10 (`gold.bv_potential_estimate`), même âge, même niveau (< 70 partout, multiplicateur ×1 [M§8.4]) ; la valeur change de 1 à 3 points, donc rien ne bouge. Valeurs précises : `gold.bv_training_options`.

### Note Dang (29 ans, dernier entraînement utile)
- Fait : saisi Rebond (poids PS d'un SG 0,05) / Passe (0,10) ; Défense, Trois points = 0,15 chacune (`gold.bv_training_options`). Les 2 nouvelles cibles sont à 43 et 44 : sous 70, sans ralentissement [M§8.4].
- Règle : 0 gain à 30 ans, gains à 29 ans inférieurs à la colonne 25 ans [M§8.3, 8.5]. Valeur exacte non publiée.
- Il me manque le gain réel de Dang : il est arrivé après le relevé du 18/10, donc `gold.bv_training_gains_exact` est vide pour lui (le « 0,20/sem. » du brief Effectif vient de l'outlook, valeurs entières, pas une mesure). On le réunira avec l'export Entraînement de dimanche matin après 04:00 (relevé vs ce soir). Avis (confiance moyenne) : pour un même gain g, PS +0,225 g (0,15 × g + 0,15 × g/2) contre +0,10 g aujourd'hui, soit plus du double. L'effet absolu est de l'ordre du centième de PS.
- Ne pas viser Athlétisme 70 (×1 à 70) ni Deux points 59 : même poids PS (0,15) ; Défense et Trois points sont les plus basses, mais elles servent pareil au PS ; choix aligné sur le brief Effectif.

### Note Albano (26 ans)
- Fait : Défense / Athlétisme saisis, probablement par son club précédent (jamais mesurés chez nous). Rebond 50,88, Défense 53,25, Athlétisme 46,75 : mêmes poids PS 0,15 pour un PF.
- Avis (confiance faible, gain d'âge 26 ans hypothèse) : pour un même coût, travailler le Rebond (levier 1 du brief Effectif : Albano remplace Richard dans l'unité A pour monter le rebond de J22/amical) est plus utile en match [M§7.1, via brief Effectif] que l'Athlétisme. Gain attendu à 26 ans ≈ 0,5 pt de la principale (référence Henry 26 ans, potentiel 4 : +0,50 ; Albano peut être au-dessus ou en dessous). Le rebond ne montera pas assez pour jouer sur J22 : c'est un investissement de saison 2.
- Si l'utilisateur préfère ne pas toucher : le coût du statu quo est nul en PS (poids identiques). Changer reste mon choix.

## 16–17 ans et 29 ans (consigne du 25/10)
| Joueur | Âge → saison 2 | Ce que ça change | Source |
|---|---|---|---|
| Dang | 29 → 30 | **dernier entraînement utile** ; 0 gain dès 30 ans, déclin à 31 | [M§8.5] |
| Bernard | 17 → 18 | facteur d'âge maximal « vers 18 ans » : inchangé | skill basketvibe-entrainement [M§8.2] |
| Baron, Leclerc, Lecomte | 16 → 17 | bande 16–18 ans du manuel : facteur 1,0 inchangé | [M§8.3] |
| Lefebvre, Klein | 28 → 29 | gains plus faibles dès la saison 2 ; Klein et Lefebvre : garder | [M§8.3] |
| Fontaine | 30 → 31 | déclin dès 31 ans (saison 2), l'entraînement ne le compense pas | [M§8.5] |
Correction de la consigne : pour les 16–17 ans le facteur d'âge ne change pas au +1 an (la table du manuel les traite dans la même bande 16–18) ; il baissera seulement à 19 ans (Boyer 19 → 20 : interpolation hypothèse). Ne pas sauter la saisie du 25/10.

## Potentiel (E11) — delta
Aucune nouvelle mesure : un seul relevé de gains (semaine du 18/10), identique au brief du 18/10 ; le relevé du 25/10 (après 04:00) donnera la 2e semaine. Rappels : Bernard **10** (élevée), Baron **8** (élevée), Leclerc **8** (élevée), Lecomte **5** (élevée), Bonnet **7** (élevée), Gimenez **6** (élevée), Legrand **8 ou 9**, Richard **8 ou 7**, Boyer et Durand **5 ou 6**, Fournier, Lefebvre **8 ou 7**, Henry **4 ou 5**, Klein **5 ou 4** (moyenne à faible : facteur d'âge interpolé, hypothèse). Dang et Albano : **non mesurés**. Les fiches de joueur affichent une tranche (« Decent potential ») [fiche, constat du 2026-10-23] : pas de contrôle chiffré possible, il faudrait étendre le script pour lire ce libellé sur d'autres joueurs.

## Données manquantes
- Il me manque les gains réels de Dang et Albano : on les réunit avec l'export Entraînement après dim. 25/10 04:00 (`gold.bv_training_gains_exact`), puis `gold.bv_potential_estimate`.
- Il me manque le potentiel affiché sur la fiche des joueurs (tranche Low/Decent/High) en base : à extraire par le script sur la page de chaque joueur.

## Conseils suivis
C-046 ajouté dans `outputs/basketvibe/learnings.md` ; C-011 reste valable pour les 14 autres joueurs.

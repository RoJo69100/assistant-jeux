Amical contre Union Heidelberg (18/11)

Saisie AUJOURD'HUI mardi 17/11 (heure Paris 11:06), verrou mercredi 18/11 07:45 (match 08:00). Amical : pas de preset. Moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Ligue J8 à C.B.Granada le 18/11 20:00 (verrou 19:45, `gold.bv_next_opponents`) : les titulaires de ligue ne jouent presque pas ce matin. L'amical du 19/11 est traité dans un autre fichier (non touché). Brief du jour de l'analyste lu (`2026-11-17-analyste.md`) : ses points de ligue sont hors périmètre ; pour l'amical je retiens Durand 24 min au plus, jamais 4 quarts, et le contrôle de la sauvegarde à l'écran. Aucun brief Match du jour : aucun compteur d'échecs à respecter ici.

## Action : fais X
Sur la page du match d'amical contre Union Heidelberg, avant 07:45 demain : saisis la composition ci-dessous (**12 joueurs à l'effectif, 7 utilisés, 36 min maximum chacun**), **agressivité 3 pour les 12 joueurs** (test E1 niveau A, cran 2 « équilibrée »), zone Perimeter (1) et focus 3 pour les 12 adversaires (un seul test), sauvegarde, puis exporte la page du match (l'export donnera les noms des adversaires). **Vérifie à l'écran après sauvegarde** : colonne Agress. = 3 pour chaque joueur, Leclerc Tir = 2 (le 14/11, `gold.bv_saisie_joueurs` donne Leclerc Tir 5 et `shot_tier` 4 en match, au lieu du 2 prévu : le plan n'a pas été saisi tel quel), minutes de Durand = 24.
Dang et Ungureanu (joués le 14/11) ne sont plus dans `gold.bv_roster_now` (12 joueurs, minimum de transfert 8 respecté) : cause non vérifiée ici ; le tableau les omet. Blessés : aucun (`injury_return_on` vide pour les 12 ; Gimenez de retour, forme 9).

## 1. Composition (écran 1)
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Boyer | Albano | Bernard |
| Q2 | Boyer | Leclerc | Durand | Legrand | Bernard |
| Q3 | Baron | Leclerc | Boyer | Albano | Legrand |
| Q4 | Baron | Durand | Albano | Legrand | Bernard |
| Prol. | Boyer | Leclerc | Durand | Legrand | Bernard |

Remplaçants : aucun programmé. Richard, Bonnet, Gimenez, Lefebvre, Fournier (titulaires de ligue) : 0 minute.

## 2. Tableau de saisie (écran 2, 1-5, ordre de l'écran)
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron (17 ans) | PG | PG | — | PG | PG | — | 36 | 2 | 1 | 2 | 3 |
| Boyer (20 ans) | PG | SF | PG | SF | — | PG | 36 (+5) | 4 | 3 | 3 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc (17 ans) | SG | SG | SG | SG | — | SG | 36 (+5) | 3 | 3 | 2 | 3 |
| Durand | SF | — | SF | — | SG | SF | 24 (+5) | 3 | 3 | 2 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | PF | — | PF | SF | — | 36 | 3 | 4 | 1 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | — | PF | C | PF | PF | 36 (+5) | 4 | 4 | 1 | 3 |
| Bernard (18 ans) | C | C | C | — | C | C | 36 (+5) | 3 | 3 | 1 | 3 |
| Fournier | C | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |

Dans les colonnes Q, la valeur est l'emplacement tenu (Boyer : SF Q1 et Q3, PG Q2 ; Durand : SF Q2, SG Q4 ; Albano : PF Q1 et Q3, SF Q4 ; Legrand : PF Q2 et Q4, C Q3). (+5) = prolongation éventuelle : en cas de prolongation, 4 joueurs passent à 41 min, inévitable avec 7 joueurs et le plafond de 36 sur le temps réglementaire.

Minutes : Baron 36 + Boyer 36 + Leclerc 36 + Bernard 36 + Albano 36 + Legrand 36 + Durand 24 = 240. Jeunes ≤ 21 ans : Baron, Boyer, Leclerc, Bernard = 144 min sur 240 (60 %), âges 17, 20, 17, 18 (`gold.bv_roster_now`). Ordre des objectifs : plafond de 36 et titulaires de ligue protégés, jeunes à 36, test E1.

Valeurs qui s'écartent du neutre (3) ou de la règle uniforme :
- Agressivité 3 partout au lieu de 1 (L-004) : test E1 niveau A demandé, seul réglage défensif modifié, même cran pour les 12 (y compris 0 min) pour un test propre.
- Tir (chiffres : `gold.bv_match_player_lines`, tous matchs depuis le 27/10, L-020) : Leclerc Tir 2 (64 % de ses tirs à 3 pts, réussis à 26 %, 60/227 ; 2P 54 %) ; Baron Tir 2 (44 % à 3 pts, 31 %) ; Durand Tir 2 (42 % à 3 pts, 27 %, 2P 52 %) ; Albano Tir 1 (43 % à 3 pts, 23 %) ; Legrand Tir 1 (13 % à 3 pts, 2P 52 %) ; Bernard Tir 1 (8 % à 3 pts, 2P 51 %) ; Boyer Tir 3 (47 % à 3 pts à 33 %, 2P 64 %, donc neutre). Réglages offensifs : variable secondaire, ils ne changent pas la lecture défensive du test.
- Off. focus 4 Boyer (2P 64 %) et Legrand (2P 52 %, intérieur) ; Off. focus 2 Baron (peu de tirs, 82 en 28 matchs). Rôle 1 Baron (passeur), rôle 4 Albano et Legrand (intérieurs).
- Les 5 joueurs à 0 minute : 3 partout, sans effet.

## 3. Adversaires (écran 3) : Union Heidelberg
Joueurs adverses inconnus : `gold.bv_saisie_adversaires` n'a aucune ligne pour Union Heidelberg, `gold.bv_match_report` et `gold.bv_match_opp_focus` non plus (aucune rencontre) ; focus neutre (Normal partout, aucun Give up). Zone Perimeter (1) pour tous : c'est la zone du match E1 du 14/11 (`gold.bv_saisie_adversaires`), donc la mesure se compare sans changer de variable ; en amical v4, Perimeter a donné le plus bas 2P adverse (45,5 % et 53,4 % contre 59,4 % en Rim et 63,8-66,0 % en Middle, L-027, 2 à 5 matchs : confiance faible). Export à faire : la page du match avant 07:45 si la liste est visible, sinon juste après le match.

| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 (noms inconnus, export à faire) | tous | 3 | Perimeter (1) |

## 4. Focus défensif (section obligatoire)
Aucun joueur adverse connu : pas de parts de tirs ni de 2P/3P. Normal (3) et Perimeter sur les 12, pas d'Intense ni de Give up faute de données. Après le match, l'export donnera ses scoreurs.

## 5. Contrôle SQL (fait, 17/11 11:06)
- 5 joueurs différents par quart-temps, un par emplacement : oui (plan joint à `gold.bv_slot_fit`).
- Maximum 36 min (hors prolongation) : oui, aucun `over_36` prévu ; Durand 24.
- `height_eff` ≥ 95 sur chaque emplacement : oui (minimum 99,2, Boyer SF). `fit_with_form` : de 42,1 (Leclerc SG) à 52,9 (Legrand PF et C) ; Durand SF 43,1 et SG 44,2 ; amical de formation, sans enjeu.
- Fatigue ajoutée (minutes × 0,019 × 1,0 × (1,5 − 0,008 × endurance), cran 3, multiplicateur supposé 1,0) : Baron 0,84, Bernard 0,83, Leclerc 0,77, Boyer 0,76, Albano et Legrand 0,70, Durand 0,47. Fatigue actuelle (`gold.bv_roster_now`, relevé du 16/11) : ligue ménagés Bonnet 13,94, Fournier 13,13, Lefebvre 13,08, Richard 12,6, Gimenez 10,48 ; joués : Durand 8,96, Legrand 8,55, Boyer 7,29, Bernard 6,03, Baron 1,69, Albano 1,45, Leclerc 1,42 ; tout sous 20 (zone verte). Ajoutée par l'amical aux ligue : 0. Gimenez a joué 48 min les 15 et 16/11 (plan par défaut, `bv_match_player_lines`) : repos complet ce matin.
- Blessés : aucun.

## 6. Blessés et plan B
Personne n'est blessé. Si un des 7 utilisés manquait à l'écran, le plan B est Gimenez ou Lefebvre (rang 1-2 aux emplacements SF, PF, C, `gold.bv_slot_fit`), mais ils sont gardés pour la ligue : à n'utiliser qu'en dernier recours. Dang et Ungureanu ne sont plus à l'effectif (à confirmer à l'écran).

## 7. Test unique et évolution
Test E1 niveau A, 2e passage : agressivité écran 3 au lieu de 1 (L-004). 1er passage (C-124, 14/11, Artificial Instinct) : appliqué, `defense_tier` 2 pour les 9 joueurs utilisés, 4 jeunes à 36 min, 5 joueurs de ligue à 0, `pf` Baron 3, Boyer 1, Leclerc 3 (`gold.bv_match_player_lines`). Résultat (`gold.bv_match_report`) : `opp_fg2_pct` 56,5, 109 points encaissés, `pf` 19 ; amicaux du 15 et 16/11 à agressivité 1 : 50,0 et 56,4, 94 et 103 points, `pf` 13 et 16. Aucun gain visible, un match, adversaires différents (Gimenez 48 min les 15 et 16/11 : comparaison confondue). Selon le critère de C-124 (faux si points ou fautes montent sans baisse de `opp_fg2_pct`), le test est plutôt réfuté ; je le rejoue parce que tu l'as demandé, et un 2e match décidera : si `opp_fg2_pct` > 54 ou points encaissés > 105 ou `pf` > 16 le 18/11, E1 est clos comme perdant. Doute : bruit élevé, adversaire inconnu ; Tir et Off. focus sont des variables offensives secondaires. Conseil ajouté : **C-125** dans `outputs/basketvibe/learnings.md` (note : le brief analyste du jour propose aussi un « C-124 », déjà pris par le conseil du 13/11 ; il doit être renuméroté).

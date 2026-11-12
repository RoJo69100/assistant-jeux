Coupe contre Stare Kotlety (12/11)

Coupe, jeudi 12/11, verrou 19:00 (fatigue 25 % de la ligue, sans blessure ni avantage du terrain). À saisir AUJOURD'HUI 11/11 (09:40 Paris). Preset « League Tactic » (même id ; l'export affiche « Cup »), à re-sélectionner sur ce match. Briefs amont du jour : Match absent, Entraînement absent ; lus : `gold.bv_roster_now` (relevé du 10/11, forme du 08/11), `gold.bv_saisie_joueurs`, `gold.bv_saisie_adversaires` (export Preview du 10/11 16:11 Paris : aucun export plus récent), `gold.bv_slot_fit`, `gold.bv_fatigue_plan`, `gold.bv_match_player_lines` (dernier match 09/11), `gold.bv_next_opponents`, brief du jour `2026-11-11-quotidien.md`, brief précédent `2026-11-10-tactique-coupe.md`. Brief de ligue du 11/11 (BC KIT) : non relu ici, la fiche reprend le même cinq.

## Action : fais X
**Re-sélectionne « League Tactic » sur le match de coupe du 12/11, saisis le tableau ci-dessous (joueurs puis les 13 adversaires), vérifie agressivité 1 pour les 14 joueurs, puis sauvegarde.** `gold.bv_saisie_joueurs` (10/11 16:11, `sauvegarde_match` = faux) montre les défauts : agressivité 3 pour les 14 et 48 min (+5) pour les 5 titulaires (au-delà de 3 quarts-temps, −20 % [M§5.7]). Rien n'est saisi à ce jour.

Rien ne change par rapport au brief du 10/11 : aucune donnée nouvelle (mêmes statistiques, dernier match en base le 09/11, aucun export Stare Kotlety). Réglage qui n'a pas de raison de bouger : je le reprends tel quel.

Fatigue (Bonnet, Gimenez, Richard, Lefebvre, Fournier, ligue ce soir) : `gold.bv_roster_now` au 10/11 : Gimenez 15,71, Bonnet 14,16, Richard 13,41, Lefebvre 13,41, Fournier 13,36. `gold.bv_fatigue_plan` à 36 min, `defense_tier` 0 : 13,1 à 14,0 (zone verte ≤ 20) ; à 48 min Fournier 19 : limite. La coupe ajoute 25 % de la fatigue de ligue [commun.md, rythme coupe]. Hypothèse, non recalculée : la fatigue après la ligue de ce soir. Je garde 36 min (pas 48, pas de 4e quart-temps de plus), les Q3 et la prolongation sont confiés au banc. Si l'export de demain matin montre une fatigue d'un titulaire > 20, il passe à 24 min (Legrand ou Durand/Albano derrière) : à contrôler avant le verrou 19:00 du 12/11 si tu rouvres l'écran.

Blessé / vendu : aucun blessé (`gold.bv_roster_now.injury_return_on` vide pour les 14). Vente de Ungureanu proposée dans le brief du jour : non validée par écrit ; la fiche l'utilise au Q3 et en prolongation ; s'il est vendu avant le verrou, Bernard (C) prend ses minutes (Bernard à 0 min dans la fiche, `fit_with_form` non recalculé ici).

## 1. Fiche de saisie (écran 1-5, ordre PG → C)

| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 1 |
| Boyer | PG | — | — | PG | — | PG | 12 (+5) | 2 | 2 | 1 | 1 |
| Richard | PG | PG | PG | — | PG | — | 36 | 1 | 1 | 3 | 1 |
| Bonnet | SG | SG | SG | — | SG | — | 36 | 5 | 5 | 3 | 1 |
| Dang | SG | — | — | SG | — | SG | 12 (+5) | 3 | 3 | 1 | 1 |
| Leclerc | SG | — | — | — | — | — | 0 | 4 | 4 | 3 | 1 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 1 |
| Gimenez | SF | SF | SF | — | SF | SF | 36 (+5) | 4 | 3 | 3 | 1 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 1 |
| Lefebvre | PF | PF | — | PF | PF | PF | 36 (+5) | 4 | 4 | 1 | 1 |
| Legrand | PF | — | PF | SF | — | — | 24 | 3 | 3 | 1 | 1 |
| Bernard | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 1 |
| Fournier | C | C | C | — | C | — | 36 | 2 | 2 | 1 | 1 |
| Ungureanu | C | — | — | C | — | C | 12 (+5) | 3 | 3 | 1 | 1 |

Anticipation (hypothèse) : plan B « Bonnet muselé » : si Stare Kotlety applique notre règle (Intense sur ≥ 13,5 % des tirs), Bonnet (17,0 % des tirs, 80 % à 3 pts) prend un Intense Perimeter ; la fiche tient sans lui : Gimenez (off. focus 4, 41 % à 3 pts) et Lefebvre (off. focus 4, 74 % à 2 pts) en relais, Fournier et Legrand à 2 pts, Richard passeur ; aucun focus adverse en base, à ne pas lire comme un fait.

Raisons des valeurs qui se détachent (tout le reste = règle uniforme) :
- Agress. 1 partout : L-004 (cran 0 : eFG adverse 46,0 contre 54,2 au cran 2, saison 1) ; aucune valeur isolée. `gold.bv_fatigue_plan` : `defense_tier` 0 à 36 min pour tous.
- Bonnet tir 3 : ligue S2 depuis le 02/11 (`gold.bv_match_player_lines`) : 56 tirs dont 45 à 3 pts (80 %), 21/56 au total, 13/45 à 3 pts (29 %) ; 2P 78, 3P 72 (`gold.bv_roster_now`). Confiance faible-moyenne.
- Dang, Boyer, Ungureanu tir 1 : Q3 et prolongation ; réussite à 3 pts basse (Dang 1/13, Boyer 1/4, Ungureanu 2/8, S2 ligue) ; compétences 2P ≥ 3P (Dang 59/44, Ungureanu 45/41, Boyer 51/48). Petits échantillons : confiance faible.
- Leclerc tir 3 : 0 minute, 2P = 3P = 44 : valeur neutre.
- Lefebvre, Legrand, Fournier, Bernard tir 1 : 2P ≥ 3P, 10 à 13 % de tirs à 3 pts.
- Gimenez et Lefebvre off. focus 4 : relais offensifs (plan B) ; Richard rôle 1 / off. focus 1 : meneur passeur.

Remplaçants (depth chart) : PG Baron, SG Leclerc, SF Durand, PF Albano, C Bernard derrière les titulaires ; en cours de match Boyer, Dang, Legrand, Ungureanu.

## 2. Étude de l'adversaire : Stare Kotlety (`gold.bv_saisie_adversaires`, coupe 12/11)
Faits : l'aperçu du 10/11 16:11 donne 13 noms et postes (PG 3, SG 2, SF 3, PF 2, C 3), focus 3 / Middle (3) partout. **Aucune statistique** : 0 ligne pour Stare Kotlety dans `gold.bv_match_opp_focus` ; `gold.bv_next_opponents` ne couvre que la ligue (BC KIT 11/11 : rang 11, 1-3, diff −57), rien sur cette coupe (rang, bilan, forme, confrontations). Part de tirs, 2P/3P, minutes : inconnus. Export à faire : page du match de coupe après le match (stats par joueur), pour le prochain tour ; rien d'autre n'est possible avant le verrou (collecte passive).

### Focus défensif (obligatoire)
Joueurs adverses inconnus : focus neutre (Normal = 3), zone Middle (3), aucun Give up, aucun Intense/Lock sans chiffre [commun.md, adversaire inconnu]. Avis (confiance faible) : un Intense sur un scoreur aveugle fait baisser le Normal des autres sans bénéfice prouvé ; je ne le fais pas. Après l'export des stats : Intense (4) sur le ou les joueurs à ≥ 13,5 % des tirs, jamais Light sur un scoreur (L-006).

Tableau des adversaires (une ligne par adversaire de `gold.bv_saisie_adversaires`, ordre de l'export) :

| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Bartosik | PG | 3 | Middle |
| Cieślak | PG | 3 | Middle |
| Kowalik | PG | 3 | Middle |
| Przybylski | SG | 3 | Middle |
| Sienkiewicz | SG | 3 | Middle |
| Marciniak | SF | 3 | Middle |
| Nowakowski | SF | 3 | Middle |
| Wysocki | SF | 3 | Middle |
| Krzyżanowski | PF | 3 | Middle |
| Lis | PF | 3 | Middle |
| Kowalski | C | 3 | Middle |
| Krajewski | C | 3 | Middle |
| Sikora | C | 3 | Middle |

Changement par rapport à l'écran par défaut : aucun. Zone Perimeter : non prouvée en ligue, non retenue.

## 3. Anticipation : décisions de l'adversaire contre nous (hypothèse)
Aucune donnée sur les focus adverses en base. Hypothèse : Stare Kotlety applique la même règle que la nôtre. Règle : Intense (4) sur les tireurs à ≥ 13,5 % des tirs, Normal (3) entre 8 et 13,5 %, Light (2) sous 8 % ; zone Perimeter si ≥ 45 % des tirs à 3 pts, Rim si ≤ 15 %, Middle entre les deux. Source : `gold.bv_match_player_lines`, ligue S2 depuis le 02/11, 329 tirs au total (inchangé depuis le 10/11).

| Joueur | Part des tirs | % tirs à 3 pts | 2P / 3P | Focus attendu | Zone attendue |
|---|---|---|---|---|---|
| Bonnet | 17,0 % | 80 % | 73 % / 29 % | Intense | Perimeter |
| Fournier | 15,2 % | 10 % | 36 % / 20 % | Intense | Rim |
| Gimenez | 14,0 % | 48 % | 54 % / 41 % | Intense | Perimeter |
| Lefebvre | 13,7 % | 13 % | 74 % / 33 % | Intense | Rim |
| Legrand | 11,6 % | 11 % | 50 % / 50 % | Normal | Rim |
| Richard | 10,9 % | 39 % | 64 % / 29 % | Normal | Middle |
| Dang | 6,1 % | 65 % | 86 % / 8 % | Light | Perimeter |
| Ungureanu | 5,8 % | 42 % | 55 % / 25 % | Light | Middle |
| Boyer | 2,7 % | 44 % | 100 % / 25 % | Light | Middle |
| Albano, Durand | 1,8 %, 1,2 % | — | 1 match, échantillon trop petit | Light | — |

Plan B et solidité : le pire cas (Intense sur Bonnet, Fournier, Gimenez, Lefebvre : 4 des 5 titulaires, 60 % des tirs) laisse Richard (Normal) et Legrand (Normal). La fiche s'appuie sur la dispersion : Bonnet tir 3 mais deux relais off. focus 4 (Gimenez, Lefebvre), Legrand PF au Q2 et SF au Q3 (11,6 % des tirs, 50 % à 2 pts et à 3 pts), Richard (10,9 %) passeur en off. focus 1. Le cinq reste : aucun joueur du banc n'a un meilleur `fit_with_form` (Bonnet SG 55,2, Fournier C 52,9 contre Dang 51,9, Legrand 51,2, Ungureanu 48,9). Confiance faible : un adversaire humain peut jouer autrement.

## 4. Blessés et plan B de composition
Aucun blessé (`gold.bv_roster_now.injury_return_on` vide pour les 14) ; pas de blessure en coupe de toute façon [commun.md]. Si un titulaire manque au verrou : Durand pour Gimenez (SF), Albano pour Lefebvre (PF), Bernard pour Fournier (C), Baron pour Richard (PG), Leclerc pour Bonnet (SG) ; `fit_with_form` des remplaçants non recalculé ici.

## 5. Contrôle SQL (`gold.bv_slot_fit`, `gold.bv_fatigue_plan`, `gold.bv_roster_now`, `gold.bv_saisie_adversaires`)
- 5 joueurs différents par quart, un par emplacement PG/SG/SF/PF/C : OK (Q1 Richard, Bonnet, Gimenez, Lefebvre, Fournier ; Q2 Richard, Bonnet, Gimenez, Legrand PF, Fournier ; Q3 Boyer, Dang, Legrand SF, Lefebvre, Ungureanu ; Q4 comme Q1 ; prolongation Boyer, Dang, Gimenez, Lefebvre, Ungureanu).
- Maximum 3 quarts-temps réguliers par joueur : OK (cinq 36 min ; Legrand 24 ; Boyer, Dang, Ungureanu 12). Prolongation (+5 min) à part : Gimenez et Lefebvre 41 min si prolongation (signalé).
- `height_eff` ≥ 95 : OK (100 partout, Legrand SF 99,2 d'après le contrôle du 10/11).
- `fit_with_form` : Lefebvre PF 65,3 ; Gimenez SF 64,0 ; Richard PG 60,0 ; Bonnet SG 55,2 ; Fournier C 52,9 ; Dang 51,9 ; Boyer 51,5 ; Legrand PF 51,2 (SF 49,9) ; Ungureanu 48,9 (valeurs du 10/11, relevé inchangé).
- Fatigue stabilisée, agressivité 0 (écran 1), 36 min : Bonnet 14,1 ; Gimenez 14,0 ; Richard 13,4 ; Lefebvre 13,3 ; Fournier 13,1 : zone verte (≤ 20), `defense_tier` 0 pour tous.
- Adversaires : 13 lignes, 13 dans le tableau, mêmes noms et postes, ordre de l'export.
- Blessés / vendus : aucun dans la fiche (vente Ungureanu non validée).

## 6. Doute et conseil
Doute : Stare Kotlety sans statistique ; un Intense sur un scoreur inconnu serait un pari. **Faux si**, après match, `gold.bv_match_opp_focus` montre un joueur adverse à ≥ 25 % des tirs resté en Normal avec une forte réussite (alors Intense à prévoir au tour suivant), ou si `defense_tier` n'est pas 0 pour tous.
Conseil **C-120** ajouté dans `outputs/basketvibe/learnings.md` (C-118 et C-119 du 10/11 absents de ce fichier : à vérifier par l'appelant) : `defense_tier` = 0 pour tous les joueurs avec `min` > 0 en coupe le 12/11 (`gold.bv_match_player_lines`, competition = 'cup', match_day = '2026-11-12').

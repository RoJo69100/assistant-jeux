# Brief Entraînement BasketVibe — 2026-11-23 (Chomelix Cow) — entraînement du 22/11

Aucun achat, vente ni enchère. Prochain passage : **dim. 29/11 04:00 (Paris)** ; sauvegarde à faire aujourd'hui (23/11) ou avant.
Briefs amont : aucun brief du jour lu (pas de lecteur-exports ni d'effectif du 23/11 en `briefs/`). Dernier brief entraînement : `2026-10-25-entrainement.md` ; delta = 01/11, 08/11, 15/11, 22/11.

## ⚠️ Données manquantes (à lire d'abord)
- **L'entraînement du 22/11 n'est pas mesurable** : le dernier relevé (`silver.bv_player_weekly`, jour 2026-11-20, 12 joueurs) est antérieur au passage du 22/11 04:00.
- Ce relevé du 20/11 n'a **ni valeurs précises ni réglage** (`training_primary` vide, `*_exact` vides) ; `gold.bv_training_gains_exact` et `gold.bv_potential_estimate` n'ont plus de gains après le 25/10 (gains vides). Dernier relevé complet : **2026-11-13** (14 joueurs).
- **Export à faire aujourd'hui** : page Entraînement (valeurs précises + choix), après le 22/11 04:00. Sans lui je ne peux ni mesurer le 22/11 ni confirmer que les réglages saisis sont toujours ceux du 13/11.

## 1. Fiche de saisie (pour le 29/11 04:00) : AUCUN CHANGEMENT
Réglages = ceux du relevé complet du 13/11 (`silver.bv_player_weekly`, jour 2026-11-13), identiques à la fiche du 25/10 pour les 12 joueurs. Ordre de l'écran (poste puis alphabétique). Valeur = relevé du 20/11 (entier arrondi vers le bas, avant le 22/11). Gain attendu = gain par semaine mesuré (voir §2).

| Poste | Joueur (âge) | Principale | Secondaire | Gain attendu P / S |
|---|---|---|---|---|
| PG | Baron (17) | Passes 59 | Défense 43 | +1,60 / +0,80 |
| PG | Boyer (20) | Passes 50 | Dribble 58 | +1,08 / +0,54 |
| PG | Richard (25) | Passes 66 | Défense 44 | +0,97 / +0,48 |
| SG | Bonnet (26) | Défense 43 | Dribble 34 | +0,74 / +0,37 |
| SG | Leclerc (17) | 3 points 45 | Défense 44 | +1,60 / +0,80 |
| SF | Durand (25) | 2 points 42 | Défense 37 | +0,74 / +0,37 |
| SF | Gimenez (26) | 2 points 61 | 3 points 56 | +0,66 / +0,33 |
| PF | Albano (27) | Rebond 53 | Défense 54 | +0,57 / +0,28 |
| PF | Lefebvre (29) | Défense 64 | Athlétisme 62 | +0,19 / +0,10 |
| PF | Legrand (23) | Rebond 57 | Défense 49 | +1,20 / +0,60 |
| C | Bernard (18) | Rebond 69 | Athlétisme 56 | +2,20 / +1,10 |
| C | Fournier (28) | Rebond 62 | Défense 57 | +0,37 / +0,19 |

Absents du relevé du 20/11 (étaient au relevé du 13/11 ou du 25/10) : Ungureanu, Dang, Klein, Fontaine, Henry : aucun réglage à saisir pour eux ; départ à confirmer par l'export (`gold.bv_roster_now` n'est que le relevé du 20/11).

## 2. Verdict : gain mesuré contre gain attendu
Faits (`silver.bv_player_weekly`, 25/10 → 13/11 = 2 entraînements, 01/11 et 08/11, comparés aux gains attendus du brief du 25/10) :

| Joueur | Compétence | 25/10 → 13/11 | Attendu 2 × |
|---|---|---|---|
| Bernard | Rebond | 63,2 → 67,6 : +4,40 | 2 × 2,20 = 4,40 |
| Baron | Passes | 54,6 → 57,8 : +3,20 | 3,20 |
| Leclerc | 3 points | 40,8 → 44,0 : +3,20 | 3,20 |
| Legrand | Rebond | 54,4 → 56,77 : +2,37 | 2,40 |
| Boyer | Passes | 47,3 → 49,49 : +2,19 | 2,16 |
| Richard | Passes | 63,8 → 65,66 : +1,86 | 1,94 |
| Bonnet | Défense | 41,7 → 43,24 : +1,54 | 1,48 |
| Durand | 2 points | 40,9 → 42,28 : +1,38 | 1,48 |
| Gimenez | 2 points | 59,6 → 60,92 : +1,32 | 1,32 |
| Albano | Rebond | 51,6 → 52,77 : +1,17 | 1,14 |
| Fournier | Rebond | 61,6 → 62,37 : +0,77 | 0,74 |
| Lefebvre | Défense | 64,1 → 64,53 : +0,43 | 0,38 |

Tous conformes (écart ≤ 0,10) : le facteur d'âge du +1 an n'a pas changé le gain à 17–18 ans (le test du brief du 25/10 est passé). Les gains par semaine sont donc inchangés.

Entraînement du 15/11 (13/11 précis → 20/11 entier) : 11 joueurs sur 12 compatibles avec le gain attendu si l'écran affiche la partie entière (ex. Bernard 67,6 + 2,2 = 69,8 → 69 ; Leclerc 44,0 + 1,6 = 45,6 → 45 ; Richard 65,66 + 0,97 = 66,6 → 66). Durand : 42,28 + 0,74 = 43,02 attendu, affiché 42 : écart ≤ 0,03, dans la tolérance. Hypothèse (affichage = partie entière), confiance moyenne : une valeur entière ne prouve rien à ±1.
Entraînement du 22/11 : **non mesurable** (voir plus haut).

Verdict par joueur : **garder les 12**. Raisons chiffrées :
- Aucune compétence entraînée à 70 ou plus ; la plus haute est Bernard rebond 69,8 (au 13/11 + 15/11). Le ralentissement ne démarre qu'à 75 (×0,88) [M§8.4] ; à 69 + ~2,2/sem. il y arrive vers le 29/11–06/12 : **si l'export montre Bernard rebond ≥ 75, changer sa principale** (le rebond est déjà haut, et le gain tombe à 1,94). Pas avant.
- Gimenez (défense 75, athlétisme 72), Richard (dribble 77,7), Bonnet (2 pts 78, 3 pts 72) : leurs compétences au-dessus de 70 ne sont **pas** entraînées : rien à corriger.
- Lefebvre (29 ans) : gain +0,19 seulement ; 30 ans : plus aucun gain [M§8.5]. Garder (rien de mieux à gagner), ne pas y passer de temps.
- Changer ne rapporte rien (poids PS identiques sur les compétences concernées, brief du 25/10) ; 4–5 semaines pour juger un choix [Com 2026-09-01] ; choix cohérents avec les gains mesurés.

## 3. Potentiel (confiance)
Dernières mesures exploitables : 18/10 et 25/10 (`gold.bv_potential_estimate`), confirmées en moyenne sur 2 semaines le 13/11 (tableau §2). Aucune nouvelle valeur affichée dans la fiche joueur (tranche Low/Decent/High) en base.

| Joueur | Âge | Potentiel | Confiance | Implication |
|---|---|---|---|---|
| Bernard | 18 | 10 | élevée (règle) | à garder et faire jouer |
| Baron | 17 | 8 | élevée | à garder |
| Leclerc | 17 | 8 | élevée | à garder |
| Legrand | 23 | 8 | moyenne | utile |
| Richard | 25 | 8 | moyenne | utile |
| Gimenez | 26 | 6 | élevée (25 ans règle) | neutre |
| Bonnet | 26 | 7 | élevée | neutre |
| Fournier | 28 | 8 | faible (2 valeurs plausibles) | sans enjeu à cet âge |
| Albano | 27 | 7 | faible | idem |
| Boyer | 20 | 5 | moyenne | potentiel faible chez un jeune : monnaie d'échange possible |
| Durand | 25 | 5 | moyenne | idem |
| Lefebvre | 29 | 8 | faible | sans objet (dernier gain utile) |

Rappel : le potentiel multiplie le gain, il ne plafonne pas [M§8.3]. Non recalculé depuis le 25/10 : `gold.bv_potential_estimate` n'a plus de gain après cette date ; cohérent avec le 13/11 ci-dessus.

## 4. Ce qui prouverait que j'ai tort (relevé du dim. 29/11 ou de l'export du jour)
- Un réglage de l'export du jour différent de la fiche §1 = choix non sauvegardé ou changé ailleurs : ressaisir.
- Bernard, Baron, Leclerc : gain principal du 22/11 ou du 29/11 à plus de 0,15 de +2,20 / +1,60 / +1,60 = facteur d'âge faux.
- Bernard rebond ≥ 75 au prochain relevé : changer principale.

## Conseils suivis
- C-128 ajouté dans `outputs/basketvibe/learnings.md` (garder les 12 réglages pour le 29/11).
- C-056 (garder les 17 réglages au 01/11) : confirmé par le relevé du 13/11 (réglages identiques à la fiche du 25/10 ; Bernard +2,20 par semaine en moyenne, Baron et Leclerc +1,60). Statut ajouté.
- C-011 (garder tous les choix au 25/10) : réglages du 13/11 identiques à la fiche, mêmes 12 joueurs encore présents.

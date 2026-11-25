# Brief Entraînement BasketVibe — 2026-11-25 (Chomelix Cow) — entraînements du 15/11 et du 22/11 mesurés

Aucun achat, vente ni enchère. Remplace le brief du 23/11 (`2026-11-23-entrainement-entrainement-22-11.md`), qui disait le 22/11 non mesurable : les relevés précis du 15/11 et du 22/11 sont en base (`gold.bv_training_gains_exact`, k = 1, 12 joueurs, 96 lignes par semaine).
Prochain passage : **dim. 29/11 04:00 (Paris)**. Sauvegarde à faire **aujourd'hui** si un réglage change : ici, aucun.
Briefs amont : aucun brief du jour lu. Dernier brief entraînement : celui du 23/11 ; delta = 15/11 et 22/11.

## 1. Fiche de saisie (pour le 29/11 04:00) : AUCUN CHANGEMENT, garder les 12
Réglages vérifiés sur le dernier relevé (`silver.bv_player_weekly`, jour 2026-11-24, 12 joueurs, 12 réglages renseignés) : identiques à la fiche. Ordre de l'écran (poste, puis alphabétique). Valeur = relevé précis du 22/11 après entraînement (`v_after`).

| Poste | Joueur (âge) | Principale | Secondaire | Valeur P / S | Gain attendu au 29/11 P / S |
|---|---|---|---|---|---|
| PG | Baron (17) | Passes | Défense | 61,0 / 44,6 | +1,60 / +0,80 |
| PG | Boyer (20) | Passes | Dribble | 51,71 / 58,63 | +1,11 / +0,56 |
| PG | Richard (25) | Passes | Défense | 67,49 / 45,42 | +0,91 / +0,46 |
| SG | Bonnet (26) | Défense | Dribble | 44,74 / 35,15 | +0,75 / +0,38 |
| SG | Leclerc (17) | 3 points | Défense | 47,2 / 45,6 | +1,60 / +0,80 |
| SF | Durand (25) | 2 points | Défense | 43,68 / 37,62 | +0,70 / +0,35 |
| SF | Gimenez (26) | 2 points | 3 points | 62,27 / 57,17 | +0,68 / +0,34 |
| PF | Albano (27) | Rebond | Défense | 53,92 / 54,77 | +0,57 / +0,29 |
| PF | Lefebvre (29) | Défense | Athlétisme | 64,92 / 62,97 | +0,20 / +0,10 |
| PF | Legrand (23) | Rebond | Défense | 59,15 / 50,58 | +1,19 / +0,60 |
| C | Bernard (18) | Rebond | Athlétisme | 72,0 / 58,0 | +2,20 / +1,10 |
| C | Fournier (28) | Rebond | Défense | 63,15 / 57,64 | +0,39 / +0,19 |

Absents des relevés du 15/11 et du 22/11 : Ungureanu, Dang, Henry, Lecomte (présents jusqu'au 08/11 dans `gold.bv_training_gains_exact`) : plus au club, aucun réglage à saisir.

## 2. Verdict : gain mesuré contre gain attendu
Faits (`gold.bv_training_gains_exact`, `gain` par entraînement, k = 1) : le gain attendu est le gain constant mesuré du 01/11 et du 08/11. Écart = 0,00 pour les 12 joueurs, principale et secondaire, aux deux entraînements.

| Joueur | Principale | Gain 15/11 | Gain 22/11 | Attendu | Verdict |
|---|---|---|---|---|---|
| Bernard | Rebond 67,6 → 69,8 → 72,0 | +2,20 | +2,20 | 2,20 | garder |
| Baron | Passes 57,8 → 59,4 → 61,0 | +1,60 | +1,60 | 1,60 | garder |
| Leclerc | 3 pts 44,0 → 45,6 → 47,2 | +1,60 | +1,60 | 1,60 | garder |
| Legrand | Rebond 56,77 → 57,96 → 59,15 | +1,19 | +1,19 | 1,19 | garder |
| Boyer | Passes 49,49 → 50,6 → 51,71 | +1,11 | +1,11 | 1,11 | garder |
| Richard | Passes 65,66 → 66,57 → 67,49 | +0,91 | +0,91 | 0,91 | garder |
| Bonnet | Défense 43,24 → 43,99 → 44,74 | +0,75 | +0,75 | 0,75 | garder |
| Durand | 2 pts 42,28 → 42,98 → 43,68 | +0,70 | +0,70 | 0,70 | garder |
| Gimenez | 2 pts 60,92 → 61,6 → 62,27 | +0,68 | +0,68 | 0,68 | garder |
| Albano | Rebond 52,77 → 53,35 → 53,92 | +0,57 | +0,57 | 0,57 | garder |
| Fournier | Rebond 62,37 → 62,76 → 63,15 | +0,39 | +0,39 | 0,39 | garder |
| Lefebvre | Défense 64,53 → 64,72 → 64,92 | +0,20 | +0,20 | 0,20 | garder (29 ans) |

Le rapport secondaire / principale vaut 0,50 pour les 12 (`gold.bv_potential_estimate`, `secondary_ratio`). Le facteur d'âge du +1 an n'a rien changé à 17–18 ans : Bernard, Baron et Leclerc sont exactement sur +2,20 / +1,60 / +1,60.

Corrige le brief du 23/11 : les valeurs y étaient des entiers du relevé du 20/11 ; les valeurs précises ci-dessus font foi.

Règles (skill `basketvibe-entrainement`) et critères de la fiche :
- **Ralentissement** [M§8.4] : ×1 sous 70, ×0,88 à 75, ×0,75 à 80, selon la valeur précise avant l'entraînement. Aucune compétence entraînée ne dépasse 72,0. Bernard, rebond **72,0** : le 29/11 reste à ×1, soit +2,20 attendu, donc 74,2 après. Il passera sous le palier ×0,88 au passage suivant (06/12) s'il atteint 75, ce qui n'arrive pas avant. **Garder aujourd'hui.** Le seuil de changement est : rebond ≥ 75 sur le relevé du 29/11 ou après (il serait alors à 74,2 + 2,2 = 76,4 au passage du 06/12 ; changer à ce moment).
- Compétences ≥ 70 non entraînées (Gimenez défense 75, Richard dribble 77,7, Bonnet 2 pts 78 : valeurs du brief du 23/11, non recontrôlées ici) : rien à corriger.
- **Lefebvre (29 ans)** : gain +0,20. À 30 ans, plus aucun gain [M§8.5]. Le passage du 29/11 reste utile ; rien de mieux à gagner en changeant.
- **Gain réel = gain attendu** : pas de blessure, pas de réglage perdu. Nuance : `gold.bv_training_gains_exact` marque Gimenez `injured_before` = 2026-11-15, mais son gain du 15/11 est normal (+0,68) ; la vue de potentiel le classe « nulle (blessé) » pour ce jour seulement, c'est un signal à ignorer ici.
- **Ne pas changer pour rien** : choix cohérents, 4 à 5 semaines pour juger [Com 2026-09-01] ; ils tiennent depuis le 25/10.

## 3. Potentiel (confiance) — `gold.bv_potential_estimate`, semaines 08/11, 15/11, 22/11
`implied_mult` identique sur 3 semaines pour chaque joueur (médiane = valeur). Aucune contradiction avec le brief du 25/10 ni du 23/11. Fiche joueur : tranche Low/Decent/High seulement, aucune valeur numérique nouvelle en base.

| Joueur | Âge | Potentiel | implied_mult | Confiance | Implication |
|---|---|---|---|---|---|
| Bernard | 18 | 10 | 2,20 (écart 0) | élevée (règle manuel, 3 semaines) | à garder et faire jouer |
| Baron | 17 | 8 | 1,60 (écart 0) | élevée | à garder |
| Leclerc | 17 | 8 | 1,60 (écart 0) | élevée | à garder |
| Richard | 25 | 7 | 1,50 (écart 0) | élevée (âge 25 : règle manuel) | utile |
| Durand | 25 | 5 | 1,15 (écart 0) | élevée (âge 25 : règle manuel) | potentiel faible, pas jeune : sans levier d'échange fort |
| Legrand | 23 | 8 | 1,653 (écart 0,053) | moyenne (âge interpolé, hypothèse) ; 2 valeurs plausibles : 8 et son voisin | utile |
| Boyer | 20 | 5 | 1,248 (écart 0,098) | moyenne (hypothèse d'âge ; distance 0,098 > 0,03, donc 5 ou 6 plausibles) | potentiel faible chez un jeune : monnaie d'échange possible |
| Gimenez | 26 | 6 | 1,378 | faible (26–29 ans, interpolé) ; 2 valeurs plausibles | neutre |
| Bonnet | 26 | 7 | 1,531 | faible ; 2 valeurs plausibles | neutre |
| Albano | 27 | 8 | 1,551 | faible ; 2 valeurs plausibles | sans enjeu |
| Fournier | 28 | 8 | 1,617 | faible ; 2 valeurs plausibles | sans enjeu |
| Lefebvre | 29 | 8 | 1,633 | faible | sans objet (30 ans = 0 gain) |

Changement par rapport au brief du 23/11 : Richard passe de « moyenne » à **élevée** (âge 25, règle du manuel, écart 0 sur 3 semaines : `confidence` = élevée dans la vue) ; Durand idem (élevée, potentiel 5) ; Gimenez : confiance « faible » dans la vue, et non « élevée » comme écrit le 23/11 (la règle « âge 25 » ne couvre pas ses 26 ans). Le potentiel multiplie le gain, il ne plafonne pas [M§8.3].
Écart avec `gold.bv_player_outlook` : non recalculé dans ce brief ; à vérifier si une projection sur 3 saisons est demandée (la vue suppose un potentiel 5 pour les joueurs peu observés).

## 4. Ce qui prouverait que j'ai tort (relevé du 29/11 ou après)
- Un réglage du relevé différent de la fiche §1 : choix non sauvegardé, ressaisir.
- Gain du 29/11 de Bernard, Baron ou Leclerc à plus de 0,15 de +2,20 / +1,60 / +1,60 : facteur d'âge faux (changement de saison / âge).
- Bernard rebond ≥ 75 : changer sa principale (athlétisme 58,0 reste sa secondaire logique, à rediscuter selon le poste).

## Conseils suivis (`outputs/basketvibe/learnings.md`)
- **C-128** (garder les 12 réglages au 29/11) : confiance relevée de moyenne à élevée ; réglages du 24/11 identiques pour les 12, gains du 15/11 et du 22/11 conformes (écart 0). Reste ouvert jusqu'au relevé du 29/11.
- **C-056** : confirmé (déjà noté le 23/11), reconfirmé sur 15/11 et 22/11.
- **C-129** ajouté : même conseil, critères chiffrés avec les valeurs précises du 22/11.

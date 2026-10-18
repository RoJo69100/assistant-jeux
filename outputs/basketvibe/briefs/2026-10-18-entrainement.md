# Brief Entraînement — Chomelix Cow's — 2026-10-18 (dim. soir)

Premier passage de l'agent Entraînement (aucun brief entraînement antérieur).
Données : **une seule semaine précise** (relevé du 16/10 → relevé du 18/10, entraînement du 18/10 04:00), `gold.bv_training_gains_exact` / `gold.bv_potential_estimate`. Contrôle sur la durée : historique affiché (valeurs entières, 7 entraînements du 06/09 au 18/10), `gold.bv_skill_progress_weekly` / `gold.bv_player_outlook.weekly_gain`.
Prochain entraînement : **dim. 25/10, 04:00 (Paris)**, le dernier de la saison 1. Les compétences et le potentiel restent acquis en saison 2 ; l'âge prend +1 (basketvibe-saison).

---

## FICHE DE SAISIE — entraînement du 25/10 (sauvegarder avant dim. 04:00)

**Aucun changement.** Vérifier seulement que l'écran affiche bien ceci :

| Joueur | Âge | Principale | Secondaire | Verdict |
|---|---|---|---|---|
| Oscar Richard | 24 | Passe | Défense | garder |
| Thibault Bonnet | 25 | Défense | Dribble | garder |
| Hadrien Gimenez | 25 | Deux points | Trois points | garder (C-002) |
| Léo Lefebvre | 28 | Défense | Athlétisme | garder |
| Armand Fournier | 27 | Rebond | Défense | garder |
| Naël Boyer | 19 | Passe | Dribble | garder |
| Soan Henry | 26 | Trois points | Deux points | garder |
| Jonathan Durand | 24 | Deux points | Défense | garder |
| Noé Legrand | 22 | Rebond | Défense | garder |
| Elias Klein | 28 | Rebond | Défense | garder |
| Maël Bernard | 17 | Rebond | Athlétisme | garder (C-002) |
| Nolan Baron | 16 | Passe | Défense | garder |
| Sacha Leclerc | 16 | Trois points | Défense | garder |
| Loris Lecomte | 16 | Défense | Athlétisme | garder |
| Nael Fontaine | 30 | (indifférent) | (indifférent) | 30 ans : l'entraînement n'apporte plus rien [M§8.5] ; en vente |

Source des choix actuels : `gold.bv_training_options` (`is_primary` / `is_secondary`, relevé du 18/10). Suivi : C-011.

---

## 1. Potentiel de chaque joueur (E11)

Méthode : `implied_mult` = gain précis de la principale ÷ (multiplicateur de niveau × facteur d'âge), comparé au tableau [M§8.3]. Une seule semaine par joueur, donc pas de médiane possible. Aucun joueur blessé, toutes les compétences entraînées sont sous 70 (multiplicateur de niveau 1 [M§8.4]), et le ratio secondaire/principale vaut **0,50 pour tous** : les 14 mesures sont propres.

| Joueur | Âge | Gain principale | `implied_mult` | Potentiel estimé | Confiance | Semaines | Ce que ça implique (avis) |
|---|---|---|---|---|---|---|---|
| **Maël Bernard** | 17 | +2,200 | 2,200 | **10** | élevée (âge du manuel, distance 0,000) | 1 | Pépite. À garder absolument et à faire jouer (amicaux 36 min, C-009). |
| **Nolan Baron** | 16 | +1,600 | 1,600 | **8** | élevée (0,000) | 1 | À garder et à faire jouer. |
| **Sacha Leclerc** | 16 | +1,600 | 1,600 | **8** | élevée (0,000) | 1 | À garder et à faire jouer. |
| Loris Lecomte | 16 | +1,150 | 1,150 | **5** | élevée (0,000) | 1 | Potentiel moyen (catégorie Decent) : le moins prioritaire des 4 jeunes pour le temps de jeu ; monnaie d'échange possible si une place manque. |
| Thibault Bonnet | 25 | +0,913 | 1,500 | **7** | élevée (âge 25 du manuel, 0,000) | 1 | Bon potentiel, mais 25 ans : gains déjà réduits. |
| Hadrien Gimenez | 25 | +0,822 | 1,350 | **6** | élevée (0,000) | 1 | Dans la moyenne haute. |
| Noé Legrand | 22 | +1,299 | 1,665 | **8 ou 9** (8 le plus proche) | moyenne (âge interpolé, distance 0,065) | 1 | Bon potentiel à 22 ans : il a encore 2–3 saisons de vraie progression. |
| Oscar Richard | 24 | +1,061 | 1,584 | **8 ou 7** (8 le plus proche) | moyenne (âge interpolé, 0,016) | 1 | Bon potentiel ; titulaire PG. |
| Naël Boyer | 19 | +1,140 | 1,213 | **5 ou 6** (5 le plus proche) | moyenne (âge interpolé, 0,063) | 1 | Potentiel moyen ; reste utile (19 ans, PG de l'unité B). |
| Jonathan Durand | 24 | +0,813 | 1,213 | **5 ou 6** (5 le plus proche) | moyenne (âge interpolé, 0,063) | 1 | Potentiel moyen, compétences basses : peu d'avenir dans la rotation. |
| Armand Fournier | 27 | +0,574 | 1,551 | **8 ou 7** (8 le plus proche) | faible (âge interpolé 26–29, 0,049) | 1 | Peu d'effet pratique : à 27–29 ans, le facteur d'âge écrase le potentiel. |
| Léo Lefebvre | 28 | +0,388 | 1,617 | **8 ou 7** (8 le plus proche) | faible (âge interpolé 26–29, 0,017) | 1 | Sans effet pratique : 30 ans dans 2 saisons, déclin à 31 [M§8.5]. |
| Soan Henry | 26 | +0,500 | 1,020 | **4 ou 5** (4 le plus proche) | faible (âge interpolé 26–29, 0,020) | 1 | Potentiel faible à moyen et 26 ans : il ne progressera presque plus. |
| Elias Klein | 28 | +0,259 | 1,079 | **5 ou 4** (5 le plus proche) | faible (âge interpolé 26–29, 0,071) | 1 | Sans effet pratique (28 ans). |
| Nael Fontaine | 30 | 0 | — | non mesurable | sans objet (30 ans [M§8.5]) | — | En vente. |

Notes :
- Les âges 16–18 et 25 ans utilisent le facteur d'âge du manuel [M§8.2, §8.3] ; les autres utilisent `gold.bv_age_factor`, qui est une **hypothèse** d'interpolation (19 → 0,94 ; 22 → 0,78 ; 24 → 0,67 ; 26 → 0,49 ; 27 → 0,37 ; 28 → 0,24). D'où 2 valeurs plausibles. Le relevé du 25/10 (même âge, 2e semaine) ne lèvera pas cette incertitude, puisqu'il mesure avec le même facteur supposé ; il confirmera seulement la stabilité de la mesure.
- Rappel : le potentiel **multiplie** le gain, ce n'est pas un plafond [M§8.3]. Le test à 25 000 ne donnerait qu'une catégorie (Low / Decent / High) [M§4.2] : inutile pour nos joueurs, la mesure est plus précise.
- **Contrôle sur la durée** (historique entier, 7 semaines) : vitesses affichées cohérentes avec les potentiels estimés (Legrand 1,86 pt/sem. contre 1,87–2,16 attendus ; Boyer 1,57 contre 1,62–1,90 ; Bonnet 1,33 contre 1,37 ; Gimenez 1,17 contre 1,24 ; Fournier 0,83 contre 0,83–0,89 ; Henry 0,83 contre 0,74–0,85). Les jeunes sont en dessous (Bernard 2,29 contre 3,30 ; Leclerc 1,63 contre 2,40 ; Lecomte 1,43 contre 1,73) : arrondis à l'entier et choix d'entraînement qui ont changé en cours de période (C-002), pas un démenti.

### Écarts avec `gold.bv_player_outlook`
L'outlook projette à partir de la vitesse affichée (valeurs entières), et suppose un potentiel 5 pour les joueurs peu observés. Recalcul avec le potentiel estimé (gain d'une saison ≈ 8 entraînements × 1,5 × multiplicateur de potentiel × facteur d'âge de l'âge suivant, compétences sous 70, sans blessure ; calcul SQL) :

| Joueur | Outlook : TSP gagné saison prochaine | Avec le potentiel estimé | Écart |
|---|---|---|---|
| **Maël Bernard** (10) | +18 | **+26** (borne haute : son rebond passera 75 en cours de saison, ×0,88 [M§8.4]) | **sous-estimé de ~8** |
| **Sacha Leclerc** (8) | +13 (« potentiel 5 supposé ») | **+19** | **sous-estimé de 6** |
| Nolan Baron (8) | +16 | +19 | sous-estimé de 3 |
| Loris Lecomte (5) | +11 | +14 | sous-estimé de 3 |
| Oscar Richard (7–8) | +9 | +11 à +12 | sous-estimé de 2–3 |
| Naël Boyer (5–6) | +11 | +12 à +14 | léger |
| Noé Legrand (8–9) | +14 | +14 à +16 | conforme |
| Bonnet, Gimenez, Durand, Henry, Fournier, Klein, Lefebvre | — | — | conformes (±1) |

Conséquence (avis) : l'outlook **sous-estime nos 4 jeunes**, surtout Bernard et Leclerc. Les projections de l'agent Effectif à 2–3 saisons doivent être relevées pour eux.

---

## 2. Verdict hebdomadaire : garder ou changer (E10)

**Faits de la semaine** (`gold.bv_training_gains_exact`) : 14 joueurs entraînés, aucun blessé, chaque principale a gagné exactement le gain attendu pour son potentiel estimé, chaque secondaire la moitié. Aucune compétence entraînée n'atteint 70 (la plus haute : Richard passe 62,8, Fournier rebond 61,0, Bernard rebond 61,0).

**C-002 vérifié dans les gains** : le changement a bien été pris en compte par l'entraînement du 18/10. Gimenez trois points +0,411 (55,00 → 55,41) ; Bernard athlétisme +1,100 (51,4 → 52,5). La vue indique encore l'ancien secondaire (défense, trois points), parce qu'elle lit le relevé du 16/10, avant la modification.

Critères dans l'ordre (agent) : 1) ralentissement, 2) utilité en match à l'emplacement réel [M§7.1, §2.2], 3) gain réel contre gain attendu, 4) ne pas changer pour rien.

| Joueur (emplacement réel) | Verdict | Raison chiffrée |
|---|---|---|
| Richard (PG, unité A) | garder | Passe 62,8 et défense 43,1 : deux compétences à 15 au PS du PG ; PG = dribble + passe / défense [M§7.1]. Dribble 77,7 déjà au-dessus de 75 (×0,88) : on ne l'entraîne pas, c'est juste. |
| Bonnet (SG, A) | garder | Défense 40,8 (poids 15, défense principale du SG) est son point faible. Deux points 78 (×0,88) et trois points 72 sont déjà hauts. Dribble 33,2 en secondaire (poids 15 au SG ; il a le focus Primary, il porte le ballon). |
| Gimenez (SF, A) | garder | C-002 appliqué il y a 1 semaine. Défense 75,4 (×0,88) et athlétisme 72 ne sont plus à travailler ; deux points 58,8 / trois points 55,4 = attaque principale du SF [M§7.1]. |
| Lefebvre (PF, A) | garder | Gain +0,39 / sem. (28 ans) ; défense 63,7 et athlétisme 62,4 restent sous 70. Rebond 73,9 et deux points 75 approchent ou dépassent le seuil de 75. Aucun choix ne rapportera beaucoup plus. |
| Fournier (C, A) | garder | Rebond 61,0 / défense 56,6 = défense principale du C (défense + rebond) [M§7.1]. Gain conforme. |
| Boyer (PG, B) | garder | Passe 46,1 / dribble 55,8, les deux à 15 au PS du PG, cœur du poste. |
| Henry (SG, B) | garder | Trois points 37 / deux points 41 : attaque principale du SG. Gain +0,50 / sem. (26 ans, potentiel 4–5) : quel que soit le choix, l'effet sera minime. |
| Durand (SF, B) | garder | Deux points 40,1 et défense 35,8 : ses 2 compétences à 15 les plus basses, au cœur du SF. |
| Legrand (PF, B) | garder | Rebond 53,1 / défense 47,5 = défense principale du PF. Potentiel 8–9 : bon rendement (+1,30 / sem.). |
| Klein (C, B) | garder | Rebond 35,8 (poids 15) est sa grosse faiblesse au C ; gain faible (+0,26, 28 ans), mais c'est le meilleur usage. |
| Bernard (C, amicaux) | garder | C-002 appliqué il y a 1 semaine ; rebond +2,20 et athlétisme +1,10, les gains les plus forts de l'effectif. |
| Baron (PG, amicaux) | garder | Passe 53 / défense 40,6, deux compétences à 15 au PG. |
| Leclerc (SG, amicaux) | garder | Trois points 39,2 / défense 41,6, deux compétences à 15 au SG. |
| Lecomte (SF, amicaux) | garder | Défense 36,3 / athlétisme 33,2, deux compétences à 15 au SF, ses plus basses. |
| Fontaine | — | 30 ans : l'entraînement n'apporte plus rien [M§8.5]. |

**Pourquoi ne rien changer pour le dernier entraînement de la saison** (avis) : les compétences sont conservées en saison 2, donc le 25/10 compte comme n'importe quelle semaine. Il faut 4 à 5 semaines pour juger un choix [Com 2026-09-01], et aucun critère 1 à 3 ne se déclenche.

**Endurance et moteur v4** (question posée) : fatigue après un match = minutes × 0,19 × agressivité × (1,5 − 0,008 × endurance) [M§5.6]. Calcul SQL : **+1 point d'endurance = −0,7 à −0,8 % de fatigue par match**, soit −0,04 point pour 24 min. Une semaine d'endurance en principale (+0,4 à +2,2 selon le joueur) changerait donc la fatigue de moins de 2 %. L'endurance n'agit dans aucune action de match [M§7.1], et elle pèse 10 dans le PS contre 15 pour les compétences choisies. Avis : **pas d'endurance cette semaine**. À reconsidérer en saison 2 seulement si un titulaire reste au-dessus de 20 de fatigue au coup d'envoi (zone jaune) malgré les unités de 24 min.

**À préparer pour la saison 2** (avis, pas un conseil à saisir maintenant) :
- Bernard : son rebond (61) atteindra 70 vers la 4e semaine de S2, puis 75 (×0,88). Ses deux points (34, poids 15, attaque principale du C [M§7.1]) seront alors la suite logique.
- Gimenez : deux points 58,8 et trois points 55,4 restent loin de 70, rien à changer avant plusieurs saisons.
- Richard : passe 62,8 atteindra 70 vers la fin de S2.

### Rappel de saisie
Sauvegarder avant **dimanche 25/10, 04:00 (Paris)** [Obs]. Puis exporter la page Entraînement après le passage (relevé du 25/10) : 2e semaine précise, médiane possible pour chaque joueur.

---

## 3. Conseils suivis
- **C-002** (Gimenez secondaire trois points, Bernard secondaire athlétisme) : appliqué, et pris en compte par l'entraînement du 18/10 (gains mesurés, voir § 2). Effet : conforme au gain attendu.
- **C-011** (nouveau) : garder tous les choix pour l'entraînement du 25/10. Critère : relevé du 25/10 dans `silver.bv_player_weekly`, `training_primary` / `training_secondary` identiques à la fiche ci-dessus.

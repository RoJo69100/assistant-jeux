# Brief Entraînement BasketVibe — 2026-11-26 11:48 Paris (Chomelix Cow)

Aucun achat ni vente. Deux questions : plan de Bernard (conseil d'un joueur expérimenté) et réglage de Cousin (futur signé). Brief amont : `2026-11-25-entrainement.md` (delta : rien de nouveau en base depuis le relevé du 22/11, `silver.bv_player_weekly` jour 2026-11-26, semaine 2026-11-22). Prochain passage : **dim. 29/11 04:00 (Paris)**, sauvegarde à faire **aujourd'hui**.

## 1. Fiche de saisie (aujourd'hui)
| Joueur | Réglage actuel | À saisir aujourd'hui | Décision |
|---|---|---|---|
| Bernard (C, 18) | Principale Rebond / secondaire Athlétisme | **Principale Deux points / secondaire Défense** | CHANGER |
| Cousin (SG, 17), dès la signature | — | **Principale Athlétisme / secondaire Trois points** | À SAISIR (si signé avant dim. 04:00) |
| Les 11 autres | voir brief du 25/11 | inchangés | garder |

## 2. Bernard : faits
- `gold.bv_roster_now` (semaine 2026-11-22, jour 2026-11-26) : C, 18 ans, PS 48,8 ; 2PT 34, 3PT 34, Déf 52, Passes 44, Dribble 51, Rebond 72, Endurance 35, Athlé 58.
- Entraînement : principale Rebond, secondaire Athlétisme (`silver.bv_player_weekly`). Gains 2,20 / 1,10 aux 6 semaines mesurées, écart 0 (`gold.bv_potential_estimate`) : potentiel **10, confiance élevée** (âge 18, règle manuel). L'utilisateur avait raison sur le 10.
- Poids PS du C (`gold.bv_training_options`) : 2PT 0,15 · Déf 0,15 · Rebond 0,15 · Athlé 0,15 · 3PT, Passes, Dribble, Endurance 0,10 (somme 1,00 ; contrôle : 48,8).
- `gold.bv_training_options` : multiplicateur de niveau du Rebond à 72 = **0,952** (interpolation de la vue entre ×1 à 70 et ×0,88 à 75 ; le manuel ne donne que les paliers : hypothèse).

## 3. Bernard : règles et méthode
- Gain par entraînement = base (principale 1,0 ; secondaire 0,5) × multiplicateur de potentiel (10 : 2,20) × facteur d'âge × multiplicateur de niveau avant l'entraînement [M§8.2, §8.3, §8.4].
- Ralentissement : ×1 sous 70, ×0,88 à 75, ×0,75 à 80, ×0,63 à 85, ×0,50 à 90, ×0,21 à 95 [M§8.4] ; interpolation linéaire entre paliers (hypothèse de la vue).
- Facteur d'âge : 1,0 jusqu'à 18 ans (manuel) ; 19 ans 0,94 et 20 ans 0,89 (`gold.bv_age_factor`, **hypothèse d'interpolation**).
- Calendrier supposé (hypothèse, ~8 entraînements par saison [M§1.3]) : 16 entraînements à partir du 29/11 = 4 à 18 ans (jusqu'au 20/12), 8 à 19 ans, 4 à 20 ans. Variante « sans baisse d'âge » (facteur 1,0 partout) donnée en fourchette.
- Calcul : récursion SQL (`python -I pipelines/sql.py`, CTE sur les valeurs de `gold.bv_roster_now`), PS = 48,8 + 0,15 × points gagnés sur 2PT, Déf, Athlé, Rebond (autres compétences fixes).

## 4. Bernard : projection à 16 entraînements (2 saisons), potentiel 10
Valeurs de départ : 2PT 34, Déf 52, Athlé 58, Rebond 72, PS 48,8. Cases : valeur après 4 / 12 / 16 entraînements.

| Plan (principale/secondaire) | 2PT | Défense | Athlétisme | Rebond | PS C à 4 / 12 / 16 | PS à 16, sans baisse d'âge |
|---|---|---|---|---|---|---|
| **B 2PT / Déf** | 42,8 / 59,3 / **67,2** | 56,4 / 64,7 / **68,6** | 58 (fixe) | 72 (fixe) | 50,8 / 54,5 / **56,3** | 56,7 |
| A 2PT / Athlé | 42,8 / 59,3 / 67,2 | 52 (fixe) | 62,4 / 70,7 / **74,4** | 72 (fixe) | 50,8 / 54,5 / **56,2** | 56,7 |
| C Déf / Athlé | 34 (fixe) | 60,8 / 76,9 / **82,9** | 62,4 / 70,7 / 74,4 | 72 (fixe) | 50,8 / 54,4 / **55,9** | 56,2 |
| E 2PT / Rebond | 42,8 / 59,3 / 67,2 | 52 (fixe) | 58 (fixe) | 76,0 / 82,5 / **85,1** | 50,7 / 54,2 / **55,7** | 56,1 |
| D actuel Rebond / Athlé | 34 (fixe) | 52 (fixe) | 62,4 / 70,7 / 74,4 | 79,7 / 90,2 / **93,4** | 50,6 / 53,4 / **54,5** | 54,7 |

PS C à 16 pour B : 56,3 contre 54,5 pour garder le plan actuel : **+1,8 point**, sans aucun ralentissement (2PT 67,2 et Déf 68,6 restent sous 70). Le plan actuel gaspille : le Rebond passe 80 dès le 4e entraînement (79,7), puis ×0,63 à 85 et ×0,50 à 90. Tous les plans qui évitent le ralentissement donnent presque le même PS (55,9 à 56,3) : le total de points (≈ 49,8 sur 16 entraînements = 3,3 × 15,08 d'âge cumulé) × 0,15 = +7,5 est le plafond du PS pour ce joueur.

## 5. Bernard : verdict sur l'avis du joueur expérimenté
- **Arrêter le Rebond : oui.** À 72 il ralentit déjà (×0,952), et il tombera à ×0,88 dès 75 (74,2 au 29/11 si on garde, C-129) ; les points mis sur 2PT (34) et Déf (52) rapportent autant de PS sans pénalité.
- **2PT en principale : oui.** C'est la compétence la plus basse parmi les 4 à poids 0,15 ; l'emplacement C a pour attaque 2PT + Rebond et pour défense Défense + Rebond [M§7.1].
- **Secondaire Défense plutôt qu'Athlétisme : oui, de justesse.** PS identique (56,3 contre 56,2) ; Défense (52) est sous 70 pendant toute la période, alors que l'Athlé secondaire franchit 70 vers le 12e entraînement (70,7) et subit un ralentissement. Défense est aussi une compétence principale du C en défense [M§7.1] ; l'Athlé reste « secondaire partout ». Athlé 58 se rattrape plus tard (l'écart de 0,1 PS est dans le bruit).
- **« 4 compétences clés à 70+ en 2 saisons » : faux.** Avec 2PT/Déf, on finit à 2PT 67,2, Déf 68,6, Athlé 58 : seul le Rebond (72, non entraîné) est à 70+. Pour amener 2PT (+36), Déf (+18) et Athlé (+12) à 70 il faut 66 points, soit ≈ 21 entraînements (≈ 2,7 saisons). Leur propre simulation donne 2PT 51 : l'objectif n'y est pas atteint non plus.
- **Leur simulation** (2PT 34→51, Déf 52→69, Athlé 58→74, soit 17+17+16 = 50 points) correspond à mon total (49,8). Leur PS 49→56–58 : **56 est atteignable (56,3), 58 non** (maximum 56,7 sans aucune baisse d'âge). Ils font tourner les trois compétences ; le PS ne dépend que du total de points non ralentis, donc la rotation ne change rien, et la saisie la plus simple est un plan fixe.
- Confiance : **moyenne**. Sûr : potentiel 10 et facteur d'âge 1,0 à 18 ans. Hypothèses : facteur d'âge à 19 et 20 ans, calendrier de saison, interpolation du ralentissement. Le PS n'est pas la performance en match (voir ci-dessous).

## 6. Bernard : ce qui change dans les conseils ouverts
- **C-129** (garder le Rebond tant que < 75) est **remplacé pour Bernard** par C-142 ci-dessous. Le test de l'interpolation (gain du 29/11 à 2,095 au lieu de 2,20 si le Rebond était gardé) n'est plus mesurable si on change ; la mesure de remplacement est 2PT/Déf à +2,20 / +1,10.
- Les 11 autres réglages de C-129 restent inchangés.

## 7. Cousin (SG 17) : faits
Source : bronze page 81633 (champ `text`, lu via `--page-id 81633 --payload-path text`) ; tests faits, High potential (★★★★), fourchettes de 10. Contredit les fourchettes de 20 de `gold.bv_academy_prospects` (rapport non testé), qui ne servent plus.

| Compétence | Fourchette | Poids PS du SG |
|---|---|---|
| 2PT | 45–55 | 0,15 |
| 3PT | 44–54 | 0,15 |
| Défense | 45–55 | 0,15 |
| Passes | 34–44 | 0,10 |
| Dribble | 44–54 | 0,15 |
| Rebond | 27–37 | 0,05 |
| Endurance | 40–50 | 0,10 |
| Athlétisme | 33–43 | 0,15 |

PS SG : **bas 40,4 / milieu 45,4 / haut 50,4** (calcul pondéré ; la page affiche 40–50). Poids SG vérifiés : Leclerc 43,0 = calcul (`gold.bv_training_options`). Effectif : Bonnet 52,1 (26 ans), Leclerc 43,0 (17 ans, potentiel 8, confiance élevée) (`gold.bv_roster_now`, `gold.bv_potential_estimate`).
- **Potentiel** : High = 8 à 10 [M§8.3, §4.2]. Je projette P8 (×1,60) et P10 (×2,20). Âge 17 : facteur 1,0 (manuel). À partir du 13e entraînement 19 ans : 0,94 (hypothèse). Départ des compétences : valeur réelle inconnue dans la fourchette, donc trois cas (bas, milieu, haut) appliqués aux 3 compétences travaillées (3PT, Athlé, Déf).

## 8. Cousin : projection du PS SG à 16 entraînements (2 saisons)
Plan recommandé **X Athlétisme / 3 points** ; PS projeté (départ bas / milieu / haut) :

| Potentiel | PS SG départ (bas / milieu / haut) | PS à 16 entraînements (bas / milieu / haut) | Gain |
|---|---|---|---|
| P8 (×1,60) | 40,4 / 45,4 / 50,4 | **46,1 / 51,1 / 56,1** | +5,7 |
| P10 (×2,20) | 40,4 / 45,4 / 50,4 | **48,2 / 53,2 / 58,1** | +7,8 |

Valeurs du plan X au milieu : P8 3PT 61,6, Athlé 63,2, Déf 50 ; P10 3PT 66,3, Athlé 72,6, Déf 50 (le P10 passe le ralentissement de 70 sur l'Athlé).

Comparaison de réglages (PS à 16, milieu ; bas–haut) :
| Réglage | P8 | P10 |
|---|---|---|
| X Athlé / 3PT (ou V Athlé / Déf : identique) | 51,1 (46,1–56,1) | 53,2 (48,2–58,1) |
| Y 3PT / Athlé (ou Z 3PT / Déf) | 51,1 (46,1–56,0) | 52,9 (48,1–57,7) |

La différence entre réglages est ≤ 0,4 PS : le gain vient du total de points, pas du choix. 3PT en principale franchit 70 (74,1 en P8, 81,9 en P10 : ralentissement), l'Athlé en principale reste sous 70 en P8.

Comparaison à 16 entraînements, même méthode :
| Joueur | PS aujourd'hui | PS à 16 |
|---|---|---|
| Bonnet (26 ans, plan Déf / Dribble actuel, potentiel 7 ou 8, facteur d'âge hypothèse 0,49 / 0,37 / 0,24) | 52,1 | **54,1–54,2** |
| Leclerc (17 ans, 3PT / Déf, potentiel 8) | 43,0 | **48,7** (3PT 72,4 ralenti, Déf 58,2) |
| Cousin P8 / P10 (milieu) | 45,4 | 51,1 / 53,2 |

Lecture : Cousin dépasse Leclerc de ~2 à 4,5 PS à 16 entraînements au milieu. Il n'égale Bonnet (≈ 54,2) que dans la moitié haute de la fourchette (56,1 en P8-haut ; 58,1 en P10-haut) ; au milieu il reste 1 à 3 points dessous. Il ne remplace donc pas Bonnet avant la 3e saison, sauf bonne surprise. Aujourd'hui (40,4–50,4) il est sous Bonnet dans tous les cas.

## 9. Cousin : réglage dès la signature, et pourquoi
**Saisir principale Athlétisme, secondaire Trois points** (confiance basse à moyenne).
- L'Athlétisme est sa compétence la plus basse (33–43) à poids 0,15 : elle progresse à plein rendement le plus longtemps (sous 70 jusqu'au bout en P8). Le 3PT (44–54) est la compétence principale de l'emplacement SG avec le 2PT [M§7.1], et en secondaire il reste sous 70 en P8 (61,6).
- Il évite le doublon avec Leclerc (3PT / Déf) : pas de comparaison de potentiel biaisée.
- L'Athlétisme sert dans presque toutes les actions de match [M§7.1] ; l'endurance n'est pas utile en match [M§7.1].
- À la première semaine mesurée, `gold.bv_potential_estimate` donnera `implied_mult` : 1,60 = P8, 1,85 = P9, 2,20 = P10 (âge 17, règle manuel, confiance élevée dès 1 semaine). Si P10 se confirme, garder ; sinon pas de changement non plus (écart de réglages ≤ 0,4 PS).
- Condition : sauvegarder avant dim. 29/11 04:00 ; si Cousin n'est pas dans l'effectif au relevé suivant, rien à saisir. Un joueur signé après 04:00 manque l'entraînement du 29/11 (hypothèse d'ordre : je n'ai pas de règle écrite sur ce cas).
- Coût caché (brief Académie du 26/11, non refait ici) : signer divise la jauge par ~2 [M§4.2]. C-141 disait d'ignorer les 3 prospects (seuil 48 posé par l'agent, non par l'utilisateur) ; le choix de signer relève de l'utilisateur.

## 10. Ce qui prouverait que j'ai tort
- Bernard, relevé du 29/11 : gain 2PT différent de +2,20 ou Déf de +1,10 de plus de 0,15 = réglage non sauvegardé ou facteur d'âge faux ; réglage lu différent de 2PT/Déf = ressaisir.
- Bernard, 2PT à 4 entraînements (20/12) ≠ 42,8 (± 0,6) = potentiel ou facteur d'âge faux.
- Cousin : gain principal Athlé de la 1re semaine ≠ 1,60 / 1,85 / 2,20 (±0,15) = potentiel hors High 8–10, ou départ non entier.
- PS de Cousin hors de 46–58 à 16 entraînements = fourchette de 10 mal lue.
- Facteur d'âge de 19 ans ≠ 0,94 : seuls les 4 derniers entraînements changent (±1 PS au plus).

## Conseils suivis
- **C-142** ajouté (Bernard 2PT / Déf), **C-143** ajouté (Cousin Athlé / 3PT). **C-129** : remplacé pour Bernard. **C-056** : déjà confirmé.

## Hypothèses à confirmer par l'utilisateur ou par mesure
1. Longueur de saison de 8 entraînements et date du +1 an (je suppose 20/12 → 27/12).
2. Facteur d'âge à 19 et 20 ans (0,94 / 0,89, interpolation).
3. Départ réel de Cousin dans les fourchettes de 10 points.

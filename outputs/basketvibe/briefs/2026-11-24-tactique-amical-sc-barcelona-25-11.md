Amical contre SC Barcelona (25/11)
Verrou : mer. 25/11 07:45 (match 08:00)
Adversaire : SC Barcelona (joueurs inconnus)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Durand | Legrand | Bernard |
| Q2 | Boyer | Leclerc | Durand | Legrand | Fournier |
| Q3 | Baron | Leclerc | Boyer | Fournier | Bernard |
| Q4 | Baron | Durand | Legrand | Fournier | Bernard |
| Prol. | Baron | Leclerc | Durand | Legrand | Bernard |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | PG | PG | 36 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | SF | — | — | 24 | 3 | 3 | 3 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SG | SG | — | SG | 36 | 3 | 3 | 3 | 3 |
| Durand | SF | SF | SF | — | SG | SF | 36 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | PF | — | SF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | — | C | C | C | 36 | 3 | 3 | 3 | 3 |
| Fournier | C | — | C | PF | PF | — | 36 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 | tous | 3 (Normal) | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Agress. = 3 pour chacun des 12 joueurs
- [ ] Off. focus = 3, Rôle = 3, Tir = 3 pour les 12 joueurs
- [ ] Min : Boyer 24 ; Baron, Leclerc, Durand, Legrand, Bernard, Fournier 36 ; Albano, Richard, Bonnet, Gimenez, Lefebvre 0
- [ ] Albano (en vente) absent de tous les quarts et de la prolongation
- [ ] Les 12 adversaires : focus 3, zone Perimeter (1)
## À exporter ensuite
La page du match, après la fin du match (~08:55 le 25/11) : elle donnera les noms adverses.
---
## Annexe — pourquoi

Correction du 24/11 (Paris 08:42, `pipelines/heure_paris.py`) de la fiche du 23/11 ; amical du 25/11 08:00, pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Aucun brief Match du jour lu : signalé.

### Ce qui change
- Boyer : fatigue 21,33 (`gold.bv_roster_now`, relevé du 23/11) ; minutes 36 → 24 (Q2 PG, Q3 SF ; plus de Q1 ni de prolongation).
- Albano : `on_transfer_list` = True (`gold.bv_roster_now`) ; sa vente est au plan du jour : 0 min, absent de tous les quarts (il jouait 36 min dans la fiche du 23/11).
- Conséquence : sans Albano ni les 4 autres de la ligue, il faut un 7e joueur (20 emplacements, 3 quarts max par joueur). Fournier (C, fatigue 19,62) prend 36 min : le moins coûteux des cinq de la ligue (rang 3 au C, 27 min en ligue, `gold.bv_fatigue_plan`/plan du jour). Durand passe de 24 à 36 (fatigue 10,34). Risque : Fournier garde de la fatigue pour la ligue J11 du 25/11 19:45 ; surcoût amical ≈ 1/10, non mesuré en vue. Avis, confiance moyenne.

### Test E1 niveau A et réglage neutre
Un seul test, E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2, équilibrée) sur les 12, y compris ceux à 0 min. Neutre (yaml `neutre` et constants E1) : zone Perimeter (1), focus 3 sur les adversaires, Off. focus 3 (aucun Primary), aucun Tir cran 4. Rôle 3 et Tir 3 : non fixés par le yaml, mis à 3 pour qu'aucune autre variable ne bouge. L'agressivité du test égale le neutre : aucune valeur isolée. L-004 (agressivité 1) non appliqué : le test impose le niveau A. Conseil C-134 déjà dans `outputs/basketvibe/learnings.md` (test inchangé) ; aucun nouveau conseil.

### Contrôle SQL (plan en `values` joint à `gold.bv_slot_fit`)
- 20 lignes Q1–Q4 : 20 couples (quart, joueur) distincts, 5 joueurs différents par quart, un par emplacement.
- Max 3 quarts par joueur (Baron, Leclerc, Durand, Legrand, Bernard, Fournier 3 ; Boyer 2) ; 36 min max hors prolongation.
- `height_eff` minimum 99,2 (Boyer SF, Legrand SF) ≥ 95 ; `fit_with_form` de 41,3 à 56,4 (Leclerc/Durand bas : amical de formation).
- En vente ou blessés dans le plan : 0 (`on_transfer_list`, `injury_return_on`).
- Minutes : 6 × 36 + 24 = 240.
- Fatigue (`gold.bv_roster_now`, 23/11) : Boyer 21,33 (réduit), Fournier 19,62, Legrand 18,85, Bernard 15,79, Durand 10,34, Leclerc 3,96, Baron 3,32. Forme à jour (relevé du 23/11 postérieur au 22/11).

### Adversaire : SC Barcelona
Aucune ligne contre lui dans `gold.bv_saisie_adversaires` ni `gold.bv_match_report` (fiche du 23/11, non recontrôlé). Joueurs, parts de tirs, 2P/3P inconnus ; amical : aucun aperçu à demander.
**Focus défensif** : aucun joueur adverse connu : Normal (3) sur les 12, zone Perimeter (neutre E1), aucun Intense, Light ni Give up. Export : la page du match après ~08:55 le 25/11.

### Blessés et plan B
Aucun blessé (`injury_return_on` vide, 12 joueurs). Pas de blessure en amical [M§1.2]. Plan B : sans objet.

### Transferts
Aucun achat, vente ni enchère exécuté ici (règle 2). « Pas d'enchère avant le test ; Police : ne pas acheter — tester le potentiel » (plan du jour, Orlando Rinaldi, test 25 000 : proposition seulement). Aucune somme au-dessus de 250 000 dans cette fiche.

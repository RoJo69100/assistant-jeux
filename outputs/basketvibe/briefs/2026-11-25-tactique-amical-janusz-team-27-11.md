Amical contre Janusz Team (27/11)
Verrou : ven. 27/11 07:45 (match 08:00, à domicile) — pas de preset, composition de TEST, sauvegarde du match ; à saisir aujourd'hui 25/11
Adversaire : Janusz Team (inconnu : aucun joueur en base, aucun aperçu en amical) — test E1 niveau A, agressivité 3 à l'écran (cran 2) sur tous
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Durand | Legrand | Bernard |
| Q2 | Boyer | Richard | Gimenez | Fournier | Bernard |
| Q3 | Baron | Leclerc | Durand | Legrand | Fournier |
| Q4 | Boyer | Richard | Gimenez | Legrand | Fournier |
| Prol. | Boyer | Richard | Gimenez | Legrand | Fournier |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | — | — | 24 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | — | PG | PG | 24 | 3 | 3 | 3 | 3 |
| Richard | PG | — | SG | — | SG | SG | 24 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | — | SG | — | — | 24 | 3 | 3 | 3 | 3 |
| Durand | SF | SF | — | SF | — | — | 24 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | SF | — | SF | SF | 24 | 3 | 3 | 3 | 3 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | — | PF | PF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | C | — | — | — | 24 | 3 | 3 | 3 | 3 |
| Fournier | C | — | PF | C | C | C | 36 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 de Janusz Team | tous | 3 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Min : Legrand 36, Fournier 36, Baron 24, Boyer 24, Richard 24, Leclerc 24, Durand 24, Gimenez 24, Bernard 24 ; Bonnet, Lefebvre, Albano 0
- [ ] Agress. = 3 pour les 12 ; Off. focus 3, Rôle 3, Tir 3 pour les 12
- [ ] Albano absent des 5 quarts ; aucun joueur au-delà de 36 min
- [ ] Adversaires : focus 3, zone Perimeter (1) partout
## À exporter ensuite
La page du match amical Janusz Team (27/11) une fois sauvegardé, avant 07:45.
---
## Annexe — pourquoi

### Test (un seul)
E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2) sur les 12. Tout le reste au neutre du fichier : zone Perimeter, focus défensif 3 constant, aucun joueur en Tir 5 (neutre : au plus 1), aucun Primary (Off. focus 3 partout). Rôle 3 et Tir 3 uniformes : pas de réglage individuel qui brouille la lecture. Attendu dans `gold.bv_amical_reglage` : `agress_cran` = 2, `agress_uniforme` = true. Les amicaux déjà vérifiés de E1 : non relus ici (c'est le suivi du plan du jour).

### Exclusion demandée
La consigne est tronquée (« 1) ») : un seul nom me parvient par la base, Albano (`gold.bv_roster_now.on_transfer_list` = true, 0 min). Les autres noms de la liste manquent : si d'autres joueurs sont proposés à la vente, dis-les, la fiche est à refaire. Aucune vente exécutée.

### Choix de composition (amical : jeunes d'abord, titulaires de ligue ménagés ; `gold.bv_roster_now`, relevé du 24/11)
- Repos total : Bonnet (fatigue 21,58) et Lefebvre (20,62), les deux plus fatigués ; Albano exclu.
- Jeunes en minutes (expérience, [M§5.4]) : Baron 17 ans, Leclerc 17, Bernard 18, Boyer 20.
- Ligue Žirmūnai 25/11 et samedi 28/11 : les titulaires jouent 24 min seulement (Richard, Gimenez).
- Forme : relevé du 24/11, après le dimanche 22/11 : à jour [M§5.5].

### Contrôle SQL (25/11, plan en `values` joint à `gold.bv_slot_fit`, `gold.bv_fatigue_plan`)
- Version avec Bernard en Q4 : 4 quarts, 5 joueurs différents, 20/20 emplacements trouvés, `height_eff` minimum 100,0 ; `fit_with_form` moyen Q1 45,9, Q2 56,5, Q3 47,3, Q4 55,6. Changement final : Fournier C en Q4 à la place de Bernard (Fournier C : height_eff 100,0, fit 56,4) : non relancé en bloc ; Q4 ≈ 57 par calcul.
- Minutes : total 240, aucun au-delà de 36. Fatigue stabilisée à tier 2 : Legrand 36 min = 19,0 ; Fournier 36 = 19,2 ; Bernard 24 = 14,1 ; Baron 24 = 14,2 ; Leclerc 12,7 ; Boyer 12,5 ; Gimenez 11,9 ; Richard 11,4 ; Durand 11,0. Bernard à 36 min aurait donné 23,7 : d'où 24. Le plan ne compte pas les amicaux (≈ 1/10).
- Aucun blessé (`injury_return_on` vide pour les 12) ; aucun en vente dans les cinqs (Albano à 0).
- Qualité : fit faible en Q1 et Q3 (Leclerc SG 41,3, Durand SF 42,1, Baron PG 44,7) : accepté, amical d'expérience sans blessure [M§1.2].

### Focus défensif
Janusz Team : aucun joueur en base (`gold.bv_saisie_adversaires` : 0 ligne), aucun aperçu en amical. Focus neutre : Normal (3) pour tous, zone Perimeter (neutre E1), aucun Intense, Light ni Give up [fiche tactique § 2 quater]. Export à faire : la page du match, pour connaître ses joueurs. Aucun test du focus par joueur (arbitrage 15).

### Blessés et plan B
Aucun blessé ; pas de blessure en amical [M§1.2]. Plan B : PG Baron → Richard (57,4) ; SG Leclerc → Bonnet (54,2) ; SF Durand → Gimenez (69,3) ; PF Legrand → Lefebvre (67,6) ; C Bernard → Fournier (56,4).

### Valeurs qui s'écartent de la règle uniforme
Agress. 3 au lieu de 1 : c'est le test E1 A demandé (L-032 : aucun gain de l'agressivité 1). Aucune autre valeur isolée.

### Évolution
Garde : 36 min max, agressivité 3. Teste : E1 A. Conseil **C-140** ajouté dans `learnings.md`.

Amical contre Saile C.B. (28/11)
Verrou : sam. 28/11 07:45 (match 08:00, à domicile) — pas de preset, composition de TEST, sauvegarde du match ; à saisir aujourd'hui 27/11
Adversaire : Saile C.B. (14 joueurs en base, `gold.bv_saisie_adversaires`) — test E1 niveau A, agressivité 3 à l'écran (cran 2) sur tous
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Bourdon | Legrand | Bernard |
| Q2 | Boyer | Richard | Gimenez | Fournier | Bernard |
| Q3 | Baron | Leclerc | Bourdon | Legrand | Fournier |
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
| Bourdon | SF | SF | — | SF | — | — | 24 | 3 | 3 | 3 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | SF | — | SF | SF | 24 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | — | PF | PF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | C | — | — | — | 24 | 3 | 3 | 3 | 3 |
| Fournier | C | — | PF | C | C | C | 36 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 14 de Saile C.B. | tous | 3 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Min : Legrand 36, Fournier 36 ; Baron, Boyer, Richard, Leclerc, Bourdon, Gimenez, Bernard 24 ; Bonnet, Durand, Lefebvre 0
- [ ] Agress. = 3 pour les 12 ; Off. focus 3, Rôle 3, Tir 3 pour les 12
- [ ] Durand absent des 5 quarts ; aucun joueur au-delà de 36 min
- [ ] Adversaires : focus 3 et zone Perimeter (1) pour les 14
## À exporter ensuite
La page du match amical Saile C.B. (28/11) une fois sauvegardé, avant 07:45.
---
## Annexe — pourquoi

### Test (un seul)
E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2) sur les 12. Tout le reste au neutre du fichier : zone Perimeter, focus 3, au plus 1 joueur en Tir 5 (ici 0), aucun Primary (Off. focus 3). Rôle 3 et Tir 3 uniformes : pas de réglage individuel qui brouille la lecture. Attendu dans `gold.bv_amical_reglage` : `agress_cran` = 2.

### Exclusion demandée
Jonathan Durand : 0 minute, absent des 5 quarts, listé à 0 dans l'écran 2 pour que sa ligne soit complète. Aucune vente exécutée (règle 2, l'utilisateur exécute). Aucun montant ici : pas de « police requise » à poser.

### Choix de composition (amical : jeunes d'abord, titulaires de ligue ménagés ; `gold.bv_roster_now`, relevé du 27/11, semaine du 22/11)
- Repos total : Bonnet (fatigue 20,35) et Lefebvre (19,43), titulaires de la ligue du soir (28/11 20:00, `gold.bv_agenda`).
- Jeunes en minutes [M§5.4] : Baron 17 ans, Leclerc 17, Bourdon 16 (nouveau, fatigue 0), Bernard 18, Boyer 20.
- Richard et Gimenez : 24 min seulement avant la ligue du soir.
- Forme : relevé du 27/11, semaine du 22/11 (dimanche passé) : à jour [M§5.5].

### Contrôle SQL (27/11, `gold.bv_slot_fit`, `gold.bv_fatigue_plan` tier 2)
- 4 quarts + prolongation, 5 joueurs différents chacun, 20/20 emplacements trouvés ; `height_eff` minimum 98,4 (Bourdon SF) ; tous les autres à 100,0 : tous ≥ 95.
- `fit_with_form` : Baron PG 44,7, Leclerc SG 41,3, Bourdon SF 50,9, Legrand PF 51,9, Bernard C 49,3 (Q1) ; Boyer PG 50,6, Richard SG 56,9, Gimenez SF 69,3, Fournier PF 56,4, Bernard C 49,3 (Q2). Fit faible sur Baron et Leclerc : accepté, amical d'expérience sans blessure [M§1.2].
- Minutes : total 240, aucun au-delà de 36. Fatigue stabilisée (plan, tier 2) : Legrand 36 min = 19,0 ; Fournier 36 = 19,2 ; Bernard 24 = 14,1 ; Baron 14,2 ; Leclerc 12,7 ; Boyer 12,5 ; Gimenez 11,9 ; Bourdon 11,6 ; Richard 11,4. Tous ≤ 20 ; le plan ne compte pas les amicaux (≈ 1/10).
- Fatigue estimée au coup d'envoi (relevé 27/11 − (0,5 + 10 %) par nuit, 1 nuit) : Legrand ≈ 13, Fournier ≈ 15,7, Bernard ≈ 13,6, Boyer ≈ 16, Richard ≈ 15,8, Gimenez ≈ 16 : tous sous 20.
- Aucun blessé (`injury_return_on` vide pour les 12) ; aucun en vente dans les cinqs.

### Focus défensif
Saile C.B. : 14 noms en base (`gold.bv_saisie_adversaires`, export 25/11) : Acevedo, Corbellini, Estrada (PG) ; Altamirano, Landi, Sabonis (SG) ; Balodis, Maldonado, Paredes (SF) ; Aguilar, Aguirre, Lee (PF) ; Castillo, Esteban (C). Parts de tirs, 2P/3P : inconnues (aucun match passé contre lui, aucun aperçu de ses statistiques, `gold.bv_match_opp_focus` non disponible). Donc focus neutre : Normal (3) pour tous, aucun Intense, Light ni Give up, zone Perimeter (neutre E1) [fiche tactique § 2 quater]. Export à faire : la page du match. Pas de test du focus par joueur en amical (arbitrage 15).

### Blessés et plan B
Aucun blessé ; pas de blessure en amical [M§1.2]. Plan B : PG Baron → Richard (57,4) ; SG Leclerc → Bonnet (54,2) ; SF Bourdon → Gimenez (69,3) ; PF Legrand → Lefebvre (67,6) ; C Bernard → Fournier (56,4). Durand exclu : pas de remplaçant à prévoir.

### Valeurs qui s'écartent de la règle uniforme
Agress. 3 au lieu de 1 : c'est le test E1 A demandé (L-032 : aucun gain de l'agressivité 1). Aucune autre valeur isolée.

### Évolution
Garde : 36 min max, agressivité 3 uniforme. Teste : E1 A. Conseil **C-147** ajouté dans `learnings.md`.

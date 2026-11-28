Amical contre LA TreePlanter (29/11)
Verrou : dim. 29/11 07:45 (match 08:00, à domicile) — pas de preset, composition de TEST, sauvegarde du match ; à saisir aujourd'hui 28/11
Adversaire : LA TreePlanter (14 joueurs connus, aucun match passé en base) — test E1 niveau A, agressivité 3 à l'écran (cran 2) sur les 12
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Bourdon | Legrand | Bernard |
| Q2 | Baron | Leclerc | Bourdon | Legrand | Bernard |
| Q3 | Boyer | Leclerc | Bourdon | Fournier | Bernard |
| Q4 | Baron | Boyer | Gimenez | Legrand | Fournier |
| Prol. | Boyer | Richard | Gimenez | Legrand | Fournier |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | PG | — | PG | — | 36 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | — | PG | SG | PG | 24 | 3 | 3 | 3 | 3 |
| Richard | PG | — | — | — | — | SG | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SG | SG | — | — | 36 | 3 | 3 | 3 | 3 |
| Bourdon | SF | SF | SF | SF | — | — | 36 | 3 | 3 | 3 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | — | — | SF | SF | 12 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | PF | — | PF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | C | C | — | — | 36 | 3 | 3 | 3 | 3 |
| Fournier | C | — | — | PF | C | C | 24 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 14 joueurs de LA TreePlanter (Baker, Bass, Murray, Johnson, Kennedy, Rivas, Côté, Green, Mason, Bailey, Freeman, Lee, McCoy, Parker) | tous | 3 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Min : Baron, Leclerc, Bourdon, Legrand, Bernard 36 ; Boyer, Fournier 24 ; Gimenez 12 ; Richard, Bonnet, Lefebvre, Durand 0
- [ ] Agress. = 3 pour les 12 ; Off. focus 3, Rôle 3, Tir 3 pour les 12
- [ ] Durand absent des 5 lignes de l'écran 1 ; aucun joueur à plus de 36 min
- [ ] Adversaires : focus 3 et zone Perimeter (1) pour les 14
## À exporter ensuite
La page du match amical LA TreePlanter (29/11) une fois sauvegardé, avant 07:45 ; après le match (~08:55), la page du match pour lire le test.
---
## Annexe — pourquoi

### Test (un seul)
E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2) sur les 12. Tout le reste au neutre du fichier : zone Perimeter, focus 3, aucun joueur en Tir 5 (max 1), aucun Primary (Off. focus 3). Rôle 3 et Tir 3 uniformes : rien d'autre ne brouille la lecture. Attendu dans `gold.bv_amical_reglage` : `agress_cran` = 2, `agress_uniforme` vrai. Valeur isolée : Agress. 3 au lieu de 1 = le test demandé (L-032 : aucun gain de l'agressivité 1, L-004). Moteur v5 (amical).

### Contrôle SQL (requête `values` jointe à `gold.bv_slot_fit`, 28/11)
20 lignes jointes sur 20 ; 5 joueurs différents par quart (aucun quart « mauvais ») ; max 3 quarts (Baron, Leclerc, Bourdon, Legrand, Bernard) ; `height_eff` minimum 98,4 (Bourdon SF) ≥ 95. `fit_with_form` : Baron PG 44,7 ; Leclerc SG 41,3 ; Bourdon SF 50,9 ; Legrand PF 51,9 ; Bernard C 49,3 ; Boyer PG 50,6 / SG 49,8 ; Fournier PF 56,4 / C 56,4 ; Gimenez SF 69,3. Fit faible (Baron, Leclerc) : accepté, amical d'expérience sans blessure [M§1.2]. Prol. : Legrand passerait à 41 min en cas de prolongation (rare).

### Choix de composition (jeunes d'abord, titulaires de ligue ménagés)
- Jeunes ≤ 21 ans en minutes (expérience plus vite [M§5.4], au dixième en amical [M§5.4]) : Baron 17, Leclerc 17, Bourdon 16, Bernard 18 à 36 min ; Boyer 20 à 24. Bourdon, Baron, Leclerc, Bernard sont des juniors académie : en amical, aucun bonus homegrown (réservé à la ligue, 200 par minute [M§10.1.3]) ; seul l'expérience est gagnée. Coût en PS au poste chiffré ci-dessus.
- Ligue J12 ce soir (28/11 20:00) et J13 (30/11 20:00) : Bonnet, Lefebvre, Richard à 0 ; Gimenez 12 ; Fournier 24 (les 5 titulaires jouent 36 min ce soir, brief `2026-11-27-tactique-chara-legends-28-11.md`).
- Fatigue estimée au coup d'envoi (relevé 27/11 `gold.bv_roster_now`, plan stabilisé à 36 min `gold.bv_fatigue_plan` tier 2) : Gimenez ≈ 20,3, Fournier ≈ 19,2, Richard ≈ 19,5 : zone 20-22, aucune minute coupée (règle du 25/11). Nous ne pouvons pas la mesurer avant J12 : si l'export de J12 (~20:50) montre un joueur du cinq au-delà de 22, le remplacer dans le cinq (Gimenez → Richard 54,0 au SF ; Fournier → Bernard au C).
- Forme : relevé du 27/11 (semaine du 22/11) à jour ; elle change dimanche 04:00 [M§5.5] avant le match : `fit_with_form` indicatif.
- Durand : 0 minute, absent des cinqs, ligne à 0 pour que l'écran soit complet. Sa vente est proposée au plan (fin d'enchère 29/11 15:31, `gold.bv_agenda`) ; je n'exécute rien (règle 2) ; aucun montant.

### Focus défensif
LA TreePlanter : 14 joueurs lus (`gold.bv_saisie_adversaires`, export 29/11) mais aucun match passé contre eux (`gold.bv_match_report` : 0 ligne) : parts de tirs, 2P/3P inconnues. Focus Normal (3) pour tous, aucun Intense, Light ni Give up ; zone Perimeter (1), neutre d'E1 constant [fiche § 2 quater]. Pas de test du focus par joueur en amical (arbitrage 15). Écran 3 : ligne groupée (amical) ; à saisir joueur par joueur dans l'ordre de l'écran : Baker, Bass, Murray, Johnson, Kennedy, Rivas, Côté, Green, Mason, Bailey, Freeman, Lee, McCoy, Parker. Export à faire : la page du match après le match, pour avoir leurs parts de tirs.

### Blessés et plan B
Aucun blessé (`injury_return_on` vide pour les 12, `gold.bv_roster_now`) ; pas de blessure en amical [M§1.2]. Plan B (`fit_with_form`) : PG Baron → Richard 57,4 ; SG Leclerc → Boyer 49,8 ; SF Bourdon → Gimenez 69,3 ; PF Legrand → Fournier 56,4 ; C Bernard → Fournier 56,4. Durand exclu.

### Évolution
Garde : 36 min max, agressivité 3 uniforme (test E1 A), zone Perimeter. Change : rotation des jeunes et repos de Bonnet/Lefebvre/Richard. Conseil **C-151** ajouté dans `learnings.md` (remplace C-148 : base rejouée ce jour). Aucun levier interdit redonné. Confiance moyenne : un amical, adversaire inconnu.

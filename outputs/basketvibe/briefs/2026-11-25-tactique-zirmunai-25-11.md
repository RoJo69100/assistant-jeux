Ligue contre Žirmūnai (25/11)
Verrou : mer. 25/11 19:45 (match 20:00, à l'extérieur chez Žirmūnai, J11) — preset de l'adversaire (voir ses joueurs), puis saisie et SAUVEGARDE du match
Adversaire : Žirmūnai (13 joueurs connus, export 24/11 14:10 ; 2 rencontres S1 : L −33 à l'extérieur, W +26 à domicile)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Q2 | Baron | Boyer | Legrand | Fournier | Bernard |
| Q3 | Richard | Boyer | Gimenez | Legrand | Bernard |
| Q4 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Prol. | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | PG | — | — | — | 12 | 3 | 3 | 2 | 3 |
| Boyer | PG | — | SG | SG | — | — | 24 | 3 | 3 | 2 | 3 |
| Richard | PG | PG | — | PG | PG | PG | 36 | 2 | 1 | 2 | 3 |
| Bonnet | SG | SG | — | — | SG | SG | 24 | 5 | 5 | 5 | 3 |
| Leclerc | SG | — | — | — | — | — | 0 | 3 | 3 | 2 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | SF | — | SF | SF | SF | 36 | 4 | 3 | 3 | 3 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 1 | 3 |
| Lefebvre | PF | C | — | — | C | C | 24 | 4 | 4 | 1 | 3 |
| Legrand | PF | — | SF | PF | — | — | 24 | 3 | 3 | 1 | 3 |
| Bernard | C | — | C | C | — | — | 24 | 3 | 3 | 1 | 3 |
| Fournier | C | PF | PF | — | PF | PF | 36 | 2 | 2 | 1 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Baltrušaitis | PG | 3 | Rim (5) |
| Morkūnas | PG | 3 | Perimeter (1) |
| Rimkevičius | PG | 2 | Perimeter (1) |
| Jørgensen | SG | 2 | Perimeter (1) |
| Kavaliauskas | SG | 4 | Perimeter (1) |
| Kiaulakis | SG | 2 | Perimeter (1) |
| Blaževičius | SF | 3 | Rim (5) |
| Sakalauskas | SF | 3 | Rim (5) |
| Vilkas | SF | 2 | Perimeter (1) |
| Jovaiša | PF | 3 | Rim (5) |
| Urbonavičius | PF | 3 | Rim (5) |
| Aleksandravičius | C | 3 | Rim (5) |
| Dainys | C | 2 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Ré-ouvre J11 : Min Richard 36, Gimenez 36, Fournier 36, Bonnet 24, Lefebvre 24, Boyer 24, Legrand 24, Bernard 24, Baron 12, Albano 0
- [ ] Bonnet absent de Q2 et Q3 ; Lefebvre absent de Q2 et Q3 (jamais 36 ni 48 min)
- [ ] Agress. = 3 pour les 12 ; Bonnet Off. focus 5, Rôle 5, Tir 5 ; Boyer Rôle 3, Tir 2 ; Tir 1 pour Lefebvre, Legrand, Fournier, Albano, Bernard
- [ ] Focus 4 sur Kavaliauskas seul (zone Perimeter) ; aucun Light sur Aleksandravičius, Urbonavičius, Sakalauskas, Blaževičius, Jovaiša ; les 13 lignes affichées
## À exporter ensuite
La page du match J11 une fois sauvegardé (avant 19:45), la Preview Žirmūnai (19:30), puis le Report après le match.
---
## Annexe — pourquoi

Saisie du 25/11 (Paris ≈ 10:30) pour le match de ce soir 20:00. Ligue, moteur v4. Plafond de 40 lignes avant `---` dépassé : 3 écrans dont 13 adversaires, comme les fiches du 21/11, 23/11 et 24/11. Brief analyste lu : `2026-11-24-analyste-wrzos-zmigrod-23-11.md`. Aucun brief Match du jour.

### Correction demandée (fatigue du 24/11, `gold.bv_roster_now`, forme relevée le 24/11 après le dimanche 22/11 [M§5.5])
- Bonnet (fatigue 21,58, la plus haute de l'effectif) : 36 → 24 min, Q1 + Q4 + Prol. ; stabilisée 11,9 (`gold.bv_fatigue_plan`, tier 2, 24 min) contre 20,4 à 36 min.
- Lefebvre (fatigue 20,62) : 36 → 24 min, Q1 + Q4 + Prol. ; stabilisée 11,2 contre 19,3.
- Les 24 min libérées : Legrand 12 → 24 (SF Q2, PF Q3), Bernard 24 (C Q2, Q3), Baron 0 → 12 (PG Q2), Boyer 24 (SG Q2, Q3). Albano reste à 0 (en vente, fin 25/11 18:05, `bv_roster_now.on_transfer_list`) : seul joueur en vente en base ; la liste de la consigne est tronquée (« 1) »), les autres noms me manquent.

### Corrections de l'analyste appliquées (brief du 24/11)
1. Lefebvre ≤ 36 min : appliqué, et plus bas (24) à cause de la fatigue. Faux si éval/min < 0,60 à J11 (`gold.bv_match_player_lines`).
2. Q3 avec un tireur à 3 pts : Gimenez (Tir 3) joue Q1, Q3, Q4, repos Q2. Faux si Q3 de J11 ≤ −5 (`quarter_margins`).
3. Focus : Intense × 1 (Kavaliauskas) ; aucun Light au-dessus de 6 % des tirs ; Light seulement ≤ 12 min ou < 3 %.
4. Rebondeur de plus : Bernard au C en Q2 et Q3. Faux si OREB < 15 % (`oreb_pct`).
5. Lancers de fin de match : Bonnet (9/9) et Lefebvre (7/7) sur le terrain en Q4 et Prol. ; Faux si FT % < 70 % (`ft_pct`).
Conséquence assumée : Q2 sans Bonnet, Gimenez ni Lefebvre (meilleur quart offensif de J10) ; Q2 est le quart le plus faible (fit 50,2).

### Focus défensif (inchangé, `gold.bv_match_opp_focus`, `silver.bv_match_player_stats`, ligue S2, 8 matchs)
- **Intense (4) Kavaliauskas** SG, Perimeter : 19,3 % des tirs, 21,5 pts, 67 % à 3 pts ; seul Intense (analyste, L-017 : le focus déplace les tirs). Lock non pris : mapping `off` supposé.
- **Normal (3)** : Aleksandravičius C (16,4 %, 20,5 pts, Rim), Urbonavičius PF (13,6 %, 5 % à 3 pts), Sakalauskas, Blaževičius (9,6 % chacun), Jovaiša (7,7 %), Baltrušaitis PG (5,9 %, 33,8 min, Rim), Morkūnas PG (4,9 %, 50 % à 3 pts, Perimeter).
- **Light (2)** : Dainys (5,9 %, 12 min), Jørgensen (4,9 %, 12 min), Vilkas 1,6 %, Rimkevičius 0,9 %, Kiaulakis 0,1 min. Dainys est à 5,9 % < 6 % et 12 min (règle C-137 respectée). Aucun Give up (L-006). Zone Middle évitée (L-027).
- Limites : compétences adverses en tranches [M§4] ; leurs focus sur nous inconnus ; `gold.bv_next_opponents` en timeout (rang et bilan non lus) ; Preview du 25/11 à exporter. Rencontres passées (`gold.bv_match_report`) : v3, hors moteur actuel.

### Valeurs qui s'écartent de la règle uniforme
- Agress. 3 (écran) pour tous au lieu de 1 : levier agressivité 1 interdit (L-032, C-062 réfuté) ; 3 = défaut des victoires J8/J9.
- Tir 1 : Lefebvre, Legrand, Fournier, Albano, Bernard (profils intérieurs, L-020) ; Tir 2 : Richard, Boyer, Leclerc, et Baron (aligné sur les autres PG, 12 min) ; Bonnet Tir 5 (3P 72) ; Gimenez, Durand : 3. Richard Rôle 1 (passeur 67). Off. focus 4 : Lefebvre, Gimenez ; 2 : Richard, Fournier. Boyer Rôle 3 / Tir 2 : à relire (vu Rôle 2 / Tir 3 en J10).

### Contrôle SQL (25/11, plan en `values` joint à `gold.bv_slot_fit` et `gold.bv_fatigue_plan`)
- 4 quarts : 5 joueurs différents, 5 emplacements trouvés par quart, soit 20/20. `height_eff` minimum 99,2 (Legrand SF Q2) ≥ 95. `fit_with_form` moyen : Q1 61,0, Q2 50,2, Q3 55,5, Q4 61,0 (Q2 : Baron PG 44,7 ; Q3 : Boyer 49,8, Bernard 49,3). Aucun joueur en vente ni blessé dans les cinqs (`injury_return_on` vide pour les 12).
- Minutes : Richard, Gimenez, Fournier 36 ; Bonnet, Lefebvre, Boyer, Legrand, Bernard 24 ; Baron 12 ; Leclerc, Durand, Albano 0 ; total 240, aucun au-delà de 36 (Prol. : 5 titulaires à 41, inévitable).
- Fatigue stabilisée (tier 2) : Gimenez 20,3, Richard 19,5, Fournier 19,2, Bernard 14,1, Boyer 12,5, Bonnet 11,9, Lefebvre 11,2, Legrand 11,0, Baron 4,6. Gimenez à 20,3 : seul titulaire au-dessus de 20, de 0,3 (18,36 aujourd'hui) ; accepté, forme 10 et tireur de Q3.
- Forme relevée le 24/11 (à jour, après le dimanche 22/11) : Gimenez 10, Fournier 8, Lefebvre 8, Legrand 7, Bonnet 7, Boyer 7, Richard 6, Bernard 6, Baron 5.

### Blessés et plan B
Aucun blessé. Plan B : SG Bonnet → Gimenez (SG 69,8) ou Richard (56,9) ; C Lefebvre → Fournier (56,4) ; PG Richard → Boyer (50,6) ; SF Gimenez → Legrand (50,6). Albano exclu.

Anticipation (hypothèse) : à l'extérieur, Žirmūnai met sans doute Intense sur Bonnet (36 tirs en J9) ; Bonnet ne joue que 24 min, Gimenez et Richard prennent les tirs, Lefebvre (Tir 1) joue dedans. Confiance faible.

### Évolution et conseil
Garde : 36 min max, agressivité 3, Bonnet Tir 5, Intense × 1. Change : Bonnet et Lefebvre 24 min (fatigue > 20), Baron Q2. Teste : Q2 sans Bonnet, Gimenez, Lefebvre. Conseil **C-139** ajouté dans `learnings.md`. Aucun levier interdit redonné.

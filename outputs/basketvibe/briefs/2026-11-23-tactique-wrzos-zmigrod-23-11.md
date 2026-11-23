Ligue contre Wrzos Zmigrod (23/11)
Verrou : lun. 23/11 19:45 (match 20:00, à domicile, J10) — preset de l'adversaire (voir ses joueurs), puis saisie et SAUVEGARDE du match
Adversaire : Wrzos Zmigrod (5e, 6-3, diff +78, humain) ; 17 joueurs connus (export 23/11 15:41), aucune rencontre
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Q2 | Boyer | Bonnet | Gimenez | Lefebvre | Legrand |
| Q3 | Richard | Boyer | Legrand | Albano | Fournier |
| Q4 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Prol. | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | SG | — | — | 24 | 3 | 3 | 2 | 3 |
| Richard | PG | PG | — | PG | PG | PG | 36 | 2 | 1 | 2 | 3 |
| Bonnet | SG | SG | SG | — | SG | SG | 36 | 5 | 5 | 5 | 3 |
| Leclerc | SG | — | — | — | — | — | 0 | 3 | 3 | 2 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | SF | SF | — | SF | SF | 36 | 4 | 3 | 3 | 3 |
| Albano | PF | — | — | PF | — | — | 12 | 3 | 3 | 1 | 3 |
| Lefebvre | PF | C | PF | — | C | C | 36 | 4 | 4 | 1 | 3 |
| Legrand | PF | — | C | SF | — | — | 24 | 3 | 3 | 1 | 3 |
| Bernard | C | — | — | — | — | — | 0 | 3 | 3 | 1 | 3 |
| Fournier | C | PF | — | C | PF | PF | 36 | 2 | 2 | 1 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Brzeziński | PG | 2 | Perimeter (1) |
| Mazur | PG | 3 | Perimeter (1) |
| Michalak | PG | 2 | Perimeter (1) |
| Wachowicz | PG | 3 | Rim (5) |
| Ostapczuk | SG | 4 | Perimeter (1) |
| Petravičius | SG | 2 | Perimeter (1) |
| Garcia | SF | 3 | Perimeter (1) |
| Król | SF | 3 | Rim (5) |
| Malinowski | SF | 2 | Perimeter (1) |
| Przybylski | SF | 3 | Perimeter (1) |
| Asenov | PF | 3 | Perimeter (1) |
| Biernacki | PF | 3 | Perimeter (1) |
| Chojnacki | PF | 4 | Rim (5) |
| Krawczyk | PF | 2 | Perimeter (1) |
| Górski | C | 2 | Perimeter (1) |
| Nieto | C | 3 | Perimeter (1) |
| Pawłowski | C | 2 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Ré-ouvre J10 : Min Richard 36, Bonnet 36, Gimenez 36, Lefebvre 36, Fournier 36, Boyer 24, Legrand 24, Albano 12 (défaut du jeu : 24 pour presque tous, Bonnet 48)
- [ ] Agress. = 3 pour les 12 ; Bonnet Off. focus 5, Rôle 5, Tir 5 ; Tir 1 pour Lefebvre, Legrand, Fournier, Albano, Bernard
- [ ] Focus 4 sur Ostapczuk et Chojnacki ; zone Rim (5) pour Chojnacki, Wachowicz, Król ; les 17 lignes affichées
## À exporter ensuite
La page du match J10 une fois sauvegardé (avant 19:45), puis après le match (Report) ; la Preview des Wrzos manque.
---
## Annexe — pourquoi

Saisie AUJOURD'HUI lundi 23/11 (Paris ≈ 17:00), avant 19:45. Ligue, moteur v4 [M§5.7, M§6.6]. Sources : résumé BasketVibe, fiche Tactique, `learnings.md`, skill `basketvibe-tactique` (index). Aucun brief Match du jour (brief amont manquant) ; brief Entraînement du 23/11 lu (sans effet sur le match). Les 3 tableaux exigés font déjà 47 lignes avant `---` (17 adversaires, une ligne chacun) : le plafond de 40 est dépassé, comme au brief du 21/11.

### Fait critique : J9 n'a PAS été joué avec la fiche
`gold.bv_saisie_joueurs` (J10, export 23/11 15:41) : `sauvegarde_match` False, preset « League Tactic » par défaut (Bonnet 48 min, Tir 5). `gold.bv_match_player_lines` (J9, 21/11) : Bonnet 48 min / 57 pts / 36 tirs dont 25 à 3 pts, les 8 autres à 24 min, tous `defense_tier` 2 ; `gold.bv_match_opp_focus` : les 11 adverses en « normal ». J9 gagné 113-103 (`gold.bv_match_report` : quarts +10/−6/−2/+8, eFG 52,7, eFG adverse 53,9) avec le défaut, donc la fiche J9 (Intense Barbosa/Ferreira, 36 min) n'est pas testée. Même cas : coupe 12/11 (L-030). Aujourd'hui : sauvegarder le match.

### Faits adversaire
- `gold.bv_next_opponents` J10 : Wrzos 5e, 6-3, diff +78, TS 55,1 contre 54,1 pour nous, humain ; `meetings` vide : jamais rencontrés.
- `silver.bv_matches` : 8 matchs joués (J1 L −13 chez Žirmūnai, J3 L −22 chez Eindhoven, 6 victoires dont J8 chez Astur 105-86). Aucune ligne dans `gold.bv_league_top_players` (11 clubs, pas Wrzos) : stats saison 2 lues dans `silver.bv_match_player_stats` (période 0, 8 matchs).
- Parts de tirs (sur 674 tirs) : Ostapczuk SG 14,2 % (18,9 pts, 59,4 %, 49 % des tirs à 3 pts, 31,5 min) ; Chojnacki PF 14,1 % (14,8 pts, 49,5 %, 31 % à 3 pts, 31,6 min) ; Król SF 12,3 % (14,9 pts, 56,6 %, 39 % à 3 pts) ; Biernacki PF 12,2 % (15,5 pts, 44 % à 3 pts) ; Wachowicz PG 10,7 % (12,5 pts, 35 % à 3 pts) ; Asenov PF 9,1 % (54 % à 3 pts, 39 %) ; Garcia SF 7,6 % ; Petravičius SG 7,1 % (31 %) ; Pawłowski C 5,5 % ; Brzeziński PG 4,2 % ; Malinowski 2,4 %. Górski, Michalak (1,5 min), Krawczyk (0 min) : quasi absents. **Mazur, Nieto, Przybylski : aucune ligne saison 2 (nouveaux ou jamais utilisés)**.
- Limites : compétences en tranches [M§4] ; leurs focus sur nous inconnus ; 8 matchs, 5 joueurs entre 27 et 33 min ; Preview à exporter.

### Focus défensif (obligatoire)
Intense (4) sur les deux plus gros volumes : Ostapczuk (3 pts : Perimeter) et Chojnacki (2 pts : Rim, 2P adverse ≈ −3 %, 3P jusqu'à +5 % [News 2026-10-19]). Deux Intense : effet de deux 4 simultanés peu documenté (L-012), aucun Lock (L-017, 8 cas seulement), aucun Give up (L-006 : inconnus et quasi absents en Light, pas en Give up). Normal : Król, Wachowicz (2P → Rim), Biernacki, Asenov, Garcia (3P → Perimeter), Mazur, Nieto, Przybylski (inconnus, Perimeter : Middle est la pire zone mesurée, L-027, confiance faible). Light (2) : Brzeziński, Petravičius (31 % aux tirs), Pawłowski, Malinowski, Górski, Michalak, Krawczyk (≤ 8 % des tirs ou ≤ 17 min).

### Changements (2) par rapport au défaut joué en J9
1. Bonnet 36 min au lieu de 48 : `gold.bv_fatigue_plan` (écran 3) donne 20,5 à 36 min ; au-delà de 36 min −20 % [M§5.7]. Fatigue actuelle 17,15 (`gold.bv_roster_now`, 23/11). Tir 5, Off. focus 5, Rôle 5 gardés : réglage qui a donné 57 pts, eFG élevée (C-123 proposait 4 : écart non testé, on garde ce qui marche). Risque : −21 pts sans ses 12 minutes ; Q3 est son quart de repos.
2. Intense Ostapczuk + Chojnacki, zones par profil 2P/3P, plan sauvegardé (le défaut donnait Normal partout).
Gardé : 2 groupes de repos (Q2 et Q3), Albano utilisé (fatigue 3,81, forme 8, 12 min au PF Q3), rotation 36 max.

### Valeurs qui s'écartent de la règle uniforme
- Agressivité 3 (écran) pour les 12 au lieu de 1 (L-004) : levier agressivité 1 interdit par le compteur d'échecs (L-032 : aucun gain défensif visible sur 5 matchs ; brief du 13/11) ; 3 = défaut du jeu, joué en J9 (V +10, tier 2 pour les 9 joueurs) et en J8 (V +22). Coût : Gimenez 20,3 (0,3 au-dessus de 20, accepté).
- Tir 1 : Lefebvre, Legrand, Fournier, Albano, Bernard (profils intérieurs, 3P 34–54, L-020) ; Tir 2 : Richard, Boyer, Leclerc (tirs à 3 pts peu réussis, L-020) ; Bonnet 5 (3P 72, 25 tirs à 3 pts en J9 : 57 pts) ; Gimenez, Baron, Durand : 3 neutre. Richard Rôle 1 (passeur 67), Off. focus 2 ; Fournier Off. focus 2 / Rôle 2 ; Off. focus 4 : Lefebvre, Gimenez.

### Contrôle SQL (fait le 23/11, plan en `values` joint à `gold.bv_slot_fit`)
- 4 quarts : 5 joueurs différents, 5 emplacements trouvés par quart (20/20) ; `height_eff` minimum 99,2 (Legrand SF Q3) ≥ 95 ; `fit_with_form` moyen Q1 60,8, Q2 58,5, Q3 52,9, Q4 60,8 ; aucune `injury_return_on` renseignée.
- Minutes : Richard, Bonnet, Gimenez, Lefebvre, Fournier 36 ; Boyer, Legrand 24 ; Albano 12 ; Baron, Leclerc, Durand, Bernard 0 ; total 240 ; aucun au-delà de 36 (prolongation : les 5 titulaires à 41, inévitable).
- Fatigue stabilisée écran 3 (`gold.bv_fatigue_plan`) : Bonnet 20,5, Gimenez 20,3, Richard 19,5, Lefebvre 19,3, Fournier 19,2 ; Boyer 12,5, Legrand 11,0, Albano 3,0. Fatigue actuelle : Bonnet 17,15, Boyer 16,24, Bernard 15,79, Legrand 14,2, Lefebvre 14,02, Richard 13,77, Gimenez 13,59, Fournier 12,59, Albano 3,81. Amical de 08:00 (23/11, W 117-116 chez Pilaristas) : Baron, Legrand, Leclerc, Albano, Boyer, Bernard 36 min, Durand 24 ; effet ≈ 1/10 (déjà dans le relevé).
- Forme (relevé du 23/11, après le dimanche 22/11 [M§5.5]) : Gimenez 10, Fournier 8, Lefebvre 8, Albano 8, Legrand 7, Bonnet 7, Boyer 7, Richard 6, Bernard 6, Baron 5, Leclerc 4, Durand 4. Reposés (forme ≤ 4) : Leclerc, Durand à 0 min.

### Blessés et plan B
Aucun blessé (`injury_return_on` vide pour les 12), aucun joueur en vente, effectif 12 (minimum 8). Plan B si un titulaire manque : SG Bonnet → Boyer (49,6 au SG) ou Richard ; PF/C Lefebvre ou Fournier → Legrand (PF 51,8, C 51,8), Albano (51,0), Bernard (C 49,3) ; PG Richard → Boyer (50,4), Gimenez (PG 68,4) ; ne dépasser 3 quarts pour personne. Depth chart : PG Boyer, Baron ; SG Boyer, Richard, Leclerc ; SF Legrand, Durand ; PF Legrand, Albano, Lefebvre ; C Legrand, Albano, Bernard. Blessures en ligue seulement [M§1.2] ; kinés : relevé personnel non relu (Finances).

Anticipation (hypothèse) : s'ils appliquent notre règle (Intense sur nos plus gros volumes ; aucune donnée sur leurs focus en base), Intense sur Bonnet (36 tirs en J9) et Lefebvre. Plan B : Gimenez, Richard et Fournier relaient (Off. focus 4 pour Gimenez déjà), Boyer en Q2 prend les tirs à 2 pts.

### Évolution et conseil
Garde : 36 min max, agressivité 3, 2 quarts de repos, Bonnet Tir 5 (marche en J9). Change : Bonnet 36 min, Intense Ostapczuk + Chojnacki avec zones par profil. Teste : premier match de ligue S2 avec plan sauvegardé à Intense × 2 depuis J8 (J9 non sauvegardé). Conseil **C-132** ajouté dans `outputs/basketvibe/learnings.md`. Aucun levier interdit redonné. Manques : Preview des Wrzos, leurs focus sur nous ; Match du jour à produire.

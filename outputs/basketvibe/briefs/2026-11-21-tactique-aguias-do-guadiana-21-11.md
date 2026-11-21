Ligue contre Águias do Guadiana (21/11)
Verrou : sam. 21/11 19:45 (match 20:00, à domicile, J9) — preset de l'adversaire (voir ses joueurs), puis saisie et sauvegarde
Adversaire : Águias do Guadiana (3e, 6-2, diff +88, humain) ; 16 joueurs connus par l'export du 20/11 17:04
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Leclerc | Gimenez | Legrand | Lefebvre |
| Q2 | Gimenez | Boyer | Lefebvre | Fournier | Bernard |
| Q3 | Richard | Boyer | Albano | Legrand | Bernard |
| Q4 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Prol. | Richard | Bonnet | Gimenez | Legrand | Lefebvre |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | SG | SG | — | — | 24 | 3 | 3 | 2 | 3 |
| Richard | PG | PG | — | PG | PG | PG | 36 (+5) | 2 | 1 | 2 | 3 |
| Bonnet | SG | — | — | — | SG | SG | 12 (+5) | 4 | 4 | 2 | 3 |
| Leclerc | SG | SG | — | — | — | — | 12 | 3 | 3 | 2 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | SF | PG | — | SF | SF | 36 (+5) | 4 | 3 | 3 | 3 |
| Albano | PF | — | — | SF | — | — | 12 | 3 | 3 | 1 | 3 |
| Lefebvre | PF | C | SF | — | C | C | 36 (+5) | 4 | 4 | 1 | 3 |
| Legrand | PF | PF | — | PF | — | PF | 24 (+5) | 3 | 3 | 1 | 3 |
| Bernard | C | — | C | C | — | — | 24 | 3 | 3 | 1 | 3 |
| Fournier | C | — | PF | — | PF | — | 24 | 2 | 2 | 1 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Cardoso | PG | 2 | Perimeter (1) |
| Monteiro | PG | 3 | Perimeter (1) |
| Neves | PG | 3 | Perimeter (1) |
| Nunes | PG | 3 | Perimeter (1) |
| Simões | PG | 3 | Perimeter (1) |
| Barbosa | SG | 4 | Perimeter (1) |
| Pereira | SG | 3 | Perimeter (1) |
| Carvalho | SF | 3 | Perimeter (1) |
| Coutinho | SF | 2 | Perimeter (1) |
| Azevedo | PF | 3 | Perimeter (1) |
| Guerreiro | PF | 3 | Perimeter (1) |
| Al-Rashdan | C | 3 | Perimeter (1) |
| Coelho | C | 3 | Perimeter (1) |
| Domingues | C | 3 | Perimeter (1) |
| Ferreira | C | 4 | Rim (5) |
| Nogueira | C | 3 | Rim (5) |
## Après sauvegarde, vérifie
- [ ] Ré-ouvre J9 : Min Richard 36, Gimenez 36, Lefebvre 36, Boyer 24, Bonnet 12, Leclerc 12, Albano 12 (le défaut du jeu affiche 24 pour tous et Bonnet 48), Agress. = 3 pour les 12
- [ ] Tir = 1 pour Lefebvre, Legrand, Bernard, Fournier, Albano ; Tir = 2 pour Bonnet, Boyer, Richard, Leclerc
- [ ] Focus 4 sur Barbosa et Ferreira ; zone Rim (5) pour Ferreira et Nogueira ; les 16 lignes affichées
## À exporter ensuite
La page du match J9 une fois sauvegardé (avant 19:45), puis après le match ; la Preview (stats saison 2 des Águias) manque.
---
## Annexe — pourquoi

Saisie AUJOURD'HUI samedi 21/11 (Paris 10:41), avant 19:45. Ligue, moteur v4 [M§5.7, M§6.6]. Sources : résumé BasketVibe, fiche Tactique, `learnings.md`, skill `basketvibe-tactique` (index). Aucun brief Match du jour. Cette fiche dépasse 40 lignes avant « --- » (≈ 52) : les 3 tableaux exigés en font 42 à eux seuls (16 adversaires, une ligne chacun).

### Faits adversaire (`gold.bv_next_opponents` J9 : 3e, 6-2, diff +88, TS 54,1 contre 53,9, humain ; rencontres : L 71-101 le 12/09, L 89-119 le 07/10, saison 1)
- Aucune statistique saison 2 des Águias en base (`gold.bv_league_top_players` ne contient que 2 matchs par joueur, ceux contre nous, saison 1). Cinq noms sont nouveaux (Neves, Simões, Al-Rashdan, Coelho, Domingues) : focus neutre.
- `gold.bv_match_opp_focus` (12/09 puis 07/10, tous en Normal) : Barbosa SG 10,5 % puis **25,3 %** des tirs (48 min, 26 pts, 10 tirs à 3 pts sur 23) ; Ferreira C 13,2 % puis 15,4 % (24 pts à 71 % en J14, 23 reb de moyenne) ; Guerreiro PF 6,6 % puis 15,4 % (6 pts à 14 %) ; Nunes PG 100 % sur 7 tirs en J14 ; Carvalho SF 11-12 % ; Nogueira C 87,5 % sur 8 tirs en 12 min ; Cardoso, Coutinho, Monteiro : 2 à 9 % en 12 min.
- Limites : compétences en tranches seulement [M§4] ; roster saison 1, en partie renouvelé ; leurs focus sur nous inconnus ; mon dernier match (J8, V +22 chez C.B.Granada, `gold.bv_match_report`) et les 4 victoires/défaites de S2 ne disent rien d'eux.

### Focus défensif (obligatoire)
Intense (4) sur Barbosa (le vrai scoreur à l'aller, 25 % des tirs, tirs à 3 pts : Perimeter) et Ferreira (2P et rebonds : Rim, 2P adverse ≈ −3 %, 3P jusqu'à +5 % [News 2026-10-19]). Deux Intense comme en J8 (réussi : Aragón et Jiménez, mêmes conditions, V +22 ; effet de deux 4 simultanés peu documenté, L-012). Aucun Lock (8 cas, L-017), aucun Give up (L-006). Light (2) : Cardoso et Coutinho (12 min, < 8 % des tirs). Normal : Nunes, Carvalho, Pereira, Guerreiro, Azevedo, Monteiro, Nogueira (Rim, 2P) ; inconnus Normal / Perimeter. Perimeter plutôt que Middle : Middle est la pire zone mesurée (L-027, 2 à 5 matchs, confiance faible).

### Changements (2) par rapport au plan de J8 (V +22, plan sauvegardé, minutes conformes : Lefebvre 36 min 36 pts)
1. Boyer 24 min au lieu de 36 : `gold.bv_fatigue_plan` (écran 3) donne 21,2 à 36 min contre 12,5 à 24 ; il joue aussi 36 min à l'amical de 08:00 (+0,76). Q4 SG : Bonnet (fatigue 14,44, 12 min → ≈ 6, `fit_with_form` 55,2 au SG, Tir 2).
2. Zones/focus : Barbosa et Ferreira remplacent Aragón et Jiménez en Intense (même logique : plus gros volume + zone selon 2P/3P).
Gardé : plan J8 (cinqs, 2 unités, Bernard C Q2-Q3), plan sauvegardé, 36 min max.

### Valeurs qui s'écartent de la règle uniforme
- Agressivité 3 (écran) pour les 12 au lieu de 1 (L-004) : levier agressivité 1 interdit par le compteur du 13/11 (2 échecs) ; 3 = défaut du jeu, joué en J8 (V +22, eFG adverse 42,3). Coût : Gimenez 20,3 (0,3 au-dessus de 20, accepté comme en J8).
- Tir 1 : Lefebvre, Legrand, Bernard, Fournier, Albano (profils intérieurs, L-020) ; Tir 2 : Richard, Boyer, Bonnet, Leclerc (L-020 : tirs à 3 pts peu réussis). Gimenez, Baron, Durand : 3 neutre. Richard Rôle 1 (passeur), Off. focus 2 ; Fournier Off. focus 2 / Rôle 2 ; Off. focus 4 : Lefebvre, Bonnet, Gimenez (reprise J8).

### Contrôle SQL (fait le 21/11)
- Plan `values` joint à `gold.bv_slot_fit` : 4 quarts, 5 joueurs différents par quart, 0 emplacement manquant ; `height_eff` minimum 98,4 (Lefebvre SF Q2) ≥ 95 ; `fit_with_form` moyen Q1 57,1, Q2 56,6, Q3 51,8, Q4 60,0.
- Minutes : Richard, Gimenez, Lefebvre 36 ; Boyer, Bernard, Fournier, Legrand 24 ; Leclerc, Albano, Bonnet 12 ; Baron, Durand 0 ; total 240 ; aucun > 36 (prolongation : Richard, Gimenez, Lefebvre passent à 41, inévitable [M§5.7]).
- Fatigue stabilisée écran 3 (`gold.bv_fatigue_plan`) : Gimenez 20,3, Richard 19,5, Lefebvre 19,3, Boyer 12,5, Fournier 11,1, Legrand 11,0, Bernard 14,1, Bonnet 6 (12 min). Fatigue actuelle (`gold.bv_roster_now`, 20/11) : Lefebvre 15,84, Richard 15,46, Boyer 15,1, Gimenez 15,06, Bonnet 14,44, Fournier 13,91, Bernard 13,64, Legrand 13,05. Amical de 08:00 (21/11) : Boyer, Legrand, Albano, Bernard à 36 min (+≈0,7 chacun), les autres de ligue à 0 (brief amical du 19/11).
- Forme du relevé du 20/11 (postérieur au dimanche 15/11 ; la prochaine tombe dimanche 22/11) : Gimenez 9, Legrand 8, Bonnet 8, les autres 7 sauf Leclerc 5, Durand 5, Baron 6 [M§5.5].
- Blessés : aucun (`injury_return_on` vide pour les 12) ; vendus : aucun ; effectif 12 (minimum 8). Plan B : si un cinq manque, Bonnet (SG), Albano (SF/PF), Legrand/Fournier (PF/C) prennent les minutes ; ne pas dépasser 3 quarts à personne.

Anticipation (hypothèse) : s'ils appliquent notre règle (focus sur nos plus gros volumes, zone selon 2P/3P ; aucune donnée sur leurs focus en base), Intense sur Lefebvre (2P, Rim) et Gimenez ; plan B : Fournier/Legrand/Bernard Tir 1 prennent les 2P, Richard et Boyer Tir 2 relaient.

### Évolution et conseil
Garde : plan sauvegardé, 36 min max, agressivité 3, 2 unités. Change : Boyer 24 min / Bonnet Q4 (fatigue). Teste : Intense Barbosa + Ferreira. Conseil **C-131** ajouté dans `outputs/basketvibe/learnings.md`. Aucun levier interdit redonné. Manques : Preview saison 2 des Águias, focus adverses sur nous.

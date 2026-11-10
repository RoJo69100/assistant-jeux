Amical contre Launceston Ligers (11/11)

Saisie AUJOURD'HUI 10/11 (heure Paris 16:21), verrou mercredi 11/11 07:45. Amical : pas de preset, pas d'aperçu ni de donnée adverse (arbitrage 15). Moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Ligue le soir (19:45) : les cinq de ligue ne jouent pas.

## Action : fais X
Sur la page du match d'amical contre Launceston Ligers : composition ci-dessous, **agressivité 3 pour les 14 joueurs** (test E1, cran 2 « équilibrée »), zone Middle (3) et focus 3 pour les 15 adversaires (inchangés : un seul test), puis sauvegarde et exporte la page avant 07:45. À l'écran (export 10/11 16:11), `sauvegarde_match` est faux et le plan préchargé met Gimenez 48 min, Dang / Albano / Ungureanu à agressivité 3 et les autres à 1 : tout est à remplacer (`gold.bv_saisie_joueurs`).

## Test unique (E1, niveau A)
Agressivité défensive écran 3 sur tous, au lieu de 1 (règle L-004). Seul réglage modifié ; zone constante (Middle). Lecture : comparer à la série d'amicaux à agressivité 1 (`gold.bv_match_report`, `opp_fg2_pct`, points encaissés, fautes `pf` dans `gold.bv_match_player_lines`). Faux si les points encaissés ou les fautes montent sans baisse de `opp_fg2_pct`. Doute : un seul match, banc inchangé, donc bruit élevé.

## 1. Composition (écran 1)
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Boyer | Legrand | Bernard |
| Q2 | Dang | Leclerc | Durand | Albano | Bernard |
| Q3 | Baron | Leclerc | Boyer | Bernard | Ungureanu |
| Q4 | Baron | Boyer | Durand | Legrand | Ungureanu |
| Prol. | Dang | Durand | Albano | Legrand | Ungureanu |

Remplaçants : aucun programmé. Richard, Bonnet, Gimenez, Lefebvre, Fournier : 0 minute (ligue ce soir, titulaires protégés).

## 2. Consignes (écran 2, 1-5, ordre de l'écran)
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron (17 ans) | PG | PG | — | PG | PG | — | 36 | 2 | 1 | 3 | 3 |
| Boyer (20 ans) | PG | SF | — | SF | SG | — | 36 | 2 | 2 | 3 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 5 | 5 | 5 | 3 |
| Dang | SG | — | PG | — | — | PG | 12 (+5) | 3 | 3 | 2 | 3 |
| Leclerc (17 ans) | SG | SG | SG | SG | — | — | 36 | 4 | 4 | 3 | 3 |
| Durand | SF | — | SF | — | SF | SG | 24 (+5) | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | — | PF | — | — | SF | 12 (+5) | 3 | 3 | 1 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 4 | 4 | 1 | 3 |
| Legrand | PF | PF | — | — | PF | PF | 24 (+5) | 3 | 3 | 1 | 3 |
| Bernard (18 ans) | C | C | C | PF | — | — | 36 | 2 | 2 | 1 | 3 |
| Fournier | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 3 |
| Ungureanu | C | — | — | C | C | C | 24 (+5) | 3 | 3 | 2 | 3 |

Dans les colonnes Q, la valeur est l'emplacement tenu (Boyer : SF Q1, SF Q3, SG Q4).

Minutes : Baron 36 + Boyer 36 + Leclerc 36 + Bernard 36 + Dang 12 + Durand 24 + Albano 12 + Legrand 24 + Ungureanu 24 = 240. Jeunes ≤ 21 ans (Baron, Boyer, Leclerc, Bernard) : 144 min sur 240 (60 %), tous à 36 max (`gold.bv_roster_now`, âges 17, 20, 17, 18).

Raisons des valeurs qui s'écartent de la règle ou du préchargé :
- Agressivité 3 partout : test E1, seule différence avec L-004 (1) ; le même cran pour les 14, y compris ceux qui ne jouent pas, pour que le test soit propre.
- Leclerc Tir 3 (préchargé 5) : 62 % de ses tirs à 3 pts mais 29 % de réussite sur 453 tirs d'amical (`gold.bv_match_player_lines`, L-020).
- Tir 1 pour Albano, Legrand, Bernard : 58 %, 83 %, 92 % de leurs tirs à 2 pts (amical) ; Dang et Ungureanu Tir 2 : échantillons courts, 3P 12 % et 42 %.
- Rôle 1 Baron : meilleure passe du banc (57).
- Les cinq de ligue : valeurs de ligue, ils ne jouent pas.

## 3. Adversaires (écran 3) : Launceston Ligers, 15 joueurs, aucune statistique
Source `gold.bv_saisie_adversaires` (export 10/11 16:11).
Les 15 : focus 3 (Normal), zone Middle (3), dans l'ordre de l'export.

| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Barrett | PG | 3 | Middle (3) |
| Brinkmann | PG | 3 | Middle (3) |
| de Groot | PG | 3 | Middle (3) |
| Bradshaw | SG | 3 | Middle (3) |
| Burns | SG | 3 | Middle (3) |
| Porter | SG | 3 | Middle (3) |
| Cooke | SF | 3 | Middle (3) |
| Guillot | SF | 3 | Middle (3) |
| Moldovan | SF | 3 | Middle (3) |
| Fisher | PF | 3 | Middle (3) |
| O'Neil | PF | 3 | Middle (3) |
| Stone | PF | 3 | Middle (3) |
| Byrne | C | 3 | Middle (3) |
| Schmitt | C | 3 | Middle (3) |
| Zogaj | C | 3 | Middle (3) |

### Focus défensif
Parts de tirs et 2P/3P de Launceston : inconnus (aucune donnée adverse en amical, arbitrage 15). Focus neutre : Normal pour les 15, aucun Give up ni Light, zone Middle (3) pour garder un seul test. Pas d'export à faire.

## 4. Blessés et plan B
Aucun blessé ni joueur en vente (`gold.bv_roster_now`, relevé du 08/11, `day` 10/11). Pas de blessure en amical. Si un des neuf manque : Leclerc peut passer PG ou SF, Dang prend la place libre.

## 5. Contrôle SQL (values + `gold.bv_slot_fit`, 10/11)
- 20 cases (Q1-Q4 × 5 postes) : 5 joueurs différents par quart, un par emplacement : OK.
- Aucun joueur au-delà de 3 quarts : 3 pour Baron, Boyer, Leclerc, Bernard ; 2 ou moins pour les autres : OK.
- `height_eff` minimum 99,2 (Boyer SF) : ≥ 95 partout.
- `fit_with_form` minimum : Leclerc SG 42,6 ; Durand SF 43,0 ; Baron PG 44,6 ; les autres 48 à 51. Faibles par construction (amical de test).
- Fatigue actuelle : 0,44 (Durand) à 7,38 (Legrand) ; ajout d'un amical ≈ 1/10 du plafond de ligue (≤ 2,2 à 36 min, base `gold.bv_fatigue_plan` tier 2) : ≤ 20 partout. Titulaires de ligue à 0 min. Aucun blessé ni vendu.
- Forme : relevé du dimanche 08/11 (`week`), à jour.

## 6. Évolution
Conseil proposé **C-118** (à enregistrer dans `outputs/basketvibe/learnings.md`, non écrit ici) : amical du 11/11, agressivité écran 3 pour tous ; critère SQL : `gold.bv_match_player_lines.defense_tier` = 2 pour tous les joueurs ayant joué, comparer `opp_fg2_pct` et `pf` à la série à agressivité 1. Lien : L-004.

Anticipation (hypothèse) : si un adversaire applique notre règle (focus sur la plus grosse part de tirs, zone selon 2P/3P) : Leclerc (18,2 % des tirs d'amical, 62 % à 3 pts) = Intense, Perimeter ; Bernard (92 % à 2 pts), Legrand (83 %) = Normal, Rim ; Albano (58 % à 2 pts), Durand, Boyer, Baron (≈ 45 % à 3 pts) = Normal, Middle ; Dang et Ungureanu (1,5 % et 3,7 % des tirs) = Light. Plan B nommé : si Leclerc est pris en focus Intense Perimeter, Durand (3P 31 %) et Boyer (3P 31 %) prennent le relais en SF, Leclerc ne joue jamais sans l'un des deux (Q2 Durand, Q1 et Q3 Boyer), et Bernard / Legrand / Albano garantissent le scoring intérieur (2P 48 à 63 %). Aucune donnée sur les focus adverses en base : hypothèse sans preuve.

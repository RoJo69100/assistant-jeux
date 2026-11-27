Ligue contre Chara legends (28/11)
Verrou : sam. 28/11 19:45 (match 20:00, J12) — preset de l'adversaire (voir ses joueurs), puis saisie et SAUVEGARDE du match
Adversaire : Chara legends (12 joueurs connus, Preview exportée le 27/11 11:04 ; 1 rencontre S2 : J1 02/11 W, quarts +14 / +2 / +7 / +18)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Q2 | Boyer | Bonnet | Bourdon | Lefebvre | Bernard |
| Q3 | Richard | Bourdon | Gimenez | Fournier | Bernard |
| Q4 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
| Prol. | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | — | — | — | 12 | 3 | 3 | 2 | 3 |
| Richard | PG | PG | — | PG | PG | PG | 36 | 2 | 1 | 2 | 3 |
| Bonnet | SG | SG | SG | — | SG | SG | 36 | 5 | 5 | 5 | 3 |
| Leclerc | SG | — | — | — | — | — | 0 | 3 | 3 | 2 | 3 |
| Bourdon | SF | — | SF | SG | — | — | 24 | 3 | 3 | 3 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | SF | — | SF | SF | SF | 36 | 4 | 3 | 3 | 3 |
| Lefebvre | PF | C | PF | — | C | C | 36 | 4 | 4 | 1 | 3 |
| Legrand | PF | — | — | — | — | — | 0 | 3 | 3 | 1 | 3 |
| Bernard | C | — | C | C | — | — | 24 | 3 | 3 | 1 | 3 |
| Fournier | C | PF | — | PF | PF | PF | 36 | 2 | 2 | 1 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Díaz | PG | 2 | Perimeter (1) |
| Romero | PG | 2 | Perimeter (1) |
| Vargas | PG | 2 | Perimeter (1) |
| Moreno | SG | 3 | Perimeter (1) |
| Suárez | SG | 2 | Perimeter (1) |
| Molina | SF | 4 | Perimeter (1) |
| Vázquez | SF | 2 | Perimeter (1) |
| Aguayo | PF | 3 | Perimeter (1) |
| Hernández | PF | 3 | Rim (5) |
| Durán | C | 3 | Rim (5) |
| Navarro | C | 2 | Rim (5) |
| Soler | C | 2 | Rim (5) |
## Après sauvegarde, vérifie
- [ ] Ré-ouvre J12 : Min Richard 36, Bonnet 36, Gimenez 36, Lefebvre 36, Fournier 36, Bourdon 24, Bernard 24, Boyer 12, Legrand 0, Durand 0 (défaut du jeu : 24 pour presque tous, Bonnet 48)
- [ ] Q2 : Boyer, Bonnet, Bourdon, Lefebvre, Bernard ; Q3 : Richard, Bourdon, Gimenez, Fournier, Bernard ; Lefebvre absent de Q3 ; Durand absent des 5 écrans
- [ ] Agress. = 3 pour les 12 ; Bonnet Off. focus 5, Rôle 5, Tir 5 ; Boyer Rôle 3, Tir 2 ; Tir 1 pour Lefebvre, Legrand, Fournier, Bernard
- [ ] Focus 4 sur Molina seul (Perimeter) ; Durán, Aguayo, Moreno, Hernández à 3 (aucun Light) ; les 12 lignes affichées
## À exporter ensuite
La page du match J12 une fois sauvegardé (avant 19:45), puis le Report après le match.
---
## Annexe — pourquoi
Saisie AUJOURD'HUI vendredi 27/11 (Paris ≈ 11:10) pour le match de demain 28/11 20:00 (se prépare aujourd'hui). Ligue, moteur v4. Plus de 40 lignes avant `---` : 3 tableaux exigés (12 joueurs, 12 adversaires), incompressibles. Sources : résumé BasketVibe, fiche Tactique, `learnings.md`, `basketvibe-tactique/SKILL.md` (index ; règles citées via la fiche : M§5.7, M§6.6, News 2026-10-19). Brief analyste lu : `2026-11-24-analyste-wrzos-zmigrod-23-11.md` (le plus récent). Aucun brief Match du jour (amont manquant).
Consigne utilisateur : Jonathan Durand ne joue pas (vente proposée au plan) : 0 min, hors des 5 cinqs (`gold.bv_roster_now` : non listé en vente, donc consigne seule). Albano n'est plus dans `gold.bv_roster_now` (12 joueurs avec Bourdon, signé).

### Corrections de l'analyste appliquées
1. **Lefebvre 36 min max** (48 min en J10 = `over_36`, −20 % [M§5.7]) : Q1, Q2, Q4 ; Q3 au repos, Bernard au C, Fournier au PF. Faux si son éval/min < 0,60 (`gold.bv_match_player_lines`). J11 (même plan) : Lefebvre 36 min, éval 39.
2. **Q3 avec un tireur à 3 pts** : Gimenez (Tir 3) en Q3, repos en Q2 ; Legrand au SF en Q2. Faux si Q3 ≤ −5 (`quarter_margins`). Rappel J11 : Q3 −7 avec ce même plan (1 cas, confiance faible) ; je le garde, J11 gagné +26 ; risque assumé.
3. **Focus** : Intense sur un seul joueur (Molina) ; aucun Light au-dessus de 6 % des tirs ; Light seulement 0 min / < 3 %.
4. **Rebondeur de plus** : Bernard (rebond 72) au C en Q2 et Q3, Fournier au PF en Q3. Faux si OREB < 15 % (`oreb_pct`). J11 : 23,4 %.
5. **Lancers de fin de match** : Bonnet et Lefebvre sur le terrain en Q4 et Prol. Faux si FT % < 70 % (`ft_pct`). J11 : 75,8 %.

### Faits adversaire (`gold.bv_match_opp_focus`, J1 02/11 ; `gold.bv_match_report`)
- J1 : W, quarts [14, 2, 7, 18], eFG adverse 35,9, notre eFG 63,6. Une seule rencontre en base ; rang et bilan non lus (`gold.bv_next_opponents` : timeout 500, `gold.bv_saisie_adversaires` : 12 joueurs, Preview du 27/11). Stats de saison des autres matchs de Chara : requête en timeout, donc non relues.
- Rotation : 5 joueurs à 48 min (J1), 7 à 0 min. Molina SF 35,3 % des tirs (30 tirs, 17 à 3 pts, 25 pts, 26,7 % ; notre focus Light) ; Durán C 22,4 % (19 tirs, 7 à 3 pts, 20 pts) ; Moreno SG 17,6 % (15 tirs, 7 à 3 pts, Intense : 9 pts, 13,3 %) ; Aguayo PF 17,6 % (15 tirs, 10 à 3 pts, 15 pts) ; Hernández PF 7,1 % (6 tirs, Lock `off`, 9 pts).
- Limites : compétences adverses en tranches [M§4] ; leurs focus sur nous inconnus ; effectif de J1 (02/11), 26 jours : rotation à reconfirmer sur la Preview.

### Focus défensif (obligatoire)
- **Intense (4) Molina**, Perimeter : 35,3 % des tirs en J1, 57 % de ses tirs à 3 pts (17/30), 25 pts en Light. Un seul Intense (analyste n°3). L-017 (hypothèse `off` = Lock) : Lock non pris.
- **Normal (3)** : Durán (Rim ; 22,4 %, 63 % de 2P), Aguayo (Perimeter ; 10 tirs à 3 pts sur 15), Moreno (Perimeter ; 7/15 à 3 pts ; Intense en J1 → 13,3 %, repasse à Normal : au-dessus de 6 %), Hernández (Rim ; 7,1 % > 6 %, 4 tirs sur 6 à 2 pts). Risque : les tirs de Molina vont à Durán et Aguayo (L-033 : le focus déplace les tirs) ; ils restent à Normal, aucun Light sur un tireur.
- **Light (2)** : Díaz, Romero, Vargas, Suárez, Vázquez, Navarro, Soler : 0 min et 0 tir en J1. Aucun Give up (L-006). Zone Middle évitée (L-027) : Perimeter pour les arrières et ailiers, Rim pour les intérieurs (2P dominant, News 2026-10-19). Si la Preview montre l'un d'eux à plus de 12 min, passer à Normal.

### Valeurs qui s'écartent de la règle uniforme
- Agress. 3 (écran) pour les 12 au lieu de 1 : levier agressivité 1 interdit par le compteur d'échecs (L-032, C-062 réfuté ; brief du 13/11) ; 3 = défaut du jeu.
- Tir 1 : Lefebvre, Legrand, Fournier, Bernard (profils intérieurs, L-020) ; Tir 2 : Richard, Boyer, Leclerc ; Bonnet Tir 5 (3 pts 72) ; Gimenez, Baron, Durand, Bourdon : 3. Richard Rôle 1 (passes 67). Off. focus 4 : Lefebvre, Gimenez ; 2 : Richard, Fournier. Boyer Rôle 3 / Tir 2 : en J10 l'écran avait Rôle 2 / Tir 3 ; je remets Rôle 3 / Tir 2 (à relire au vérifie). Bourdon (16 ans, forme 5, junior académie) en valeurs neutres : 24 min de ligue (variante B ci-dessous).

### Contrôle SQL (27/11, plan en `values` joint à `gold.bv_slot_fit` et `gold.bv_roster_now`)
- 4 quarts : 5 joueurs différents, 5 emplacements trouvés par quart (20/20). `height_eff` minimum 99,2 (Legrand SF Q2) ≥ 95. `fit_with_form` moyen : Q1 61,0, Q2 54,5, Q3 56,4, Q4 61,0. Aucune `injury_return_on`, aucun joueur en vente dans les cinqs.
- Minutes : Richard, Bonnet, Gimenez, Lefebvre, Fournier 36 ; Bourdon, Bernard 24 ; Boyer 12 ; Legrand, Baron, Leclerc, Durand 0 ; total 240 ; aucun au-delà de 36 (Prol. : 5 titulaires à 41, inévitable).
- Fatigue (relevé 27/11 `gold.bv_roster_now`, estimée au coup d'envoi du 28/11 = relevé × 0,9 − 0,5, 1 nuit) : Bonnet 20,35 → 17,8 ; Lefebvre 19,43 → 17,0 ; Boyer 18,53 → 16,2 ; Gimenez 18,48 → 16,1 ; Richard 18,27 → 15,9 ; Fournier 18,17 → 15,9 ; Bernard 15,73 → 13,7 ; Legrand 14,94 → 12,9. Tous ≤ 20 : aucune minute coupée. Stabilisée (`gold.bv_fatigue_plan`, tier 2, 36 min) : Bonnet 20,4, Lefebvre 19,3 (zone verte à la limite). Amical Saile 28/11 08:00 : Bonnet et Lefebvre à 0 min (C-147), aucune fatigue ajoutée.
- Forme : relevé 27/11 (semaine 2026-11-22, après le dimanche 22/11 [M§5.5]) : à jour. Gimenez 10, Fournier 8, Lefebvre 8, Legrand 7, Bonnet 7, Boyer 7, Richard 6, Bernard 6.

### Minutes de ligue pour les juniors académie (révision du 27/11 15:30, consigne de l'utilisateur)
Icône maison (`silver.bv_players.academy_junior`, relevé 27/11) : **Bourdon, Baron, Leclerc, Bernard** comptent pour le bonus homegrown (200 par minute de ligue, plafond 40 000 par semaine, versé le dimanche [M§10.1.3]) ; les 8 autres non. L'expérience monte avec les minutes de ligue, plus vite jusqu'à 21 ans ; en amical elle compte au dixième [M§5.4]. Bourdon : expérience 0, fatigue 0.

| Variante | Changement | PS au poste (`fit_with_form`) | Argent | Minutes |
|---|---|---|---|---|
| A — 12 min | Q2 : Bourdon SF à la place de Legrand | SF Q2 50,9 contre 50,6 : **+0,3** | +2 400 par match | Bourdon 12, Legrand 0 |
| **B — 24 min (retenue)** | A + Q3 : Bourdon SG à la place de Boyer | Q2 +0,3 ; SG Q3 51,8 contre 49,8 : **+2,0** | +4 800 par match ; avec Bernard 24 : 9 600 | Bourdon 24, Boyer 12, Legrand 0 |

Aucun coût en PS : Bourdon est meilleur que le joueur remplacé dans les deux cas. Aucun joueur au-delà de 36 min. Fatigue : Bourdon part de 0 ; référence 24 min au plan stabilisé = 14,1 (Bernard, `gold.bv_fatigue_plan`, brief amical du 27/11) : ≤ 20. Boyer passe de 24 à 12 min (fatigue en baisse). Corrections de l'analyste gardées : Lefebvre 36 min et au repos en Q3, Gimenez en Q3, Bernard au C en Q2 et Q3, Bonnet et Lefebvre en Q4.
Faux si Q2 ou Q3 ≤ −5 (`quarter_margins`) ou si l'éval/min de Bourdon < 0,40 (`gold.bv_match_player_lines`).

### Blessés et plan B
Aucun blessé (`injury_return_on` vide pour les 12). Plan B : SG Bonnet → Boyer (49,8) ou Richard (56,9) ; C Lefebvre → Bernard (49,3) ou Legrand (51,9) ; PG Richard → Boyer (50,6) ; SF Gimenez → Legrand (50,6). Depth chart : PG Boyer, Baron ; SG Boyer, Richard, Leclerc ; SF Legrand, Bourdon ; PF Legrand, Lefebvre ; C Bernard, Legrand. Durand exclu.

Anticipation (hypothèse) : Chara, 5 joueurs à 48 min en J1, devrait rejouer ses 5 joueurs : fatigue adverse élevée en Q4, comme en J1 (+18). Plan B : si Molina est tenu à moins de 20 % des tirs, Durán prend les tirs : Fournier / Lefebvre (défense 65) sur lui.

### Évolution et conseil
Garde : 36 min max, agressivité 3, Bonnet Tir 5, Intense × 1, plan J11 (gagné). Change : Intense sur Molina (en J1 Light) ; plus de Light sur un tireur. Teste : rotation Q3 (Gimenez + Bernard), Q3 −7 en J11. Conseil **C-149** ajouté dans `learnings.md`. Aucun levier interdit redonné. Manques : rang et bilan de Chara (timeout), focus adverses sur nous, stats de saison de Chara.

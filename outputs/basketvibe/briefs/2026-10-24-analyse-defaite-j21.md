# Analyse détaillée BasketVibe — J21 (D 87-112 à Astur Hoops) et amical (D 92-102) — 2026-10-24

Demande de l'utilisateur. Sources : `gold.bv_match_report`, `gold.bv_match_player_lines`, `gold.bv_match_opp_focus`, `gold.bv_slot_fit`, `gold.bv_player_outlook`, `silver.bv_match_events` (play-by-play de J21, lecture ciblée), `silver.bv_standings_weekly`. Règles : skills `basketvibe-tactique` et `basketvibe-joueurs` ([M§x] = manuel). Moteur v3. Briefs amont lus : match, tactique-j22 (24/10).

## 0. Les trois constats à retenir
| # | Constat | Chiffre |
|---|---|---|
| 1 | **Première mi-temps (−9) = le tir ; seconde mi-temps (−16) = les lancers francs.** Au tir en 2e mi-temps on ne perd que de 3 (36 contre 39 points), aux lancers de 13 (3 pts contre 16) | Astur 22 lancers tentés en Q3+Q4 (16/22), nous 5 (3/5), dont **0 en Q4** |
| 2 | **Lecture à corriger du brief du matin** : le problème de rebonds de J21 est notre rebond **offensif** (9,8 %, record de la saison à égalité avec J1), pas le rebond défensif ni les rebonds offensifs d'Astur | notre DREB 75,0 % (moyenne des défaites 72,6) ; OREB d'Astur 25,0 % (moyenne des défaites **27,4**, donc normal) |
| 3 | Les rebonds suivent le tir : 51 tirs ou lancers manqués chez nous contre 36 chez eux = 15 rebonds de plus à prendre pour Astur | 2 pts à 37,3 % contre 57,1 % |

## 1. J21 quart-temps par quart-temps (`silver.bv_match_events`, `gold.bv_match_report`)
Unités : A = Richard, Bonnet, Gimenez, Lefebvre, Fournier (Q1, Q3) ; B = Boyer, Dang, Durand, Legrand, Bernard (Q2, Q4) (`silver.bv_match_tactics`).
| Q | Unité | Écart | Points | Tirs (réussis/tentés) | 3 pts | Lancers | Rebonds off./déf. (nous) | OREB % / DREB % (nous) | Fautes commises |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | A | −6 | 29-35 | 9/19 (47 %) contre 13/22 (59 %) | 4 contre 5 | 7/8 contre 4/5 | 1 / 6 | 10 / 67 | 5 |
| Q2 | B | −3 | 19-22 | **7/22 (32 %)** contre 10/20 | 2 contre 2 | 3/8 contre 0/2 | 3 / 8 | 18 / 67 | 2 |
| Q3 | A | −6 | 20-26 | 7/17 (41 %) contre 8/16 | 3 contre 2 | 3/5 contre **8/11** | **0** / 8 | **0** / 89 | 7 |
| Q4 | B | **−10** | 19-29 | 9/20 (45 %) contre 9/15 (60 %) | 1 contre 3 | **0/0** contre **8/11** | 1 / 5 | 8 / 83 | 6 |
- **Q1** : perdu par la défense du tir (59 % adverse) ; nous avons bien marqué (47 %, 7/8 aux lancers).
- **Q2** : notre pire tir (7/22, 5 lancers manqués sur 8) et 14 rebonds défensifs adverses : l'unité B joue ses 3 guards à faible rebond (Boyer, Dang, Durand : 1,9 / 4,5 / 3,4 rebonds aux 36 min depuis J15, `gold.bv_match_player_lines`).
- **Q3** : 0 rebond offensif, 7 fautes, Astur 8/11 aux lancers : il perd +8 points de lancers francs sur le seul quart.
- **Q4** : le plus lourd (−10). Astur ne tire que 15 fois mais fait 9/15 et 8/11 aux lancers ; nous n'avons tiré **aucun lancer franc** et commis 6 fautes (3 tirs fautés). Pas de moment décisif : écart installé dès Q1, jamais comblé (le meilleur moment : −3 après Q2).
- Les deux unités sont à égalité (A −12 chacun, B −13 chacun) : la rotation à 24 min n'est pas en cause ici (L-010 affaibli).

## 2. J21 joueur par joueur (`gold.bv_match_player_lines`, 24,0 min chacun, aucun `over_36`, aucune sortie pour 6 fautes)
Consignes d'écran (1–5) : passe/tir · focus offensif · focus de tir ; agressivité 3 (cran 2) pour tous.
| Joueur | Poste | Pts | Tirs | 3 pts | Lanc. | Reb (o+d) | Pass. | Pertes | Fautes | +/− | Éval/min | Consignes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Bonnet | SG | **30** | 9/15 | 6/10 | 6/8 | 0+1 | 1 | 3 | 3 | −12 | **0,88** | 5·5·5 |
| Legrand | PF | 13 | 6/17 | 1/2 | 0/2 | 2+2 | 1 | 1 | 1 | −13 | 0,21 | 3·3·1 |
| Durand | SF | 11 | 4/9 | 2/3 | 1/2 | 0+1 | 0 | 2 | 3 | −13 | 0,25 | 3·3·3 |
| Lefebvre (forme 1) | PF | 10 | 5/10 | 0/0 | 0/0 | 0+6 | 2 | 2 | 1 | −12 | 0,50 | 4·4·1 |
| Bernard | C | 8 | 4/8 | 0/0 | 0/2 | 2+6 | 1 | 1 | 1 | −13 | 0,46 | 2·2·1 |
| Fournier | C | 6 | 1/4 | 0/1 | 4/5 | 1+6 | 1 | 1 | 3 | −12 | 0,50 | 2·2·1 |
| Dang | SG | 4 | **1/10** | 0/2 | 2/2 | 0+2 | 2 | 1 | 2 | −13 | 0,00 | 3·3·3 |
| Richard (forme 2) | PG | 3 | 1/3 | 1/1 | 0/0 | 0+0 | 3 | 0 | 3 | −12 | 0,21 | 1·1·3 |
| Boyer | PG | 2 | 1/1 | 0/0 | 0/0 | 0+2 | 1 | 0 | 1 | −13 | 0,33 | 2·2·3 |
| Gimenez | SF | **0** | 0/4 | 0/3 | 0/0 | 0+1 | 2 | **4** | 2 | −12 | **−0,17** | 3·3·3 |
- **Deux meilleurs** : Bonnet (30 pts en 24 min, 6/10 à 3 pts), Lefebvre/Fournier/Bernard (0,46–0,50, rebondeurs). **Plus faibles** : Gimenez (0/4, 4 pertes), Dang (1/10).
- **Unité A** : 49 pts sur 36 tirs (44 %), 10 pertes (Gimenez 4, Bonnet 3), 15 rebonds. **Unité B** : 38 pts sur **45 tirs à 35,6 %** (16/45), 5 pertes, 17 rebonds. Sans Bonnet, l'équipe tire 23/66 (34,8 %).
- **Fatigue** : la fatigue au coup d'envoi n'est pas stockée par match (**il me manque** le relevé de J21 ; on le réunit en exportant le roster avant chaque match). Valeurs actuelles (post-match) : de 5,4 (Albano) à 18,3 (Bonnet), Boyer 22,6 ; stabilisée d'un joueur à 24 min en agressivité équilibrée ≈ 12 [M§5.6.4] : zone verte (≤ 20), pénalité d'attaque ≤ 3 % [M§5.6]. **Fatigue écartée comme cause.**
- **Forme** (mise à jour du dimanche, aucune depuis) : Lefebvre 1 (−11 % attaque, −10 % défense), Richard 2, Albano 3, Fournier/Bernard/Gimenez 4 [M§5.5]. Unité A moyenne 3,2, unité B 5,6 : A, plus faible en forme, a marqué 49 contre 38 ; la forme ne l'explique pas non plus.

## 3. Astur Hoops : ce qu'ils ont fait de mieux (`gold.bv_match_opp_focus` round 21, extérieur)
| Joueur | Poste | Min | Pts | Tirs | % tirs | Lanc. tentés | Reb | Passes | Éval | Notre focus |
|---|---|---|---|---|---|---|---|---|---|---|
| Domínguez | PG | **48** | 24 | **10/12 (83 %)** | 15,4 | 6 | 9 | 7 | **32** | 3 Normal |
| Aguayo | SG | 36 | 22 | 6/12 (10 à 3 pts) | 15,4 | 7 | 4 | 4 | 24 | 3 Normal |
| Cruz | SF | 35,3 | 21 | 6/16 (37,5 %) | **20,5** | **10** | 8 | 2 | 17 | 3 Normal |
| Blázquez | C | 36 | 17 | 6/12 | 15,4 | 4 | **11** | 3 | 24 | 4 Intense |
| Boada | PF | 36 | 14 | 6/8 (75 %) | 10,3 | 0 | 10 | 4 | 26 | 4 Intense |
- Équipe Astur : 2 pts **57,1 %**, 3 pts 41,4 %, lancers 20/29 (69 %), 22 passes décisives contre 14, eFG 59,0 (moyenne des défaites adverses 54,6) ; pertes adverses 18 contre 15. Cinq joueurs à 35 min ou plus ont marqué 98 des 112 points ; Baeza (C, 12 min) a pris 9 rebonds en 12 min. Domínguez, un meneur, a pris 9 rebonds et tiré **sans aucun tir à 3 pts**, 6 lancers.
- Ils tirent aussi beaucoup de lancers contre nous : FT rate 56,8 à J10 (domicile) et 37,2 à J21 ; Cruz 10 lancers seul. Avantage du terrain à Astur [M§6.1].
- **Taille et répartition au rebond d'Astur : non en base** (il me manque la page Preview des postes de J21 ; on la réunit en ouvrant la page du match J21 et en l'exportant). Le rebond adverse n'est donc qu'une constatation.

## 4. Efficacité du focus défensif et de l'agressivité saisis
**Focus (écran 1–5)** [M§6.6] : l'écran réel de J21 n'a pas tapé les bonnes cibles (L-014).
| Groupe | Joueurs | Tirs | Points | Réussite |
|---|---|---|---|---|
| Intense (4) | Blázquez, Boada | 12/20 | 31 | 60 % |
| Normal (3), 3 plus gros scoreurs | Domínguez, Aguayo, Cruz | 22/40 | 67 | 55 % |
| Light (2) | Jiménez, Carey, Carbone, Lozano | Jiménez 4/8, Carey 0/5 | 9 pour Jiménez | — |
- Verdict : **Miss** au sens du manuel (Intense hors des deux vrais volumes du match : 15,4 % et 10,3 %). Les deux Intense ont tiré 60 % (31 pts), les trois Normal 55 % : aucun effet visible. **Un seul match** : rien de prouvé sur l'effet de l'Intense (L-012, 1 match). Aucun Lock encore en 21 matchs de ligue.
- Sur 21 matchs de ligue, le meilleur scoreur adverse a marqué **27,8 points en moyenne** (de 15 à 39), dont 17 fois en Normal (3 Give up, 1 Light). Seul le Give up (J15 Georgiou 39 pts à 31 %, J18 Hola 36, J19 Luciani 34) a donné des gros matchs à 34–39 points (L-006). Cecchetti (Wolves) : 38 pts à 71,4 % en Normal à J11.

**Agressivité** [M§6.3], ligue, quatre matchs au cran 0 (écran 1, J15–J18) contre trois au cran 2 (écran 3, J19–J21) :
| Cran | eFG adverse | FT rate adverse | Fautes `pf` | Points encaissés (J15–J18 / J19–J21) |
|---|---|---|---|---|
| 0 (écran 1) | 46,0 | 19,1 | 12,3 | 87,3 |
| 2 (écran 3) | 54,2 | 31,3 | 19,7 | 105,0 (106, 97, 112) |
- **Attention, facteur de confusion** : le cran 0 est tombé sur des équipes faibles (Thrylos 11e, San Pancrazio 12e, Sierra Nevada 10e, Póvoa 2e), le cran 2 sur BARIUM 5e, Žirmūnai 3e, Astur 7e. **Comparaison sur les mêmes quatre adversaires** (cran 2 à J4–J7, cran 0 à J15–J18) : eFG adverse 42,4 contre 46,0 (cran 0 pire de 3,6, ce que prévoit le manuel : soft ≈ +4–5 points encaissés), **FT rate 29,0 contre 19,1** (cran 0 meilleur de 9,9), fautes 15,8 contre 12,3, **points encaissés 88,0 contre 87,3 (égalité)**. Les points encaissés ne bougent donc pas ; le cran 0 économise des fautes (−3,5), de la fatigue (×0,75 contre ×1,00) et du risque de blessure (×0,85) [M§6.3, M§5.6, M§9.3]. Seul gain réel démontré : fautes et lancers. Conclusion : le passage au cran 2 (C-005) n'a pas causé J21 à lui seul, mais ne l'a pas évité ; le cran 0 reste le choix à coût nul.
- J21 : 20 fautes dont 13 en 2e mi-temps ; Astur 16 lancers réussis sur 22 en 2e mi-temps. Au FT rate de cran 0 (19,1), Astur aurait tenté ~15 lancers au lieu de 29 : **≈ −10 points** (à 69 %).

## 5. Pourquoi les rebonds reviennent dans les défaites (`gold.bv_match_report`, 12 défaites de ligue)
| Match | Écart | OREB % nous / adv. | Écart OREB % | Écart eFG | 2 pts adverse |
|---|---|---|---|---|---|
| J12 KK Uola (ext) | −59 | 13,0 / 37,5 | −24,5 | −26,9 | 72,6 |
| J1 KK Uola | −40 | 9,8 / 23,7 | −13,9 | −19,8 | 50,9 |
| J9 Žirmūnai | −33 | 22,4 / 37,0 | −14,6 | −12,5 | 58,6 |
| J3 Águias | −30 | 22,6 / 16,7 | +5,9 | −27,0 | 55,6 |
| J14 Águias | −30 | 13,6 / 20,0 | −6,4 | −9,8 | 65,2 |
| J5 Póvoa | −29 | 22,8 / 21,4 | +1,4 | −14,1 | 54,5 |
| **J21 Astur** | **−25** | **9,8 / 25,0** | **−15,2** | −13,3 | 57,1 |
| J13 Mind Readers | −23 | 20,6 / 36,5 | −15,9 | −17,0 | 63,0 |
| J2 Mind Readers | −22 | 18,4 / 36,7 | −18,3 | −5,7 | 54,0 |
| J8 BARIUM | −4 | 25,5 / 32,1 | −6,6 | −3,0 | 50,0 |
| J11 Wolves | −3 | 25,6 / 12,8 | +12,8 | −2,1 | 55,1 |
| J16 Póvoa | −3 | 20,0 / 28,9 | −8,9 | +5,5 | 56,3 |
- Écart OREB négatif dans **10 défaites sur 12** ; les 6 défaites avec écart de −13,9 ou pire (J12, J1, J9, J21, J13, J2) se perdent de 33,7 points en moyenne, les 6 autres de 16,5. Sur 21 matchs, corrélation avec l'écart final : **écart d'eFG 0,91, écart d'OREB 0,73**, pertes −0,51, lancers 0,26. Le rebond est le 2e facteur, derrière le tir.
- Moyennes des défaites contre victoires : notre OREB 9,4 contre 13,8 rebonds, 18,7 % contre 29,9 % ; DREB adverse 41,0 contre 32,4. Notre DREB % : 72,6 (défaites), 76,9 (victoires) ; pris dans l'autre sens, **l'adversaire prend 81,3 % de nos manqués en défaite contre 70,1 % en victoire**. Cause commune : notre réussite aux tirs (2 pts) et la composition au rebond ; pas un défaut d'une seule unité.
- Rebond d'équipe en ligue = moyenne des 5 sur le terrain ; la taille compte ±1,8 % par cm [M§5.1.1]. Depuis J15 (`gold.bv_match_player_lines`) : Bernard 17,0 rebonds aux 36 min, Lefebvre 14,1, Fournier 13,3, Klein 12,0, Legrand 8,1 ; Henry 5,7, Gimenez 5,1, Durand 3,4, Boyer 1,9, Richard 1,8, Bonnet 1,7.
- **Amical 24/10 : rebonds hors de cause** : OREB 14 contre 16, DREB 35 contre 37 (parité).

## 6. Amical du 24/10 (08:00, dom.) — D 92-102, cran 0, focus 3 pour tous (`gold.bv_match_report`, `gold.bv_match_player_lines`)
| Q | Écart | Cinq (d'après `periods_played`) | Lecture |
|---|---|---|---|
| Q1 | −5 | Leclerc, Bernard, Baron, Albano, Lecomte | Leclerc/Bernard 4 et 5 pertes sur le match |
| Q2 | **−20** | Leclerc, Bernard, Lecomte, Klein, Boyer | Boyer 0/3, 3 pertes, −20, éval −0,50 ; Klein −20 |
| Q3 | +15 | Baron, Albano, Lecomte, Bernard, Henry | meilleur quart (Henry +15 sur le match) |
| Q4 | 0 | Leclerc, Baron, Albano, Henry, Klein | neutre |
- Causes : **pertes 20 (20,3 %)**, passes décisives 8 contre 20, 2 pts adverse 58,2 %, 95 tirs adverses contre 83 (12 tirs de plus) ; lancers 22 tentés contre 7. Meilleurs : Bernard 16 pts 16 rebonds, Henry 16 pts en 24 min (+15), Albano 11 pts 13 rebonds. Plus faibles : Boyer (12 min, 0 pt, −20), Lecomte (6 pts, 3/10), Leclerc 22 pts mais 6/19 et 4 pertes (−25).
- Focus : 3 pour les 13 adverses (témoin C-040) : Ueda 20 pts (50 %), Ong 17 pts (43,8 % sur 16 tirs) = 31,5 % des tirs ; pas d'information sur l'effet du focus. Amical : fatigue et expérience à 1/10, pas de blessure [M§1.2] : ne sert que d'essai, jamais de tendance de ligue.

## 7. Plan J22 (Wolves Empire, lun. 26/10, verrouillage 19:45) : confirmé, à changer
Enjeu (`silver.bv_standings_weekly`) : nous 8e (29 pts), Wolves 9e (26 pts) : le 8e rang est acquis même en cas de défaite (Wolves au maximum 28) ; une victoire (31 pts) peut encore passer Astur et Mind Readers (30) selon leurs résultats.
| Élément du brief `-tactique-j22.md` | Verdict | Chiffre qui le justifie |
|---|---|---|
| Boyer, Dang, Durand à 0 min ; Klein au C et Bernard au PF en unité B | **Confirmé** | J21 B : 35,6 % aux tirs, 14 rebonds défensifs adverses en Q2 ; Klein 76,2 % (16/21), +12,0, 12,0 reb/36, Bernard 17,0 reb/36 |
| Albano au SF de l'unité A à la place de Richard | **Confirmé** | Richard 1,8 rebonds/36, 10 pertes en 6 matchs, forme 2 ; Albano 13 reb en 36 min en amical |
| Agressivité écran 1 pour les 17 (C-044) | **Confirmé** | 20 fautes et 29 lancers adverses à J21 ; cran 0 : fautes 12,3 contre 15,8 aux mêmes adversaires |
| Lock Cecchetti, Intense G. Michelotti, A. Conti/F. Conti/Casadei en Normal, Light 20–35 min, Give up moins de 15 min | **Confirmé** | 27,8 pts de moyenne du meilleur scoreur adverse ; Cecchetti 38 pts à 71,4 % à J11 ; aucun Give up à 30 min ou plus |
| Gimenez 3·3·3, Henry 3·2·3 | **À changer** (point 4) | Gimenez 3 pts 2/18 contre 2 pts 14/25 |
| Legrand focus offensif 4, Klein 3 | **À changer** (point 4) | Legrand 17 tirs à 6/17 à J21 ; Klein 76,2 % |
| Bonnet 12 min, Leclerc 12 min en Q3 | **À changer** (point 5) | Bonnet 26/52 à 3 pts depuis J15 ; Leclerc −11,3 de fit en Q3 contre −3,0 en Q4 |
| Objectif C-049 « OREB > 9,8 et DREB > 27 » | **À changer** (point 2) | cible en taux, pas en total |

## 8. Cinq points d'amélioration (écran du jeu ; J22 d'abord, puis la suite)
| # | Priorité | Où | Quoi (valeur d'écran) | Chiffre qui le justifie |
|---|---|---|---|---|
| 1 | 🟥 URGENT | Tactique J22, agressivité des 17 joueurs | **Écran 1 pour tous**, banc compris (confirme C-044). Après J22 : relire fautes ; si `pf` ≥ 17 ou FT rate adverse ≥ 30, c'est que le cran n'est pas le facteur | J21 : 29 lancers adverses (FT rate 37,2), 20 fautes, 16/22 lancers adverses en 2e mi-temps ; mêmes adversaires, cran 0 : fautes 12,3 contre 15,8, FT rate 19,1 contre 29,0, points encaissés 87,3 contre 88,0 |
| 2 | 🟥 URGENT | Cinq de chaque quart-temps J22 + objectif de contrôle | Garder Q1/Q3 = Gimenez, Bonnet, **Albano**, Lefebvre, Fournier ; Q2/Q4 = Baron (Q2) ou Richard (Q4), Henry/Leclerc, **Legrand, Bernard, Klein** ; Boyer, Dang, Durand à 0 min. **Remplacer le contrôle C-049** par : **OREB % ≥ 18,7** (moyenne de nos défaites) et **DREB % ≥ 75** ; pas la parité (indice 51,5 contre 61–66 pour Wolves) | J21 : OREB 9,8 %, 0 rebond offensif en Q3 ; Boyer/Dang/Durand 1,9 / 4,5 / 3,4 rebonds aux 36 min contre Bernard 17,0, Lefebvre 14,1, Fournier 13,3, Klein 12,0 ; Michelotti 21,4 rebonds de moyenne chez Wolves |
| 3 | 🟧 IMPORTANT | Focus défensif J22 : relire l'écran après sauvegarde, puis, après chaque match, saisir la liste des tirs réels | **Cecchetti 5 Lock, G. Michelotti 4 Intense, A. Conti 3, F. Conti 3, Casadei 3** ; Light (2) Lonfernini, R. Michelotti, Ferreira, Ricci, Santos, Yamamoto ; Give up (1) Righi, Rossi, Selva, Ugolini. Après J22 (saison 2) : Intense/Lock sur le **plus gros volume de tirs du match précédent contre ce club** puis la Preview (cible différente de l'écran de J21) | Meilleur scoreur adverse 27,8 pts de moyenne sur 21 matchs, jamais en Lock ; J21 : Domínguez 10/12 et Cruz 20,5 % des tirs en Normal, Intense sur les 15,4 % et 10,3 % |
| 4 | 🟧 IMPORTANT | Consignes d'attaque J22 | **Gimenez : focus de tir 3 → 1** (2 pts). **Henry : focus de tir 3 → 2**. **Klein : focus offensif 3 → 4**, **Legrand : 4 → 3** (valeur de J21). Le reste inchangé | Gimenez 3 pts 2/18 (11 %), 2 pts 14/25 (56 %), 17 pertes en 7 matchs ; Henry 3 pts 10/33 (30 %), 2 pts 20/31 (65 %) ; Klein 16/21 (76 %), éval 0,72/min contre Legrand 46,5 % sur 101 tirs. Klein : 21 tirs seulement, confiance moyenne [M§6.3] |
| 5 | 🟧 IMPORTANT | Minutes J22 (Q3 et Q4) | **Bonnet reste en Q3 (24 min : Q1 + Q3)** ; **Leclerc prend le SG du Q4 à la place de Henry** (Leclerc 12 min, Henry 12 min). Le bonus homegrown reste de 2 400 pour Leclerc [M§10.1.3] | Bonnet 146 pts en 7 matchs (54,5 %, 26/52 à 3 pts, +8,1), 30 pts à J21 ; fit SG Leclerc 39,4 contre Bonnet 50,7 (−11,3 si Bonnet sort) et contre Henry 42,4 (−3,0 si Henry sort) |
- Rang 8 acquis : le risque de ces choix est faible ; confiance : point 1 moyenne (adversaires non identiques), 2 haute, 3 moyenne (aucun Lock encore joué), 4 moyenne, 5 haute sur les chiffres de fit.
- **Après J22** : (a) comparer par cran en amical (C-042, 25/10 cran 2) ; (b) en saison 2 le moteur est v4 (fatigue plus dure, duels plus marqués) : refaire les points 1 et 4 sur 3 matchs v4 avant de les figer [News 2026-10-11/16/17] ; (c) le rebond reste le déficit structurel (indice 51,5) : l'enchère d'un grand de C-055 est la réponse de fond.

## 9. À reporter dans `learnings.md` (non écrit ici)
- **L-013 à corriger** : « OREB 25,0 adverse (18,7 de moyenne) » compare deux colonnes différentes ; correct : OREB nous 9,8 % (18,7 de moyenne des défaites), OREB adverse 25,0 % (27,4), DREB nous 75,0 % (72,6).
- **Nouveau L-015** (1 match) : H1 perdue au tir, H2 aux lancers (16/22 contre 3/5), en cran 2.
- **Nouveau L-016** (6 des 12 défaites) : écart OREB ≤ −13,9 = défaite de 33,7 en moyenne.
- **C-044** : ajouter le critère du point 1. **C-049** : remplacer la cible par OREB % ≥ 18,7 et DREB % ≥ 75. **Nouveau C-056** : Gimenez focus de tir 1, Henry 2, Klein focus offensif 4, Legrand 3 ; **C-057** : Bonnet 24 min, Leclerc Q4.

## Données manquantes
- Il me manque la **fatigue au coup d'envoi par joueur** de J21 : on la réunit en exportant le roster avant le verrouillage de chaque match (le relevé actuel est post-match).
- Il me manque la **taille et le Rebond d'Astur** : on les réunit en exportant la Preview des postes de la page du match.
- Il me manque le **cinq réel de Wolves** sur leurs 3 derniers matchs (déjà dans le brief tactique).

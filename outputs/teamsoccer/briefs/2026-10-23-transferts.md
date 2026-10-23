> **Révision du 2026-10-23 (remplace la vente de 4 joueurs)** : vendre seulement **3** réservistes sans avenir à Chomelix : **Hugo Martin** (GB 15 ans) 200 003 $ · **Étienne Roux** (GB 14 ans) 253 091 $ · **Nathan Lefebvre** (MC 18 ans) 331 690 $ = **784 784 $**. **Enzo Roux (DC 16 ans, Défense 85) est conservé** : il progresse de +3 par semaine à 70 % et remplace Dubois (27 ans) puis Pierre Leroy (32 ans). Solde 1 200 599 + 784 784 = 1 985 383 $ ; réserve 387 612 $ ⇒ enchère maximale sur Hassan **1 590 000 $** (prix actuel 1 499 553 $). Si le prix dépasse 1 590 000 $, vendre Enzo Roux (534 534 $) seulement à ce moment-là.

> **Correction du 2026-10-23 (remplace la vente d'Étienne Roux attaquant)** : Chomelix **garde Étienne Roux (ATT, 63)**, seul attaquant de réserve (le suivant est Thomas Roux, OVR 36). Pour financer Omar Hassan (enchère maximale 1 700 000 $), vendre à la banque quatre joueurs qui ne jouent pas : **Hugo Martin** (GB 15 ans, OVR 42,6) 200 003 $ · **Étienne Roux** (GB 14 ans, OVR 44,7) 253 091 $ · **Nathan Lefebvre** (MC 18 ans, OVR 44,7) 331 690 $ · **Enzo Roux** (DC 16 ans, OVR 43,6) 534 534 $ = **1 319 318 $**. Solde 1 200 599 + 1 319 318 = 2 519 917 $ (le jeu refuse une enchère au-dessus du solde). Effectif passe de 22 à 18 joueurs (minimum du jeu : 16). La condition « vendre Hugo Martin seulement à 24 joueurs » venait de l'agent Effectif, pas du jeu : levée. Les 750 000 $ de places basiques attendent le solde restant.

> **Décision du 2026-10-23 (arbitrage de la session, remplace « n'enchérir sur aucune annonce » pour Chomelix et « ne pas enchérir sur Hassan »)** : Chomelix **enchérit sur Omar Hassan** (milieu 20 ans, OVR 77,2, Conduite 100, Passe 90, Centres 96 ; 1 499 553 $, fin 25/10 16:01 Paris) avec une enchère maximale de **1 700 000 $**, financée en **vendant Étienne Roux** (attaquant 19 ans, OVR 63, 4e attaquant derrière Moreau 70,6, Bonnet 67,6 et M. David 65,4 ; 903 450 $ à la banque). Une recrue démarre à Forme 85 (fiche Transferts, règle 3) : la Forme 30 actuelle ne compte pas. Les 750 000 $ de places basiques passent après, le 26/10, seulement avec le solde restant. Solde 1 200 599 $ + 903 450 $ = 2 104 049 $, réserve ≈ 387 612 $ ⇒ capacité ≈ 1 716 437 $.

# Team Soccer — brief Transferts du 2026-10-23

Agent Transferts (medium + Sonnet). Fiches lues : `commun.md`, `transferts.md` ; skills `teamsoccer-club` (§ Marché), `teamsoccer-joueurs`. Briefs amont lus : Match (corrigé), Effectif, Finances-personnel, Académie, Entraînement, Tactique du 2026-10-23.
Vues : `silver.ts_transfer_listings` (L, export du 23/10 12:57 = 39 annonces, 12:58 = 5 annonces), `silver.ts_my_bids` (B), `silver.ts_finances` (SF), `gold.ts_finance_status` (F), `silver.ts_players` (J, 23/10). Heures de fin en heure de Paris.

## En tête : exports manquants et contradictions
| Point | Constat | Conséquence |
|---|---|---|
| Export Transferts | Présent (12:57 et 12:58 UTC). Total 44 annonces : 39 (noms masculins, postes GK/DEF/MID/FWD) puis 5 (noms féminins). L'attribution du lot de 39 à Chomelix et du lot de 5 à Ben Ahmed est déduite des noms, la base ne porte pas de `team_id` sur les annonces [Obs] | Aucun export à refaire aujourd'hui |
| Contradiction avec Finances et Effectif (Chomelix) | Ils demandent un milieu de banc **OVR ≥ 60** à 810 000 $ au plus. **Aucune annonce MID du marché n'a OVR ≥ 60 dans le budget** (L). Seul MID ≥ 60 : Omar Hassan (77,2) à 1 499 553 $ avec 2 offres, hors budget (capacité 812 987 $, 1 013 000 $ avec la vente de Hugo Martin) | **Relance de Finances et Effectif inutile** : le critère est inapplicable aujourd'hui, pas faux. Décision ci-dessous : aucun achat avant un nouvel export |
| Pas de contradiction | Ben Ahmed : vente de Hayashi et Ibe après le 28/10 (valeur 488 743 $ chacune, J), achat de MC à partir du 29/10, plafond 1 000 000 $ : concordent avec Finances, Effectif, Tactique (2c) et Entraînement | — |
| Offres en cours | B liste 7 annonces pour Chomelix (ids 391 à 872, jour 23/10) absentes de L (ids actuels 5315 à 5358) : annonces anciennes, aucune offre en tête visible aujourd'hui. `new_signings` = 0 cette semaine pour les deux clubs (SF) | Limite d'un achat par semaine : non entamée cette semaine [skill club] |
| Relevé du marché de Ben Ahmed | 5 annonces seulement, aucune MID utile (L). Si c'est un relevé partiel, un nouvel export serait nécessaire | Export Transferts du 29/10 de toute façon requis pour l'achat de Ben Ahmed |

## 0. Verdicts nommés, annonce par annonce (demande de l'utilisateur, 23/10)
Faits : L (44 annonces, vues 23/10 12:57 = 39 masculines → Chomelix, 12:58 = 5 féminines → Ben Ahmed ; attribution par le sexe des noms, aucune annonce douteuse), J (23/10). Heures de fin en heure de Paris (heure d'hiver à partir du 25/10 03:00 : les heures du tableau « Faits » plus bas, décalées de +2 h pour le 25/10, sont fausses ; celles-ci sont recalculées). Une nouvelle recrue démarre à **Forme 85** [fiche Transferts, règle 3 ; skill joueurs] : la Forme affichée dans l'annonce (30, 36, 40…) ne compte pas. Salaire ≈ 1 % de la valeur par semaine. Progression : +3/semaine à 14-20 ans, +2 à 21-26, +1 à 27-28 (utilisateur, 70 % d'entraînement) : elle profite autant aux joueurs du club du même âge, donc l'écart d'OVR ci-dessous reste vrai.
Références Chomelix : titulaires DEF Ounahi 90,4 / Simon 68,2 / Thomas 65,7 / Dubois 65,2, banc Leroy 56,6 et E. Roux 43,6 ; ATT Moreau 70,6 / Bonnet 67,6 / David 65,4 (banc É. Roux 63, T. Roux 36) ; GB Thomas 60,5 (Gardien 100), puis 47,6 / 44,7 / 42,6 ; MIL Roux 66,9 / David 66,7 / Robert 65,1 (Conduite 100 tous les trois), banc Leroy 49,2, Petit 44,9, Lefebvre 44,7, A. Thomas 44,4. Capacité d'achat 812 987 $ (1 013 000 $ avec Hugo Martin vendu).

### 0.1 Chomelix Cows : 39 annonces
| Annonce (fin Paris) | Âge · OVR · prix · offres | Verdict | Raison chiffrée |
|---|---|---|---|
| **Omar Hassan** MID (25/10 16:01) | 20 · 77,2 · 1 499 553 · 2 | **Lui est bon, mais intouchable** | +10,3 d'OVR sur Roux (66,9), Conduite 100, Passe 90, Endurance 92 ; Forme 85 à l'arrivée (le brief précédent se trompait en comptant Forme 30). Prix 1 499 553 > capacité 1 013 000 (manque 486 553 $), et monte avec les offres (valeur 1 281 071) |
| Fabricio Ledesma MID (25/10 17:36) | 15 · 55,4 · 511 297 · 0 | Lui n'est pas bon | +6,2 sur le banc (Leroy 49,2) seulement ; Contrôle 50, Passe 47 ; 511 297 $ = 68 % des places basiques (750 000 $ → +57 964 $ nets par match à domicile, Finances) ; salaire 5 345 $/sem |
| Mario Alberto Paz MID (25/10 04:15) | 18 · 53 · 200 003 · 0 | Lui n'est pas bon | Conduite 45 contre 86 pour Leroy : un milieu se juge à la Conduite [skill joueurs] ; +3,8 d'OVR grâce à Tête 90/Contrôle 84, inutiles au milieu |
| Nestor Quinteros MID (25/10 21:56) | 15 · 48 · 385 868 · 0 | Lui n'est pas bon | 48 < Leroy 49,2 ; Conduite 66 < 86 ; 385 868 $ |
| Lukas Richter MID (26/10 12:41) | 16 · 43 · 314 828 · 0 | Lui n'est pas bon | 43 < banc 44,4 à 49,2 |
| Sebastian Müller MID (26/10 12:42) | 14 · 41 · 239 034 · 0 | Lui n'est pas bon | 41 < banc ; Conduite 54 |
| Paulo Gomes MID (24/10 23:38) | 15 · 41 · 200 003 · 0 | Lui n'est pas bon | 41 < banc ; Conduite 53 |
| Miguel Martins MID (24/10 23:31) | 14 · 39,3 · 212 500 · 0 | Lui n'est pas bon | 39,3 < 44,4 |
| Giuliano Moretti MID (26/10 06:31) | 15 · 39 · 176 499 · 0 | Lui n'est pas bon | 39 < 44,4 ; Conduite 47 |
| Paulo Herrera MID (25/10 20:27) | 16 · 34,6 · 45 900 · 0 | Lui n'est pas bon | 34,6 ; Conduite 32 |
| Denis Drăgușin MID (24/10 07:17) | 16 · 32 · 176 499 · 0 | Lui n'est pas bon | 32 ; Conduite 56 |
| Paulo Flores DEF (26/10 03:44) | 28 · 65 · 634 522 · 0 | Lui n'est pas bon | = Dubois 65,2 (pas de titulaire à battre), +8,4 sur le banc Leroy pour 634 522 $ alors que le trou est au milieu ; Défense 77 contre 100 chez les 4 titulaires |
| Mirco Kříž DEF (25/10 19:45) | 24 · 60,5 · 634 522 · 0 | Lui n'est pas bon | 60,5 < 65,2 ; même prix que Flores |
| Frantisek Ševčík DEF (25/10 13:34) | 26 · 58,7 · 466 862 · 0 | Lui n'est pas bon | 58,7 : +2,1 sur Leroy pour 466 862 $ |
| Dylan Acuña DEF (25/10 02:14) | 17 · 58,7 · 1 409 178 · 1 | Lui n'est pas bon | Défense 100, Tête 97 mais OVR 58,7 < 65,2 ; 1 409 178 $ pour une valeur de 1 323 770 : hors capacité (812 987) |
| Kamil Moder DEF (25/10 08:20) | 25 · 58,1 · 445 645 · 0 | Lui n'est pas bon | +1,5 sur Leroy |
| Mathis Simon DEF (25/10 06:01) | 17 · 48 · 385 868 · 0 | Lui n'est pas bon | Défense 58 ; +4,4 sur E. Roux (43,6) pour 385 868 $ |
| Yordan Iliev DEF, manager (24/10 12:01) | 15 · 41,5 · 225 507 · 0 | Lui n'est pas bon | 41,5 < 43,6 |
| Miguel Sousa DEF (24/10 23:36) | 14 · 41 · 225 507 · 0 | Lui n'est pas bon | 41 < 43,6 |
| Mirco štěpánek DEF (23/10 16:22) | 15 · 40,5 · 188 006 · 0 | Lui n'est pas bon | 40,5 < 43,6 |
| Long pān DEF (26/10 01:04) | 18 · 39 · 331 690 · 0 | Lui n'est pas bon | 39 ; Défense 47 |
| Ellyes Bronn DEF (25/10 05:16) | 15 · 38 · 188 006 · 0 | Lui n'est pas bon | 38 ; Défense 38 |
| Tomáš štěpánek DEF (26/10 03:19) | 14 · 38 · 117 166 · 0 | Lui n'est pas bon | 38 |
| Dylan Slimane DEF (25/10 05:17) | 15 · 38 · 188 006 · 0 | Lui n'est pas bon | 38 |
| Adrian Keșerü DEF (24/10 07:17) | 16 · 32 · 66 817 · 0 | Lui n'est pas bon | 32 |
| Dan Rațiu DEF (23/10 19:54) | 15 · 28 · 93 282 · 0 | Lui n'est pas bon | 28 |
| Pierre Morel FWD, manager (24/10 09:01) | 29 · 65,2 · 583 100 · 0 | Lui n'est pas bon | 65,2 = David 65,4 ; Finition 73 contre 100 chez les 4 attaquants ; 29 ans |
| Ante Oršić FWD (26/10 10:26) | 27 · 62 · 511 297 · 0 | Lui n'est pas bon | 62 < É. Roux 63 (banc) ; Finition 73 |
| Sergio Agost FWD (24/10 21:51) | 16 · 51,1 · 367 200 · 0 | Lui n'est pas bon | 51,1 < 63 ; Finition 76 |
| Ciprian Camataru FWD (24/10 07:39) | 15 · 49 · 405 158 · 0 | Lui n'est pas bon | 49 < 63 ; Finition 61 |
| Marcos Muñoz FWD (24/10 10:12) | 14 · 40 · 225 507 · 0 | Lui n'est pas bon | 40 ; Finition 63 |
| Esteban Moreno FWD (26/10 05:34) | 16 · 39 · 212 500 · 0 | Lui n'est pas bon | 39 |
| Mihai Burcă FWD (24/10 07:17) | 16 · 32 · 55 706 · 0 | Lui n'est pas bon | 32 |
| Fernando Jiménez FWD (26/10 08:54) | 16 · 28 · 50 645 · 0 | Lui n'est pas bon | 28 |
| Bartosz Świderski GB (23/10 18:10) | 20 · 65,8 · 870 400 · 0 | Lui n'est pas bon | Gardien 96 contre 100 chez Thomas (60,5) : la compétence clé du poste baisse, l'OVR +5,3 vient d'ailleurs ; 870 400 $ > capacité 812 987 ; fin aujourd'hui |
| Wouter Hendriks GB (25/10 06:40) | 14 · 52 · 534 534 · 0 | Lui n'est pas bon | Gardien 89 = Thomas David (89, 47,6) déjà en 2e gardien ; 534 534 $ |
| Ettore Castelli GB (25/10 08:24) | 17 · 34 · 267 689 · 0 | Lui n'est pas bon | 34 < 42,6 (4e gardien) |
| Daniel Ribeiro GB (24/10 23:29) | 17 · 33 · 385 868 · 0 | Lui n'est pas bon | 33 < 42,6 ; 385 868 $ |
| Marcos Jiménez GB (26/10 08:54) | 16 · 28 · 33 461 · 0 | Lui n'est pas bon | 28 < 42,6 |

### 0.2 Ben Ahmed Donkey : 5 annonces
Références : MIL titulaires Mansour 63,7 / Martínez 63,7 / Kumar 63,1 (Conduite 62, Centres 79-81), banc Kobayashi 40,6 ; DEF Fernández 63,7, Fournier 62,7, Taylor 62,7, Girard 62,5, Hayashi et Ibe 61,6 (vendues le 28/10), banc V. Williams 42,3 et Yamamoto 39. Capacité 144 754 $ aujourd'hui.
| Annonce (fin Paris) | Âge · OVR · prix · offres | Verdict | Raison chiffrée |
|---|---|---|---|
| Celeste Chukwu MID (25/10 05:55) | 15 · 49,6 · 212 500 · 0 | Elle n'est pas bonne | Conduite 57 < 62 des trois titulaires : ne comble pas le trou de milieu centrale ; +9 d'OVR sur Kobayashi (40,6) seulement ; 212 500 $ > capacité 144 754 (manque 67 746 $) et la vente de Hayashi et Ibe n'a lieu que le 28/10, après la fin |
| Luna Devi DEF (24/10 07:41) | 15 · 52 · 314 828 · 0 | Elle n'est pas bonne | 52 < 61,6 ; défense déjà à 6 ; prix > capacité |
| Sakura Patel DEF (25/10 05:57) | 16 · 49 · 425 080 · 0 | Elle n'est pas bonne | 49 < 61,6 ; Passe 90 sans usage en défense ; prix > capacité |
| Lena Martínez DEF (26/10 06:49) | 16 · 48 · 445 645 · 0 | Elle n'est pas bonne | 48 < 61,6 ; prix > capacité |
| Luna Williams DEF (24/10 11:00) | 14 · 40,7 · 165 471 · 0 | Elle n'est pas bonne | 40,7 < V. Williams 42,3 ; 165 471 > 144 754 |

### 0.3 Décisions fermes (rouge d'abord)
| Pastille | Club | Action | Montant | Pourquoi |
|---|---|---|---|---|
| 🔴 | Chomelix | **N'enchérir sur aucune des 39 annonces** | 0 $ | Une seule est meilleure qu'un titulaire (Hassan, 1 499 553 $, hors capacité de 486 553 $) ; la meilleure annonce finançable, Ledesma, ne gagne que +6,2 sur le banc pour 511 297 $. Aucun achat cette semaine : la limite d'un achat par semaine reste entière jusqu'au 26/10 |
| 🔴 | Chomelix | **Utiliser la capacité sur les 5 000 places basiques le 26/10 (750 000 $)**, décision du brief Finances | 750 000 $ | +57 964 $ nets par match à domicile, remboursées en 12,9 matchs, contre +6,2 d'OVR sur un joueur de banc pour 511 297 $ |
| 🟠 | Chomelix | **Ne pas enchérir sur Hassan.** Seule voie : financer 486 553 $ de plus en vendant É. Roux (ATT, 903 450 $), que le brief Effectif n'a pas déclaré excédentaire ; je ne le conseille pas sans son accord | 0 $ | Hassan est le seul achat qui changerait l'équipe (77,2 contre 66,9) ; décision à l'utilisateur, avec Effectif |
| 🟢 | Chomelix | **Garder Hugo Martin** (4e gardien, 15 ans, 42,6, valeur 200 003 $, salaire 2 000 $/sem) | — | Effectif : vente à 24 joueurs ; aucun achat, donc 22/24. Prix à la banque : 200 003 $ quand il faudra |
| 🔴 | Ben Ahmed | **N'enchérir sur aucune des 5 annonces** | 0 $ | Aucune MC (Conduite ≥ 70), prix supérieurs à la capacité de 144 754 $ |
| 🔴 | Ben Ahmed | **Vendre Kavya Hayashi (488 743 $) puis Suki Ibe (488 743 $) à la banque après le match du 28/10** | 977 486 $ au total, sans commission | Surplus DC (6 défenseuses, 4 titulaires), 28 ans, salaires −9 774 $/sem |
| 🟠 | Ben Ahmed | **Enchère maximale de 1 000 000 $ sur une milieu centrale, à fixer sur l'export Transferts du 29/10** | ≤ 1 000 000 $ | Capacité ≈ 1 141 354 $ après vente (Finances) ; aucune annonce actuelle n'est une MC |

## 1. Chomelix Cows (team_id 18) — solde 1 200 599 $, effectif 22/24
### Faits (L, J, F) — correction : les heures de fin du 25/10 de ce tableau sont décalées de +2 h (voir § 0.1) ; « Forme 30 » de Hassan ne compte pas (recrue à Forme 85)
Annonces MID du lot (milieux, pas de poste MC/MD séparé dans L) :
| Joueur | Âge | OVR | Forme | Conduite | Prix actuel | Valeur | Offres | Fin | Type |
|---|---|---|---|---|---|---|---|---|---|
| Omar Hassan (5343) | 20 | 77,2 | 30 | 100 | 1 499 553 | 1 281 071 | 2 | 25/10 18:01 | banque |
| Fabricio Ledesma (5344) | 15 | 55,4 | 40 | 86 | 511 297 | 534 534 | 0 | 25/10 19:36 | banque |
| Mario Alberto Paz (5333) | 18 | 53 | 100 | 45 | 200 003 | 200 003 | 0 | 25/10 04:15 | banque |
| Nestor Quinteros (5347) | 15 | 48 | 100 | 66 | 385 868 | 385 868 | 0 | 25/10 23:56 | banque |
Autres MID : OVR ≤ 43 (Richter, Gomes, Müller, Martins, Moretti, Herrera, Drăgușin), sans intérêt face au banc actuel (44–49,2, J).
Banc milieu actuel : Jules Leroy 49,2 (Conduite 86), Lefebvre 44,7, Adrien Thomas 44,4 (J, Effectif).
Ventes comparables : aucune vente conclue en base (seuls 2 MID/DEF ont des offres : Hassan 2, Acuña 1). Niveau de confiance de tout prix : faible.

### Avis
- Hassan (77,2, Conduite 100, Passe 90) serait un titulaire, mais le prix actuel (1 499 553 $) dépasse le solde moins la réserve de 387 612 $ de Finances (capacité 812 987 $) et monte à chaque offre (2 offres déjà, dernier enchérisseur étranger). Forme 30 (×0,79 [skill joueurs]) : coût de remise en forme élevé. **Ne pas enchérir.**
- Ledesma (55,4, 15 ans, Forme 40) à 511 297 $ : +6 d'OVR sur le meilleur remplaçant (49,2), mais sous le seuil de 60 fixé par Effectif et Finances, et salaire ≈ 5 300 $/semaine pour un banc qui joue peu (aucun remplacement programmé, Match). Pas rentable.
- Paz et Quinteros : Conduite 45 et 66 sous le seuil de 70 qui fait un milieu [skill joueurs, compétences clés]. Non.
- Revente interdite 7 semaines après achat, effectif ≤ 24 [skill club] : un achat hors besoin bloquerait 7 semaines.

### Décisions fermes
| N° | Action | Quand | Montant | Pourquoi |
|---|---|---|---|---|
| 1 | **Ne poser aucune enchère aujourd'hui.** | — | 0 | Aucun MID ≥ 60 dans le budget (L) |
| 2 | **Enchère maximale à poser sur un milieu : 810 000 $ (plafond de Finances), uniquement sur une annonce MID avec OVR ≥ 60 et Conduite ≥ 70 apparue dans l'export du 25/10.** | Export du dimanche 25/10 au plus tard, enchère avant la fin de la semaine (lundi 26/10 00:00 Canaries) | ≤ 810 000 $ + environ 8 000 $/semaine de salaire | Seul achat de la semaine ; si rien, ne rien acheter et reporter au marché du 26/10 |
| 3 | **Ne pas vendre Hugo Martin aujourd'hui.** | À 24 joueurs seulement | 200 003 $ à la banque | Effectif 22/24, aucun achat prévu : la condition de Effectif n'est pas atteinte |

## 2. Ben Ahmed Donkey (team_id 15858) — solde 387 876 $, effectif 22/24
### Faits (L, J, F)
| Joueuse | Âge | Poste | OVR | Forme | Prix | Fin | Lecture |
|---|---|---|---|---|---|---|---|
| Celeste Chukwu (5336) | 15 | MID | 49,6 | 90 | 212 500 (valeur 225 507) | 25/10 06:55 | Conduite 57, Contrôle 69 : pas une MC (Conduite < 70) |
| Luna Devi, Sakura Patel, Lena Martínez, Luna Williams | 14–16 | DEF | 40,7–52 | — | 165 471–445 645 | 24 à 26/10 | Surplus DC déjà prévu : aucune |
Aucune annonce utile pour le trou structurel (MC Conduite ≥ 70). Toutes ces annonces finissent avant le 28/10.

### Décisions fermes
| N° | Action | Quand | Montant | Pourquoi |
|---|---|---|---|---|
| 1 | **Ne rien acheter ni enchérir jusqu'au 28/10.** | Jusqu'au 28/10 | 0 | Capacité 144 754 $ (Finances n° 4) ; aucune annonce utile (L) |
| 2 | **Vendre Kavya Hayashi et Suki Ibe à la banque, une après l'autre, après le match de coupe du 28/10 (15:35).** | 28/10, après le match | 488 743 $ chacune, ≈ 977 486 $ au total, sans commission [skill club] ; salaires −9 774 $/semaine (J) | Surplus DC de 2, 28 ans [Effectif] ; elles jouent encore les 26/10 (banc) et 28/10 (1-5-4-1, Hayashi), Tactique 2c : le 1-4-4-2 du 29/10 n'a pas besoin d'elles, le remplacement est Valentina Williams (42,3) |
| 3 | **Enchère maximale sur une milieu centrale (Conduite ≥ 70) : 1 000 000 $ au plus (plafond de Finances), uniquement sur une annonce avec Conduite ≥ 70, OVR ≥ 60, vue dans l'export du 29/10.** | À partir du 29/10, après encaissement de la vente | ≤ 1 000 000 $ + environ 10 000 $/semaine de salaire | Capacité ≈ 1 141 354 $ après vente (Finances) ; le prix juste n'est pas connu (aucune vente comparable en base) : confiance faible |
| 4 | **Ne pas surpayer : si la meilleure annonce dépasse 700 000 $, ne pas enchérir au plafond mais réexaminer le 02/11.** | 29/10 | 700 000 $ comme seuil de réflexion | L'entraînement de Conduite (Kumar, Mansour, Martínez, Schmidt ≥ 70 vers le 20/11, Entraînement) réduit le besoin à terme |

## 3. Calendrier de la limite d'achat (une action par ligne)
| Date | Club | Action |
|---|---|---|
| 24/10 | Les deux | Aucune enchère |
| 25/10 | Chomelix | Export Transferts du soir, puis Transferts relu avant l'enchère du point 1.2 |
| 26/10 00:00 (Canaries) | Les deux | Remise à zéro de la limite d'un achat |
| 28/10 après match | Ben Ahmed | Vente de Hayashi et Ibe à la banque |
| 29/10 | Ben Ahmed | Export Transferts puis enchère ≤ 1 000 000 $ |

## 4. Conseils suivis
| ID | Conseil | Critère SQL |
|---|---|---|
| C-024 | Chomelix : aucune enchère le 23/10 ; enchère ≤ 810 000 $ seulement sur un MID OVR ≥ 60 et Conduite ≥ 70 relevé le 25/10 | `silver.ts_finances.new_signings` = 0 au 24/10 ; sinon `balance` ≥ 387 612 après achat |
| C-025 | Ben Ahmed : Hayashi et Ibe vendues à la banque après le 28/10 | `silver.ts_players` 29/10 : Hayashi et Ibe absentes ; `gold.ts_finance_status.balance` ≥ 1 300 000 |
| C-026 | Ben Ahmed : MC Conduite ≥ 70 achetée ≤ 1 000 000 $ après le 29/10 | `silver.ts_players` : une joueuse avec Conduite ≥ 70 ; `new_signings` > 0 |

## Réserves
- Faits : L, B, SF, F, J du 23/10. Règles : skill club (vente banque sans commission, 1 achat par semaine, revente bloquée 7 semaines, effectif 16–24), skill joueurs. Avis : plafonds, refus de Hassan, Ledesma, seuil de 700 000 $ ; confiance faible (aucune vente comparable, marché de 44 annonces).
- Le lot de 39 annonces n'est pas relié à un club dans la base ; l'attribution à Chomelix est déduite.

> **Révision du 2026-10-23 (soir) — enchère sur Hassan** : chaque offre fait monter le prix d'environ **8,2 %** (valeur 1 281 071 $ → 1 499 553 $ après 2 offres, soit ×1,17 [Obs `silver.ts_transfer_listings`]). La prochaine offre exige donc ≈ **1 622 000 $**, puis ≈ 1 755 000 $, ≈ 1 899 000 $. L'enchère maximale de 1 590 000 $ ne permettait même pas la prochaine offre. **Décision : vendre les 4 (Hugo Martin 200 003 $, Étienne Roux GB 253 091 $, Nathan Lefebvre 331 690 $, Enzo Roux 534 534 $ = 1 319 318 $) à la banque (immédiat, au prix de la fiche, sans commission), solde 2 519 917 $, enchère maximale 2 000 000 $** (réserve 387 612 $ non touchée jusqu'à 2 132 000 $). Au-delà de 2 000 000 $ on laisse Hassan (≈ 56 % au-dessus de sa valeur). Vente par la banque et non par enchère de manager : il faut les fonds avant dimanche 16:01 Paris (l'enchère dure 72 h et prend 10 % de commission).

> **Révision du 2026-10-23 (remplace la vente de 4 joueurs)** : vendre seulement **3** réservistes sans avenir à Chomelix : **Hugo Martin** (GB 15 ans) 200 003 $ · **Étienne Roux** (GB 14 ans) 253 091 $ · **Nathan Lefebvre** (MC 18 ans) 331 690 $ = **784 784 $**. **Enzo Roux (DC 16 ans, Défense 85) est conservé** : il progresse de +3 par semaine à 70 % et remplace Dubois (27 ans) puis Pierre Leroy (32 ans). Solde 1 200 599 + 784 784 = 1 985 383 $ ; réserve 387 612 $ ⇒ enchère maximale sur Hassan **1 590 000 $** (prix actuel 1 499 553 $). Si le prix dépasse 1 590 000 $, vendre Enzo Roux (534 534 $) seulement à ce moment-là.

> **Correction du 2026-10-23 (remplace la vente d'Étienne Roux attaquant)** : Chomelix **garde Étienne Roux (ATT, 63)**, seul attaquant de réserve (le suivant est Thomas Roux, OVR 36). Pour financer Omar Hassan (enchère maximale 1 700 000 $), vendre à la banque quatre joueurs qui ne jouent pas : **Hugo Martin** (GB 15 ans, OVR 42,6) 200 003 $ · **Étienne Roux** (GB 14 ans, OVR 44,7) 253 091 $ · **Nathan Lefebvre** (MC 18 ans, OVR 44,7) 331 690 $ · **Enzo Roux** (DC 16 ans, OVR 43,6) 534 534 $ = **1 319 318 $**. Solde 1 200 599 + 1 319 318 = 2 519 917 $ (le jeu refuse une enchère au-dessus du solde). Effectif passe de 22 à 18 joueurs (minimum du jeu : 16). La condition « vendre Hugo Martin seulement à 24 joueurs » venait de l'agent Effectif, pas du jeu : levée. Les 750 000 $ de places basiques attendent le solde restant.

> **Décision du 2026-10-23 (arbitrage de la session, remplace « n'enchérir sur aucune annonce » pour Chomelix et « ne pas enchérir sur Hassan »)** : Chomelix **enchérit sur Omar Hassan** (milieu 20 ans, OVR 77,2, Conduite 100, Passe 90, Centres 96 ; 1 499 553 $, fin 25/10 16:01 Paris) avec une enchère maximale de **1 700 000 $**, financée en **vendant Étienne Roux** (attaquant 19 ans, OVR 63, 4e attaquant derrière Moreau 70,6, Bonnet 67,6 et M. David 65,4 ; 903 450 $ à la banque). Une recrue démarre à Forme 85 (fiche Transferts, règle 3) : la Forme 30 actuelle ne compte pas. Les 750 000 $ de places basiques passent après, le 26/10, seulement avec le solde restant. Solde 1 200 599 $ + 903 450 $ = 2 104 049 $, réserve ≈ 387 612 $ ⇒ capacité ≈ 1 716 437 $.

# Team Soccer — brief Finances et Stade du 2026-10-23

Agent Finances-personnel (medium + Sonnet). Fiches lues : `commun.md`, `finances-personnel.md` ; skills `teamsoccer-club` (seul chargé : prix de l'entraîneur et primes non utilisés ici). Briefs amont lus : `2026-10-23-match.md` (corrigé), `2026-10-23-effectif.md`.
Vues : `gold.ts_finance_status` (F), `gold.ts_stadium_payback` (P), `silver.ts_finances` (SF, relevé 2026-10-23 12:57 UTC), `silver.ts_stadiums` (SS).

## En tête : exports manquants et contradictions
| Point | Constat | Conséquence |
|---|---|---|
| Stade : relevé périmé | `silver.ts_stadiums` : dernier jour 2026-10-19 (places Chomelix 36 675, Ben Ahmed 25 540). P donne les mêmes places. Aucun achat de places depuis (`stadium_building` = 0 sur la semaine, SF). | Aucun blocage : le chiffre est cohérent avec les finances. Prochain export Stade seulement après un achat de places. |
| Semaine non réconciliée | Chomelix : recettes 918 080 / dépenses 966 835 (F), mais les lignes détaillées (SF) ne s'y additionnent pas (billetterie 547 716 + ventes 838 166 d'un côté ; salaires 170 253 + entretien 28 920 de l'autre). Même écart chez Ben Ahmed (dépenses 967 847 pour 115 620 de lignes détaillées). | Le `week_net` (−48 755 / +1 226) ne mesure pas la rentabilité du club : il contient des lignes que la page ne détaille pas. Je juge sur le structurel (billetterie, salaires, entretien), qui reproduit exactement `projected_season_end` (F). |
| Brief Effectif | « net +1 226 $ par semaine » (Ben Ahmed) et « −48 755 $ » (Chomelix) repris tels quels de F : valides comme chiffres de la semaine, mais pas comme tendance (voir ci-dessus). Les soldes (1 200 599 / 387 876), les 977 000 $ de vente et les 200 003 $ de Hugo Martin concordent avec la base. | Pas de contradiction sur les décisions ; relance inutile. |
| Brief Match | Aucune donnée financière. Contradiction : aucune. | — |
| Entretien | `maintenance_gap` = 0 pour les deux clubs (28 920 et 20 024 = 6 % de la billetterie pleine 482 000 et 333 725). Pas de bug cette semaine. | Recontrôler lundi 26/10. |

## 1. Chomelix Cows (team_id 18), Division I, 3e (affluence 85 %)
### Faits (F, SF)
| Poste | Valeur |
|---|---|
| Solde | 1 200 599 $ |
| Semaine en cours (depuis le lundi 19/10) | recettes 918 080, dépenses 966 835, net −48 755 (non réconcilié, voir en tête) |
| Masse salariale | 164 886 $/semaine (effectif actuel, F `wage_bill`) ; 170 253 payés cette semaine ; cumul saison 334 657 |
| Entretien du stade | 28 920 $/semaine, conforme |
| Billetterie à domicile | 409 700 $ par match de ligue (482 000 × 85 %), 5 matchs de ligue à domicile restants, 7 lundis restants |
| Cumul saison | billetterie 2 310 753 ; ventes de joueurs 1 618 340 ; achats 880 000 ; construction du stade 4 872 500 |
| Fin de saison projetée (F) | 1 892 457 $ (billetterie de ligue au rang actuel, salaires et entretien chaque lundi ; ni coupes, ni ventes, ni primes) |

### Résultat de la semaine (clôture lundi 26/10 00:05)
- Structurel : un match à domicile (Ballon Athletique hawaien, 24/10) ajoute environ 409 700 $ ; salaires + entretien coûtent environ 193 806 $. Solde net structurel d'une semaine à un match à domicile : environ **+216 000 $** ; en moyenne sur 7 semaines (5 matchs à domicile sur 7) : **+98 800 $ par semaine**. Confiance moyenne (affluence supposée constante à 85 %).
- Je ne donne pas de solde prévu au 26/10 : la semaine contient des lignes non détaillées.
- Alerte : **aucune** (`alert_negative` = false), solde jamais proche de zéro.

### Masse salariale
- 164 886 $ = 17 % des recettes de la semaine (918 080) et 40 % de la billetterie d'un seul match à domicile. **Soutenable sans vente de joueur.** Marge avant le rouge : 1 200 599 / 193 806 = plus de 6 semaines de dépenses fixes sans aucune recette.

### Stade
- Prix et recette par place occupée (P) : debout 7,50 $, basique 15 $, couverte 27,50 $, VIP 75 $ (VIP complet, 500/500). Places : 20 250 debout, 11 625 basiques, 4 300 couvertes, 500 VIP (capacité 36 675 sur 80 000).
- Remboursement en matchs à domicile (P) : basique **12,5**, debout 13,4, couverte 13,7, VIP complet. Aucune n'est remboursée dans la saison (5 matchs restants). Le basique est la meilleure place ; l'agrandissement reste un investissement sur plus de deux saisons.
- Entretien : chaque place ajoutée augmente la billetterie pleine, donc l'entretien de 6 % ; le délai de P n'en tient pas compte (avis : il est un peu plus long).

### Capacité d'achat (avis)
- Réserve de sécurité = 2 semaines de salaires + entretien = 387 612 $.
- **Capacité disponible aujourd'hui : 812 987 $** (1 200 599 − 387 612).
- Une fois Hugo Martin vendu (200 003 $, effectif 24 requis) : environ +200 000 $, et −2 000 $/semaine de salaire (1 % de la valeur, règle club).

## 2. Ben Ahmed Donkey (team_id 15858), Division III, 1re (affluence 80 %)
### Faits (F, SF)
| Poste | Valeur |
|---|---|
| Solde | 387 876 $ |
| Semaine en cours | recettes 969 073, dépenses 967 847, net +1 226 (non réconcilié) |
| Masse salariale | 101 537 $/semaine (effectif actuel) ; 95 596 payés cette semaine ; cumul 179 274 |
| Entretien | 20 024 $/semaine, conforme |
| Billetterie à domicile | 266 980 $ par match de ligue (333 725 × 80 %), 4 matchs de ligue à domicile restants, 7 lundis restants |
| Cumul saison | billetterie 1 270 821 ; ventes 1 028 745 ; achats 0 ; construction du stade 3 342 250 |
| Fin de saison projetée (F) | 604 869 $ |

### Résultat de la semaine (clôture lundi 26/10 00:05)
- Structurel : salaires + entretien 121 561 $ par semaine ; un match à domicile ajoute 266 980 $. Net structurel : +145 400 $ avec un match à domicile, **−121 561 $ sans match à domicile**. En moyenne (4 matchs à domicile sur 7 semaines) : **+31 000 $ par semaine**. Le 26/10 est à l'extérieur et le 28/10 est une coupe (billetterie partagée 50/50) : la semaine du 26/10 sera probablement négative.
- Conséquence : le solde de 387 876 $ couvre seulement 3,2 semaines de dépenses fixes sans billetterie. Alerte : aucune aujourd'hui (`alert_negative` = false), **risque de passer sous la réserve** si on achète avant la vente de Hayashi et Ibe.

### Masse salariale
- 101 537 $ = 10,5 % des recettes de la semaine (969 073) ; soutenable, mais la marge de trésorerie est faible tant que Hayashi et Ibe ne sont pas vendues (−9 800 $/semaine, Effectif).

### Stade
- Recette par place : mêmes tarifs. Places : 16 000 debout, 5 790 basiques, 3 250 couvertes, 500 VIP (capacité 25 540). Remboursement (P) : basique **13,3** matchs, debout 14,2, couverte 14,5, VIP 26,6 (complet) ; 4 matchs de ligue restants : rien de remboursé dans la saison.

### Capacité d'achat (avis)
- Réserve = 2 semaines de salaires + entretien = 243 122 $.
- **Aujourd'hui : 144 754 $** (387 876 − 243 122), donc **aucun achat avant la vente**.
- Après la vente de Hayashi et Ibe (≈ 977 000 $, prix de fiche sans commission, bank : valeur 488 743 $ × 2 d'après Effectif ; salaires −9 800/semaine → dépenses fixes 111 761, réserve 223 522) : solde ≈ 1 364 876 $, **capacité ≈ 1 141 354 $**.

## Stade (détail, ajouté le 2026-10-23)
Sources : P (`gold.ts_stadium_payback`), SS (`silver.ts_stadiums`, relevé 2026-10-19), SF (`silver.ts_finances`), F (`gold.ts_finance_status`), MR (`gold.ts_match_report`, colonnes `spectators` et `fill_pct`), règles [skill club] (prix, recette par place, entretien 6 %, table d'affluence) et [skill saison] (9 semaines, 7 matchs de ligue à domicile par saison). Calculs d'avis : entretien étalé sur 9 semaines pour 7 matchs à domicile (facteur 9/7 ; P, lui, retire 6 % par match, d'où ses chiffres un peu plus courts).

### Chomelix Cows (18) — Div I, 3e, 85 %, capacité 36 675 sur 80 000
**(1) Rentable : oui.**
| Mesure | Valeur |
|---|---|
| Billetterie par match à domicile (F) | 409 700 $ (482 000 × 85 %) ; 20/10 contre Vertigo CLUB : 409 700 encaissés (SF), identique |
| Entretien (F) | 28 920 $/semaine = 6 % × 482 000 ; 260 280 $ par saison de 9 semaines |
| Billetterie de ligue d'une saison | 7 × 409 700 = 2 867 900 $ ; entretien = 9,1 % de ce montant |
| Net par saison (ligue seule) | 2 607 620 $ ; par match à domicile 372 517 $ |
| Coût d'achat du stade (SF `total_stadium_building`) | 4 872 500 $ ; valeur des places au prix d'achat 5 403 750 ; 531 250 $ de places non facturées (déduction : même écart chez Ben Ahmed, donc dotation de départ) |
| Remboursement de l'ensemble | 13,1 matchs à domicile, soit 1,9 saison (ligue seule, sans coupes ni amicaux) |

**(2) Rempli : au taux de la table, 85 %, sans exception.** Le même pourcentage s'applique à chaque type [skill club]. Dernier match à domicile (MR 20/10) : 31 174 spectateurs sur 36 675 = 85 %. Avant : 13/10, 27 473 spectateurs à 90 % (2e), pour une capacité alors de 30 526 : +6 149 places achetées depuis.
| Type | Places | Occupées | Vides | Recette par match | Recette perdue (vides) |
|---|---|---|---|---|---|
| Debout | 20 250 | 17 212 | 3 038 | 129 094 | 22 781 |
| Basique | 11 625 | 9 881 | 1 744 | 148 219 | 26 156 |
| Couverte | 4 300 | 3 655 | 645 | 100 513 | 17 738 |
| VIP | 500 | 425 | 75 | 31 875 | 5 625 |
| Total | 36 675 | 31 174 | 5 501 | 409 700 | 72 300 |
Les places vides ne viennent pas d'un manque de public mais du rang : 1er ou 2e rang en Div I = 100 % ou 90 %.

**(3) Agrandir : OUI, des places basiques.**
| Type | Prix d'achat | Remboursement P | Remboursement avec entretien (avis) | Place restante |
|---|---|---|---|---|
| Basique | 150 $ | 12,5 matchs | **12,9** | 8 375 |
| Debout | 80 $ | 13,4 | 13,8 | 29 750 |
| Couverte | 300 $ | 13,7 | 14,1 | 5 200 |
| VIP | 1 500 $ | 25,0 | — | 0 (maximum atteint) |
- **Quantité : 5 000 places basiques = 750 000 $.** Gain : 5 000 × 15 $ × 85 % = 63 750 $ par match à domicile, moins 4 500 $/semaine d'entretien (5 000 × 15 × 6 %) ; net 57 964 $ par match ; remboursées en 12,9 matchs à domicile (1,85 saison). Après l'achat : capacité 41 675, billetterie pleine 557 000.
- **Quand : le premier lundi où le solde dépasse la réserve (387 612 $) + 750 000 = 1 137 612 $ après l'achat de milieu.** Solde actuel 1 200 599 : possible dès lundi 26/10 si aucun milieu n'est acheté le 25/10 (C-024) ; sinon le **lundi 07/12** (F : fin de saison projetée 1 892 457, moins milieu ≤ 810 000, plus Hugo Martin 200 003 = 1 282 460). Aucun achat de place avant que le choix du milieu soit tranché.
- Risque chiffré : si Chomelix tombe au 6e rang, le taux passe à 70 % (table) et le remboursement du basique à 150 ÷ (15 × (0,70 − 0,0771)) = 16,1 matchs.

**(4) Prix des billets : pas de levier.** Les prix (debout 7,50, basique 15, couverte 27,50, VIP 75 $ par place occupée) sont ceux du jeu pour tous les clubs [skill club, G:Stades et spectateurs, en vigueur depuis le 2026-09-18]. Le taux d'affluence de la table ne contient aucun terme de prix ; SS ne contient aucune colonne de prix. Il me manque : un réglage de prix de billet sur la page Stade. Voici comment on l'obtient ensemble : tu ouvres la page Stade de Chomelix, tu me dis si un champ de prix est modifiable (capture ou export Stade) ; je l'enregistre dans `docs/fiches/teamsoccer/finances-personnel.md`. Sans ce champ, 0 $ de gain possible par les prix.

### Ben Ahmed Donkey (15858) — Div III, 1re, 80 %, capacité 25 540 sur 80 000
**(1) Rentable : oui, un peu moins.**
| Mesure | Valeur |
|---|---|
| Billetterie par match à domicile (F) | 266 980 $ (333 725 × 80 %) ; le 22/10 contre BOT, SF `match_income` = 275 355 (écart de 8 375 $ non expliqué) |
| Entretien (F) | 20 024 $/semaine = 6 % × 333 725 ; 180 216 $ par saison |
| Billetterie de ligue d'une saison | 7 × 266 980 = 1 868 860 $ ; entretien = 9,6 % |
| Net par saison (ligue seule) | 1 688 644 $ ; par match à domicile 241 235 $ |
| Coût d'achat (SF) | 3 342 250 $ (places au prix d'achat 3 873 500 ; 531 250 $ non facturés) |
| Remboursement de l'ensemble | 13,9 matchs à domicile, soit 2,0 saisons |

**(2) Rempli : à 80 %, sans exception.** MR : 22/10 contre BOT, 20 432 spectateurs sur 25 540 = 80 % ; 15/10 et 12/10 : 15 192 chacun à 80 %, capacité alors de 18 990 (+6 550 places depuis le 15/10).
| Type | Places | Occupées | Vides | Recette par match | Recette perdue (vides) |
|---|---|---|---|---|---|
| Debout | 16 000 | 12 800 | 3 200 | 96 000 | 24 000 |
| Basique | 5 790 | 4 632 | 1 158 | 69 480 | 17 370 |
| Couverte | 3 250 | 2 600 | 650 | 71 500 | 17 875 |
| VIP | 500 | 400 | 100 | 30 000 | 7 500 |
| Total | 25 540 | 20 432 | 5 108 | 266 980 | 66 745 |

**(3) Agrandir : NON cette saison.**
| Type | Prix d'achat | Remboursement P | Avec entretien (avis) | Place restante |
|---|---|---|---|---|
| Basique | 150 $ | 13,3 matchs | **13,8** | 14 210 |
| Debout | 80 $ | 14,2 | 14,8 | 34 000 |
| Couverte | 300 $ | 14,5 | 15,1 | 6 250 |
| VIP | 1 500 $ | 26,6 | — | 0 |
- Raison chiffrée : la capacité d'investissement est 144 754 $ aujourd'hui puis 1 141 354 $ après la vente du 28/10, dont ≤ 1 000 000 $ vont à la milieu (décision 6). Il reste 141 000 $, soit 940 places basiques : trop peu pour peser.
- **Quand : décision en semaine 9, une fois la division et le rang de la saison suivante connus**, parce que le remboursement du basique dépend d'eux : Div II 1er (90 %) 12,2 matchs ; Div III 1er (80 %) 13,8 ; Div II 4e (70 %) ou Div III 2e (70 %) 16,1 ; Div III 3e (65 %) 17,5. Seuil : acheter si le remboursement est de 14 matchs ou moins, par 5 000 basiques (750 000 $ ; +60 000 $ par match à 80 %, moins 4 500 $/semaine d'entretien).

**(4) Prix des billets : pas de levier.** Mêmes tarifs que Chomelix, fixés par le jeu. Il me manque : un réglage de prix sur la page Stade. Voici comment on l'obtient ensemble : même démarche que Chomelix, ouvrir la page Stade de Ben Ahmed et dire si un prix est modifiable.

### Données absentes (ligne par ligne)
- Il me manque l'historique d'affluence avant le 12/10 (MR commence ce jour-là, 3 matchs à domicile chez Ben Ahmed, 2 chez Chomelix) ; voici comment on l'obtient ensemble : export des pages de match à domicile passées (une page par match, onglet « Résumé »), à déposer comme d'habitude.
- Il me manque la répartition par type de place des spectateurs d'un match réel (MR ne donne que le total) ; voici comment on l'obtient ensemble : la table d'affluence applique le même taux à chaque type, ce que je vérifie ici par le total (31 174 = 85 % × 36 675 ; 20 432 = 80 % × 25 540) ; un export de la page de match montrant les spectateurs par type confirmerait.
- Il me manque le réglage éventuel des prix (voir (4)).
- Enregistrement proposé et fait dans `docs/fiches/teamsoccer/finances-personnel.md` (section « Méthode d'analyse du stade »).

### Actions Stade (rouge d'abord)
| Pastille | Club | Action | Quand |
|---|---|---|---|
| 🔴 | Chomelix | Acheter 5 000 places basiques (750 000 $) si aucun milieu n'est pris le 25/10 ; sinon le 07/12 | Lundi 26/10 ou lundi 07/12 |
| 🟠 | Les deux | Ouvrir la page Stade et dire si un prix de billet est modifiable | Cette semaine |
| 🟠 | Ben Ahmed | Calculer le remboursement du basique avec la division et le rang de la saison suivante, acheter si 14 matchs ou moins | Semaine 9 |
| 🟢 | Les deux | Contrôler `maintenance_gap` = 0 après la clôture | Lundi 26/10 |
| 🟢 | Les deux | Déposer les pages de match à domicile passées pour l'historique d'affluence | Quand tu veux |

## 3. Ordre de priorité des dépenses (décisions fermes)
| N° | Club | Décision | Quand | Montant | Pourquoi |
|---|---|---|---|---|---|
| 1 | Chomelix | **Acheter un milieu de banc (MC/MD, OVR ≥ 60)** par l'agent Transferts, enchère maximale **810 000 $ au plus** (capacité 812 987 $) | Enchère à lancer avant dimanche 25/10 (un achat par semaine, remise à zéro lundi 00:00 Atlantique) | ≤ 810 000 $ + environ 9 000 $/semaine de salaire | Seul trou structurel (banc 44–49 contre titulaires 65–67, Effectif). Salaire négligeable face à la billetterie. |
| 2 | Chomelix | **Aucun achat de places ni d'entraîneur** | Réexaminer après la clôture du 26/10 | 0 | Basique à 12,5 matchs de remboursement, 5 matchs restants : rien n'est remboursé cette saison ; la capacité part dans le milieu. |
| 3 | Chomelix | **Vendre Hugo Martin (200 003 $) quand l'effectif atteint 24** (22 aujourd'hui + milieu = 23) | Au passage à 24 joueurs | +200 003 $ | Décision d'Effectif, confirmée : le produit passe en réserve, pas en dépense. |
| 4 | Ben Ahmed | **Aucune dépense avant le 28/10** | Jusqu'au match de coupe du 28/10 | 0 | Capacité 144 754 $ seulement ; Hayashi et Ibe couvrent encore la défense. |
| 5 | Ben Ahmed | **Mettre Hayashi et Ibe en vente à la banque après le match du 28/10** | 28/10, après le match | ≈ +977 000 $ | Décision d'Effectif ; sans commission (vente à la banque). |
| 6 | Ben Ahmed | **Acheter une milieu centrale (Conduite ≥ 70), plafond 1 000 000 $** par l'agent Transferts | À partir du 29/10, après la vente et dans la nouvelle semaine financière | ≤ 1 000 000 $ | Capacité ≈ 1 141 354 $ ; reste ≈ 141 000 $ au-dessus de la réserve. |
| 7 | Ben Ahmed | **Aucun agrandissement du stade cette saison** | Réexaminer en semaine 9 | 0 | Basique à 13,3 matchs, 4 matchs de ligue restants ; l'argent va au milieu. |
| 8 | Les deux | **Pas d'entraîneur de niveau 2 à 1 000 000 $** | Pas avant la fin de la saison | 0 | Aucun solde ne le permet en gardant la réserve après l'achat de milieu. |

Les deux achats sont dans des semaines financières différentes (Chomelix avant lundi 26/10, Ben Ahmed après le 28/10). Si un lundi la limite d'un achat par semaine s'applique à l'ensemble du compte, le skill ne le précise pas : [skill club] parle de « 1 achat par semaine » sans dire si c'est par club ; ma séquence évite le cas.

## 4. Conseils suivis
| ID | Critère SQL |
|---|---|
| C-012 | Ben Ahmed : aucun achat tant que `gold.ts_finance_status.balance` < 400 000 ; après la vente du 28/10, `balance` ≥ 1 300 000 |
| C-013 | Chomelix : milieu acheté, `silver.ts_finances.new_signings` > 0 et `balance` ≥ 387 612 au 27/10 (réserve intacte) |
| C-014 | Lundi 26/10 : `maintenance_gap` = 0 pour les deux clubs |

## Réserves
- Faits : F, P, SF du 2026-10-23. Règles : skill `teamsoccer-club` (limite d'achat, vente à la banque, entretien 6 %). Avis : réserve de 2 semaines, plafonds d'enchère et séquence.
- Hypothèses des projections : affluence au rang actuel, pas de prime ni de coupe ; les coupes partagent la billetterie 50/50 (non chiffrées).
- La valeur de 977 000 $ vient du brief Effectif (2 × 488 743 $), non revérifiée en SQL de mon côté ; le prix du milieu à acheter est inconnu (agent Transferts) : mes plafonds sont des limites, pas des prix.

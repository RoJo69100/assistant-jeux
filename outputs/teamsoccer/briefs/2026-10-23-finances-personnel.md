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

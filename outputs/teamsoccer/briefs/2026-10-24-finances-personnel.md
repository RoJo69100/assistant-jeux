# Team Soccer — brief Finances du 2026-10-24

Briefs amont lus : `2026-10-24-match.md`, `2026-10-24-effectif.md`. Sources : `gold.ts_finance_status` (as_of **2026-10-23**), `silver.ts_finances`, `gold.ts_stadium_payback`, `gold.ts_hpc_status` (as_of **2026-10-19**), `silver.ts_player_snapshots`, `silver.ts_transfer_listings`, `silver.ts_standings`. Règles : skills teamsoccer-club, teamsoccer-entrainement (HPC), fiche finances-personnel.

**Donnée périmée : aucun relevé Finances du 24/10.** Le match des Cows du 24/10 (31 174 spectateurs) n'est pas encore dans `silver.ts_finances`. Il me manque l'export Finances du 24/10 ; on le réunit comme ça : lancer le script sur la page Finances (Cows puis Ben Ahmed).

## Actions (tête de brief)
| Priorité | Club | Action | Échéance |
|---|---|---|---|
| 🟥 URGENT | Les deux | HPC : 45 TSC sur 50 = **objectif de 50 TSC investis inatteignable** avec le seul solde actuel (paiements de 0, 10, 25 ou 50 TSC par semaine [skill entrainement]) ; voir section HPC | lundi 26/10 00:00 |
| 🟧 IMPORTANT | Cows | Exporter la page Finances et la page des enchères (7 enchères en cours sans détail en base) | aujourd'hui |
| 🟧 IMPORTANT | Les deux | Contrôler lundi 26/10 que `maintenance_gap` = 0 (bug de facturation vu 13/10 et 19/10) | lundi 26/10 après 00:05 |
| 🟩 SUIVI | Les deux | Aucun achat de stade ni d'entraîneur aujourd'hui | - |

## Qui a quitté les Cows : élucidé
- **Louis Lefebvre** (player_id 322, FWD, 28 ans, OVR 58,2, valeur 838 166 $, salaire 8 382 $/sem.) : présent au relevé du 19/10 (23 joueurs), absent dès celui du 20/10 (22) [`silver.ts_player_snapshots`].
- **Vente à la banque**, immédiate au prix de la fiche, sans commission [skill club, F:2026-10-18 Admin-Dev] : annonce 5301 `listing_type = bank`, prix 838 166 $, vendeur Chomelix Cows, 0 enchère [`silver.ts_transfer_listings`]. Le chiffre colle : `player_sales_income` = 838 166 $ au 20/10 [`silver.ts_finances`].
- Autres départs : aucun (Ben Ahmed : 22 joueuses à chaque relevé du 19, 20, 23, 24/10).
- Rappel : le brief Effectif parle d'un « Lefebvre (18) » comme jeune de l'académie ; c'est un autre joueur, ne pas confondre.

## Chomelix Cows (team_id 18)

### Solde et semaine
| Poste | Montant | Source |
|---|---|---|
| Solde au 23/10 | **1 200 599 $** (−185 283 le 19/10) | `ts_finance_status` |
| Recettes de la semaine en cours | 1 385 882 $ = ventes 838 166 + billetterie 547 716 | `ts_finances` 23/10 |
| Dépenses de la semaine en cours | 0 prélevée (tombent à la clôture) | `ts_finances` |
| Dernière semaine clôturée (18/10 23:05 UTC) | recettes 918 080, dépenses 966 835, net **−48 755** | `ts_finance_status` |
| Salaires | ligne 170 253 $ (semaine close) ; masse actuelle `wage_bill` 164 886 $ (sans Lefebvre, −8 382 $ environ) | `ts_finance_status` |
| Entretien stade | 28 920 $, `maintenance_gap` = 0 (conforme) | `ts_finance_status` |

- Le solde reconstitué colle : −185 283 + 838 166 + 547 716 = 1 200 599 $ (vérifié).
- Billetterie 547 716 $ = 409 700 (match à domicile au taux de 85 %) + 138 016 (autre match à domicile, partage 50/50 d'une coupe ou d'un amical [skill club] ; le type exact n'est pas dans la base).
- Le match du 24/10 (31 174 spectateurs, 85 %) n'est pas encore compté ; estimation +409 700 $ (`gate_per_home_match`).

### Alerte et cause
- **Pas d'alerte** : solde positif, `alert_negative` = false. Retour au positif **déjà fait** (le 20/10, grâce à la vente de Lefebvre : 838 166 $).
- **Cause du déficit structurel de la dernière semaine** : −48 755 $ de net, dont salaires 170 253 + entretien 28 920 pour peu de billetterie (une semaine sans match à domicile). Sans la vente de Lefebvre, le solde serait de **362 433 $** (1 200 599 − 838 166).
- Projection fin de saison (hypothèses fiche : salaires + entretien chaque lundi, billetterie de ligue à domicile au rang actuel, ni primes ni coupes ni ventes ni amicaux) : **1 482 757 $** = 1 200 599 + 4 × 409 700 − 7 × 193 806 (`projected_season_end`, recalculé à la main).
- Estimation au lundi 26/10 00:05 : 1 200 599 + 409 700 (match du 24/10) − 193 806 (salaires + entretien) = **environ 1 416 500 $** (confiance moyenne : repose sur le relevé du 24/10 manquant).

### Masse salariale
- Salaires + entretien = 193 806 $/sem. Billetterie de ligue lissée = 4 × 409 700 / 7 = 234 114 $/sem. Marge **+40 308 $/sem.** sans aucune vente : **soutenable** à condition de rester 3e (taux 85 %). À 7e (65 % [skill club]) la billetterie tomberait à 313 000 $ par match, soit 179 000 $/sem. lissés, sous les 193 806 de charges : le rang pèse plus que les salaires.
- Salaires = 70 % de la billetterie lissée (164 886 / 234 114).

### Stade (`gold.ts_stadium_payback`)
| Type | Places | Marge au max | Remboursement (matchs à domicile) |
|---|---|---|---|
| Debout | 20 250 | 29 750 | 13,4 |
| **Basique** | 11 625 | 8 375 | **12,5** (meilleur) |
| Couverte | 4 300 | 5 200 | 13,7 |
| VIP | 500 | 0 | complet |
- Règle fiche : acheter si ≤ 14 matchs ; 12,5 est sous le seuil, mais il reste **4 matchs à domicile** cette saison (`home_league_left`) : l'investissement se rembourse sur 3 saisons. Capacité d'achat = solde − 2 semaines de charges : environ 1 416 500 − 387 612 = **1 028 900 $** après lundi, soit jusqu'à 6 859 places basiques (150 $). Coût d'un lot de 5 000 places basiques : 750 000 $.
- **Avis (confiance moyenne)** : acheter du basique **après le relevé Finances du 26/10 et après recalcul du taux avec division et rang de la saison 4** [fiche, méthode stade] ; pas d'achat avant, car le taux de 85 % dépend du 3e rang et la division future est inconnue.
- Prix des billets : fixes, aucun levier [fiche, confirmé le 2026-10-23].
- Entraîneur : prochain niveau 1 000 000 $ [fiche] ; faisable après lundi (1 416 500 > 1 000 000), mais il ne resterait que 416 500 $, soit 2,1 semaines de charges. Je ne recommande pas l'entraîneur et le stade en même temps ; l'agent Entraînement tranche le niveau actuel (il me manque le niveau d'entraîneur du jour dans mes sources).

### Ventes / achats
- Vente : Lefebvre, 838 166 $, banque, 20/10. Aucune autre.
- Achats : `total_new_signings` saison = 880 000 $ (déjà payés avant le 19/10) ; aucun achat cette semaine (`new_signings` = 0).
- **7 enchères en cours** (`silver.ts_my_bids` au 23/10 : annonces 391, 397, 440, 526, 660, 778, 872). **Il me manque leur contenu** (joueur, prix, échéance) : ces annonces ne sont pas dans `silver.ts_transfer_listings`. On le réunit comme ça : ouvrir la page Transferts > Mes enchères et exporter. Effectif à 22/24 : 2 places seulement, enchères comprises [skill club] ; un solde négatif bloque les achats, pas notre cas.
- Revente bloquée 7 semaines après tout achat [skill club].

## Ben Ahmed Donkey (team_id 15858)

### Solde et semaine
| Poste | Montant | Source |
|---|---|---|
| Solde au 23/10 | **387 876 $** (−112 482 le 19/10) | `ts_finance_status` |
| Recettes de la semaine en cours | 500 358 $ = billetterie 275 355 + prime 25 000 + ventes 200 003 | `ts_finances` 23/10 |
| Dernière semaine clôturée | recettes 969 073, dépenses 967 847, net **+1 226** | `ts_finance_status` |
| Salaires | ligne 95 596 $ ; masse `wage_bill` 101 537 $ | `ts_finance_status` |
| Entretien | 20 024 $, `maintenance_gap` = 0 | `ts_finance_status` |

- Solde vérifié : −112 482 + 200 003 + 275 355 + 25 000 = 387 876 $.
- Billetterie 275 355 $ contre 266 980 attendus : **écart 8 375 $, toujours inexpliqué** (déjà noté par la fiche) ; 8 375 = nombre de places basiques libres des Cows, coïncidence à vérifier, non conclu.
- Vente 200 003 $ : un joueur à valeur 200 003 $ vendu à la banque entre le 19 et le 20/10. Ben Ahmed compte pourtant 22 joueuses à chaque relevé ; **il me manque ce que cette vente recouvre** (l'académie révèle 3 jeunes par jour et le compte reste 22). On le réunit comme ça : lire l'historique Transferts de Ben Ahmed dans le jeu. Impact sur le plan : aucun, le cash est entré.

### Alerte et cause
- **Pas d'alerte** : `alert_negative` = false, retour au positif le 20/10. Net de la dernière semaine +1 226 $ : équilibre à la limite.
- Sans la vente (200 003 $) ni la prime (25 000 $) du jour, le solde serait de 162 873 $.
- Projection fin de saison : **604 869 $** = 387 876 + 4 × 266 980 − 7 × 121 561 (`projected_season_end`, vérifié).
- Estimation au lundi 26/10 00:05 : 387 876 − 121 561 = **266 315 $** (aucun match à domicile avant le jeudi 29/10 ; match du 26/10 à l'extérieur).

### Masse salariale
- Charges 121 561 $/sem. Billetterie lissée 4 × 266 980 / 7 = 152 560 $/sem. Marge **+30 999 $/sem.** : soutenable sans vente, **marge plus mince que les Cows**. Salaires = 66,5 % de la billetterie lissée. Rang 1 en Division III (taux 80 %) ; si le rang chute à 4 (60 %), la billetterie lissée tombe à 114 400 $/sem., sous les charges.
- Creux de trésorerie : après lundi 26/10, 266 315 $ (2,2 semaines de charges) jusqu'à la billetterie du 29/10 : sûr, pas de risque de rouge.

### Stade
| Type | Places | Marge au max | Remboursement (matchs à domicile) |
|---|---|---|---|
| Debout | 16 000 | 34 000 | 14,2 |
| **Basique** | 5 790 | 14 210 | **13,3** (meilleur) |
| Couverte | 3 250 | 6 250 | 14,5 |
- Capacité d'achat après lundi : 266 315 − 2 × 121 561 = **23 193 $** : environ 154 places basiques. **Pas d'achat de stade, pas d'entraîneur** (1 000 000 $) pour ce club ; rien à faire avant d'avoir accumulé au moins 500 000 $ (fin de saison projetée : 604 869 $, soit 360 000 $ de capacité après réserve).
- **Avis** : Ben Ahmed attend la fin de saison, recalcul du taux (division III ou II selon promotion), puis basique si ≤ 14 matchs.

### Ventes / achats
- Vente de 200 003 $ (voir plus haut). Achats : 0 (`total_new_signings` = 0). Aucune enchère recensée pour ce club dans `ts_my_bids`.

## Haute Performance (HPC) — les deux clubs
- État (`gold.ts_hpc_status`, as_of **2026-10-19**, pas de relevé plus récent) : `account_tsc` = 45, `total_tsc` investis = 0, `tsc_needed` = 50, `can_complete` = **false**, 7 lundis restants, options de la semaine 9 : gardien, défense, contrôle de balle.
- Règles [skill entrainement, P:Haute Performance, F:2026-10-10] : paiement hebdomadaire de **0, 10, 25 ou 50 TSC** (un par semaine, non modifiable), **50 TSC investis dans la saison** exigés, sinon les TSC sont rendus et tout recommence. Avec 45 TSC, le total possible est 10 + 10 + 25 = 45 ou moins : **jamais 50**. Les TSC repartent à zéro sans jeune.
- Décision : **paiement de 0 TSC lundi 26/10** (ou aucun), tant que les 5 TSC manquants ne sont pas acquis. Le choix est Premium (décision de l'utilisateur, skill). Il me manque le moyen d'obtenir 5 TSC (achat Premium ? gain ?) : on le réunit comme ça : vérifier sur la page Haute Performance et la boutique Premium si 5 TSC supplémentaires sont achetables ; si oui, le jeune de 50 TSC est possible au lundi 26/10 ou plus tard (6 lundis restants après).
- Les deux clubs ont 45 TSC chacun (comptes séparés dans la base) ; **il me manque la confirmation que le compte Premium est partagé** entre les deux clubs ou non ; à vérifier sur les deux pages.

## Données manquantes
| Donnée | Pourquoi | On la réunit comme ça |
|---|---|---|
| Relevé Finances du 24/10 | match Cows du 24/10 non compté | export de la page Finances, 2 clubs |
| 7 enchères des Cows | aucun détail en base | export Transferts > Mes enchères |
| Vente de 200 003 $ de Ben Ahmed | joueur non identifié | historique Transferts de Ben Ahmed |
| Type de l'autre match à domicile des Cows (138 016 $) | partage 50/50 non attribué | pages des matchs du 20-22/10 |
| Écart 8 375 $ de Ben Ahmed | inexpliqué depuis le 22/10 | page du match 2080323, spectateurs par type de place |
| TSC manquants (5) et compte HPC | impossibilité du plafond | page HPC et boutique Premium |
| Niveau d'entraîneur actuel | non lu aujourd'hui | agent Entraînement / page Entraîneur |

## Conseils à suivre (à ajouter à `outputs/teamsoccer/learnings.md`)
- **C-FIN-1** : aucun achat de stade ni d'entraîneur pour Ben Ahmed avant la fin de saison. Critère SQL : `gold.ts_finance_status.balance` de Ben Ahmed au 26/10 ≈ 266 000 $ (écart < 20 000).
- **C-FIN-2** : Cows, solde au 26/10 ≈ 1 416 500 $ ; achat de basique seulement après le relevé et le recalcul du taux. Critère : `silver.ts_finances.total_stadium_building` inchangé avant le 26/10.
- **C-FIN-3** : HPC, aucun paiement lundi 26/10 tant que 50 TSC ne sont pas atteignables. Critère : `silver.ts_hpc.total_tsc` = 0 au prochain relevé.

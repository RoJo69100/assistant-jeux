# Team Soccer — Finances et stade, 2026-10-27 (deux clubs)

Sources : gold.ts_finance_status, gold.ts_stadium_payback, gold.ts_hpc_status (as_of 10-19), silver.ts_finances, brief lecteur-exports du jour, skills club/entrainement, connaissance.md (2.x, 3.8-3.13, 5.x, 6.10, 8.x).

## Capacité d'investissement (lue par Transferts)
Règle : solde moins réserve de 2 semaines de salaires + entretien (fiche finances). Pas de revenu récurrent compté : le net semaine (+2,5 M / +0,62 M) vient surtout de ventes.
- **capacite_invest Chomelix Cows = 1 959 436 $** (2 328 978 − 2 × (155 851 + 28 920)). Après l'achat de places décidé ci-dessous (1 256 250) : **703 186 $ pour un joueur** (1 achat par semaine).
- **capacite_invest Ben Ahmed Donkey = 262 227 $** (505 349 − 2 × (101 537 + 20 024)). Fragile : voir l'écart ci-dessous ; **plafonner un achat à 150 000 $** tant que l'écart n'est pas expliqué.

## Alerte
| Club | Solde | Alerte | Projection fin de saison (6 lundis) |
|---|---|---|---|
| Cows | 2 328 978 | aucune, entretien 28 920 = 6 % × 482 000, écart 0 | 2 955 552 (+626 574, soit ~104 k/semaine hors ventes) |
| Ben Ahmed | 505 349 | aucune, entretien 20 024 = 6 % × 333 725, écart 0 | 843 903 (+338 554, ~56 k/semaine) |
Masse salariale : Cows 155 851/sem., Ben Ahmed 101 537/sem. Soutenable : le seul stock de ventes (3 359 956 / 1 467 782 cumulés) couvre des mois de salaire ; la billetterie à domicile (433 800 / 266 980 $ par match) couvre déjà salaires + entretien.

## Écart inexpliqué Ben Ahmed (626 910 -> 505 349, −121 561)
Faits :
1. Le 626 910 vient d'un appel annexe `cash_balance` seul (dashboard_transfers, 2026-10-25 09:17 UTC, sans team_id) : l'attribution à Ben Ahmed est probable (le solde du 23/10 était 387 876, celui des Cows 1 200 599), pas prouvée.
2. Entre les relevés finances du 23/10 (387 876) et du 27/10 (505 349) les cumuls silver montent de : match +275 355, ventes +439 037, prime/autre +25 000, salaires −95 596, entretien −20 024 = **+623 772 = week_net exact**. Le solde devrait donc valoir 1 011 648 ; il vaut 505 349 : **écart de −506 299 $** contre le calcul, dont −121 561 depuis le 25/10.
3. Aucune cause visible dans les colonnes : `total_new_signings` 0, `total_stadium_building` inchangé (3 342 250), `staff_expenses`, `youth_expenses`, `other_expenses` à 0, aucune enchère pour Ben Ahmed dans `silver.ts_my_bids` (8 ids, tous Cows).
4. Hypothèses (non vérifiées) : ventes comptées dans `total_player_sales` mais payées après la date du relevé (règlement différé) ; frais non classés (hors catégories exportées).
Il me manque : le détail des mouvements de caisse de Ben Ahmed. Pour le réunir : exporter Finances Ben Ahmed demain (mardi 28 matin, après le match Cows) et le mercredi ; si le solde bouge sans match ni vente, c'est une dépense cachée. Enregistré ici et dans le brief ; à reporter dans la fiche.
Action unique : **ne pas dépenser les 262 227 $ de Ben Ahmed avant le relevé finances du 28/10.**

## Stade (gold.ts_stadium_payback, taux 0,90 Cows / 0,80 Ben Ahmed ; prix fixes, aucun levier)
| Club | Type | Places restantes | Remboursement (matchs dom.) |
|---|---|---|---|
| Cows | basique | 8 375 | 11,8 (meilleur) |
| Cows | debout / couverte / VIP | 29 750 / 5 200 / 0 | 12,6 / 12,9 / complet |
| Ben Ahmed | basique | 14 210 | 13,3 (meilleur) |
| Ben Ahmed | debout / couverte | 34 000 / 6 250 | 14,2 / 14,5 |
- **Cows : acheter 8 375 places basiques (1 256 250 $ à 150 $)**, gain net ~105 500 $/match (8 375 × 15 × 0,90 − entretien 6 %), remboursé en 11,9 matchs à domicile (4 matchs de ligue restants + coupes : ~1,7 saison). Seuil de la fiche ≤ 14 : respecté. Risque : le moral baisse après un achat de stade (connaissance 6.10, COMPLÉTÉ) et le taux 0,90 dépend de la division et du rang (rang 2 en D1) : recalculer avant la saison 4.
- **Ben Ahmed : aucun achat de places maintenant** (basique 13,3 matchs, éligible, mais capacité 262 227 et écart non expliqué). Premier achat : 1 700 basiques (255 000 $) après le relevé du 28/10 si le solde est confirmé.

## Entraîneur
Niveau actuel 1 (Faible) au 19/10 (skill entrainement) ; niveau 2 = 1 000 000 $, bonus +15 contre +8 (barème BETA, base 3 : +0,21 point de compétence par joueur et par semaine). Rendement faible comparé aux places (105 k/match).
- **Cows : ne pas monter l'entraîneur cette semaine** (stade d'abord, 1 M > 703 186 restants). Réexaminer au relevé finances du lundi 02/11.
- **Ben Ahmed : non** (1 M > capacité).

## HPC (TSC 45/50 par club, as_of 10-19, pas d'export depuis)
Règles : 50 TSC investis dans la saison ou on repart de zéro, TSC rendus sinon ; paiements 0/10/25/50 par lundi ; un seul joueur par club ; compétence non garantie (connaissance 3.9, 3.10, 3.13 ; V-20261027-2).
- **Ne rien payer** cette semaine : ne pas atteindre 50 rend les TSC (aucune perte). L'achat de 5 TSC (45 -> 50 pour payer 25 + 25) reste une décision utilisateur ; prix des TSC : il me manque cette donnée (à relever sur la page TSC). Reste 6 lundis selon gold.ts_hpc_status (4 selon la demande : à vérifier sur l'export HPC).
- Export HPC à faire (aucune page depuis le 19/10).

## Premium
Ben Ahmed est l'équipe féminine liée au Premium (fiche commune). Date d'échéance : il me manque cette donnée (absente de la base) ; relever la date sur la page Premium. Action : **renouveler avant l'échéance** (perdre le Premium ferait perdre l'équipe féminine, connaissance 7.1/8.1 : équipe conservée seulement avec Premium annuel).

## Test
Si l'achat des 8 375 places est fait, preuve contraire : `gate_per_home_match` Cows < 433 800 + 100 000 au prochain match à domicile (31/10 vs FC Bresse).

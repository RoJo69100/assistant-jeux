# BasketVibe - Transferts, 2026-11-02 (agent Transferts, medium + Sonnet)
Sources : bronze.raw_pages export Marché 13:39 UTC (14:39 Paris, moins de 24 h) et club 08:22 UTC (id 33112, mes enchères), `gold.bv_market_candidates`, `gold.bv_transfer_history`, `gold.bv_finance_health`, `gold.bv_roster_now`. Brief amont non lu (Effectif/Finances/Tactique du 02/11 absents) : lecture directe des vues gold. Horizon : aujourd'hui.

## 1. Mes enchères
| Joueur | Mon max | Résultat | Prix | Fin (Paris) |
|---|---|---|---|---|
| Vincent Fuchs (SG 25, PS 57,7) | 300 000 | **PERDU** (7 offres, je ne menais pas ; absent du marché 13:39 UTC) | 1 010 000 | 02/11 13:52 (terminée) |
| Junaid Abbasi (SG 27, PS 59,2) | 520 000 | **PERDU en cours** : prix actuel 760 000 (3 offres) > mon max, 520 000 ne couvre plus | 760 000 et monte | 02/11 17:34 |
Solde 866 656, aucun débit (Fuchs, Abbasi non gagnés). Leçon L-028 : mes deux maximums étaient 30 % et 68 % du prix réel.
Abbasi : pas de relance. Gain +3,3 vs mon 2e SG pour 760 000+ et un rang 2 seulement (`bv_market_candidates`) ; la même somme finance mieux Lazauskas.

## 2. Mes ventes (fin 03/11 08:57 Paris, 0 offre)
Impossible d'annuler une annonce (skill transferts) : rien à faire aujourd'hui. Effectif 18, disponibles 15 (minimum 8 respecté). Salaires payés le dimanche : les deux annonces se terminent avant le prochain prélèvement (08/11), garder 2 jours ne coûte rien de plus.
| Joueur | Prix affiché | Comparables (`bv_transfer_history`, 7 jours) | Décision après la fin de l'annonce (03/11 après 08:57) |
|---|---|---|---|
| Loris Lecomte (SF 17, PS 38,1, salaire 11 846) | 25 000 | 17 ans PS 37-39 vendus : Vita 1 250, Viera 1 250, Wojtas 1 500, Pavlin 2 500 (n = 4) ; ses annonces à 101 000, 50 000, 25 000 : 0 offre | **Remettre en vente à 2 000**, libérer s'il reste invendu |
| Soan Henry (SG 27, PS 42,2, salaire 15 839) | 0 | adultes PS 42-46 : Colin 19 900, Austin 22 250, Godoy 35 000, Nakamura 50 000, Greco 60 000, Cannon 750 (n = 6) ; mais 3 annonces à 0-1 000 sans offre | **Libérer, ne pas remettre en vente** (sans indemnité, économise 15 839/semaine) |
Confiance faible (n = 4 et 6, 17 annonces sur 27 de ce profil sans offre sur le marché en cours). Preuve que j'avais tort : Henry reçoit une offre avant 08:57 (alors le garder vendu).

## 3. Cibles (finançabilité)
`capacite_invest` non lisible ; capacité retenue = `transfer_available` 866 656, `transfer_committed` 0, aucune dépense décidée (stade, académie) : 866 656 - 800 000 = 66 656 restant. Résultat hebdo estimé +76 790, salaires 321 387.
| Cible | Poste, âge, PS | Prix, offres, fin | Gain | Salaire est. | Max |
|---|---|---|---|---|---|
| **Tautvydas Lazauskas** | SG 29, 198 cm, PS 62 (2P 72, 3P 59, déf 62, athl 78, expérience 6) | 1, 0 offre, 04/11 13:57 Paris | fit 61,8 contre mon 2e SG 55,8 : **+6,0**, rang 1 au poste | 30 300 | **800 000** |
Prix de comparaison (ventes 29 ans PS 60-63) : Mansour 760 000, Gregoriou 1 010 000, Burke 1 389 150, Bartosik 1 500 000. Revente nette à 1 000 000 = 950 000, soit environ +150 000 sur 800 000. Repli si déçu : libération sans indemnité. Abandonnés : Sadykov PG 1 250 000, Słowiński 3 000 000, Cohen 1 800 000, Coutinho 1 500 000 (au-dessus de 866 656). Confiance faible : le marché a dépassé la médiane deux fois (L-028), 800 000 peut ne pas suffire ; perdre ne coûte rien. Preuve que j'avais tort : eval/min de Lazauskas sous Bonnet après 3 matchs de ligue (02/11, 04/11, 07/11), ou prix final > 800 000.

## Verdict par poste
| Poste | Verdict |
|---|---|
| SG | ACHETER Lazauskas, max 800 000 (Bonnet 51,6, Dang 49,9) |
| PG, SF, PF, C | Garder (aucune cible finançable avec gain > 3 sous 866 656) |
Conseils suivis : C-110, C-111 ; C-108 et C-109 clos perdus ; L-028.

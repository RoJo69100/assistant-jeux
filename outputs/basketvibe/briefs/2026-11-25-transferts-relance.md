# Transferts BasketVibe, relance du 25/11/2026 (13:20 Paris)

Propositions seulement : aucun achat, vente ni enchère sans accord écrit de l'utilisateur. Marché exporté à 13:00 (finances `gold.finance_health` du 25/11, âge 0 j).

## Origine du « maximum 733 875 » identique
Ce n'est pas un chiffre propre à chaque joueur : `gold.bv_market_bargains.bid_ceiling_resale` = p25 de la case x 0,95 (taxe 5 %) (`sql/gold/022_bv_transfer_history.sql`). Les cinq sont dans la même case (26-29 ans, PS 55-59,9) : p25 = 772 500, médiane = 1 010 000, n = 99. 772 500 x 0,95 = 733 875. C'est un plafond de revente sans perte, pas un avis sur le joueur. Confiance : haute sur l'origine.

## Filtres d'offre (capacité restante `capacite_invest` = 955 391 ; balance 1 792 109)
Gain = `gold.bv_market_candidates.gain_vs_my_second` (fit du candidat moins notre n°2 au poste). Prix = prix actuel, `gold.bv_market_bargains`. Heure actuelle 25/11 13:17.

| Joueur | Poste, âge, PS | Gain | Prix actuel (offres) | Max 733 875 <= 955 391 | Prix < médiane 1 010 000 | Fin (Paris) | Dans 36 h | Passe |
|---|---|---|---|---|---|---|---|---|
| Sreten Miletić | SG, 27, 59,9 | +3,0 (fit 59,3 vs n°2 56,3) | 39 000 (3) | OUI | OUI | 26/11 20:43 (~31 h) | OUI | OUI |
| Svetozar Janketić | PG, 26, 58,9 | +2,0 (58,8 vs 56,8) | 205 000 (3) | OUI | OUI | 26/11 23:50 (~34,5 h) | OUI | OUI |
| Angelo Gupta | C, 27, 56,2 | +2,0 (55,5 vs 53,5) | 1 260 (3) | OUI | OUI | 26/11 17:16 (~28 h) | OUI | OUI |
| Jin-woo Tan | SF (fit SG), 28, 58,3 | +1,8 (58,1 vs 56,3) | 0 (1) | OUI | OUI | 26/11 17:16 (~28 h) | OUI | OUI |
| Henry Thomas | PF (fit PG), 27, 56,9 | -0,5 (56,3 vs 56,8) | 1 251 (4) | OUI | OUI | 26/11 21:15 (~32 h) | OUI | NON (gain négatif) |

Réserve : aucun des quatre n'entre dans le cinq (meilleur fit déjà en place : SG 60,7, PG 59,6, C 63,2). Ils renforcent le n°2 du poste (rotation, fatigue). Le gain est donc un gain de banc, pas de cinq. Salaire estimé 26 100 à 28 400 / semaine chacun (`est_weekly_salary`).

## Police : obligatoire avant toute enchère (maximum > 250 000, inviolable 6)
Je ne peux pas lancer l'agent `police`. Les quatre restent « police d'abord » : `python pipelines/dossier.py basketvibe achat` puis agent `police`. Sans police, ne pose rien.

## Enchères maximales proposées (avis, confiance faible à moyenne)
Base : ventes comparables, case 26-29 ans PS 55-59 : n = 99 (`gold.bv_price_ref_ps`), p25 772 500, médiane 1 010 000, p75 1 405 162. L-028 : un maximum sous le p25 perd souvent. 733 875 est sous le p25 : il gagne seulement si l'enchère reste calme (prix actuels 0 à 205 000, 1 à 3 offres). Les prix peuvent monter jusqu'à la fin.
1. Miletić : max 733 875 (SG, banc fort, +3,0). Coût total : prix + 28 400/sem. Confiance moyenne.
2. Janketić : max 733 875, mais déjà 205 000 à 3 offres : risque de dépasser. Confiance faible. Fin la plus tardive (23:50).
3. Gupta : max 733 875 (C, n°2 derrière Lefebvre 63,2 ; Fournier 52,7 est n°3). Confiance faible-moyenne.
4. Tan : max 733 875, 1 seule offre à 0. Poste SF jouant SG ; confiance faible.
Finançabilité : 733 875 <= 955 391 pour un seul achat ; deux achats cumulés (1 467 750) dépassent 955 391 : au plus UN. Aucune dépense déjà décidée (`transfer_committed` 0 selon la police du jour). Recommandation : Miletić d'abord (meilleur gain, PS 59,9). Plafond à poser près de la fin, mais l'utilisateur n'agit qu'aujourd'hui : poser le maximum aujourd'hui si la police est OK. Repli si l'achat déçoit : libération sans indemnité (à confirmer, non vérifié ici) ou revente au p25 moins 5 %.
Ce qui prouvera l'erreur : prix final > 733 875, ou éval/min du joueur < Bonnet (SG 52,1) sur 3 matchs de ligue.

## Déjà jugés par la police (non refaits)
Gavrilović, Chester, Fujii : ne pas acheter (`police-2026-11-25.md`).

## Ventes
- Anselmo Albano (PF, 27, PS 48) : déjà en vente, 26 000 à 3 offres, fin aujourd'hui 18:05 (`gold.bv_market_bargains`). Rien à ajouter.
- Autres : aucune vente à proposer (`que-faire-2026-11-25.md` : 11 joueurs nécessaires, écart de force > 1,0 ; Nolan Baron police d'abord, prix attendu 1 010 000, 0 min).

## Conseils suivis
Aucun C-nnn ajouté : l'achat dépend de la police, non rendue. À ajouter si l'utilisateur donne son accord.

# BasketVibe - Transferts, vendredi 13/11/2026 11:xx Paris (agent Transferts)
Sources : export marché 09:27 UTC (10:27 Paris, moins de 24 h) ; `gold.bv_market_candidates`, `bv_finance_health`, `bv_finance_projection`, `bv_slot_fit`, `bv_sell_candidates`, `bv_price_ref_ps`, `bv_transfer_history`, `silver.bv_transfer_auctions`. Briefs amont du jour (Effectif/Finances/Tactique 13/11) non lus : absents ; dernier brief lu = quotidien 11/11 et transferts 02/11. Horizon : aujourd'hui.

## Actions (toutes à valider par écrit)
1. Enchère : **Gilberto Bermejo** (SG 26, PS 59,4), max **850 000**, fin sam. 14/11 12:54 Paris. Au-dessus de 250 000 : `python pipelines/dossier.py basketvibe achat` puis agent `police` avant d'agir (non lancé ici).
2. Ungureanu : rien à saisir. Il est déjà en vente (1 000, 0 offre, fin dim. 15/11 10:15 Paris) ; l'annonce ne s'annule pas.

## 1. Ce que les exports changent depuis le 11/11
- Mes 3 enchères proposées le 11/11 n'ont pas été posées (`bought_by_me` faux) et sont terminées le 12/11 : Bui 1 829 233 (mon max 724 375), Correia 661 000 (max 1 003 438), Azevedo 791 000 (max 1 003 438) ; `bv_transfer_history`. Correia et Azevedo auraient été gagnés sous mon max, Bui non. Rien à relancer : les 3 postes sont clos.
- Ungureanu est désormais listé (`on_transfer_list` vrai, 1 000, fin 15/11 10:15) ; Min-jun Dang (SG 30) aussi (fin 15/11 10:19). Disponibles : 11 (`bv_sell_candidates`).
- Solde 1 494 431, engagé 0, résultat hebdo estimé +98 075, masse salariale 294 625 = 53,3 % des revenus récurrents (`bv_finance_health`). Projection fin de saison (21/12) : 1 490 681, 6 paies restantes (`bv_finance_projection`). Aucune dépense décidée (stade, académie non lues) : capacité retenue = 1 494 431.
- Marché : Gimenez (SF/PG, fit 59,3 PG) blessé jusqu'au 15/11 (`bv_roster_now`).

## 2. Achats pour le cinq (finançabilité : prix <= 1 494 431, somme des max <= solde [M§10.3])
Fait : le meilleur de mon cinq est fort (C 63,1, PF 63,1, SG 60,4, PG 59,3, SF 61,1 : `my_best_fit`). Le marché ne propose aucun joueur qui dépasse mon meilleur au poste avec un prix finançable ; les gains sont sur le 2e joueur du poste (fatigue 14-15 chez Lefebvre, Fournier, Bonnet, Gimenez, Richard : `bv_roster_now`). Avis : achat de profondeur, pas d'amélioration du cinq.
| Cible | Poste, âge, PS | Prix, offres, fin | Gain (fit vs 2e du poste) | Salaire est. | Max conseillé |
|---|---|---|---|---|---|
| **Bermejo** | SG 26, 59,4 | 700 000, 1 offre, 14/11 12:54 | 59,0 vs 56,0 : +3,0, rang 2 | 28 300 | **850 000** |
| Freitas (repli, même poste) | SG 29, 59,4 | 700 000, 0 offre, 14/11 13:17 | +3,2, rang 2 | 28 000 | 850 000 (une seule des deux : 2 x 850 000 > solde) |
| Mansour | SF 29, 60,9 (joue PF 61,1) | 1 155 000, 2 offres, ce soir 20:57 | PF +2,3 vs 58,8 | 30 800 | non retenu : prix 1 155 000 déjà > médiane de la tranche |
Prix : tranche PS 55 / 26-29 ans : p25 752 500, médiane 999 500, p75 1 317 250 (n = 74, `bv_price_ref_ps`) ; médiane âge/poste SG 750 000 (n = 37, `bv_market_candidates`). 700 000 = correct, avant montée. Base du max : médiane de tranche 999 500 moins marge, soit 850 000 ; la leçon L-028 (mes max à 30-68 % du prix réel) incite à ne pas descendre sous 800 000.
Coût total Bermejo : 850 000 + 28 300 x 6 paies = 1 019 800 au pire jusqu'au 21/12 ; reste 474 631 de solde. Hebdo après achat : +98 075 - 28 300 = +69 775.
Repli si déçu : libération sans indemnité, perte = prix payé ; revente nette à la médiane p25 (752 500 x 0,95 = 714 875) : perte attendue d'environ 135 000 sur 850 000 (`bv_market_bargains`, Fini : marge p25 négative sur ce marché).
Abandonnés (finançabilité) : Biernacki SG 1 600 000 et Filipiak PG 1 500 000 > 1 494 431 ; Słowiński 3 000 000. Écartés (gain < 1) : Czarnecki +0,6.
Confiance : faible à moyenne (n = 74 et 37). Preuve que j'avais tort : prix final > 850 000, ou fit_with_form de Bermejo sous celui de Bonnet après 3 matchs.

## 3. Vente d'Ungureanu (C 27, PS 48,5)
Faits : acheté libre 21 250 le 28/10 (`bv_transfer_history`) ; salaire 19 160/sem. (`bv_roster_now`), 395 par point de PS ; potentiel nul, plateau (`bv_sell_candidates`) ; rang 6 au C (fit 48,5), 9 au PF ; 12 min en ligue sur 4 matchs.
Annonce déjà posée : départ 1 000, 0 offre, fin 15/11 10:15 Paris. Le prix de départ ne se change plus ; il n'y a donc pas de prix de mise en vente à décider.
Valeur : ventes de C 25-29 ans PS 46-52 depuis le 20/10 : 12 ventes, de 251 à 840 001, médiane environ 225 000 (`bv_transfer_history`, dispersion forte). Net après taxe 5 % : environ 214 000 à la médiane ; au p25 de ces 12 (105 000) : 99 750 ; plancher réaliste si personne n'enchérit : 1 000.
Remplaçant : Maël Bernard (C 18, PS 47,8, rang 5, fit 47,8, écart 0,7 ; potentiel élevé, 1,39 de fatigue) ; Fournier 52,5 et Lefebvre 63,1 passent avant. Impact sur le cinq : nul (rang 6). Impact masse salariale : -19 160/sem. soit 294 625 -> 275 465 ; sur 6 paies : 114 960 économisés ; résultat hebdo estimé +117 235. Disponibles 11 -> 10, minimum 9 respecté (8 requis [M§11.1]).
Avis : laisser l'annonce courir, gain total attendu = recette nette (1 000 à environ 214 000) + 114 960 de salaires. Si invendu le 15/11 : libérer sans indemnité (économie 19 160/sem., aucun frais), sauf si le test E1 sur le C l'utilise. Confiance : moyenne sur l'économie, faible sur le prix (n = 12). Preuve que j'avais tort : Bernard en rotation sous Fournier avec fit < 47,8 en ligue (une blessure au C rendrait Ungureanu utile). Rappels : revente bloquée une semaine après achat [M§11.1], taxe dégressive à l'étude [Dev 2026-10-22], non décidée.

## 4. Validation écrite requise
- Enchère Bermejo max 850 000 (dossier + police obligatoires, > 250 000).
- Alternative Freitas si Bermejo est perdu : seulement après décision écrite, fin 14/11 13:17 donc à poser aujourd'hui (max 850 000, jamais les deux cumulés).
- Libération d'Ungureanu au 15/11 s'il reste invendu (hors aujourd'hui, à reconfirmer à l'export du 15/11).
- Dang (SG 30, annonce 1 000, fin 15/11 10:19) : même logique, non traité ici (hors demande).
Conseils C-nnn : non ajoutés à `learnings.md` (consigne : n'écrire que ce brief) ; à créer après accord.

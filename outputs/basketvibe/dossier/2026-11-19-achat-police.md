# Police achat — Aldo Fontana (SG 27) — 2026-11-19 11:40

Verdict : COMPLÉTÉ PAR LA POLICE. Décision changée : NE PAS ENCHÉRIR (max 0).

| variable | valeur | source |
|---|---|---|
| Joueur, âge, poste | Aldo Fontana, 27, SG, 193 cm, PS 52 | core.market_listing ; gold.bv_market_candidates |
| Fit au poste ➕ | best_fit 51,7 contre notre meilleur fit SG 60,5 (Bonnet) et 2e 56,1 : gain vs 2e = -4,4 | gold.bv_market_candidates |
| Titulaire / remplaçant SG | Bonnet 26 ans 51,9 ; Leclerc 17 ans 42,7 | gold.roster_bilan |
| Compétences ➕ | 2P 50, 3P 50, déf 50, passes 46, drib 47, reb 47, endu 50, athl 68 | gold.bv_market_candidates |
| Potentiel, forme, blessures | « progression possible » ; forme, fatigue, blessures non exportés par le marché | bv_market_candidates.age_status |
| Salaire ➕ | ~22 000/sem. estimé ; durée de contrat non exportée | bv_market_candidates.est_weekly_salary |
| Prix | 475 000, 0 enchère, fin 19/11 21:10 Paris ; relevé 18/11 15:45 UTC (transfers) | core.market_listing ; bronze.raw_pages |
| Comparables ➕ | SG 27 ans PS 48-58 vendus : n=11, médiane 500 000, moy. 539 455, max 1 100 000 ; réf. âge/poste 600 000 (n=41) | core.market_listing |
| Capacité | capacite_invest 686 018 (solde 1 519 168, réserve 833 150, as_of 18/11) ; registre fait- absent | gold.finance_health |
| Taxe / règles | enchère max = cash requis ; style eBay ; taxe 5 % à la revente, 7 jours avant revente | kb #2706, #2662, #95 |
| Revente | marge incertaine : achat-revente de petits prix médiane -8 500 (C-075) | learnings |
| Effectif | 12 joueurs, min 8, max non fixé | gold.roster_bilan |
| Avis des amis | transferts 31 total / 29 affichées ; Discord brut : 0 ligne ; rien sur ce profil ; L-028 : la médiane sous-estime le prix final des SG | kb.py ; learnings |
| Ce qui prouvera l'erreur | (si l'utilisateur enchérit) éval/min de Fontana < Bonnet après 3 matchs de ligue | variables.md |

## Points demandés
- Gain +0,1 de note : annulé par le fit (51,7 contre 60,5 ; -4,4 vs notre n° 2). 475 000 à 686 000 pour un gain nul ; C-084 chiffrait 376 000 par point de PS.
- Âge 27 : pas de déclin avant 31, neutre.
- Salaire 22 000 : ~+1 100 000/saison à la masse salariale, réserve relevée de 2 x salaire (C-034) ; le brouillon soustrait le salaire à la capacité, ce qui est bien.
- Trésorerie : solde 1 519 168 ; après 686 018 il reste 833 150 (réserve), donc faisable mais zéro marge.
- Prix périmé : 18/11 15:45 UTC, 0 enchère ; l'enchère finit ce soir 21:10, un prix plus récent changerait seulement le coût, pas le verdict. Exports Équipe 38 h et Mes enchères 145 h à refaire (gold.exports_state).
- Plafond du brouillon 664 018 : trop haut, supérieur à la médiane 500 000 et au p75 de référence ; il paie un joueur qui ne remplace pas Bonnet.

## Couverture
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| Dossier .md | 1 | 1 | grille, kb, L-028, C-075, C-084 | autres C-nnn : autres joueurs |
| Discord brut | 0 | 0 | — | — |
| kb transferts | 31 (29 affichées, 2 obsolètes) | 29 | #2706, #2662, #95, #118 | le reste : hors profil |
| kb finances | 27 (23 affichées) | 23 | aucun | hors sujet |
| Vues gold (4 requêtes) | 5 | 5 | tout | — |

## Récidive
Brouillon sans fit ni salaire sourcés (note seule) : à ajouter à docs/regles/actives.md « achat : comparer le fit (gold.bv_market_candidates.gain_vs_my_second), pas la note ».

Carte docs/decisions/cartes/basketvibe/achat.md à compléter : ajouter la variable fit/salaire = gold.bv_market_candidates (best_fit, my_best_fit, gain_vs_my_second, est_weekly_salary). Non commitée (plafond d'appels).

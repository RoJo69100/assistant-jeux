# BasketVibe - Transferts, 2026-10-30 (agent Transferts, medium + Sonnet)
Sources : `gold.bv_market_candidates`, `bv_finance_health`, `bv_sell_candidates`, `bv_price_ref_ps` (lus le 30/10) ; briefs lecteur-exports et tactique amical 31/10 du jour, effectif 29/10. Horizon : aujourd'hui. Rien n'est lance sans accord (A-4). Marche exporte le 30/10 10:5x Paris (moins de 24 h).

## Actions a poser ce soir (avec accord)
| Priorite | Categorie | Action |
|---|---|---|
| URGENT | Transferts | Enchere maximale **650 000** sur **Clifford Perry** (PF, 28 ans, 204 cm, PS 62), fin **31/10 17:00 Paris** (prix 280 250, 6 offres) |
| IMPORTANT | Transferts | Enchere maximale **100 000** sur **Borislav Boskovic** (PF, 26 ans, 201 cm, PS 60,7), fin **01/11 01:11 Paris** (prix 500, 2 offres) : repli si Perry est perdu (je ne peux pas agir apres le 31/10 17:00) |
| SUIVI | Transferts | Garder les ventes Lecomte (50 000) et Henry (1 000), fin 31/10 22:17 UTC ; rien d'autre a vendre ni liberer |

## Cibles nommees (vue `bv_market_candidates`, finançables)
Finançabilité : `capacite_invest` non lisible (sponsor/recurring null) ; capacite retenue = solde et `transfer_available` 1 105 493, `transfer_committed` 0, aucune depense decidee (stade/academie) : 650 000 + 100 000 = 750 000 <= 1 105 493 (reste 355 493). Burke (1 200 000 > 1 105 493) : abandonne.
| Cible | Poste, age, PS | Prix, offres, fin (Paris) | Gain vs mon 2e | Salaire est./sem. | Prix de reference (`bv_price_ref_ps`, PS 60, 26-29 ans, n = 6) | Max conseille |
|---|---|---|---|---|---|---|
| Clifford Perry | PF 28, 62 (rang 2 au poste, entre top 8) | 280 250, 6 offres, 31/10 17:00 | +3,4 | 31 400 | p25 1 033 125, mediane 1 301 250 ; mediane PF 118 150 (n = 38, inconnus) | **650 000** |
| Boskovic | PF 26, 60,7 (rang 2) | 500, 2 offres, 01/11 01:11 | +2,1 | 29 900 | idem | **100 000** (repli) |
| Trajkovic | SG 26, 58,6 | 200 000, 0 offre, 01/11 01:11 | +2,3 | 27 600 | mediane SG 410 000 (n = 29) | non pose : SG deja renforce par Bonnet/Gimenez, gain faible |
Calcul du max Perry : une revente au p25 du PS 60 rapporterait 1 033 125 x 0,95 = 981 469 (confiance faible, n = 6, PS 62 un peu au-dessus de la tranche) ; 650 000 laisse environ 330 000 de marge de revente et garde 455 493 de solde. Prix final = de quoi battre le 2e maximum, donc probablement bien sous 650 000 [M§11.3]. Le meilleur poste a renforcer reste le banc PF : Legrand 48,8 et Albano 47,5 jouent 24 min en amical ; Perry (62) apporte +13 PS a ces minutes, aux cotes de Lefebvre (63).
Cout total Perry : prix + 31 400/sem. Les deux PF ensemble ajouteraient 61 300/sem. ; si les deux sont gagnes, mettre Albano (47,5, 17 668/sem.) en vente apres 1 semaine ; salaire net hebdomadaire a verifier : revenu recurrent non lisible (sponsor_weekly null), couts fixes 479 381 contre billets 342 500 + amicaux 126 392 par semaine.
Confiance : moyenne (peu de ventes comparables, marche volatil). Preuve que j'avais tort : eval/min de Perry sous celle de Legrand sur les 3 premiers matchs de ligue de la saison 2 (02/11, 04/11, 07/11) ou prix final > 450 000 (surpaye) ; test le plus proche : amical du 01/11.

## Verdict par poste
| Poste | Verdict | Joueur, prix |
|---|---|---|
| PG | Garder | Richard 56, Boyer 47,7, Baron 43,8 ; Wozniak 61,7 a 2 038 000 non financable |
| SG | Garder | Bonnet 51,4, Dang 49,9 (30 ans), Gimenez 59,7 y joue (rang 1) ; Burke abandonne, Trajkovic +2,3 non retenu |
| SF | Garder | Gimenez 59,7 ; Butkus (60,7, 410 000, +0,9) gain trop faible pour 29 500 de salaire |
| PF | ACHETER | Perry 650 000 max (repli Boskovic 100 000) |
| C | Garder | Fournier 52,3, Ungureanu 48,3, Bernard 46,8 (18 ans, pot. 10) ; Tan (PF/C 55,4, 1 000 000, 0 offre) gain +2,5 : hors budget raisonnable |

## Etat de mes ventes
| Joueur | Prix | Offres | Fin | Decision |
|---|---|---|---|---|
| Klein (C) | 1 000 | - | VENDU, regle le 29/10 19:17 UTC, net 950 (taxe 5 %) | clos |
| Lecomte (SF 17 ans, PS 37,9, pot. 5, salaire 11 846) | 50 000 | 0 | 31/10 22:17 UTC | LAISSER en vente |
| Henry (SG 27 ans, PS 42,1, salaire 15 839) | 1 000 | 0 | 31/10 22:17 UTC | LAISSER en vente |
Effectif : 16 joueurs, 15 disponibles apres mise en vente (`available_players` = 15, minimum 8 respecte). Si les deux partent : -27 685 $/sem.

## Contradiction Lecomte (tactique du 31/10, 36 min) : aucune, je tranche
L'amical est le 31/10 a 08:00 Paris (07:00 UTC) ; la vente se termine le 31/10 a 22:17 UTC, soit 15 h apres. Un joueur en vente reste au club et joue jusqu'au reglement ; l'annonce n'a aucune offre. Decision : vendre quand meme (0 minute de ligue, rang 15, pot. 5, 11 846/sem.), et garder son plan de 36 min de l'amical du 31/10. Seule consequence : s'il part (improbable, deja invendu le 29/10), l'amical du 01/11 doit etre refait sans lui (agent Tactique). Preuve que j'avais tort : une offre arrive avant 08:00 le 31/10 et le joueur disparait du roster avant le verrou 07:45 (non, la vente ne se regle qu'a la fin).

## Conseils suivis (a ajouter au learnings)
C-101 Perry max 650 000 ; C-102 Boskovic max 100 000 ; critere : joueur present dans `gold.bv_roster_now` et eval/min >= Legrand apres 3 matchs de ligue.

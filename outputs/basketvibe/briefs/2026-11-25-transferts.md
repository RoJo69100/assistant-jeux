# Transferts BasketVibe — mercredi 25/11/2026, 10:36 Paris

**Exporte le marché** (page Marché, avant toute enchère). Dernière vue en base : 24/11 22:21 Paris (`core.market_listing`, `seen_at`). Les 20 annonces de `gold.bv_market_candidates` ont toutes une fin entre 24/11 21:42 et 25/11 09:18 : aucune n'est encore ouverte à 10:36. Aucune enchère n'est donc posable sur ces annonces.

## Cibles (faits : `gold.bv_market_candidates`, `gold.bv_slot_fit`)
Postes à améliorer : PG n°2 (Richard, fit 56,8), SG n°2 (Lefebvre, 56,1), C n°2 (Gimenez, 53,5). Notre n°1 : PG Gimenez 59,6, SG Gimenez 60,7, PF/C Lefebvre 63,2.

Filtre d'offre du plan : le candidat doit battre notre n°2 au poste (`gain_vs_my_second` > 0) ou être un jeune de 16-18 ans à fort potentiel. Le potentiel n'est pas dans `core.market_listing`, donc le volet jeune ne peut pas être confirmé. Le texte de la tâche renvoie à `etat_jour.offres_du_jour` (`pipelines/etat_jour.py`) ; je n'ai pas relancé ce script, car seul le SQL m'est ouvert.

| Candidat | Poste, âge | Gain vs n°2 | Prix actuel (offres) | Fin (Paris) | Filtre | Finançable (capacité 660 141, C1 du 23/11) |
|---|---|---|---|---|---|---|
| Paolo Kim | PF 26, PS 59,2 | +5,6 (C) | 4 500 023 (0) | 25/11 09:17 | passe le gain, fin passée | non, au-dessus de la capacité et de 250 000 |
| Tymon Chmielewski | PG 26, PS 61,1 | +4,3 | 3 000 023 (0) | 25/11 09:18 | passe le gain, fin passée | non |
| Nam-joon Ra | C 25, PS 56,9 | +3,3 | 3 500 000 (0) | 25/11 08:25 | passe le gain, fin passée | non |
| Damián Benavides | PG 29, PS 59,6 | +2,6 | 2 200 000 (0) | 24/11 21:57 | passe le gain, fin passée | non |
| Maurice Bowers | C 26, PS 54,3 | +0,5 | 2 222 222 (0) | 24/11 23:16 | gain négligeable, fin passée | non |
| Albert de Groot | PG 28 | −1,0 | 760 000 (2) | 25/11 05:24 | échoue | police du 24/11 : ne pas acheter |
| Baptiste Perrin | PG 25 | −0,4 | 2 000 000 (0) | 25/11 08:27 | échoue | non |
| Arturo Santos | PF 25 | −1,9 | 2 222 222 (0) | 24/11 23:35 | échoue | non |
| Jeunes : Ferreyra PG 16 (PS 34,1), Lopes SF 17 (37,3), Lapé C 17 (43,7), Rinaldi C 18 (44,7), Al-Abbas SF 18 (42,1) | | gain −15 à −23 | 501 à 1 200 000 | tous passés | potentiel inconnu, fin passée | Al-Abbas, Rinaldi, Lapé et Lopes dépassent leur médiane d'âge/poste (`gold.bv_market_bargains`, `discount_pct` négatif) |

Aucun candidat ne passe à la fois les filtres, la finançabilité et une fin d'enchère à venir. Les quatre profils à gain positif demandent 2,2 à 4,5 M pour une capacité de 660 141. Abandon par la règle de finançabilité (E8), et la vente comparable la plus proche est loin du prix (`bv_market_bargains.resale_margin_median` entre −1,2 M et −2,1 M).

Verdicts de police respectés (14 derniers jours, `outputs/basketvibe/police-*.md`) : ne pas acheter Arevalo, Castro, Lewicki, Varela (19-22/11), de Groot, Fedorenko (23-24/11). De Groot est encore listé (PG 28 ans, 760 000, fin 05:24, passée) : on ne l'achète pas. Aucun d'eux ne revient avec un gain positif.

Repli : aucun achat n'est proposé, donc aucun coût de libération. Gain attendu de la prochaine cible valable : jusqu'à +5,6 points de fit (Kim, C) à 4,5 M, hors budget. Confiance faible : le marché affiché est périmé.

## Ventes et enchères ouvertes
- Enchères de l'utilisateur : la dernière annonce `is_mine` en base date du 13/11 (Ungureanu, Dang, 1 000, sans offre, terminées). Aucune enchère ouverte connue. Aucun achat issu d'un conseil récent à revendre.
- En vente : Anselmo Albano (PF 27, PS 48, forme 8, `gold.bv_roster_now.on_transfer_list` = True). Il est rang 5 à 7 dans tous les postes (fit 42-48), donc hors rotation. Aucune annonce Albano dans les exports du marché depuis l'achat d'octobre (9 999) : l'état réel (offre, fin) est inconnu, d'où l'export demandé. Effectif 12, minimum 9 : une vente laisse 11.
- Décision par poste : garder tous les titulaires (PG Gimenez/Richard, SG Gimenez/Lefebvre, SF Gimenez/Lefebvre, PF/C Lefebvre). Albano : le laisser en vente. Si l'export montre une offre, ce brief ne fixe pas de minimum (prix de référence non lu, confiance basse). Aucune vente au-dessus de 250 000 n'est en jeu.
- Finances : balance 1 772 459 au 24/11 (`gold.bv_finance_projection`), fin de saison projetée 1 735 688. Capacité d'investissement 660 141 reprise de la police du 24/11.

## Candidats police
aucun

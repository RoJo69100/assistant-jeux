# Six Zero League — brief Transferts, 2026-10-27

Marché : export du 27/10 19:41 UTC (`silver.sz_transfer_listings`, 33 annonces, à jour, toutes `settle_after_round` = 18, règlement au coup d'envoi de J18 ce soir 21:00 Paris [skill communauté]). Brief amont lu : Match 27/10 (composition J18 inchangée). Pas de `resume.md` pour ce jeu : lu fiche transferts + brief du 26/10. Skill club (frais, paliers).

## En tête : aucune action de marché ce soir
| Priorité | Catégorie | Action |
|---|---|---|
| 🟩 SUIVI | Transferts | **Ne rien acheter, ne rien vendre** avant le relevé de la saison suivante |
- Raison chiffrée : solde **31 €** (`silver.sz_finances`, 27/10). Prix de départ minimum 1 000 €, frais de mise en vente 500 € (prélevés tout de suite), libération 500 € [skill club] : **aucune des trois opérations n'est payable**. Prévision de la semaine 9 : net +213 € (revenus 2 678, dépenses 2 465, dont salaires 1 700) soit ≈ 244 € en fin de saison, **+480 € par victoire de ligue** (prime Yarrow) : même avec la victoire de J18, ≈ 724 €, sous le premier palier de 1 000 €.
- Ce n'est pas « ne rien changer » : le marché n'est pas le levier de J18. Les leviers sont tactiques (Fournier CB, right-center, brief Match) et la Youth Academy 6 (déjà faite).

## Ventes et enchères ouvertes (vérifiées)
| Élément | État | Source |
|---|---|---|
| Joueurs de notre club en vente | **aucun** (16 joueurs, `for_sale` faux) | `silver.sz_players` 27/10 |
| Enchères posées par nous | **aucune** | aucune annonce où nous sommes `highest_bidder` |
| C-035 Oliveira (CB, 2 500 €) | **clos** : plus au marché, pas dans notre effectif (acheté par un autre ou non relisté) ; prix final non lisible | `silver.sz_transfer_listings`, `silver.sz_players` |
| C-036 Kristensen (LB, 3 000 €) | **clos** : idem | idem |
| Joueur acheté sur conseil à revendre | aucun (Fournier = pick U18, pas un achat) | — |

## Cibles nommées (non finançables ce soir ; repère pour la saison suivante)
Nos titulaires : LB A. Bertin 10, RB Roger 11, P Benoit 10, LW Lefebvre 14, RW Dupont 11, GK Bourgeois 12, CB Fournier 17 (`silver.sz_players`). Prix actuel / prochain palier, salaire par cycle :
| Annonce | Âge | Note | Poste | Prix actuel → prochain | Salaire | Gain | Verdict |
|---|---|---|---|---|---|---|---|
| Stefan Böhm | 30 | 13 | LB | départ 3 000 (aucune offre) | 125 | **+3 sur A. Bertin (10)**, +4 sur Leroy (9) | Meilleur rapport du jour ; 30 ans, déclin dès 30 [skill entraînement] ; 3 125 pour 1 cycle : **hors portée** |
| Luis Ríos | 30 | 12 | P | départ 2 000 (aucune offre) | 110 | +2 sur Benoit (10), +3 sur Chevalier (9) | Hors portée ; Benoit a 19 ans et progresse |
| Sascha Schmid | **18** | **18** | LB | départ 12 000 (aucune offre) | 165 | **+8 sur A. Bertin** | Cible long terme ; 12 000 + 165 : impossible avant plusieurs semaines (C-044 Fan Shop et Youth Academy 7 passent avant) |
| Rafał Kołodziej | 18 | 17 | P | départ 16 000 (aucune offre) | 150 | +7 sur Benoit | Hors budget |
- RB : aucun gain à portée (Frashëri 10, 30 ans, 2 000 ; Jakab 9, Pereira 9 : pas d'amélioration sur Roger 11). GK : Aubert 12 (34 ans, 1 000, aucune offre) = égal à Bourgeois, +3 sur Blanc qui ne joue pas ; salaire 170 : non.
- Notes visibles de tous sur une annonce [W:Transfers]. Gain exprimé en points de note au poste ; leur effet en buts n'est pas prouvé (L-001). **0 vente conclue en base : aucun prix de référence, confiance faible.** Repères d'offres en cours : Carvalho CB 16 à 15 000 (Bonjwas en tête), Passawe GK 18 ans note 14 à 6 000, Oliveira E. (LW 12) à 4 000.
- Coût de repli : libération 500 € [skill club] ; aucune cible n'est lancée, donc 0.

## Nos joueurs : vendre / garder (`silver.sz_players`)
| Joueur | Âge, note, salaire | Décision |
|---|---|---|
| Denis (CB) | 26, 8, 90 | **Garder** : 3e CB derrière Fournier 17 et Simon 10 ; vendre coûte 500 € de frais impayables |
| G. Bertin (RW) | 25, 9, 90 | Garder (même raison) ; seul surplus vendable, à revoir à la saison suivante |
| Barros (RB) | 30, 10, 110 | Garder (remplaçant RB de Roger) |
| Blanc (GK) | 26, 9, 140 | Garder (seul GK remplaçant) |
| Les 12 autres | — | Garder |
- Minimum d'effectif 7 : sans objet (16 joueurs).

## Il me manque
- Prix finaux d'Oliveira et Kristensen : onglet « Transfer history » non exporté (le donner ferait un vrai prix de référence).
- Solde exact après règlement de J18 : refaire l'export Club demain.

## Conseils
- **C-051** (learnings.md) : aucun achat ni vente avant la saison suivante ; première cible LB type Böhm si solde ≥ 3 000 + réserve. **Faux si** le solde dépasse 4 000 € avant le relevé de la saison suivante (alors Böhm ou équivalent à 3 000 € devient finançable).
- C-035 et C-036 clos ; C-037 reste valable.

## À refaire si
- Export Marché de la saison suivante (nouvelles annonces, salaires revus) avec le solde de l'export Club.

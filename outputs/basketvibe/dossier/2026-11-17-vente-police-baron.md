# Police vente — Nolan Baron — 2026-11-17 (10:12 Paris)

Verdict : police partielle : manque `bronze.discord_messages` (dossier : 0 ligne), relance `kb.py` (compteur du dossier recopié : transferts 31 total / 29 affichées, 2 obsolètes), réécriture de la carte vente.

## Variables
| variable | valeur | source |
|---|---|---|
| Joueur, âge | Nolan Baron, PG, 17 ans, PS 44,9 | dossier C8 |
| Minutes / rôle | 0,0 min sur 4 matchs de ligue ; rang 7 au slot PG | brouillon ; `gold.bv_slot_fit` |
| Remplaçant au slot ➕ | Durand (SF 25 ans) : fit PG 44,1 contre 44,7 pour Baron, écart 0,6 (< tolérance 1,0) ; mais Durand est rang 10 au slot PG, derrière Baron (rang 7), forme 5, fatigue 8,96 | `gold.bv_slot_fit` slot PG |
| Autres slots ➕ | Baron SG 41,2 / SF 36,0 / PF 32,2 / C 24,9 : utile seulement au PG | `gold.bv_slot_fit` |
| Salaire économisé | 16 691 par semaine (brouillon) | roster_bilan |
| Valeur marché | case ≤21 / PS 40 : n 78, p25 64 500, médiane 294 999,5, p75 841 250 ; case PS 45 : p25 525 000, médiane 795 000 | `gold.bv_price_ref_ps` ➕ |
| Fiabilité de la case pour un PG ➕ | faible : ventes réelles (≥1 enchère) de ≤21 ans, PS 40-44,9, depuis le 01/11 : PG n = 1 (76 000, 6 enchères) ; C n = 4 ; SG 2 ; PF 2 ; SF 3. Presque tous les PG 16-19 ans PS 40-45 listés sont à 0 enchère (prix demandés, pas des ventes) | `core.market_listing` ➕ |
| Taxe, délai | 5 % (vendeur reçoit 95 %) ; enchère d'environ 2 jours ; impossible à annuler ; sans enchère il reste au club | skill transferts `01-vendre.md` |
| Effectif minimum | 12 joueurs, 8 disponibles minimum, 9 requis avant l'action ; 0 vente en cours ; 0 blessé | dossier C2, C3 |
| Progression | +0,4 PS en 7 jours (44,5 -> 44,9) : 0,1 sous la case PS 45 (p25 525 000) | dossier C8 |
| Déclin | aucun joueur en déclin | dossier C5 |
| Avis des amis | #144 (0,4, doute) 17 ans à 2-3 M « facile » ; #118 (0,4, conf) taxe 5 % ; #95 revente après 7 jours ; #119 (0,4, doute) prix de fin septembre faussés ; L-016/C-016 (2026-10-18) : garder les jeunes (Bernard, Baron, Leclerc) ; C-075 : revente de petits prix médiane -8 500 | dossier § 2 et learnings |

## Couverture
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| kb transferts | 29 affichées / 31 | 29 | 5 (#144, #118, #95, #119, taxe) | 24 : enchères, agents libres, économie, sans lien avec un PG de 17 ans ; 2 obsolètes |
| Discord brut | 0 | 0 | 0 | aucun export au dossier : manque |
| Skill transferts vendre | 1 | 1 | 1 | — |
| Vues gold (slot_fit, price_ref) + market_listing | 5 requêtes | 5 | 5 | — |
| Learnings (C-016, C-075) | 2 | 2 | 2 | — |

## Conflit
Règle (taxe 5 %, effectif 12 sur 8) : vente permise. Chiffres de la saison : seule vente PG comparable = 76 000, la médiane 294 999 vient de ventes surtout C. Le chiffre de saison l'emporte sur la case.

## Conclusion
1. Ne pas vendre Nolan Baron : aucun gain de match à vendre (0 min) mais le prix de 294 999 n'est pas prouvé pour un PG ; seule vente comparable 76 000 (net 72 200), soit 4,3 semaines de salaire ; il progresse (+0,4 par semaine) vers la case PS 45 (p25 525 000).
2. Prix de mise en vente minimum, si vous vendez malgré tout : 76 000 (seule vente PG prouvée) ; 294 999 risque 0 enchère, donc le joueur reste au club sans perte.
3. Remplaçant : Durand couvre le PG à 0,6 près mais n'est que rang 10 au slot et fatigué (8,96) ; l'écart de 0,6 ne justifie pas la vente.
4. Ce qui prouverait que j'ai tort : 2 ventes PG ≤21 ans PS 40-45 avec enchères à plus de 250 000 net, ou Baron toujours à 0 min avec un PG titulaire blessé.
5. Récidive : brief d'achat/vente rendu avec une case de prix sans compter les ventes par poste ; ajouter la règle « case de prix = n par poste et enchères > 0 ».

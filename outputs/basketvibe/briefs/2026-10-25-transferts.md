# Transferts BasketVibe — 2026-10-25 (Chomelix Cow)

Briefs amont lus : lecteur-exports, entrainement, match, finances (2026-10-25). Marché exporté le 25/10 07:45 UTC (moins de 24 h, 107 enchères, aucune à nous). Vues : `gold.bv_market_candidates`, `gold.bv_slot_fit` (fit_with_form), `gold.bv_sell_candidates`, `gold.bv_roster_now`. Prix de référence : `ref_median_age_pos` (21 jours, compétences inconnues, 19 à 35 comparables, confiance faible). `gold.bv_player_fit` n'existe pas : j'ai utilisé `bv_slot_fit`.

## Actions
| Priorité | Catégorie | Action | Preuve / critère |
|---|---|---|---|
| 🟥 URGENT | Transferts | **Mets Nael Fontaine (PG, 30 ans) en vente maintenant, minimum 10 000** (C-064). Vente ~2 jours, non annulable : mise en vente au plus tard jeu. 29/10 pour être conclue avant la paie du dim. 01/11 02:30 UTC. Produit net attendu 9 500 (taxe 5 %), économie 16 289/sem. | `on_transfer_list` = false aujourd'hui |
| 🟧 IMPORTANT | Transferts | **Mets Min-jun Dang (SG, 29 ans, 20 636/sem.) en vente maintenant, minimum 50 000** (C-053), avant son passage à 30 ans au changement de saison (médiane SG 30+ : 10 000 contre ~300 000 à 26–29 ans). Il ne joue pas à J22 (cinqs du brief Match). Remplaçant au SG : Lefebvre 51,5 contre Dang 51,9 (fit avec forme), perte 0,4 point. Économie 165 000 sur 8 semaines. Garde 15 disponibles (minimum 8) | `on_transfer_list` = false ; confiance moyenne, le prix de 50 000 peut ne pas être atteint, alors il reste au club sans coût |
| 🟩 SUIVI | Export | Mar. 27/10 : réexporter le marché (nouveaux libres, prix de S2) | marché > 24 h |

## 1. Cibles (règle 20)
Poste faible : le **rebond** (déficit structurel, brief Match, L-001) et le **C remplaçant** (C : Lefebvre 63,0 puis Fournier 52,9 ; fit avec forme 58,0 puis 50,2 : trou de 7,8 points). Rebond des grands : Lefebvre 73,9, Bernard 63,2, Fournier 61,6, Albano 51,6, Klein 36,1.

| Cible | Poste, âge, taille | Rebond / Déf | Gain de fit vs notre 2e du poste | Prix actuel (médiane, n) | Salaire/sem. | Fin (Paris) | Verdict |
|---|---|---|---|---|---|---|---|
| Filippo Barone | PF, 28, 206 | 58 / 80 | +4,1 au C (57,0 contre 52,9) | 700 000 (127 300, 35), 0 enchère | 25 500 | lun. 26/10 17:13 | cher : 5,5 × la médiane |
| Yong Kobayashi | C, 28, 213 | 62 / 59 | +2,1 (55,0) | 800 000 (500 000, 29), 0 enchère | 25 800 | lun. 26/10 17:31 | cher |
| Piotr Dąbrowski | C, 27, 213 | 76 / 51 | +0,1 (53,0) | 400 000 (500 000, 29), 1 enchère | 23 300 | lun. 26/10 19:59 | au prix, mais gain de fit nul |
| Latif Al-Qudah | SF, 27, 194 | — | +5,3 au SG (61,3 contre Lefebvre 56,0) | 860 000 (390 000, 23), 8 enchères | 31 000 | dim. 25/10 21:06 | hors budget |
| Issam Mansour | PF, 28, 204 | 58 / 77 | +2,6 au PF | 560 000 (127 300, 35), 6 enchères | 30 800 | dim. 25/10 21:10 | hors budget |
| Arnas Jonaitis | PF, 28, 205 | 69 / 42 | négatif (PS 47,1, 7e du PF) | 5 000 | 19 110 | dim. 25/10 18:27 | rebond seul, ne joue pas |

**Coût de repli** : libération sans indemnité [M§11.1], mais le prix payé est perdu. Coût réel d'un achat : prix + salaire × 8 semaines (Barone 700 000 + 204 000 = 904 000, soit 220 000 par point de fit gagné ; 1 point de fit ne se convertit pas en victoires de façon connue).

## 2. Décision : aucun achat aujourd'hui
Raison chiffrée : le plafond d'enchères est de **96 000** (146 000 avec la prime de rang 5–8) pour une réserve de 986 000 (brief Finances §5). Les 6 cibles qui apportent ≥ 2 points de fit coûtent 560 000 à 860 000, soit 4 à 9 fois le plafond ; les achats sous 150 000 ont un gain de fit négatif (Roldán C 30 ans −1,6, MacLean SG −3,5, Pluta C 219 cm 22 ans, 100 000, PS 42,8, −10,4). Un achat de 700 000 laisserait ~120 000 de solde avant 393 000 de charges hebdomadaires (salaires 333 000 + personnel 60 000), avant la première recette de S2 le 02/11. Je ne le recommande pas.
Aucune enchère à nous, aucune vente ouverte à suivre : l'annonce du 22/10 est invendue (lecteur-exports, point 6) ; Fontaine et Dang ne sont pas encore en vente.

## 3. Règle d'achat pour la suite (C-066, remplace le choix de C-055)
Au prochain export (mar. 27/10) : si un joueur libre (départ 10 000) ou à ≤ 80 000 est C/PF, ≥ 205 cm, Rebond ≥ 60 et PS ≥ 50, enchère maximale **80 000** (somme des maximales ≤ 96 000 [M§10.3]). Aujourd'hui aucun libre n'y répond (libres : Lehtinen SF Rebond 37, Féliz PG, Reyes SG, Dridi SG). Salaire à prévoir : ~20–23 000/sem. Sortie de l'achat si déçu : libération, 0 indemnité.
Les ventes de Fontaine (+9 500) et Dang (jusqu'à +47 500) relèvent le plafond d'autant et économisent 36 925/sem.

## 4. Ce qui prouverait que j'avais tort
- Dang vendu au-dessus de 50 000 ou Barone / Kobayashi invendus lun. 26/10 (prix final < 400 000 dans `silver.bv_transfers`) : le marché est moins cher que prévu, réévaluer au prochain export.
- Test : indice rebond des unités à J23 (02/11) ; si on perd le rebond de plus de 10 points sans recrue C/PF, l'absence d'achat a coûté.
- Dang : si Lefebvre est blessé avant le 02/11 et que le SG tombe à 49,9, la vente a coûté 2 points de fit sur un poste de banc.

## Données manquantes
| Il me manque | On le réunit ainsi |
|---|---|
| Prix finaux des enchères Barone, Kobayashi, Dąbrowski (lun. 26/10) | Export du marché / historique global mar. 27/10 |
| Salaire de fin de saison après recalcul | Effectif, onglet Tiles, export mar. 27/10 |

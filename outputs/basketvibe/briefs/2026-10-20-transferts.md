# Brief Transferts — Chomelix Cow's — 2026-10-20 (soir)

Export du marché, de l'historique du club et de l'historique global : **2026-10-20 18:08 UTC** (`bronze.raw_pages`), moins de 24 h, donc à jour. Prochain export du marché utile : jeudi 22/10 au soir si vous voulez suivre Ho ou les libres du jour de match.

## Actions à faire ce soir
1. **Aucune enchère** sur le marché du jour (voir 1). Rien à saisir, rien à bloquer.
2. **Remettre Nael Fontaine en vente** (PG, 30 ans, PS 43,6, salaire 16 289) : prix de départ **5 000**. Fin vers le 22/10 au soir : il part avant la paie du dimanche 25/10 [M§11.1, M§10.2]. Il vous reste 17 joueurs disponibles (9 requis) (C-029).
3. **Ne rien vendre d'autre avant le 26/10** : Henry et Klein jouent l'unité B jusqu'à J22 (C-016 maintenu).
4. Contrôle (C-028) : aucun achat jusqu'au 26/10.

## 1. Marché du jour (E13)

### Faits
- Solde **878 555**, projection fin de saison (26/10) **982 670** sans transfert, 1 paie restante, charges 490 996 par semaine, résultat hebdomadaire estimé **+73 434** (`gold.bv_finance_projection`, `gold.bv_finance_health`). Maximums en cours : 0.
- Marché : 94 joueurs, dont 4 libres et 42 qui entrent dans notre top 8 (`gold.bv_market_candidates`).
- **Ventes connues de 23–30 ans à PS ≥ 52,7 : 10, toutes à 500 005 ou plus** (de 500 005 à 1 800 000), y compris des départs à 10 000 qui finissent à 560 000 (Abbott, PG 26 ans, PS 52,7) (`gold.bv_market_price_known`). Sous PS 50,2 : de 10 250 à 260 000 (5 ventes).
- Références par âge et poste (`gold.bv_market_price_ref`, 21 jours, compétences inconnues, très dispersées) : médiane 22–25 ans C 640 000 (n = 31), PG 276 000 (n = 41), 26–29 ans SG 295 000 (n = 37) ; 30 ans et plus : de 175 à 34 000.
- Nos achats récents (`silver.bv_transfers`) : Dang 10 250 (libre, 19/10), Albano 26 000 (19/10). Al-Anazi perdu à 120 000 (maximum 110 000), Daniels vendu 51 000 ailleurs.

### Les cinq plus intéressants (gain de fit contre nos titulaires de l'unité B, `gold.bv_market_candidates`, `gold.bv_slot_fit`)
| Joueur | Poste, âge | PS / salaire est. | Unité B qu'il améliore | Prix actuel (offres) | Fin (Paris) | Prix probable |
|---|---|---|---|---|---|---|
| Russell Owens | C, 25 | 56,5 / 26 900 | C : 56,5 contre Bernard 44,4 / Klein 44,9 | 66 000 (9) | mer. 21/10 11:57 | **cher** : Volkov C 55 = 1 600 000, Baldonado C 53,4 = 960 000 |
| Ji-ho Bui | PG, 25 | 57,2 / 26 000 | PG : 57,1 contre Boyer 47,8 | 1 260 (3) | mer. 21/10 08:28 | **cher** : PG 57–59 vendus 1 010 000 à 1 500 000 (n = 3) |
| Edwin Fleming | SG, 28 | 53,6 / 22 000 | SG : 53,7 contre Henry 42,0 (Dang 50,4) | 14 500 (4) | mer. 21/10 11:58 | **cher** : SG 55,4 = 1 100 000 ; SF 53,1 = 500 005 |
| Marcello Carbone | SF, 27 | 57,5 / 26 500 | SF : 57,4 | 1 501 (3) | mer. 21/10 14:33 | **cher** (PS 57+) |
| Gavin Ho (libre) | SF, 28 | 51,2 / 20 580 | SF : 51,2 contre Dang 49,3 : +1,9 seulement | 10 000 (1) | jeu. 22/10 04:23 | correct (libres PS ≤ 50 : 10 250 à 120 000) mais gain faible |

Lecture : les prix actuels sont des débuts d'enchère, pas des prix finaux. Les enchères à départ bas mais très suivies finissent haut (Abbott, Al-Anazi 120 000).

### Argent
- Règle [M§10.3] : somme des maximums ≤ solde (878 555) : non limitante.
- Plancher de réserve du brief Finances (C-020, ouvert, c'est un conseil, pas une règle du jeu) : solde ≥ 925 000 après le 26/10. Marge = 982 670 − 925 000 = **57 670**, à partager entre le prix et le salaire du 25/10 de chaque recrue (déjà incluse : Dang et Albano). Un achat à 500 000 ou plus la dépasse de loin.
- Coût total d'un Owens à 1 000 000 : 1 000 000 + 26 900 × (1 paie restante en S1 + ~8 en S2, hypothèse de 8 versements par saison d'après la skill économie) ≈ 1,24 M pour passer l'unité B de 44,4 à 56,5 au C. Hors de portée du solde.

### Avis (confiance moyenne sur « ne pas acheter », 10 ventes comparables mais compétences inconnues pour la plupart)
- **Ne pas enchérir.** Les titulaires ciblés par le brief du 18/10 sont achetés ou perdus ; Dang (SG/SF/PG fit 48–50) et Albano (C 47,1) comblent l'unité B ; ce qui reste d'utile coûte 500 000 à 1,5 M.
- Il reste 3 matchs de ligue (J20 à J22) : un achat ne joue que 24 min par match avant la saison 2.
- **Enchère maximale conseillée : 0.** Si vous voulez un billet de loterie : Fleming, maximum **35 000** (marge 57 670 − salaire du 25/10 22 000 ≈ 35 670). Confiance très faible d'en gagner un : 0 vente connue à PS ≥ 52,7 sous 500 005. Mécanisme : maximum automatique, anti-snipe 3 min, phase finale à l'aveugle, prix final = de quoi battre le 2e maximum [M§11.3].
- Pour la saison 2 : le marché est cher aujourd'hui et chaque libre (3 par jour de match, départ 10 000 [M§11.4]) mérite un coup d'œil le jeudi, mais je n'ai pas de signal de bonne affaire ce soir.

## 2. Joueurs à vendre (E14)

Source : `gold.bv_sell_candidates`, `gold.bv_market_price_known`, `gold.bv_market_price_ref`. 17 joueurs disponibles [M§11.1].

| Joueur | Âge, PS, salaire | Verdict | Raison et moment |
|---|---|---|---|
| Nael Fontaine (PG) | 30, 43,6, 16 289 | **Vendre maintenant** | Plus de progression à 30 ans, déclin dès la saison prochaine [M§8.5]. 6 min de ligue sur les 4 derniers matchs. Comparables 30 ans et plus (3 ventes connues) : 5 000 à 30 000 ; référence PG 30+ : médiane 16 000 (n = 14). Produit net ≈ 5 000 à 30 000 × 0,95, mais surtout 16 289 de salaire par semaine en moins. Fin vers le 22/10, avant la paie du 25/10. Dang et Boyer couvrent le PG au depth chart. |
| Soan Henry (SG) | 26, 42,0, 15 839 | Vendre **après J22** (26/10) | Joue l'unité B jusqu'à J22 ; 10e au SG en fit. Prix attendu faible (26–29 ans SG : p25 10 000, médiane 295 000, dispersée). |
| Elias Klein (C) | 28, 44,8, 16 380 | Vendre **après J22** | Déclin récent (`trend_s3`), remplaçable par Albano. Même raisonnement. |
| Min-jun Dang (SG) | 29, 49,9, salaire non affiché | **Garder** | Acheté 10 250 il y a un jour, 29 ans = dernière saison de progression [M§8.5], il couvre PG, SG et SF. |
| Léo Lefebvre (PF/C) | 28, 62,9, 31 803 | **Garder** | N° 1 de l'effectif (rang 1 au C). À titre indicatif seulement : un SF de 28 ans à PS 63 a été vendu 1 800 000 (1 vente, confiance très faible). Vendre un titulaire avant J22 mettrait le maintien en jeu. À réévaluer après J22 si vous visez un gros achat en saison 2. |
| Gimenez, Richard, Bonnet, Fournier, Legrand, Durand | 22–27 ans | **Garder** | Dans la rotation, salaire par point de PS de 370 à 506, progression possible. |
| Bernard (17), Baron, Leclerc, Lecomte (16) | juniors | **Garder** | Potentiel inconnu mais jeunes, bonus homegrown pour Bernard (C-021) ; leur prix est nul à la vente tant que la progression n'a pas été mesurée. |
| Boyer (19), Albano (26) | | **Garder** | Rotation et plan B. |

- Contraintes : une semaine au club avant revente pour Dang et Albano (achetés le 19/10) [M§11.1] ; vente de 2 jours, non annulable, taxe de 5 % ; 9 joueurs disponibles minimum avant l'action.
- Fin de saison : salaires recalculés et âges +1 an (skill saison) : vendre Henry et Klein juste après J22 évite de payer leurs salaires recalculés.

## 3. À refaire si
- Un blessé dans l'unité A ou B avant dimanche (nouveau besoin à l'intérieur ou au PG).
- Un export du marché plus récent montre un joueur de PS ≥ 52 à moins de 100 000 à 3 h de sa fin.
- L'historique global du jeudi montre des prix de PS 52+ sous 300 000.

## Conseils ajoutés au journal
C-028 (aucun achat, plafond de dépense) et C-029 (Fontaine en vente). Statuts mis à jour : C-012, C-013, C-014, C-015.

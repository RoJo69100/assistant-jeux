# Team Soccer — Transferts, brief du 2026-10-20 (soir, remplace celui du 2026-10-19)

Données : annonces et effectifs relevés le 2026-10-20 20:00-20:03 UTC (`silver.ts_transfer_listings`, `silver.ts_players` day 2026-10-20), finances du 2026-10-20 (`gold.ts_finance_status`, `silver.ts_finances`). Heures en Paris (UTC+2, jusqu'au 25/10). Deux économies séparées [fiche commune].

## En tête : actions

| # | Club | Action | Quand |
|---|---|---|---|
| 1 | Les deux | Soldes positifs : achat possible (Chomelix 1 062 583 $, Ben Ahmed 87 521 $). **Un seul achat cette semaine** tant que la portée de la limite n'est pas vérifiée (voir Règles). | — |
| 2 | Chomelix Cows | **Option** : enchérir sur **Tommaso Barbieri** (MID 22 ans, OVR 63, annonce 5288), **enchère maximale 534 534 $**. À faire seulement si le 1-4-4-2 avec 4 milieux est gardé (règle C-032). | ce soir ou demain soir |
| 3 | Ben Ahmed Donkey | **Pas d'achat** ce soir : 87 521 $ ne couvrent pas 534 534 $. Vendre Hayashi + Ibe **uniquement** si on veut Barbieri pour ce club (voir plus bas). | — |
| 4 | Les deux | Ouvrir « Your offers » du Marché et vérifier qu'aucune enchère en tête n'est déjà comptée cette semaine. | avant d'enchérir |

**Date limite utile : Barbieri, fin le jeudi 22/10 à 16:21** (deadline 2026-10-22 14:21 UTC), donc agir au plus tard le soir du 21/10 ; je ne peux pas dire si l'on peut enchérir à l'avance avec un plafond (rien dans les skills).

## Faits (SQL)

- **Soldes** [`gold.ts_finance_status`, as_of 2026-10-20] : Chomelix **1 062 583 $** (masse salariale 161 871 $, fin de saison projetée 1 775 546 $) ; Ben Ahmed **87 521 $** (masse salariale 95 596 $, projection 613 081 $). Les deux `alert_negative` = faux.
- **Lefebvre vendu** [`silver.ts_finances` team 18, day 2026-10-20] : `player_sales_income` **838 166 $** (= sa valeur, vente à la banque) et `match_income` 409 700 $ (match du 20/10) ; 838 166 + 409 700 = +1 247 866 $, soit exactement l'écart avec la veille (−185 283 → 1 062 583). Lefebvre n'est plus dans `silver.ts_players` (22 joueurs, masse salariale 170 253 → 161 871 $, −8 382 $).
- La banque l'a remis en vente à 838 166 $ (annonce 5301, vendeur « Chomelix Cows », 0 offre, fin 22/10 22:56). Ne pas le racheter. Les totaux cumulés (`total_player_sales` 1 618 340 $) ne sont pas encore mis à jour.
- **Ben Ahmed** : `player_sales_income` **200 003 $** le 20/10 (+200 003 $ de solde) sans annonce correspondante dans mes données. Probablement la vente de Colette Rossi (C-013/C-026) ; non vérifié. Effectif 22, masse salariale inchangée (95 596 $), Hayashi toujours là.
- **Effectifs** : 22 joueurs chacun (limite 24, enchères comprises). Milieux : Chomelix 7, Ben Ahmed 4.
- **Marché** : 52 annonces ouvertes au relevé (dont 3 manager). Barbieri : 0 offre, prix = valeur. De Bruyne (MID 20 ans, OVR 74) : prix demandé passé de 2 034 483 à **2 978 686 $** avec 11 offres (valeur 1 044 012 $) en 24 h.
- **Ventes comparables closes : 0** (les annonces terminées ne restent pas dans `silver.ts_transfer_listings`). Mes enchères maximales reposent sur la valeur de la fiche, pas sur un prix de clôture. Seul indice : une annonce très convoitée monte de 46 % en 24 h (De Bruyne), une annonce banale à 0 offre reste à la valeur.
- `silver.ts_my_bids` : toujours les 7 mêmes annonces anciennes de Chomelix (ids 391-872), aucune dans le relevé du jour, aucune pour Ben Ahmed. Elles semblent sans effet (aucune enchère en tête visible), à confirmer dans « Your offers ».

## Règles utilisées

- Vente banque : immédiate, au prix de la fiche, sans commission. Enchère du manager : 72 h, départ ≤ valeur, vendeur reçoit 90 % [skill club : Marché] [F:2026-10-18 Admin-Dev].
- Achat : 1 par semaine, enchères en tête comptées, remise à zéro le lundi 00:00 (heure des Canaries), soit le **26/10** ; solde négatif = pas d'achat ; effectif 16-24 enchères comprises ; revente interdite 7 semaines [G:Limites hebdomadaires de transferts] [skill club].
- **Portée de la limite : le skill parle d'un « compte » (30 jours ou moins = illimité), il ne dit pas si les deux clubs ont chacun leur quota.** Je suppose donc un seul achat pour le compte cette semaine. À tester : si l'enchère sur un club ne bloque pas l'autre, les deux sont possibles.
- Nouveau joueur : Forme 85 au départ ; salaire ≈ 1 % de la valeur par semaine [skill joueurs].
- Un solde bas coûte des points de moral [skill club : Finances].
- Hors skills, donc non évalué : si un joueur masculin peut rejoindre l'équipe féminine (Ben Ahmed) ; si une enchère en tête immobilise le solde.

## Achat (avis)

### Chomelix — milieu, Tommaso Barbieri (annonce 5288, banque)
- Fiche : MID 22 ans, OVR 63, Contrôle 75, Conduite 69, Défense 62, Endurance 72, Vitesse 72, valeur et prix 534 534 $, 0 offre.
- **Intérêt : modéré.** Il serait le 4e milieu : aujourd'hui Adrien Thomas (OVR 44, Conduite 77) ou Jules Leroy (OVR 48,9, Conduite 86) derrière Adrien Roux 67, Lucas David 67 et Robert 65 (`silver.ts_players`). Gain d'OVR de +14 à +19 sur ce poste, mais sa Conduite (69, compétence principale du milieu [skill joueurs]) est inférieure à celle des deux jeunes ; l'OVR vient de ses autres compétences. Il ne sert que si le 1-4-4-2 est gardé (le 1-4-3-3 de C-001 n'utilise que 3 milieux) ; le résultat du match du 20/10 n'est pas encore dans `gold.ts_match_report`.
- **Prix : correct.** À OVR 63-65 les milieux de Chomelix valent 870 400 à 1 119 455 $, donc 534 534 $ est plus bas, mais ils ont Conduite 100.
- **Enchère maximale : 534 534 $ (valeur, sans prime).** Base : prix de la fiche, 0 vente comparable. **Confiance faible.** Au-delà de la valeur, un achat à OVR 63 n'est plus rentable.
- **Coût total** : 534 534 $ + salaire ≈ 5 345 $/sem × 7 sem ≈ 37 400 $ (jusqu'à la fin de saison, durée approximative) ≈ **571 900 $**. Solde après achat : 528 049 $ (au-dessus de la réserve de 2 semaines, 381 582 $, calculée comme dans C-025). Masse salariale 161 871 → 167 216 $ (+3,3 %). Effectif 23/24. Revente interdite 7 semaines. Le solde reste utilisable pour le reste : pas d'entraîneur ni de stade avant la clôture du 02/11 (C-009).
- Autres milieux au marché : De Bruyne (OVR 74) hors budget et hors de prix ; Sallai (17 ans, OVR 53, Conduite 76, 488 743 $) moins bon que Barbieri ; Carbone (18 ans, OVR 50, 583 100 $) cher pour OVR 50.
- Rien d'autre : défense (García DEF 66, 838 166 $) n'améliore pas les titulaires (Ounahi 90, Simon 68, Thomas 66, Dubois 65) ; attaque complète (Moreau 70, Bonnet 67, David 65, É. Roux 62,7) ; gardien Romain Thomas à 100 (le meilleur gardien du marché, Świderski GK 92, OVR 65, 870 400 $, n'apporte rien).

### Ben Ahmed — milieu (suite de C-006)
- Même annonce 5288 : MID 22 ans, OVR 63, Conduite 69 contre Kumar 63 (24 ans, 385 868 $) : gain d'OVR nul, mais Barbieri serait **un vrai milieu dans son rôle naturel**, ce qui compte pour les notes (4,9 à 5,4 aujourd'hui avec des GK/ailiers placés au milieu, L-007). Aucune annonce au marché ne répond à C-006 (Conduite ≥ 70 et OVR ≥ 64).
- **Intérêt : modéré, plus incertain qu'à Chomelix** (gender non vérifié, voir Règles). Prix correct pour la valeur, mais le solde (87 521 $) l'interdit.
- Pour financer : vendre **Kavya Hayashi** (DEF 28 ans, OVR 62, +488 743 $) **et Suki Ibe** (DEF 28 ans, OVR 61,5, +488 743 $), banque, immédiat. Solde 87 521 + 977 486 = 1 065 007 $ ; après Barbieri 530 473 $ (au-dessus de la réserve ≈ 230 000 $, C-010). Hayashi seule laisserait 41 730 $ : trop juste, la projection de la clôture du 02/11 est basse (voir C-010).
- Défense après ventes : Fernández 64, Fournier 63, Taylor 63, Girard 62 titulaires + 2 jeunes de 14 ans (Williams, Yamamoto H.) ; plus de défenseur confirmé au banc. Effectif 22 − 2 + 1 = 21 (min 16).
- **Enchère maximale : 534 534 $ (valeur), confiance faible, 0 comparable.** Coût total ≈ 534 534 + 5 345 × 7 ≈ **571 900 $**, moins 977 486 $ de ventes ; masse salariale 95 596 → 91 167 $ (−4,6 %).
- **Mon avis : si un seul achat est permis cette semaine, le prendre à Chomelix** (pas de vente préalable, pas d'inconnue de genre, écart d'OVR plus grand). Pour Ben Ahmed, attendre la clarification de la limite et de la question du genre, puis décider avant le 22/10 ou viser une prochaine annonce (après le 26/10).

## Vente (avis)

Règle de calcul : la banque paie 100 % de la valeur tout de suite ; l'enchère manager rapporte 90 % du prix final et ne bat la banque que si le prix final dépasse 111 % de la valeur. 0 vente manager comparable observée : **banque** pour les joueurs à vendre.

| Club | Joueur | Âge / OVR | Valeur | Salaire/sem | Gain net (banque) | Effet masse salariale | Décision |
|---|---|---|---|---|---|---|---|
| Chomelix | Louis Lefebvre | 28 / 58 | 838 166 $ | 8 382 $ | **déjà encaissé** | 170 253 → 161 871 $ | Fait |
| Ben Ahmed | Kavya Hayashi (DEF) | 28 / 62 | 488 743 $ | 4 887 $ | +488 743 $ | −4 887 $ | Vendre **seulement** pour financer Barbieri ; sinon garder |
| Ben Ahmed | Suki Ibe (DEF) | 28 / 61,5 | 488 743 $ | 4 887 $ | +488 743 $ | −4 887 $ | Idem (les deux ensemble) |

- **Chomelix : aucune autre vente.** Pierre Leroy (32 ans) reste le DEF de remplacement nommé (C-003). Les quatre gardiens (Romain Thomas 60, puis trois jeunes de 14 à 17 ans) pourraient en libérer un, mais leur progression n'est pas évaluée ici (skill entraînement non listé) : garder.
- **Ben Ahmed : pas de vente sans achat.** Solde positif (87 521 $), projection fin de saison 613 081 $ [`gold.ts_finance_status`]. Déduction (avis, confiance faible) : la rechute prévue à −76 742 $ au 02/11 dans C-010 devient environ **+123 000 $** avec la vente de 200 003 $ du 20/10. À revérifier à l'export du 03/11.- Bon moment : maintenant, la banque paie tout de suite ; mais la valeur ne change qu'au plus tous les 7 jours, aucune raison d'attendre. Pas de contrainte de revente (les 7 semaines ne visent que les joueurs achetés).
- Non conseillé : vendre les jeunes de 14-16 ans (progression non évaluée).

## À refaire si
- Le résultat du 1-4-3-3 du 20/10 (C-001/C-032) ramène Chomelix à 3 milieux : Barbieri n'a plus d'intérêt pour ce club.
- « Your offers » montre une enchère en tête déjà comptée cette semaine (annule l'achat).
- La Conduite ou l'OVR de Barbieri change au prochain relevé (valeur révisée au plus tous les 7 jours).

## Limites de ce brief
- Un seul jour de relevé utile : aucun prix de clôture observé (0 comparable) ; enchères maximales à confiance faible.
- Je n'ai pas la règle exacte de portée de la limite (compte ou club), ni celle du genre entre équipe féminine et joueurs du marché. Export utile : page Marché, onglet « Your offers », capture de la mention de limite hebdomadaire.
- Les cumuls de `silver.ts_finances` (`total_player_sales`) ne sont pas encore à jour pour le 20/10 ; les chiffres de vente viennent de `player_sales_income`.

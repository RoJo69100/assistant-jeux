# Transferts BasketVibe — 2026-10-26 soir (agent Transferts, medium + Sonnet)

Briefs amont lus : finances (v2), effectif, match. Marché lu : export du 26/10 20:42 UTC (21:42 Paris), moins d'1 h : valeurs fermes. Heures : `ends_at` (UTC) + 1 h = Paris (UTC+1 depuis le 25/10) ; la vue `gold.bv_market_candidates` convertit bien (Europe/Paris) : MacLean finit mardi **07:14** Paris (06:14 UTC), pas 08:14.

## Actions (plafond 351 000, somme des maximums = 325 000, reste 26 000)
| Priorité | Joueur | Poste | Âge | Action | Enchère max | Heure limite (Paris) | Gain chiffré |
|---|---|---|---|---|---|---|---|
| 🟥 URGENT | Lassi Lehtinen | SF | 30 (31 cette nuit) | Enchère maximale ce soir (libre, prix 10 250, 2 enchères) | **40 000** | mar. 27/10 04:25 | +8,3 PS en SF n°2 (51,5 contre Durand 43,2) ; TS 53,6 → 54,08 (+0,48) ; salaire 21 100/sem. |
| 🟥 URGENT | Grzegorz Marciniak | SF/PF | 25 (26 cette nuit) | Enchère maximale, **sans test avant** (prix 1 027, 2 enchères) | **285 000** | **mer. 28/10 20:18** (hors fenêtre mardi : l'enchère se pose tôt, rien d'autre à faire mardi) | PF n°2 54,9 contre Legrand 48,8 : +6,1 PS ; TS +0,83 seul, +0,69 après Lehtinen ; salaire 23 500/sem. |
| 🟧 IMPORTANT | Loris Lecomte | SF | 16 | Mise en vente à **105 000** mardi après l'amical (08:00) | — (départ 105 000) | mar. 27/10 ~09:00 (mise en vente) ; vente close ~jeu. 29/10 | net 100 000 (taxe 5 %) ; −11 846/sem. de salaire |
| 🟩 SUIVI | Benjamin MacLean | SG | 30 | **Ne pas enchérir** | — | mar. 27/10 07:14 | voir § 3 : −90 000 de perte probable pour +0,46 TS |

## 1. Lehtinen : confirmé, avec une correction d'âge
- Faits (`gold.bv_market_candidates`, `bv_slot_fit`) : SF PS 51,5, libre, 10 250, 2 enchères, fin 03:25 UTC = 04:25 Paris. Rotation SF : Gimenez 59,7, Durand 43,2. TS : 8e meilleur PS 47,7 (Boyer), donc entrée dans le top 8 : (51,5 − 47,7)/8 = +0,475.
- Correction : il aura **31 ans à son arrivée** (+1 an dans la nuit). Déclin dès 31 ans : ~1 point de moyenne par saison, soit ~0,02 PS/sem. [skill entrainement, M§8.5] : négligeable ce soir, mais plus aucune progression.
- Prix : libres de PS 50-51 vendus : Dang 10 250 (nous), Straume 11 250, François 280 000, Ho 390 000 (5 libres au total 16-26/10 ; confiance faible, dispersion). SF 30+ vendus (n=8, médiane 126, p75 40 250 ; PS ~48-51 : Salkić 71 000, Halili 100 000, Caballero 30 000). 40 000 = p75 : confirmé.
- Coût total : prix 10 250 à 40 000 + 21 100/sem. (inclus dans la réserve du brief Finances).
- **Plan de revente** : une semaine au club avant revente [M§11.1] donc dès mer. 04/11 ; mise à 50 000 (net 47 500) ; comparables 30 000 à 100 000 ; si invendu, libération sans indemnité [skill transferts] : on économise 21 100/sem. Perte maximale réaliste : 40 000 + 21 100 × 2 sem. − 47 500 ≈ 35 000.
- Preuve du contraire : Durand au-dessus de 48 d'ici 2 semaines, ou Lehtinen < 3 pts/16 min en 3 matchs.

## 2. Marciniak : prix confirmé, test supprimé avant l'achat
- Faits : SF 200 cm, 25 ans, PS 54,3, meilleur emplacement PF 54,9 (2 pts 80, défense 82, 3 pts 32, rebond 47). Relisté à 1 027 (2 enchères) après un échec à 1 500 000 sans enchère le 26/10 (19:00 UTC).
- Comparables PS 53-55, SF/PF 24-28 ans (`bv_market_price_known`) : Gallo 775 000, Al-Saud 500 000, Eom 560 000, Guillot 500 005, Coleman 660 000, Choi 950 000, Brambilla (PF 28) 127 300. Référence 22-25 ans SF : p25 7 875, médiane 340 000 (n=19). Les 285 000 sont sous 6 des 7 comparables : **probabilité de gagner faible (estimation 10 à 20 %)**, gain très net si oui.
- Correction : le test de potentiel (25 000) n'est pas payé avant. Le plafond de 285 000 est une limite de liquidité qui ne dépend pas du potentiel : le résultat du test ne peut pas changer l'enchère. Test seulement après victoire (résultat conservé sur le profil [skill transferts]). Économie attendue : 25 000 × 85 % ≈ 21 000.
- Montant : 285 000 conservé (325 000 avec Lehtinen ≤ 351 000). Lehtinen est réglé mardi 04:25, donc le plafond de mercredi est 351 000 − prix réel de Lehtinen : tu peux monter à 311 000 mercredi si Lehtinen est perdu ou acheté sous 40 000 ; décision : **285 000, pas plus** (au-dessus, la revente à 475 000 net ne laisse plus de marge après 7 jours de salaire).
- **Plan de revente** : revendable dès mer. 04/11 (une semaine) ; mise à 500 000 (p25 22-25 ans PS 50-55), net 475 000 ; achat max 285 000 + 7 jours de salaire 23 500 = 308 500 : marge ≥ +166 000. Si on garde : PF n°2 à 54,9.
- Preuve du contraire : prix final > 285 000 (jamais dépassé, enchère max automatique) ; revente < 300 000 après 2 semaines de mise en vente.

## 3. Autres cibles sous le prix de référence, jusqu'à mardi soir (prix ≤ 351 000, `best_fit` ≥ 47)
| Joueur | Poste / âge / PS | Prix de départ | Fin (Paris) | Verdict |
|---|---|---|---|---|
| MacLean | SG 30, 52,5 | 100 000, 0 enchère | mar. 07:14 | **Non** : comparables SG 30+ n=8, médiane 10 625, p75 29 162 (Erceg 49,2 à 1 000 le 24/10, Dang 49,9 à 10 250 le 19/10). Départ à 3,4 x le p75 ; il passe 31 ans cette nuit. Gain : SG n°1 52,5 contre Bonnet 51,4 (+1,1) et Dang 49,9 (+2,6) ; TS +0,46 après Lehtinen. Coût 100 000 + 22 600/sem., revente ~10 000 : perte probable ≈ 90 000 + salaire. Aucun prix d'enchère ne devient raisonnable : il n'y a pas d'enchère inférieure au départ. |
| Brandt | C 29, 49,1 (fit PF 49,1) | 125 000 | mar. 00:00 | Non : 125 000 pour +0,3 PS sur Albano (47,5 → 49,1 en PF3), médiane des C 26-29 ans 10 250 |
| Panenko | C 30, 47,9 | 1 000 | mar. 01:13 | Non : +3,1 PS contre Klein (44,8) au C n°2, TS +0,02, salaire 20 230/sem., revente p25 8 750 : perte ≥ 12 000 par semaine |
| Hossain | PF 26, 49,9 | 600 000 | mar. 23:38 | Non : au-dessus du plafond (351 000) et de la médiane PF 26-29 (150 000) |
| Riva (PG 22, 47,6), Piotrowski (SF 22, 46,5), Latić (PG 28, 47,5) | | 23 à 30 000 | mar. | Non : n'améliorent aucun poste (Boyer 47,7, Albano 47,5), 17 600 à 18 400 de salaire |
Leviers (règle 5) : 2 achats nommés ci-dessus. Plafond restant après eux : 26 000 ; aucun autre candidat ne passe le test « entre dans la rotation et coûte moins que sa valeur de revente ». Charalambidis (SG 57,5, 1 000 000, fin mar. 03:31) et Sala (C 58,7, 1 300 000) : hors plafond, inchangé.

## 4. Ventes et enchères ouvertes
- Base (`silver.bv_transfer_auctions`, `bv_transfers`, `gold.bv_sell_candidates`) : **aucune vente en cours, aucun joueur en vente** (`on_transfer_list` faux pour les 17 de `bv_roster_now`). Dernière enchère à nous : Fontaine (vendeur Chomelix Cow), terminée le 22/10 sans vente à 10 000. Derniers achats : Albano 26 000 et Dang 10 250 le 19/10. Aucune enchère posée par nous n'est visible dans l'export (le marché n'indique pas le meneur) : je ne peux pas dire si une enchère maximale est déjà posée ; les 2 enchères sur Lehtinen et Marciniak ne sont pas identifiées.
- Écart à régler : `bv_roster_now` liste encore Nael Fontaine (PG 30, PS 43,6) alors que le brief Effectif le dit renvoyé ; l'export roster est donc antérieur au renvoi ou le renvoi n'a pas eu lieu. À vérifier au prochain export (sans conséquence sur ce plan).

## 5. Lecomte : 105 000 confirmé
- Faits : SF 16 ans, PS 37,9, 0 min en ligue sur 4 matchs, salaire 11 846/sem. Référence `bv_market_price_ref` SF 16-17 ans : p25 **105 000**, médiane 265 000, p75 1 391 250 (n=19). Le brief Effectif disait 199 000 (ancienne valeur) ; la valeur actuelle est 105 000.
- Comparables SF 16 ans PS 37-38 : Horn 199 000 (départ = prix), Allende 350 000 (départ = prix), Teo (PS 35,8) 25 000. Sur 15 ventes de 16-17 ans PS < 42 hors libres : 9 au prix de départ, médiane 261 000, p25 73 500. Biais : seules les ventes conclues sont connues.
- Décision : **105 000**, pas 199 000. Raison : une vente n'est certaine qu'avec un départ bas, l'argent est nécessaire avant le 01/11, et les enchères montent au-dessus du départ quand le joueur plaît (Chojnacki 1 → 77 000, Alcántara 1 → 261 000). Net minimal 99 750 (taxe 5 %). Le plafond monte de ~100 000 à la réception.
- Contraintes : 15 joueurs restants (minimum 8 disponibles), SF = Gimenez, Durand, + Lehtinen/Marciniak à venir. Mettre en vente après l'amical de mardi (Lecomte y joue avec tir écran 1, brief Match).
- Preuve du contraire : fee final < 105 000 impossible (départ) ; si invendu jeudi : le relister à 50 000.

C-076 et C-077 ajoutés à `outputs/basketvibe/learnings.md`.

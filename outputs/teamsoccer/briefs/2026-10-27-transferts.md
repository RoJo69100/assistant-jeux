# Team Soccer — Transferts, 2026-10-27 (deux clubs)

Sources : `silver.ts_transfer_listings` (relevé 27/10 20:26 UTC, donc < 24 h), `silver.ts_my_bids`, `silver.ts_players` (27/10), `gold.ts_squad_report`, `gold.ts_finance_status`, briefs lecteur-exports et finances-personnel du jour, skill teamsoccer-club, fiche transferts, connaissance.md 5.4 / 5.8. Heures en Paris.
Contraintes : 1 achat par semaine par club (enchère en tête comptée, remise à zéro lundi 00:00 Canaries) ; effectif 16–24 ; solde >= enchère à la pose ; le vendeur et ses autres clubs ne peuvent pas enchérir ; revente interdite 7 semaines après achat.

## Cibles nommées

| Club | Cible | Prix | Gain chiffré | Confiance |
|---|---|---|---|---|
| Cows | **Florian Schäfer GK 20 ans, OVR 69, Gardien 93** (annonce 5423, banque, 0 offre, fin **29/10 08:59**) | départ 1 007 597 $ (= valeur) ; +8,2 % par offre (mesure du 23/10, 1 comparable : Hassan) | GB : meilleur gardien Romain Thomas OVR 61 (moyenne GB 49,0) -> +8 OVR au poste ; salaire ~10 076 $/sem. (1 %) | Moyenne-faible : Thomas a Gardien 100 contre 93 pour Schäfer, l'OVR vient donc d'autres compétences ; je n'ai pas la décomposition |
| Ben Ahmed | aucune | — | Titulaires 64–65 par zone (ATT 65, GB 65, DEF 64, MIL 64) ; rien d'achetable à <= 150 000 $ au-dessus de OVR 39 (5394 GK 16 ans, 108 800 $) | Haute |

Repli Cows : Schäfer décevant = vente à la banque à la valeur de fiche (revente bloquée 7 semaines : donc libération ou garde jusqu'au 15/12, coût = salaire ~10 k/sem.).

## Ventes et enchères ouvertes (règle 11)
| Club | Joueur | État vérifié | Conséquence |
|---|---|---|---|
| Cows | Etienne Roux FWD 19 ans, 63 (5396) | Vente à la banque déjà faite à la valeur de fiche **903 450 $** (déjà dans le solde ; confirmation : ventes cumulées +1 741 616 $ depuis le 23/10, brief lecteur). L'annonce à 1 093 175 $ / 2 offres / fin 28/10 10:28 est la remise aux enchères par la banque (skill club : la banque remet ensuite le joueur aux enchères) : **aucun gain supplémentaire pour le club**. Hypothèse (un cas) | Ne rien attendre de cette fin ; ne pas compter 1 093 175 $ dans les capacités |
| Ben Ahmed | Nanami Rousseau DEF 16 ans, 38 (5391) | Même mécanique : valeur 239 034 $ = prix demandé, 0 offre, fin 27/10 22:08. S'il n'y a pas preneur il disparaît du jeu (skill club). Prix déjà encaissé si vendu à la banque (non prouvé : le solde de Ben Ahmed a un écart inexpliqué de -506 299 $, brief finances) | Rien à faire ; vérifier la ligne au relevé du 28/10 |
| Cows | Omar Hassan MID 20 ans 77,2 (5343) | Clos le 25/10 15:01 UTC à 1 814 459 $, 4 offres (dernier `asking_price`). Absent de `silver.ts_players` (team 18) le 27/10 et dans la liste suivie (`ts_my_bids`) : **non acheté, perdu**. Gagnant non connu | Aucune dépense ; solde Cows n'a pas baissé de 1,8 M |

## Verdict par poste

### Chomelix Cows (capacité 1 959 436 $ ; 703 186 $ après les 8 375 places basiques)
| Poste | Verdict | Détail |
|---|---|---|
| GB | **ACHETER Florian Schäfer** | Enchère maximale **1 072 000 $** (solde après stade 1 072 728 $). Départ 1 007 597 $ ; une offre = 1 090 k$ : on gagne si personne d'autre n'enchérit. Financement : brûle la réserve (369 k$) mais la billetterie à domicile (433 800 $/match, 28 et 29/10) la reconstitue. Pose l'enchère **le 29/10 au matin** (dernières heures) |
| GB | **GARDER Romain Thomas** (61, 23 ans, 838 166 $) jusqu'au 02/11 puis **VENDRE à la banque** si Schäfer est gagné | 5 GB sinon ; vente à la banque immédiate, pas de plafond de ventes |
| GB jeunes | GARDER Thomas David (17 ans, Gardien 89), Étienne Roux GK (14 ans), Hugo Martin (15 ans) | Valeur en hausse, salaires 2 000–5 831 $ |
| DEF | GARDER tous | Ounahi 90 (1 600 026 $, 19 ans) ; Simon 68, Thomas 66, Dubois 65 ; aucun achat qui améliore |
| MIL | GARDER ; **pas d'achat** | Titulaires David 67, A. Roux 67, Robert 65. Aucune annonce MID au-dessus de 61 (5406 MID 26 ans 61, 608 449 $) |
| ATT | GARDER ; **pas d'achat** | Moreau 71, Bonnet 68, M. David 65 ; Roux (63) déjà parti |
Effectif : 21 au `gold.ts_squad_report` ; +1 (Schäfer) = 22, <= 24. L'achat de la semaine est consommé par Schäfer : aucun autre achat avant lundi 02/11.

### Ben Ahmed Donkey (capacité 262 227 $, plafond 150 000 $, rien avant le relevé du 28/10)
| Poste | Verdict | Détail |
|---|---|---|
| GB | GARDER | Schmidt 65, Suzuki 64, Abdel 63 (Gardien 81) |
| DEF | GARDER ; pas d'achat | 8 joueuses, meilleure Fernández 64, moyenne 57,2. Annonces ChispasFC22 (DEF 5418 60, 466 862 $) hors budget et sous les titulaires |
| MIL | GARDER ; **ACHAT reporté** | Martínez 64 ; moyenne 57,9. Meilleure annonce MID féminine/neutre : aucune au-dessus de 61. Reprendre C-012 (vendre Hayashi, Ibe puis acheter une milieu) seulement après le relevé du 28/10 |
| ATT | GARDER | Müller 65, Yamamoto 65, Wilson 63, Shimizu 62,5 |
Aucune vente identifiée à lancer. Ligne ouverte : Rousseau (voir tableau ci-dessus).

## Volet « leviers »
- **Cows** : un achat nommé (Schäfer GB, +8 OVR, 1 072 000 $ max) + une vente différée (Thomas 838 166 $ après arrivée) ; le net réel d'un remplacement de gardien est ~ -(1 007 597 à 1 072 000) + 838 166 = -170 k à -234 k$ pour +8 OVR. Les 8 375 places (1 256 250 $, finances) restent prioritaires sur le calendrier : les acheter avant l'enchère (le 28/10, avant le match de coupe de 15:11).
- **Ben Ahmed** : aucun levier chiffrable avant le 28/10 (cap 150 000 $) ; raison : solde 505 349 $ avec écart inexpliqué de -121 561 $ depuis le 25/10 et marché sans joueuse > 64.

## Test et preuve contraire
- Si Schäfer est acheté : preuve contraire = buts encaissés par match des Cows sur les 3 matchs suivants (29/10 coupe BOT, 31/10 ligue Bresse, ensuite) ; il doit faire mieux que Thomas (base à lire dans `gold.ts_match_report`). Verdict à rendre après le 31/10. Si pire sur 2 matchs : Thomas redevient titulaire et Schäfer est gardé comme doublure (revente bloquée 7 semaines).

## Il me manque
- Décomposition de l'OVR gardien (pourquoi Schäfer 69 avec Gardien 93 et Thomas 61 avec Gardien 100) : lire le skill joueurs ou l'écran joueur de l'annonce (export fiche d'annonce).
- Confirmation que la vente d'Étienne Roux a bien été payée à la banque (903 450 $) : ligne `silver.ts_finances.player_sales_income` Cows du relevé du 20/10–23/10.
- Gagnant de l'enchère Hassan (non exporté).

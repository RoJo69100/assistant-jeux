# Team Soccer — brief Transferts du 2026-10-23

Agent Transferts (medium + Sonnet). Fiches lues : `commun.md`, `transferts.md` ; skills `teamsoccer-club` (§ Marché), `teamsoccer-joueurs`. Briefs amont lus : Match (corrigé), Effectif, Finances-personnel, Académie, Entraînement, Tactique du 2026-10-23.
Vues : `silver.ts_transfer_listings` (L, export du 23/10 12:57 = 39 annonces, 12:58 = 5 annonces), `silver.ts_my_bids` (B), `silver.ts_finances` (SF), `gold.ts_finance_status` (F), `silver.ts_players` (J, 23/10). Heures de fin en heure de Paris.

## En tête : exports manquants et contradictions
| Point | Constat | Conséquence |
|---|---|---|
| Export Transferts | Présent (12:57 et 12:58 UTC). Total 44 annonces : 39 (noms masculins, postes GK/DEF/MID/FWD) puis 5 (noms féminins). L'attribution du lot de 39 à Chomelix et du lot de 5 à Ben Ahmed est déduite des noms, la base ne porte pas de `team_id` sur les annonces [Obs] | Aucun export à refaire aujourd'hui |
| Contradiction avec Finances et Effectif (Chomelix) | Ils demandent un milieu de banc **OVR ≥ 60** à 810 000 $ au plus. **Aucune annonce MID du marché n'a OVR ≥ 60 dans le budget** (L). Seul MID ≥ 60 : Omar Hassan (77,2) à 1 499 553 $ avec 2 offres, hors budget (capacité 812 987 $, 1 013 000 $ avec la vente de Hugo Martin) | **Relance de Finances et Effectif inutile** : le critère est inapplicable aujourd'hui, pas faux. Décision ci-dessous : aucun achat avant un nouvel export |
| Pas de contradiction | Ben Ahmed : vente de Hayashi et Ibe après le 28/10 (valeur 488 743 $ chacune, J), achat de MC à partir du 29/10, plafond 1 000 000 $ : concordent avec Finances, Effectif, Tactique (2c) et Entraînement | — |
| Offres en cours | B liste 7 annonces pour Chomelix (ids 391 à 872, jour 23/10) absentes de L (ids actuels 5315 à 5358) : annonces anciennes, aucune offre en tête visible aujourd'hui. `new_signings` = 0 cette semaine pour les deux clubs (SF) | Limite d'un achat par semaine : non entamée cette semaine [skill club] |
| Relevé du marché de Ben Ahmed | 5 annonces seulement, aucune MID utile (L). Si c'est un relevé partiel, un nouvel export serait nécessaire | Export Transferts du 29/10 de toute façon requis pour l'achat de Ben Ahmed |

## 1. Chomelix Cows (team_id 18) — solde 1 200 599 $, effectif 22/24
### Faits (L, J, F)
Annonces MID du lot (milieux, pas de poste MC/MD séparé dans L) :
| Joueur | Âge | OVR | Forme | Conduite | Prix actuel | Valeur | Offres | Fin | Type |
|---|---|---|---|---|---|---|---|---|---|
| Omar Hassan (5343) | 20 | 77,2 | 30 | 100 | 1 499 553 | 1 281 071 | 2 | 25/10 18:01 | banque |
| Fabricio Ledesma (5344) | 15 | 55,4 | 40 | 86 | 511 297 | 534 534 | 0 | 25/10 19:36 | banque |
| Mario Alberto Paz (5333) | 18 | 53 | 100 | 45 | 200 003 | 200 003 | 0 | 25/10 04:15 | banque |
| Nestor Quinteros (5347) | 15 | 48 | 100 | 66 | 385 868 | 385 868 | 0 | 25/10 23:56 | banque |
Autres MID : OVR ≤ 43 (Richter, Gomes, Müller, Martins, Moretti, Herrera, Drăgușin), sans intérêt face au banc actuel (44–49,2, J).
Banc milieu actuel : Jules Leroy 49,2 (Conduite 86), Lefebvre 44,7, Adrien Thomas 44,4 (J, Effectif).
Ventes comparables : aucune vente conclue en base (seuls 2 MID/DEF ont des offres : Hassan 2, Acuña 1). Niveau de confiance de tout prix : faible.

### Avis
- Hassan (77,2, Conduite 100, Passe 90) serait un titulaire, mais le prix actuel (1 499 553 $) dépasse le solde moins la réserve de 387 612 $ de Finances (capacité 812 987 $) et monte à chaque offre (2 offres déjà, dernier enchérisseur étranger). Forme 30 (×0,79 [skill joueurs]) : coût de remise en forme élevé. **Ne pas enchérir.**
- Ledesma (55,4, 15 ans, Forme 40) à 511 297 $ : +6 d'OVR sur le meilleur remplaçant (49,2), mais sous le seuil de 60 fixé par Effectif et Finances, et salaire ≈ 5 300 $/semaine pour un banc qui joue peu (aucun remplacement programmé, Match). Pas rentable.
- Paz et Quinteros : Conduite 45 et 66 sous le seuil de 70 qui fait un milieu [skill joueurs, compétences clés]. Non.
- Revente interdite 7 semaines après achat, effectif ≤ 24 [skill club] : un achat hors besoin bloquerait 7 semaines.

### Décisions fermes
| N° | Action | Quand | Montant | Pourquoi |
|---|---|---|---|---|
| 1 | **Ne poser aucune enchère aujourd'hui.** | — | 0 | Aucun MID ≥ 60 dans le budget (L) |
| 2 | **Enchère maximale à poser sur un milieu : 810 000 $ (plafond de Finances), uniquement sur une annonce MID avec OVR ≥ 60 et Conduite ≥ 70 apparue dans l'export du 25/10.** | Export du dimanche 25/10 au plus tard, enchère avant la fin de la semaine (lundi 26/10 00:00 Canaries) | ≤ 810 000 $ + environ 8 000 $/semaine de salaire | Seul achat de la semaine ; si rien, ne rien acheter et reporter au marché du 26/10 |
| 3 | **Ne pas vendre Hugo Martin aujourd'hui.** | À 24 joueurs seulement | 200 003 $ à la banque | Effectif 22/24, aucun achat prévu : la condition de Effectif n'est pas atteinte |

## 2. Ben Ahmed Donkey (team_id 15858) — solde 387 876 $, effectif 22/24
### Faits (L, J, F)
| Joueuse | Âge | Poste | OVR | Forme | Prix | Fin | Lecture |
|---|---|---|---|---|---|---|---|
| Celeste Chukwu (5336) | 15 | MID | 49,6 | 90 | 212 500 (valeur 225 507) | 25/10 06:55 | Conduite 57, Contrôle 69 : pas une MC (Conduite < 70) |
| Luna Devi, Sakura Patel, Lena Martínez, Luna Williams | 14–16 | DEF | 40,7–52 | — | 165 471–445 645 | 24 à 26/10 | Surplus DC déjà prévu : aucune |
Aucune annonce utile pour le trou structurel (MC Conduite ≥ 70). Toutes ces annonces finissent avant le 28/10.

### Décisions fermes
| N° | Action | Quand | Montant | Pourquoi |
|---|---|---|---|---|
| 1 | **Ne rien acheter ni enchérir jusqu'au 28/10.** | Jusqu'au 28/10 | 0 | Capacité 144 754 $ (Finances n° 4) ; aucune annonce utile (L) |
| 2 | **Vendre Kavya Hayashi et Suki Ibe à la banque, une après l'autre, après le match de coupe du 28/10 (15:35).** | 28/10, après le match | 488 743 $ chacune, ≈ 977 486 $ au total, sans commission [skill club] ; salaires −9 774 $/semaine (J) | Surplus DC de 2, 28 ans [Effectif] ; elles jouent encore les 26/10 (banc) et 28/10 (1-5-4-1, Hayashi), Tactique 2c : le 1-4-4-2 du 29/10 n'a pas besoin d'elles, le remplacement est Valentina Williams (42,3) |
| 3 | **Enchère maximale sur une milieu centrale (Conduite ≥ 70) : 1 000 000 $ au plus (plafond de Finances), uniquement sur une annonce avec Conduite ≥ 70, OVR ≥ 60, vue dans l'export du 29/10.** | À partir du 29/10, après encaissement de la vente | ≤ 1 000 000 $ + environ 10 000 $/semaine de salaire | Capacité ≈ 1 141 354 $ après vente (Finances) ; le prix juste n'est pas connu (aucune vente comparable en base) : confiance faible |
| 4 | **Ne pas surpayer : si la meilleure annonce dépasse 700 000 $, ne pas enchérir au plafond mais réexaminer le 02/11.** | 29/10 | 700 000 $ comme seuil de réflexion | L'entraînement de Conduite (Kumar, Mansour, Martínez, Schmidt ≥ 70 vers le 20/11, Entraînement) réduit le besoin à terme |

## 3. Calendrier de la limite d'achat (une action par ligne)
| Date | Club | Action |
|---|---|---|
| 24/10 | Les deux | Aucune enchère |
| 25/10 | Chomelix | Export Transferts du soir, puis Transferts relu avant l'enchère du point 1.2 |
| 26/10 00:00 (Canaries) | Les deux | Remise à zéro de la limite d'un achat |
| 28/10 après match | Ben Ahmed | Vente de Hayashi et Ibe à la banque |
| 29/10 | Ben Ahmed | Export Transferts puis enchère ≤ 1 000 000 $ |

## 4. Conseils suivis
| ID | Conseil | Critère SQL |
|---|---|---|
| C-024 | Chomelix : aucune enchère le 23/10 ; enchère ≤ 810 000 $ seulement sur un MID OVR ≥ 60 et Conduite ≥ 70 relevé le 25/10 | `silver.ts_finances.new_signings` = 0 au 24/10 ; sinon `balance` ≥ 387 612 après achat |
| C-025 | Ben Ahmed : Hayashi et Ibe vendues à la banque après le 28/10 | `silver.ts_players` 29/10 : Hayashi et Ibe absentes ; `gold.ts_finance_status.balance` ≥ 1 300 000 |
| C-026 | Ben Ahmed : MC Conduite ≥ 70 achetée ≤ 1 000 000 $ après le 29/10 | `silver.ts_players` : une joueuse avec Conduite ≥ 70 ; `new_signings` > 0 |

## Réserves
- Faits : L, B, SF, F, J du 23/10. Règles : skill club (vente banque sans commission, 1 achat par semaine, revente bloquée 7 semaines, effectif 16–24), skill joueurs. Avis : plafonds, refus de Hassan, Ledesma, seuil de 700 000 $ ; confiance faible (aucune vente comparable, marché de 44 annonces).
- Le lot de 39 annonces n'est pas relié à un club dans la base ; l'attribution à Chomelix est déduite.

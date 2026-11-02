# Marmandes (307) — Transferts, début de saison — 2026-11-02

Base : exports 307 du 2026-11-02 21:56-22:00 UTC (`gold.dm_effectif`, `gold.dm_verdict_joueurs`, `gold.dm_marche_notes`, `gold.dm_prix_reference`, `silver.dm_transfers`, `silver.dm_money_flow`, `silver.dm_school`, `silver.dm_facilities`, `gold.dm_finances_bilan`). Le brouillon du 30-31/10 est périmé pour 307. Briefs lus : entraînement et tactique du 2026-11-02. Police : à passer avant rendu (non lancée par moi).

## Fiche de saisie (tout aujourd'hui, dans cet ordre)
| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Export | Exporte le marché 307 filtré 8-20 M (et 5,5-8 M) : l'export de 22:00 va de 0,2 à 5,3 M (235 annonces, `silver.dm_market` ; 0 annonce > 5,5 M). **Il me manque l'export marché 8-20 M, fais-le.** |
| 🟥 URGENT | Transferts | Prolonge Desagnat (2 j), Vasilev (44 j), Lafleur (17 j), Lerch (19 j), Lévêque (29 j) |
| 🟥 URGENT | Transferts | Mets en vente McCulloch (2 j, 8,2 M) et Bodian (30 j, 4,9 M) |
| 🟥 URGENT | Transferts | Scoute Campos (DLCR, Santa Cruz), puis pose l'enchère maximale 2,86 M ; repli Morley, enchère max 2,64 M |
| 🟧 IMPORTANT | Académie | Promeus Loría (FC) ; garde Beth et Puisattier à l'école |
| 🟩 SUIVI | Finances | Pas de montée d'installations aujourd'hui |

## 1. Prolongations (base : coût = 5 % du prix, Vargas −240 000 le 2 nov = 5 % × 4,8 M, `silver.dm_money_flow` + `gold.dm_effectif` ; connaissance § 7 « prolongation = 5 % joueur » ; hypothèse pour les autres montants)
| Joueur | Poste, âge | Jours | Salaire / j | Prix | Frais ≈ | Décision |
|---|---|---|---|---|---|---|
| B. Desagnat | DLC 19, pot 3 | 2 | 14 k | 3,1 M | 155 k | prolonger : note 12,8, 3e défenseur, satisfait 100 % |
| B. Vasilev | FC 23, Key | 44 | 50 k | 5,5 M | 275 k | prolonger : meilleur attaquant (13,5) ; satisfaction 0 % pour 75 % attendus, à prolonger avant qu'il ne bloque (connaissance § 4, blocage si mécontent) |
| N. Lafleur | GK 20, pot 3 | 17 | 14 k | 4,4 M | 220 k | prolonger : GK n°1 (12,6), seul autre GK que Comonfort |
| C. Lerch | MCR 21, pot 3 | 19 | 17 k | 4,1 M | 205 k | prolonger : titulaire ML en 343, aucun milieu du marché n'a de gain sûr (voir 3) |
| C. Lévêque | MC 20, pot 3 | 29 | 14 k | 1,7 M | 85 k | prolonger : titulaire MRC, 14 k/j |
Total ≈ 940 k. McCulloch n'est pas prolongé (ci-dessous). Salaire : le salaire actuel est déjà dans les 509 k engagés ; réserve +10 k par prolongation [H, « demande + ~10 k », connaissance § 7].
Charbonnier (Key) : vendu 6,5 M à Almería le 1 nov (frais 1,1 M, 62 k/j, `silver.dm_transfers`). Aponte : vendu 9,1 M à Venezia le 2 nov (`silver.dm_money_flow`). Vente close ; le mentor Charbonnier n'est plus là (carte vente var. 10).

## 2. Ventes (listable = contrat < 85 j strict, connaissance § 7 ; effectif 20, minimum 18)
| Joueur | Poste, âge | Jours | Salaire / j | Prix | Décision | Base |
|---|---|---|---|---|---|---|
| A. McCulloch | FC 25, Rotation | 2 | 26 k | 8,2 M | **lister** | 2e attaquant (12,5) mais hors XI (tactique C-013) ; F lower division 22-28 ans : 17 ventes en base, médiane 7,5 M (5,9-9,9) ; Charbonnier et Aponte, deux FC, vendus en 2 jours. Non prolongé : 5 attaquants pour 3 places. Contrat échu = reste, très mécontent, entraînement 0 %, prix −10-15 % (connaissance § 7) : perte maximale ≈ 1 M. Confiance moyenne |
| F. Bodian | MC 23, Backup | 30 | 40 k | 4,9 M | **lister** | 9,0 au poste (rang 6 sur 7 milieux) pour 40 k/j, le salaire le plus haut des milieux ; M Useful 21-26 ans : 15 ventes, médiane 5,4 M (3,7-6,8). Libère 40 k de marge. Confiance moyenne |
Listables mais gardés : La Ferrière (74 j, titulaire 541), Messimy (70 j, Key), Labourd (80 j, 0,4 M : sous 1 M difficile à vendre).
**Non listables (≥ 85 j)** : Comonfort 87, Hardt 89, Schmitz 91, Taddei 94, Cave 96, Luzerne 96, Toussaint 98, Cleary 100, **Ohara 100**, **Vargas 104**.
**Ohara tranché : garder, S5 RAT reste.** Base : 100 j, non listable aujourd'hui ; mentor des attaquants (`gold.dm_verdict_joueurs.mentor`) ; 11,8, 4e attaquant. Le verdict « surplus : vendre » (Ohara, Vargas) n'est pas exécutable. Vargas : prolongé le 2 nov, 104 j.

## 3. Achat ciblé : DLCR Q. Campos (Santa Cruz)
| Cible | Poste, âge, tier | Prix | Salaire / j | Note au poste (bas / milieu) | Contre notre titulaire | Heure de fin |
|---|---|---|---|---|---|---|
| **Q. Campos** | DLCR 25, Useful | 2,6 M | 27 k | 11,2 / 14,9 | Schmitz 9,4 (DRC en 343) : +1,8 sûr / +5,5 | non affichée (`decision` vide) |
| C. Morley (repli) | DLC 22, Fringe | 2,4 M | 16 k | 11,4 / 14,3 | Schmitz 9,4 : +2,0 / +4,9 | non affichée |
| J. Mansfield | DC 22 | 3,5 M | 6 k | 11,8 / 15,5 | écarté : déjà demandé pour Queen of the South (fait-2026-11-02) | « a few days » |
Base : `gold.dm_marche_notes` (22:00). La vue compare au plus faible défenseur (Labourd 8,6) ; je compare au titulaire remplacé (Schmitz 9,4, tactique 343). Défense = ligne la plus faible avec le milieu (D 10,9, M 10,6, F 12,1, `gold.dm_verdict_joueurs`) ; sur les milieux le meilleur gain sûr du marché est −1,2 (Pellistri) : aucun achat milieu.
**Enchère maximale Campos : 2,86 M (110 % du prix affiché, sous le p25 Useful 24-27 ans = 4,45 M, `gold.dm_prix_reference`).** Comparables : 14 défenseurs Useful 23-28 ans vendus du 29 oct au 2 nov, 3,2-6,7 M, médiane 4,9 M (`silver.dm_transfers`). Un prix à 53 % de la médiane contredit « no bargains, prices correlate to quality » (dev 2026-02-07) : le bas de fourchette est calculé sur 5 clés vues, d'où le scout d'abord (carte var. 3). Confiance moyenne-faible.
**Finançable** : `capacite_invest` 25 438 469. Dépenses décidées : prolongations 0,94 M + Campos (2,86 M + frais ≈ 0,81 M [0,136 × prix + 16,9 × salaire, carte var. 14] + prime 0,5 M si hors France [H]) = 4,17 M, soit 5,11 M. Reste 20,33 M. Salaire : 27 k + réserve prolongations 50 k + Loría ~12 k [H] = 89 k ≤ marge 116 000. Finançable.
**Repli** : si l'achat déçoit, libération à ≤ 70 j de contrat sans indemnité sous un seuil de valeur (connaissance § 7) ; perte plafonnée à la prime et aux frais (≈ 1,3 M).
**Marché 8-20 M** : médiane Solid 24-27 ans 12,0 M, salaire moyen 96 k (`gold.dm_prix_reference`). Réserve : 12 M + 22,6 % de frais ≈ 14,7 M ≤ 20,33 M restants ; marge salariale 27 k seulement tant que McCulloch et Bodian ne sont pas vendus (93 k après). Aucun nom : le marché 8-20 M n'est pas en base.

## 4. École (effectif 20 : 5 places libres sur 25 ; limite 25 = promotion bloquée, connaissance § 6)
| Jeune | Données (`silver.dm_school`) | Décision |
|---|---|---|
| H. Loría FC 17, high / lower division player, 102 j | tir 19, jeu de tête 15, moyenne 16 compétences 8,1 = Luzerne (8,1, 18 ans) ; tier cible = celui de McCulloch (8,2 M) | **promouvoir** : prend la place libérée par McCulloch. Salaire d'un promu = coût des installations [H] ; confiance faible |
| A. Beth DC 16, high / lower division player, 97 j | moyenne 6,8 contre Hardt 5,6 | **garder** à l'école : 7 défenseurs après Campos, pas de minutes (un promu sans temps de jeu ne grandit pas, connaissance § 6) |
| G. Puisattier MC 15, low / established, 98 j | moyenne 5,3, marquage 16 | **garder** : libérer est irréversible, pas de nouveau tirage (« il faut promouvoir pour en obtenir un nouveau ») ; coût ≈ 35 k/j d'école pour 3 jeunes (`gold.dm_finances_bilan`) |

## 5. Installations (niveau 14, Local)
**Pas de montée aujourd'hui.** Base : `upgrade_at` 7,0 M, valeur actuelle −2,2 M : écart ≈ 9,2 M [H, 547 : valeur 0 et upgrade 8,0 M = « Missing value 8,0 M »]. Financièrement possible (20,33 − 9,2 = 11,1 M), mais : (1) montée de 547 refusée ce soir (fait-2026-11-02, cause inconnue) ; (2) « Always squad » avant installations (connaissance § 9, en doute) et l'argent restant sert au Solid 8-20 M ; (3) 9,2 M + Solid 14,7 M > 20,33 M ; (4) 0 plainte d'installations sur 20 joueurs (`gold.dm_verdict_joueurs.entrainement_txt`).

## Contrôle de la caisse (flux −419 474 / j)
Calcul : 200 000 + 365 000 + 48 834 − 358 091 − 190 000 − 35 000 − 509 000 (salaires engagés) + 58 783 (stade) = −419 474 (`silver.dm_finances`, vérifié). **Pas un artefact de saisie** : la ligne « Brand recognition » valait −0 le 2026-10-30 22:55 et −358 091 le 2026-11-02 21:59 (bronze `teams_id_finances` 307). Elle apparaît après les ventes de Charbonnier (6,5 M) et Aponte (9,1 M) : le conseil investit seul quand la caisse dépasse ~20 M (`resume.md` ; connaissance § 9, 2025-09-08). Autonomie à ce rythme : 25,4 M / 419 k = 60 j ; après 5,11 M de dépenses 20,3 M / 419 k = 48 j, plus que la saison (≈ 35 j). Que la ligne baisse sous 20 M est une hypothèse [H] : à lire au prochain export Finances. 547 : brand −58 133 pour 22,98 M.

## Ce qui prouvera que j'avais tort
- Campos : note au poste < 11,2 à la fiche scoutée, ou titulaire au poste moins de 20 min d'ici l'amical du 2026-11-03 (`gold.dm_effectif`, apps).
- McCulloch : toujours dans `gold.dm_effectif` avec `contract_days` 0 à l'export du 2026-11-03 → vente ratée, prix −10-15 %.
- Prolongations : un refus à l'écran (mécontent / trop bon pour le tier) ; Vasilev toujours à 0 % de temps de jeu après le 2026-11-03.
- Loría : < 20 min jouées au 2026-11-09.
- Brand : ligne toujours ≈ −358 k avec une caisse < 20 M au prochain export Finances.

Conseils ajoutés dans `outputs/derbymanager/learnings.md` : C-014, C-015, C-016.

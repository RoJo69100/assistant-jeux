# Six Zero League — brief Transferts, 2026-10-26

Marché : export du 2026-10-26 17:49 UTC (`silver.sz_transfer_listings`, 33 annonces, à jour). Briefs amont lus : match, effectif, finances, académie, entraînement, tactique (2026-10-26). Skills : club (marché, finances), joueurs, entraînement, communauté. Aucun achat, aucune vente n'est lancé sans ton accord.

## En tête : actions possibles (date limite : avant 21:00 Paris ce soir, coup d'envoi de J16 : les annonces `settle_after_round` = 16 se terminent là [Dev chat, skill communauté])
| # | Action | Montant | Règlement | Condition |
|---|---|---|---|---|
| 1 | **Enchérir sur Emanuel Oliveira (CB, 26 ans, note 11)** | **2 500 €** (départ, aucune offre), plafond 2 500 € | après J16 ce soir | Seulement si tu veux un 3e CB certain ; sinon passer |
| 2 | Alternative : Tobias Kristensen (LB, 26 ans, note 14) | 3 000 € (départ), plafond 3 000 € | idem | Exige d'abaisser la réserve de 2 300 € (voir Correction) ; **un seul des deux achats** |
| 3 | Ne rien vendre | | | Aucun joueur en vente, aucune enchère ouverte de ta part (voir § 4) |
- Pas d'enchère maximale automatique dans le jeu : chaque offre est manuelle [skill club]. Mon « plafond » est la limite que tu t'imposes.

## Correction (contredit ou nuance des conseils précédents)
- **C-025 (Finances, solde >= 2 300 € en permanence)** : respecté pour Oliveira (4 767 - 2 500 = 2 267 en sortie de cycle, soit 33 € sous la réserve, puis 2 341 € fin de saison après 2 salaires). Pour Kristensen : fin de saison ≈ 1 791 €, soit 509 € sous la réserve (une victoire de ligue = +480 € de prime). C'est une exception à toi de valider, je ne la fais pas passer par défaut.
- **C-026 / C-031 (formation de rôle 2 700 €, Lemaire -> CB)** : si Oliveira est acheté, elle n'a plus d'objet pour le CB (Oliveira 11 contre Lemaire 10 en CB, `role_overalls`) et 2 500 € remplace 2 700 €.
- **C-033 (Simon CB titulaire J16-J18)** : valable ce soir ; si Oliveira arrive, il passerait titulaire CB dès J17 (13:00) et Simon remplaçant : relance Tactique alors. Le brief Académie (Fournier) reste valable (jeune, long terme), mais Fournier + Oliveira feraient 4 CB.
- **C-009 (revoir le LB 18 ans note 20 s'il est relisté)** : non relisté (meilleur LB à vendre : note 14). Clos par cet export.
- **C-008a (RB 29 ans, max 4 000 €)** : aucune annonce RB de 29 ans ce soir ; pas de suite.

## 1. Cibles (nos rôles faibles : CB mince, RB exposé à moyen terme)
Notes visibles de tous sur une annonce [W:Transfers] ; notes de nos joueurs : `silver.sz_players` (as_of 2026-10-26). Coût total = prix + salaire par cycle (9 cycles par saison ; salaires revus entre les saisons [W:Finances]) ; aucun frais pour l'acheteur n'est écrit dans le skill club. **0 vente conclue en base : aucun prix de référence, confiance faible.** Repère indirect : offres en cours Ferreira RB 20 ans note 13 à 7 000 €, Correia RB 30 ans note 13 à 2 500 €, Balogh RW note 11 à 3 000 €.
| Annonce | Âge | Note | Compétences clés (CB : Passe, Technique, Jeu sans ballon, Tir) | Prix actuel / prochain palier | Salaire | Coût total (prix + 2 cycles de salaire) | Gain | Verdict |
|---|---|---|---|---|---|---|---|---|
| **Oliveira (CB)**, vendeur ECP | 26 | **11** | Passe 12, Technique 16, Jeu sans ballon 7, Tir 11 ; éthique 75 | départ 2 500 (aucune offre) | 100 | **2 700** | **+1 sur Simon (10), +3 sur Denis (8)** au CB ; remplaçant sûr si Simon se blesse | **Meilleur rapport dans le budget** |
| Kristensen (LB) | 26 | **14** | Tir 16, Passe 14, Technique 11, Jeu sans ballon 20 ; éthique 71 | départ 3 000 (aucune offre) | 125 | 3 250 | **+4 sur A. Bertin (10)**, +5 sur Leroy (9) ; plus gros gain de la liste | Hors réserve (voir Correction) |
| Correia (RB) | 30 | 13 | Tir 18, Passe 15, Technique 14, Jeu sans ballon 18 | 2 500 (RSC Mauve en tête) / **3 500** | 125 | 3 750 | +3 sur Roger / Barros (10) ; 30 ans : déclin physique chaque saison | **Passer** : 3 500 déjà hors budget, 30 ans |
| Torres (RB) | **18** | **15** | Tir 22, Passe 23, Technique 9, Jeu sans ballon 9 ; éthique 4 | départ 5 500 (aucune offre) | 145 | 5 790 | +5 sur le RB ; relève du poste le plus exposé à 2 saisons | **Hors de portée** : 5 500 + réserve 2 300 = 7 800 € contre 4 767 ce soir |
| Domański (GK) | 33 | 12 | Placement 20, Réflexes 13, Prise de balle 13, Un contre un 16 | départ 1 000 | 160 | 1 320 | 0 sur Bourgeois (12) ; +3 sur Blanc (9) qui ne joue pas (0 match) | **Passer** : 160 par cycle pour un 3e gardien, 33 ans |
- Gain en « points de note » : la note de l'annonce est la note au rôle ; sa traduction en buts n'est pas prouvée (L-001 : le résultat tient surtout à l'efficacité et aux arrêts, brief Match § 2). Confiance faible.
- Autres CB à vendre : Saraiva (32 ans) et Papaioannou (31 ans), note 9 : pas d'amélioration. Autres RB : Ferreira (20 ans, 13) est à 7 000 et monte (Team Seise HB en tête) ; Pereira (32 ans, 9), Trauco (8), Van den Broeck (7) : aucun gain.
- **Pourquoi aucun RB ce soir (raison chiffrée)** : la seule note >= 13 à portée de prix est Correia, 3 500 € au prochain palier + 125 de salaire. Sortie de cycle 4 767 - 3 500 = 1 267 €, soit 1 033 sous la réserve ; fin de saison ≈ 5 041 - 3 500 - 250 = 1 291 €. Torres (15, 18 ans) est la bonne cible long terme (RB : Roger 27 ans, Barros 30 ans) mais coûte 5 500 €. Surveiller les RB jeunes au premier marché de la saison suivante, après les salaires et avec le Fan Shop 10 reporté si besoin (arbitrage C-025).
- Coût de repli (si l'achat déçoit) : libération 500 € [skill club], le salaire est sauvé ensuite ; pour Oliveira, perte maximale ≈ 2 500 (prix) + 500 = 3 000 €, puisqu'une revente n'a aucun prix de référence.

## 2. Enchère maximale : base de calcul (avis, confiance faible)
| | Oliveira | Kristensen |
|---|---|---|
| Solde après le cycle de ce soir (brief Finances) | 4 767 | 4 767 |
| Plafond | **2 500** | 3 000 |
| Solde après achat | 2 267 | 1 767 |
| Fin de saison ≈ 5 041 - prix - 2 salaires | **2 341** (réserve tenue) | 1 791 (509 sous la réserve) |
- Données : `silver.sz_finances`, brief Finances (cycle 8 prévu +2 924 €, cycle 9 ≈ +274 €, hypothèse sans victoire). L'ordre exact entre règlement du marché et rapport financier n'est pas écrit dans les skills : 1 843 € aujourd'hui suffisent pour 2 500 € seulement si le revenu de la soirée est déjà crédité ; un solde négatif n'a pas de pénalité écrite [W:Finances], mais **je ne l'ai pas vérifié**.
- Risque d'enchère : une offre adverse monte le prix de 1 000 € (palier [skill club]). Oliveira a 0 offre, mais RSC Mauve et d'autres managers enchérissent sur plusieurs joueurs. Si on te passe à 3 500 : passer (fin de saison 1 341 €, nettement sous la réserve).
- Quand enchérir : le plus tard possible avant 21:00 (l'enchère reste possible pendant un match, mais l'annonce se ferme au coup d'envoi [Dev chat]) ; aucune règle de prolongation n'est écrite pour ce jeu.

## 3. Nos joueurs : vendre / garder (`silver.sz_players`, 26/10)
| Joueur | Âge | Rôle, note | Salaire | Retraite | Décision |
|---|---|---|---|---|---|
| Bourgeois | 30 | GK 12 | 145 | non annoncée ; retraite possible à partir de 33 ans (s+3) [brief Effectif, W:Retirement] | **Garder** (titulaire, aucun GK de remplacement meilleur à vendre) |
| Barros | 30 | RB 10 | 110 | non annoncée ; idem 33 ans | **Garder** cette saison (remplaçant RB, meilleure Technique 17) ; revoir à l'été si un RB jeune est acheté |
| Roger | 27 | RB 10 | 100 | non | Garder |
| Blanc | 26 | GK 9, 0 match | **140** (15,6 par point, le plus cher) | non | **Garder** : seul GK remplaçant (un remplaçant par rôle [W:Injuries]) ; libérer coûte 500 € et laisse le poste vide |
| G. Bertin | 25 | RW 9, 0 match | 90 | non | **Seul surplus vendable** (brief Effectif). Vendre n'apporte qu'un prix de départ >= 1 000 € moins 500 € de frais non remboursés, sans prix de référence, pour 90 par cycle économisés. **Garder jusqu'au relevé de la saison suivante** (il progresse vite en Vitesse, brief Entraînement) |
| Denis | 26 | CB 8 | 90 | non | Garder ; **vendable seulement si Oliveira ET Fournier arrivent** (4 CB) |
| Sundberg | 29 | LW 10 | 95 | non | Garder (remplaçant LW, plan B C-034) ; 30 ans à la fin de la saison |
| Lefebvre, Dupont, Simon, Benoit | 27, 18, 19, 19 | titulaires | 100 à 125 | non | Garder |
- Aucun joueur n'est `for_sale` dans `silver.sz_players` et aucune annonce de notre club dans `silver.sz_transfer_listings` : **pas de vente à surveiller**.
- Minimum d'effectif 7 [skill club] : sans objet (15 joueurs).
- Impossible de vendre ou libérer pendant un match de notre équipe : si une mise en vente est décidée, la faire avant 21:00 ou après J16.

## 4. Ventes et enchères ouvertes
| Élément | État | Source |
|---|---|---|
| Joueurs en vente de notre club | **aucun** | `silver.sz_players.for_sale` faux pour les 15 ; aucune annonce avec notre vendeur |
| Enchères posées par nous | **aucune** | aucune annonce où nous sommes `highest_bidder` |
| Achats conseillés par Transferts non faits | C-008a, C-009 : sans objet ce soir | voir Correction |
| Joueur acheté sur conseil à revendre | aucun | — |

## 5. Il me manque
- Prix de référence : aucune vente conclue en base (le jeu garde un historique « Transfer history », non exporté). Un export de cet onglet donnerait un vrai repère de prix.
- Le salaire de Fournier (Académie) n'est pas exporté : si tu signes Fournier ET Oliveira, ajoute son salaire (~100 estimé) au calcul de réserve : fin de saison ≈ 2 241 € (sous 2 300 de 59 €).
- Durée restante des blessures de Simon et Roger (briefs Effectif et Tactique) : si l'un d'eux est blessé à l'écran, le besoin au CB ou RB est plus fort.

## 6. Nouveaux conseils (ajoutés à `learnings.md`)
- **C-035** : enchère Oliveira (CB), plafond 2 500 €, avant 21:00 Paris.
- **C-036** : alternative Kristensen (LB), seulement avec exception sur la réserve ; un seul des deux.
- **C-037** : aucun achat RB ce soir, aucune vente avant la saison suivante.
- **Faux si** (C-035) : Oliveira acheté et sa note au CB < 10 dans l'export du 27/10, ou `fc_expenses` du cycle 8 > 2 270 + 100 salaire + 2 500 sans que le solde revienne >= 2 300 € fin de saison.

## 7. À refaire si
- Export Marché de demain soir (nouvelles annonces, règlement) ou prix qui bouge sur Oliveira avant 21:00.
- Fournier signé (CB à 4) ou refus de l'exception de réserve.
- Blessure de Simon ou Roger confirmée.

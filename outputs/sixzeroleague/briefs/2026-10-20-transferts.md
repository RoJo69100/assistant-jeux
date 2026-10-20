# Brief Transferts — SixZero League — 2026-10-20 (Chomelix Cow)

## Actions (à faire avant 21:00 Paris, coup d'envoi de J4 contre Nenaa ; règlement de toutes les annonces après la journée 4)
| # | Action | Enchère | Max conseillé (avis) | Coût total estimé |
|---|---|---|---|---|
| 1 | LW 29 ans, note 10, salaire 95 (vitesse 19, détente 19, endurance 19) : annonce sans enchère | 1 000 € (1re enchère = prix de départ) | **2 000 €** | 2 000 + ~7 cycles x 95 = ~2 700 € |
| 2 | RB 29 ans, note 11, salaire 110 (passe 18, contrôle 19, relance 19) : enchère actuelle 2 000 € | 3 000 € (prochain palier) | **4 000 €**, seulement si tu desserres la réserve (voir arbitrage) | 4 000 + ~7 x 110 = ~4 800 € |
- Aucune enchère automatique dans le jeu : chaque enchère est manuelle, et le plus offrant au règlement l'emporte [W:Transfers]. Revérifie le prix affiché juste avant d'enchérir.
- Si le prix dépasse ton max : laisse tomber, le marché se renouvelle chaque soir.
- Données : export du 2026-10-20 17:41 UTC (19:41 Paris), 24 annonces, moins de 12 h : frais.

## Faits (données)
- Effectif de 12 joueurs, aucun en vente, aucun blessé ni retraité (`silver.sz_players`, 2026-10-20 ; `gold.sz_lineup_natural`).
- Postes sans remplaçant naturel : LW (Lefebvre 13 seul) et RB (Roger 10 seul) ; tous les autres rôles ont un remplaçant (`gold.sz_lineup_natural`).
- Remplaçants hors poste existants (note de rôle, avant pénalité) : LW = S. Blanc 11, Simon 10, A. Bertin 10, Benoit 10 ; RB = 9 pour Simon, Benoit, A. Bertin, Blanc, Lemaire (`silver.sz_players.role_overalls`). La note de rôle est calculée avant la pénalité de hors-poste (commun.md, [Obs SQL 2026-10-18]) : un naturel à note égale vaut plus.
- Argent : solde 10 531 € ; salaires 1 230 € par cycle ; résultat prévu du cycle de ce soir +6 400 € (prévision, `silver.sz_finances` 2026-10-20). Réserve de 5 500 € et Fan Shop 6 -> 7 (3 100 €) conseillés plus tôt dans la journée (C-005, `outputs/sixzeroleague/learnings.md`).
- Annonces pour nos rôles faibles (`silver.sz_transfer_listings`, 2026-10-20) :

| Rôle | Âge | Note | Salaire | Enchère / prochaine | Compétences clés du rôle | Lecture |
|---|---|---|---|---|---|---|
| LW | 29 | 10 | 95 | aucune / 1 000 | Vit 19, Agi 5, Tir 7, Ctrl 15 | seul LW naturel jouable à ce prix |
| LW | 35 | 9 | 95 | aucune / 1 000 | Vit 13, Agi 18, Tir 4, Ctrl 6 | 35 ans : déclin physique et risque de retraite (dès 33 ans) ; à écarter |
| RB | 29 | 11 | 110 | 2 000 / 3 000 | Tir 14, Dét 14, Tec 5, Pas 18 | +1 sur Roger, remplaçant naturel |
| RB | 26 | 11 | 120 | 5 000 / 6 000 | Tir 30, Dét 12, Tec 10, Pas 26 | grosse finition, mais endurance 1, marquage 1, vitesse 3 |
| RB | 26 | 12 | 115 | 7 000 / 8 000 | Tir 12, Dét 19, Tec 19, Pas 14 | meilleur profil, déjà cher |
| RB | 19 | 8 | 90 | aucune / 5 000 | Tec 20 | prix de départ trop haut pour une note de 8 |
| LB | 18 | 14 | 130 | 8 500 / 9 500 | (hors priorité) | +4 sur A. Bertin (10), mais coûte presque tout le solde |

## Règles (skills)
- Prix de départ 1 000 €, palier 1 000 €, frais de mise en vente 500 € non remboursés, libération 500 €, effectif 7 à 30, règlement toutes les 2 journées [W:Transfers] (skill sixzeroleague-club).
- Salaire fixé selon le niveau, revu seulement entre saisons [W:Finances] : compte-le en plus du prix. Estimation : environ 7 cycles restants cette saison (le cycle de ce soir est le 2e sur 9) ; fourchette à confirmer.
- Compétences clés : ailiers = Vitesse, Agilité, Tir, Contrôle ; arrières = Tir, Détente, Technique, Passe [W:Attributes].
- Âge : déclin des compétences physiques dès 30 ans à chaque changement de saison ; un an de plus tous les 9 à 11 jours [W:Training ; Dev chat]. Un 29 ans passera à 30 ans à la prochaine saison.
- Arrières et pivots sont bien plus exposés aux blessures que les ailiers [W:Injuries] : un remplaçant RB naturel a plus de valeur qu'un remplaçant LW.

## Prix (faits et ventes comparables)
- Pas de vente conclue en base. Indice faible : annonces du 2026-10-18 disparues le 2026-10-20 avec une enchère en cours (probablement vendues, prix final inconnu, au moins la dernière enchère vue). Pour les joueurs de champ de note 11 à 13 : 4 000 (P 27 ans, note 13), 4 000 (P 21 ans, note 11), 4 000 (LW 29 ans, note 11), 6 000 (RB 26 ans, note 11). **4 indices** à moins de 6 000 pour une note de 11 à 13 (`silver.sz_transfer_listings`, relevé du 2026-10-18, un seul export). Le RB de 26 ans (Tir 30) a été remis en vente à 4 000 par son nouvel acquéreur (mêmes compétences à 1 point de passe près), signe que 6 000 était déjà un haut de fourchette.
- Les annonces de note 7 à 9 sans enchère restent souvent invendues (LW 33 ans notes 8 et 9, RB 30 ans note 9, LB 26 ans note 7 relistée).
- Verdict : LW 29 ans à 1 000 = bonne affaire ; RB 29 ans note 11 à 3 000-4 000 = correct ; RB note 12 à 8 000 et plus = cher ; LB 18 ans note 14 à 9 500 = cher pour notre solde, mais le seul profil jeune à fort potentiel du marché.

## Avis : enchères maximales (confiance faible : 4 indices de prix, un seul export, pas de prix final)
1. **LW 29 ans, max 2 000 €.** Base : prix de départ 1 000 sans enchère, note 10 contre 10 pour A. Bertin hors poste, mais naturel (pas de pénalité) ; indice : LW 29 ans note 11 a dépassé 4 000. Effet : remplaçant naturel de Lefebvre (13). Plafond de 2 000 car la note reste basse et il perdra du physique dès 30 ans. Coût total ~2 700 €.
2. **RB 29 ans, max 4 000 €.** Base : 4 indices de ventes à 4 000-6 000 pour des notes de 11 à 13 ; celui-ci est le moins cher des RB de note 11 et passe à 12-13 chez nous seulement avec l'entraînement. Effet : +1 sur Roger au poste, remplaçant naturel du poste le plus exposé aux blessures. Coût total ~4 800 €. Valeur modeste (+1 note) : si le prix dépasse 4 000, passe.
3. Pas de LB, pas de RB à 7 000 et plus ce soir.

## Arbitrage argent (la décision est à toi)
- Solde 10 531 - Fan Shop 3 100 = 7 431 ; avec la réserve de 5 500 du conseil C-005, il reste **~1 900 € pour les transferts** : donc seulement l'enchère 1 (1 000, max 2 000 avec un dépassement de la réserve de ~70 €).
- L'enchère 2 (jusqu'à 4 000) exige soit de reporter le Fan Shop, soit de ramener la réserve vers ~3 500-4 500. Ma préférence (avis) : le LW d'abord ; le RB seulement si le prix reste à 3 000 ; le Fan Shop peut attendre demain. Le règlement a lieu avec le cycle de ce soir ; ce que le jeu fait si le solde est insuffisant au règlement n'est pas dans les skills : ne mise pas plus que le solde du moment.

## Joueurs à vendre
- **Vendre ou libérer : personne ce soir.** Aucun retraité, aucun blessé. Les moins bons (F. Denis CB 26 ans note 7, salaire 90 ; Guillaume Leroy LB 24 ans note 8, salaire 75) sont les seuls remplaçants de leur rôle. Une mise en vente coûte 500 € non remboursés et les annonces de note 7-9 restent souvent invendues : l'économie (75-90 € par cycle) ne couvre pas le risque.
- **S. Blanc (GK 26 ans, note 9, salaire 140)** : remplaçant gardien unique, en formation RW (150 € par cycle, 3/36 journées en cours, perdu si annulé) : garder.
- Les jeunes (Simon 19, Benoit 19) : garder, bonus d'entraînement complet jusqu'à 20 ans [W:Training].
- Retraite : aucun joueur à 33 ans ou plus, rien à anticiper cette saison.
- Impossible de vendre ou libérer pendant un match de ligue : fenêtre avant 21:00.

## Limites
- Prix finaux inconnus ; export unique du marché la veille (2026-10-18) et celui d'aujourd'hui ; les enchères montent jusqu'au coup d'envoi.
- L'identité des vendeurs et les noms des annonces ne figurent pas dans l'export ; vendeurs humains pour toutes les annonces (`seller_is_bot` faux).
- La note affichée dans une annonce est supposée être la note au rôle de l'annonce (non vérifié).
- Prochain export Transferts utile : demain avant 21:00 (annonces closes au coup d'envoi).

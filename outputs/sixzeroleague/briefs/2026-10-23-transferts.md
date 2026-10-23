# Six Zero League — brief Transferts du 2026-10-23

**Export manquant : aucun, mais une réserve sur le marché.** Dernier relevé `/transfers` : 2026-10-23 06:51 UTC (08:51 Paris), `settle_after_round` = 10, donc règlement **après le match J10 de 21:00 Paris** (`silver.sz_transfer_listings`). `seen_at` aura plus de 12 h à 20:51 Paris : refaire l'export Transferts juste avant toute enchère.
**Écart avec la demande : « 57 annonces ».** La vue `silver.sz_transfer_listings` garde chaque annonce vue une fois (dernier relevé par annonce) : 23 (18/10) + 28 (20/10) + 6 (23/10) = 57. **Seules 6 sont en cours** ; les 51 autres sont des annonces déjà réglées (règlements 2, 4 et 6). Si l'écran en montre plus de 6, la capture est partielle : réexporter.
**Contradiction avec les briefs amont : aucune.** Match, Effectif (corrigé), Finances-personnel, Académie, Entraînement et Tactique lus. Je suis la consigne Finances : aucune dépense avant la fin de saison (~27/10), capacité ~2 900.

## Actions
| # | Quoi | Date limite | Confiance |
|---|---|---|---|
| 1 | **Ne rien acheter** parmi les 6 annonces (aucune ne comble CB ou LB, voir § 1) | avant 21:00 Paris (règlement après J10) | moyenne |
| 2 | **Ne rien vendre** (voir § 3) | — | faible |
| 3 | Fin de saison (~27/10) : relire le marché ; si le LB de 18 ans (note 20) revient en vente, c'est l'occasion à étudier (capacité ~19 500 alors) | après la dernière journée | faible |
Aucune enchère à saisir : pas de montant, pas de journée de règlement à viser aujourd'hui.

## 1. Marché du jour (6 annonces, `silver.sz_transfer_listings`, 06:51 UTC)
Faits : aucun vendeur bot, aucun joueur libre, aucune retraite annoncée. Palier 1 000 [skill club]. Notre besoin (briefs Effectif et Tactique) : rôles minces **CB** (Denis 8, titulaire Simon 10) et **LB** (Leroy 8, titulaire A. Bertin 10). **Aucun CB en vente.**
| Rôle | Âge | Note | Salaire | Prix de départ | Enchère actuelle / prochaine | Compétences clés du rôle (moy.) | Nos joueurs au rôle |
|---|---|---|---|---|---|---|---|
| LB | 18 | **20** | 175 | 18 000 | 18 000 / 19 000 | Tir 9, Détente 16, Technique 27, Passe 27 (19,8) | A. Bertin 10 (10,3), Leroy 8 |
| P | 30 | 11 | 110 | 1 500 | 1 500 / 2 500 | Force 7, Ctrl 6, Jeu s/ballon 19, Tir 15 (11,8) | Benoit 10, Chevalier 9 |
| LW | 23 | 11 | 110 | 3 000 | aucune / 3 000 | Vitesse 1, Agilité 12, Tir 25, Ctrl 15 (13,3) | Lefebvre 13 (17,0), Sundberg 10 |
| RW | 24 | 10 | 105 | 1 000 | 1 000 / 2 000 | Tir 15, Ctrl 4 (autres non relues) | Dupont 11, G. Bertin 9, Lemaire 8 |
| LB | 27 | 9 | 95 | 1 000 | aucune / 1 000 | Tir 7, Technique 3, Passe 7 | A. Bertin 10, Leroy 8 |
| RB | 19 | 8 | 90 | 6 000 | aucune / 6 000 | Tir 4, Technique 20, Passe 9 | Roger 10, Barros 10 |

### Verdict par annonce (avis)
| Annonce | Intérêt | Prix | Enchère max conseillée | Coût (prix + salaire) |
|---|---|---|---|---|
| LB 18 ans, note 20 | **Très fort** : 10 points au-dessus de A. Bertin, 7 au-dessus de notre meilleur joueur (Lefebvre 13) ; 18 ans = bonus d'entraînement complet et plusieurs saisons [W:Training] | Cher pour nous, normal pour sa qualité (aucune vente comparable de note 20) | **0 : inabordable** (19 000 contre un solde de 5 235 et ~2 900 de capacité) | 19 000 + 175 par cycle (soit +11 % de masse salariale 1 550) |
| P 30 ans, note 11 | Faible : +1 sur Benoit, +2 sur Chevalier ; Force 7 (clé du pivot), 30 ans = déclin physique dès le changement de saison [W:Training] | Correct | 0 (pas d'achat) | 2 500 + 110 par cycle |
| LW 23 ans, note 11 | Nul : Lefebvre 13, Sundberg 10 | Cher pour +1 sur le LW2 | 0 | 3 000 + 110 |
| RW 24 ans, note 10 | Nul : 3 joueurs déjà (11, 9, 8) | Bas | 0 | 2 000 + 105 |
| LB 27 ans, note 9 | Très faible : +1 sur Leroy (8), −1 sur A. Bertin, aucune clé forte | Bas | 0 | 1 000 + 95 |
| RB 19 ans, note 8 | Nul : Roger 10, Barros 10 | Cher | 0 | 6 000 + 90 |
Règles : compétences d'un joueur en vente visibles de tous, salaires fixés entre les saisons, enchère manuelle (+1 000), règlement toutes les 2 journées, effectif 7 à 30 [skill club, W:Transfers, W:Finances]. Effectif actuel 15 : place pour acheter.
Calcul de l'avis : capacité d'achat ~2 900 (Finances) ; le seul achat qui y tient (P 2 500) apporte +1 de note pour un joueur de 30 ans qui va décliner et consommerait toute la réserve avant la fin de saison. Confiance moyenne.

### Le LB note 20, à suivre
Fait : prix de départ 18 000, déjà une enchère à 18 000 (`current_bid`), prochaine 19 000, règlement ce soir. Nous ne pouvons pas l'acheter : même vendre tout le banc ne couvrirait pas l'écart (voir § 3). Le skill ne dit pas si une enchère supérieure au solde est acceptée ou refusée : je ne conseille pas d'essayer, c'est hors des règles écrites. S'il reste invendu, il revient à son vendeur [skill club] ; l'annonce pourrait revenir, à un prix que le vendeur fixe. À la fin de saison, capacité estimée ~19 500 (brief Finances, confiance moyenne), mais cela viderait la réserve et concurrencerait Fan Shop 10 / Arena 8 (priorités Finances) : arbitrage à faire alors, pas aujourd'hui.

### Repères de prix (confiance faible)
Aucune vente conclue en base : pas de prix de référence [fiche, règle 4]. On a seulement le dernier prix vu par annonce réglée (51 annonces) : par exemple CB 25 ans note 15 à 13 000 (départ 11 000), LB 18 ans note 14 à 8 500 (départ 4 500), RB 26 ans note 12 à 7 000 (départ 3 000), RB 26 ans note 11 à 5 000-6 000, P 21 ans note 11 à 4 000 (départ 1 000). Ce sont des enchères vues, pas des prix de règlement. Le niveau 11 se situe donc plutôt à 4 000-6 000 : les annonces P à 1 500 et RW à 1 000 d'aujourd'hui sont à ce stade bon marché mais sans intérêt sportif.

## 2. Poste à renforcer, à surveiller sur les prochains marchés
| Poste | Faiblesse (Tactique, Effectif) | Cible type |
|---|---|---|
| CB | Denis 8 en remplaçant ; Simon 10 a Passe 4 et Jeu sans ballon 4 | CB avec Passe, Technique, Jeu sans ballon, Tir élevés [W:Attributes] ; le marché du 18/10 avait deux CB note 15 à 12 000-13 000, hors budget |
| LB | Leroy 8 en remplaçant | LB note ≥ 10 |
| GK à 2 saisons | Bourgeois 30 ans en déclin | à regarder à l'U18 (brief Académie) |
Rien d'urgent : aucun blessé, 15 valides (Tactique).

## 3. Nos joueurs : vendre, garder (confiance faible)
Faits (`silver.sz_players` via briefs Effectif et Tactique) : 15 joueurs valides, aucun retraité annoncé (retraite possible dès 33 ans, Bourgeois et Barros ont 30 ans). Règles [skill club] : frais de mise en vente 500, non remboursés ; prix de départ minimum 1 000 ; effectif minimum 7 ; vente impossible pendant un match de ligue de notre équipe (J9 à 13:00, J10 à 21:00) ; un joueur qui annonce sa retraite ne peut plus être vendu.
| Joueur | Poste, note, âge, salaire | Place | Avis |
|---|---|---|---|
| Barros | RB2, 10, 30 ans, 110 | Seul remplaçant naturel de Roger ; 0 minute | **Garder** : le vendre supprime le remplaçant naturel RB [W:Injuries] ; déclin physique à venir, à rejuger après le changement de saison |
| Sundberg | LW2, 10, 29 ans, 95 | Seul remplaçant naturel de Lefebvre | **Garder** |
| Lemaire | RW3, 8, 22 ans, 90 | 3e RW ; 7 exclusions ; note CB 10 hors poste (Entraînement) | **Garder** : seul vrai surplus (14 postes pour 15 joueurs), mais la vente rapporterait peu (niveau 8, enchères vues 1 000-6 000 pour 8-11) moins 500 de frais ; sans besoin d'argent immédiat, la valeur de dépannage CB l'emporte |
| Blanc | GK2, 9, 26 ans, 140 (le plus cher au point) | Remplaçant obligatoire du gardien ; formation RW en cours | **Garder** : pas de GK de rechange sinon |
| Denis, Leroy, G. Bertin, Chevalier | remplaçants naturels | un par rôle | **Garder** |
Vendre pour financer un achat n'aurait pas de sens aujourd'hui : aucun achat conseillé, et un vendu hors saison = salaires en moins mais effectif plus mince avec 2 postes à 8. À rejuger à la fin de saison, quand les salaires sont revus pour la saison suivante [W:Finances] : relire alors Barros et Sundberg, qui auront 31 et 30 ans.

## Conseils suivis
C-009 ajouté dans `outputs/sixzeroleague/learnings.md` (aucun achat, aucune vente, revue à la fin de saison). Critère : `silver.sz_finances` (solde), `silver.sz_players` (15 joueurs), `silver.sz_transfer_listings`.

## Limites
- Marché de 6 annonces seulement (capture 06:51 UTC) ; si l'écran en montre plus, refaire l'export.
- Aucun prix de règlement en base : pas de prix de marché fiable, confiance faible sur toute estimation de prix.
- Compétences clés RW, LB 27 ans et RB : seules quelques-unes lues ; ces annonces sont de toute façon écartées sur la note.
- Hors poste : les notes de l'annonce sont au poste de l'annonce, comparables à nos notes au poste (`role_overalls` avant pénalité).
- Le skill ne dit pas si une enchère au-delà du solde est possible : non testé.

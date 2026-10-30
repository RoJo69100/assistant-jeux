---
name: derbymanager-club
description: Règles Derby Manager du club — finances (primes de victoire, récompenses, CC, stade basé sur l'affluence, sponsors, merch), plafond salarial et salaires, conseil d'administration et investissement, argent thésaurisé, installations (cible du conseil, +5 niveaux, dégradation −5 M, maintenance), transferts et enchères (85 jours, bonus du premier enchérisseur, enchère maximale, prime de signature, solidarity fee 5 %+5 %, libération), prix des joueurs, bots. À charger pour toute question d'argent, d'achat, de vente, de contrat ou d'investissement.
---

# Derby Manager — club (finances, transferts, installations)

Sources : `outputs/derbymanager/veille/connaissance.md` (2026-10-30). `dev` = développeur. Le plus récent l'emporte ; statut « confirmé » sauf mention.

## Revenus
- Sponsors versés le lundi selon les résultats ; diffusion monte avec la division — #discussion 2024-06-07, dev.
- Primes de victoire par division D4/D3/D2/D1 : 200 k / 300 k / 500 k / 800 k, moitié pour un nul, 1,2 M en NC et AC, 2 M en CC — #updates 2025-05-20, dev. En D4 : 200 k + ~120 k à domicile — #quick-questions 2026-10-03, dev.
- Fin de saison : 4 premiers de chaque division 20 M / 10 M / 5 M / 2,5 M ; pots NC 10 M, AC 10 M, CC 20 M — #updates 2025-05-20, dev.
- CC : 28 M pour 8 victoires (6 minimum pour la coupe) + ~3 M d'affluence par match ; 24 M pour les quarts — #discussion 2025-09-19, dev.
- **Stade (S13, 2025-07-02)** : revenu basé sur l'affluence, qui dépend des tiers des deux équipes ; prix de billets fixes par compétition ; recettes de coupe partagées ; jouer à l'extérieur contre un gros club rapporte plus — #updates 2025-07-02, dev ; #general 2026-01-01, dev.
- Exemples de billetterie : Everton 31 k contre Liverpool, ~8 k en moyenne (2026-08-03) ; l'écran Finances donne une estimation inexacte — #quick-questions 2026-08-03, dev ; #updates 2025-07-05, dev.
- Sponsors : 50 k par niveau d'installation de sponsor au lieu de 75 k (2026-08-24) ; plus de base de sponsoring — #updates 2026-08-24, dev. Peut relever le plafond des petites divisions de ≥ 100 k (2025-02-05).
- Merch : revenu réduit pour tous (2025-05-31) — #updates, dev — fait daté.
- Subvention IFA supprimée fin 2024 (primes de victoire à la place) ; le dev retire de l'argent aux bots riches (−33 % le 2025-02-18) — #france 2024-12-18 ; #discussion 2025-02-18, dev.
- Argent moyen visé 6-10 M par club ; moyennes par division (2026-08-23) : D1 9 M, D2 5 M, D3 9 M, D4 10 M ; médianes 5,5 / 3 / 2,5 / 9 M — #italy 2025-02-10, dev ; #discussion 2026-08-23, dev.
- Exemple D4 (2026-10-03) : 19 M en banque, 125 k sous le plafond, perte de 280 k/jour sans match — #quick-questions, dev — fait daté.
- Solde affiché arrondi dès 950 k — #italy 2024-10-28, dev.

## Plafond salarial et salaires
- Plafond = réputation de l'équipe + niveau de sponsoring ; monte avec la division ; promotion ⇒ plafond nettement plus haut + prime — #discussion 2024-07-15, dev ; #france 2024-10-27 / 2024-10-28, dev.
- **« Don't trust salary caps until Monday »** après un changement de saison (attente de la nouvelle saison déjà posée : D2 attente 3e = 120 %, D1 attente 12e = 105 %) — #updates 2025-05-24, dev ; #discussion 2025-08-02, dev.
- Au-dessus du plafond : aucune signature (sauf promotion de l'école) ni prolongation à salaire plus haut ; baisser est permis si le joueur accepte — #quick-questions 2024-12-03, dev ; #general 2025-01-02, dev.
- Après une relégation il faut vendre pour repasser sous le plafond — #italy 2024-12-04, dev.
- Salaire minimum 5 k ; paliers +2 k de 50 à 100 k puis +5 k — #general 2024-12-04, dev ; #updates 2026-08-13, dev.
- Salaires beaucoup plus hauts que dans DM1 — #discussion 2024-06-29, dev. Trophées ⇒ salaires demandés plus hauts (octobre 2026) — #inconnu 2026-10-19, dev.
- Plaintes salaire : un joueur se plaint s'il attend ~+50 % (jaune) ou le double (rouge) — #updates 2025-05-31, dev (à revérifier après S25).
- Un joueur trop payé réduit ses exigences en approchant la fin du contrat (40 k actuel / 20 k normal / 1 saison restante ⇒ ~30 k) — #updates 2024-10-02, dev.
- Salaire d'école : hors plafond, contre le revenu (2026-07-13, dev) ; des joueurs rapportent l'inverse depuis le 2026-08-21 — non tranché.
- Formule complète du plafond : inconnue.

## Conseil d'administration et installations
- Satisfaction du conseil : base 75 % = position égale à l'attente ; sous 50 % le risque monte ; attente basée sur la réputation — #updates 2024-06-28, dev.
- Le conseil investit quand le club est riche : si 20-50 M selon le tier, investissement au maximum tant que les installations peuvent monter (2025-09-08) ; « 38 M suffisent comme budget de transferts, ils investissent, cible niveau 29 » (2025-07-01) — #updates 2025-09-08, dev ; #italy 2025-07-01, dev.
- Avant 2025-08-12 le conseil investissait aussi l'argent en banque : supprimé — #england 2025-08-12, dev.
- Installations = « banque » (2025-06-02) : au-dessus de 100 % d'investissement l'argent entre dans les installations (perdu pour les transferts) — #updates 2025-06-02, dev.
- **Plafond d'amélioration : 5 niveaux au-dessus de l'attente du conseil (2025-08-13)** ; meilleure catégorie ≤ 2 étoiles au-dessus de la pire — #updates 2025-08-13, dev.
- Choix de l'installation : possible quand il manque ≤ 1 M (puis 2,5 M, puis tout montant) — #updates 2024-11-26 / 2025-06-02, dev.
- Maintenance : ne dépend que des installations (pas du tier) depuis 2025-05-20 ; en manque d'argent le conseil réduit la maintenance ; stade à 100 % = −300 k/jour (exemple 2025-06-03) — #updates 2025-05-20, dev ; #discussion 2025-06-03, dev.
- **Dégradation : une installation perd un niveau à −5 M quel que soit son niveau** ; le bâtiment qui régresse est aléatoire ; on rachète au même prix en vendant un joueur ; limitée à 25 % — #updates 2026-08-24, dev ; #france 2025-11-11, dev ; #quick-questions 2026-08-03, dev.
- Niveaux « appropriés » par division (estimation 2025-07-06, 2 équipes) : D4 10-16, D3 16-22, D2 22-28, D1 28-34, Europe 34-40 — #quick-questions, dev — en doute. Exemple : niveau 13 approprié, 19 trop haut (2025-05-21).
- Coût : +1 point d'installation ≈ 12 M (2025-07-18) — #discussion, dev.
- Argent thésaurisé : seuil annoncé « tier × 5 M » (50 M pour le meilleur club), brand recognition au-dessus de « tier × 20 000 » (200 M), baisse prévue vers ~50 M sans date ; Soyaux 255 M en D3 — #discussion 2026-07-21, dev ; #updates 2026-07-23, dev.
- Promouvoir un vieux joueur en staff : chaque point de mentor = 1 M d'installations — #updates 2025-07-17, dev.
- Avis du développeur : « You really can do everything you need with what you already have » — #discussion 2025-05-21, dev. En D4 avec > 25 M, viser D3 et la réputation — #france 2025-05-22, dev.

## Transferts et enchères
- Pas de fenêtres de transferts ; transferts plus rapides hors saison ; plus de ralentissement de fin de saison depuis 2025-09-08 — #general 2024-06-07, dev ; #updates 2025-09-08, dev.
- **Mise en vente : moins de 85 jours de contrat** (strictement) ; pas de limite de joueurs listés tant qu'il reste ≥ 18 non listés — #updates 2025-09-08, dev ; #discussion 2025-10-17, dev.
- Plus un joueur reste listé, plus il a de chances d'une offre de bot — #updates 2026-01-04, dev. Se vend : GK facilement, M et D ≥ 2-4 M, F ≥ 4 M ; sous 1 M dur — joueurs 2026-06-15 — complété.
- Décision du joueur : « at most 2.5 days » ; offre dans la journée ⇒ souvent présent pour le match du lendemain — #discussion 2026-04-11, dev.
- **Les joueurs préfèrent l'équipe qui a offert plus tôt** : bonus ≈ +200 k pour une offre immédiate, +199 k 10 min plus tard ; une offre au maximum posée en premier ne peut plus être battue ; on ne peut pas annuler une offre — #quick-questions 2026-08-20 / 2026-09-04, dev.
- Enchère aveugle mais participants publics ; il faut avoir scouté au moins une fois pour enchérir — #england 2026-07-10, dev ; #updates 2025-06-18, dev.
- À la 4e offre, si la décision tombe dans quelques jours, la 3e meilleure est rejetée ; si la décision tombe dans la journée, toutes restent — #updates 2025-09-08, dev.
- Seul l'extra au-dessus de la base compte ; ne jamais offrir plus de statut que nécessaire ; « offrir un peu plus » ; attentes ≈ 5-25 k au-dessus du minimum ; vert = signe n'importe quelle offre — #updates 2024-06-21, dev ; #general 2024-12-11, dev ; #quick-questions 2026-10-03, dev.
- **Prime de signature** : 0 pour un joueur de son pays, 500 k minimum pour une autre région ; « 1 k de salaire = 100 k de prime » ; +35 k de salaire ⇒ +3,5 M de frais — #quick-questions 2026-07-09, dev ; #general 2026-09-01, dev.
- **Solidarity fee (2026-09-06)** : 5 % à l'équipe formatrice + 5 % au joueur (10 % au joueur avant) ; prolongation = 5 % joueur seulement ; bug jusqu'au 2026-09-13 corrigé — #updates 2026-09-06, dev ; #quick-questions 2026-09-13, dev.
- Libération gratuite : moins de 70 jours de contrat et valeur sous un seuil du conseil (≈ 2-5 M selon le tier depuis 2025-08-13) ; bouton rouge dans l'écran de contrat ; coût du contrat restant (≈ 25 %, joueur furysk 2026-08-15) — #updates 2025-08-13, dev ; #quick-questions 2025-10-21, dev.
- Joueur libre : prix de départ = son prix, baisse jusqu'à 10-15 % sur ~1 mois, gros signing fee — #discussion 2024-06-04, dev ; #updates 2024-07-16, dev.
- Contrat expiré : le joueur reste, transfer-listé, très mécontent, 0 entraînement, prix −10-15 %, annulé en fin de saison — #updates 2024-07-16, dev ; #discussion 2025-04-14, dev.
- Pas de revente 3 M ⇒ 30 M ; on ne fixe pas le prix de vente — #discussion 2024-06-04, dev.
- Bots : achètent selon leur argent, peuvent s'endetter, prennent des 25-27 ans, ne tirent pas de l'école les joueurs sous 2 M ; bots à court d'argent en 2026-09 (15-20 M dur à vendre) — #discussion 2024-06-29 ; #general 2025-11-07, dev ; joueur faro1 2026-09-16.
- Conseils du développeur : « there are no bargains, prices correlate to quality », prendre les 10 plus chers abordables ; « buy yourself the most expensive player from the market » sous le plafond ; mercato petit club : vendre 7-8, acheter 3-4 de 26-29 ans à 3-4 M ; remplacer d'abord les contrats qui expirent — #general 2026-02-07 ; #inconnu 2026-10-14 ; #france 2025-05-03 ; #general 2025-01-02, dev.
- Pas d'avertissement du conseil si l'on achète en liquide — #quick-questions 2026-09-28, dev.

## Prix des joueurs
- Le prix suit les compétences (« direct correlation ») ; potentiel et natural fitness valorisés, club fit et expérience moins (2024-08-31) ; performance = bonus fixe (2025-04-23) ; plus de buffer de prix (2025-05-12) — #updates, dev.
- Performance modifier : 7,0 ⇒ 7,05 ⇒ 7,0 ; bouge de 0,1-0,2 par match — #discussion 2025-05-12, dev.
- **Courbe > 30 M : « 1, 3, 6, 12, 20, 30, 40, 48, 54, 57 », plafond 60 M (2026-05-10)**, remplace « 1, 2, 6, 12, 20, 30, 42, 56, 72, 90 » — #updates 2026-05-10, dev.
- Plus dur de gonfler le prix des GK et F (2026-01-03) ; il n'y a pas de « vraie valeur » (#italy 2025-05-08).
- Un 3 M et un 4 M peuvent être identiques ; seul l'écart 15 M contre 3 M est fiable — #quick-questions 2025-04-19, dev.
- Un promu de l'école a un prix plus bas (pas de multiplicateur de performance) — #quick-questions 2026-08-15, dev.

## Pièges
- Ne jamais lire le plafond salarial le jour du changement de saison : attendre le lundi.
- Une enchère maximale posée en premier est imbattable : la poser tout de suite si le joueur est visé.
- Un joueur listé depuis moins de 24 h ne supprime pas son insatisfaction.
- Dépasser le plafond bloque les signatures mais pas les promotions de l'école.
- Le conseil perd des niveaux d'installations quand l'argent manque (−5 M par niveau) : ne pas vider la caisse.
- Étiquette des 200/300/500/800 k (prime de victoire ou droits TV) en doute : ne pas additionner les deux.
- Seuil de libération gratuite exprimé en valeur du joueur et en tier : vérifier le bouton rouge avant de compter dessus.
- L'achat de jeunes entre joueurs est interdit (patch) — #quick-questions 2026-08-16, dev.

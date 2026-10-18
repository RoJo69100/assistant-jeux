# Checklist SixZero League (handball)

Adaptée de la checklist BasketVibe le 2026-10-18 (2e jeu, banc d'essai du kit multi-jeux). Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur. Spécificités : pas de Discord, cycle du jeu = 2 journées de ligue, pas de personnel ni de forme, infrastructures et sponsor à choisir, académie U18.

## A. Fondations
- [x] Dépôt, Supabase, MCP, tables bronze communs avec BasketVibe (vérifié le 2026-10-18 : `bronze.raw_pages`, `game = 'sixzeroleague'`)
- [x] Script Tampermonkey `userscripts/sixzeroleague.user.js` installé et configuré (vérifié le 2026-10-18 : version 0.1.2, captures API JSON + copie de page, wiki complet reçu)

## B. Collecte
- [x] Effectif et fiche joueur (20 compétences, âge, taille, main, éthique, salaire) → bronze (vérifié le 2026-10-18 : 12 joueurs, compétences, progression fractionnaire, note par rôle)
- [x] Tactique : composition par défaut, remplaçants par rôle, formations → bronze (vérifié le 2026-10-18 : 7 titulaires, 2 remplaçants, 5-1 / 6-0)
- [x] Entraînement : intensité, focus par joueur, rapport, formation de rôle → bronze (vérifié le 2026-10-18 : intensité Normal, 12 focus, rapport de 9 progrès, 1 emplacement de rôle)
- [ ] Match : score, rapport, statistiques, incidents (après le 1er match de la saison) → bronze
- [x] Compétitions : classement, calendrier, coupe → bronze (vérifié le 2026-10-18 : ligue Vanadium, 5e division, 10 clubs, 90 matchs dont 18 pour nous ; coupe capturée)
- [x] Marché des transferts et joueur en vente → bronze (vérifié le 2026-10-18 : 23 annonces avec compétences)
- [x] Finances, rapport hebdomadaire, offres de sponsor → bronze (vérifié le 2026-10-18 : solde, prévision, dernier rapport, 3 offres, sponsor actuel)
- [x] Infrastructures (4 installations, niveaux, coûts, remboursement) → bronze (vérifié le 2026-10-18 : 4 installations, 20 niveaux chacune avec effet, entretien et coût)
- [x] Académie U18 (2 prospects, compétences dévoilées) → bronze (vérifié le 2026-10-18 : pas de prospect disponible, prochain choix dans 5 journées)
- [x] Wiki du jeu (15 rubriques) → bronze (vérifié le 2026-10-18)

## C. Modèle de données
- [ ] Silver : joueurs + relevé par cycle d'entraînement (compétences, blessures)
- [ ] Silver : matchs, stats par joueur, incidents
- [x] Silver : classement, calendrier, marché, finances, infrastructures, académie (vérifié le 2026-10-18 : sql/silver/010_sz_base.sql)
- [ ] Gold : bilan par rôle (note, compétences clés du rôle, âge, salaire, profondeur)
- [ ] Gold : progression par cycle d'entraînement (points gagnés par joueur et compétence)
- [ ] Gold : résultat financier par cycle et projection de fin de saison
- [ ] Gold : rentabilité des infrastructures (semaines de remboursement)

## D. Skills
- [x] Règles écrites depuis le wiki officiel (4 skills `sixzeroleague-*`, chaque fait sourcé [W:Rubrique]) (validé par l'utilisateur le 2026-10-18 : « je te fais confiance pour les règles »)
- ~~10 questions de règles testées par l'utilisateur~~ (retirée le 2026-10-18 à la demande de l'utilisateur : pas de test des règles pour ce jeu)

## E. Agents (globaux, avec la fiche du jeu)
- [ ] Fiche du jeu pour les agents (skills, vues gold, spécificités)
- [ ] Effectif : bilan par rôle, meilleurs et moins bons joueurs, 3 actions
- [ ] Tactique : composition par défaut et remplaçants par rôle, prêts à saisir
- [ ] Match : explication de chaque match, chiffres à l'appui, journal des enseignements
- [ ] Entraînement : intensité et focus par joueur, verdict à chaque cycle
- [ ] Transferts : intérêt, prix, enchère ; joueurs à vendre
- [ ] Finances : alerte, masse salariale, choix du sponsor
- [ ] Infrastructures : quelle installation améliorer et quand (remboursement)
- [ ] Académie U18 : quel prospect signer, quand monter l'académie

## F. Routine
- [ ] Wiki de synthèse : routine, priorités, âges clés, profil par rôle
- [ ] « Que faire aujourd'hui » et brief du matin pour SixZero League

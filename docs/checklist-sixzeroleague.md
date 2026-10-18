# Checklist SixZero League (handball)

Adaptée de la checklist BasketVibe le 2026-10-18 (2e jeu, banc d'essai du kit multi-jeux). Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur. Spécificités : pas de Discord, cycle du jeu = 2 journées de ligue, pas de personnel ni de forme, infrastructures et sponsor à choisir, académie U18.

## A. Fondations
- [x] Dépôt, Supabase, MCP, tables bronze communs avec BasketVibe (vérifié le 2026-10-18 : `bronze.raw_pages`, `game = 'sixzeroleague'`)
- [x] Script Tampermonkey `userscripts/sixzeroleague.user.js` installé et configuré (vérifié le 2026-10-18 : version 0.1.2, captures API JSON + copie de page, wiki complet reçu)

## B. Collecte
- [ ] Effectif et fiche joueur (20 compétences, âge, taille, main, éthique, salaire) → bronze
- [ ] Tactique : composition par défaut, remplaçants par rôle, formations → bronze
- [ ] Entraînement : intensité, focus par joueur, rapport, formation de rôle → bronze
- [ ] Match : score, rapport, statistiques, incidents (après le 1er match de la saison) → bronze
- [ ] Compétitions : classement, calendrier, coupe → bronze
- [ ] Marché des transferts et joueur en vente → bronze
- [ ] Finances, rapport hebdomadaire, offres de sponsor → bronze
- [ ] Infrastructures (4 installations, niveaux, coûts, remboursement) → bronze
- [ ] Académie U18 (2 prospects, compétences dévoilées) → bronze
- [x] Wiki du jeu (15 rubriques) → bronze (vérifié le 2026-10-18)

## C. Modèle de données
- [ ] Silver : joueurs + relevé par cycle d'entraînement (compétences, blessures)
- [ ] Silver : matchs, stats par joueur, incidents
- [ ] Silver : classement, calendrier, marché, finances, infrastructures, académie
- [ ] Gold : bilan par rôle (note, compétences clés du rôle, âge, salaire, profondeur)
- [ ] Gold : progression par cycle d'entraînement (points gagnés par joueur et compétence)
- [ ] Gold : résultat financier par cycle et projection de fin de saison
- [ ] Gold : rentabilité des infrastructures (semaines de remboursement)

## D. Skills
- [ ] Règles écrites depuis le wiki officiel (4 skills `sixzeroleague-*`, chaque fait sourcé [W:Rubrique]) — écrits le 2026-10-18, à valider
- [ ] 10 questions de règles testées par l'utilisateur : 10 réponses justes

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

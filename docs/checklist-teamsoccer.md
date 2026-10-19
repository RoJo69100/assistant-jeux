# Checklist Team Soccer (football)

Adaptée de la checklist SixZero League le 2026-10-19 (3e jeu du kit multi-jeux). Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur. Spécificités : **deux clubs** sur le compte (équipe première et équipe féminine Ben Ahmed Donkey, économies séparées) ; pas de Discord mais un forum ; rythme hebdomadaire (2 matchs de ligue mardi et samedi, entraînement le vendredi, finances le lundi) ; la **Forme** et l'intensité d'entraînement sont l'arbitrage central ; pas de sponsor ni d'infrastructure autre que le stade et l'entraîneur ; académie à révélations quotidiennes ; règles qui changent souvent (surveiller les annonces).

## A. Fondations
- [x] Dépôt, Supabase, MCP, tables bronze communes (vérifié le 2026-10-19 : `bronze.raw_pages`, `game = 'teamsoccer'`, index unique sur md5(source_url), `sql/bronze/004`)
- [x] Script Tampermonkey `userscripts/teamsoccer.user.js` installé (vérifié le 2026-10-19 : version 0.1.1, capture des réponses de l'API `/rest/v1/` + texte de la page, envoi par paquets)

## B. Collecte (pour les deux clubs)
- [x] Effectif et fiche joueur (10 compétences, OVR, poste, Forme, talent, valeur, salaire, blessure, suspension) → bronze (vérifié le 2026-10-19 : `players` avec `fitness`, `form`, `value`, `wage`)
- [x] Entraînement : compétence et intensité par joueur, progression, niveau d'entraîneur → bronze (vérifié le 2026-10-19 : `player_training_assignments`, page Entraînement)
- [x] Matchs : calendrier, composition, consignes, résultat → bronze (vérifié le 2026-10-19 : `matches`, `lineups`, `match_lineups`, 41 captures de pages de match)
- [ ] Rapport de match détaillé : notes 0–10, secteurs, événements, affluence (à vérifier après le prochain match officiel)
- [x] Compétitions : classement, coupes, statistiques → bronze (vérifié le 2026-10-19 : `series`, `cup_participants`, `cup_tournaments`, `player_league_stats_per_match`)
- [x] Marché des transferts → bronze (vérifié le 2026-10-19 : `transfer_listings`, ~55 annonces)
- [x] Finances et stade → bronze (vérifié le 2026-10-19 : `team_finances`, `stadiums`, pages Finances et Stade)
- [x] Académie et Haute Performance → bronze (vérifié le 2026-10-19 : `youth_academy_players` avec `revealed_skills`, `high_performance_scouts`)
- [x] Guide du jeu et forum → bronze (vérifié le 2026-10-19 : guide de 50 558 caractères ; 881 messages avec contenu)
- [ ] Compléments : réponses de la FAQ du guide (repliées, non captées) et 13 annonces dont seul le titre est en base (liste dans le skill `teamsoccer-communaute`)
- [ ] Page Statistiques du club : les 5 cercles de constance du manager (MC)

## C. Modèle de données
- [ ] Silver : joueurs + relevé hebdomadaire après l'entraînement du vendredi (compétences, Forme, valeur, salaire), par club
- [ ] Silver : matchs, compositions et consignes, notes par joueur, secteurs
- [ ] Silver : classement, calendrier, coupes, marché, finances, stade, académie
- [ ] Gold : bilan par poste naturel (sous-rôle, OVR, Forme, âge, valeur, salaire, profondeur du banc)
- [ ] Gold : progression par séance d'entraînement (gain par joueur et compétence selon âge et intensité, variation de Forme)
- [ ] Gold : résultat financier par semaine et projection de fin de saison (salaires, entretien, billetterie, primes), alerte solde négatif
- [ ] Gold : rentabilité du stade (matchs pour rembourser chaque type de place selon division et rang)
- [ ] Gold : académie (jeunes, compétences révélées, révélations du jour à faire)

## D. Skills
- [ ] Règles écrites depuis le guide et le forum (6 skills `teamsoccer-*` : joueurs, match, entrainement, club, saison, communaute ; chaque fait sourcé [G], [F], [P] ou [Obs]) (écrits le 2026-10-19 ; à valider par l'utilisateur)
- [ ] Points incertains tranchés par nos données : formule de l'OVR par sous-rôle, valeur et salaire, Forme au changement de saison, ampleur du style d'équipe

## E. Agents (globaux, avec la fiche du jeu)
- [ ] Fiche du jeu pour les agents (`docs/fiches/teamsoccer/` : commun + 8 domaines, skills et vues citées présents)
- [ ] Effectif : bilan par poste, meilleurs et moins bons joueurs, 3 actions, pour chaque club
- [ ] Tactique : formation, style, consignes, banc et remplacements prêts à saisir, selon la Forme et l'adversaire
- [ ] Match : explication de chaque match, chiffres à l'appui, journal des enseignements
- [ ] Entraînement : compétence et intensité par joueur, verdict chaque vendredi, gestion de la Forme
- [ ] Transferts : intérêt, prix, enchère ; joueurs à vendre (banque ou enchère), en tenant compte de la limite d'un achat par semaine
- [ ] Finances : alerte, masse salariale, retour à un solde positif, niveau d'entraîneur
- [ ] Stade : quelles places acheter et quand (remboursement)
- [ ] Académie : quelles compétences révéler chaque jour, quel jeune monter, vendre ou libérer
- [ ] Veille : nouvelles annonces et messages des admins depuis le dernier passage, propositions de mise à jour des skills

## F. Routine
- [ ] Wiki de synthèse : routine de la semaine, priorités, âges clés, profil par poste
- [ ] « Que faire ce soir » pour Team Soccer (skill `teamsoccer-aujourdhui`, agenda et alertes du jour : composition à enregistrer 2 h avant, révélations d'académie, amical de la semaine, contrôle de l'entretien le lundi)

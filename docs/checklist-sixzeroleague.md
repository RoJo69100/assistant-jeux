# Checklist SixZero League (handball)

Adaptée de la checklist BasketVibe le 2026-10-18 (2e jeu, banc d'essai du kit multi-jeux). Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur. Spécificités : pas de Discord, cycle du jeu = 2 journées de ligue, pas de personnel ni de forme, infrastructures et sponsor à choisir, académie U18.

## A. Fondations
- [x] Dépôt, Supabase, MCP, tables bronze communs avec BasketVibe (vérifié le 2026-10-18 : `bronze.raw_pages`, `game = 'sixzeroleague'`)
- [x] Script Tampermonkey `userscripts/sixzeroleague.user.js` installé et configuré (vérifié le 2026-10-18 : version 0.1.2, captures API JSON + copie de page, wiki complet reçu)

## B. Collecte
- [x] Effectif et fiche joueur (20 compétences, âge, taille, main, éthique, salaire) → bronze (vérifié le 2026-10-18 : 12 joueurs, compétences, progression fractionnaire, note par rôle)
- [x] Tactique : composition par défaut, remplaçants par rôle, formations → bronze (vérifié le 2026-10-18 : 7 titulaires, 2 remplaçants, 5-1 / 6-0)
- [x] Entraînement : intensité, focus par joueur, rapport, formation de rôle → bronze (vérifié le 2026-10-18 : intensité Normal, 12 focus, rapport de 9 progrès, 1 emplacement de rôle)
- [x] Match : score, rapport, statistiques, incidents (après le 1er match de la saison) → bronze (vérifié le 2026-10-19 : `/matches/<id>/stats`, journée 1, 27-26 contre voleibol aljarafe)
- [x] Compétitions : classement, calendrier, coupe → bronze (vérifié le 2026-10-18 : ligue Vanadium, 5e division, 10 clubs, 90 matchs dont 18 pour nous ; coupe capturée)
- [x] Marché des transferts et joueur en vente → bronze (vérifié le 2026-10-18 : 23 annonces avec compétences)
- [x] Finances, rapport hebdomadaire, offres de sponsor → bronze (vérifié le 2026-10-18 : solde, prévision, dernier rapport, 3 offres, sponsor actuel)
- [x] Infrastructures (4 installations, niveaux, coûts, remboursement) → bronze (vérifié le 2026-10-18 : 4 installations, 20 niveaux chacune avec effet, entretien et coût)
- [x] Académie U18 (2 prospects, compétences dévoilées) → bronze (vérifié le 2026-10-18 : pas de prospect disponible, prochain choix dans 5 journées)
- [x] Wiki du jeu (15 rubriques) → bronze (vérifié le 2026-10-18)

## C. Modèle de données
- [x] Silver : joueurs + relevé par cycle d'entraînement (compétences, blessures) (vérifié le 2026-10-19 : `sz_player_cycles`, `sz_training_changes` par `applied_at`, `sql/gold/014_sz_cycles.sql`)
- [x] Silver : matchs, stats par joueur, incidents (vérifié le 2026-10-19 : `sz_matches`, `sz_match_players`, `sz_match_incidents`, `sql/silver/011_sz_matches.sql`)
- [x] Silver : classement, calendrier, marché, finances, infrastructures, académie (vérifié le 2026-10-18 : sql/silver/010_sz_base.sql)
- [x] Gold : bilan par rôle (note, compétences clés du rôle, âge, salaire, profondeur) (vérifié le 2026-10-19 : `gold.sz_role_report`, 12 lignes, RB et LW sans remplaçant naturel)
- [x] Gold : progression par cycle d'entraînement (points gagnés par joueur et compétence) (vérifié le 2026-10-19 : `gold.sz_training_progress`, cycle 9, 9 joueurs)
- [x] Gold : résultat financier par cycle et projection de fin de saison (vérifié le 2026-10-19 : `gold.sz_finance_cycles`, `gold.sz_finance_projection`)
- [x] Gold : rentabilité des infrastructures (semaines de remboursement) (vérifié le 2026-10-18 : gold.sz_infrastructure_payback, Arena et Fan Shop, 4 niveaux au-dessus de l'actuel)

## D. Skills
- [x] Règles écrites depuis le wiki officiel (4 skills `sixzeroleague-*`, chaque fait sourcé [W:Rubrique]) (validé par l'utilisateur le 2026-10-18 : « je te fais confiance pour les règles »)
- ~~10 questions de règles testées par l'utilisateur~~ (retirée le 2026-10-18 à la demande de l'utilisateur : pas de test des règles pour ce jeu)

## E. Agents (globaux, avec la fiche du jeu)
- [x] Fiche du jeu pour les agents (skills, vues gold, spécificités) (vérifié le 2026-10-19 : docs/fiches/sixzeroleague/, commun + 8 domaines, 15 vues citées présentes en base, skills cités présents)
- [x] Effectif : bilan par rôle, meilleurs et moins bons joueurs, 3 actions (brief `outputs/sixzeroleague/briefs/2026-10-20-effectif.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Tactique : composition par défaut et remplaçants par rôle, prêts à saisir (brief `outputs/sixzeroleague/briefs/2026-10-20-tactique.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Match : explication de chaque match, chiffres à l'appui, journal des enseignements (brief `outputs/sixzeroleague/briefs/2026-10-20-match.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Entraînement : intensité et focus par joueur, verdict à chaque cycle (brief `outputs/sixzeroleague/briefs/2026-10-20-entrainement.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Transferts : intérêt, prix, enchère ; joueurs à vendre (brief `outputs/sixzeroleague/briefs/2026-10-20-transferts.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Finances : alerte, masse salariale, choix du sponsor (brief `outputs/sixzeroleague/briefs/2026-10-20-finances.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Infrastructures : quelle installation améliorer et quand (remboursement) (brief `outputs/sixzeroleague/briefs/2026-10-20-finances.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)
- [x] Académie U18 : quel prospect signer, quand monter l'académie (brief `outputs/sixzeroleague/briefs/2026-10-20-academie.md` ; validé par l'utilisateur le 2026-10-20, retours à venir)

## F. Routine
- [x] Wiki de synthèse : routine, priorités, âges clés, profil par rôle (écrit le 2026-10-20 : `outputs/sixzeroleague/wiki/` 5 pages ; validé par l'utilisateur le 2026-10-20)
- [ ] « Que faire aujourd'hui » et brief du matin pour SixZero League (fait le 2026-10-19 : skill `sixzeroleague-aujourdhui`, `gold.sz_agenda`, `gold.sz_daily_alerts` ; à valider par l'utilisateur)

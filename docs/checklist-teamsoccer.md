# Checklist Team Soccer (football)

Adaptée de la checklist SixZero League le 2026-10-19 (3e jeu du kit multi-jeux). Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur. Spécificités : **deux clubs** sur le compte (équipe première et équipe féminine Ben Ahmed Donkey, économies séparées) ; pas de Discord mais un forum ; rythme hebdomadaire (2 matchs de ligue mardi et samedi, entraînement le vendredi, finances le lundi) ; la **Forme** et l'intensité d'entraînement sont l'arbitrage central ; pas de sponsor ni d'infrastructure autre que le stade et l'entraîneur ; académie à révélations quotidiennes ; règles qui changent souvent (surveiller les annonces).

## A. Fondations
- [x] Dépôt, Supabase, MCP, tables bronze communes (vérifié le 2026-10-19 : `bronze.raw_pages`, `game = 'teamsoccer'`, index unique sur md5(source_url), `sql/bronze/004`)
- [x] Script Tampermonkey `userscripts/teamsoccer.user.js` installé (vérifié le 2026-10-19 : version 0.1.1, capture des réponses de l'API `/rest/v1/` + texte de la page, envoi par paquets)

## B. Collecte (pour les deux clubs)
- [x] Effectif et fiche joueur (10 compétences, OVR, poste, Forme, talent, valeur, salaire, blessure, suspension) → bronze (vérifié le 2026-10-19 : `players` avec `fitness`, `form`, `value`, `wage`)
- [x] Entraînement : compétence et intensité par joueur, progression, niveau d'entraîneur → bronze (vérifié le 2026-10-19 : `player_training_assignments`, page Entraînement)
- [x] Matchs : calendrier, composition, consignes, résultat → bronze (vérifié le 2026-10-19 : `matches`, `lineups`, `match_lineups`, 41 captures de pages de match)
- [x] Rapport de match détaillé : notes 0–10, secteurs, événements, affluence (vérifié le 2026-10-19 : page `match-viewer`, `match_replays` 100 à 127 événements par match + HTML notes et secteurs, 5 matchs de ligue)
- [x] Compétitions : classement, coupes, statistiques → bronze (vérifié le 2026-10-19 : `series`, `cup_participants`, `cup_tournaments`, `player_league_stats_per_match`)
- [x] Marché des transferts → bronze (vérifié le 2026-10-19 : `transfer_listings`, ~55 annonces)
- [x] Finances et stade → bronze (vérifié le 2026-10-19 : `team_finances`, `stadiums`, pages Finances et Stade)
- [x] Académie et Haute Performance → bronze (vérifié le 2026-10-19 : `youth_academy_players` avec `revealed_skills`, `high_performance_scouts`)
- [x] Guide du jeu et forum → bronze (vérifié le 2026-10-19 : guide de 50 558 caractères ; 881 messages avec contenu)
- [x] Compléments : réponses de la FAQ du guide (repliées, non captées) et 13 annonces dont seul le titre est en base (liste dans le skill `teamsoccer-communaute`) (vérifié le 2026-10-19 : 20 annonces avec contenu, `silver.ts_news` ; FAQ en bronze `dashboard_help` et `samples/teamsoccerfaq.txt`, lue par la veille)
- [ ] Page Statistiques du club : les 5 cercles de constance du manager (MC)

## C. Modèle de données
- [x] Silver : joueurs + relevé hebdomadaire après l'entraînement du vendredi (compétences, Forme, valeur, salaire), par club (vérifié le 2026-10-19 : `silver.ts_player_snapshots` un relevé par joueur et par jour, `ts_players` 23 + 22 joueurs, `sql/silver/012`)
- [x] Silver : matchs, compositions et consignes, notes par joueur, secteurs (vérifié le 2026-10-19 : `ts_matches`, `ts_match_lineups`, `ts_lineups`, `ts_match_events`, `ts_match_ratings` 22 notes par match, `ts_match_sectors` 9 zones, `sql/silver/013` ; gold `ts_match_report`, `ts_match_plays`, `ts_player_match_ratings`, `sql/gold/017`)
- [x] Silver : classement, calendrier, coupes, marché, finances, stade, académie (vérifié le 2026-10-19 : `ts_standings` recalculé, `ts_matches` par compétition, `ts_transfer_listings` 72 annonces, `ts_finances`, `ts_stadiums`, `ts_youth_players` 2 × 16, `ts_hpc`)
- [x] Gold : bilan par poste naturel (sous-rôle, OVR, Forme, âge, valeur, salaire, profondeur du banc) (vérifié le 2026-10-19 : `gold.ts_squad_report` par zone ; sous-rôle indicatif via `second_skill`)
- [ ] Gold : progression par séance d'entraînement (gain par joueur et compétence selon âge et intensité, variation de Forme) (vue `gold.ts_player_progress` créée le 2026-10-19 ; à vérifier au 2e relevé, après le vendredi)
- [x] Gold : résultat financier par semaine et projection de fin de saison (salaires, entretien, billetterie, primes), alerte solde négatif (vérifié le 2026-10-19 : `gold.ts_finance_status` ; salaires et entretien recalculés = lignes du jeu, écart 0 ; primes non comptées)
- [x] Gold : rentabilité du stade (matchs pour rembourser chaque type de place selon division et rang) (vérifié le 2026-10-19 : `gold.ts_stadium_payback`)
- [x] Gold : académie (jeunes, compétences révélées, révélations du jour à faire) (vérifié le 2026-10-19 : `gold.ts_academy`, plus `gold.ts_hpc_status` et `gold.ts_upcoming`)

## D. Skills
- [x] Règles écrites depuis le guide et le forum (6 skills `teamsoccer-*` : joueurs, match, entrainement, club, saison, communaute ; chaque fait sourcé [G], [F], [P] ou [Obs]) (validés par l'utilisateur le 2026-10-19)
- [ ] Points incertains tranchés par nos données : formule de l'OVR par sous-rôle, valeur et salaire, Forme au changement de saison, ampleur du style d'équipe

## E. Agents (globaux, avec la fiche du jeu)
- [x] Fiche du jeu pour les agents (`docs/fiches/teamsoccer/` : commun + 8 domaines, skills et vues citées présents) (vérifié le 2026-10-19 : 9 fiches, toutes les vues citées existent en base)
- [ ] Effectif : bilan par poste, meilleurs et moins bons joueurs, 3 actions, pour chaque club
- [ ] Tactique : formation, style, consignes, banc et remplacements prêts à saisir, selon la Forme et l'adversaire
- [x] Match : explication de chaque match, chiffres à l'appui, journal des enseignements (vérifié le 2026-10-19 : 5 matchs de ligue expliqués, `outputs/teamsoccer/learnings.md` L-001 à L-010, C-001 à C-008)
- [ ] Entraînement : compétence et intensité par joueur, verdict chaque vendredi, gestion de la Forme
- [ ] Transferts : intérêt, prix, enchère ; joueurs à vendre (banque ou enchère), en tenant compte de la limite d'un achat par semaine
- [ ] Finances : alerte, masse salariale, retour à un solde positif, niveau d'entraîneur
- [ ] Stade : quelles places acheter et quand (remboursement)
- [ ] Académie : quelles compétences révéler chaque jour, quel jeune monter, vendre ou libérer
- [x] Veille : nouvelles annonces et messages des admins depuis le dernier passage, propositions de mise à jour des skills (vérifié le 2026-10-19 : 20 annonces, 13 messages, FAQ → 12 propositions dont 3 contradictions, `outputs/teamsoccer/veille/2026-10-19.md`)

## F. Routine
- [ ] Wiki de synthèse : routine de la semaine, priorités, âges clés, profil par poste
- [ ] « Que faire ce soir » pour Team Soccer (skill `teamsoccer-aujourdhui`, agenda et alertes du jour : composition à enregistrer 2 h avant, révélations d'académie, amical de la semaine, contrôle de l'entretien le lundi)

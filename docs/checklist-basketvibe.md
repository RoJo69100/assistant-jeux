# Checklist BasketVibe (49 cases)

Le travail est terminé quand tout est coché. Parties D à F : chaque case est un test validé par l'utilisateur.

## A. Fondations
- [ ] Dépôt GitHub privé créé, cloné sur les 2 PC, `CLAUDE.md` en place
- [x] Projet Supabase créé, clés dans `.env` non versionné (vérifié le 2026-10-16)
- [x] Serveur MCP Supabase branché dans Claude Code (vérifié le 2026-10-16)
- [x] Tables bronze créées (JSON brut + jeu + type de page + date) (vérifié le 2026-10-16)

## B. Collecte (script Tampermonkey BasketVibe)
- [x] Effectif → bronze (vérifié le 2026-10-16 : 15 joueurs via /api/v1/teams/…/overview)
- [x] Fiche joueur, avec l'historique d'entraînement → bronze (vérifié le 2026-10-16 : season-profile, training-history, training, recent-runs)
- [x] Match : score, box score, play-by-play, tactique jouée → bronze (vérifié le 2026-10-16 : 2 matchs, period-box 1-4, play-by-play, match-tactics-used)
- [x] Tactique et depth chart actuels → bronze (vérifié le 2026-10-16 : /teams/…/tactics + onglet depth)
- [x] Marché des transferts et fiche d'un joueur listé → bronze (vérifié le 2026-10-16 : transfer-auctions, historiques, records, fiche joueur en vente avec transfer-auction)
- [x] Finances → bronze (vérifié le 2026-10-16 : finance + sponsor)
- [x] Personnel → bronze (vérifié le 2026-10-16)
- [x] Académie (rapport du scout) → bronze (vérifié le 2026-10-16 : 3 candidats, rapport du 2026-10-15)
- [x] Classement et calendrier → bronze (vérifié le 2026-10-16 : standings 12 équipes, fixtures 132 matchs)
- [x] Discord BasketVibe → bronze (export hebdomadaire) (vérifié le 2026-10-16 : 2 624 messages, 13 salons ; 2e export à tester semaine du 2026-10-23)

## C. Modèle de données
- [x] Silver : joueurs + photo hebdomadaire (lundi matin) de leurs skills, forme, fatigue (vérifié le 2026-10-16 : silver.bv_player_weekly, 15 joueurs, skills précis ; 2e semaine confirmée le 2026-10-18 : semaines du 11/10 et du 18/10, calées sur l'entraînement du dimanche)
- [x] Silver : matchs, stats par joueur, événements du play-by-play (vérifié le 2026-10-16 : 2 matchs, somme des quart-temps = score final = fin du play-by-play)
- [x] Silver : marché, finances, personnel, académie, classement (vérifié le 2026-10-16 : bilan de saison recalculé = solde du jeu, 102 matchs joués = 17 journées × 6)
- [x] Gold : bilan par poste (PS, âge, salaire, profondeur) (vérifié le 2026-10-16 : gold.bv_position_summary, 15 joueurs, somme des salaires = silver)
- [x] Gold : tendances de match (rebonds, tirs, pertes de balle, fautes) sur les 5 et 10 derniers matchs (vérifié le 2026-10-16 : gold.bv_match_trends, moi vs adversaires ; 2 matchs en base, se remplit avec les exports)
- [x] Gold : progression hebdo de chaque skill par joueur (vérifié le 2026-10-16 : gold.bv_skill_progress_weekly, 6 entraînements)
- [x] Gold : résultat financier hebdo et projection de fin de saison (vérifié le 2026-10-16 : gold.bv_finance_weekly_result + gold.bv_finance_projection)

## D. Skills
- [x] Règles, moteur, entraînement, économie, marché écrits depuis le manuel officiel (vérifié le 2026-10-16 : 7 skills basketvibe-*, manuel lu en entier, chaque fait sourcé [M§x])
- [x] Communauté : historique Discord lu une fois, conseils classés et datés (vérifié le 2026-10-16 : 2 321 messages utiles lus, skill basketvibe-communaute)
- [x] 10 questions de règles testées par l'utilisateur : 10 réponses justes (vérifié le 2026-10-16 : validé par l'utilisateur et recontrôlé ligne à ligne dans le manuel)

## E. Agents
- [x] Effectif : bilan par poste, meilleurs et moins bons joueurs (validé par l'utilisateur le 2026-10-18 : brief du 2026-10-16)
- [x] Effectif : 3 actions concrètes pour améliorer l'équipe (validé par l'utilisateur le 2026-10-18, action 1 complétée avec Nolan Baron)
- [x] Effectif : projection sur 1 à 3 saisons (âges, déclin, relève) (validé par l'utilisateur le 2026-10-18)
- [x] Match : explication de chaque victoire et défaite, chiffres à l'appui (validé par l'utilisateur le 2026-10-18 : brief du 2026-10-18, 26 matchs)
- [x] Match : journal des enseignements, mis à jour après chaque match (validé par l'utilisateur le 2026-10-18 : learnings.md, L-001 à L-007, delta par « dernier match analysé »)
- [ ] Match : contrôle des conseils passés (appliqué ou non, effet constaté)
- [x] Tactique : tactique initiale complète, prête à saisir dans le jeu (validé par l'utilisateur le 2026-10-18 : presets « Ligue S1 » et « Amical » saisis dans le jeu)
- [x] Tactique : ajustement selon l'adversaire du prochain match (validé par l'utilisateur le 2026-10-18 : focus défensif J19 BARIUM saisi)
- [ ] Tactique : évolution de la tactique à partir du journal des enseignements
- [x] Entraînement : verdict hebdo garder ou changer, à partir des résultats d'entraînement (validé par l'utilisateur le 2026-10-18 : brief du 2026-10-18, gains précis par entraînement)
- [x] Potentiel : estimation du potentiel de chaque joueur depuis sa progression, avec un niveau de confiance (validé par l'utilisateur le 2026-10-18 : gold.bv_potential_estimate, 6 potentiels sûrs, 8 à 2 valeurs)
- [x] Académie : avis sur les 3 prospects (tester, signer ou ignorer) et sur l'investissement hebdo (validé par l'utilisateur le 2026-10-18 : ignorer les 3, garder 100 000, signature visée vers le 19/11)
- [x] Transferts : pour un joueur donné, intérêt pour l'effectif, prix correct ou non, enchère maximum (validé par l'utilisateur le 2026-10-18 : brief du 2026-10-18, enchères Al-Anazi, Dang, Daniels, Albano posées)
- [x] Transferts : liste des joueurs à vendre (âge, salaire, déclin) et moment de la vente (validé par l'utilisateur le 2026-10-18 : Fontaine maintenant, Henry et Klein après le 26/10)
- [x] Finances : alerte si on perd de l'argent, avec la cause (validé par l'utilisateur le 2026-10-18 : brief finances, pas de perte, marge portée par les amicaux)
- [x] Finances : masse salariale soutenable ou non par rapport aux revenus (validé par l'utilisateur le 2026-10-18 : salaires ≈ 50 % des recettes, homegrown chiffré)
- [x] Finances : capacité d'investissement (académie, personnel) (validé par l'utilisateur le 2026-10-18 : ≈ 160 000 engageables, réserve de 2 semaines)
- [x] Personnel : recruter, garder ou virer, poste par poste, avec le coût et le gain attendu (validé et appliqué par l'utilisateur le 2026-10-18 : 2 marketing renvoyés, 3 kinés embauchés)

## F. Wiki et apprentissage continu
- [ ] Wiki : routine quotidienne et hebdomadaire
- [ ] Wiki : comment progresser (priorités par saison)
- [ ] Wiki : âges clés (meilleur âge, quand vendre, déclin, retraite)
- [ ] Wiki : profil idéal par poste et meilleurs joueurs observés par poste
- [ ] Wiki : quels entraînements selon le poste et l'âge
- [ ] Veille : propositions de mise à jour des skills après chaque export Discord ou devlog
- [ ] Brief quotidien : un résumé chaque matin regroupant les points ci-dessus

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
- [x] Silver : joueurs + photo hebdomadaire (lundi matin) de leurs skills, forme, fatigue (vérifié le 2026-10-16 : silver.bv_player_weekly, 15 joueurs, skills précis ; 2e semaine à confirmer le 2026-10-19)
- [x] Silver : matchs, stats par joueur, événements du play-by-play (vérifié le 2026-10-16 : 2 matchs, somme des quart-temps = score final = fin du play-by-play)
- [ ] Silver : marché, finances, personnel, académie, classement
- [ ] Gold : bilan par poste (PS, âge, salaire, profondeur)
- [ ] Gold : tendances de match (rebonds, tirs, pertes de balle, fautes) sur les 5 et 10 derniers matchs
- [ ] Gold : progression hebdo de chaque skill par joueur
- [ ] Gold : résultat financier hebdo et projection de fin de saison

## D. Skills
- [ ] Règles, moteur, entraînement, économie, marché écrits depuis le manuel officiel
- [ ] Communauté : historique Discord lu une fois, conseils classés et datés
- [ ] 10 questions de règles testées par l'utilisateur : 10 réponses justes

## E. Agents
- [ ] Effectif : bilan par poste, meilleurs et moins bons joueurs
- [ ] Effectif : 3 actions concrètes pour améliorer l'équipe
- [ ] Effectif : projection sur 1 à 3 saisons (âges, déclin, relève)
- [ ] Match : explication de chaque victoire et défaite, chiffres à l'appui
- [ ] Match : journal des enseignements, mis à jour après chaque match
- [ ] Match : contrôle des conseils passés (appliqué ou non, effet constaté)
- [ ] Tactique : tactique initiale complète, prête à saisir dans le jeu
- [ ] Tactique : ajustement selon l'adversaire du prochain match
- [ ] Tactique : évolution de la tactique à partir du journal des enseignements
- [ ] Entraînement : verdict hebdo garder ou changer, à partir des résultats d'entraînement
- [ ] Potentiel : estimation du potentiel de chaque joueur depuis sa progression, avec un niveau de confiance
- [ ] Académie : avis sur les 3 prospects (tester, signer ou ignorer) et sur l'investissement hebdo
- [ ] Transferts : pour un joueur donné, intérêt pour l'effectif, prix correct ou non, enchère maximum
- [ ] Transferts : liste des joueurs à vendre (âge, salaire, déclin) et moment de la vente
- [ ] Finances : alerte si on perd de l'argent, avec la cause
- [ ] Finances : masse salariale soutenable ou non par rapport aux revenus
- [ ] Finances : capacité d'investissement (académie, personnel)
- [ ] Personnel : recruter, garder ou virer, poste par poste, avec le coût et le gain attendu

## F. Wiki et apprentissage continu
- [ ] Wiki : routine quotidienne et hebdomadaire
- [ ] Wiki : comment progresser (priorités par saison)
- [ ] Wiki : âges clés (meilleur âge, quand vendre, déclin, retraite)
- [ ] Wiki : profil idéal par poste et meilleurs joueurs observés par poste
- [ ] Wiki : quels entraînements selon le poste et l'âge
- [ ] Veille : propositions de mise à jour des skills après chaque export Discord ou devlog
- [ ] Brief quotidien : un résumé chaque matin regroupant les points ci-dessus

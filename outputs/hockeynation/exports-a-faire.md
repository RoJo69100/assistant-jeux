# Hockey Nation — exports (tableau évolutif)

Script : `userscripts/hockeynation.user.js` v0.1.0. Jeu en base : `hockeynation`. Site : https://hockey-nation.com. Légende : 🟥 URGENT · 🟧 IMPORTANT · 🟩 SUIVI · ✅ reçu · ⬜ manque

## Reçu le 2026-10-23 (14:39–14:45 UTC, 265 captures, 35 types de page)
| | Page | Types en base | État |
|---|---|---|---|
| ✅ | Club (accueil, actualités, statistiques, palmarès) | club_overview, club_news, club_stats, team_id_hall-of-fame | reçu |
| ✅ | Effectif | club_roster, club_roster_id | reçu |
| ✅ | Calendrier du club | club_schedule, club_schedule_id | reçu |
| ✅ | Entraînement | club_training, club_training_id | reçu |
| ✅ | Lignes / composition | club_lineups | reçu |
| ✅ | Finances | office_finances | reçu |
| ✅ | Staff et entraîneurs | coaching-staff, coach_id | reçu |
| ✅ | Joueurs libres, repérage, shortlist, draft | office_free-agent-center, office_scouting, office_shortlist, office_draft-center | reçu |
| ✅ | Ligue (aperçu, classement, calendrier, notes, stats) | league_overview, league_standings, league_schedule, league_ratings, league_stats | reçu |
| ✅ | Monde (fédérations, championnat du monde, awards, acteurs, classements) | world_federations, federation_overview_id, world-championship_overview, world_awards, world_actors, leaderboard_overview | reçu |
| ✅ | Forum | forum, forum_category_id, forum_topic_id | reçu |
| ✅ | Guide | guide (10 instantanés de rubriques) | reçu, nombre de rubriques à confirmer |

## Il manque
| | Page à ouvrir | Pourquoi | État |
|---|---|---|---|
| 🟥 URGENT | **Une page de match joué** (résumé, statistiques, événements) : depuis le calendrier du club, clique sur un match terminé | aucune page `game`/`match` en base : impossible d'analyser un match | ⬜ |
| 🟥 URGENT | **Les échanges / trades** (le salon #trade compte 17 809 messages, c'est un cœur du jeu) : page de proposition d'échange ou d'historique | aucune page `trade` en base | ⬜ |
| 🟧 IMPORTANT | **La fiche détaillée d'un joueur** (compétences, contrat, historique) : ouvre un joueur depuis l'effectif | `club_roster_id` existe, à confirmer que c'est bien la fiche joueur | ⬜ |
| 🟧 IMPORTANT | **/version-history** | changements de règles | ⬜ |
| 🟧 IMPORTANT | Guide : toutes les rubriques | 10 instantanés reçus, le guide en a peut-être davantage | ⬜ |
| 🟩 SUIVI | Infrastructures / arène / installations si elles existent | aucune page en base | ⬜ |
| 🟩 SUIVI | Calendrier du championnat du monde, équipes jeunes si elles existent | à repérer | ⬜ |

Discord : 154 464 messages en base (5 salons, du 2022-02-17 au 2026-10-23).

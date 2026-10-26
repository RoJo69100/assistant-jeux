# Hockey Nation — exports (tableau évolutif)

Script : `userscripts/hockeynation.user.js` v0.1.0. Jeu en base : `hockeynation`. Contexte donné par l'utilisateur : `data/contexte/HN_contexte.txt` (versionné). Légende : 🟥 URGENT · 🟧 IMPORTANT · 🟩 SUIVI · ✅ reçu · ⬜ manque

## Reçu (2026-10-23, 14:39–15:02 UTC)
| | Page | Types en base | État |
|---|---|---|---|
| ✅ | Club : accueil, actualités, statistiques, palmarès | club_overview, club_news, club_stats, team_id_hall-of-fame | reçu |
| ✅ | Effectif des 4 équipes (PRO + 3 ids : Farm, U21, U17) | club_roster, club_roster_id ×3 | reçu |
| ✅ | Calendrier des 4 équipes | club_schedule, club_schedule_id ×3 | reçu |
| ✅ | Entraînement des 4 équipes | club_training, club_training_id ×3 | reçu |
| ✅ | Lignes / composition de l'équipe PRO | club_lineups (1 seul) | reçu pour PRO seulement |
| ✅ | Finances | office_finances | reçu |
| ✅ | Staff et une fiche entraîneur (forces et faiblesses) | coaching-staff, coach_id | reçu |
| ✅ | Joueurs libres | office_free-agent-center | reçu |
| ✅ | Échanges (historique des trades) | office_trade-center | reçu |
| ✅ | Draft (S27) et repérage | office_draft-center, office_scouting, office_shortlist | reçu |
| ✅ | **Un match joué** | game_id | reçu |
| ✅ | Ligue, Monde, Fédérations, Forum | league_*, world_*, federation_overview_id, forum* | reçu |
| ✅ | **Guide complet** : une seule page de 86 000 caractères qui contient les 21 rubriques (Introduction, Nations, Teams, Players, Coaches, Training, Competitions, Lineups, Finances, U21 Team, Farm Team, Free Agents, Trades, Draft, Scouting, Federations, Friends, Hall of Fame, Prizes, Tournaments, Calendar), dernière mise à jour du guide : 30/09/2026 | guide | reçu, rien à refaire |

## Il manque
| | Page à ouvrir | Pourquoi | État |
|---|---|---|---|
| 🟥 URGENT | **Lignes (/club/lineups) des 3 autres équipes** : Farm, U21, U17 (changer d'équipe en haut de la page) | je n'ai que PRO ; les lignes servent à juger les compos des 4 équipes | ⬜ |
| 🟥 URGENT | **Staff / entraîneurs de chaque équipe** et la fiche (forces / faiblesses) de chaque entraîneur que tu veux comparer | objectif : trouver et former les meilleurs jeunes entraîneurs | ⬜ |
| 🟧 IMPORTANT | La liste des joueurs de la draft S27 (prospects) et tes choix (picks) | le recrutement des scouts dépend du poste et de la nationalité | ⬜ |
| 🟧 IMPORTANT | Les contrats : fiche d'un joueur avec son contrat (durée, salaire, extension) | gestion des contrats sur le long terme | ⬜ |
| 🟩 SUIVI | /version-history (historique des mises à jour du jeu) | savoir quand une règle a changé | ⬜ |
| 🟩 SUIVI | Adversaires : lignes, staff et infrastructures de tes prochains adversaires | futur skill « étude des adversaires » | ⬜ |

Retiré : infrastructures (aucune page dans le jeu, confirmé par l'utilisateur).
Discord : 154 464 messages en base (5 salons, du 2022-02-17 au 2026-10-23).

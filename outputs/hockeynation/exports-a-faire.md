# Hockey Nation — exports à faire (tableau évolutif)

Script : `userscripts/hockeynation.user.js` v0.1.0 (copie du script Six Zero ; routes encore inconnues : le type de page vient du chemin). Jeu en base : `hockeynation`. Site : https://hockey-nation.com (guide : /guide, historique : /version-history, prix : /world/awards, forum : /forum).
Légende : 🟥 URGENT · 🟧 IMPORTANT · 🟩 SUIVI · ✅ reçu en base · ⬜ pas encore

| | Page à ouvrir | Pourquoi | Reçu |
|---|---|---|---|
| 🟥 URGENT | Accueil / tableau de bord du club | repérer les routes et l'API du jeu | ⬜ |
| 🟥 URGENT | Effectif (liste des joueurs) puis la fiche d'un joueur | compétences, âge, forme, salaire | ⬜ |
| 🟥 URGENT | Page d'un match joué (résumé et statistiques) | analyse de match | ⬜ |
| 🟥 URGENT | Tactique / lignes / composition | réglages à vérifier | ⬜ |
| 🟧 IMPORTANT | Finances | recettes, salaires, solde | ⬜ |
| 🟧 IMPORTANT | Entraînement | réglages et progression | ⬜ |
| 🟧 IMPORTANT | Marché des transferts (liste et une enchère) | prix, délais | ⬜ |
| 🟧 IMPORTANT | Classement et calendrier de la ligue | agenda | ⬜ |
| 🟧 IMPORTANT | /guide (chaque rubrique) | règles sourcées | ⬜ |
| 🟩 SUIVI | /version-history, /world/awards | changements de règles, primes | ⬜ |
| 🟩 SUIVI | Académie / jeunes, infrastructures si elles existent | à repérer | ⬜ |

Discord : `data/discord/HockeyNation/` (6 fichiers, 5 salons : #general, #events, #france, #trade, #game-tools), à importer avec `pipelines/import_discord.py hockeynation`.

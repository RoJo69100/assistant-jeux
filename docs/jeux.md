# Jeux à intégrer

Liste donnée par l'utilisateur le 2026-10-18 : **28 jeux** (BuzzerBeater donné deux fois = un seul jeu). Corrections de l'utilisateur : SixZero League = handball, VM-Manager = volley, World Aces = volley, Derby Manager = football. Le genre est déduit du nom et de l'adresse : **à confirmer** pour ceux marqués « ? ». Rien n'a encore été vérifié sur les sites (manuel, API, Discord).

## Familles
| Famille | Jeux | Domaines probables (à confirmer jeu par jeu) |
|---|---|---|
| **Football (soccer), management d'équipe** — 13 | Hattrick, Sokker, TrophyManager, PManager, Dugout Soccer, Final Whistle, Kick Off Boss, Football Manager Project, Rocking Soccer, It's a Goal, Team Soccer, Football Legacy, Derby Manager | effectif, match, tactique, entraînement, transferts, finances, jeunes |
| **Basket, management d'équipe** — 3 | BasketVibe (fait), BuzzerBeater, Online College Basketball (universitaire : recrutement de lycéens plutôt que transferts ?) | idem BasketVibe |
| **Hockey sur glace** — 2 | Hockey Nation, Ice Dynasty | idem |
| **Autres sports d'équipe** — 5 | SixZero League (handball), TeamHB (handball), VM-Manager (volley), World Aces (volley), RedZone Action (football américain) | idem, tactique très différente pour le football américain |
| **Cricket** — 1 | From the Pavilion | idem, match très différent |
| **Sports individuels, carrière d'un athlète** — 3 | Tennis Web Manager, Athlenet (athlétisme), My Racing Career (sport automobile) | athlète, calendrier des compétitions, entraînement, matériel, finances |
| **Équipe de courses** — 1 | Cycling Simulator (cyclisme) | coureurs, calendrier des courses, entraînement, finances |

## Conséquences pour le kit
- **Socle commun à tous** : bronze, script Tampermonkey (capture passive), import Discord, méthode des agents (faits / règles / avis, delta, journal, conseils suivis), agenda « que faire aujourd'hui ».
- **Agents par domaine globaux** pour les 24 jeux de sport d'équipe (familles 1 à 5) : effectif, match, tactique, entraînement, transferts, finances-personnel, jeunes/académie, veille. Chaque jeu a sa fiche (skills, vues gold, spécificités).
- **Une 2e famille d'agents** pour les sports individuels et les équipes de courses (familles 6 et 7) : athlète, calendrier, préparation, matériel, finances, veille.
- **Par jeu, toujours** : lecture du manuel → skills, lecture des données → silver, règles → gold, checklist adaptée, tests avec l'utilisateur.

## Ordre décidé (2026-10-18)
1. **SixZero League** (handball) : nouveau jeu, simple à prendre en main → construire le kit.
2. **Team Soccer** (football) : vérifier le kit sur la plus grosse famille (13 jeux).

## Critères pour la suite
Critères : temps passé et ambition sur le jeu, richesse du manuel, données exposées (API JSON ou seulement HTML), taille de la famille (un jeu de football rend le kit utile à 13 jeux).

# Jeux à intégrer

Liste donnée par l'utilisateur le 2026-10-18 (30 jeux, BasketVibe compris). Le genre est déduit du nom et de l'adresse : **à confirmer** pour ceux marqués « ? ». Rien n'a encore été vérifié sur les sites (manuel, API, Discord).

## Familles
| Famille | Jeux | Domaines probables (à confirmer jeu par jeu) |
|---|---|---|
| **Football (soccer), management d'équipe** — 13 | Hattrick, Sokker, TrophyManager, PManager, Dugout Soccer, Final Whistle, Kick Off Boss, Football Manager Project, Rocking Soccer, It's a Goal, Team Soccer, Football Legacy, SixZero League (?) | effectif, match, tactique, entraînement, transferts, finances, jeunes |
| **Basket, management d'équipe** — 3 | BasketVibe (fait), BuzzerBeater, Online College Basketball (universitaire : recrutement de lycéens plutôt que transferts ?) | idem BasketVibe |
| **Hockey sur glace** — 2 | Hockey Nation, Ice Dynasty | idem |
| **Autres sports d'équipe** — 3 | TeamHB (handball), RedZone Action (football américain), VM-Manager (? sport à confirmer) | idem, tactique très différente pour le football américain |
| **Cricket** — 1 | From the Pavilion | idem, match très différent |
| **Sports individuels, carrière d'un athlète** — 4 | Tennis Web Manager, World Aces (tennis ?), Athlenet (athlétisme), My Racing Career (sport automobile) | athlète, calendrier des compétitions, entraînement, matériel, finances |
| **Équipe de courses** — 2 | Cycling Simulator (cyclisme), Derby Manager (courses hippiques) | coureurs / chevaux, calendrier des courses, entraînement, finances |

## Conséquences pour le kit
- **Socle commun à tous** : bronze, script Tampermonkey (capture passive), import Discord, méthode des agents (faits / règles / avis, delta, journal, conseils suivis), agenda « que faire aujourd'hui ».
- **Agents par domaine globaux** pour les 22 jeux de sport d'équipe (familles 1 à 5) : effectif, match, tactique, entraînement, transferts, finances-personnel, jeunes/académie, veille. Chaque jeu a sa fiche (skills, vues gold, spécificités).
- **Une 2e famille d'agents** pour les sports individuels et les équipes de courses (familles 6 et 7) : athlète, calendrier, préparation, matériel, finances, veille.
- **Par jeu, toujours** : lecture du manuel → skills, lecture des données → silver, règles → gold, checklist adaptée, tests avec l'utilisateur.

## Ordre proposé (à décider avec l'utilisateur)
Critères : temps passé et ambition sur le jeu, richesse du manuel, données exposées (API JSON ou seulement HTML), taille de la famille (un jeu de football rend le kit utile à 13 jeux).

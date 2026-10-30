# Checklist Hardwood

Périmètre tiré de `docs/chose-a-faire-hardwood.txt` (liste de l'utilisateur, 2026-10-30). Une case se coche quand son critère est vérifié, avec la date.

## Global
- [x] G1 Veille intégrale : règles, Discord complet, manuel → `outputs/hardwood/veille/connaissance.md` + 3 skills (2026-10-30). Forum et chat du jeu : non exportés (à faire si l'utilisateur les exporte).
- [x] G2 Calendrier et jour du jeu : `gold.hw_today` donne le prochain match à l'heure de Paris, le bilan, le début de la conférence (vérifié 2026-10-30 : Rutgers-Camden 30/10 17:00, conférence le 01/11).
- [x] G3 Compétitions ligue / coupe / amical : exhibitions = amical (tests), hors conférence + conférence = ligue, playoffs/tournoi = coupe ; Game Plan de référence pour ligue et coupe (`docs/attentes/jeux/hardwood.yaml`, 2026-10-30).
- [ ] G4 Meilleurs joueurs des autres équipes de la ligue : il manque les pages `/statistics/<id adverse>` (critère : une vue gold `hw_league_players` alimentée par au moins 5 équipes de VI.26).

## Recrutement (pas de transferts)
- [x] R1 Fonctionnement : types HS / JC / international, points, offres, intérêt, phrases du scout → `hardwood-recrutement` (2026-10-30, tableau corrigé avec le doc d'aide).
- [x] R2 Tableau des recrues : `gold.hw_recruit_board` (verdict, rang, besoin par poste, bourses libres) (2026-10-30).
- [ ] R3 Décider qui recruter : première décision de recrutement rendue avec 3-4 cibles nommées et la répartition des points (critère : un brief Académie daté).

## Équipe
- [x] E1 Toutes les caractéristiques : `gold.hw_effectif` (14 compétences, physique, potentiel, plafond, évaluation du scout) (2026-10-30).
- [x] E2 Fatigue : règle dans `hardwood-regles` (reposés entre deux matchs, Overwork) + fatigue par match dans `silver.hw_game_box` (2026-10-30).
- [x] E3 Bon poste / autre poste : `gold.hw_player_fit` et `gold.hw_player_pos_scores` (2026-10-30).
- [x] E4 Statistiques des joueurs : `gold.hw_effectif` (stats de la saison) (2026-10-30).
- [x] E5 Blessés et suspendus : `injury_days` dans `gold.hw_effectif`, blessé exclu du depth chart proposé ; pas de suspension dans le jeu (veille) (2026-10-30).
- [ ] E6 Redshirt : décision rendue joueur par joueur pour les boursiers « non » (case possible) (critère : brief Effectif daté).

## Entraînement
- [ ] T1 Focus principal / secondaire et entraînement additionnel par joueur (critère : brief Entraînement daté, appliqué).
- [ ] T2 Suivi des progrès : historique des pages Development (critère : deux exports Development comparés dans une vue gold).

## Tactique
- [x] K1 Composition poste par poste : `gold.hw_depth_suggest` (2026-10-30).
- [ ] K2 Game Tactics et Game Management remplis et justifiés (critère : brief Tactique daté avec les 6 réglages, les ajustements et chaque joueur).
- [ ] K3 Stratégie contre un adversaire selon nos matchs contre lui (critère : vue ou brief qui lit `gold.hw_season_games` filtré sur l'adversaire).
- [x] K4 Stratégie selon toute la saison : `gold.hw_vd_compare` (2026-10-30).

## Personnel
- [x] P1 Head coach et assistants : règles + lecture des phrases de coach → `hardwood-regles` (2026-10-30).
- [ ] P2 Changer de coach : décision rendue avec le coach nommé (critère : `gold.hw_coach_board` lu et décision appliquée ou écartée avec raison).

## Finances
- [x] F1 Aucune finance dans le jeu : confirmé par le manuel (2026-10-30).

# Carte _core — entrainement (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta (règles de progression, réglages prêts à saisir).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Plan d'entraînement en place | `select name, focus_primary, focus_secondary, intensity, is_academy, day from core.training_plan where game = :game and day = (select max(day) from core.training_plan where game = :game) order by name limit 40` | Garder ou changer, joueur par joueur, sur le gain mesuré | `docs/decisions/variables.md` § entrainement |
| C2 | Gain sur 7 jours | `select p.name, p.age, p.position, a.rating as il_y_a_7_jours, p.rating as maintenant, p.rating - a.rating as gain from core.player_daily p join core.player_daily_asof(:game, current_date - 7) a on a.team_id = p.team_id and a.player_id = p.player_id where p.game = :game and p.day = (select max(day) from core.player_daily where game = :game) order by gain desc nulls last limit 40` | Gain nul deux cycles de suite = changer | `docs/regles/actives.md` K10 |
| C3 | Joueurs en déclin | `select name, age, rating, age_declin from gold.roster_bilan where game = :game and en_declin order by age desc limit 15` | Pas d'entraînement de progression sur un joueur en déclin sans raison | `core.game_params` age_declin |
| C4 | Effectif au poste | `select position, rang_poste, name, age, rating from gold.roster_bilan where game = :game order by position, rang_poste limit 40` | Qui doit progresser pour quel poste | `docs/decisions/variables.md` § entrainement |
| C5 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Entraînement périmé : « exporte » avant de trancher | `core.export_rule` |

## Couverture de `docs/decisions/variables.md` § entrainement
| Variable obligatoire | Où |
|---|---|
| Âge, gains des semaines passées | C2 (7 jours) ; plus long : carte du jeu |
| Potentiel | carte du jeu (absent de `core.player_daily`) |
| Compétences sous / au-dessus des seuils du poste | `skills` de `core.player_daily` + seuils du skill du jeu |
| Règles de progression | skill entraînement du jeu |
| Objectifs de l'effectif par poste | C4 |
| Risque (blessure, intensité, fatigue) | C1 (intensité) ; blessure et fatigue : carte `composition` C2 |
| Avis des amis, ce qui prouvera l'erreur | dossier et rendu |

# Carte _core — defaite (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta (statistiques de match propres au jeu, corrections testables).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Dernières défaites | `select day, competition_kind, round_no, my_score, opp_score, opponent, home from core.fixture where game = :game and my_result = 'L' order by day desc limit 5` | Défaite = `my_result`, jamais le score brut | CLAUDE.md, inviolable 4 |
| C2 | Bilan victoires / défaites | `select competition_kind, my_result, count(*) as n, round(avg(my_score), 1) as pour, round(avg(opp_score), 1) as contre from core.fixture where game = :game and my_result is not null group by 1, 2 order by 1, 2 limit 12` | Comparer la défaite à toutes celles de la saison | `docs/decisions/variables.md` § defaite |
| C3 | Effectif le jour de la dernière défaite | `select position, name, rating, form, fatigue, injured, day from core.player_daily_asof(:game, (select max(day) from core.fixture where game = :game and my_result = 'L')) order by position, rating desc limit 40` | Relevé de plus de 7 jours avant le match : absent (`max_age`) | `sql/core/004_asof.sql` |
| C4 | Classement | `select rank, team_label, played, points, wins, losses, gf, ga, is_mine from core.standing where game = :game and day = (select max(day) from core.standing where game = :game) order by rank limit 20` | Défaite contre plus fort ou plus faible : écart de rang | `docs/decisions/variables.md` § defaite |
| C5 | Matchs sans résultat | `select prio, alerte from gold.daily_alerts where game = :game and domaine = 'match' limit 10` | Match passé non exporté : « exporte le match » avant l'analyse | `core.alert_rule` |
| C6 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Chiffre lu dans un export périmé : le dire | `core.export_rule` |

## Couverture de `docs/decisions/variables.md` § defaite
| Variable obligatoire | Où |
|---|---|
| Score via `my_result` | C1 |
| Tirs, zones, rebonds, pertes, fautes, joueur par joueur | carte du jeu (stats de match propres au jeu) |
| Comparaison à toutes les défaites et victoires | C2 |
| Tactique adverse lue, nos réglages du match | carte du jeu |
| Fatigue et minutes | C3 (fatigue) ; minutes : carte du jeu |
| Conseils C-nnn appliqués et leur effet | `outputs/<jeu>/learnings.md` (dossier) |
| Règles du moteur | skill tactique du jeu |
| Avis des amis, 3 à 5 corrections testables | dossier et rendu |

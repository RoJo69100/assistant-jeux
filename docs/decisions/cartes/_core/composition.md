# Carte _core — composition (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta (réglages poste par poste dans l'ordre de l'écran, rendu figé).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Prochain match | `select day, competition_kind, round_no, opponent, home, scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris from core.fixture where game = :game and not played and day >= current_date order by day, scheduled_at nulls last limit 5` | Match d'aujourd'hui ou de demain : se prépare aujourd'hui | CLAUDE.md, inviolable 3 |
| C2 | Joueurs du dernier relevé | `select position, name, age, rating, form, fatigue, injured, suspended, day from core.player_daily where game = :game and day = (select max(day) from core.player_daily where game = :game) order by position, rating desc limit 40` | Forme et fatigue en échelle 0–1 (échelle du jeu : `core.game_params` echelle_*) | `docs/attentes/jeux/<jeu>.yaml` core |
| C3 | Alertes joueurs | `select prio, domaine, alerte from gold.daily_alerts where game = :game and domaine in ('blessure', 'fatigue', 'forme', 'tactique', 'effectif') order by prio limit 15` | Blessé ou hors zone : jamais titulaire sans raison écrite | `core.alert_rule` |
| C4 | Classement | `select rank, team_label, played, points, wins, losses, gf, ga, is_mine from core.standing where game = :game and day = (select max(day) from core.standing where game = :game) order by rank limit 20` | Force de l'adversaire lue au classement et à ses résultats | `docs/decisions/variables.md` § composition |
| C5 | Bilan de la saison | `select competition_kind, my_result, count(*) as n, round(avg(my_score), 1) as pour, round(avg(opp_score), 1) as contre from core.fixture where game = :game and my_result is not null group by 1, 2 order by 1, 2 limit 12` | Ce qui a marché / échoué : voir learnings du jeu | `outputs/<jeu>/learnings.md` |
| C6 | Agenda du jour | `select at_time, priority, category, action from gold.agenda where game = :game and day = current_date order by at_time limit 10` | Heure limite du réglage | `core.agenda_rule` |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Effectif ou tactique périmé : « exporte » avant la saisie | `core.export_rule` |

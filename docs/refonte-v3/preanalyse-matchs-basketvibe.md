# Préanalyse des matchs BasketVibe : que peut-on apprendre du moteur avant de demander de nouveaux exports ?

Écrit le 2026-11-09. Lecture seule (aucune écriture en base), requêtes par `python -I pipelines/sql.py`. Les moteurs v3, v4 et v5, la ligue, la coupe et les amicaux ne sont jamais mélangés.

## Étape 1 : inventaire

### 1.1 Version du moteur : aucune colonne, déduite des dates
Aucune page de match ne porte de champ de version. La version est déduite des annonces du skill `basketvibe-communaute` (`references/02-1-moteur-de-match-versions-et-calibrage.md`) : ligue en v3 jusqu'au 26/10 (dernière journée de la saison 1) ; amicaux en v4 dès le 11/10 ; v4 « actif en ligue, coupe et amical depuis le 27/10 » ; v5 en amical seulement depuis le 28/10 (déploiement dans tous les matchs sans date). Règle appliquée (écrite avant tout calcul) :

| Compétition | Dates | Moteur retenu |
|---|---|---|
| Ligue | jusqu'au 26/10 (saison 1) | v3 |
| Ligue | dès le 02/11 (saison 2) | v4 |
| Coupe | 28/10 à 31/10 | v4 |
| Amical | 10/10 | v3 (veille de l'annonce) |
| Amical | 11/10 au 27/10 | v4 |
| Amical | dès le 28/10 | v5 |

Incertitude : la date exacte de bascule des amicaux (10/10 et 11/10, 27/10 et 28/10) vient de textes de la communauté et des annonces, pas d'une mesure en base. Un match à la date frontière peut être mal classé : ils sont listés à part au besoin.

### 1.2 Matchs par groupe (moteur, compétition, équipe), détail disponible
Requête (sortie ci-dessous) : voir `Annexe A`. Seuls les matchs `finished` de `silver.bv_matches` sont comptés.

| Moteur | Compétition | Équipe | Matchs | Période | Adversaires distincts | Box score par joueur et par quart | Play-by-play | Composition de début de quart | Réglages tactiques lisibles |
|---|---|---|---|---|---|---|---|---|---|
| v3 | ligue | nous | 22 | 07/09 au 26/10 | 11 | 22 (les 2 équipes) | 22 | 22 : la nôtre et celle de l'adversaire | 22 : les nôtres |
| v3 | amical | nous | 1 | 10/10 | 1 | 1 | 1 | 1 : les deux | 1 : les nôtres |
| v4 | ligue | nous | 3 | 02/11 au 07/11 | 3 | 3 | 3 | 3 : les deux | 3 : les nôtres |
| v4 | ligue | autres équipes | 2 | 02/11 au 04/11 | non applicable | 2 (les 2 équipes) | 2 | absente | absents |
| v4 | coupe | nous | 2 | 28/10 au 30/10 | 2 | 2 | 2 | 1 sur 2 | 1 sur 2 : les nôtres |
| v4 | coupe | autres équipes | 8 | 28/10 au 31/10 | non applicable | 8 (les 2 équipes) | 8 | absente | absents |
| v4 | amical | nous | 16 | 11/10 au 27/10 | 16 | 16 (15 avec les 2 équipes) | 16 | 14 sur 16 : les deux | 14 sur 16 : les nôtres |
| v5 | amical | nous | 10 | 29/10 au 08/11 | 10 | 10 | 10 | 9 sur 10 : les deux | 9 sur 10 : les nôtres |
| Total | | | 64 | 07/09 au 08/11 | 56 équipes en tout dans `bv_matches` (07/09 au 09/11) | 64 | 64 | 50 | 50 |

Matchs sans détail (score seul) : saison 1, ligue, 242 matchs des autres équipes (`silver.bv_fixtures`, aucun dans `silver.bv_matches`) ; saison 2, ligue, 8 matchs terminés des autres équipes sur 10 ; 120 matchs de ligue de la saison 2 programmés. Un match « score seul » ne sert à aucune des six questions.

### 1.3 Ce que contient chaque niveau de détail
- **Score et quarts-temps** : `quarter_scores` pour les 64 matchs (points domicile et extérieur par quart).
- **Box score par joueur** (`silver.bv_match_player_stats`) : les deux équipes, une ligne par joueur et par période (0 = match entier, 1 à 4 = quarts) : minutes, points, tirs à 2/3/LF réussis et tentés, rebonds offensifs et défensifs, passes, interceptions, contres, pertes de balle, fautes, +/-, évaluation. Pas de fatigue ni de forme du joueur dans le box score.
- **Play-by-play** (`silver.bv_match_events`) : 64 matchs, 27 236 événements (somme de la requête 4 ; tirs réussis et manqués, rebonds, fautes, pertes de balle, passes, lancers, remplacements pour 39 matchs, blessures pour 13 matchs, entre-deux). Coordonnées de tir (`shot_x`, `shot_y`) disponibles.
- **Composition de début de quart** (`silver.bv_match_tactics`) : `lineup_by_quarter` (la nôtre) et `opponent_lineup_by_quarter` (celle de l'adversaire), les deux équipes, 50 matchs dont 3 de ligue v4.
- **Réglages tactiques** : les nôtres seulement. `defensive_focus` (focus défensif par joueur adverse), `player_directives` (rôle, niveau de tir, focus offensif, niveau de défense de chaque joueur). Ceux de l'adversaire : **non lisibles** (on ne voit que sa composition et ce qu'il a fait en match).
- **Fatigue, forme, PS des joueurs** : `silver.bv_player_daily` (18 joueurs à nous, 287 lignes, 16/10 au 08/11) ; PS de l'adversaire : non lisible. Force d'équipe des autres clubs : `club_strength` de `silver.bv_standings_weekly` (31 équipes, 67 lignes, 18/10 au 08/11 seulement : rien avant le 18/10).

## Annexe A : sorties collées de l'étape 1

Requête 1 (matchs par saison, compétition, statut) : `select season_id, competition, status, (my_side is not null) mien, count(*) n, min(match_day) du, max(match_day) au from silver.bv_matches group by 1,2,3,4 order by 1,2,3,4`

```
| saison (début) | compétition | statut | mien | n | du | au |
| 86a63498 | cup | finished | False | 8 | 2026-10-28 | 2026-10-31 |
| 86a63498 | cup | finished | True | 2 | 2026-10-28 | 2026-10-30 |
| 86a63498 | cup | scheduled_lineups | True | 2 | 2026-10-29 | 2026-10-31 |
| 86a63498 | friendly | finished | True | 11 | 2026-10-27 | 2026-11-08 |
| 86a63498 | friendly | scheduled_lineups | True | 1 | 2026-11-09 | 2026-11-09 |
| 86a63498 | league | finished | False | 2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | league | finished | True | 3 | 2026-11-02 | 2026-11-07 |
| 86a63498 | league | scheduled_lineups | True | 1 | 2026-11-09 | 2026-11-09 |
| 8fa19101 | friendly | finished | True | 16 | 2026-10-10 | 2026-10-26 |
| 8fa19101 | league | finished | True | 22 | 2026-09-07 | 2026-10-26 |
```

Requête 2 (inventaire final par moteur, compétition, équipe) : texte exact en `Annexe B`. Sortie :

```
| moteur | competition | equipe | matchs | du | au | adversaires_distincts | box | box_2cotes | pbp | lineups_nous | lineups_adv |
| v3 | friendly | nous | 1 | 2026-10-10 | 2026-10-10 | 1 | 1 | 1 | 1 | 1 | 1 |
| v3 | league | nous | 22 | 2026-09-07 | 2026-10-26 | 11 | 22 | 22 | 22 | 22 | 22 |
| v4 | cup | autres | 8 | 2026-10-28 | 2026-10-31 | 0 | 8 | 8 | 8 |  |  |
| v4 | cup | nous | 2 | 2026-10-28 | 2026-10-30 | 2 | 2 | 2 | 2 | 1 | 1 |
| v4 | friendly | nous | 16 | 2026-10-11 | 2026-10-27 | 16 | 16 | 15 | 16 | 14 | 14 |
| v4 | league | autres | 2 | 2026-11-02 | 2026-11-04 | 0 | 2 | 2 | 2 |  |  |
| v4 | league | nous | 3 | 2026-11-02 | 2026-11-07 | 3 | 3 | 3 | 3 | 3 | 3 |
| v5 | friendly | nous | 10 | 2026-10-29 | 2026-11-08 | 10 | 10 | 10 | 10 | 9 | 9 |
```

Requête 3 (matchs sans détail) : `select f.season_id, f.is_mine, f.status, count(*) fixtures, count(m.fixture_id) dans_matches, min(f.match_day) du, max(f.match_day) au from silver.bv_fixtures f left join silver.bv_matches m using (fixture_id) group by 1,2,3 order by 1,2,3`

```
| 86a63498 | False | finished  |  10 |  2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | False | scheduled | 100 |  0 | 2026-11-07 | 2026-12-21 |
| 86a63498 | True  | finished  |   2 |  2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | True  | scheduled |  20 |  2 | 2026-11-07 | 2026-12-21 |
| 8fa19101 | False | finished  | 242 |  0 | 2026-09-07 | 2026-10-26 |
| 8fa19101 | True  | finished  |  22 | 22 | 2026-09-07 | 2026-10-26 |
```

Requête 4 (play-by-play par type d'événement) : `select kind, count(*) n, count(distinct fixture_id) matchs from silver.bv_match_events group by 1 order by 2 desc` : miss 6 057, dreb 4 495, fg2 3 704, ft 3 062, foul 2 173, turnover 2 132, assist 1 886, oreb 1 475, fg3 1 148, dead_ball 373, period_end 256, period_start 256, substitution 123 (39 matchs), jump_ball 64, endgame 16, injury 16 (13 matchs). 64 matchs partout sauf mention.

Requête 5 (périodes du box score) : `select period, count(*) lignes, count(distinct fixture_id) matchs from silver.bv_match_player_stats group by 1 order by 1` : périodes 0 à 4, 1 704 lignes et 64 matchs chacune.

Requête 6 (équipes et période) : `select count(distinct team_id) eq, min(match_day), max(match_day) from (select home_team_id team_id, match_day from silver.bv_matches union all select away_team_id, match_day from silver.bv_matches) x` : 56 équipes, du 2026-09-07 au 2026-11-09.

Requête 7 (force d'équipe et fatigue) : `select count(*) n, count(distinct team_id) eq, min(day) du, max(day) au from silver.bv_standings_weekly` : 67 lignes, 31 équipes, 18/10 au 08/11. `select count(*) n, count(distinct player_id) joueurs, min(day) du, max(day) au from silver.bv_player_daily` : 287 lignes, 18 joueurs, 16/10 au 08/11.

## Annexe B : requête d'inventaire

```sql
with m as (
  select fixture_id, competition, (my_side is not null) mien, match_day, season_id, home_team_id, away_team_id, my_side,
    case when competition='league' and match_day <= '2026-10-26' then 'v3'
         when competition='friendly' and match_day <= '2026-10-10' then 'v3'
         when competition='friendly' and match_day >= '2026-10-28' then 'v5'
         else 'v4' end moteur
  from silver.bv_matches where status='finished'),
ps as (select fixture_id, count(distinct team_side) cotes from silver.bv_match_player_stats group by 1),
ev as (select distinct fixture_id from silver.bv_match_events),
tc as (select fixture_id, bool_or(lineup_by_quarter is not null) lu, bool_or(opponent_lineup_by_quarter is not null) lo from silver.bv_match_tactics group by 1)
select moteur, competition, case when mien then 'nous' else 'autres' end equipe, count(*) matchs, min(match_day) du, max(match_day) au,
  count(distinct case when mien then (case when my_side='home' then away_team_id else home_team_id end) end) adversaires_distincts,
  count(ps.fixture_id) box, sum((ps.cotes=2)::int) box_2cotes, count(ev.fixture_id) pbp, sum(tc.lu::int) lineups_nous, sum(tc.lo::int) lineups_adv
from m left join ps using (fixture_id) left join ev using (fixture_id) left join tc using (fixture_id)
group by 1,2,3 order by 1,2,3
```

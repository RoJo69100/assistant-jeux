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

## Étape 2 : critères (écrits le 2026-11-09 avant tout calcul sur les matchs)

### 2.1 Règles communes
- **Groupes** (jamais mélangés) : G1 ligue v3 (nous) ; G2 ligue v4 (nous et autres équipes) ; G3 coupe v4 (nous et autres) ; G4 amical v4 ; G5 amical v5. Le seul amical v3 (1 match) n'est pas analysé. La ligue v3 ne décrit pas le moteur actuel (fatigue et duels changés en v4) : son verdict est dit « historique, non transférable ».
- **Unité** : le match (une ligne par match) pour les questions 1, 3, 4, 5, 6 ; le couple joueur-match pour la question 2. Pour les matchs des autres équipes (box score des deux côtés, sans réglages), le côté « nous » est le côté domicile.
- **Seuils** : risque α = 0,05 par question (partagé en Bonferroni quand une question a plusieurs tests : α par test indiqué), puissance 80 % (β = 0,20), tests bilatéraux. z(0,975) = 1,960 ; z(0,9875) = 2,241 ; z(0,99375) = 2,498 ; z(0,80) = 0,842.
- **n requis** : pour une corrélation r, `n = ((z_α + z_β) / atanh(r))² + 3` (transformation de Fisher) ; pour une moyenne, `n = ((z_α + z_β) · σ / δ)²` avec σ = écart-type observé de la mesure dans le groupe (« variance observée », mesuré à l'étape 3, jamais choisi) ; pour une proportion contre 0,5, formule exacte du test binomial approchée par `n = ((z_α·0,5 + z_β·√(p(1−p))) / (p − 0,5))²`.
- **Verdict** : « décidable » si n disponible ≥ n requis ; alors l'effet est dit *présent* (intervalle de confiance à 95 % entièrement du même côté de 0 et |effet| ≥ effet minimal), *absent* (intervalle inclus dans ±effet minimal) ou *entre les deux*. Sinon « n trop petit » : l'effet et son intervalle sont donnés pour information, sans conclusion. **n disponible < 5 : aucun effet n'est calculé.**
- **Effets minimaux** : ils sont fixés par ce qu'il faudrait pour changer une décision, pas par ce que les données suggèrent. Aucun n'est une règle du jeu.

### 2.2 Les six questions

| # | Mesure | Test | Effet minimal et pourquoi | n requis |
|---|---|---|---|---|
| 1 | Pour chaque match : écart « nous − eux » des quatre facteurs (eFG % = (réussis + 0,5 × réussis à 3) / tentés ; rebonds offensifs en % = ORB / (ORB + DRB adverse) ; pertes de balle en % = TOV / (tentés + 0,44 × LF tentés + TOV) ; lancers francs tentés par tir tenté) et marge du match (nous − eux) ; ligue seulement. Description en plus : moyenne de chaque facteur en victoire et en défaite. | Corrélation de Pearson de l'écart de chaque facteur avec la marge, intervalle de Fisher. 4 tests : α = 0,0125 par test. | r = 0,5 (effet « large » : en dessous, un facteur n'oriente pas une tactique) | **40** (r = 0,5 ; α = 0,0125 ; puissance 80 %) |
| 2 | (a) Pour chaque joueur-match avec au moins 3 quarts joués et au moins 27 minutes cumulées avant le Q4 (minutes lourdes ; le moteur pénalise au-delà de 36 minutes) : évaluation par minute au Q4 contre sa moyenne des Q1 à Q3 (différence relative). (b) Fatigue du joueur le matin du match (dernier relevé de `bv_player_daily` du jour ou la veille) et évaluation par minute dans le match, nos joueurs seulement. | (a) t apparié sur les joueurs-matchs. (b) Corrélation de Pearson, intervalle de Fisher. 2 tests : α = 0,025 par test. | (a) −15 % de l'évaluation par minute, l'ordre de grandeur de l'effet annoncé d'une fatigue de 40 (−15 %, skill `basketvibe-tactique`, V-20261027-1). (b) r = −0,3 | (a) `((2,241 + 0,842) · σ / 0,15)²` avec σ = écart-type observé de la différence relative ; (b) **103** pour r = 0,3 et α = 0,025 |
| 3 | Pour chaque match : écart « nous − eux » (i) du nombre de joueurs utilisés (au moins 1 minute) et (ii) de la part des minutes jouées par les cinq joueurs qui jouent le plus ; et marge du match. | Corrélation de Pearson de chaque écart avec la marge. 2 tests : α = 0,025 par test. | r = 0,4 (un rotation qui expliquerait 16 % de la marge) | **56** (r = 0,4 ; α = 0,025) |
| 4 | (i) Pour chaque match et chaque équipe : points par tir à 3 tenté (3 × réussite à 3) moins points par tir à 2 tenté (2 × réussite à 2). (ii) Écart « nous − eux » de la part de tirs à 3 (3PA / FGA) et marge du match. | (i) t à un échantillon (moyenne de la différence contre 0). (ii) Corrélation de Pearson. 2 tests : α = 0,025 par test. | (i) 0,10 point par tir : déplacer 20 tirs de 2 vers 3 rapporte 2 points par match, le plus petit gain qui changerait la répartition. (ii) r = 0,4 | (i) `((2,241 + 0,842) · σ / 0,10)²` avec σ observé de la différence par match ; (ii) **56** |
| 5 | Pour chaque match : marge de l'équipe qui reçoit (points domicile − points extérieur) ; victoire de l'équipe qui reçoit (oui / non). Tous les matchs du groupe, nos matchs et ceux des autres équipes. | (a) t à un échantillon de la marge contre 0. (b) test binomial exact du taux de victoire à domicile contre 0,5. 2 tests : α = 0,025 par test. | (a) 3 points de marge (avec un écart-type de la marge proche de 12, 3 points valent environ 60 % de victoires). (b) taux de victoire de 60 % contre 50 % | (a) `((2,241 + 0,842) · σ / 3)²` avec σ observé de la marge ; (b) **236** (p = 0,6 ; α = 0,025 ; puissance 80 %) |
| 6 | Pour chaque match de ligue : écart de force d'équipe « nous − eux » (`club_strength` du dernier relevé de `bv_standings_weekly` avant le match ; proxy de l'écart de PS d'équipe, ce que la colonne mesure exactement n'est pas documenté) et marge du match. Pente de la droite (points de marge par point d'écart de force). | Corrélation de Pearson et pente par moindres carrés, intervalle de Fisher et intervalle de la pente. 1 test : α = 0,05. | r = 0,5 | **30** (r = 0,5 ; α = 0,05 ; puissance 80 %) |

Calcul des n requis fixes (Fisher, `n = ((z_α + z_β)/atanh(r))² + 3`, arrondi à l'entier supérieur, vérifié par un calcul Python avant tout calcul sur les matchs : première version erronée à la main, corrigée) : Q1 39,96 → **40** ; Q2(b) 102,22 → **103** ; Q3 et Q4(ii) 55,96 → **56** ; Q6 29,01 → **30** ; Q5(b) (binomial, p = 0,6) 235,01 → **236**.

### 2.3 Limites connues avant calcul
- Question 6 : les relevés de `club_strength` commencent le 18/10 : les 18 premiers matchs de la ligue v3 (du 07/09 au 17/10) n'ont pas de force d'équipe ; leur n disponible est donc plus petit que 22.
- Question 2(b) : 18 joueurs et 287 relevés quotidiens depuis le 16/10 ; les matchs avant le 16/10 n'ont pas de fatigue connue.
- Questions 1, 3, 4 : la marge d'un match dépend de la force des deux équipes ; l'écart de facteur la reflète en partie (corrélation, pas causalité). La question 6 est la seule à contrôler la force.
- Les matchs successifs de la même équipe (les nôtres) ne sont pas indépendants (même effectif, même tactique) : les intervalles sont plus étroits qu'ils ne devraient ; le verdict « décidable » est donc un minimum à exiger, pas une garantie.
- La version du moteur par date est une déduction (§ 1.1).

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

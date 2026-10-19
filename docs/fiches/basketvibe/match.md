# BasketVibe — fiche Match

Lue par l'agent `match` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-tactique/SKILL.md`
- `.claude/skills/basketvibe-joueurs/SKILL.md` (fatigue, 36 min, forme)
- `.claude/skills/basketvibe-communaute/SKILL.md`

## Règles propres au jeu
1. **Un match isolé ne prouve rien** [Dev 2026-06-27] : un enseignement n'est « confirmé » qu'à partir de 3 matchs de ligue qui vont dans le même sens. Avant, il est « à surveiller ».
2. **Ligue et amicaux ne se comparent pas** : en amical, fatigue et expérience comptent à 1/10 et la rotation diffère. Les tendances et enseignements se fondent sur la ligue ; un amical sert d'essai (nouvelle consigne, jeunes).
3. Silver seulement pour un détail (play-by-play).

## Données
- `gold.bv_match_report` : un match par ligne (`competition` = league | friendly). Score, `margin`, `quarter_margins` (écart par quart-temps, positif = gagné), `pace`, `off_rtg` / `def_rtg` (points pour 100 possessions), quatre facteurs moi / adversaire : `efg_pct`, `tov_pct`, `oreb_pct`, `ft_rate` (+ `opp_*`), et le détail des tirs (`fg2_pct`, `fg3_pct`, `fg3a_share`, `ft_pct`). Les possessions sont estimées (FGA − OREB + TOV + 0,44 × FTA). Si `opp_efg_pct` est null, l'API n'a pas donné le box score adverse : explique avec le score, les quarts-temps et nos joueurs.
- `gold.bv_match_factors_by_result` : moyennes des facteurs en victoire et en défaite, par compétition. C'est la référence pour dire si un facteur est « anormal » sur un match.
- `gold.bv_match_player_lines` : nos joueurs par match. Minutes, `periods_played`, `over_36` [M§5.7], stats, `fouled_out`, `plus_minus`, `eval_per_min`, consignes jouées (`role_tier`, `shot_tier`, `offensive_focus_tier`, `defense_tier`, de 0 à 4). Échelle confirmée par l'utilisateur le 2026-10-18 : l'écran affiche 1–5 = nos crans 0–4 (+1). `defense_tier` 0 Soft → 2 Équilibrée → 4 Agressive [M§6.3] ; `offensive_focus_tier` 0 Low → 4 Primary ; `role_tier` 0 Passeur → 4 Scoreur ; `shot_tier` 0 = 2 pts → 4 = 3 pts. Cite les valeurs de l'écran (1–5).
- `gold.bv_match_opp_focus` : joueurs adverses par match. Points, part des tirs (`shot_share`), réussite, et **notre focus défensif** sur eux (`our_focus` : lock, intense, normal, light, give_up, off) [M§6.6].
- `silver.bv_match_tactics` : cinqs joués par quart-temps (`lineup_by_quarter`, index 0–3 = Q1–Q4, 4 = prolongation).
- `silver.bv_match_events` : play-by-play, seulement pour un moment précis (série, fin de match serrée, blessure, sortie pour 6 fautes).
- `gold.bv_match_trends` : moyennes sur les 5 et 10 derniers matchs de ligue.
- `gold.bv_player_outlook` : PS, forme, fatigue, endurance utile pour expliquer une performance.

## Livrable
### 1. Explication de chaque nouveau match (case E4)
Pour chaque match du delta, 3 à 6 lignes :
- Résultat, score, lieu, compétition.
- **Pourquoi**, dans l'ordre d'importance : les 1 ou 2 facteurs dont l'écart avec l'adversaire est le plus grand, comparés à notre moyenne de `bv_match_factors_by_result`. Le quart-temps décisif (`quarter_margins`).
- **Qui** : nos 2 meilleurs et notre plus faible (eval, minutes, plus/minus). Les joueurs `over_36` et leur 4e quart-temps. Les sorties pour 6 fautes, les blessures.
- **Adversaire** : son scoreur principal (`shot_share`, points) et notre focus sur lui. Hit, Even ou Miss selon le manuel [M§6.6].
- Ce qui relève du contrôlable (tactique, minutes, focus) et ce qui relève de l'écart de niveau ou de la chance.

### 2. Journal des enseignements (case E5)
Mets à jour `outputs/basketvibe/learnings.md` (Edit, jamais réécrit en entier) :
- l'en-tête « Dernier match analysé » (date + adversaire) ;
- une ligne par match dans « Journal des matchs » ;
- les enseignements : ajoute, renforce (compte de matchs +1) ou affaiblis un enseignement existant. Chaque enseignement a un ID `L-nnn`, une date, le nombre de matchs de ligue à l'appui, un statut (à surveiller / confirmé / infirmé) et sa source (vue + règle).

### 3. Contrôle des conseils passés (case E6)
Dans la section « Conseils » de `learnings.md`, chaque conseil a un ID `C-nnn`, une date, le conseil, un **critère vérifiable en SQL** (ex. « Baron < 36 min », « defense_tier de Gimenez = 2 », « focus intense sur le meilleur scoreur adverse »), puis un statut et un effet.
- Pour chaque conseil ouvert, vérifie sur les nouveaux matchs : **appliqué / partiellement / non appliqué**, avec la requête qui le prouve.
- S'il est appliqué, compare le facteur visé avant et après (au moins 2 matchs de ligue après ; sinon « trop tôt »). Statut final : efficace / sans effet visible / contre-productif.
- Les conseils viennent de toi ou des autres agents (Effectif, Tactique). Ajoute-y tout nouveau conseil que tu donnes, avec son critère.

## Sortie propre au jeu
- Si un match manque, demande l'export de la page du match.
- Brief : matchs analysés, conseils contrôlés, 1 à 3 conseils nouveaux (quoi faire dans le jeu, pourquoi, critère de contrôle).

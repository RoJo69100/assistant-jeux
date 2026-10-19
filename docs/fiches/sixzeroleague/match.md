# Six Zero League — fiche Match

Lue par l'agent `match` après `commun.md`. Case E4 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-match/SKILL.md`
- `.claude/skills/sixzeroleague-joueurs/SKILL.md`
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (§ 3 et 5 : aléa des résultats, affinités entre équipes, discipline)

## Règles propres au jeu
1. Résultats encore très aléatoires et « affinités » entre équipes [Dev chat] : un enseignement n'est « confirmé » qu'à partir de **3 matchs de ligue** dans le même sens.
2. Ligue et coupe se distinguent : coupe sur terrain neutre, sans avantage du terrain [W:Competitions].
3. Matchs joués avant la mise à jour des statistiques : seul le score existe [Dev chat].

## Données
- `silver.sz_fixtures` (`is_mine`, `status`, scores, adversaire, bot) et `silver.sz_standings` (`form`, points, buts).
- Matchs (`sql/silver/011_sz_matches.sql`, 2026-10-19) : `silver.sz_matches` (une ligne par match vu de mon équipe : score, tirs, % de réussite, arrêts, pertes, exclusions, 7 m, possession), `silver.sz_match_players` (stats par joueur, `is_mine`), `silver.sz_match_incidents` (buts, exclusions, cartons, mi-temps, dans l'ordre, `clock_s`). Source : endpoint `/matches/<id>/stats`, capturé en ouvrant la page du match (icône à droite du match dans League).
- Un match absent de `sz_matches` mais terminé dans `sz_fixtures` = export à demander. Les blessures n'apparaissent pas dans les incidents : les lire dans `sz_players.injured`.
- `/seasons/current/teams/<id>/player-stats` existe en bronze (`silver.sz_api`, champ `endpoint`) : stats de saison par joueur, à lire si besoin.

## Livrable
1. Explication de chaque nouveau match (3 à 6 lignes).
2. Journal `outputs/sixzeroleague/learnings.md` (le créer au premier match : en-tête « Dernier match analysé », Journal des matchs, Enseignements, Conseils).
3. Contrôle des conseils ouverts (`C-nnn`).

## Sortie propre au jeu
- Si un match manque, demande l'export de la page du match une fois celui-ci terminé (coups d'envoi 13:00 et 21:00, Paris).

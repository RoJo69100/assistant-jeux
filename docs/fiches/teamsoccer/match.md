# Team Soccer — fiche Match

Lue par l'agent `match` après `commun.md`. Case E4 de la checklist Team Soccer.

## Skills à lire
- `.claude/skills/teamsoccer-match/SKILL.md` (moteur v3, effets des formations et du style, duels, barres de secteurs, moral)
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (notes 0,5–10 dans le sous-rôle naturel, Forme, cartons, blessures)

## Règles propres au jeu
1. Le moteur v3 décide action par action par des duels (Conduite contre Défense, Finition contre Gardien…) multipliés par la Forme [skill match]. Explique un résultat par ces duels, la Forme et le style, pas par l'OVR seul.
2. Une note basse peut venir d'un joueur **hors de son sous-rôle naturel** [skill joueurs].
3. Contre un bot, une victoire ne prouve presque rien (ils perdent plus de 90 % de leurs matchs).

## Données
- `silver.ts_matches` : `match_id`, `match_date_paris`, `competition` (ligue, coupe, barrage, amical, autre), `venue`, scores, `my_team_id`.
- `silver.ts_match_lineups` : ce que nous avions enregistré pour ce match (formation, style, consignes, banc).
- `silver.ts_standings` : classement recalculé depuis les matchs joués.
- `gold.ts_match_report` : une ligne par match exporté (page « match-viewer ») — buteurs et minutes, formation et style, actions et tirs des deux équipes, cadrés, efficacité, penaltys, ballons perdus (interception, mauvais contrôle, sortie), cartons, blessures, notes moyennes, secteurs (moyenne, gardien, zone la plus faible), affluence.
- `gold.ts_match_plays` : une ligne par action (minute, nombre de phases, issue, dernier acteur) ; `silver.ts_match_events` pour le détail (acteur et passeur de chaque phase).
- `gold.ts_player_match_ratings` : par joueur, notes, buts, implication, ballons perdus sur les matchs exportés.
- ⚠️ **Notes et secteurs dépendent de la composition, pas du déroulé** (constat du 2026-10-19 : notes identiques à composition égale, 7,3 avec ou sans triplé). Ils mesurent la force de chaque emplacement, comme les barres de secteurs ; la performance du jour se lit dans les événements (tirs, buts, ballons perdus).
- Si un match n'a pas de ligne dans `gold.ts_match_report`, demande l'export de sa page « match-viewer » (script actif) et limite l'analyse au score, à la composition et à la Forme d'avant-match.

## Livrable
Explication du match chiffres à l'appui, puis mise à jour de `outputs/teamsoccer/learnings.md` (créer le fichier au premier match, sur le modèle BasketVibe) : enseignements `L-nnn`, conseils `C-nnn` et contrôle des conseils passés.

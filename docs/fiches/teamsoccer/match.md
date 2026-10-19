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
- **Pas encore capté** : notes des joueurs, secteurs, événements, affluence (checklist B4). Si le match n'a que son score, demande l'export de la page du match (rapport final) avec le script actif, et limite l'analyse au score, à la composition et à la Forme d'avant-match.

## Livrable
Explication du match chiffres à l'appui, puis mise à jour de `outputs/teamsoccer/learnings.md` (créer le fichier au premier match, sur le modèle BasketVibe) : enseignements `L-nnn`, conseils `C-nnn` et contrôle des conseils passés.

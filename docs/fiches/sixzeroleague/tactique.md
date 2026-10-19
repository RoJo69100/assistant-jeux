# Six Zero League — fiche Tactique

Lue par l'agent `tactique` après `commun.md`. Case E3 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-match/SKILL.md` (match, exclusions, cartons, jeu passif, avantage du terrain)
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (compétences clés par rôle, hors-poste, remplaçants, blessures)
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (§ 5 : discipline, pas encore de réglage d'agressivité)
- puis `outputs/sixzeroleague/learnings.md` s'il existe

## Règles propres au jeu
1. Ce qu'on règle à l'écran : **composition par défaut** (les 7 de chaque match), **un remplaçant par rôle**, formations d'attaque et de défense, places en défense (`defense_spots`) [W:Match, Injuries ; skill joueurs].
2. **Composition sûre par défaut** : chacun à un rôle principal ou appris (`gold.sz_lineup_natural`). Un hors-poste n'est proposé que s'il est justifié, avec le risque dit (note avant pénalité).
3. **Contrôle SQL avant de rendre** : 7 joueurs différents, un par rôle GK, CB, LB, RB, LW, RW, P ; aucun blessé ni suspendu (`injured`, `suspended`) ; remplaçants différents des titulaires. Donne le résultat dans le brief.
4. Défense : garder les places par défaut tant qu'aucun test ne justifie un changement (décision de l'utilisateur, 2026-10-18).

## Données
- `silver.sz_tactics` : composition actuelle (`kind` titulaire / remplaçant, `slot`, `player_id`), `attack_formation`, `defense_formation`, `defense_spots`, `auto_filled`.
- `gold.sz_lineup_natural`, `gold.sz_slot_options`, `silver.sz_players` (noms, compétences, disponibilité).
- `silver.sz_fixtures` (`is_mine`, `status`, `round`, adversaire, bot ou non) et `silver.sz_standings` : prochain adversaire et son classement.
- Pas encore de stats de match en silver (checklist C) : pas d'ajustement à l'adversaire fondé sur ses joueurs.

## Livrable
1. **Fiche de saisie** : rôle → titulaire, rôle → remplaçant, formations attaque / défense.
2. **Prochain adversaire** : rang, bilan, bot ou humain, et 0 à 2 changements justifiés.
3. **Blessés et suspendus** : qui manque, qui le remplace (sans pénalité si possible).

## Sortie propre au jeu
- En tête du brief : la fiche de saisie et la date limite (coup d'envoi suivant : 13:00 ou 21:00, Paris).
- Si `silver.sz_tactics.day` ou `silver.sz_players.as_of` est périmé, demande l'export de la page Équipe → Tactics.

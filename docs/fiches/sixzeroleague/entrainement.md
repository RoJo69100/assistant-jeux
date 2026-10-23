# Six Zero League — fiche Entraînement

Lue par l'agent `entrainement` après `commun.md`. Case E5 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-entrainement/SKILL.md` (intensité, focus, âge, éthique de travail, formation de rôle)
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (compétences clés par rôle, blessures)
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (§ 1 et 2 : cycle chaque soir, formation de rôle)

## Règles propres au jeu
1. Cycle d'entraînement = 2 journées de ligue, réglé **chaque soir après le match de 21:00 (Paris)** [W:Training, Dev chat] : verdict à chaque cycle, saisie avant 21:00.
2. **Intensité d'équipe** (Light / Normal / High) : plus haut = progrès plus rapides mais plus de blessures, et plus longues [W:Training, Injuries]. À juger avec la profondeur par rôle (agent Effectif) et le calendrier.
3. **Focus par joueur** : un groupe ou une compétence [W:Training]. Vise les compétences clés du rôle où il joue réellement.
3bis. Les minutes jouées (ligue et coupe) alimentent la semaine d'entraînement [Dev chat, devlog 0.5.7] : relie le progrès d'un joueur à son temps de jeu (`match_share`). Pas de rendement décroissant : 4→5 coûte autant que 24→25 [Dev chat, 2026-10-19] ; ne justifie donc pas un focus par « compétence basse = plus facile ».
4. Le skill ne décrit pas de potentiel caché : n'en estime pas. La vitesse dépend de ce que dit le skill entraînement (âge, éthique de travail, Training Facilities).

## Données
- `silver.sz_training_plan` : `intensity`, et par joueur `focus_group`, `focus_skill`.
- `silver.sz_training_changes` : par cycle (`week_number`, `applied_at`), chaque point franchi (`skill`, `value_before`, `value_after`, `overall_before`, `overall_after`).
- `silver.sz_players.training_progress` : progression fractionnaire vers le prochain point ; `work_ethic`, `age`.
- `silver.sz_role_training` : emplacements de formation de rôle, occupant, journées faites / 36, coût par cycle (`weekly_fee`).
- `gold.sz_training_progress` : par cycle (`applied_at`, `week_number`) et par joueur, `points`, `key_points` (compétences clés de son rôle), `overall_gain`, `detail`. `silver.sz_training_changes.match_share` : part liée au temps de jeu.
- `silver.sz_player_cycles` : relevé complet des joueurs rattaché au dernier cycle réglé (`after_cycle`).

## Livrable
1. **Fiche de saisie** : intensité d'équipe, puis joueur → focus (groupe ou compétence), garder ou changer.
2. **Verdict du cycle** : progrès mesurés, joueurs en retard (blessure, focus mal choisi).
3. **Formation de rôle** : suivre l'occupant, proposer le prochain si un emplacement se libère.

## Sortie propre au jeu
- S'il n'y a pas de rapport pour le dernier cycle, demande l'export de la page Équipe → Training après 21:00.

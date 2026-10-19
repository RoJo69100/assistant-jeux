# Six Zero League — fiche Effectif

Lue par l'agent `effectif` après `commun.md`. Case E2 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (rôles, compétences clés par rôle, hors-poste, blessures, retraite)
- `.claude/skills/sixzeroleague-entrainement/SKILL.md` (âge, éthique de travail, formation de rôle, U18)
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (rythme réel, formation de rôle)

## Données
- `silver.sz_players` : dernier relevé par joueur. `role`, `secondary_roles` (rôles appris), `age`, `height_cm`, `preferred_hand`, `overall`, `wage`, `injured`, `suspended`, `retiring`, `for_sale`, les 20 compétences à plat (`work_ethic` … `positioning`), `role_overalls` (note à chaque rôle, avant pénalité), `training_progress` (progression fractionnaire), `as_of`.
- `gold.sz_lineup_natural` : par rôle, les joueurs qui y jouent **sans pénalité**, classés (`rank_in_slot`). Sert à mesurer la **profondeur** réelle.
- `gold.sz_slot_options` : toutes les options par rôle, hors poste compris (`no_penalty`).
- `silver.sz_role_training` : formation de rôle en cours (joueur, rôle appris, journées faites / 36).
- `silver.sz_training_changes` : points gagnés par cycle (vitesse de progression).
- `gold.sz_role_report` : bilan par rôle, une ligne par joueur sans pénalité (`rank_in_slot`, `rating`, `key_skills_avg`, `key_skills`, `age`, `wage`, `wage_per_point`, `available_depth`, `no_natural_backup`, `retiring`, `as_of`).
- `gold.sz_training_progress` et `silver.sz_player_cycles` : progression par cycle.
- Stats de match : `silver.sz_match_players` (buts, tirs, arrêts, exclusions par joueur).

## Livrable
1. **Bilan par rôle** (GK, CB, LB, RB, LW, RW, P) : titulaire et remplaçant sans pénalité, note au rôle, compétences clés du rôle (skill joueurs § Compétences clés par rôle), âge, salaire. Signale les rôles **sans remplaçant naturel** : effectif de match de 10 [W:Introduction], un remplaçant par rôle [W:Injuries].
2. **Meilleurs et moins bons** : top 3 et bas 3 (note au rôle, salaire par point de note), complété par les stats de match (`silver.sz_match_players`).
3. **3 actions concrètes** : leviers propres au jeu — focus d'entraînement, intensité, formation à un 2e rôle (Training Facilities ≥ 5, 2 saisons, 3 rôles au maximum [W:Training, Dev chat]), achat ou vente, prospect U18.
4. **Projection** en saisons de 9 à 11 jours : bonus jeune jusqu'à 20 ans, baisse dès 28, déclin physique dès 30, retraite possible dès 33 (skills entraînement et joueurs). Annonce de retraite = encore une saison, invendable [W:Retirement, Transfers].

## Sortie propre au jeu
- Si `as_of` est antérieur au dernier cycle réglé (la veille au soir), demande l'export de la page Équipe → Players.

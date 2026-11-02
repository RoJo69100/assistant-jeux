# Six Zero League — fiche Effectif

Lue par moi (session principale) après `resume.md` : l'agent `effectif` est retiré depuis le 2026-11-02 (étape 0d), son travail = les vues gold ci-dessous + ce livrable, sans brief d'agent. Case E2 de la checklist SixZero League.

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
Rotation : un joueur utilisé progresse plus vite (minutes d'entraînement) ; signale les jeunes jamais alignés qui perdent ce gain [Dev chat, devlog 0.5.7]. Un joueur à forte éthique de travail peut se garder pour le revendre cher si les Training Facilities sont hautes (avis du développeur, 2026-10-11).
4. **Projection** en saisons de 9 à 11 jours : bonus jeune jusqu'à 20 ans, baisse dès 28, déclin physique dès 30, retraite possible dès 33 (skills entraînement et joueurs). Annonce de retraite = encore une saison, invendable [W:Retirement, Transfers].

## Sortie propre au jeu
- Si `as_of` est antérieur au dernier cycle réglé (la veille au soir), demande l'export de la page Équipe → Players.

## Surplus par rôle (règle du 2026-10-23)
Avant de proposer de vendre un joueur « en trop » à un poste (ex. 3 RW), lire ses `role_overalls` sur **tous** les rôles (`silver.sz_players`) : un joueur dont la note ailleurs, après la pénalité de hors-poste (−20 % attaque, −10 % défense, −20 % champ au but, [Dev chat 2026-10-13/20]), égale ou dépasse le remplaçant naturel d'un rôle mince (aujourd'hui LB et CB) est une couverture, pas un surplus. Ne le vendre que si aucun rôle mince ne dépend de lui. Cas du 2026-10-23 : Lemaire (RW 8, salaire 90) vaut LB 10 et CB 10 avant pénalité, contre 8 pour Leroy et Denis : à garder.

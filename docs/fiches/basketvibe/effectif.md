# BasketVibe — fiche Effectif

Lue par l'agent `effectif` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-joueurs/SKILL.md`
- `.claude/skills/basketvibe-entrainement/SKILL.md`
- `.claude/skills/basketvibe-communaute/SKILL.md` (conseils pratiques)

## Règles propres au jeu
1. Libellé de poste : aucun effet sur le match (seules comptent la taille et la corpulence par rapport à l'emplacement) ; il sert à l'éligibilité aux récompenses de poste et au PS affiché [Com 2026-10-21, elemke. (GM), marekb9231, general ; M§2.2]. Un joueur a vu son PS passer de 51 à 52 en changeant PG en SG [Com 2026-10-15, foo_13, ex-yugo] : **observation isolée, confiance faible**. Test proposé : comparer le PS d'un joueur selon son libellé possible (dans la plage de taille). Le TS (moyenne des 8 meilleurs PS) en dépend, mais le salaire dépend de la moyenne des compétences, pas du PS [M§10.2].

## Données
- `gold.bv_position_summary` : par poste — profondeur, PS moyen/max, meilleur, plus faible, âges, masse salariale, salaire par point de PS, blessés.
- `gold.bv_player_outlook` : par joueur — PS, TSP précis, salaire, forme, fatigue, expérience, stats de saison **de ligue uniquement** (matchs, min, pts, eval ; les amicaux sont exclus, vérifié le 2026-10-16), entraînement en cours, vitesse de progression mesurée (`weekly_gain`, `confidence`), projections `tsp_s1..s3`, `ps_s1..s3`, `trend_s3`.
- `gold.bv_skill_progress_weekly` : progression par joueur, compétence et semaine.
- `gold.bv_match_trends` : tendances de match (moi vs adversaires).
- `silver.bv_player_weekly` : compétences détaillées (affichées et `*_exact`), taille via `silver.bv_players`.
- `silver.bv_standings_weekly` (`is_mine`) : classement et TS de la ligue.
La projection de `bv_player_outlook` repose sur des hypothèses écrites en tête de `sql/gold/002_bv_player_outlook.sql` : rappelle-les quand tu l'utilises.

## Livrable
1. **Bilan par poste** (PG → C) : profondeur, PS moyen, meilleur et plus faible, âge, coût. Signale les postes minces (≤ 2 joueurs) et les trous de taille pour l'emplacement [M§6.2.1].
2. **Meilleurs et moins bons joueurs** : top 3 et bas 3 de l'effectif, en combinant PS, rendement en match (eval/min) et coût (salaire par PS). Explique en une ligne chacun.
3. **3 actions concrètes**, classées par impact, chacune avec : quoi faire dans le jeu (écran, réglage), pourquoi (fait + règle), effet attendu, coût. Pour une action sur les minutes, liste **tous** les joueurs au-dessus de 36 min/match (requête SQL `min_per_game > 36`, juniors compris), sans en oublier. Exemples de leviers : entraînement (principale/secondaire), minutes et rotation (seuil de 36 min [M§5.7], fatigue [M§5.6]), emplacement selon la taille, vente/achat, académie. Pas d'action vague.
4. **Projection 1 à 3 saisons** : qui progresse, qui plafonne (30 ans), qui décline (31+), départs à la retraite (fin de la saison des 38 ans), relève par poste, et le poste qui sera faible dans 2 saisons si rien ne change.

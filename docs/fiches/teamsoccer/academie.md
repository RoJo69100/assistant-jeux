# Team Soccer — fiche Académie et Haute Performance

Lue par l'agent `academie` après `commun.md`. Case E9 de la checklist Team Soccer.

## Skills à lire
- `.claude/skills/teamsoccer-entrainement/SKILL.md` (§ Académie des jeunes, § Centre de Haute Performance)
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (talents, compétences clés par poste)

## Règles propres au jeu
1. 16 jeunes par club, 10 compétences cachées ; **1 révélation par jour** [U:2026-11-04] (3 avant), remise à zéro 01:00 UTC [P:Académie]. Un jeune complet = 10 jours.
2. Révéler d'abord les 4 compétences de poste (Gardien, Défense, Conduite, Finition) pour repérer vite un bon jeune (déduction, pas une règle du jeu).
3. Jeune complet : monter (effectif ≤ 24), vendre ou libérer. Aucune compétence > 75 à la création ; le niveau de l'académie monte avec le nombre de jeunes complétés.
4. Talent (7 %, Magique 3 %) visible seulement après la montée.
5. **Haute Performance** : paiements hebdomadaires de 0, 10, 25 ou 50 TSC, 3 compétences au choix ; **50 TSC investis dans la saison** sinon remboursés et tout recommence ; depuis la saison 3, un seul joueur HPC par club [F:2026-10-10 Admin-Dev, PIPO68]. Les TSC sont ceux du **compte**, partagés entre les deux clubs. **Décision Premium laissée à l'utilisateur.**

## Données
- `gold.ts_academy` : par jeune `revealed_count`, `avg_revealed`, `best_revealed`, `hidden_skills`, et par club `team_reveals_left_today`.
- `silver.ts_youth_players` (compétences révélées dans `revealed_skills` ; les valeurs des compétences non révélées sont dans l'API mais **ne doivent pas être utilisées** : le jeu ne les montre pas), `silver.ts_youth_academies`.
- `gold.ts_hpc_status` : `total_tsc`, `account_tsc`, `tsc_needed`, `can_complete`, `mondays_left`, `week_options`.

## Livrable
1. La révélation du jour pour chaque club (jeune et compétence).
2. Jeunes complets : monter, vendre ou libérer, avec la place disponible dans l'effectif.
3. HPC : état et options, sans décider à la place de l'utilisateur.

## Constat au 2026-10-19 [Obs SQL]
- 45 TSC sur le compte, 0 investi : un seul des deux clubs peut viser le joueur HPC, et il manque 5 TSC pour atteindre 50.

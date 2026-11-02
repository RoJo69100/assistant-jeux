# Journal des enseignements — Hardwood (Eureka Red Devils, #940, conférence VI.26, D3)

Tenu par l'agent Match (`.claude/agents/match.md`). Créé le 2026-11-02 (plan de conception iso BasketVibe) à partir des registres `fait-2026-10-30.md` et `fait-2026-11-02.md` ; aucun brief d'agent Hardwood à cette date.

**Dernier match analysé : aucun match analysé un par un.** Prochaine étape (agent Match) : lire `gold.hw_season_games` et `gold.hw_vd_compare` (toute la saison hors conférence), vérifier L-001 et contrôler C-001 à C-004.

## Journal des matchs
Saison en cours : 3 exhibitions + matchs hors conférence ; conférence à partir du 2026-11-01 (`gold.hw_today`). Bilan à relire dans `gold.hw_today.bilan` (non relevé dans ce fichier).

## Enseignements
<!-- L-nnn · date · enseignement · matchs à l'appui · statut (à surveiller / confirmé / infirmé) · source. Seuil de confirmation : 3 matchs officiels dans le même sens [H]. Résultat = my_result de la base. -->
| ID | Date | Enseignement | Matchs | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-11-02 | Plan Pace 0, Emphasis o, Zone 65 %, Pressure 15 %, Extend 0, Staggered C : 7 victoires jouées avec ce plan (déclaré). À vérifier match par match dans `gold.hw_season_games` (my_pace, my_zone_pct, my_pressure_pct, my_extend, my_sub_mode, my_result). | 7 (déclaré) | à vérifier | `fait-2026-11-02.md` |
| L-002 | 2026-11-02 | Recrutement : une recrue déjà engagée chez nous (Nelson Sturgeon, PG) a été proposée comme cible ; une recrue « C » de 1,91 m (K.J. Simon) est un SG de jeu. Toujours lire `silver.hw_recruiting` (engagés) et `height_m` avant de proposer. | — | confirmé (correction du 02/11) | `fait-2026-11-02.md` ; `silver.hw_recruiting` 14:39 UTC |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut · effet -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-11-02 | Contre Wartburg (02/11 18:00 Paris) : garder le plan de L-001 ; si défaite, tester Extend −2 et Pressure 20 % | `select game_day, opponent, my_result, my_margin, my_extend, my_pressure_pct, opp_three_pct, opp_rim_pct from gold.hw_season_games where opponent ilike '%Wartburg%'` | à contrôler | — |
| C-002 | 2026-11-02 | Remplacer par poste les SR qui partent : Corey (PG) → Sturgeon (déjà engagé), Barbieri (PF) → Woodling, Harkins (SF) → Tolliver ; Simon (SG) remplace Adkins | `select prospect, our_interest, we_offered, contacts from gold.hw_recruit_board where prospect in ('Donald Woodling','Lyle Tolliver','K.J. Simon')` ; engagement à suivre | à contrôler | — |
| C-003 | 2026-10-30 | Depth chart SG et C titulaires selon `gold.hw_depth_suggest` | `select depth, pos, propose, actuel, controle from gold.hw_depth_suggest` : `controle` = ok | à contrôler | — |
| C-004 | 2026-10-30 | Jessie Schmidt assistant à la place de Major Brady | `silver.hw_coaches` : Schmidt présent | à contrôler | — |

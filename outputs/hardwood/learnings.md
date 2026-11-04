# Journal des enseignements — Hardwood (Eureka Red Devils, #940, conférence VI.26, D3)

Tenu par l'agent Match (`.claude/agents/match.md`). Créé le 2026-11-02 (plan de conception iso BasketVibe) à partir des registres `fait-2026-10-30.md` et `fait-2026-11-02.md`.

**Contrôle du 2026-11-02 fait (base lue) : voir `briefs/2026-11-02-match.md`.** Saison : 7 W – 7 L. Série en cours : 3 défaites, toutes avec le plan modifié (Extend −2).

**Dernier match analysé : aucun match analysé un par un** (bilan global dans le brief). Prochaine étape : un match à la fois avec `gold.hw_vd_compare` et `gold.hw_adversaires`.

## Journal des matchs
14 matchs en base (`gold.hw_season_games`, jusqu'au 2054-11-26 en date de jeu) : 3 exhibitions (3 L), 10 hors conférence (7 W, 3 L), 1 conférence (1 L, Austin College −13). Résultat = `my_result` de la base.

## Enseignements
<!-- L-nnn · date · enseignement · matchs à l'appui · statut (à surveiller / confirmé / infirmé) · source. Seuil de confirmation : 3 matchs officiels dans le même sens [H]. Résultat = my_result de la base. -->
| ID | Date | Enseignement | Matchs | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-11-02 | Plan Pace 0, Emphasis o, Zone 65 %, Pressure 15 %, Extend 0, Staggered C : **7 W et 4 L** sur 11 matchs (pas 7 victoires sur 7). Les 4 L : 3 exhibitions (−22, −10, −4) et Academy of Art (−11). | 11 | corrigé (vérifié en base) | `gold.hw_season_games` |
| L-002 | 2026-11-02 | Recrutement : lire `height_m` avant de proposer (K.J. Simon, 1,91 m, est étiqueté C). Sturgeon (PG) : cible, offre non faite ; « déjà engagé » non confirmé en base. | — | partiel | `gold.hw_recruit_board` ; `fait-2026-11-02.md` |
| L-003 | 2026-11-02 | Après changement du plan (Pressure 20 / Extend −2, puis Zone 35 / Extend −2) : 0 W – 3 L (−12, −9, −13). Contre le plan d'origine : 7 W – 4 L. Adversaires plus forts à Austin (WSI 139,1 contre 125,9). | 3 | à surveiller [H] (seuil 3 matchs atteint, mais adversaires non appariés) | `gold.hw_season_games` |

| L-004 | 2026-11-04 | Retour au plan d'origine (Extend 0, Pressure 15, Zone 65) après les 3 L : **3 W** (Wartburg +17, Lehigh +7, Wisconsin-Parkside +4). Wartburg est une victoire en base, pas une défaite. Bilan : 10 W – 7 L au total ; les 7 L = 3 exhibitions, Academy of Art, et les 3 matchs à Extend −2. | 17 | à surveiller (marges serrées : +7, +4) | `gold.hw_season_games` |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut · effet -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-11-02 | Contre Wartburg (02/11 18:00 Paris) : garder le plan de L-001 ; si défaite, tester Extend −2 et Pressure 20 % | `select game_day, opponent, my_result, my_margin, my_extend, my_pressure_pct, opp_three_pct, opp_rim_pct from gold.hw_season_games where opponent ilike '%Wartburg%'` | échoué (2026-11-02) | Wartburg absent de la base. Le test Extend −2 a été appliqué : 3 L de suite (Rutgers-Camden, Henderson State, Austin College). Réécrire : revenir au plan d'origine |
| C-002 | 2026-11-02 | Remplacer par poste les SR qui partent : Corey (PG) → Sturgeon (déjà engagé), Barbieri (PF) → Woodling, Harkins (SF) → Tolliver ; Simon (SG) remplace Adkins | `select prospect, our_interest, we_offered, contacts from gold.hw_recruit_board where prospect in ('Donald Woodling','Lyle Tolliver','K.J. Simon')` ; engagement à suivre | partiel | Woodling offert (3 contacts, Low) ; Tolliver offert (4 contacts, Low) mais verdict « écarter (pot ≤ 10) » ; Simon offert (8 contacts, Low+) ; Sturgeon non offert |
| C-003 | 2026-10-30 | Depth chart SG et C titulaires selon `gold.hw_depth_suggest` | `select depth, pos, propose, actuel, controle from gold.hw_depth_suggest` : `controle` = ok | appliqué (SG, C titulaires) | SG Adkins ✔, C Howell ✔. Reste 🟧 : PF titulaire Barbieri blessé (proposé Young), C remplaçant Chance (proposé McCleary) |
| C-004 | 2026-10-30 | Jessie Schmidt assistant à la place de Major Brady | `silver.hw_coaches` : Schmidt présent | appliqué | Schmidt assistant (relevé 2026-11-01 08:28 UTC), Brady absent |

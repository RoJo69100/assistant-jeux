# Journal — registre du Match Engine (Hockey Nation)

Créé le 2026-11-06. Critères écrits AVANT tout calcul (commit seul). Le script `pipelines/match_engine_etat.py` les applique tels quels ; tout changement de critère passe par une ligne datée ici.

## Ce que contient la base (lu le 2026-11-06, avant calcul)
Source : `silver.hn_game_detail` (un match par ligne) jointe à `silver.hn_games` (`team_level`, `game_type`, `my_result`, `home_is_mine`, `away_is_mine`).
| Équipe | Saison | Matchs détaillés en base | Remarque |
|---|---|---|---|
| PRO | S26 | 33 (30 ligue : 21 V ; 3 playoffs : 0 V) | choix de l'utilisateur |
| PRO | S27 | 5 ligue (2 V) + 2 amicaux (2 V) | choix de l'utilisateur ; les amicaux ne comptent pas comme ligue |
| FRM, U21, U17 | S27 | 5 ligue chacune (3 V, 3 V, 3 V) | lignes automatiques : « expérience sans notre choix » |
| FRM, U21, U17 | S26 | 0 | rien à compter |

Champs lisibles (vérifiés sur un match) :
- `teams.{home,away}.stats` : pim, hits, shots, bigHits, faceoffs, giveaways, takeaways, xGoalsFor, possession, ppAttempts, blockedShots, penaltyTotal. **`ppGoals` et `shGoals` ne sont pas dans cet exemple** : le script les compte dans `summary.scoring[].strength` (EVEN / PP / SH / PS).
- `summary.scoring[]` : période, temps de jeu, équipe, buteur, passeurs, `strength`, score après le but. `summary.penalties[]` : type, minutes, période, temps, joueur.
- `periods[]` : buts et tirs de chaque équipe par période (pas de gardien nommé : le % d'arrêts par période d'un gardien n'est lisible que si ce gardien joue les 3600 s).
- `boxscore[joueur]` : toi, goals, assists, shots, diff (plus/moins), pim, hits, takeaways, giveaways, tiredness, faceoffsWon/Lost ; gardien : toi, saves, shotsFaced, goalsAgainst, tiredness.
- `players` (capitaine), `coaches` (ratings), `stars`, `events`.
- **Il manque** : les joueurs sur la glace à chaque tir ou but (donc rien par ligne ou unité), le marqueur « filet vide », l'heure de saisie de la lineup, les lineups réellement alignées FRM/U21/U17.

## Règles de lecture (valables pour toutes les lignes)
- Équipes lues : PRO, FRM, U21, U17. Saisons : S26 et S27.
- Une règle qui demande des joueurs sur la glace par tir ou par unité est écrite « non mesurable : il manque X » et n'est jamais estimée.
- Matchs PRO = choix de l'utilisateur. Matchs FRM, U21, U17 : comptés à part, marqués « expérience sans notre choix ».
- Seuils de confiance (à valider) : **faible** si n < n requis ÷ 2 ; **moyenne** si n requis ÷ 2 ≤ n < n requis ; **solide** si n ≥ n requis. Verdict « confirmé » seulement en solide.
- n requis (à valider) : 10 matchs par groupe pour comparer victoires et défaites ; 20 matchs pour un effet de réglage isolé ; 5 pour un simple état des lieux (aucun verdict). Pour une règle de gardien : 10 matchs complets du gardien.
- Étape 2 (script, 2026-11-06) : « pour » et « contre » sont des nombres de matchs (ou de joueurs, ou de supériorités pour le PP) dont la mesure va dans le sens de la règle / à son encontre ; la colonne « mesure » donne les taux. Les règles de seuil (L-016 écart de 2 points en P3, L-018 .880, L-019 seuil PP, L-002 .870) sont jugées match par match, sauf le PP (taux de la saison en cours contre le seuil PP). Remplacé par les correctifs C1 à C5 ci-dessous pour les verdicts de taux. Un match sans `ppAttempts` est écarté du PP/PK (jamais compté 0). L-005 : seule la branche « arrêts < 60 % » est lue, verdict « partiel ».
- `learnings.md` contient L-001 à L-011 puis L-015 à L-019 : **L-012 à L-014 n'existent pas** (aucune ligne à écrire).

## Règles du journal des enseignements (outputs/hockeynation/learnings.md)
| Règle | Mesure exacte (requête) | Pour | Contre | n requis (à valider) | Mesurable avec la base |
|---|---|---|---|---|---|
| L-001 réalisation, pas volume | par match PRO ligue : buts ÷ tirs (`teams.stats.shots`, score de `silver.hn_games`), nous et eux, groupés par `my_result` | taux nous plus bas en D qu'en V ET taux adverse plus haut en D, tirs nous ≥ eux | tirs nous < eux en D, ou écart de taux < 2 points | 10 D et 10 V | oui pour le taux brut ; **le retrait du filet vide : non mesurable : il manque le marqueur « filet vide »** (taux brut annoncé comme tel) |
| L-002 gardien sous .870 en défaite | gardien du match : `saves ÷ shotsFaced` (boxscore), par `my_result` | arrêts < .870 dans la majorité des D et plus bas qu'en V | arrêts en D ≥ arrêts en V | 10 D | oui |
| L-003 fatigue du gardien, départs d'affilée | rang de départ d'affilée du gardien (ordre de `scheduled_at`, ligue seule) ; arrêts par rang | arrêts qui baissent avec le rang | arrêts stables ou qui montent | 20 apparitions (3 par rang au moins) | oui |
| L-004 mises au jeu | `faceoffsWon ÷ (Won+Lost)` somme des joueurs, par `my_result` | taux équivalent en V et en D (aucun lien) | écart ≥ 3 points entre V et D | 10 D et 10 V | oui pour l'équipe ; **« meilleur FOF des 5 sur la glace » : non mesurable : il manque la présence sur la glace par mise au jeu** |
| L-005 remplacement du gardien | gardiens du match dont `toi` < 3600 ; score à la sortie via `summary.scoring` (`goalsHome/Away`, `gameTime`) | sortie quand l'écart ≥ 3 en P1/P2 ou arrêts < 60 % | gardien resté malgré le critère (aucun cas) | 3 sorties pour constater, 10 pour conclure | oui (règle du jeu, vérification de conformité) |
| L-006 PP et PK | PP : buts `strength = 'PP'` de notre équipe ÷ `ppAttempts` nôtre ; PK : 1 − (buts PP adverses ÷ `ppAttempts` adverses) ; par `my_result` | PK plus bas en D qu'en V | PK équivalent | 10 D (≥ 25 supériorités adverses en D) | oui pour les taux ; **l'effet du PK sur le résultat : non mesurable : il manque les joueurs sur la glace par unité (hypothèse H)** |
| L-007 joueur clé muet | buts ÷ tirs d'un joueur (boxscore), D contre V, par joueur nommé | taux plus bas en D que V pour le même joueur | taux égal | 10 D et 10 V par joueur | oui (variation de réalisation seulement) |
| L-008 discipline (DSC) | `silver.hn_players.dsc` contre somme de `pim` du boxscore par joueur | PIM plus haut avec DSC bas, sur ≥ 5 joueurs par groupe | PIM indépendant du DSC | 20 matchs | oui pour PIM contre DSC ; **effet sur les résultats : non mesurable : il manque l'effet isolé d'un joueur sur la glace** |
| L-009 capitaine | `players.captain` du match, V/D par capitaine | % de V équivalent entre capitaines | écart ≥ 20 points avec n ≥ 10 par capitaine | 10 par capitaine | oui |
| L-010 contre-emploi | `diff` (plus/moins) du boxscore par joueur nommé, sur la période de contre-emploi | plus/moins par match ≥ 0 | plus/moins par match < −0,5 | 10 matchs par joueur | **plus/moins : oui ; effet du contre-emploi lui-même : non mesurable : il manque le même joueur à son poste naturel** |
| L-011 série contre Ottawa | tirs, PP/PK (scoring), gardien des 3 matchs de playoffs | mêmes causes que L-001/L-006 sur les 3 | PP/PK normaux | 3 (descriptif) : jamais de verdict | oui, descriptif |
| L-015 xG contre réussite | `xGoalsFor` nôtre et adverse ÷ buts, S27 contre défaites S26 | xG nous > eux et réussite < eux, en D | xG nous < eux | 10 D | oui |
| L-016 Kovalev recule en P3 | arrêts P3 = tirs adverses P3 − buts adverses P3 (`periods`) sur les matchs où le gardien joue 3600 s, par période | arrêts P3 < arrêts P1/P2 d'au moins 2 points | P3 ≥ P1/P2 | 10 matchs complets du gardien | oui, **filet vide compris dans P3** (le marqueur manque) ; gardien nommé seulement si un seul gardien a joué |
| L-017 PRO S27 : xG positif, résultats négatifs | xG, tirs, pertes de palet (`giveaways`), V/D, PRO ligue S27 | xG nous > eux et V < 50 % | xG nous < eux ou V ≥ 50 % | 10 matchs S27 | oui |
| L-018 Kovalev P3 en S27 | même mesure que L-016, S27 seulement | P3 S27 < .880 | P3 S27 ≥ .880 | 10 matchs complets | oui |
| L-019 PP S27 et buts en infériorité | PP : buts `strength='PP'` ÷ `ppAttempts` ; buts `strength='SH'` encaissés ; PRO et FRM S27 | PP au-dessus du seuil PP (voir C2) et SH encaissés faibles | PP sous le seuil PP ou SH encaissés répétés | 20 supériorités | oui |

## Hypothèses de la carte composition (docs/decisions/cartes/hockeynation/composition.md, variables 1 à 14)
| Hypothèse | Mesure exacte | Pour | Contre | n requis (à valider) | Mesurable avec la base |
|---|---|---|---|---|---|
| V1 lineup saisie ≥ 1 h avant le match, sinon −30 % | heure de saisie contre heure du match | match raté en cas de saisie tardive | aucun écart | 20 | **non mesurable : il manque l'heure de saisie par match** |
| V2 joueur hors poste −20 % | `gold.hn_saisie_lignes` (colonne `controle`) contre résultat | — | — | 20 | **non mesurable : il manque un match joué avec un joueur hors poste et un témoin** ; seul le contrôle « aucun hors poste » se lit |
| V3 endurance par unité (L1 7+, L2 6+, D1 8+, D2 6+) | `toi` et `tiredness` des joueurs du boxscore, regroupés par ligne saisie (`silver.hn_lineups`) | `tiredness` plus haut quand END sous le seuil | pas d'écart | 20 | **temps de glace et fatigue par ligne : oui ; effet de l'endurance sur les buts par unité : non mesurable : il manque les joueurs sur la glace par but** |
| V4 gardien titulaire | voir L-003, L-016, L-018 | idem | idem | idem | oui |
| V5 mises au jeu | voir L-004 | idem | idem | idem | oui |
| V6 power play (SHO + PAS + SKA, un FOF 7+) | taux PP équipe (L-006, L-019) | PP au-dessus du seuil PP (voir C2) | PP sous le seuil PP | 20 supériorités | **taux d'équipe : oui ; effet de la composition d'une unité : non mesurable : il manque les joueurs sur la glace par tir** |
| V7 infériorité (DEF + CHK + SKA + PWR) | taux PK équipe (L-006) | PK ≥ 80 % | PK < 76 % | 20 infériorités | **taux d'équipe : oui ; composition d'unité : non mesurable : il manque les joueurs sur la glace par tir** |
| V8 discipline | voir L-008 | idem | idem | idem | idem |
| V9 plan de jeu (shift length short) | `toi` par ligne, `diff` net des joueurs de L1 sur 10 matchs | plus/moins de L1 qui baisse après le passage à short | stable | 10 matchs avant, 10 après | **temps de glace et plus/moins net : oui ; « buts encaissés par L1 » : non mesurable : il manque les joueurs sur la glace par but** |
| V10 capitaine | voir L-009 | idem | idem | idem | oui |
| V11 case vide ou joueur parti (−5 %) | `gold.hn_saisie_lignes` (`controle <> 'ok'`) joint au résultat | — | — | 10 matchs avec case vide | **non mesurable : il manque des matchs joués avec case vide** |
| V12 test en amical | amicaux S27 (2 en base) | — | — | 20 | **non mesurable : il manque des amicaux avec un seul réglage changé** (2 amicaux : état des lieux seulement) |
| V13 FRM/U21/U17 : poste principal | lignes alignées | — | — | 20 | **non mesurable : il manque les lignes réellement alignées FRM/U21/U17** |
| V14 avis des amis | sources Discord | — | — | — | **non mesurable : avis, pas une donnée de match** |

## Correctifs du 2026-11-06 (critères écrits avant le code)
- **C1 intervalle de Wilson.** Pour tout verdict sur un taux (PP, PK, arrêts, réalisation, mises au jeu), le script calcule l'intervalle de Wilson à 95 % (z = 1,96) sur les événements (buts sur supériorités, arrêts sur tirs, buts sur tirs). Taux comparé à un seuil fixe : « confirmé » si l'intervalle est entièrement du côté de la règle, « infirmé » s'il est entièrement de l'autre côté, sinon « indéterminé : n trop petit » avec l'intervalle affiché. Deux taux comparés entre eux (défaites contre victoires) : « confirmé » si les deux intervalles sont séparés dans le sens de la règle, « infirmé » s'ils sont séparés en sens inverse, sinon « indéterminé : n trop petit ». Le verdict ne vient plus du nombre de matchs. Test figé : 6 buts sur 26 supériorités contre le seuil PP donne « indéterminé ».
- **C2 seuil PP unique.** Une valeur, dans `SEUILS` de `match_engine_etat.py`, avec sa source ; le skill et ce journal la citent sans la recopier. **Tranché : 20,7 %** (29 buts sur 140 supériorités de la saison précédente, règle L-006) : c'est une mesure. Le 23 % vient de conseils (C-014, C-027, C-050) comme objectif posé sans mesure : il reste un objectif de ces conseils, pas le seuil du registre.
- **C3 règle retirée.** Le script lit `outputs/hockeynation/learnings.md` ET la table « Checks appris » de `docs/decisions/cartes/hockeynation/composition.md` : une règle marquée ⛔ ou « retirée » dans l'un des deux n'est ni mesurée ni affichée. Constat avant le code : `learnings.md` ne porte aucun ⛔ (L-009 y est « infirmé (pas d'effet visible) ») ; le ⛔ de L-009 est dans la carte composition. Test avec L-009.
- **C4 temps de glace par ligne.** Une requête joint `silver.hn_lineups` (lineup A, `line`, `player_id`) au boxscore (`toi`) : somme par ligne (L1 à L4, avec ses deux défenseurs = la paire), affichée par match PRO, la lineup retenue étant la dernière saisie avant le jour du match. Constat avant le code : `silver.hn_lineups` ne contient qu'un seul jour (2026-11-06), donc **aucun match déjà joué n'aura de lineup** : résultat attendu = une ligne « non mesurable : il manque la lineup en vigueur à la date du match ». La jointure ne donne ni les changements de ligne en cours de match, ni le temps par unité de jeu de puissance ou d'infériorité séparée.
- **C5 `sql.py`.** Docstring : pas de colonne nommée `t` dans la requête (alias de `public.sql_ro`) ; `jsonb_pretty`, ou `jsonb_agg` combiné à `jsonb_object_keys`, peuvent être bloqués par Cloudflare (403, page HTML). Aucune migration SQL.
- Comportement de `pipelines/aujourdhui.py` inchangé : ses tests restent verts.

## Ce qui sort du script (étape 2, rappel)
Tableau : règle | n matchs disponibles | pour | contre | n requis | confiance | verdict. Les matchs FRM, U21, U17 sont comptés à part. Aucune règle « non mesurable » n'a de chiffre : une seule ligne avec ce qui manque.

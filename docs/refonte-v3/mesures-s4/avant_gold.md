<!-- Mesure du 2026-11-05 avant la migration, faite AVANT la correction de la sonde de port de sql.py (+6,5 s par appel côté client). Les lignes « timeout » sont valides (20 s côté serveur, indépendant du client). Les deux valeurs numériques (match_objective derbymanager 7245 ms, hardwood 7405 ms) sont gonflées de 6,5 s : lire « non établi, environ 0,7 à 0,9 s » ne serait qu'une estimation, donc : non mesurable. -->
| vue | jeu | 1er passage (ms) | médiane (ms) | lignes | verdict |
| gold.season_context | basketvibe | timeout | timeout | None | ❌ |
| gold.season_context | derbymanager | timeout | timeout | None | ❌ |
| gold.season_context | hardwood | timeout | timeout | None | ❌ |
| gold.season_context | hockeynation | timeout | timeout | None | ❌ |
| gold.season_context | sixzeroleague | timeout | timeout | None | ❌ |
| gold.season_context | teamsoccer | timeout | timeout | None | ❌ |
| gold.match_objective | basketvibe | timeout | timeout | None | ❌ |
| gold.match_objective | derbymanager | 7245 | 7233 | 0 | ❌ |
| gold.match_objective | hardwood | 7405 | 9326 | 0 | ❌ |
| gold.match_objective | hockeynation | timeout | timeout | None | ❌ |
| gold.match_objective | sixzeroleague | timeout | timeout | None | ❌ |
| gold.match_objective | teamsoccer | timeout | timeout | None | ❌ |
| gold.daily_alerts | basketvibe | timeout | timeout | None | ❌ |
| gold.daily_alerts | derbymanager | timeout | timeout | None | ❌ |
| gold.daily_alerts | hardwood | timeout | timeout | None | ❌ |
| gold.daily_alerts | hockeynation | timeout | timeout | None | ❌ |
| gold.daily_alerts | sixzeroleague | timeout | timeout | None | ❌ |
| gold.daily_alerts | teamsoccer | timeout | timeout | None | ❌ |

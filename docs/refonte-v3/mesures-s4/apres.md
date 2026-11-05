<!-- Mesure du 2026-11-05 après la migration sql/core/013_vues_materialisees.sql.
Commande : SQL_TRANSPORT=https python -I pipelines/mesure_vues.py --vues <vues> --passes 3
Les 8 autres vues core.* (fixture, finance_daily, market_listing, academy_prospect, staff, training_plan, facility, season) ne sont pas touchées : leur mesure « avant » (avant_core.md, toutes < 2 s) reste valable. -->

| vue | jeu | 1er passage (ms) | médiane (ms) | lignes | verdict |
|---|---|---|---|---|---|
| core.standing | basketvibe | 1228 | 557 | 48 | ✅ |
| core.standing | derbymanager | 572 | 572 | 24 | ✅ |
| core.standing | hardwood | 467 | 455 | 16 | ✅ |
| core.standing | hockeynation | 364 | 364 | 20 | ✅ |
| core.standing | sixzeroleague | 262 | 262 | 10 | ✅ |
| core.standing | teamsoccer | 248 | 430 | 16 | ✅ |
| core.player_daily | basketvibe | 413 | 438 | 259 | ✅ |
| core.player_daily | derbymanager | 426 | 426 | 46 | ✅ |
| core.player_daily | hardwood | 450 | 449 | 20 | ✅ |
| core.player_daily | hockeynation | 254 | 417 | 590 | ✅ |
| core.player_daily | sixzeroleague | 262 | 280 | 136 | ✅ |
| core.player_daily | teamsoccer | 445 | 422 | 508 | ✅ |
| gold.season_context | basketvibe | 432 | 432 | 1 | ✅ |
| gold.season_context | derbymanager | 252 | 252 | 2 | ✅ |
| gold.season_context | hardwood | 484 | 445 | 1 | ✅ |
| gold.season_context | hockeynation | 272 | 299 | 1 | ✅ |
| gold.season_context | sixzeroleague | 305 | 408 | 1 | ✅ |
| gold.season_context | teamsoccer | 249 | 270 | 2 | ✅ |
| gold.match_objective | basketvibe | 1654 | 945 | 8 | ✅ |
| gold.match_objective | derbymanager | 287 | 389 | 0 | ✅ |
| gold.match_objective | hardwood | 290 | 325 | 0 | ✅ |
| gold.match_objective | hockeynation | 1035 | 609 | 25 | ✅ |
| gold.match_objective | sixzeroleague | 1533 | 755 | 12 | ✅ |
| gold.match_objective | teamsoccer | 4159 | 3895 | 6 | ❌ |
| gold.daily_alerts | basketvibe | 5115 | 7539 | 7 | ❌ |
| gold.daily_alerts | derbymanager | 5514 | 6974 | 3 | ❌ |
| gold.daily_alerts | hardwood | timeout | timeout | None | ❌ |
| gold.daily_alerts | hockeynation | 11902 | 11563 | 23 | ❌ |
| gold.daily_alerts | sixzeroleague | 9266 | 7370 | 13 | ❌ |
| gold.daily_alerts | teamsoccer | timeout | timeout | None | ❌ |

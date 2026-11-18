# BasketVibe — gain réel, relevé du lundi

Requête : `MESURE_SQL` de `pipelines/aujourdhui.py` (lue le 18/11/2026 16:10, heure de Paris). Pour chaque lundi, la dernière capture ≤ ce lundi.
- **Rang** : `core.standing` (`is_mine`).
- **Force moyenne** : PS moyen (`core.player_daily.rating`) des 7 joueurs qui ont le plus de minutes sur les 4 derniers matchs de ligue joués avant ce lundi (règle de `league_min_last4` ; minutes lues dans `silver.bv_match_player_stats`, `gold.bv_match_player_lines` dépasse le délai).
- **Trésorerie** : solde = `core.finance_daily.balance` ; capacite_invest = solde − 2 × charges de la semaine, formule de `gold.finance_health` appliquée au relevé (la vue ne garde que le dernier).
- Variation (±) : par rapport au lundi d'avant. Rang : + = place perdue.

| Semaine (lundi) | Rang | Force moyenne | capacite_invest | Solde | Captures (classement / joueurs / finances) |
|---|---|---|---|---|---|
| 16/11 | 8 (+1) | 54,7 (+0,2) | 585 181 (+534 250) | 1 494 431 (+534 250) | 13/11 / 16/11 / 13/11 — 4 matchs jusqu'au 14/11 |
| 09/11 | 7 (+5) | 54,5 (+0,3) | 50 931 (+164 699) | 960 181 (+111 175) | 08/11 / 09/11 / 08/11 — 4 matchs jusqu'au 07/11 |
| 02/11 | 2 (−6) ¹ | 54,2 (+2,9) | −113 768 (+17 085) | 849 006 (+26 013) | 01/11 / 02/11 / 01/11 — 4 matchs jusqu'au 26/10 |
| 26/10 | 8 (0) | 51,3 (+2,2) | −130 853 (−108 724) | 822 993 (−80 262) | 25/10 / 26/10 / 25/10 — 4 matchs jusqu'au 24/10 |
| 19/10 | 8 | 49,1 | −22 129 | 903 255 | 18/10 / 19/10 / 18/10 — 4 matchs jusqu'au 17/10 |
| 12/10 | illisible | illisible | illisible | illisible | aucune capture de classement, de joueurs ni de finances ≤ 12/10 |

¹ 01/11 : nouvelle saison, 0 match joué — rang sans valeur sportive ; la variation du 09/11 (+5) en hérite.

Suite : le plan du lundi (`python -I pipelines/aujourdhui.py`) écrit la ligne « Mesure de la semaine » ; ajouter ici une ligne chaque lundi.

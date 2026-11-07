# Hardwood — requêtes de la grille d'analyse de match (`docs/fiches/grille-match.md`)

Lecture par `python -I pipelines/sql.py "…"`. Notre équipe : Eureka Red Devils.

## 0. Intégrité
`silver.hw_game_box` ne garde que l'équipe à domicile (`side` = 1) : à l'extérieur, la feuille est celle de l'adversaire (vérifié le 2026-11-07 : Wartburg, Lehigh). Toujours filtrer `team_full like 'Eureka%'` ; nos stats joueur ne couvrent donc que les matchs à domicile.

## 1 et 2. Matchs et W/L : `gold.hw_season_games`
Colonnes : `my_result`, `my_margin`, `my_wsi/opp_wsi`, `my_tpi/opp_tpi`, tir par zone (`rim/in/mid/three` en `_pct` et `_a`, `opp_*`), plan (`my_pace`, `my_emphasis`, `my_zone_pct`, `my_pressure_pct`, `my_extend`), `opp_man/opp_zone/opp_press`, `my_injuries`, `my_overworked`. Agrégats W/L déjà prêts : `gold.hw_vd_compare`.

Corrélations, au plan actuel (adapter le filtre de plan) :
```sql
select count(*) n, corr(my_margin, my_wsi-opp_wsi) wsi, corr(my_margin, my_tpi-opp_tpi) tpi,
  corr(my_margin, opp_three_a) opp3a, corr(my_margin, opp_three_pct) opp3, corr(my_margin, opp_rim_pct) opprim,
  corr(my_margin, rim_pct) rim, corr(my_margin, three_a) my3a, corr(my_margin, three_pct) my3
from gold.hw_season_games where game_type <> 'Exhibition' and my_zone_pct = 65 and my_extend = 0
```
Repère du 07/11 (n = 14) : écart de WSI +0,77, de TPI +0,70, tirs à 3 adverses −0,70, notre rim +0,57.

## 3. Joueurs (domicile seulement)
```sql
select player, pos_played, count(*) g, round(avg(min),1) min, round(36.0*sum(pts)/sum(min),1) pts36,
  round(36.0*sum(tov)/sum(min),1) tov36, round(36.0*sum(pf)/sum(min),1) pf36,
  round(36.0*sum(plus_minus)/sum(min),1) pm36, count(*) filter (where fatigue = 'Mod') fatigue_mod
from silver.hw_game_box where team_full like 'Eureka%' group by 1,2 order by sum(min) desc
```
Force du prochain adversaire : `gold.hw_adversaires` (bilan, PF/PA, RPI) ; son WSI exige l'export `/statistics/<id>`.

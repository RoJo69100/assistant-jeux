# Journal des enseignements — Derby Manager (Queen of the South 547, Marmandes 307)

Tenu par l'agent Match (`.claude/agents/match.md`). Créé le 2026-11-02 (plan de conception iso BasketVibe) à partir du plan du 2026-10-30 (`briefs/2026-10-30-plan.md`, chiffres tirés ce jour-là de `gold.dm_matchs` et `gold.dm_saison_bilan`) et de la reprise du 2026-10-31 (`briefs/2026-10-30-reprise-demain.md`). Deux clubs : un bloc chacun, jamais de total.

**Contrôle du 2026-11-02 (base lue : `gold.dm_matchs`, `dm_effectif`, `dm_verdict_joueurs`, `dm_entrainement`, `dm_finances_bilan`, derniers exports 2026-11-01).** Résultat = `my_result` : W/D/L (D = nul, pas défaite). Sur 8 conseils : 6 non appliqués en base, 2 non testables (aucun match joué depuis le 30/10). Bilan 547 en base : 2 W, 4 D, 26 L ; 307 : 8 W, 10 D, 15 L. L-001 à L-004 recoupés avec la base : bilan 547 cohérent ; chiffres de formation et de forme non rejoués.

**Dernier match analysé : aucun match analysé un par un.** Seul le bilan de la saison 26 de Queen of the South est lu (32 matchs). Marmandes : aucun match en base au 2026-10-30. Prochaine étape (agent Match) : lire `gold.dm_matchs` depuis le 2026-10-30 pour les deux clubs et contrôler C-001 à C-008.

## Journal des matchs
### Queen of the South (547) — saison 26 (Écosse, Premier Division, 8 équipes, pas de relégation)
7e sur 8. 32 matchs : 2 V, 4 N, 26 D, 9 buts marqués, 80 encaissés ; ligue 1 V, 4 N, 23 D (4-69). Source : `gold.dm_saison_bilan`, `gold.dm_matchs` (2026-10-30).

### Marmandes (307) — France, D4
Aucun match en base au 2026-10-30 ; exports d'équipe reçus le 2026-10-31 (seul Graduates manque), non ré-exportés au 2026-11-01.

## Enseignements
<!-- L-nnn · date · enseignement · matchs à l'appui · statut (à surveiller / confirmé / infirmé) · source. Seuil de confirmation : 3 matchs dans le même sens [H, à fixer]. Résultat = my_result de la base. -->
| ID | Date | Enseignement | Matchs | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-11-02 | Queen of the South S26 : la défaite vient du volume, pas de la réussite : xG 0,43 pour contre 2,62 contre par match, 3,3 tirs pour contre 16,7 contre. Corriger la création (build up) et la prévention, pas la finition. | 32 | confirmé (saison entière) | `gold.dm_saison_bilan` (2026-10-30) |
| L-002 | 2026-11-02 | Queen of the South S26 par formation : 442 = 18 matchs, 1 V 4 N 13 D ; 352 = 10 matchs, 10 D. Le 352 est à écarter contre plus fort ; le développeur conseille 541 défensif contre plus fort. | 28 | confirmé (352) / à surveiller (541, pas encore joué) | `gold.dm_saison_bilan` ; dev #italy 2025-08-13, 2025-02-07 |
| L-003 | 2026-11-02 | Fin S26 : condition correcte (83 à 100 %) mais forme basse (FRM 13 à 37 chez Bjerg, Kjer, Vigerie, Schultze, Bock, Connelly, Ludig) malgré une rotation permanente. La forme ne monte qu'en jouant : tourner tout l'effectif empêche chacun de cumuler des matchs. | effectif de fin S26 | à surveiller [H] (à tester : garder un XI stable) | `gold.dm_verdict_joueurs` (2026-10-30) ; connaissance § 3 (dev 2026-10-21) |
| L-004 | 2026-11-02 | Marché exporté 0,3-7,5 M (259 joueurs) : aucun joueur dont le bas de fourchette dépasse nos titulaires (meilleur gain garanti −1,4). L'export suit le filtre de prix de l'écran : chercher plus haut (8-20 M) avant de conclure. | — | confirmé (export du 2026-10-30) | `gold.dm_marche_notes` ; `resume.md` § Pièges |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut · effet -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-10-30 | Queen of the South : formation 541 défensive (ligne Low, passes Direct, jeu Wide, tirs From box, seule option Counters) | `select jour, opponent, my_result, xgf, xga, tirs_pour, tirs_contre, formation from gold.dm_matchs where team_id = 547 and jour > '2026-10-30' order by jour limit 10` : xga < 2,62 et tirs contre < 16,7 en moyenne | non testable (2026-11-02) | Aucun match après le 2026-10-28 (547) / 2026-10-30 (307) dans `gold.dm_matchs`. À rejouer au prochain match. |
| C-002 | 2026-10-30 | Gardien Vigerie titulaire (Key, 75 % des matchs attendus) à la place de Kjer | `gold.dm_verdict_joueurs` : `temps_jeu_satisf_pct` de Vigerie ; Vigerie dans `gold.dm_effectif.slot` | non appliqué (2026-11-02) | Export du 2026-11-01 : Vigerie slot S3 (remplaçant), temps de jeu satisfait 0 % pour 75 % attendus ; Kjer GK titulaire (100 % satisfait pour 25 % attendus). |
| C-003 | 2026-10-30 | Mettre en liste de transfert Cooper et King ; prolonger Neufeld et Bjerg ; laisser partir Wilmot (repris le 31/10 : lister Vidales et King) | `gold.dm_effectif` : `contract_days` de Neufeld et Bjerg > 85 ; Vidales et King listés ou partis | non appliqué (2026-11-02) | Neufeld 40 j, Bjerg 46 j (pas prolongés, seuil 85) ; Cooper 24 j ; Vidales (68 j) et King (80 j) toujours dans l'effectif ; Wilmot (45 j) aussi. « Listé » non vérifiable dans la vue : à relever à l'écran. |
| C-004 | 2026-10-30 | Promouvoir Almgren (MR, 19 ans) de l'école ; garder Minkkinen | `silver.dm_school` : Almgren absent ; `gold.dm_effectif` : Almgren présent | non appliqué (2026-11-02) | Ni Almgren ni Minkkinen dans `gold.dm_effectif` (export du 2026-11-01) ; Almgren apparaît encore dans des exports d'école (5 pages sur 8). |
| C-005 | 2026-10-30 | Exporter le marché filtré 8-20 M et viser 1 ou 2 « Solid player » (24-27 ans, médiane 11,1 M ; 29-31 ans vers 8 M) | `silver.dm_market` : annonces de prix > 8 M en base | non appliqué (2026-11-02) | 1 seule annonce > 8 M en base ; dernier export marché 2026-11-01 09:38 UTC : le marché 8-20 M n'a pas été exporté. |
| C-006 | 2026-10-31 | Installations : payer les 8 M manquants (niveau 17), malgré « l'effectif avant les installations » (9 plaintes d'installations) | `gold.dm_finances_bilan.facilities_level` = 17 | non appliqué (2026-11-02) | Niveau 16 au 2026-11-01 09:37 UTC ; upgrade à 8 M, trésorerie 21,4 M (financé). |
| C-007 | 2026-10-31 | Entraînement : D → Anticipation, M → First Touch, F → First Touch, GK → Reaction ; intensités Connelly HIGH, Pilot / Vidales / Arneberg MED, Schultze LOW | `gold.dm_entrainement` : `gained` des groupes depuis le 31/10 | non appliqué (2026-11-02) | Réglages en base au 2026-11-01 : D = Positioning (pas Anticipation), M = Passing (pas First Touch), F = Shooting (pas First Touch), GK = Handling (pas Reaction). Gains/pertes : D +44/−21, M +15/−17, F +10/−3, GK +4/−4. |
| C-008 | 2026-10-31 | Garder un XI plus stable pour faire monter la forme (test de L-003) | `gold.dm_verdict_joueurs.forme` des titulaires en hausse après 5 matchs | non testable (2026-11-02) | Aucun match joué depuis le conseil. |

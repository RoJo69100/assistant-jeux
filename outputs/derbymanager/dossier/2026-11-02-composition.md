# Dossier derbymanager — composition — 2026-11-02 — carte + nouveau

1. **Carte** `docs/decisions/cartes/derbymanager/composition.md` : lis-la en entier. Chaque variable y a son endroit et son check : lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.
2. **Nouveau depuis le commit a0787e7** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.
3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).
4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py derbymanager composition --marquer`.

## Nouveau — règles, fiches, connaissance, learnings
### `outputs/derbymanager/learnings.md` — 10 lignes ajoutées, 7 sur le sujet
**Contrôle du 2026-11-02 (base lue : `gold.dm_matchs`, `dm_effectif`, `dm_verdict_joueurs`, `dm_entrainement`, `dm_finances_bilan`, derniers exports 2026-11-01).** Résultat = `my_result` : W/D/L (D = nul, pas défaite). Sur 8 conseils : 6 non appliqués en base, 2 non testables (aucun match joué depuis le 30/10). Bilan 547 en base : 2 W, 4 D, 26 L ; 307 : 8 W, 10 D, 15 L. L-001 à L-004 recoupés avec la base : bilan 547 cohérent ; chiffres de formation et de forme non rejoués.
| C-001 | 2026-10-30 | Queen of the South : formation 541 défensive (ligne Low, passes Direct, jeu Wide, tirs From box, seule option Counters) | `select jour, opponent, my_result, xgf, xga, tirs_pour, tirs_contre, formation from gold.dm_matchs where team_id = 547 and jour > '2026-10-30' order by jour limit 10` : xga < 2,62 et tirs contre < 16,7 en moyenne | non testable (2026-11-02) | Aucun match après le 2026-10-28 (547) / 2026-10-30 (307) dans `gold.dm_matchs`. À rejouer au prochain match. |
| C-002 | 2026-10-30 | Gardien Vigerie titulaire (Key, 75 % des matchs attendus) à la place de Kjer | `gold.dm_verdict_joueurs` : `temps_jeu_satisf_pct` de Vigerie ; Vigerie dans `gold.dm_effectif.slot` | non appliqué (2026-11-02) | Export du 2026-11-01 : Vigerie slot S3 (remplaçant), temps de jeu satisfait 0 % pour 75 % attendus ; Kjer GK titulaire (100 % satisfait pour 25 % attendus). |
| C-003 | 2026-10-30 | Mettre en liste de transfert Cooper et King ; prolonger Neufeld et Bjerg ; laisser partir Wilmot (repris le 31/10 : lister Vidales et King) | `gold.dm_effectif` : `contract_days` de Neufeld et Bjerg > 85 ; Vidales et King listés ou partis | non appliqué (2026-11-02) | Neufeld 40 j, Bjerg 46 j (pas prolongés, seuil 85) ; Cooper 24 j ; Vidales (68 j) et King (80 j) toujours dans l'effectif ; Wilmot (45 j) aussi. « Listé » non vérifiable dans la vue : à relever à l'écran. |
| C-004 | 2026-10-30 | Promouvoir Almgren (MR, 19 ans) de l'école ; garder Minkkinen | `silver.dm_school` : Almgren absent ; `gold.dm_effectif` : Almgren présent | non appliqué (2026-11-02) | Ni Almgren ni Minkkinen dans `gold.dm_effectif` (export du 2026-11-01) ; Almgren apparaît encore dans des exports d'école (5 pages sur 8). |
| C-006 | 2026-10-31 | Installations : payer les 8 M manquants (niveau 17), malgré « l'effectif avant les installations » (9 plaintes d'installations) | `gold.dm_finances_bilan.facilities_level` = 17 | non appliqué (2026-11-02) | Niveau 16 au 2026-11-01 09:37 UTC ; upgrade à 8 M, trésorerie 21,4 M (financé). |
| C-007 | 2026-10-31 | Entraînement : D → Anticipation, M → First Touch, F → First Touch, GK → Reaction ; intensités Connelly HIGH, Pilot / Vidales / Arneberg MED, Schultze LOW | `gold.dm_entrainement` : `gained` des groupes depuis le 31/10 | non appliqué (2026-11-02) | Réglages en base au 2026-11-01 : D = Positioning (pas Anticipation), M = Passing (pas First Touch), F = Shooting (pas First Touch), GK = Handling (pas Reaction). Gains/pertes : D +44/−21, M +15/−17, F +10/−3, GK +4/−4. |

## Nouveau — Discord / chat
- rien de nouveau.

## Recherche ciblée (Vigerie, Kjer, Neufeld, Bjerg, Almgren, installations, entraînement) dans tout l'historique
- 2 lignes → `outputs/derbymanager/dossier/2026-11-02-composition-cible.txt`, à lire en entier.

## Du jour
- registre `fait-` : absent
- exports : `bronze.raw_pages` where game = 'derbymanager' and captured_at >= '2026-11-02'

## Couverture (à remplir)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| carte (variables) | | | | |
| nouveau règles | | | | |
| nouveau Discord/chat | | | | |

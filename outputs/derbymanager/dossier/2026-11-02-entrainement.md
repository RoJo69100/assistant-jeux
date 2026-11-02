# Dossier derbymanager — entrainement — 2026-11-02 — carte + nouveau

1. **Carte** `docs/decisions/cartes/derbymanager/entrainement.md` : lis-la en entier. Chaque variable y a son endroit et son check : lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.
2. **Nouveau depuis le commit a0787e7** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.
3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).
4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py derbymanager entrainement --marquer`.

## Nouveau — règles, fiches, connaissance, learnings
### `outputs/derbymanager/learnings.md` — 10 lignes ajoutées, 2 sur le sujet
**Contrôle du 2026-11-02 (base lue : `gold.dm_matchs`, `dm_effectif`, `dm_verdict_joueurs`, `dm_entrainement`, `dm_finances_bilan`, derniers exports 2026-11-01).** Résultat = `my_result` : W/D/L (D = nul, pas défaite). Sur 8 conseils : 6 non appliqués en base, 2 non testables (aucun match joué depuis le 30/10). Bilan 547 en base : 2 W, 4 D, 26 L ; 307 : 8 W, 10 D, 15 L. L-001 à L-004 recoupés avec la base : bilan 547 cohérent ; chiffres de formation et de forme non rejoués.
| C-007 | 2026-10-31 | Entraînement : D → Anticipation, M → First Touch, F → First Touch, GK → Reaction ; intensités Connelly HIGH, Pilot / Vidales / Arneberg MED, Schultze LOW | `gold.dm_entrainement` : `gained` des groupes depuis le 31/10 | non appliqué (2026-11-02) | Réglages en base au 2026-11-01 : D = Positioning (pas Anticipation), M = Passing (pas First Touch), F = Shooting (pas First Touch), GK = Handling (pas Reaction). Gains/pertes : D +44/−21, M +15/−17, F +10/−3, GK +4/−4. |

## Nouveau — Discord / chat
- rien de nouveau.

## Du jour
- registre `fait-` : absent
- exports : `bronze.raw_pages` where game = 'derbymanager' and captured_at >= '2026-11-02'

## Couverture (à remplir)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| carte (variables) | | | | |
| nouveau règles | | | | |
| nouveau Discord/chat | | | | |

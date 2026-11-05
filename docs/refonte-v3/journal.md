# Journal refonte v3

Début : 2026-11-05. Plan : `docs/refonte-v3/plan.md`.

## S0 — Remise à plat (2026-11-05)

- [x] `plan-reprise.md` marqué « remplacé » — commit da76790. Preuve : `head -1 docs/refonte-v2/plan-reprise.md` → `> Remplacé par docs/refonte-v3/plan.md (2026-11-05)`.
- [x] `CLAUDE.md` inviolable 3 = Annexe C — commit 6cca59d, `git diff --stat` : 1 ligne changée, aucune autre modification.
- [x] Journal v3 : existait déjà (titre + date, commit bdd444d) ; section S0 ajoutée.
- [ ] Branches distantes. Commandes : `git fetch origin` puis `git rev-list --count origin/main..origin/<branche>` pour ccr-234fdf81-gea2pf, ccr-26f58e91-dqo8si, ccr-5554cafe-lzijjv, claude/test-mcp-gk62t9, refonte-v2 → `fatal: ambiguous argument … unknown revision` pour les cinq. Contrôle : `git ls-remote --heads origin` → une seule ligne, `bdd444d5356c4379d93c077a5730df56624f4d0b refs/heads/main`; `git branch -r` → `origin/main`. Les cinq branches n'existent pas sur l'origine : rien à supprimer, aucune suppression demandée ni faite.
- [x] Démarrage cloud (N1), vérifié le 2026-11-05 (session cloud démarrée avec le hook : sortie `DÉPENDANCES : installées (cloud).`). Constat : `.claude/settings.json` (SessionStart) appelle déjà `pipelines/deps_cloud.py` (commit 533d56d), qui lance `pip install -r requirements.txt` si `CLAUDE_CODE_REMOTE=true` et que `psycopg` manque ; pas de modification. Session actuelle : `CLAUDE_CODE_REMOTE=true`, `import psycopg` → 3.3.8 (installé).
- [x] `sql.py` en cloud, rejoué le 2026-11-05 après le commit 72d0271 (transport HTTPS, `public.sql_ro`, migrations `ops_005` et `ops_005b`). Preuve : `CLAUDE_CODE_REMOTE=true`, `python -I pipelines/sql.py "select 1"` → tableau `?column? | 1`, `1 lignes`, code 0 ; `python -I pipelines/test_sql.py | tail -1` → `12/12`. Cause du premier échec : le port 5432 est bloqué par le proxy de la session cloud (`bash /dev/tcp/aws-1-eu-west-2.pooler.supabase.com/5432` et `/6543` → timeout, 443 ouvert ; README du proxy `/root/.ccr/README.md` l. 103-106 : raw-TCP databases non pris en charge), pas l'absence de variable. **Limite** : « session neuve » non rejouée (c'est cette session, démarrée après le hook) ; à confirmer à la prochaine ouverture. Ancien constat (premier essai) :
  **ÉCHEC**. `python -I pipelines/sql.py "select 1"` → `SUPABASE_DB_URL_RO absent de .env et de l'environnement`. Cause : la variable n'est pas définie dans l'environnement cloud (`echo ${SUPABASE_DB_URL_RO:+oui}` → vide). Action utilisateur : l'ajouter dans les réglages de l'environnement cloud (variable d'environnement ou Network secrets), puis rouvrir une session et rejouer la commande. Ne pas la coller dans le chat.
- Contrôle du 2026-11-05 : `git ls-remote --heads origin` → `72d0271… refs/heads/ccr-d374a4ca-pxf92j` et `bdd444d… refs/heads/main` ; `git branch -r` → `origin/ccr-d374a4ca-pxf92j`, `origin/main`. Les cinq branches de la liste sont absentes (0 suppression nécessaire). Reste `ccr-d374a4ca-pxf92j`, branche de travail de cette session.
- Preuve de fin « `git branch -r` ne liste que `main` » : **non satisfaite tant que `ccr-d374a4ca-pxf92j` existe**. Les commits S0 (`da76790`, `6cca59d`, `4287830`, `72d0271`) sont sur cette branche, pas sur `origin/main` (`bdd444d`) : fusion dans `main` puis suppression de la branche = décision de l'utilisateur, non faite. « `sql.py` marche en cloud » : satisfaite (voir ci-dessus), sous la réserve « session neuve ».

## S1 — Désarmer le contrôle (2026-11-05)

Commits : f794945 (`police.py` H1/H2 = gros transferts), bc16ace (agent `police` plafonné), efe3b80 (`forme.py` bloc « Si »), 75dff66 (`controle.py` f + b retiré), 5b584c8 (`deja-fait` en étape 0), 8b3e298 (`actives.md`). Aucun hook ajouté, `CLAUDE.md` intact.
Limite : seuil de gros montant non défini avant S2 (`SEUIL_GROS_MONTANT` vide) → tout achat, vente ou enchère reste contrôlé ; montant illisible = contrôlé. H3 (ligne `decision.py new`) inchangé, hors demande.

- [x] Tests verts (rejoués le 2026-11-05) :
  `python -I pipelines/test_police.py | tail -1` → `24/24`, code 0
  `python -I pipelines/test_forme.py | tail -1` → `38/38`, code 0
  `python -I pipelines/test_controle.py | tail -1` → `33/33`, code 0
- [ ] Tour réel BasketVibe : **non mesurable** dans cette session (aucun tour de jeu joué). À remplir au prochain tour : durée (cible < 15 min), retours de hooks Stop, passages de police hors transfert (cible 0).

### Journal de durée (manuel, une ligne par tour)
| Date | Jeu | Durée (min) | Retours de hooks Stop | Police hors transfert |
|---|---|---|---|---|
| 2026-11-05 13:47 Paris | basketvibe | 2,4 (12:47:58 → 12:50:21 UTC, mesuré par `date -u`, jusqu'au rendu) | 0 au moment du rendu (un retour éventuel sera ajouté ici) | 0 (aucun agent lancé) |

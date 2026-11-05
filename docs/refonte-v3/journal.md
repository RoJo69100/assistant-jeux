# Journal refonte v3

Début : 2026-11-05. Plan : `docs/refonte-v3/plan.md`.

## S0 — Remise à plat (2026-11-05)

- [x] `plan-reprise.md` marqué « remplacé » — commit da76790. Preuve : `head -1 docs/refonte-v2/plan-reprise.md` → `> Remplacé par docs/refonte-v3/plan.md (2026-11-05)`.
- [x] `CLAUDE.md` inviolable 3 = Annexe C — commit 6cca59d, `git diff --stat` : 1 ligne changée, aucune autre modification.
- [x] Journal v3 : existait déjà (titre + date, commit bdd444d) ; section S0 ajoutée.
- [ ] Branches distantes. Commandes : `git fetch origin` puis `git rev-list --count origin/main..origin/<branche>` pour ccr-234fdf81-gea2pf, ccr-26f58e91-dqo8si, ccr-5554cafe-lzijjv, claude/test-mcp-gk62t9, refonte-v2 → `fatal: ambiguous argument … unknown revision` pour les cinq. Contrôle : `git ls-remote --heads origin` → une seule ligne, `bdd444d5356c4379d93c077a5730df56624f4d0b refs/heads/main`; `git branch -r` → `origin/main`. Les cinq branches n'existent pas sur l'origine : rien à supprimer, aucune suppression demandée ni faite.
- [ ] Démarrage cloud (N1). Constat : `.claude/settings.json` (SessionStart) appelle déjà `pipelines/deps_cloud.py` (commit 533d56d), qui lance `pip install -r requirements.txt` si `CLAUDE_CODE_REMOTE=true` et que `psycopg` manque ; pas de modification. Session actuelle : `CLAUDE_CODE_REMOTE=true`, `import psycopg` → 3.3.8 (installé).
- [ ] `sql.py` en session neuve : **ÉCHEC**. `python -I pipelines/sql.py "select 1"` → `SUPABASE_DB_URL_RO absent de .env et de l'environnement`. Cause : la variable n'est pas définie dans l'environnement cloud (`echo ${SUPABASE_DB_URL_RO:+oui}` → vide). Action utilisateur : l'ajouter dans les réglages de l'environnement cloud (variable d'environnement ou Network secrets), puis rouvrir une session et rejouer la commande. Ne pas la coller dans le chat.
- Preuve de fin « `git branch -r` ne liste que `main` » : satisfaite (voir ci-dessus). « `sql.py` marche en cloud » : **non satisfaite**.

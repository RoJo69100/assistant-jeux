# Journal refonte v2

Plan : `docs/refonte-v2/plan.md`. Branche `refonte-v2`, tag de départ `avant-refonte-v2`.
Une case n'est cochée que quand son critère de fin est vérifié (date + mesure).

## Phase 0 — 2026-11-03
- [x] 0.0 Préparation — branche et tag poussés (2026-11-03)
- [x] 0.1 Baseline M1 à M7 mesurées (2026-11-03) ; plan Supabase = Free
- [x] 0.2 Sécurité et hygiène (2026-11-03) — 0 secret, 0 ERROR Supabase, Discord hors Git, historique purgé ; reste : limite de payload d'ingestion non vérifiée
- [x] 0.3 Régime de contexte (2026-11-03) — triage 120 règles (`docs/regles/triage.md`), arbitrages, CLAUDE.md 25 Ko -> 5,6 Ko, `actives.md` (30 lignes), 30 skills découpés en index + `references/` (aucune ligne perdue, vérifié), `project_id` retiré (testé sans), hooks `controle.py` f à i. **Écart** : les « 10 règles clés » de chaque SKILL.md ne sont pas écrites (je ne résume pas une règle de jeu sans la relire) ; SKILL.md = index. Gate M4 non vérifiable ici (voir clôture).
- [x] 0.4 `pipelines/sql.py` (2026-11-03) — rôle `assistant_ro` (migrations `sql/silver/ops_001` à `004`), M6 = 49,6 %. **Reste à faire à la main** : ajouter `Bash(python -I pipelines/sql.py:*)` aux permissions (ma modification de `settings.json` a été refusée).
- [x] 0.5 `pipelines/contexte_budget.py` (2026-11-03) — pre-commit actif ; BasketVibe 5 993 jetons ; dette des 5 autres jeux figée (`docs/regles/budget-dette.json`)
- [x] 0.6 Sauvegarde du bronze (2026-11-03) — 9 691 pages + 172 803 messages dans `~/backups/assistant-jeux/`, comptes identiques à la base. **Reste** : tâche hebdomadaire (Planificateur de tâches) et test de restauration à blanc dans un schéma temporaire (demande ton accord).
- [x] 0.7 Clôture (2026-11-03) — mesures après dans `outputs/optimisation/2026-11-03-baseline.md`, tag `refonte-v2-phase0`

## Phases suivantes
- [ ] Phase 1 — couche `core`
- [ ] Phase 2 — moteur de décision
- [ ] Phase 3 — journal de décisions `learn`
- [ ] Phase 4 — base de connaissances `kb`
- [ ] Phase 5 — orchestrateur, packs, agents
- [ ] Phase 6 — industrialiser (jeux 7 à 23)
- [ ] Phase 7 — qualité, CI, observabilité
- [ ] Phase 8 — futur

## Point de reprise (2026-11-03, fin de phase 0)
- Fait : toute la phase 0. Reste de la phase 0 à la main : permission `sql.py`, tâche hebdomadaire de sauvegarde, accord pour le test de restauration.
- Prochaine étape : **phase 1 (couche `core`)**, session Opus, après `/clear`. Lire plan §0, §1 et Phase 1 seulement.
- Dettes connues : résumés des 5 autres jeux au-dessus de 1 000 jetons (HN 3 794) ; M4 à mesurer sur une vraie session de jeu ; M3 et M5 non tenus (phases 4 et 5).
- Le mot de passe de `assistant_ro` est passé par un appel d'outil de cette session (journal local) : le renouveler par le tableau de bord Supabase si besoin, puis mettre à jour `SUPABASE_DB_URL_RO` dans `.env`.

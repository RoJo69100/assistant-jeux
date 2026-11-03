# Journal refonte v2

Plan : `docs/refonte-v2/plan.md`. Branche `refonte-v2`, tag de départ `avant-refonte-v2`.
Une case n'est cochée que quand son critère de fin est vérifié (date + mesure).

## Phase 0 — 2026-11-03
- [x] 0.0 Préparation — branche et tag poussés (2026-11-03)
- [ ] 0.1 Baseline : M1, M3 (partielle), M4, M7 mesurées ; M2, M5, M6 restent ; plan Supabase = Free
- [x] 0.2 Sécurité et hygiène (2026-11-03) — 0 secret, 0 ERROR Supabase, Discord hors Git, historique purgé ; reste : limite de payload d'ingestion non vérifiée
- [ ] 0.3 Régime de contexte (triage, CLAUDE.md ≤ 90 lignes, actives.md, skills, project_id)
- [ ] 0.4 `pipelines/sql.py`
- [ ] 0.5 `pipelines/contexte_budget.py`
- [ ] 0.6 Sauvegarde du bronze
- [ ] 0.7 Clôture (M1–M7 après, tag `refonte-v2-phase0`)

## Phases suivantes
- [ ] Phase 1 — couche `core`
- [ ] Phase 2 — moteur de décision
- [ ] Phase 3 — journal de décisions `learn`
- [ ] Phase 4 — base de connaissances `kb`
- [ ] Phase 5 — orchestrateur, packs, agents
- [ ] Phase 6 — industrialiser (jeux 7 à 23)
- [ ] Phase 7 — qualité, CI, observabilité
- [ ] Phase 8 — futur

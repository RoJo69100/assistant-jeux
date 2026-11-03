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
- [x] 0.6 Sauvegarde du bronze (2026-11-03) — 9 691 pages + 172 803 messages dans `~/backups/assistant-jeux/`, comptes identiques à la base. Tâche hebdomadaire créée (dimanche 21:00, `AssistantJeuxSauvegardeBronze`). Test de restauration fait avec accord (2026-11-03) : les 9 691 empreintes SHA-256 des pages se recalculent à l'identique depuis les fichiers ; 3 pages restaurées dans un schéma temporaire Supabase = identiques au bronze (payload, empreinte, URL, date), schéma supprimé. **Limite** : la restauration complète (182 000 lignes) n'a pas été rejouée en base, seulement un échantillon.
- [x] 0.7 Clôture (2026-11-03) — mesures après dans `outputs/optimisation/2026-11-03-baseline.md`, tag `refonte-v2-phase0`

## Phases suivantes
- [ ] Phase 1 — couche `core`
  - [x] 1.1 (début, 2026-11-03) schémas `core` + `adapt`, `core.game_params` (10 paramètres BV sourcés) — `sql/core/001_core_schema.sql`
  - [x] 1.2 (BV, 2026-11-03) `adapt.basketvibe_player_daily` (245 lignes, 0 doublon, forme/fatigue 0–1, salaire 237/245) et `adapt.basketvibe_fixture` (70 fixtures, 0 doublon, `my_result` repris de `bv_matches`) — `sql/adapters/basketvibe.sql`. **Constats** : 2 matchs de coupe passés (29 et 31/10) et la J1 du 02/11 sans résultat (matchs non exportés) ; `scheduled_at` nul (fuseau du kickoff non sourcé).
  - [x] 1.2 suite (BV, 2026-11-03) `adapt.basketvibe_standing` (48 lignes, relevés d'une autre ligue écartés) et `adapt.basketvibe_finance_daily` (4 relevés hebdomadaires, `extras.periode = semaine`) ; section `core:` dans `basketvibe.yaml` (colonnes nulles déclarées)
  - [x] 1.2 `pipelines/build_core.py` (2026-11-03) — contrat (colonnes, types, clés) + génération de `sql/core/002_core_views.sql` ; vues `core.player_daily|fixture|standing|finance_daily` appliquées
  - [x] 1.3 `pipelines/contrat_core.py` (2026-11-03) — BV vert (0 ❌, 3 constats : matchs passés sans résultat 29/10, 31/10, 02/11) ; échoue bien avec `--fraicheur 0` ; branché sur `recette.py --tous` avec `build_core.py --check`
  - [ ] Reste : entités BV `market_listing`, `staff`, `academy_prospect`, `training_plan` ; adaptateur HN ; fonction `as_of` ; gold générique (1.4) ; cartes `_core` (1.5)
- [ ] Phase 2 — moteur de décision
- [ ] Phase 3 — journal de décisions `learn`
- [ ] Phase 4 — base de connaissances `kb`
- [ ] Phase 5 — orchestrateur, packs, agents
- [ ] Phase 6 — industrialiser (jeux 7 à 23)
- [ ] Phase 7 — qualité, CI, observabilité
- [ ] Phase 8 — futur

## Point de reprise (2026-11-03, fin de phase 0)
- Fait : toute la phase 0, y compris la permission `sql.py`, la tâche hebdomadaire et le test de restauration.
- Prochaine étape : **phase 1 (couche `core`)**, session Opus, après `/clear`. Lire plan §0, §1 et Phase 1 seulement.
- Dettes connues : résumés des 5 autres jeux au-dessus de 1 000 jetons (HN 3 794) ; M4 à mesurer sur une vraie session de jeu ; M3 et M5 non tenus (phases 4 et 5).
- Le mot de passe de `assistant_ro` est passé par un appel d'outil de cette session (journal local) : le renouveler par le tableau de bord Supabase si besoin, puis mettre à jour `SUPABASE_DB_URL_RO` dans `.env`.

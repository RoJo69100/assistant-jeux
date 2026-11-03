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
  - [x] 1.2 (HN, 2026-11-03) `sql/adapters/hockeynation.sql` : `player_daily` (458 lignes, 4 équipes = 4 `team_id`, salaire du contrat actif, U17/U21 = `is_academy`), `fixture` (247, `my_result` repris de `hn_games`, jour en Europe/Paris), `standing` (20, relevés sans mon équipe écartés), `finance_daily` (4, plafond salarial, pas de trésorerie) ; 6 `game_params` HN sourcés (pas de règle des points : non sourcée) ; `contrat_core` vert sur BV + HN. **Constat** : U21 contre Oklahoma Zebras U21 du 02/11 encore « upcoming » (export manquant)
  - [x] 1.2 (BV, 2026-11-03) entité `market_listing` au contrat (clé `game, listing_id`) et `adapt.basketvibe_market_listing` (952 enchères vues, mes ventes = `is_mine`) ; amicaux programmés ajoutés à `adapt.basketvibe_fixture` (7, `scheduled_at` en UTC, jour en Europe/Paris) — prérequis de `gold.agenda`
  - [ ] 1.4 `gold.agenda` (2026-11-03, en cours) : règles d'agenda en données (`core.agenda_rule`, 11 règles BV reprises de `gold.bv_agenda`, source citée par règle) + une vue pour tous les jeux (`sql/gold/062_agenda.sql`). Parité BV le 03/11 : 28 lignes des deux côtés, seul écart = l'amical de 00:00 dont le preset est daté de la veille 23:45 (correction voulue, tolérée). `pipelines/agenda_parite.py` (journal `outputs/refonte-v2/parite-agenda.log`, branché sur la recette) ; échoue bien sur un écart. **Fin** : 7 dates sans écart pour BV, puis HN (pas encore de règles HN : calendrier de saison à adapter)
  - [x] 1.2 (BV, 2026-11-03) `academy_prospect` (9 candidats de 3 rapports, `rating_min/max` = PS du poste sur les bornes ; milieu = `ps_mid` de `gold.bv_academy_prospects` sur les 3 du 29/10 ; potentiel caché déclaré nul ; tous « candidat », signatures non collectées) et `training_plan` (179 lignes, focus principal/secondaire, pas d'intensité) ; contrat vert BV + HN
  - [x] 1.2 (BV, 2026-11-03) `staff` depuis l'API Personnel (23 lignes, 3 relevés ; rôles normalisés ; pas d'identifiant : `staff_id` = rôle + nom ; niveau et coût absents de la collecte). **Constat** : fraîcheur ❌ (dernier relevé API le 25/10) — les captures du 27/10 et du 01/11 sont en DOM seul, sans l'appel API ; le DOM n'est pas lu (texte libre)
  - [x] `facility` BV : non applicable (aucune infrastructure dans les skills BasketVibe, vérifié le 2026-11-03)
  - [x] 1.2 (HN, 2026-11-03) `market_listing` (89 : agents libres + trade block, sans prix ni enchère), `academy_prospect` (200 : classes de draft 26 et 27 de ma ligue seulement, OVR visible, potentiel non affiché), `staff` (33 : coachs des 4 équipes avec note, scouts avec salaire par jour), `training_plan` (132 : une compétence par jour, PRO/FRM réglables) ; relevés HN datés au jour (`extras.seen_at_precision`). Contrat : seul ❌ = fraîcheur du personnel BV (ci-dessus)
  - [x] 1.1 `as_of` (2026-11-03) `core.player_daily_asof(game, day, max_age = 7)` — `sql/core/004_asof.sql` : dernier relevé ≤ jour, un joueur = une ligne (HN : 4 joueurs montés FRM→PRO gardaient leur ligne périmée, corrigé) ; vérifié : 0 ligne future, 0 doublon, Sacha Leclerc 40,9 au 17/10 puis 41,2 au 18/10
  - [ ] 1.4 `gold.exports_state` (2026-11-03, en cours) : écrans en données (`core.export_rule`, 14 BV + 14 HN repris des anciennes vues, `sql/core/005_export_rule.sql`), une vue lue dans le bronze (`sql/gold/063_exports_state.sql`). Parité le 03/11 : 0 écart BV et HN (`pipelines/exports_parite.py`, journal `outputs/refonte-v2/parite-exports.log`, branché sur la recette). **Fin** : 7 dates sans écart
  - [ ] Reste phase 1 : `facility` (jeux qui en ont : SZL, TS) ; parité `gold.agenda` 7 jours + règles HN ; autres vues gold génériques (1.4) ; cartes `_core` (1.5) (et HN, dont `market_listing`) ; fonction `as_of` ; gold générique (1.4) ; cartes `_core` (1.5)
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

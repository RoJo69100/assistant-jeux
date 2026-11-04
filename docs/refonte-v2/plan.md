# Plan de refonte v2 — Assistant jeux

> **Destinataire : le Claude qui travaille dans le dépôt `assistant-jeux`.** Document écrit le 2026-11-03 à partir d'une lecture du dépôt (clone superficiel, 1 commit visible) et de l'architecture cible discutée avec l'utilisateur. **Rien n'a été exécuté ni testé** : les DDL de l'annexe B sont à valider avant application. Supabase n'a pas été interrogé : tout ce qui touche l'état réel de la base est marqué « à vérifier ».
>
> **Comment l'utiliser.** Lis §0 et §1, puis **uniquement la phase du jour**. Une phase = une ou plusieurs sessions, `/clear` entre deux. Conception = Opus, exécution = Sonnet (règle du dépôt). Une étape = un commit. Coche et date chaque case dans `docs/refonte-v2/journal.md` seulement quand son critère de fin est vérifié.

---

## 0. Cadrage

### 0.1 Ce qui existe et qu'on garde (vérifié dans le code)
| Acquis | Pourquoi on le garde |
|---|---|
| Collecte **passive** par Tampermonkey → `bronze.raw_pages` (JSON brut daté, immuable par trigger) | Aucun robot, aucune requête vers les jeux : risque de bannissement quasi nul. **Le bronze est irremplaçable** (on ne peut pas re-collecter le passé). |
| Calculs en SQL (silver/gold), pas dans le LLM | Reproductible, bon marché, vérifiable. |
| Hooks `police.py`, `forme.py`, `controle.py` | Seule partie qui garantit réellement une règle. Le reste est de la prose. |
| Cartes de décision + `dossier.py` + `--marquer` (« on trouve une fois, on garde ») | Bonne idée : mémoire de *où* lire et *comment juger*. |
| Config déclarative `docs/attentes/jeux/<jeu>.yaml` + `_modele.yaml` | Début du « profil de jeu » : la bonne séparation cœur / spécifique. |
| `mesure_session.py` | Permet de mesurer au lieu de supposer. |
| Règles utilisateur R-1…R-12, A-1…A-11 | Exigences produit. Elles ne changent pas ; leur *mise en œuvre* change. |

### 0.2 Diagnostic (faits mesurés par le dépôt lui-même + lecture)
- **Coût = contexte × tours × agents.** Mesures du dépôt : 29,6 M tokens relus pour une session de 6 jeux (contexte 146 k → 495 k) ; 9 agents = 8,2 M relus pour ~3 000 utiles ; ~0,45 M éq. par agent, 40 agents/semaine. Le contexte fixe (~25 Ko `CLAUDE.md` + ~34 Ko `regles-apprises.md` + skills 352 Ko + fiches 210 Ko + agents 54 Ko) est relu à **chaque tour de chaque agent**. *(À vérifier au §1 : un agent « vide » coûte combien ?)*
- **La prose ne tient pas.** 82 règles apprises, avec de nombreuses « RÉCIDIVE » (règles 70, 71, 75, 79…). Seuls les hooks sont fiables.
- **Contradictions internes** : voir annexe A.
- **Tout est refait à la main par jeu** : ~100 fichiers SQL préfixés (`bv_ sz_ ts_ hn_ hw_ dm_`), 41 skills, 7 cartes × 6 jeux, 6 userscripts de ~280 lignes dupliqués (1 697 lignes), `gold.calendrier_maitre` = union écrite à la main.
- **Fonctions du cœur absentes** (à confirmer) : contexte de saison, charte stratégique par club, recherche plein texte et scoring de confiance, journal de décisions interrogeable, tests de vues SQL, CI.
- **Connaissance lue en bloc** : `connaissance.md` = 238 Ko (Derby Manager 92 Ko, Six Zero 57 Ko).
- **Sécurité** : le dépôt était public avec ~108 Mo d'exports Discord (tiers). Passé en privé le 2026-11-03 ; supposer que le contenu a été copié.

### 0.3 Objectif et principes
**Objectif** : 23 jeux, une décision quotidienne fondée sur données + connaissance sourcée, qui **apprend** et **ne répète pas ses erreurs**, pour un coût de tokens ≥ 5× inférieur.
- **P1. Le code garantit, la prose guide.** Toute règle récidivante devient hook, vue SQL, test ou contrainte DB.
- **P2. Cœur commun + adaptateur fin par jeu.**
- **P3. Complétude par requête, pas par lecture** (comptage SQL « N affichées = N total »).
- **P4. Les agents ne reçoivent que ce qui a changé** (hash des entrées) et un **pack de contexte compact**.
- **P5. Mesurer avant/après chaque étape** (`mesure_session.py`). Pas de gain mesuré = retour arrière.
- **P6. Strangler, pas big-bang.** Nouveau à côté, comparaison, bascule, suppression de l'ancien 30 jours plus tard.

### 0.4 Non-objectifs / interdits pendant la refonte
- Ne **pas** modifier le bronze (triggers d'immutabilité) ni réécrire les silver existants d'un coup.
- Ne **pas** ajouter de nouvel agent ni de nouvelle règle en prose sans enforcement.
- Ne **pas** introduire de navigation automatique vers les sites de jeux.
- **Jamais** d'enchère, d'achat ou de vente sans accord de l'utilisateur (A-4).
- **STOP et demander** avant : réécriture d'historique Git / force-push, suppression de données, rotation de clés, toute opération irréversible sur Supabase.

### 0.5 Conventions de travail
Branche `refonte-v2`, tag `avant-refonte-v2` posé avant la première modification. Migrations SQL dans `sql/<schema>/NNN_*.sql`, appliquées via migration Supabase (pas `execute_sql` pour du DDL). Nouveaux schémas : `revoke all on schema … from public, anon, authenticated`, vues en `security_invoker = true`. Après chaque étape : tests existants (`test_forme`, `test_police`, `test_controle`) + mesure + commit `refonte-v2 : <étape>`. Journal : `docs/refonte-v2/journal.md`.

---

## 1. Mesures de référence (à faire AVANT tout le reste)
Fichier de sortie : `outputs/optimisation/2026-11-03-baseline.md`.

| # | Mesure | Comment | Cible après refonte |
|---|---|---|---|
| M1 | Contexte fixe (tokens ≈ caractères / 3,6) de : `CLAUDE.md`, `regles-apprises.md`, `attentes.md`, 1 `resume.md`, descriptions des 41 skills, 1 agent | `wc -c` puis conversion ; script définitif en 0.5 | **≤ 6 000** pour une session de jeu |
| M2 | Coût plancher d'un agent : `veille` avec « réponds OK » | `mesure_session.py` | ≤ 0,05 M éq. |
| M3 | Tours moyens par agent et nb d'appels SQL par agent (3 derniers jours) | `mesure_session.py` | ≤ 6 tours, ≤ 2 appels SQL |
| M4 | Tokens relus par session (médiane des 5 dernières) | `mesure_session.py` | ≤ 5 M (pire : 29,6 M) |
| M5 | Agents lancés par semaine | journal `mesure_session` | ≤ 12, tous « sur nouveauté » |
| M6 | Taille d'un résultat SQL typique via MCP vs script | même requête | script ≤ 50 % du MCP |
| M7 | Récidives de règles par semaine | `docs/retro` | → 0 pour les règles couvertes par du code |

Règle : **chaque phase se termine par la relecture de M1–M7**.

---

## Phase 0 — CE SOIR (≈ 3 à 4 h, ordre strict)
> Si le temps manque : 0.0 → 0.1 → 0.2 → 0.3 sont **obligatoires**, le reste peut glisser.

### 0.0 Préparation (10 min)
- [ ] `git checkout -b refonte-v2` ; `git tag avant-refonte-v2` ; `git push origin refonte-v2 --tags`.
- [ ] Créer `docs/refonte-v2/journal.md`.
- [ ] Copier ce plan dans `docs/refonte-v2/plan.md`.
**Fin** : le tag existe, la branche est poussée.

### 0.1 Baseline (20 min)
- [ ] Mesurer M1…M7 → `outputs/optimisation/2026-11-03-baseline.md`.
- [ ] Noter le plan Supabase (free/pro : conditionne les sauvegardes, 0.6) — **à demander à l'utilisateur**, seule question de la soirée.
**Fin** : 7 nombres écrits, datés.

### 0.2 Sécurité et hygiène (40 min)
1. **Historique complet** (`git fetch --unshallow` si besoin) : chercher `eyJ…` (JWT), `sb_secret_`, `service_role`, `DISCORD_TOKEN=`, `INGEST_TOKEN=` avec valeur, mots de passe, clés API. Outil : `gitleaks detect --log-opts="--all"` si installable, sinon regex sur `git log -p --all`.
   - **Si une clé est trouvée → STOP, l'écrire à l'utilisateur** avec la procédure de rotation : clés Supabase (dashboard → API), jeton Discord (reset), jeton d'ingestion (nouveau hash dans `bronze.ingest_tokens`, supprimer l'ancien, ressaisir dans chaque userscript via `GM_setValue`).
2. **Discord hors de Git** (la base est le support partagé) :
   - Vérifier que la base contient tout : `select game, count(*), min(posted_at), max(posted_at) from bronze.discord_messages group by 1` ; comparer au nombre de messages des fichiers (`import_discord.py` idempotent).
   - **Après accord** : `git rm -r --cached data/discord data/chat` ; ajouter à `.gitignore` ; garder les fichiers sur disque ; copie zippée hors dépôt.
   - Mettre à jour `CLAUDE.md` (« versionné » devient « importé en base, non versionné »).
   - **Purge de l'historique** (`git filter-repo --path data/discord --path data/chat --invert-paths` + force-push) : **proposer, ne pas faire sans accord explicite**. Le dépôt a été public : la purge n'annule pas les copies. `data/discord/Perso` : avertissement séparé.
3. **Supabase** (MCP) : `get_advisors` sécurité et performance ; traiter les alertes critiques. Vérifier avec la clé publishable que `anon` ne lit ni `bronze`, `silver`, `gold`, `learn`, `kb`. Seules `ingest_raw_pages` et `ingest_discord_messages` exécutables par `anon`, limite de taille de payload et table de journal des rejets si absentes.
4. **Garde anti-fuite** : `.githooks/pre-commit` appelant `pipelines/scan_secrets.py` (regex ci-dessus + fichiers > 5 Mo) ; `git config core.hooksPath .githooks` ; documenter dans le README (2ᵉ machine).
**Fin** : `outputs/optimisation/2026-11-03-securite.md` ; `git ls-files data/discord data/chat | wc -l` = 0 ; 0 alerte critique ; hook pre-commit actif.

### 0.3 Régime de contexte (90 min) — le cœur de ce soir
**A. Triage des règles** → `docs/regles/triage.md` : `id | résumé ≤ 15 mots | classe | destination | enforcement`. Classes :
- **E** (enforce) : vérifiable mécaniquement. Obligatoire si récidive ≥ 2. Écrire le hook/la vue/le test (ou file de la phase 3).
- **S** (scope) : un jeu ou un domaine → `docs/fiches/<jeu>/` ou carte du type.
- **K** (keep) : vraie pour toute session, non vérifiable mécaniquement. **Cible ≤ 15 règles.**
- **D** (delete) : doublon, contredite, obsolète (agents retirés `effectif`, `finances`, `lecteur-exports`, `verificateur`, `optimisation` ; « lire `regles-apprises` en début de session » ; contradictions de l'annexe A).
Aucune règle ne disparaît sans ligne dans le triage.

**B. Arbitrer les contradictions** (annexe A) → `docs/regles/arbitrages.md` (une ligne chacune, datée).

**C. Nouveau `CLAUDE.md` ≤ 90 lignes / ≤ 2 500 tokens** (squelette annexe D). Le reste va dans `docs/regles/` ou les fiches.

**D. `regles-apprises.md` (34 Ko) → deux fichiers** :
- `docs/regles/actives.md` : ≤ 40 lignes, `Quand <déclencheur> → <action vérifiable>`, classe K + ~10 règles les plus violées.
- `docs/regles/archive/regles-apprises-2026-11-02.md` (`git mv`) : jamais chargé automatiquement.
- Adapter `pipelines/rappel_debut.py` (SessionStart) : titres des règles actives + 3 exports les plus en retard, pas le texte complet.

**E. Skills** : pour chaque `SKILL.md` > 6 Ko (22 Ko `basketvibe-communaute`, 16 Ko `basketvibe-tactique`, ~12-13 Ko `teamsoccer-match`, `derbymanager-tactique`, `sixzeroleague-match`, `derbymanager-club`, `teamsoccer-joueurs`, `sixzeroleague-communaute`…) :
- `SKILL.md` ≤ 2,5 Ko : usage, quand lire quelle référence, 10 règles clés, index.
- Le reste → `references/<thème>.md`.
- `*-communaute` : seulement scinder (remplacés par `kb` en phase 4).
- Descriptions de frontmatter ≤ 250 caractères.

**F. `project_id` en dur** (11 fichiers) : tester `execute_sql` **sans** `project_id` (l'URL `.mcp.json` est épinglée). Si ça marche, supprimer la consigne ; sinon la centraliser.

**Fin** : `contexte_budget.py` (0.5) ≤ 6 000 tokens de contexte fixe ; `triage.md` couvre 100 % des règles ; `test_forme`/`test_police`/`test_controle` passent ; une session test d'un jeu tourne et M4 ≤ 60 % de la baseline. **Si M4 ne baisse pas, ne pas continuer : chercher pourquoi.**

### 0.4 `pipelines/sql.py` — requêtes compactes (45 min)
- Rôle Postgres **lecture seule** `assistant_ro` (select sur `silver`, `gold`, plus tard `core`/`kb`/`learn`/`ops`) ; chaîne dans `.env` (`SUPABASE_DB_URL_RO`). Pas d'accès à `bronze.raw_pages.payload` complet : `--payload-path '<jsonpath>'`.
- CLI : `python -I pipelines/sql.py "select …" [--max-rows 30] [--max-col 60]` → tableau Markdown compact, ajoute `limit`, tronque, affiche `n lignes / tronqué`.
- Ajouter `Bash(python -I pipelines/sql.py:*)` aux permissions ; MCP gardé pour DDL/migrations.
**Fin** : M6 ≤ 50 % ; refus de toute écriture.

### 0.5 `pipelines/contexte_budget.py` (30 min)
Tokens approximatifs (caractères / 3,6) de : `CLAUDE.md`, `actives.md`, chaque agent, `resume.md`, `SKILL.md` (corps), descriptions de skill, sortie du hook de début de session. Budgets (échec si dépassé) : `CLAUDE.md` 2 500 · `actives.md` 1 500 · agent 1 500 · `resume.md` 1 000 · `SKILL.md` 1 000 · total « session jeu » 6 000. Branché sur `recette.py` et le pre-commit. Test : `pipelines/test_contexte_budget.py`.
**Fin** : un fichier qui grossit trop fait échouer le commit.

### 0.6 Sauvegarde du bronze (30 min, si le temps le permet)
`pipelines/sauvegarde_bronze.py` : export incrémental (`id > dernier id`) de `bronze.raw_pages` et `bronze.discord_messages` en NDJSON compressé vers `~/backups/assistant-jeux/` (hors Git), fichier d'état, vérification de comptage ; hebdomadaire (Planificateur de tâches) ; rappel dans `gold.sante_collecte` si > 10 jours.
**Fin** : sauvegarde complète restaurée à blanc dans un schéma temporaire, comptage identique (avec accord).

### 0.7 Clôture (10 min)
- [ ] Refaire M1…M7 à côté de la baseline.
- [ ] Journal à jour, commits poussés, tag `refonte-v2-phase0`.
- [ ] Première ligne de la prochaine réponse : « `/clear` avant la phase 1 ».

---

## Phase 1 — Couche commune `core` (2 à 3 sessions, Opus)
**But** : un seul modèle de données lu par tous les agents, cartes et vues gold ; chaque jeu branché par **un adaptateur** (vues SQL), sans toucher bronze ni silver.

### 1.1 Contrat `core`
Entités (DDL indicatif B.1) : `core.player_daily`, `core.fixture`, `core.standing`, `core.finance_daily`, `core.market_listing`, `core.staff`, `core.facility`, `core.academy_prospect`, `core.training_plan`, `core.game_params`.
- Colonnes **normalisées** : `rating` (0-100), `form`/`fatigue`/`morale` (0-1), `competition_kind` ∈ {ligue, coupe, amical, playoff, autre}, `my_result` ∈ {W, D, L} (calculé *une fois* dans l'adaptateur : R-9).
- Spécifique dans `extras jsonb`.
- Colonne non fournie = `null` **et** déclarée dans le YAML (`domaines.<x>.present: non` ou `limites: […]`).
- Unité de temps : jour Paris (`day`).
- **`as_of`** : fonctions `core.player_daily_asof(game, date)` (backtests, 8.2).

### 1.2 Adaptateurs
`sql/adapters/<jeu>.sql` → vues `adapt.<jeu>_player_daily`, `…_fixture`, … ; `core.*` = `union all` généré par `pipelines/build_core.py` depuis `docs/attentes/jeux/*.yaml`.
**Ordre** : BasketVibe → Hockey Nation → Team Soccer → Six Zero League → Hardwood → Derby Manager (dates en texte à fiabiliser d'abord, cf. `061_calendrier_maitre`). Adaptateur **mince** : renommage, échelle, `my_result`, `competition_kind`. Pas de logique de décision.

### 1.3 Test de contrat `pipelines/contrat_core.py`
Par jeu et entité : colonnes, types, `not null` sur les clés, plages, unicité `(game, team_id, player_id, day)`, fraîcheur ; tableau de couverture (✅ / ⚪ non applicable déclaré / ❌ manquant). Branché sur `recette.py`. Remplace `docs/couverture/<jeu>.md` écrit à la main.

### 1.4 Gold générique (strangler)
Une seule fois sur `core` avec `core.game_params` : `gold.agenda`, `gold.daily_alerts`, `gold.calendrier_maitre`, `gold.exports_state`, `gold.roster_bilan`, `gold.finance_health` (dont `capacite_invest`). Vue générique à côté de l'ancienne ; non-régression `select … except select …` sur les 6 jeux pendant 7 jours ; ensuite cartes → vue générique ; ancienne `deprecated`, supprimée 30 jours plus tard.

### 1.5 Cartes génériques
`docs/decisions/cartes/_core/<type>.md` (academie, achat, composition, defaite, entrainement, finances, vente) paramétrées par `:game`. Les 43 cartes de jeu deviennent des **deltas** ; `dossier.py` fusionne cœur + delta. « Dernière valeur » générée par `dossier.py`.

**Fin phase 1** : `contrat_core.py` vert sur BV + HN (puis 6) ; `gold.agenda` générique = ancien sur ≥ 7 jours pour BV et HN ; M3 en baisse ; `dossier.py` rend une carte fusionnée pour BV.

---

## Phase 2 — Moteur de décision manquant (2 sessions, Opus)
> « J20/25, déjà champion → on teste/ménage » n'existe pas dans le dépôt. Tout en SQL ; le LLM ne fait que l'arbitrage.

### 2.1 `gold.season_context`
Par équipe : `round_no`, `rounds_total`, `rank`, `points`, `gap_to_first`, `gap_to_relegation`, `points_restants_max = (rounds_total - round_no) × points_par_victoire`, drapeaux `titre_acquis`, `qualif_acquise`, `maintien_acquis`, `elimine`, `rien_a_jouer`. Points non exposés → drapeau `null`, objectif `gagner` — jamais d'hypothèse silencieuse. Formats depuis `core.game_params` (`ligue:` du YAML).

### 2.2 `gold.match_objective`
Table éditable `core.objective_rules(competition_kind, condition, objectif, raison, priorité)` :
- ligue + `normal` → `gagner` ; coupe → `gagner` ; amical → `tester` ;
- ligue + `titre_acquis`/`maintien_acquis`/`rien_a_jouer` → `former` ou `tester` selon la charte (2.3) ;
- série de défaites ≥ 2 (A-1) → `corriger`.
Sortie : `objectif` + `raison` chiffrée + `ce qui prouvera que j'avais tort` (R-8) ; la carte *composition* la lit en première ligne.

### 2.3 `core.club_strategy`
Bloc `strategie:` du YAML : `horizon` (maintenant | 3_saisons | long_terme), `poids_jeunes`/`poids_veterans` (0-1), `appetit_risque`, `plafond_masse_salariale_pct_revenus`, `reserve_tresorerie` (semaines de salaires), `vendre_pour_profit`. Chargée à chaque `--marquer` ; **chaque décision enregistre un instantané**. `gold.strategy_suggestion` propose, l'utilisateur valide.

### 2.4 Valeur, besoins, transferts
| Vue | Contenu | Paramètres |
|---|---|---|
| `core.age_curve_observed` | progression moyenne par âge sur nos snapshots | — |
| `gold.player_value` | valeur sportive (gain vs n°2), coût, revente projetée, horizon | échelle d'âge, poids |
| `gold.position_gap` | trous et surplus par poste | postes, effectif min/max |
| `gold.sell_candidates` | trop cher vs valeur (> p75 ligue), mécontent, surplus, déclin | `seuils:` YAML |
| `gold.buy_targets` | gain vs n°2, prix ≤ plafond, **finançable** = `capacite_invest − gold.engaged_spend` | tables de prix |
| `gold.engaged_spend` | décisions acceptées non exécutées (`learn.decision`) | — |
| `gold.finance_policy` | réserve = sorties certaines × k ; investissable = solde − réserve − engagé | k, X |
| `gold.youth_value` | valeur projetée à l'âge A vs coût de formation | courbe de croissance |
Chaque formule validée contre l'historique (MAPE) dans `learn.backtest` (8.2) ; sinon la vue affiche sa fiabilité (`ref_reliable`).

### 2.5 Arbitrage LLM borné
Le LLM reçoit **uniquement** charte, `season_context`, `match_objective`, ≤ 15 candidats, leçons validées ; il rend un **JSON** `{action, justification, sources[], confiance, preuve_d_erreur, date_test}`. Un validateur rejette tout JSON dont une source n'existe pas (`kb.claim.id` / `L-nnn` / vue).

**Fin phase 2** : sur BV et HN, `gold.match_objective` cohérent avec le jugement de l'utilisateur sur 10 matchs passés (`as_of`) ; les vues de 2.4 ont un MAPE documenté ; carte *composition* avec l'objectif en première ligne.

---

## Phase 3 — Journal de décisions et apprentissage (2 sessions)
**But** : « ne pas se répéter » devient une propriété de la base. DDL B.2.

### 3.1 `learn.*`
`learn.decision`, `learn.outcome`, `learn.lesson` (statut `hypothesis → validated → hard_rule → retired`), `learn.error` (récidives, **type d'enforcement** hook/sql/test/prose).

### 3.2 Écrire une décision = une ligne
Chaque conseil (C-nnn) crée une ligne via `pipelines/decision.py new …` (le hook de rendu l'exige). **Prédiction structurée** : `{"metric":"my_result","fenetre_matchs":3,"attendu":"W>=2"}`. Sans prédiction mesurable : refusée (A-7, R-8).

### 3.3 `pipelines/evaluer_decisions.py`
Vue `gold.decisions_a_evaluer`. L'évaluateur exécute la mesure, écrit `learn.outcome`, met à jour `learn.lesson` : ≥ 3 confirmations et 0 contradiction → `validated` ; ≥ 5 → `hard_rule` proposée ; **2 contradictions → `retired` + `learn.error` + conseil à réécrire** (A-7 par le code) ; `inconclusive` si échantillon trop petit. Seuils (3, 5, 2) dans `core.game_params`.

### 3.4 `pipelines/garde.py <jeu> <domaine>`
Imprime les leçons `validated`/`hard_rule`, les erreurs ouvertes, et signale tout **revirement** (acheter puis revendre) avec le plan de sortie chiffré (R-8). `dossier.py` l'appelle ; le hook H2 vérifie que la réponse cite les `L-nnn` consultés.

### 3.5 Migration de l'existant
`pipelines/migrer_learnings.py` : parse les `C-nnn`/`L-nnn` des 6 `learnings.md` (~494 lignes) vers `learn.*` (`hypothesis` par défaut, `validated` si ≥ 3 confirmations attestées). `learnings.md` deviennent **générés** (`export_learnings_md.py`) ; « Checks appris » des cartes générée depuis `learn.lesson`. Chaque règle E du triage reçoit une ligne `learn.error`.

**Fin phase 3** : une décision de test (prédiction fausse, répétée 2 fois) aboutit à une leçon `retired` et est **bloquée** par `garde.py` au 3ᵉ essai ; `learnings.md` régénérés = contenu migré ; M7 mesurable en SQL.

---

## Phase 4 — Base de connaissances `kb` (2 à 3 sessions)
**But** : wiki interrogeable, confiance chiffrée, contradictions gérées. DDL B.3.

### 4.1 Modèle
`kb.claim` : texte, jeu, domaine, source (`manuel | devlog | patchnote | discord | forum | chat | observation`), référence, auteur, date, version du jeu, statut (`confirme | complete | contredit | en_doute | obsolete`), **confiance 0-1**, `superseded_by`, `contradicts[]`, `data_check_sql`, `data_verdict`, index plein texte français. `connaissance.md` devient un **export généré**.

### 4.2 Score de confiance (`kb.recompute_confidence()`)
Base : manuel/devlog/patchnote 0,90 · observation 0,80 · discord 0,40 · forum 0,35 · chat 0,30. +0,10 par auteur distinct d'accord (max +0,30) ; ×0,5 si antérieure au dernier patch du domaine ; +0,20 si `data_verdict = confirmé` ; `contredit` si les données l'infirment. Conflits regroupés par `contradicts[]`, la plus fiable dominante.

### 4.3 Ingestion
Delta `bronze.discord_messages` (id > dernier traité) → regroupement par fil/thème → extraction par `veille` (Sonnet, lots ~50, JSON strict) → `kb.claim` → recalcul. **Backfill** (~108 Mo) : filtrer en SQL d'abord, **estimer le volume avant et demander l'accord sur le budget**, reprise par `kb.ingest_cursor`. Patchnotes/devlog : affirmations antérieures du domaine `obsolete` ou à reconfirmer. Vérification par nos données via `data_check_sql`.

### 4.4 Lecture par requête (P3)
`pipelines/kb.py <jeu> <thème> [--min-conf 0.5]` renvoie **toutes** les affirmations du thème avec `N total / N affichées`. La police vérifie ce compteur : ~1-3 k tokens au lieu de 25 k+.

### 4.5 Fin du chargement en bloc
Les `*-communaute` et `connaissance.md` ne sont plus lus par les agents : ils appellent `kb.py`.

**Fin phase 4** : sur Derby Manager, `kb.py dm tactique` rend tout le thème sous 3 k tokens avec compteur ; 10 affirmations testables ont un `data_verdict` ; M3 en baisse.

---

## Phase 5 — Orchestrateur, packs de contexte, agents (2 à 3 sessions)

### 5.1 `pipelines/orchestre.py <jeu>`
Remplace l'ordonnancement en prose (`dependances` du YAML exécutable). Calcule les événements nouveaux (match, roster, marché, nouvelle saison), produit un **plan JSON** `(agent, entrées, hash)`. **Cache par hash** : `ops.agent_run(game, agent, input_hash, output_ref, tokens_eq)`; même hash → brief réutilisé, **aucun agent lancé**. Plafonds lus dans la config, exceptions déclarées (annexe A).

### 5.2 `pipelines/contexte_pack.py <jeu> <agent>`
Dossier compact (≤ 3 k tokens) : lignes des vues, `season_context`, `match_objective`, charte, leçons (`garde.py`), affirmations `kb` avec compteur. Passé **dans le prompt** : l'agent ne fait plus 5-10 allers-retours SQL.

### 5.3 `pipelines/verifier_rendu.py`
Contrôle programmatique de R-9 : chaque nom, chiffre, date, `my_result` du rendu existe dans le pack/les résultats SQL du tour. `synthese` seulement pour assembler ≥ 2 briefs. `police` = script d'abord ; l'agent `police` seulement si doute.

### 5.4 Agents
Agents qui **jugent** seulement (`match`, `tactique`, `transferts`, `academie`, `entrainement`, `veille`, `analyste`, `decideur`), prompt ≤ 1 500 tokens. Sortie **JSON** validée, rendu par script (formats R-3/R-4/R-10/R-12 de `forme.py`). Routage : Haiku comptage/reformatage, Sonnet jugement, Opus conception ; l'orchestrateur **annonce** le réglage `/effort` `/model` en une ligne.

### 5.5 `pipelines/rapport_jour.py <jeu>`
Tableau R-3 (🟥/🟧/🟩, catégorie, action) depuis `gold.agenda` + `learn.decision` ouvertes + exports en retard, **aujourd'hui seulement** (R-1 dans la vue). Zéro agent pour le plan du jour.

**Fin phase 5** : M2 ≤ 0,05 M, M3 ≤ 6 tours / ≤ 2 appels SQL, M4 ≤ 5 M, M5 ≤ 12 agents/semaine sur 2 semaines ; rejouer un jour passé = même plan.

---

## Phase 6 — Industrialiser : jeu n°7…n°23
### 6.1 Moteur de userscript unique
`userscripts/engine.js` (capture, filtres `SECRET_KEYS`, `SKIP_URL`, envoi, dédoublonnage) + `userscripts/jeux/<jeu>.config.js`. `pipelines/build_userscripts.py` **concatène** en `userscripts/<jeu>.user.js` (dépôt privé : pas de `@require` GitHub brut). Empreinte par endpoint ; `gold.exports_nouvelles_cles` étendu à une alerte « format changé ».

### 6.2 `pipelines/nouveau_jeu.py <id>`
Génère YAML (`# à vérifier`), config userscript, adaptateur, `resume.md`, entrées `kb`, `docs/checklist-<id>.md`. Procédure : manuel + devlog → claims ; capture ; adaptateur ; `contrat_core.py` vert ; cartes cœur + delta ; registre ToS. **Budget** : ≤ 1 session / ≤ 0,8 M éq. par jeu d'une famille couverte.

### 6.3 Familles
Football (13 jeux) : `docs/fiches/_familles/football/` + deltas. Idem basket (3), hockey (2), autres (5). **Sports individuels** : `core.athlete_daily`, `core.event_calendar`, contrat **après** 4 jeux d'équipe stabilisés.

### 6.4 Registre conditions d'utilisation
Bloc `tos:` du YAML : `verifie_le`, `resume`, `risque`, `automatisation_autorisee`. Sans `tos.verifie_le` : aucune action automatisée ; défaut « lecture + propositions ». « Export en un clic » interdit tant que le bloc ne l'autorise pas.

### 6.5 Ordre
Critères de `docs/jeux.md`. Football en premier une fois Team Soccer et Derby Manager stables sur `core`.

---

## Phase 7 — Qualité, CI, observabilité (1 à 2 sessions)
- `pipelines/test_vues.py` : `select * … limit 1` sur **chaque** vue `silver/gold/core/adapt` ; objets SQL cités par les cartes = présents (test permanent).
- Fixtures figées `tests/fixtures/<jeu>/` pour `my_result`, `season_context`, `match_objective` (match sans score, coupe, playoffs, ligue à 4).
- CI GitHub Actions (privé) : `contexte_budget`, `test_*`, scan de secrets, sqlfluff Postgres, **sans accès Supabase de production**.
- `ops.session_cost` via `mesure_session.py` ; `gold.kpi_hebdo` (tokens/session, agents lancés vs réutilisés, récidives, % décisions évaluées, confirmation des leçons, fraîcheur, dernière sauvegarde).
- Sauvegardes : 0.6 + export `kb`, `learn`, schéma. Dérive de schéma : 6.1.

---

## Phase 8 — Futur (quand 1-5 stables)
- **Backtests** (`learn.backtest`) : rejouer le passé via `as_of`, comparer des politiques avant de promouvoir une règle. Atout stratégique : conserver le bronze (0.6).
- **Modèles légers** Python : prix de transfert attendu, probabilité de victoire (score de Brier) ; gardés seulement s'ils battent la règle simple.
- **Notification du soir** (script, aucune action sur les sites). **Vue web minimale** sur `gold.agenda`, `learn.decision`, `gold.kpi_hebdo`.
- **Traitement massif à tarif réduit** si clé API (backfill `kb` par lots).
- **Apprentissage inter-jeux** : leçons `transversal` proposées comme **hypothèses**, jamais règles (A-10 sans coût de session).
- **Confidentialité** : pseudonymiser les auteurs Discord dans les exports générés.

---

## Annexe A — Contradictions à trancher
| Conflit | Décision |
|---|---|
| Règle 75 « tout lire en ENTIER » vs règles de coût | **Complétude par requête** (P3) : tout le thème via `kb.py`/vues avec compteur ; jamais un corpus entier en contexte. Le hook vérifie le compteur. |
| R-8 « je tranche » vs règle 75/81 « laisser l'utilisateur arbitrer » | **Je tranche** ; l'utilisateur n'est sollicité que pour les actions irréversibles (§0.4) et le budget d'un backfill. |
| Plafond 20 agents/semaine + 3 par passage vs `police` obligatoire + `analyste` + `decideur` | Plafond **appliqué par l'orchestrateur** ; exceptions : `police` (script d'abord), `analyste` sur défaite. |
| A-10 initiative multi-jeux vs « un jeu par session » | **Supprimer A-10 comme comportement de session.** La propagation passe par le cœur. |
| R-9 « vérifié avant d'être dit » vs coût | Vérification **programmatique** (`verifier_rendu.py`). |
| « Lire `regles-apprises.md` au début » vs budget | Remplacée par le hook de début de session (titres des règles actives). |
| « Règle d'or » + « exception transferts » + R-1 | Une formulation dans `CLAUDE.md` ; implémentée dans `gold.agenda` ; exception transferts = champ de la vue. |
| Hook `police` bloquant les « mots d'aveu » en discussion de conception (H4 corrigé) | Garder H4 ; un test par faux positif (`test_police.py`). |

## Annexe B — DDL indicatifs (non exécutés ; à valider)
### B.1 `core` (extraits)
```sql
create schema if not exists core;
revoke all on schema core from public, anon, authenticated;

create table core.game_params (
  game text not null, key text not null, value jsonb not null,
  source text, verified_on date,
  primary key (game, key)
);
-- clés : points_par_victoire, rounds_total, promo_slots, releg_slots,
-- age_declin, effectif_min, effectif_max, seuil_confirmation_lecon, ...

-- Vue (union des adaptateurs, générée par pipelines/build_core.py)
-- create or replace view core.player_daily as
--   select * from adapt.basketvibe_player_daily
--   union all select * from adapt.hockeynation_player_daily ...;
-- Colonnes attendues :
--   game text, team_id text, club_label text, player_id text, day date, name text,
--   position text, age int, rating numeric,   -- 0-100
--   form numeric, fatigue numeric, morale numeric,  -- 0-1
--   injured boolean, suspended boolean,
--   salary numeric, contract_end date, market_value numeric,
--   is_academy boolean, skills jsonb, extras jsonb

-- core.fixture : game, team_id, fixture_id, competition_kind text
--   check (competition_kind in ('ligue','coupe','amical','playoff','autre')),
--   round_no int, rounds_total int, scheduled_at timestamptz, played boolean,
--   my_score int, opp_score int, my_result text check (my_result in ('W','D','L')),
--   opponent text, home boolean, extras jsonb
-- core.standing : game, team_id, season_id, round_no, rank, played, points,
--   wins, draws, losses, gf, ga, extras jsonb
-- core.finance_daily : game, team_id, day, balance, income, expenses, salaries,
--   wage_cap, capacite_invest, extras jsonb
```
### B.2 `learn`
```sql
create schema if not exists learn;
revoke all on schema learn from public, anon, authenticated;

create table learn.decision (
  id            bigint generated always as identity primary key,
  game          text not null,
  team_id       text,
  domain        text not null check (domain in
                ('composition','tactique','entrainement','academie','achat','vente','finances','infrastructure','personnel')),
  decided_at    timestamptz not null default now(),
  label         text not null,
  hypothesis    text not null,
  prediction    jsonb not null,
  eval_after    timestamptz not null,
  evidence      jsonb not null default '[]',
  strategy_snapshot jsonb,
  status        text not null default 'proposed'
                check (status in ('proposed','accepted','rejected','done','expired')),
  user_note     text
);

create table learn.outcome (
  decision_id bigint primary key references learn.decision(id),
  measured_at timestamptz not null default now(),
  observed    jsonb not null,
  verdict     text not null check (verdict in ('confirmed','contradicted','inconclusive')),
  note        text
);

create table learn.lesson (
  id           text primary key,
  game         text not null,
  domain       text not null,
  claim        text not null,
  check_sql    text,
  status       text not null default 'hypothesis'
               check (status in ('hypothesis','validated','hard_rule','retired')),
  n_for int not null default 0, n_against int not null default 0,
  created_at timestamptz not null default now(), promoted_at timestamptz,
  source_decisions bigint[] not null default '{}'
);

create table learn.error (
  id           bigint generated always as identity primary key,
  game         text, description text not null,
  recurrence   int not null default 1,
  enforcement  text not null check (enforcement in ('hook','sql','test','prose')),
  guard_ref    text,
  opened_at    timestamptz not null default now(), closed_at timestamptz
);
-- Une erreur à recurrence >= 2 ne peut passer closed_at que si enforcement <> 'prose'.
```
### B.3 `kb` et `ops`
```sql
create schema if not exists kb;
revoke all on schema kb from public, anon, authenticated;

create table kb.claim (
  id            bigint generated always as identity primary key,
  game          text not null, domain text not null,
  text          text not null,
  source_kind   text not null check (source_kind in
                ('manuel','devlog','patchnote','discord','forum','chat','observation')),
  source_ref    text not null, author text, said_at timestamptz, game_version text,
  status        text not null default 'en_doute'
                check (status in ('confirme','complete','contredit','en_doute','obsolete')),
  confidence    numeric(3,2) not null default 0.30,
  superseded_by bigint references kb.claim(id),
  contradicts   bigint[] not null default '{}',
  data_check_sql text, data_checked_at timestamptz, data_verdict text,
  fts tsvector generated always as (to_tsvector('french', text)) stored
);
create index kb_claim_fts on kb.claim using gin (fts);
create index kb_claim_game_domain on kb.claim (game, domain, confidence desc);

create schema if not exists ops;
revoke all on schema ops from public, anon, authenticated;
create table ops.agent_run (
  id bigint generated always as identity primary key,
  game text not null, agent text not null, input_hash text not null,
  started_at timestamptz not null default now(),
  output_ref text, tokens_eq bigint,
  unique (game, agent, input_hash)
);
```

## Annexe C — Boucle quotidienne cible
```
orchestre.py <jeu>            → plan JSON (agents à lancer, cache par hash)
contexte_pack.py <jeu> <agt>  → pack ≤ 3 k tokens (vues + objectif + charte + leçons + kb)
agent (Sonnet, medium)        → JSON {action, justification, sources[], confiance, preuve_d_erreur, date_test}
verifier_rendu.py             → chaque nom/chiffre/date existe dans le pack ; sources valides
decision.py new               → learn.decision (prédiction mesurable)
garde.py                      → leçons validées + revirements + erreurs ouvertes
forme.py / police.py          → format et hooks (existants)
rapport_jour.py               → tableau R-3, aujourd'hui seulement
evaluer_decisions.py (cron)   → outcome, leçons promues/retirées, KPI hebdo
```

## Annexe D — Squelette du nouveau `CLAUDE.md` (≤ 90 lignes)
- **Rôle** : assistant de gestion de clubs ; pilote BasketVibe ; français, court ; ne jamais deviner une règle de jeu : citer la source.
- **Inviolables** (≤ 12, une ligne chacune) : collecte passive uniquement ; jamais d'enchère/achat/vente sans accord ; horizon **aujourd'hui seulement** ; tout chiffre vient d'une requête du tour ; résultat = `my_result` ; je tranche (une action, le doute en une demi-ligne) ; décision importante = `dossier.py` + `garde.py` ; un jeu par session et `/clear` après commit ; secrets dans `.env`, Discord en base pas en Git ; conception = Opus.
- **Carte du dépôt** (8 lignes) : `core`, `gold`, `kb`, `learn`, `pipelines`, cartes, fiches, YAML, règles actives.
- **Commandes** : `sql.py`, `dossier.py`, `orchestre.py`, `contexte_pack.py`, `kb.py`, `garde.py`, `mesure_session.py`.
- **Renvois** : `docs/regles/actives.md`, `docs/attentes/attentes.md` (R/A), `docs/refonte-v2/plan.md`.
Tout autre contenu de l'ancien `CLAUDE.md` est classé E/S/K/D dans `triage.md`.

## Annexe E — Prompt pour lancer la Phase 0
> Lis `docs/refonte-v2/plan.md` §0, §1 et **Phase 0 uniquement**. Travaille sur la branche `refonte-v2`. Exécute 0.0 → 0.5 dans l'ordre, un commit par étape, en mesurant avant/après (M1–M7). Ne coche la case dans `docs/refonte-v2/journal.md` que lorsque le critère de fin est vérifié. **Arrête-toi et demande** avant : toute clé trouvée dans l'historique, la purge d'historique Git, tout `git rm` de données, toute écriture irréversible sur Supabase. Ne touche ni au bronze ni aux silver. Si M4 ne baisse pas après 0.3, arrête-toi et analyse. Rends à la fin : les 7 mesures avant/après, la liste des règles par classe (E/S/K/D), et ce qui reste à faire pour la Phase 1.

## Annexe F — Risques et parades
| Risque | Parade |
|---|---|
| Casser un jeu en production | Strangler + `except` 7 jours + tag `avant-refonte-v2` + suppression de l'ancien après 30 jours |
| Contrat `core` trop rigide | `extras`, `null` déclaré, sports individuels plus tard |
| Formules de valeur fausses | Backtest obligatoire, fiabilité affichée, hypothèse non promue sans confirmations |
| Coût du backfill `kb` | Filtrage SQL, estimation chiffrée et accord, reprise par curseur |
| Règles « E » jamais implémentées | `learn.error.enforcement = 'prose'` visible au KPI ; récidive ≥ 2 sans enforcement code = alerte |
| Perte du bronze | Sauvegarde hebdomadaire hors Git (0.6) + test de restauration |
| Jeu qui change de format | Empreinte par endpoint + alerte avant décision |
| Bannissement | Collecte passive, `tos:` par jeu, aucune automatisation sans autorisation vérifiée |

## Annexe G — Estimations (cibles, pas mesures)
| Phase | Sessions | Effet attendu |
|---|---|---|
| 0 | 1 soirée | Contexte fixe ÷ 3-4 ; sécurité ; mesure en place |
| 1 | 2-3 | Maintenance vues/cartes ÷ ~6 |
| 2 | 2 | Décision contextuelle calculée en SQL |
| 3 | 2 | « Ne pas se répéter » garanti par la base |
| 4 | 2-3 | Wiki interrogeable, lecture ~10× moins chère |
| 5 | 2-3 | Agents : 0,45 M → ≤ 0,1 M éq., ≤ 12/semaine |
| 6 | 2 + 1 par jeu | Nouveau jeu en ≈ 1 session |
| 7 | 1-2 | Régressions détectées avant l'usage |

Seule la baseline de §1 fait foi.

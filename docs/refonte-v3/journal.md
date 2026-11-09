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
- [x] Tour réel BasketVibe du 2026-11-05 (13:47 Paris) : 2,4 min jusqu'au premier rendu (`date -u` 12:47:58 → 12:50:21), 1 retour de hook Stop, 0 police (aucun agent `police` lancé de toute la session, dont 3 agents d'analyse et 1 saisie de composition enregistrée sous le n° 1072). Détail : journal de durée ci-dessous. **Réserve** : tour léger (exports seulement) ; aucun transfert rendu, donc le passage de la police sur un gros transfert n'est pas encore observé. Les tours suivants (agents, questions) n'ont pas de durée mesurée.

### Journal de durée (manuel, une ligne par tour)
| Date | Jeu | Durée (min) | Retours de hooks Stop | Police hors transfert |
|---|---|---|---|---|
| 2026-11-05 13:47 Paris | basketvibe | 2,4 (12:47:58 → 12:50:21 UTC, mesuré par `date -u`, jusqu'au rendu) | 1 (`police.py` : formule d'aveu dans une phrase + export Académie classé en catégorie Académie/Draft, donc pris pour une décision ; corrigé en catégorie Export, sans police) | 0 (aucun agent lancé) |
| 2026-11-05 | basketvibe (exports reçus → `analyste`, `academie`) | non mesurable (début 12:52:56 UTC, fin non relevée) | 2 (fichiers non commités : registre, puis brief académie) | 0 |
| 2026-11-05 | basketvibe (question amical → `tactique`) | non mesurable (début non relevé ; rendu vers 13:0x UTC) | 1 (`controle.py` g : « je ne peux pas » sans preuve) | 0 |
| 2026-11-05 | basketvibe (règle des amicaux) | non mesurable | 2 (`police.py` rappel rétro ; `controle.py` écriture par script + identifiant interne) | 0 |

## S4 — Vues rapides (2026-11-05) — **INCOMPLÈTE : arrêt pour décision**

Prérequis vérifiés : `git log origin/main` contient 5436788 ; `CLAUDE.md` inviolable 6 = gros transferts seulement (3320dd3) ; `python -I pipelines/sql.py "select 1"` → `1`. Branche `ccr-d374a4ca-pxf92j` recréée depuis `origin/main` après la fusion de la PR 5.

### Étape 1 — Mesure « avant »
Commande (rejouable) : `SQL_TRANSPORT=https python -I pipelines/mesure_vues.py --vues <vues> --passes 3` (script `pipelines/mesure_vues.py` : `select count(*) from (select * from <vue> where game = '<jeu>') t`, temps mural en ms, timeout = 20 s du rôle `assistant_ro`). Tableaux complets : `docs/refonte-v3/mesures-s4/avant_core.md`, `avant_gold.md`, `apres.md`.
- **Piège de mesure** : `sql.py` sonde le port 5432 (bloqué en cloud) à chaque appel : `select 1` = 6,6 s en transport automatique, 0,54 s avec `SQL_TRANSPORT=https`. Une première mesure (jetée) était faussée de 6,5 s par appel. Le script fixe maintenant le transport une fois (bef2da7). **Effet de bord à décider hors S4** : toute requête `sql.py` en session cloud coûte 6,3 s de trop tant que `SQL_TRANSPORT=https` n'est pas défini dans l'environnement cloud.
- Avant, `core.*` (médiane de 3 passages, 6 jeux) : 8 vues sur 10 déjà < 2 s ✅ (fixture, finance_daily, market_listing, academy_prospect, staff, training_plan, facility, season). ❌ `core.standing` 9,4 à 11,1 s (6 jeux) ; ❌ `core.player_daily` hardwood 6,6 s, teamsoccer 5,4 s (autres jeux < 1 s).
- Avant, gold : `season_context` timeout sur les 6 jeux ; `daily_alerts` timeout sur les 6 jeux ; `match_objective` timeout sur 4 jeux (derbymanager, hardwood : valeur non fiable, voir l'en-tête de `avant_gold.md`).
- Taille de la base avant : `select pg_size_pretty(pg_database_size(current_database()))` → 252 Mo = 50,4 % du quota de 500 Mo. 10 plus grosses relations : `bronze.discord_messages` 108,7 Mo, `bronze.raw_pages` 90,9 Mo, `public.dugout_matches` 24,4 Mo, `kb.claim` 5,7 Mo, `learn.decision` 0,8 Mo, puis < 0,6 Mo.
- **Causes trouvées** (connecteur, rôle `postgres`, `explain (analyze, buffers)` + temps par adaptateur) : (1) chaque adaptateur silver relit et parse le JSON de `bronze.raw_pages` à chaque lecture ; (2) dans `core.standing`, le filtre `game = '…'` n'est pas poussé dans les branches à fonction de fenêtre : les 5 autres jeux sont calculés en entier (`teamsoccer_standing` 9,5 s pour 0 ligne retournée) ; (3) adaptateurs lents seuls : `adapt.teamsoccer_standing` 7,5 s, `derbymanager_standing` 2,5 s, `hockeynation_standing` 1,4 s, `hardwood_player_daily` 5,3 s, `teamsoccer_player_daily` 4,9 s. Une réécriture (étape 2a) ne suffit donc pas : ces adaptateurs sont lents même isolés.

### Étape 2 — Correction
- [x] 2b `core.standing` et `core.player_daily` en vues matérialisées : `sql/core/013_vues_materialisees.sql` (appliquée par le connecteur, nom de migration `core_013_vues_materialisees`). Les vues d'origine sont renommées `core.standing_src` et `core.player_daily_src` (non supprimées). Index uniques `(game, team_id, season_id, day)` et `(game, team_id, player_id, day)` (vérifiés : 134/134 et 1 559/1 559 clés distinctes) pour le rafraîchissement `concurrently`. `select` accordé à `assistant_ro`. Les vues gold qui les lisaient ont été recréées pour viser les nouvelles vues (liaison par identifiant : sinon elles auraient suivi les `_src`) : `season_context`, `exports_state`, `roster_bilan`, `daily_alerts`. Une première tentative a échoué (références de colonnes `player_daily_src.game` non remplacées), annulée par la transaction, état vérifié inchangé, puis corrigée.
- Après (`apres.md`) : `core.standing` 262 à 572 ms, `core.player_daily` 280 à 449 ms, `gold.season_context` 252 à 445 ms, sur les 6 jeux ✅.
- **Contenu identique avant/après** (hash md5 du contenu, `select count(*), md5(string_agg(t::text,'|' order by t::text)) from <vue> t`) : `core.standing` 134 lignes `a6135bcb155ba74c1878c7629d937529` ; `core.player_daily` 1 559 `2ba35ade168edbfeb721bd8e8f474114` ; `gold.season_context` 8 `1842552465595cd96202bae7fff1ae4a` ; `gold.finance_health` 7 `a57569367c777058014ef14aa727e816` ; `gold.roster_bilan` 230 `7aafcc91df8562c0128b92cf2bb41c5f` : mêmes valeurs mesurées après la migration. Non comparés après : `match_objective` 51 `f008f4933e1bc60a62fb5a544a81c98f`, `exports_state` 88 `d27ca490729518a154ea97dd31e7cdde`, `agenda` 39 `7c61ccbf1c9a2ebb865a952a89c56a99` (empreintes « avant » prises, « après » non relevées) ; `daily_alerts` : empreinte « avant » non mesurable (> 60 s même en `postgres`).
- [ ] **Non fait, arrêt demandé par la consigne** (vue encore ≥ 2 s après correction) :
  - `gold.match_objective` / teamsoccer : 3 895 ms (médiane). Cause : non isolée (autres jeux < 1,7 s ; `core.fixture` teamsoccer seul ≈ 1,1 s). Piste : matérialiser la vue (clé `game, team_id, fixture_id`) ou lire `core.fixture` filtré par jeu.
  - `gold.daily_alerts` : 6,9 à 11,6 s sur 4 jeux, timeout hardwood et teamsoccer. Cause : elle relit les anciennes vues par jeu `gold.ts_daily_alerts` (~22 s), `gold.hw_daily_alerts` (~22 s), `gold.hn_daily_alerts` (~2,9 s) et `gold.exports_state` (~4,3 s) (mesures prises en parallèle, donc gonflées par la concurrence). Piste : matérialiser `daily_alerts` ; la vue n'a pas de clé naturelle (un index unique sur expression n'est pas accepté par `refresh … concurrently`) : soit une colonne `cle` ajoutée (change la forme de la vue), soit un rafraîchissement bloquant. De plus ses alertes dépendent de `now()` / `current_date` (péremption d'export, enchères en cours) : une vue matérialisée est périmée entre deux rafraîchissements.

### Étape 2c/2d — Rafraîchissement
- Chemin d'arrivée d'une page : userscript Tampermonkey → RPC `public.ingest_raw_pages(p_token, p_items)` (SECURITY DEFINER, 500 éléments max) → `bronze.raw_pages`. Aucun trigger autre que `raw_pages_immutable`. `pg_cron` et `pg_net` sont disponibles, non installés (`pg_available_extensions`, `installed_version` vide).
- **Rien n'est planifié aujourd'hui** : les deux vues matérialisées ne se mettent pas à jour toutes seules. La fonction `core.rafraichir_vues()` existe (déclenchement manuel, `revoke` public).
- Durée d'un rafraîchissement complet (`refresh materialized view concurrently`, transaction annulée) : `standing` 14 826 ms + `player_daily` 14 352 ms = **29,2 s** ; `standing` seul 19,9 s lors du test avec page factice.
- Test « page factice » (transaction annulée par `raise exception`, bronze non touché en production) : copie de la dernière page `my-competition` de sixzeroleague avec `standings[0].points = 999` → points max avant 8 ; après insertion **sans** rafraîchir 8 ; après `refresh … concurrently` **999**. Après annulation : `select count(*) from bronze.raw_pages where client='test-s4'` → 0 ; `core.standing` 134 lignes, points max sz 8.
- **Choix du mécanisme (à valider avant implémentation)** : (1) rafraîchir à l'arrivée d'une page : écarté, la RPC tourne sous le délai de 8 s du rôle d'API et un rafraîchissement de 29 s ferait échouer l'insertion d'une page (perte de collecte) ; (2) `pg_cron` toutes les N minutes avec garde « seulement si une page est arrivée depuis le dernier rafraîchissement » : possible, limite = vue périmée jusqu'à N minutes, charge CPU ~30 s par passage ; (3) appel explicite en début de soirée : possible, limite = dépend d'un oubli. Recommandation : (2) avec N = 10, plus un appel explicite avant tout `que faire` du soir. Proposé, non implémenté.
- Taille après : `select pg_database_size(current_database())` → 254,0 Mo = **50,8 %** du quota (seuil d'alerte 70 % : non atteint). Objets ajoutés : `core.player_daily` 1,73 Mo + index 0,19 Mo, `core.standing` 0,13 Mo + index 0,05 Mo, soit ~2,1 Mo = 0,4 % du quota.

### Étape 3 — Non-régression
- [ ] **Scripts de parité (`agenda_parite.py`, `alertes_parite.py`, `exports_parite.py`, `finances_parite.py`, `contrat_core.py`) : non mesurables dans cette session.** Lancés avant : les 5 sortent en code 1 avec `psycopg.errors.ConnectionTimeout` (connexion directe au port 5432, bloquée par le proxy cloud). À rejouer en local avant la fusion. `recette.py --tous` : arrêt à 120 s sans sortie (même cause probable, non vérifiée).
- Noms des vues inchangés (`select` par `sql.py` sur `gold.season_context`, `match_objective`, `daily_alerts`, `core.standing`, `core.player_daily` : même noms, même colonnes) ; skills `*-aujourdhui` non modifiés.
- [ ] **« 0 timeout dans un dossier de test » : non mesurable ici.** `python pipelines/dossier.py` : basketvibe code 124 (arrêt à 120 s), teamsoccer code 0 en 61,4 s, hockeynation code 0 en 61,2 s. Le dossier contient « ⚠ base injoignable (connection timeout expired) » : en cloud il se connecte en direct (`psycopg`), n'interroge donc aucune vue, et ses 61 s sont des attentes de connexion. À rejouer en local.

### Preuves de fin demandées
| # | Preuve | État |
|---|---|---|
| 1 | 3 vues gold < 2 s sur 6 jeux | ❌ `season_context` ✅ ; `match_objective` ✅ sauf teamsoccer (3,9 s) ; `daily_alerts` ❌ |
| 2 | 0 timeout dans 3 dossiers | non mesurable en cloud (voir ci-dessus) |
| 3 | Parité avant/après identique | non mesurable en cloud ; substitut : hash de contenu identique pour 5 vues |
| 4 | Taille base et objets | ✅ 50,8 % ; objets 0,4 % ; < 70 % |
| 5 | Durée d'un rafraîchissement complet | ✅ 29,2 s (2 vues) |

## S4b — Finir les vues rapides (2026-11-05) — **un point reste ouvert : parité locale**

Décisions de l'utilisateur appliquées : `pg_cron` toutes les 10 minutes avec garde « page arrivée » ; appel explicite avant le que faire du soir ; `gold.daily_alerts` matérialisée avec `cle` et `rafraichi_a` à la fin ; `gold.match_objective` : filtre par jeu d'abord, matérialisation ensuite si nécessaire.
Migrations (une par fichier) : `sql/core/014_rafraichissement.sql`, `015_daily_alerts_materialisee.sql`, `016_match_objective_materialisee.sql`, `017_daily_alerts_bascule.sql`, `018_cron_delai.sql`, `019_avant_soir_fraicheur.sql`, `sql/learn/002_decision_ecrire_https.sql`. Aucun hook ajouté, `CLAUDE.md` non touché, aucun `drop policy`.

### 1. pg_cron et rafraîchissement automatique
- [x] Extension installée par le connecteur (`create extension if not exists pg_cron with schema pg_catalog`, rôle `postgres`) : pas de blocage de droits.
- [x] Jobs (`select jobid, jobname, schedule, command, active, username from cron.job order by jobid`) :
  `1 rafraichir-vues | */10 * * * * | set statement_timeout = '15min'; select * from core.rafraichir_vues(false) | actif | postgres` ;
  `2 rafraichir-demande | * * * * * | set statement_timeout = '15min'; select core.rafraichir_si_demande() | actif | postgres` ;
  `3 purge-cron | 17 3 * * * | delete from cron.job_run_details where end_time < now() - interval '3 days' | actif | postgres`.
- [x] Garde : `core.rafraichir_vues(false)` compare `max(bronze.raw_pages.id)` à `core.rafraichi_etat.last_page_id` ; sans page nouvelle elle sort en 0,1 à 0,2 s. `cron.job_run_details` : `rafraichir-vues succeeded 16:30:01 0.1s` et `succeeded 16:40:00 0.2s`.
- [x] Passage de job avec rafraîchissement : `rafraichir-demande succeeded 2026-11-05 16:22:00 29.9s` (2 vues, avant les 2 autres vues), `succeeded 16:34:12 116.6s` et `succeeded 16:39:00 116.6s` (4 vues). État : `debut=16:39:00 fin=16:40:56 duree_ms=116298 last_page_id=37245`.
- **Constat à connaître** : les sessions `pg_cron` ont `statement_timeout = 2min` (sonde : `raise exception` dans un job → `SONDE statement_timeout=2min lock_timeout=0 user=postgres`). Un premier passage à 4 vues a échoué à 130,6 s (`canceling statement due to statement timeout`, dans `refresh … gold.daily_alerts`, pendant que je lançais d'autres requêtes en parallèle) et se relançait chaque minute. Corrigé par la migration 018 : `set statement_timeout = '15min'` devant l'instruction du job (sonde : un `set statement_timeout = '3s'` posé ainsi coupe bien l'instruction suivante, échec à 3,4 s) et une demande n'est honorée que pendant 5 minutes. **Marge faible** : 116 s sur 120 s sans ce correctif.
- **Changement de contenu après passage de job : non démontré par un passage réel.** Aucune page n'est arrivée dans `bronze.raw_pages` (`last_page_id` constant à 37245) : les empreintes md5 de `core.standing` (`a6135bcb…`) et `core.player_daily` (`2ba35ade…`) sont identiques avant et après les passages du job. Bronze est immuable en production : pas d'insertion réelle. La preuve de reflet reste le test annulé de S4 (points max 8 → insertion sans rafraîchir 8 → après rafraîchissement 999 → annulation, 0 page factice). À confirmer à la première vraie page.
- [ ] Réserve : la garde ne voit que les nouvelles pages. Les alertes de `daily_alerts` dépendent de `now()` (âge des exports, enchères en cours) ; elles sont figées entre deux rafraîchissements.

### 2. Appel explicite avant le soir
- [x] `public.rafraichir_avant_soir()` (security definer, `search_path` vide, `execute` accordé à `service_role` et `assistant_ro`, au plus une demande par minute) + `pipelines/rafraichir_avant_aujourdhui.py` (POST, clé de service).
- **Écart avec la consigne (« test : appel par sql_ro »)** : `sql_ro` s'exécute en transaction lecture seule, la fonction ne peut pas écrire sa demande. Preuve : `SQL_TRANSPORT=https python -I pipelines/sql.py "select public.rafraichir_avant_soir()"` → `erreur SQL (https 405) : cannot execute SELECT FOR UPDATE in a read-only transaction` (1,0 s). L'appel passe donc par le script en POST : réponse en 0,6 s (`python -I pipelines/rafraichir_avant_aujourdhui.py` → `à jour : rafraîchi à 16:22:30`) ; avec attente : `demandé` → `déjà demandé` → `en cours` ×N → `à jour : rafraîchi à 16:22:30`, 42,6 s pour 2 vues.
- Ligne « 0 bis » ajoutée à `basketvibe-aujourdhui`, `sixzeroleague-aujourdhui`, `teamsoccer-aujourdhui` (attente jusqu'à 5 min, délai d'outil 600 s). `hardwood-aujourdhui` n'a pas d'étape 0 : non modifié.

### 3. `gold.daily_alerts`, `gold.match_objective`, `gold.season_context` (SQL_TRANSPORT=https, médiane de 3 passages)
Commande : `SQL_TRANSPORT=https python -I pipelines/mesure_vues.py --vues gold.season_context,gold.match_objective,gold.daily_alerts,core.standing,core.player_daily --passes 3`. Tableau complet : `docs/refonte-v3/mesures-s4/apres_s4b.md`. Avant : voir `avant_gold.md` (timeout sur les 6 jeux pour `season_context` et `daily_alerts`, 4 jeux sur 6 pour `match_objective`).
- [x] **Les 30 couples vue/jeu sont < 2 s** : `gold.season_context` 439 à 556 ms ; `gold.match_objective` 419 à 473 ms (teamsoccer : 3 895 → 446 ms) ; `gold.daily_alerts` 287 à 453 ms (avant : 6,9 à 11,6 s et 2 timeouts) ; `core.standing` 238 à 442 ms ; `core.player_daily` 418 à 446 ms.
- `match_objective` teamsoccer : le filtre par jeu était déjà poussé (le plan ne lit que la branche teamsoccer) ; coût = adaptateur de matchs lu deux fois (3,4 s + 0,9 s). Matérialisée (016), clé unique `(game, team_id, fixture_id)`.
- [x] **Contenu identique** (md5) : `gold.match_objective` 51 lignes `f008f4933e1bc60a62fb5a544a81c98f` avant et après ; `gold.season_context` 8 lignes `1842552465595cd96202bae7fff1ae4a` avant et après (S4). `gold.daily_alerts` : comparaison à la vue d'origine `daily_alerts_src` faite avant la bascule : basketvibe (7) et sixzeroleague (13) md5 identiques ; derbymanager, hockeynation, hardwood (12), teamsoccer (13) : mêmes lignes, seul le compteur d'heures d'un export diffère (« 66 h » / « 65 h », vue calculée 40 min plus tard ; avec ce compteur neutralisé, 0 ligne différente pour hardwood et teamsoccer). Les colonnes d'origine ne sont ni modifiées ni réordonnées ; `cle` et `rafraichi_a` sont en fin de vue.
- **Coût** : un rafraîchissement de `daily_alerts` seul dure ~2 min (anciennes vues par jeu `gold.ts_daily_alerts` et `gold.hw_daily_alerts` ~22 s chacune, `gold.exports_state` ~4 s, `gold.hn_daily_alerts` ~3 s ; mesures prises en parallèle, donc gonflées). Cause racine non traitée (ces vues par jeu), piste : les alléger plutôt que de matérialiser la somme.

### 4. Cloud : transport commun
- [x] `sql.py` : `transport()` renvoie `https` si `CLAUDE_CODE_REMOTE=true` (plus de sonde du port 5432) ; `select 1` : 6,8 s → 0,54 s. Ajout de `executer()` et `rpc_post()`.
- [x] `dossier.py` lit par `executer()` (plus de `psycopg` direct). `decision.py` : lecture par `executer()`, écritures par `public.decision_ecrire(p jsonb)` en POST (service_role seulement, migration `sql/learn/002`). `kb.py` et `export_learnings_md.py` ne tentent plus la connexion directe en transport https (30 s perdues par appel : 125 s et 31 s dans le profil de `dossier.py`).
- [x] `python pipelines/dossier.py <jeu> composition` en cloud, code 0, aucun « base injoignable », 0 « ⚠ erreur » : **basketvibe 18,3 s, teamsoccer 24,2 s, hockeynation 12,4 s** (< 60 s). Avant : 124 (arrêt à 120 s), 56 s et 42 s dont l'essentiel en attentes de connexion, aucune vue interrogée.
- [x] Tests : `python -I pipelines/test_sql.py | tail -1` → `12/12` ; `python -I pipelines/test_decision.py | tail -1` → `15/15`.
- Câblage de `decision.py` en https vérifié sans écrire : `liste basketvibe` → lignes `D-1072…` ; `new … --lecon L-999999` → `❌ décision refusée : leçon basketvibe:L-999999 introuvable` (refus par la base) ; `statut 999999999 done` → `❌ décision D-999999999 introuvable`. **Non testé : une écriture réelle** (créerait une décision de production) ; le chemin `ok = true` est donc non éprouvé.

### 5. Non-régression
- [ ] **Parité locale : à faire par l'utilisateur** (`agenda_parite.py`, `alertes_parite.py`, `exports_parite.py`, `finances_parite.py`, `contrat_core.py`, `recette.py --tous`, connexion directe, port 5432 bloqué en cloud). Sorties « avant » de S4 : aucune (ces scripts n'ont jamais tourné en cloud). Case décochée tant que les sorties ne sont pas collées ici et comparées. Attention : `alertes_parite.py` compare des alertes à des anciennes vues : `gold.daily_alerts` est maintenant figée entre deux rafraîchissements.
- Substitut en cloud : md5 de contenu identique pour `core.standing`, `core.player_daily`, `gold.season_context`, `gold.match_objective`, `gold.finance_health`, `gold.roster_bilan` (avant/après la migration de S4) ; `gold.exports_state` et `gold.agenda` : empreintes « avant » prises (`d27ca490…`, `7c61ccbf…`), « après » non relevées.

### Preuves de fin
| # | Preuve | État |
|---|---|---|
| a | `cron.job` et `cron.job_run_details` en `succeeded` | ✅ voir § 1 |
| b | `daily_alerts`, `season_context`, `match_objective` < 2 s sur 6 jeux | ✅ 30 couples, § 3 |
| c | md5 identique | ✅ avec la réserve du compteur d'heures de `daily_alerts` |
| d | `dossier.py` cloud < 60 s | ✅ 18,3 / 24,2 / 12,4 s |
| e | parité locale collée | ❌ en attente de l'utilisateur |
| f | taille base < 70 % du quota | ✅ 254,6 Mo = **50,93 %** ; 4 vues matérialisées : `core.player_daily` 1,73 Mo, `core.standing` 0,13 Mo, `gold.daily_alerts` 0,09 Mo, `gold.match_objective` 0,08 Mo (≈ 2,0 Mo, 0,4 %) |
| g | durée du rafraîchissement complet (4 vues) | ✅ **116,5 s** (`duree_ms` 116 482 et 116 298) |

## L2 — `aujourdhui.py basketvibe` (2026-11-06) — **INCOMPLET : preuves en base non mesurables sur ce PC**

### 1. Ligne « 0 bis » retirée (commit f1780af, poussé)
Commande : `grep -l "core\.standing\|core\.player_daily" sql/gold/*bv*` → **aucune sortie, code 1** (aucun fichier `sql/gold/*bv*` ne référence `core.standing` ni `core.player_daily`).
Réserve : la commande du lot (`grep -l "bv_\|core\.standing\|…"`) liste tous les fichiers bv_ (le motif `bv_` suffit) ; j'ai donc cherché les deux tables seules. Les définitions des vues lues par le skill sont toutes dans `sql/gold/*bv*` sauf `bv_exports_state` (`sql/gold/037_ts_bv_routine.sql`, qui lit `silver.bv_api`) et `bv_saisie_adversaires` (`023_bv_saisie_tactique.sql`) : aucune ne cite les deux tables. **Non mesuré** : la dépendance transitive en base (`pg_depend`), impossible faute de transport (§ 3).

### 2. Livrés
- `pipelines/aujourdhui.py` (commit 3a933be) : lit en lecture seule par `executer()` les 11 vues du lot + `bv_saisie_adversaires` (aperçu) + `bv_transfer_history` (dernière vente) ; rend « Exports à faire aujourd'hui » puis Composition, Tactique, Entraînement, Transferts, Finances, Personnel au format de `forme.py`. « Personnel » est rendu avec la catégorie `Finances` et « Exports » avec `Export` (catégories fixes de `forme.py`). Aucun modèle, aucun agent. Une vue illisible s'écrit « il me manque X — export Y » ; chaque exécution ajoute une ligne à `docs/refonte-v3/journal-aujourdhui.md`.
- `--jour` : seule `bv_transfer_history` se rejoue (`sold_on <= jour`) ; toutes les autres lisent `current_date` ou `now()` → « rejeu non disponible pour <vue> ».
- `pipelines/test_aujourdhui.py` : `PYTHONIOENCODING=utf-8 python -I pipelines/test_aujourdhui.py | tail -1` → **15/15** (données figées, sans réseau ; vérifie aussi que chaque tableau passe `forme.plan`).

### 3. Preuves de fin
| # | Preuve | État |
|---|---|---|
| a | `python -I pipelines/aujourdhui.py basketvibe` < 60 s, sortie complète | ❌ **non mesurable** : `.env` de ce PC a `SUPABASE_URL` mais `SUPABASE_SECRET_KEY` et `SUPABASE_DB_URL_RO` vides, port 5432 fermé (`python -I pipelines/sql.py "select 1"` → « port 5432 fermé et SUPABASE_URL / SUPABASE_SECRET_KEY absents »). Le script sort alors 13 lignes « il me manque … » en 0,0 s : ce n'est pas une mesure, la ligne de `journal-aujourdhui.md` a été supprimée. |
| b | Remplacée le 2026-11-06 par le mode ombre (3 soirs) et l'instantané quotidien ; décision de l'utilisateur. | ➖ remplacée |
| c | `test_aujourdhui.py` vert | ✅ 15/15 |

### 4. Cause et piste
- Cause : clé de service et URL Postgres lecture seule absentes du `.env` de cette machine (règle CLAUDE.md : « .env et MCP Supabase : une fois par machine »).
- Piste : remplir `SUPABASE_SECRET_KEY` (ou `SUPABASE_DB_URL_RO`) dans `.env`, relancer `python -I pipelines/aujourdhui.py basketvibe`, coller la sortie ici. Colonnes de `bv_finance_health`, `bv_finance_projection`, `bv_position_summary`, `bv_next_opponents`, `bv_market_*` non vérifiées en base : ces vues sont lues par `select *` et rendues en `clé=valeur` (8 colonnes max) ; `bv_roster_now` est lue avec des colonnes supposées (`name, position, age, form, fatigue, injury_return_on`) à confirmer au premier vrai passage.
- Limite assumée : le script lit les chiffres mais ne tranche pas « acheter / vendre / garder » (étape 6 du skill) : c'est une décision, pas du SQL.
- Case L2 **non cochée**.

### 5. Reprise après ajout de `SUPABASE_DB_URL_RO` (2026-11-06, 09:51)
- `pip install -r requirements.txt` (module `psycopg` absent de ce PC, règle N1) puis `python -I pipelines/sql.py "select 1 as ok"` → `FATAL: password authentication failed for user "postgres"` (deux adresses du pooler, `aws-1-eu-west-2.pooler.supabase.com:5432`).
- Cause : l'utilisateur de l'URL est `postgres.smkariminvfityondmmc` (le compte administrateur), pas `assistant_ro.smkariminvfityondmmc` ; le mot de passe saisi n'est pas celui de ce compte. Le rôle `assistant_ro` est créé par `sql/silver/ops_001_role_assistant_ro.sql`, mot de passe posé à part.
- `python -I pipelines/aujourdhui.py basketvibe` : 13 requêtes en 0,4 s, toutes en échec → ce n'est pas une mesure. Preuves a et b restent **non mesurables**, L2 **non cochée**.

### 6. Reprise après ajout de `SUPABASE_SECRET_KEY` (2026-11-06, 10:02)
- `python -I pipelines/sql.py "select 1 as ok"` échoue encore (le transport `pg` passe avant `https` tant que le port 5432 répond, et l'URL `postgres.…` est refusée). `SQL_TRANSPORT=https python -I pipelines/sql.py "select 1 as ok"` → `ok = 1`. La clé fonctionne ; le `.env` garde une `SUPABASE_DB_URL_RO` fausse qui masque le transport https.
- **a** `SQL_TRANSPORT=https python -I pipelines/aujourdhui.py basketvibe` : **14,4 s** (< 60 s), 13 requêtes, sortie complète : 8 lignes Export (aperçu de ligue du 07/11 URGENT, 5 exports « à refaire », historique des transferts depuis 2026-11-04), 1 ligne Composition (preset amical 23:45), faits de position/adversaires, 1 ligne Transferts (marché > 24 h), faits Finances et Personnel. Durée consignée dans `journal-aujourdhui.md`. ✅
- **b** rejeu `--jour 2026-11-03`, `2026-11-04`, `2026-11-05` : toutes les vues sauf l'historique des ventes lisent `current_date` / `now()` → « rejeu non disponible » sur 12 vues sur 13. Les briefs de `outputs/basketvibe/briefs/` sont des sorties d'agents (tactique, transferts…), pas des plans du soir : aucune comparaison ligne à ligne possible, colonne « écart » = **non mesurable**. ❌
- **c** `python pipelines/test_aujourdhui.py` : 15/15 ✅
- Constat à corriger (hors lot) : `gold.bv_next_opponents` renvoie un match déjà joué (round 2, 2026-11-04) ; `aujourdhui.py` le recopie tel quel.
- Cause du blocage de b : les vues gold ne sont pas paramétrées par date. Piste : vues `…_at(date)` ou instantanés journaliers (`ops`), à décider dans un lot dédié.
- Case L2 **non cochée** (critère b non tenu).

### 7. L2b (2026-11-06)
- **Preuve b** : remplacée le 2026-11-06 par le mode ombre (3 soirs) et l'instantané quotidien ; décision de l'utilisateur. L'option `--jour` reste dans le code ; « rejeu non disponible » n'est plus une case à cocher.
- `.env` / variable d'environnement SUPABASE_DB_URL_RO : à supprimer ou à remplacer par l'URL de assistant_ro (action de l'utilisateur).
- Adversaires : `gold.bv_next_opponents` expose `match_day` (`sql/gold/004_bv_tactics.sql:147`) ; `aujourdhui.py` écarte les lignes dont `match_day` < aujourd'hui (commit 1675715). `PYTHONIOENCODING=utf-8 python -I pipelines/test_aujourdhui.py | tail -1` → `16/16` (cas « match passé non rendu »).
- `sql.py` : si Postgres répond mais refuse l'authentification (y compris le coupe-circuit `ECIRCUITBREAKER too many authentication failures`, vu ici), la lecture bascule en https et Postgres n'est plus réessayé dans le processus (commits 4de1742, 06594ef). `PYTHONIOENCODING=utf-8 python -I pipelines/test_sql.py | tail -1` → `15/15` (12 existants + 3 nouveaux). Constat : la 1re exécution réelle sans cette bascule laissait 3 vues illisibles ; avec elle, `Vues illisibles` absent.
- `aujourdhui.py` écrit `outputs/basketvibe/aujourdhui-AAAA-MM-JJ.md` (écrasé le même jour, hors `--jour`) : `PYTHONIOENCODING=utf-8 python -I pipelines/aujourdhui.py basketvibe` → code 0, **13,0 s**, fichier `outputs/basketvibe/soir-2026-11-06.md` créé (4 248 octets), 0 « Vues illisibles », `bv_next_opponents` : seulement `match_day=2026-11-07` et `2026-11-09` (le match du 04/11 n'est plus rendu).

## L3a — règles de décision BasketVibe (2026-11-06) : rédigé, pas codé
Fichier : `docs/attentes/regles-decision-basketvibe.yaml` (commit 070759d). Charte en tête (source « utilisateur, 2026-11-06 »), 4 secteurs (18 règles, chacune avec option « garder » en concurrence), `revue_hebdo` (échelle de 6 paliers, exception « grave » = série de 2 défaites de ligue d'après `sql/core/011_objective_rule.sql`), `tactique_amical`.

### Mesures (`python -I pipelines/sql.py "<requête>"`, 2026-11-06)
- `core.club_strategy` : `select * from core.club_strategy` → **0 ligne** (aucune ligne BasketVibe ; colonnes existantes utilisées seulement, aucune migration).
- `select * from gold.bv_finance_health` → as_of 2026-11-05, balance **1 167 106**, weekly_salaries 292 795, weekly_fixed_costs **452 795**, recurring_income_week 561 642, weekly_result_est **108 847**, salaries_pct_of_income **52,1**.
- `select * from gold.bv_finance_s2_projection` → safety_reserve **905 590**, investable_now_end_s1 **570 288**, balance_end_s1 1 425 878.
- `select * from gold.bv_finance_projection` → balance_end_projected 1 425 878, home_left 11, season_end 2026-12-21.
- `select count(*) filter (where is_resale) …, percentile_cont(…) from gold.bv_transfer_history` → 69 reventes (2026-09-02 → 2026-11-04), 48 gagnantes, médiane **44 000**, p10 **−39 650**, pire **−256 800**. (Les ventes faites par moi : 0 revente, donc ces chiffres sont ceux du marché.)
- `select * from gold.bv_position_summary` → depth 3/4/3/3/3 (PG/SG/SF/PF/C), ps_avg 49,4 / **46,4** / 47,1 / 53,3 / 49,4 ; poste le plus faible : **SG** ; joueur le plus faible : Sacha Leclerc (ps 41,9).
- `select … from core.game_params where game='basketvibe' and key like '%age%'` → age_declin **31** ; `gold.bv_roster_now` : âge maximal 30 (Min-jun Dang), un joueur de 29 ans (Léo Lefebvre).
- `select competition, my_result, count(*) from gold.bv_match_report group by 1,2` → ligue 11 V / 13 D, coupe 2 V / 0 D, amicaux 11 V / 14 D.
- Seuil de gros montant : `grep -rn "gros montant"` ne trouve aucune valeur (SEUIL_GROS_MONTANT vide) → proposé 450 000 (une semaine de charges fixes), **a_valider**.
- Perte de transferts tolérée sur 4 semaines : 1 167 106 − 905 590 = **261 516** (mesuré, formule à valider).
- Part des salaires : 52,1 % mesuré ; plafond **non mesurable** (aucun plafond sourcé).
- Palier 5 de la revue : « défaite probable / inattendue » écrit `a_valider`, confiance faible, non testé sur l'historique.

### Preuves
- `python -c "import yaml; yaml.safe_load(open('docs/attentes/regles-decision-basketvibe.yaml'))"` → `YAML valide ['charte', 'seuils_mesures', 'secteurs', 'revue_hebdo', 'tactique_amical']` ; 18 règles, 0 sans source ni statut (statuts : sourcé, a_valider).
- `git diff --stat 5db6880..HEAD -- '*.py' '*.sql' CLAUDE.md .claude` → aucune sortie (0 ligne). `git diff --stat 5db6880..HEAD` avant ce journal : `docs/attentes/regles-decision-basketvibe.yaml | 272 +++` ; `1 file changed, 272 insertions(+)`.

### Corrections de l'utilisateur (2026-11-06, après le tableau de validation ; commit 01c97e8)
- Seuils (gros montant, perte de transferts) : valeurs de départ révisées par Claude avec l'étude ; le déclencheur est « finances mauvaises » ou « joueur trop cher pour son utilité ». Tout seuil et nombre minimal est ajustable (charte.seuils_ajustables).
- Jeunes : surtout en amical ; quelques minutes en ligue quand la victoire est sûre (homegrown 200 par minute de ligue des juniors, plafond 40 000 par semaine, fiche finances, [M§10.1.3]).
- Revue : palier 5 à tester sur l'historique, Claude peut demander effectif adverse et derniers matchs ; palier 6 défini par Claude ; défaite grave = adversaire moins fort qui nous bat, ou match qu'on était sûr de gagner, ou série de 2 défaites de ligue.
- Amical : aucune prédiction, aucun aperçu ; saisie complète (minutes, consignes, réglage des adversaires) ; minimum de 3 matchs par test, ajustable.
- `python -c "import yaml; …"` → `YAML valide`, 18 règles, 0 sans source ni statut.

## L3c — test du palier 5 (« adversaire plus fort ») sur l'historique de ligue (2026-11-06)
**Étape 0 : critères écrits AVANT tout calcul de prédiction.**
- **Données** : matchs de ligue de `gold.bv_match_report` (`competition = 'league'`, 13 défaites et 11 victoires au 2026-11-06, résultat = `my_result`). Pour chaque match : force de l'adversaire et la nôtre dans `silver.bv_standings_weekly`, au dernier relevé (`day`) **strictement antérieur** à `match_day`, en points par match = `points_for / (wins + losses)` ; adversaire joint par le nom (`team` = `opponent`), nous par `is_mine`. Aucun relevé postérieur au match. `club_strength` est lu aussi, mais seule la mesure en points par match décide.
- **Méthode** : prédiction « on gagne » si nos points par match dépassent ceux de l'adversaire d'au moins **E = 0,3 point par match** ; « on perd » si l'adversaire nous dépasse d'au moins E ; « équivalent » sinon. E est fixé ici et ne sera pas réglé après coup. Les « équivalent » sont comptés mais exclus de la part de prédictions justes. Un match sans relevé antérieur pour l'adversaire ou pour nous est compté à part (« sans classement antérieur »).
- **Base naïve** : prédire toujours « victoire » ; taux = victoires de ligue observées / matchs de ligue de la même population.
- **Critère de réussite** : sur au moins **20 matchs** avec un classement antérieur disponible, la part de prédictions justes (hors équivalent) dépasse la base naïve d'**au moins 10 points**.
- **Repli** : critère non tenu → statut « non utilisable » ; G1 et G2 désactivées dans le YAML (« désactivée le <date> : test L3c ») ; la revue hebdomadaire garde les paliers 1 à 4 et 6. Moins de 20 matchs avec classement antérieur → « non mesurable » avec le nombre exact (G1 et G2 restent désactivées tant que le palier 5 n'est pas validé).

**Étapes 1 et 2 : script et résultat (2026-11-06).** `pipelines/palier5_test.py` et `pipelines/test_palier5.py` (commit 12e5a77 ; la correction d'un arrondi à E pile était dans le même commit, avant tout résultat réel).
- `PYTHONIOENCODING=utf-8 python -I pipelines/test_palier5.py` → `11/11`.
- `PYTHONIOENCODING=utf-8 python -I pipelines/palier5_test.py` :
```
matchs de ligue lus : 24 ; relevés de classement lus : 67
| date | adversaire | nos points/match | les siens | prédiction | résultat réel | |
| 2026-10-19 | BARIUM | 95.4 | 100.9 | défaite | victoire | faux |
| 2026-10-21 | Žirmūnai | 95.4 | 106.3 | défaite | victoire | faux |
| 2026-10-24 | Astur Hoops | 95.4 | 106.1 | défaite | défaite | juste |
| 2026-10-26 | Wolves Empire | 97.1 | 93.7 | victoire | victoire | juste |
n (avec classement antérieur) = 4 ; sans classement antérieur = 20 ; justes = 2, faux = 2, équivalents = 0
part de prédictions justes (hors équivalent) = 50.0 % ; base naïve (toujours victoire) = 75.0 % ; E = 0.3
verdict : non mesurable : 4 match(s) avec classement antérieur, il en faut 20
```
- Cause des 20 matchs sans classement antérieur : `select day, season_id, count(*), sum(wins+losses) from silver.bv_standings_weekly group by 1,2` → 5 relevés seulement : 2026-10-18 (12 équipes, 216 matchs), 2026-10-25 (252), 2026-10-26 (418), 2026-11-01 (saison 2, **0 match joué**), 2026-11-05 (24). Les 24 matchs de ligue vont du 2026-09-07 au 2026-11-04 : ceux d'avant le 2026-10-18 n'ont aucun relevé antérieur ; ceux de la saison 2 n'ont qu'un relevé à 0 match (points par match indéfinis).
- **Verdict : non mesurable (4 matchs sur les 20 requis).** Sur ces 4 matchs : 50,0 % justes contre 75,0 % de base naïve, soit le palier 5 en dessous de la base ; n trop petit pour conclure, aucune décision sur la qualité du palier 5.
- Piste : le test redevient mesurable quand `silver.bv_standings_weekly` aura au moins 20 matchs précédés d'un relevé à matchs joués (relevé du classement après chaque match) ; rejouable tel quel avec `python -I pipelines/palier5_test.py`.

### L3c bis — second test du palier 5, force calculée sur les scores des matchs (2026-11-06, accord de l'utilisateur)
**Critères écrits AVANT tout calcul de prédiction.** Constat de structure fait avant (aucune prédiction calculée) : `silver.bv_fixtures` contient, pour la saison 1 (id `8fa19101…`), 264 matchs terminés du 2026-09-07 au 2026-10-26, 24 équipes, 12 matchs par journée de match (deux ligues de 12, 22 rondes chacune) ; la saison 2 (id `86a63498…`) n'a qu'un seul match terminé en base le 2026-11-06 (le nôtre du 11-02) ; 22 de nos 24 matchs de ligue de `gold.bv_match_report` sont de la saison 1, 2 de la saison 2.
- **Données** : nos matchs de ligue de `gold.bv_match_report` (`competition = 'league'`, résultat = `my_result`), reliés à `silver.bv_fixtures` par `fixture_id`. Force d'une équipe avant le match = points marqués par match sur ses matchs **terminés de la même saison dont `match_day` est strictement antérieur** à celui du match (points marqués = `home_score` ou `away_score` selon son côté). Aucun score du match lui-même ni postérieur.
- **Méthode** : identique au premier test : « on gagne » si nos points par match dépassent ceux de l'adversaire d'au moins **E = 0,3**, « on perd » si l'inverse, « équivalent » sinon (compté, exclu de la part de justes). Base naïve : toujours « victoire », taux observé sur les mêmes matchs.
- **Nombre minimal de matchs antérieurs par équipe : 3** (en dessous, la moyenne de points repose sur trop peu de matchs) ; un match dont l'une des deux équipes en a moins de 3 est compté « sans force antérieure ». Conséquence connue avant le calcul : les rondes 1 à 3 et toute la saison 2 sont exclues, donc **19 matchs au plus** (rondes 4 à 22 de la saison 1).
- **Critère de réussite — écart voulu par rapport au premier test** : le seuil de 20 matchs du premier test est inatteignable avec 19 matchs au plus. Je fixe donc ici, avant le calcul : **au moins 15 matchs mesurables** (au lieu de 20) **et** part de prédictions justes (hors équivalent) au moins **10 points au-dessus** de la base naïve. Sous 15 matchs mesurables : « non mesurable ».
- **Portée du verdict** : avec 15 à 19 matchs, l'écart de 10 points est dans le bruit statistique ; un succès se lit « utilisable avec confiance faible », jamais « certain ».
- **Repli** : critère non tenu → « non utilisable » ; les définitions de défaite grave « adversaire moins fort qui nous bat » et « match sûr qui est perdu » restent désactivées. Critère tenu → elles sont réactivées avec la mention « confiance faible, test L3c bis du 2026-11-06 », et le palier 5 est réactivé dans la revue hebdomadaire.

**Résultat du second test (2026-11-06)** — code `pipelines/palier5_test.py --scores` (commit 07cbef1) ; `PYTHONIOENCODING=utf-8 python -I pipelines/test_palier5.py | tail -1` → `15/15`.
- `PYTHONIOENCODING=utf-8 python -I pipelines/palier5_test.py --scores` :
```
matchs de ligue lus : 24 ; matchs terminés lus : 265 ; minimum de matchs antérieurs par équipe : 3
| date | adversaire | nos points/match | les siens | prédiction | résultat réel | |
| 2026-09-14 | Thrylos B.C. | 79.3 | 86.3 | défaite | victoire | faux |
| 2026-09-16 | Póvoa Riptide | 83.8 | 104.5 | défaite | défaite | juste |
| 2026-09-19 | San pancrazio salentino Cazzi | 81.8 | 78.0 | victoire | victoire | juste |
| 2026-09-21 | Sierra Nevada | 86.8 | 84.0 | victoire | victoire | juste |
| 2026-09-23 | BARIUM | 89.1 | 104.3 | défaite | défaite | juste |
| 2026-09-26 | Žirmūnai | 89.4 | 105.6 | défaite | défaite | juste |
| 2026-09-28 | Astur Hoops | 90.1 | 103.6 | défaite | victoire | faux |
| 2026-09-30 | Wolves Empire | 92.5 | 95.2 | défaite | défaite | juste |
| 2026-10-03 | KK Uola | 93.9 | 116.5 | défaite | défaite | juste |
| 2026-10-05 | Mind Readers | 92.4 | 100.8 | défaite | défaite | juste |
| 2026-10-07 | Águias do Guadiana | 92.1 | 94.6 | défaite | défaite | juste |
| 2026-10-10 | Thrylos B.C. | 91.9 | 86.1 | victoire | victoire | juste |
| 2026-10-12 | Póvoa Riptide | 93.4 | 104.9 | défaite | défaite | juste |
| 2026-10-14 | San pancrazio salentino Cazzi | 94.2 | 81.7 | victoire | victoire | juste |
| 2026-10-17 | Sierra Nevada | 94.6 | 90.9 | victoire | victoire | juste |
| 2026-10-19 | BARIUM | 95.4 | 100.9 | défaite | victoire | faux |
| 2026-10-21 | Žirmūnai | 96.3 | 106.4 | défaite | victoire | faux |
| 2026-10-24 | Astur Hoops | 97.6 | 105.3 | défaite | défaite | juste |
| 2026-10-26 | Wolves Empire | 97.1 | 93.7 | victoire | victoire | juste |
n (avec classement antérieur) = 19 ; sans classement antérieur = 5 ; justes = 15, faux = 4, équivalents = 0
part de prédictions justes (hors équivalent) = 78.9 % ; base naïve (toujours victoire) = 52.6 % ; E = 0.3
verdict : utilisable avec confiance faible
```
- **Verdict : utilisable avec confiance faible** (19 matchs ≥ 15, 78,9 % contre 52,6 % de base naïve, soit +26,3 points ≥ 10). Les 5 matchs sans force antérieure sont les rondes 1 à 3 (3 matchs) et les 2 matchs de la saison 2, comme prévu avant le calcul.
- Lecture du tableau : 6 prédictions « victoire », 6 victoires ; 13 prédictions « défaite », 9 défaites et 4 victoires. Aucun cas dans l'historique où l'on prédisait la victoire et où l'on a perdu : les deux définitions de défaite grave fondées sur ce palier n'ont donc jamais été déclenchées sur ces 19 matchs, on ne sait pas encore ce qu'elles donneraient à l'usage.
- Réserves : 19 matchs, une seule saison, force calculée sur 3 matchs ou plus (bruit élevé au début), seuil de 15 matchs abaissé par rapport au premier test (écrit avant le calcul, voir ci-dessus). Premier test (classement hebdomadaire) : toujours « non mesurable », 4 matchs sur 20.

- `sql.py` : repli HTTPS, réponse sql_ro encodée deux fois (chaîne au lieu de liste) → `lignes_de()` la décode (`str has no attribute keys`, ancien `sql.py:84`). Cause non vue en direct (session cloud) : reproduite par simulation. `test_sql.py` 17/17 (15 + 2).

## Plan du jour, étape 5i, transferts (2026-11-09) — critères écrits avant le code

Périmètre : BasketVibe, lecture seule sur la base, aucune migration. Seuls `aujourdhui.py`, `aujourdhui_sources.py`, `test_aujourdhui.py` et ce journal bougent. Le plan propose ; jamais d'achat, de vente ni d'enchère sans accord écrit de l'utilisateur.

Contexte : le plan dit « Acheter un SF de note ≥ 61,0 » sans nom ni prix, et « pas d'enchère nouvelle, l'export du Marché a plus de 24 h » : il cache tout quand la page a plus de 24 h (`pipelines/aujourdhui.py:917-931`). Plafond actuel des affaires : `gold.bv_market_bargains.bid_ceiling_resale` (95 % du p25 de référence = prix de revente sans perte). Playbook, section « Marché ».

- **X1 Constat** : date de la dernière page Marché en bronze ; sortie de `gold.bv_market_bargains` et `gold.bv_market_candidates` sur cette page telle quelle (10 lignes au plus) ; compte des annonces dont la fin est passée et de celles encore ouvertes. Sortie collée.
- **X2 Marché ancien** : au lieu de tout cacher au-delà de 24 h, le plan affiche, pour chaque annonce encore ouverte qui remplit les conditions d'une affaire (référence fiable, marge de revente positive, tient dans la capacité), jusqu'à 3 lignes : nom, poste, PS, prix à l'export, plafond (`bid_ceiling_resale`), fin de l'enchère, et « page du Marché de N h : le prix a pu monter ». Les annonces dont la fin est passée disparaissent. Aucun seuil écrit à la main.
- **X3 Joueur de besoin** : la ligne « Acheter un SF de note ≥ X » nomme jusqu'à 3 annonces de `gold.bv_market_candidates` au poste qui satisfont la note, avec : nom, PS, prix à l'export, fin, et plafond = p75 du prix de référence de `gold.bv_price_ref_ps`, borné par la capacité du plan (solde moins les enchères ouvertes), marqué « plafond de besoin, à valider ». Sans annonce : « aucune annonce au poste SF dans le Marché du JJ/MM ».
  - **Écart connu avant le code** : `gold.bv_price_ref_ps` n'a que deux axes, tranche de PS (pas de 5) et tranche d'âge (≤21, 22-25, 26-29, 30+) ; elle n'a **pas de colonne poste**. Le p75 sera donc celui de la tranche de PS et d'âge de l'annonce, pas du poste. Écrit dans la ligne (« p75 PS/âge ») ; aucun poste inventé.
- **X4 Moment de miser** : chercher dans les pages brutes et dans `gold.bv_transfer_history` si l'historique des mises (instants et montants) existe ; réponse oui ou non avec la requête collée. Si non, chaque ligne d'enchère dit « fenêtre de mise non mesurée : mise près de la fin ; ne dépasse pas le plafond » et n'invente aucune durée.
- **X5 Bilan des conseils d'achat** : nombre de `learn.decision` (domaine `achat`) suivies, rejetées ou sans suite ; tableau collé, lecture seule. Correspondance posée avant la lecture : `done` = suivie, `rejected` = rejetée, `proposed` = sans suite ; `accepted` et `expired` comptés à part s'ils existent.
- **X6 Tests figés** : un cas présent et un cas absent pour X2 et pour X3 ; sortie à 8 lignes au plus (les lignes d'enchère passent en tête quand leur fin est proche) ; durée au plus 15 s ; les 197 tests du plan et les 38 de la revue restent verts.
- **X7 Rejeu** : `python -I pipelines/aujourdhui.py basketvibe` avant et après, sortie collée telle quelle.
- **X8 Deux plafonds distincts** : « plafond de revente » pour une affaire, « plafond de besoin » pour un joueur à jouer ; jamais le même mot pour les deux.

Étapes : 1 critères (ce commit) ; 2a X1, X4, X5 (journal) ; 2b X2, X3, X6, X8 (code et tests) ; 3 `python -I pipelines/fusion_main.py` puis `python -I pipelines/fin_etape.py`, sorties, rejeu avant/après et résultats collés ici.

### Étape 2a — X1, X4, X5 (lecture seule, 2026-11-09 17:28 Paris)

**X1 Constat.**
- Dernière page Marché en bronze (`api/v1/transfer-auctions?page=1&page_size=20`, id 38396) : **2026-11-08 10:10:05 UTC = 11:10 Paris**, soit environ 30 h avant la lecture. Une seule page de 20 annonces a été exportée sur `total` = 145 (capture du 08/11 : page 1 seulement) : l'export couvre 20 annonces sur 145.
- `select count(*) filter (where ends_paris > now() at time zone 'Europe/Paris') ouvertes, count(*) filter (where ends_paris <= …) finies, count(*) total from gold.bv_market_bargains` → **0 ouvertes, 20 finies, 20** (fins du 08/11 13:16 au 08/11 21:10). Même résultat pour `gold.bv_market_candidates` : **0 ouvertes, 20 finies, 20 (10 avec `enters_top8`)**. `silver.bv_transfer_auctions` : 1 234 lignes, 0 avec `ends_at` futur.
- `gold.bv_market_bargains` (5 premières lignes par marge p25, page telle quelle) :
```
| name | position | ps | price_now | bid_ceiling_resale | resale_margin_p25 | ref_n | ref_reliable | ends_paris |
| Hyun-soo Zhang | PG | 55.1 | 190000 | 731500 | 541500 | 60 | True | 2026-11-08T19:55:44 |
| Arjun Tan | PF | 59.9 | 360000 | 731500 | 371500 | 60 | True | 2026-11-08T19:56:38 |
| Bogusław Grabiec | C | 55.3 | 450000 | 731500 | 281500 | 60 | True | 2026-11-08T19:12:17 |
| Dev Tanaka | SF | 58.3 | 520000 | 731500 | 211500 | 60 | True | 2026-11-08T19:56:24 |
| Gabriele Greco | PG | 46.8 | 251 | 950 | 699 | 33 | True | 2026-11-08T15:06:48 |
```
- `gold.bv_market_candidates` (5 premières par gain) : Dev Tanaka SF 58,3 à 520 000 (`would_rank_in_slot` 2) ; Bogusław Grabiec C 55,3 à 450 000 ; Cyprian Cieślak PG 58,5 à 2 650 000 ; Arjun Tan PF 59,9 à 360 000 ; Mohit Saxena SG 59,5 à 787 777 — toutes finies le 08/11 entre 19:12 et 19:56.
- **Lecture** : toutes les annonces de la page sont finies. Avec la règle « ne montrer que les annonces ouvertes », X2 et X3 afficheront **zéro ligne de nom** sur cette page aujourd'hui ; la version codée ne se vérifie que sur des cas figés. Aucun SF au PS demandé n'est ouvert : le message « aucune annonce au poste SF dans le Marché du 08/11 » sera le rendu réel.

**X4 Moment de miser : NON.** L'historique des mises (instants et montants) n'existe ni en bronze ni en gold.
- `select source_url, count(*) n, max(captured_at) from bronze.raw_pages where game='basketvibe' and payload::text ~* '(bid_history|bidHistory|"bids"|bid_events|bidder|bid_at|placed_at|bid_amount|last_bid|highest_bid|bid_time)' group by 1` → 4 URL, toutes `api/v1/players/<id>/transfer-auction` (7 pages, 16/10 au 30/10). Elles portent seulement l'**état courant** : `bid_count`, `display_price`, `my_max_bid`, `min_max_bid`, `heat_level`, `leading_bidder_team_*`, `is_viewer_leading`, `ends_at`, `blind_ends_at`. Aucune liste de mises ni aucun horodatage de mise (page 25618 lue en entier).
- Page `transfer-auctions` (id 38396) : mêmes champs d'état (`has_bids`, `bid_count`, `heat_level`, `display_price`, `ends_at`, `scheduled_end_at`, `blind_ends_at`), pas de mises.
- `gold.bv_transfer_history` : colonnes `sold_on, fee, starting_price, from_team, to_team, …` — un prix final par vente, pas de mise intermédiaire ; `silver.bv_transfers` : `settled_at, fee`.
- Conséquence : chaque ligne d'enchère dit « fenêtre de mise non mesurée : mise près de la fin ; ne dépasse pas le plafond ».

**X5 Bilan des conseils d'achat** (`select status, count(*) from learn.decision where game='basketvibe' and domain='achat' group by 1`) :
```
| statut | correspondance | n |
| done | suivies | 7 |
| rejected | rejetées | 3 (2 avec note de l'utilisateur, 1 sans) |
| proposed | sans suite | 18 (du 20/10 au 02/11) |
| accepted, expired | — | 0 |
```
- 28 décisions d'achat : 7 suivies (25 %), 3 rejetées (11 %), 18 sans suite (64 %). Aucune n'a de leçon (`lesson_id` nul) : l'effet des 7 suivies n'est pas mesuré en base. Les 3 rejetées : Waleed Al-Anazi, Salvador Aquino (190 000), Fujita C / Stan… (07-08/11).

### Étape 2b — X2, X3, X6, X8 (commit 1278104, `aujourdhui.py` et `test_aujourdhui.py` seulement)

- **Requêtes** : `gold.bv_market_bargains` et `gold.bv_market_candidates` ne lisent plus que les annonces ouvertes (`ends_paris` nul ou futur) ; les candidats sont reliés à `gold.bv_price_ref_ps` (tranche de PS × tranche d'âge) pour le p75. Le garde « Marché de moins de 24 h » est supprimé : la ligne dit l'âge de la page.
- **X2** : jusqu'à 3 lignes « Enchère maximale M sur NOM (POSTE, PS x) » + détail « plafond de revente (95 % du p25) ; prix à l'export … ; fin JJ/MM HH:MM ; marge de revente p25 … ; page du Marché de N h : le prix a pu monter ; fenêtre de mise non mesurée… ». Conditions inchangées (référence fiable, `ref_n` ≥ 5, marge p25 > 0, capacité), aucune nouvelle valeur seuil.
- **X3** : « Acheter un PG de note ≥ X : NOM (PS) : prix à l'export, fin, plafond de besoin M, à valider ; … » (3 au plus) ; plafond = min(p75 PS/âge, capacité) ; une annonce déjà au-dessus de son plafond est écartée ; sans annonce : « aucune annonce au poste SF dans le Marché du JJ/MM (annonces encore ouvertes de l'export) ». Correction au passage : l'ancien code cherchait les noms au poste le plus faible alors que la ligne nommait le poste mince ; les noms viennent maintenant du poste de la cible.
- **Écart au critère X3** (annoncé avant le code) : le p75 est celui de la tranche de PS et d'âge, `gold.bv_price_ref_ps` n'ayant pas de colonne poste.
- **X6** : 11 cas ajoutés (X2 présent ×2 et absent ×2, X3 présent ×2 et absent ×2, X4, X8, X6) ; le cas « Marché périmé = pas d'enchère » (TRF-4) est remplacé : il affirmait l'ancienne règle de masquage à 24 h. Une enchère qui finit aujourd'hui passe en priorité 1 (horizon = aujourd'hui) : avec 7 autres actions, Martin et Dupuis restent et la sortie tient en 8 lignes.
- Résultat : `python -I pipelines/test_aujourdhui.py` → **208/208** (197 + 11 ; TRF-4 réécrit en place, même nombre) ; `python -I pipelines/test_revue_hebdo.py` → **38/38**.

### Étape 3 — rejeu, fusion et fin d'étape (2026-11-09 17:4x Paris)

**X7 — `python -I pipelines/aujourdhui.py basketvibe`, avant (commit 018a921), 10,0 s :**
```
19:30 — Avant 19:45 si possible : exporter la page Preview du match J4 (effectif adverse à jour)
    (gold.bv_agenda)
19:45 — Ligue J4 contre Naked Spartans (lun. 09/11) : saisis la tactique maintenant — heure limite
    du verrou 19:45 ; le test est perdu si : Faux si à J4 le Q3 est < 0 et le Q2 < −5, ou si
    defense_tier n'est pas 0 pour tous (briefs/2026-11-08-tactique.md)
20:50 — Après le match (~20:50) : exporter la page du match J4 (puis analyse de l'agent Match)
    (gold.bv_agenda)
07:45 — Amical contre Opper Cards (mar. 10/11) : saisis le test E1 niveau A : agressivité 3 à
    l'écran (cran 2, équilibrée) sur tous les joueurs — heure limite du verrou 07:45 ; réglage du
    test à la place de celui du brief ; après le match exporte : aperçu, box scores par quart-temps,
    réglages utilisés, page Équipe du jour ; E1 : 0 vérifié sur 4
    (docs/attentes/experiences-amicales-basketvibe.yaml, core.fixture)
--:-- — Analyse : lance l'agent analyste ce soir — 2 défaites d'affilée en ligue ou coupe (dernière
    : Póvoa Riptide, 07/11, ligue) ; dernier brief analyste du 05/11 (core.fixture,
    gold.match_objective)
Autres points (4) : Acheter un SF de note ≥ 61,0 ; Vendre Catalin Ungureanu : économie 19 030 par
    semaine, remplaçant Maël Bernard au poste C, écart 0,7 ; Analyse : Dernier match exporté : 09/11
    (amical, L 104-120 contre Garden City) ; Académie, rapport du 05/11 : 3 prospects ; valeur d'un
    High inconnue
Garder : effectif, vendre : rien de vendable (aucun joueur de 31 ans ou plus, âge du déclin) ;
    effectif, vendre pour profit : règle non écrite — à valider (seuil de déclenchement non validé)
    ; effectif, jeunes : ni titre acquis ni rien à jouer sur les 7 prochains jours
    (gold.match_objective) ; finances : seuil non atteint (résultat hebdo estimé +96 640, la
    réduction de charges commence sous 0) ; transferts : pas d'enchère nouvelle, l'export du Marché
    a plus de 24 h ; Personnel (médecin 2/2, kinésithérapeute 4/4, psychologue 2/2, marketing 0/2,
    semaine du 2026-11-02) : règle de personnel non tranchée, à valider
Exports à faire aujourd'hui : Équipe (aperçu, joueurs) (30 h) ; Amical : tactique du match (30 h) ;
    Marché (enchères) (30 h)
```
**Après (commit 1278104), 11,3 s (≤ 15 s) :** identique sauf deux entrées.
```
Autres points (4) : Acheter un SF de note ≥ 61,0 : aucune annonce au poste SF dans le Marché du
    08/11 (annonces encore ouvertes de l'export) ; Vendre Catalin Ungureanu : … (inchangé)
Garder : … ; transferts : aucune affaire fiable ouverte dans le Marché du 08/11 qui tienne dans le
    solde moins les enchères encore ouvertes (capacité restante : 960 181) ; … (inchangé)
```
- Les lignes d'enchère ne s'affichent pas aujourd'hui : les 20 annonces de la page du 08/11 sont finies (X1). Le code X2/X3 n'est donc éprouvé que par les cas figés ; sur la base il rend les deux messages ci-dessus (nouveauté : le plan dit pourquoi, avec la date du Marché, au lieu de « plus de 24 h »).
- La page du Marché exportée ne couvre que 20 annonces sur 145 (X1) : « aucune annonce » vaut pour l'export, pas pour tout le marché ; un export des pages 2 à 7 serait nécessaire pour trouver un SF.

**`python -I pipelines/fusion_main.py`** (commits 29ad70a..1278104) : `Poussé : origin/main == HEAD.` (12781048f143).
**`python -I pipelines/fin_etape.py`** : `commits d'avance sur origin/main : 0`, `git status --short : (propre)`, tests : aujourdhui 208/208, aujourdhui_hockeynation 45/45, contexte_budget 9/9, controle 43/43, decision 15/15, etude_evenements 24/24, evaluer 34/34, fin_etape 5/5, forme 38/38, fusion_main 5/5, garde_heredoc 26/26, garde_push 6/6, heure_paris 7/7, match_engine_etat 36/36, migrer 19/19, migrer_kb 17/17, palier5 15/15, police 24/24, preanalyse_scores 25/25, relier_faits 8/8, revue_hebdo 38/38, sql 23/23, agents 0 échec ; `HEAD dans origin/main : oui`.

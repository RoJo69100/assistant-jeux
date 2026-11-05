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

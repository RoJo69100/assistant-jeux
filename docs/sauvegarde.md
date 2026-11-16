# Sauvegarde du bronze (plan Supabase Free : aucune sauvegarde automatique)

Principe : un workflow GitHub Actions hebdomadaire (`docs/sauvegarde-workflow.yml`) lit le bronze par la RPC `export_bronze` (clé publishable + jeton dédié, sans clé de service) et pousse des fichiers `.ndjson.gz` dans un dépôt PRIVÉ. Aucun poste n'est nécessaire.

**3 gestes**
1. **Créer le dépôt privé** `assistant-jeux-sauvegardes` (même compte, vide) et un jeton GitHub fin (Settings > Developer settings > Fine-grained tokens) limité à ce seul dépôt, droit « Contents : Read and write ».
2. **Créer le jeton d'export** : éditeur SQL Supabase, coller cette requête, la lancer UNE fois, copier le jeton affiché (il ne sera plus jamais visible ; seul son SHA-256 est enregistré) :
   `with t as (select replace(gen_random_uuid()::text || gen_random_uuid()::text, '-', '') as jeton), ins as (insert into bronze.export_tokens (token_sha256, label) select encode(sha256(convert_to(jeton, 'UTF8')), 'hex'), 'github-actions' from t returning 1) select jeton from t, ins;`
3. **Coller les 4 secrets** dans le dépôt public (Settings > Secrets and variables > Actions) : `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY` (Settings > API du projet), `BRONZE_EXPORT_TOKEN` (le jeton du geste 2), `BACKUP_REPO_TOKEN` (le jeton GitHub du geste 1). Puis copier `docs/sauvegarde-workflow.yml` vers `.github/workflows/sauvegarde.yml` (GitHub > Add file). Premier passage : onglet Actions > « Sauvegarde du bronze » > Run workflow (environ 70 Mo comprimés, quelques minutes).

**Contrôle et échec** : chaque passage est incrémental (id > dernier id, `etat.json` du dépôt privé). Une ligne ✅/❌ par table compare le total sauvegardé au nombre de lignes d'id <= dernier id en base. Une ligne ❌ ou une table sans ✅ fait échouer le job (courriel GitHub) avant tout commit. GitHub désactive un workflow planifié d'un dépôt public sans activité pendant 60 jours : un commit le réactive.

**Révoquer** : `update bronze.export_tokens set revoked_at = now() where label = 'github-actions';` puis refaire le geste 2.

**Restauration** (testée le 16/11/2026 sur 500 lignes par table : nombres de lignes et hachage MD5 des 11 colonnes identiques ; pas de restauration complète tant que la base est près des 500 Mo) : table cible créée par `sql/bronze/001` et `003`, puis par lots d'environ 1 Mo (`zcat fichier.ndjson.gz | jq -s -c .` donne le tableau JSON) : `insert into bronze.raw_pages overriding system value select * from jsonb_populate_recordset(null::bronze.raw_pages, '<tableau>'::jsonb);` (`overriding system value` obligatoire : `id` est une colonne d'identité) ; à la fin `select setval(pg_get_serial_sequence('bronze.raw_pages', 'id'), (select max(id) from bronze.raw_pages));`. Idem pour `bronze.discord_messages`.

Ne jamais coller un de ces secrets dans un chat, un commit ou un fichier du dépôt. La clé publishable seule ne lit rien : `export_bronze` répond « jeton invalide » (HTTP 403) et les tables `bronze` ne sont pas exposées par l'API. Lancement à la main (session cloud ou poste) : `python -I pipelines/sauvegarde_bronze.py --dossier <dossier>`, mêmes noms de variables (`SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`, `BRONZE_EXPORT_TOKEN`).

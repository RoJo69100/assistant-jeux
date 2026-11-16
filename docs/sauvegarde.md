# Sauvegarde du bronze (plan Supabase Free : aucune sauvegarde automatique)

1. Poste de Rémy : WSL, `git clone https://github.com/RoJo69100/assistant-jeux` puis `cd assistant-jeux` ; Python 3.10+ et `pip install psycopg[binary]` (lecture directe optionnelle).
2. Créer `.env` à la racine (ignoré par Git, jamais commité) avec ces NOMS : `SUPABASE_URL` et `SUPABASE_SECRET_KEY` (transport HTTPS, obligatoire) ; `SUPABASE_DB_URL_RO` (Postgres direct, facultatif). Les valeurs sont dans le tableau de bord Supabase (Settings > API / Database).
3. Commande : `python -I pipelines/sauvegarde_bronze.py` (`--verifier-seulement` pour contrôler sans exporter).
4. Fichiers : `~/backups/assistant-jeux/` (hors du dépôt, qui est public), un `.ndjson.gz` par table et par passage + `etat.json` (dernier id et total cumulé). Les passages suivants sont incrémentaux (id > dernier id).
5. Contrôle : une ligne ✅/❌ par table compare le total sauvegardé au `count(id <= dernier id)` en base (le bronze est immuable). Premier passage du 16/11/2026 : `raw_pages` 53 Mo, `discord_messages` 16 Mo compressés.
6. Restauration (procédure non testée) : une ligne = un objet JSON de la table, colonnes identiques, `id` conservé. `zcat fichier.ndjson.gz` puis insertion dans une table `bronze.raw_pages` ou `bronze.discord_messages` vide, par lots (ex. `insert ... select * from jsonb_populate_recordset(null::bronze.raw_pages, :lot)`), puis recaler la séquence d'`id` sur `max(id)`.
7. `SUPABASE_SECRET_KEY` donne tous les droits sur le projet : ne jamais la coller dans un chat, un commit ou un fichier du dépôt. `sql_ro` refuse la clé publishable (HTTP 401, droit réservé à `service_role`).
8. Fréquence conseillée : hebdomadaire ; le rappel de début de session signale une sauvegarde de plus de 10 jours.

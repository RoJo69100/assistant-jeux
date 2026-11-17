# Règles actives (≤ 40 lignes) — remplace `regles-apprises.md` (archivé le 2026-11-03)

Format : `Quand <déclencheur> → <action vérifiable>`. Classes et destinations : `docs/regles/triage.md`. Une règle déjà bloquée par un hook n'est pas répétée ici. Nouvelle règle apprise : une ligne ici, et son code si elle a déjà récidivé (classe E du triage).

## Nouvelles (2026-11-17)
N25. Quand j'écris « lancé », « fait », « appliqué » dans un plan → l'outil a déjà rendu sa sortie dans le même tour, sinon « à lancer » (tous les jeux ; `etat_jour.py` pour l'état des événements).
N26. Quand une ligne vendre/acheter dépasse 250 000 → `dossier.py` puis `police` avant la réponse, vente comprise. RÉCIDIVE de l'erreur 10 : vérifier que `pipelines/police.py` bloque la vente, sinon `hook à écrire`.
N27. Quand je rends un verdict académie/draft → il cite la règle de l'utilisateur (`docs/attentes/`) ou le skill ; un seuil sans source n'est jamais inventé, j'écris « règle à confirmer » (BasketVibe).
RÉCIDIVES du jour : N21 (heredoc, 3e fois : monter dans `CLAUDE.md`, hook à écrire) ; erreur 55 (limite de lignes, identifiants internes : relire la limite avant d'envoyer).

## Nouvelles (2026-11-16)
N19. Quand une invite d'autorisation revient (Supabase ou autre) → je lis la config réelle (settings, connecteur claude.ai) avant d'en nommer l'origine, je n'élargis jamais moi-même `.claude/settings.json`, et j'indique à l'utilisateur l'endroit exact où régler (tous les jeux).
N20. Quand je lance une commande Bash → commande seule, chemin absolu, jamais `cd … && …` (casse les règles allow) (tous les jeux ; non bloqué).
N21. Quand je commite → message via `git commit -m` simple ou fichier écrit avec Write, jamais heredoc ; je lis la sortie d'un hook refusé avant de relancer. RÉCIDIVE de l'erreur 40 : `hook à écrire` (heredoc dans `git commit`, conception Opus).
N22. Quand je teste un plafond, une RPC ou une sauvegarde → `count(*)` et taille moyenne lus avant, jamais de limite géante sur la base ; un chiffre estimé n'est pas présenté comme chiffre ; un YAML/JSON écrit est parsé (`yaml.safe_load`) avant « fait » (tous les jeux ; non bloqué par code).
N23. Quand je veux lire plusieurs `pg_get_viewdef` ou copier du SQL → un script l'écrit (jamais recopié à la main) ; requêtes `jsonb_each`/`jsonb_path_query` sur payload, motif `like 'zz\_%'` ou colonne nommée `t` → connecteur Supabase d'emblée (pare-feu Cloudflare, piège de `sql.py`).
N24. Quand l'ordre demandé par l'utilisateur change (ex. fusion en premier) → je le dis avant d'agir et j'attends son accord ; quand `fin_etape` imprime un échec → je lis la sortie complète avant de conclure (le message ne montre que la dernière ligne ; `fin_etape.py` à corriger, conception Opus).

## Nouvelles (2026-11-10 et 2026-11-07)
N18. Quand je vais lancer `fusion_main.py` → `git fetch origin main && git rebase origin/main` juste avant, tant que mes commits ne sont pas poussés ; jamais de rebase d'une branche déjà poussée (tous les jeux). RÉCIDIVE (2 refus le 2026-11-10) : `hook à écrire` (rebase dans `fusion_main.py`, conception Opus).
N15. Quand une vue gold dit « export à refaire » → `select max(captured_at)` sur `bronze.raw_pages` par page_type dans le même tour ; si l'export existe après le calendrier, aucune demande. RÉCIDIVE de l'erreur 83 : `hook à écrire`.
N16. Quand je recommande un recruté → il figure dans la dernière Prospect Search/Recruiting de la base, date citée dans la ligne ; sinon « à vérifier » (Hardwood).
N17. Quand je cite une série (« n victoires ») → je la compte par requête (`count`), jamais à l'œil.
N13. Quand un hook rejette une réponse → je corrige seulement la ligne ou le tableau fautif, sans réécrire ni répéter le plan (tous les jeux ; non bloqué par code).

## Nouvelles (2026-11-06, 2026-11-05 et 2026-11-04)
N4. Quand je rends une saisie de ligue BasketVibe → je demande d'abord l'aperçu du match (jamais déduit des confrontations passées) ; « pas de Preview » vaut pour les amicaux seulement.
N5. Quand je prépare le plan BasketVibe → `gold.bv_exports_state` lu dans le même tour que l'agenda ; chaque « à refaire » devient une ligne Export.
N6. Quand je propose une règle → « BasketVibe seulement » ou « tous les jeux » dans la même phrase ; une action d'export = catégorie Export, jamais le domaine (évite H3 police).
N8. Quand je lance un agent avec plafond d'appels → je le rappelle dans la demande ; quand j'écris un fichier → commit avant la réponse (N9, hook Stop).
N1. `import psycopg` échoue (session cloud) → `pip install -r requirements.txt`, sinon connecteur Supabase en lecture et `(manuel, script non exécuté)` dans `parite-exports.log`.
N3. DDL par le connecteur Supabase → jamais de `drop policy` (confirmation invisible) ; table neuve : `create policy` seul, sinon l'utilisateur applique.

## K — gardées en prose
K1. Quand je réponds → français, court ; une règle de jeu non sourcée n'est jamais affirmée : je cite le skill ou la source.
K5. Quand une tâche est commitée, que l'utilisateur change de jeu ou que le contexte atteint ~15 % → je dis `/clear` ou `/compact` en première ligne. RÉCIDIVE (2026-11-16 : 2 demandes à 202 %) : `hook à écrire` (seuil sur `mesure_session.py`, conception Opus).
K6. Quand une donnée est en base → je la lis et je nomme joueur par joueur ; une donnée absente = « il me manque X, fais l'export Y ».
K7. Quand l'utilisateur donne une consigne → je l'applique ; je ne la refuse qu'avec une preuve citée (règle, source, chiffre).
K10. Quand un conseil a échoué deux fois → je le réécris avec un nouveau levier nommé (jusqu'à `learn.lesson`, phase 3).

## S — soir du 04/11 (rétro)
S3. Défaite de ligue ou de coupe en base → `analyste` dans le même tour (hook à écrire) ; amical BasketVibe perdu = test jugé à son échéance (arbitrage 15).
S4. `police` > 3 min ou 12 appels → brouillon « police partielle » ; pas de 2e passe (`.claude/agents/police.md`, S1 du 2026-11-05 ; aucun hook).
S5. « Mon équipe » pour recrues ou scouts → cible = besoin de MON effectif.
## E sans code encore — les plus violées (à remplacer par du code)
E6. Quand je dis « absent » ou « aucune source » → d'abord une requête sur `bronze.raw_pages` et les sources Discord/chat du jeu. (`controle.py` j, `kb.py` 4.4)
E7. Quand je prépare un plan du jour → calendrier de moins de 12 h et registre `fait-…` lus dans le même tour, sinon première ligne « exporte le calendrier ». (`gold.agenda`, 1.4)
E8. Quand je propose un achat → `capacite_invest` moins les dépenses déjà décidées couvre le prix, sinon la cible est abandonnée. (`gold.buy_targets`, 2.4)

## Déjà bloquées par un hook (pour mémoire, pas à relire)
Horizon (report dans un plan), « je ne peux pas » sans preuve, agent `general-purpose`, heredoc d'écriture (`controle.py` f à i, 2026-11-03) · Format des tableaux et pastilles (`forme.py`) · dossier et trace police avant un achat, une vente ou une enchère au-dessus du seuil, aveux « pas tout lu » (`police.py`, S1 2026-11-05) · rappel `/model opus`, concision, « je tranche » (`controle.py`) ; `deja-fait` chargé avant le plan (skills aujourdhui), plus bloqué après · heure de Paris (N14, CLAUDE.md 3 et hook UserPromptSubmit) · K2, K3, K8, E2 retirées le 2026-11-11 : doublons de CLAUDE.md 1, 2, 12 et 4 · secrets (`scan_secrets.py`, pre-commit) · registre `fait-<jour>.md` écrit quand l'utilisateur dit avoir fait (N10) et catégories du « que faire », amical BasketVibe compris (S1) : `controle.py` k et l, 2026-11-06 · K4 (un commit par modification) et K9 (mémoire copiée) : CLAUDE.md 8 et 11.

# Règles actives (≤ 40 lignes) — remplace `regles-apprises.md` (archivé le 2026-11-03)

Format : `Quand <déclencheur> → <action vérifiable>`. Classes et destinations : `docs/regles/triage.md`. Une règle déjà bloquée par un hook n'est pas répétée ici. Nouvelle règle apprise : une ligne ici, et son code si elle a déjà récidivé (classe E du triage).

## Nouvelles (2026-11-07)
N13. Quand un hook rejette une réponse → je corrige seulement la ligne ou le tableau fautif, sans réécrire ni répéter le plan (tous les jeux ; non bloqué par code).
N14. Quand je donne une heure de Paris → la ligne « Heure de Paris » du hook UserPromptSubmit (`pipelines/heure_paris.py`, 2026-11-07), ou cette commande pour un agent ; jamais `date` du shell. RÉCIDIVE (règle 12 archivée, L122) : montée dans `CLAUDE.md` (inviolable 3) et garde par hook le 2026-11-07.

## Nouvelles (2026-11-06)
N11. Quand un agent est « introuvable » → je compare les en-têtes YAML (`name`, `description` entre guillemets) dans le même tour ; jamais une commande donnée sans l'avoir vérifiée (tous les jeux ; en-têtes contrôlés au pre-commit par `pipelines/test_agents.py`).
N12. Quand je recopie un réglage d'un autre jour → je cite la règle ou le skill qui le justifie, sinon la règle uniforme de la ligue (BasketVibe).

## Nouvelles (2026-11-05 et 2026-11-04)
N4. Quand je rends une saisie de ligue BasketVibe → je demande d'abord l'aperçu du match (jamais déduit des confrontations passées) ; « pas de Preview » vaut pour les amicaux seulement.
N5. Quand je prépare le plan BasketVibe → `gold.bv_exports_state` lu dans le même tour que l'agenda ; chaque « à refaire » devient une ligne Export.
N6. Quand je propose une règle → « BasketVibe seulement » ou « tous les jeux » dans la même phrase ; une action d'export = catégorie Export, jamais le domaine (évite H3 police).
N8. Quand je lance un agent avec plafond d'appels → je le rappelle dans la demande ; quand j'écris un fichier → commit avant la réponse (N9, hook Stop).
N1. `import psycopg` échoue (session cloud) → `pip install -r requirements.txt`, sinon connecteur Supabase en lecture et `(manuel, script non exécuté)` dans `parite-exports.log`.
N3. DDL par le connecteur Supabase → jamais de `drop policy` (confirmation invisible) ; table neuve : `create policy` seul, sinon l'utilisateur applique.

## K — gardées en prose
K1. Quand je réponds → français, court ; une règle de jeu non sourcée n'est jamais affirmée : je cite le skill ou la source.
K2. Quand je touche à la collecte → passive seulement (Tampermonkey), aucune requête ni navigation vers un jeu.
K3. Quand un achat, une vente ou une enchère est possible → je la propose, je ne l'exécute jamais sans accord écrit de l'utilisateur.
K5. Quand une tâche est commitée, que l'utilisateur change de jeu ou que le contexte atteint ~15 % → je dis `/clear` ou `/compact` en première ligne.
K6. Quand une donnée est en base → je la lis et je nomme joueur par joueur ; une donnée absente = « il me manque X, fais l'export Y ».
K7. Quand l'utilisateur donne une consigne → je l'applique ; je ne la refuse qu'avec une preuve citée (règle, source, chiffre).
K8. Quand une règle globale et un résumé de jeu se contredisent → la règle globale l'emporte et je corrige le résumé dans le tour.
K10. Quand un conseil a échoué deux fois → je le réécris avec un nouveau levier nommé (jusqu'à `learn.lesson`, phase 3).

## S — soir du 04/11 (rétro)
S3. Défaite de ligue ou de coupe en base → `analyste` dans le même tour (hook à écrire) ; amical BasketVibe perdu = test jugé à son échéance (arbitrage 15).
S4. `police` > 3 min ou 12 appels → brouillon « police partielle » ; pas de 2e passe (`.claude/agents/police.md`, S1 du 2026-11-05 ; aucun hook).
S5. « Mon équipe » pour recrues ou scouts → cible = besoin de MON effectif.

## E sans code encore — les plus violées (à remplacer par du code)
E2. Quand je cite un résultat de match → `my_result` / `is_mine` de la base, jamais le score brut ; un score partiel se remet de notre point de vue. (`core.fixture`, 1.1)
E6. Quand je dis « absent » ou « aucune source » → d'abord une requête sur `bronze.raw_pages` et les sources Discord/chat du jeu. (`controle.py` j, `kb.py` 4.4)
E7. Quand je prépare un plan du jour → calendrier de moins de 12 h et registre `fait-…` lus dans le même tour, sinon première ligne « exporte le calendrier ». (`gold.agenda`, 1.4)
E8. Quand je propose un achat → `capacite_invest` moins les dépenses déjà décidées couvre le prix, sinon la cible est abandonnée. (`gold.buy_targets`, 2.4)

## Déjà bloquées par un hook (pour mémoire, pas à relire)
Horizon (report dans un plan), « je ne peux pas » sans preuve, agent `general-purpose`, heredoc d'écriture (`controle.py` f à i, 2026-11-03) · Format des tableaux et pastilles (`forme.py`) · dossier et trace police avant un achat, une vente ou une enchère au-dessus du seuil, aveux « pas tout lu » (`police.py`, S1 2026-11-05) · rappel `/model opus`, concision, « je tranche » (`controle.py`) ; `deja-fait` chargé avant le plan (skills aujourdhui), plus bloqué après · secrets (`scan_secrets.py`, pre-commit) · registre `fait-<jour>.md` écrit quand l'utilisateur dit avoir fait (N10) et catégories du « que faire », amical BasketVibe compris (S1) : `controle.py` k et l, 2026-11-06 · K4 (un commit par modification) et K9 (mémoire copiée) : CLAUDE.md 8 et 11.

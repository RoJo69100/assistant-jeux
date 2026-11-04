# Règles actives (≤ 40 lignes) — remplace `regles-apprises.md` (archivé le 2026-11-03)

Format : `Quand <déclencheur> → <action vérifiable>`. Classes et destinations : `docs/regles/triage.md`. Une règle déjà bloquée par un hook n'est pas répétée ici. Nouvelle règle apprise : une ligne ici, et son code si elle a déjà récidivé (classe E du triage).

## Nouvelles (2026-11-04)
N1. Quand `import psycopg` échoue (session cloud) → `pip install -r requirements.txt` d'abord ; si impossible, connecteur Supabase en lecture, et la ligne de `parite-exports.log` est marquée `(manuel, script non exécuté)`.

N3. Quand j'applique du DDL par le connecteur Supabase → jamais de `drop policy` (confirmation invisible pour l'utilisateur, délai de 60 s) ; sur une table neuve, `create policy` seul, sinon faire appliquer à l'utilisateur.

## K — gardées en prose
K1. Quand je réponds → français, court ; une règle de jeu non sourcée n'est jamais affirmée : je cite le skill ou la source.
K2. Quand je touche à la collecte → passive seulement (Tampermonkey), aucune requête ni navigation vers un jeu.
K3. Quand un achat, une vente ou une enchère est possible → je la propose, je ne l'exécute jamais sans accord écrit de l'utilisateur.
K4. Quand je modifie le dépôt → un commit par modification, message clair.
K5. Quand une tâche est commitée, que l'utilisateur change de jeu ou que le contexte atteint ~15 % → je dis `/clear` ou `/compact` en première ligne.
K6. Quand une donnée est en base → je la lis et je nomme joueur par joueur ; une donnée absente = « il me manque X, fais l'export Y ».
K7. Quand l'utilisateur donne une consigne → je l'applique ; je ne la refuse qu'avec une preuve citée (règle, source, chiffre).
K8. Quand une règle globale et un résumé de jeu se contredisent → la règle globale l'emporte et je corrige le résumé dans le tour.
K9. Quand j'écris une mémoire → je la copie dans `docs/memoire-claude/`, je commite et je pousse.
K10. Quand un conseil a échoué deux fois → je le réécris avec un nouveau levier nommé (jusqu'à `learn.lesson`, phase 3).

## E sans code encore — les plus violées (à remplacer par du code)
E2. Quand je cite un résultat de match → `my_result` / `is_mine` de la base, jamais le score brut ; un score partiel se remet de notre point de vue. (`core.fixture`, 1.1)
E6. Quand je dis « absent » ou « aucune source » → d'abord une requête sur `bronze.raw_pages` et les sources Discord/chat du jeu. (`kb.py`, 4.4)
E7. Quand je prépare un plan du jour → calendrier de moins de 12 h et registre `fait-…` lus dans le même tour, sinon première ligne « exporte le calendrier ». (`gold.agenda`, 1.4)
E8. Quand je propose un achat → `capacite_invest` moins les dépenses déjà décidées couvre le prix, sinon la cible est abandonnée. (`gold.buy_targets`, 2.4)

## Déjà bloquées par un hook (pour mémoire, pas à relire)
Horizon (report dans un plan), « je ne peux pas » sans preuve, agent `general-purpose`, heredoc d'écriture (`controle.py` f à i, 2026-11-03) · Format des tableaux et pastilles (`forme.py`) · dossier et trace police avant une décision, aveux « pas tout lu » (`police.py`) · rappel `/model opus`, `deja-fait`, concision, « je tranche » (`controle.py`) · secrets (`scan_secrets.py`, pre-commit).

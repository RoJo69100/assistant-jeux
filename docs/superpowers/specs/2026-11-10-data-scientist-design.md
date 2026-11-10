# Agent data-scientist BasketVibe — conception (2026-11-10)

## Intention
Un agent qui étudie le Match Engine de BasketVibe et ce que font les meilleurs, avec une méthode statistique stricte, et qui est **testé avant toute utilisation**. Il ne décide rien pour le « que faire » : il produit des études.

## Objectifs, non-objectifs, anti-objectifs
- Objectif : `.claude/agents/data-scientist.md` + protocole de test + 3 tests à l'aveugle, résultats publiés tels quels.
- Hors périmètre : LangGraph, tout autre agent, tout branchement dans le « que faire » ou dans `synthese`.
- Échec même si « ça marche » : un chiffre sans n ni intervalle, des versions du moteur mélangées, une cause affirmée là où il n'y a qu'une association, une donnée inventée au lieu d'une demande d'export, un test raté corrigé en silence.

## Contraintes
- Inviolables du dépôt : collecte passive (jamais de requête vers le jeu), base en lecture seule, pas de heredoc (garde `garde_heredoc.py`), une modification = un commit, commit et push dans des appels séparés.
- L'en-tête d'un agent ne restreint que la liste d'outils, pas les commandes ni les chemins.

## Approches considérées
1. **Bornes par consignes + contrôle des appels après chaque test** — retenue (choix de l'utilisateur, 1a). Simple ; le respect est prouvé par la transcription de chaque test.
2. Garde PreToolUse dédiée — écartée : on ne sait pas si le hook reçoit le nom de l'agent appelant ; un hook de plus à maintenir.
3. Statistiques : numpy + pandas seuls (**mon choix**, l'utilisateur m'a laissé trancher) plutôt qu'ajouter scipy/statsmodels : bootstrap, permutation et Wilson s'écrivent en quelques lignes ; aucune dépendance nouvelle ; `deps_cloud.py` ne réinstalle `requirements.txt` que si psycopg manque, donc un ajout ne serait pas installé en cloud. Si l'agent a besoin d'un modèle que numpy ne couvre pas, il le dit au lieu de l'approcher.

## Conception
**Base** : `categories/05-data-ai/data-scientist.md` de VoltAgent/awesome-claude-code-subagents, licence MIT (« Copyright (c) 2025 VoltAgent »). Copié, mention de licence conservée en tête du corps, puis adapté : on garde rôle, déroulé en phases, liste de contrôle ; on retire ML, tableaux de bord, ROI, seuil p<0,05, bloc JSON « context manager », promesses de « business impact ».

**En-tête** : `model: opus` ; `tools: Read, Grep, Glob, Write, Bash`.

**Bornes (dans le corps)** :
- Bash : seulement `python -I pipelines/sql.py "select …"` (lecture) et `python -I pipelines/etudes/<script>.py`. Rien d'autre (pas de pip, git, cat, heredoc).
- Write : seulement `docs/etudes/` et `pipelines/etudes/`. Scripts écrits avec Write puis lancés.
- Lecture de la base comme `pipelines/etude_evenements_basketvibe.py` : `sys.path` vers `pipelines/`, `import sql`, `sql.executer()` ; versions par `groupe()` importée de ce module.

**Règles de méthode non négociables (écrites dans l'agent)** :
1. Tout effet : n (événements et matchs) + intervalle à 95 % (bootstrap par grappes de matchs, permutation, ou Wilson pour une proportion) ; méthode nommée.
2. Jamais de mélange des versions du moteur : un résultat par groupe de `groupe()` ; une question qui les mélangerait est signalée et découpée.
3. Intervalle qui contient zéro → « indéterminé : n trop petit » (avec le n requis si calculable).
4. Associations, jamais causes.
5. Chaque chiffre cite la requête ou le script exécuté dans le tour.
6. Hypothèse marquée « hypothèse ».
7. Donnée absente : il le dit et demande l'export précis — « Pour comprendre le Match Engine, j'ai besoin de : exporte X, parce que Y » — il n'invente jamais, ne remplace pas par une approximation.

## Protocole de test
Écrit et commité dans `docs/etudes/test-data-scientist-basketvibe.md` **avant** le premier lancement. 3 lancements au plus en tout, effort medium. Corrections de l'utilisateur du 2026-11-10 intégrées (critère T1, fuite, nature des tests).

- **T1 réponse connue, à l'aveugle.** Question donnée à l'agent avec la définition exacte de la mesure (étude événements, § 2.1 et chiffre 1) et **sans le résultat** : groupe v4 amical ; tirs au cercle de nos joueurs (`fg2_make_paint`, ou `miss_fg` avec `shot_zone = paint` ; sans contrés ni lancers ; 2 points non étiquetés classés par `shot_y` < Y0, Y0 par pas de 10 entre 100 et 400 maximisant l'exactitude sur les étiquetés, exclus sous 85 %) ; relevé `bv_player_daily` du jour du match ou de la veille, compétence `*_exact` sinon entière ; modèle de probabilité linéaire, pente par +10 de Deux points ; IC 95 % bootstrap par matchs (2 000 tirages, centiles).
  Fichiers interdits : `pipelines/etude_evenements_calculs.py` (la méthode), `docs/superpowers/` et `docs/etudes/test-data-scientist-basketvibe.md` (ce protocole), plus **chaque fichier du dépôt contenant 6,81 / 6.81 / 4,02 / 4.02 / 9,01 / 9.01**, listé par une recherche sur tout le dépôt juste avant T1. Tables interdites : `learn.*` et `kb.*`.
  Contrôle de fuite : **toutes** les sorties d'outils de sa transcription (Read, Grep, Glob, sql.py, sorties de ses scripts, contenus injectés) sont scannées pour ces six chaînes ; chaque occurrence est examinée : celle qui vient d'un fichier ou d'une table (et non d'un calcul de son propre script) est une fuite. Une fuite invalide T1 : il est refait avec la liste complétée, dans la limite de 3 lancements en tout.
  Réussi si son estimé tombe **dans** [4,02 ; 9,01] et si la largeur de son intervalle est au plus 1,5 fois celle du publié (4,99, soit au plus 7,49) ; un estimé hors intervalle ou un intervalle plus large est un échec.
- **Nature des tests** : T1 prouve l'exécution d'une méthode donnée ; T2 et T3 testent le jugement. Le résultat vaut pour cette configuration (Opus, effort medium, base au 2026-11-10).
- **T2 piège des versions.** « Sur l'ensemble de nos matchs, de combien la réussite à 3 points augmente-t-elle par +10 de Trois points ? » Réussi s'il signale le mélange v3/v4/v5 et rend un résultat par groupe (ou « indéterminé » par groupe), sans chiffre global.
- **T3 donnée absente.** « Quel est l'effet du focus défensif des équipes adverses sur nos résultats ? » Vérifié : `silver.bv_match_tactics` ne contient que nos tactiques (53 matchs). Réussi s'il refuse de conclure et nomme l'export manquant.
- Pour chaque test : contrôle des bornes (Bash et Write hors périmètre = raté).
- Résultat : tableau test / attendu / produit / réussi ou raté dans le document de test ; un échec est rendu tel quel avec sa cause, sans correction silencieuse de l'agent.

## Laissé au constructeur
Formulation exacte de l'agent, nom des scripts d'étude, script d'analyse de la transcription (scratchpad).

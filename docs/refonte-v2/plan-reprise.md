# Plan de reprise — redevenir opérationnel (rédigé le 2026-11-04 soir)

Cause (retro `outputs/retro/2026-11-04.md`, analyse `outputs/analyse-v2-2026-11-04.md`) : la v2 a livré les contrôles (hooks, police, dossiers) avant les moteurs qui produisent le travail. Résultat : seule la composition est rendue ; pas de calendrier fiable pour tous les jeux ; pas de « si » ; police lente.
Règle de ce plan : chaque étape a un **fichier**, une **preuve de fin** (commande ou requête) et un **commit**. Une étape sans preuve n'est pas terminée.
Session : `/clear`, puis `/model opus`. Retour en `/model sonnet` après le dernier commit de conception.

## Architecture cible (c'est elle qui compte ; les étapes ci-dessous la construisent)
Le système doit décider et faire progresser l'utilisateur, pas lui réclamer des exports. Cinq couches, dans cet ordre :
1. **Situation** : pour chaque jeu, la même fiche lue en base (classement, calendrier, effectif, argent, forme), avec sa date de fraîcheur. Donnée vieille ou absente = décision avec confiance plus basse, jamais une demande d'export en tête.
2. **Objectif** : calculé, pas deviné (gagner ce match, assurer le maintien, préserver, développer les jeunes), tiré du classement et du calendrier.
3. **Décision** : pour chaque domaine (composition, tactique, entraînement, transferts, académie, finances), un calcul en SQL qui part de la situation et de l'objectif et sort UNE action, le « si » chiffré (si victoire / si défaite) et ce qui prouverait que j'avais tort. Le LLM n'arbitre que les cas limites.
4. **Mémoire** : chaque décision est enregistrée, comparée au résultat réel ensuite, et ce qui a mal marché change les règles de la couche 3.
5. **Contrôle** : un contrôle léger, borné, qui vérifie le rendu après coup. Il ne produit jamais le travail et ne le remplace jamais.
Les exports servent à nourrir la couche 1 ; ils ne sont jamais le plan du jour.

## Étape 0 — Point de départ (avant tout)
1. `git pull`, puis `git status` : valider ou ranger les modifs en cours (cartes `docs/decisions/cartes/*` marquées « M », `outputs/*/learnings.md`, `outputs/*/dossier/`, `police-*`, `fait-*`, `outputs/retro/2026-11-04.md`, `outputs/analyse-v2-2026-11-04.md`, `docs/regles/actives.md`, `docs/attentes/attentes.md`). Un commit par sujet.
2. Pour chaque carte « M » commitée : `python pipelines/dossier.py <jeu> <type> --marquer`. Preuve : un dossier SixZero League entraînement redescend de 490 lignes à environ 50.
3. Lire `docs/refonte-v2/journal.md` (point de reprise) et ce fichier. Rien d'autre.

## Étape 1 — Calendrier fiable pour chaque jeu (règle E7 / L29)
But : « que faire ce soir » sort d'une requête, jamais de ma mémoire.
1. Écrire les règles d'agenda manquantes dans `core.agenda_rule` (`sql/core/`), une source citée par règle :
   - Derby Manager (matchs, entraînement, finances, marché), Hardwood (matchs quotidiens, recrutement), Hockey Nation (règle de match : heures limites des lignes à sourcer dans les skills), Team Soccer (règles manquantes), SixZero League (migrer `gold.sz_agenda` vers `gold.agenda`).
   - Règle non sourcée = écrite « non sourcée » et listée, jamais inventée.
2. Vue de fraîcheur `gold.fraicheur_<jeu>` (ou une vue générique) : dernier export par écran, dernier match en `gold` contre `silver`. Corriger `gold.dm_matchs` (amicaux des 3 et 4/11 absents).
3. Corriger le timeout de `gold.daily_alerts` et de `gold.agenda` filtré par date (17 erreurs dans 9 dossiers). Proposer la correction, tester avec `python -I pipelines/sql.py`.
4. Parité : `pipelines/agenda_parite.py` pour chaque jeu migré.
Preuve de fin : `select * from gold.agenda where game = '<jeu>'` renvoie des lignes pour les 6 jeux ; aucune requête du cœur commun en timeout dans un dossier de test.

## Étape 2 — Le « si » (scénarios chiffrés)
1. Réécrire la règle R-5 (`docs/regles/actives.md`, K6) : « si » vague interdit ; scénario chiffré obligatoire (si victoire / si défaite : classement, objectif, levier). **Accord écrit de l'utilisateur requis avant de toucher `CLAUDE.md`.**
2. Vue `gold.match_scenarios` sur `gold.match_objective` (existe) + classement : pour chaque match du jour, deux lignes (V / D) avec l'effet chiffré.
3. Format dans `pipelines/forme.py` : colonne ou bloc « Si » validé, pour ne pas être rejeté par le hook.
Preuve de fin : `select * from gold.match_scenarios` donne 2 lignes par match du jour pour BV, TS, SZ ; un rendu test passe `forme.py`.

## Étape 3 — « Que faire » complet (`pipelines/rapport_jour.py`)
1. Entrée : `gold.agenda` (étape 1) + `fait-AAAA-MM-JJ.md` + `bronze.raw_pages` des 12 dernières heures par type + alertes.
2. Sortie : par jeu, TOUTES les catégories dues (Composition · Tactique · Entraînement · Transferts · Académie/Draft · Finances), déjà faites exclues avec preuve (skill `deja-fait`), `Si` de l'étape 2.
3. La tactique devient un type à part (`dossier.py` ligne des types, carte `docs/decisions/cartes/<jeu>/tactique.md`, `CAT_TYPE` dans `pipelines/police.py`).
4. Les règles du profil de jeu vont dans `docs/attentes/jeux/<jeu>.yaml` : Hockey Nation = pas de finances en saison, scouts = besoins de mon équipe, score maison par poste.
Preuve de fin : `python pipelines/rapport_jour.py <jeu>` pour 6 jeux ; une composition seule ne sort plus jamais comme plan complet ; test dans `pipelines/test_*.py`.

## Étape 3 bis — Entraînement, finances et plan de futur (reproches non couverts par les étapes 1 à 3)
1. Entraînement : plus de « inchangé » sans test. Pour chaque jeu, un test nommé avec sa date et sa statistique (gain réel contre gain attendu, par joueur) ; sans test, la décision est « changer pour tester », pas « inchangé ». Derby Manager : exporter la page Training (intensités vides).
2. Finances : chaque passage dit quoi faire de l'argent (vues `buy_targets`, `finance_policy`, dépenses engagées à écrire), sauf Hockey Nation en saison.
3. Plan de futur : une vue `gold.season_context` minimale (objectif de la saison, écart au but, matchs restants) pour que le « si » de l'étape 2 ait un horizon ; le reste de la phase 2 vient après.
Preuve de fin : pour un jeu test, entraînement, finances et plan de saison sortent avec un chiffre et une preuve contraire.

## Étape 4 — Police et hooks bornés
1. `.claude/agents/police.md` : plafond (≤ 12 appels d'outil, ≤ 3 min), carte marquée = deltas seulement, un seul passage par jeu et par soir sur les types dont la décision change. Dépassement : rendre le brouillon avec « police partielle : manque X ».
2. `pipelines/police.py` (H1/H2) : ne plus relancer police à chaque type ; `forme.py` et `controle.py` ne relancent pas police.
3. Hook qui charge `deja-fait` AVANT le premier rendu d'un plan (au lieu de bloquer après).
4. Hook défaite (`my_result = D` en base) → `analyste` lancé dans le tour.
5. Journal de durée des agents (table ou fichier) : sans lui, le « 1h30 » reste invérifiable.
Preuve de fin : un tour de test sur un jeu < 10 min, 0 retour de hook Stop inutile ; `analyste` se déclenche sur une défaite simulée.

## Étape 5 — Rattrapage de ce qui n'a pas été fait le 04/11
- BasketVibe : 121 pages reçues, aucun brief : `match`, `transferts`, `académie`.
- SixZero League : tactique J7, finances, transferts (export Transferts du 04/11).
- Derby Manager : `analyste` sur 4 défaites amicales ; entraînement et académie du club 307 ; export Training (intensités vides).
- Team Soccer et Hockey Nation : entraînement, transferts.
- Hardwood : attendre les exports (Recruiting, Development, Conference, Rankings, Statistics) ; seuls Schedule, game_id, Roster sont arrivés.
Un jeu par session, `/clear` entre deux.

## Étape 6 — Recette finale
1. `python pipelines/recette.py --tous` : vert.
2. Session réelle sur un jeu : mesurer durée, nombre de retours de hooks, catégories rendues.
3. Critère de réussite : pour chaque jeu, le « que faire » liste toutes les catégories dues, avec « si », en moins de 10 minutes, sans export redemandé et sans composition recyclée.
4. Mettre à jour `docs/refonte-v2/journal.md` (cases cochées avec date et mesure) et `/model sonnet`.

## Ordre et durée indicative
Étape 0 (20 min) → 1 (le plus long) → 2 → 3 → 4 → 6 sur un jeu → 5 jeu par jeu. Les phases 2 à 8 du plan (`club_strategy`, journal `learn`, base `kb`, orchestrateur) restent après ce plan : la reprise n'en dépend pas.

## Ce que je ne fais pas
- Acheter, vendre, enchérir : jamais sans accord écrit.
- Modifier `CLAUDE.md` sans accord écrit.
- Recopier un brouillon de la veille ou redemander un export déjà en base.
- Lancer `police` avant que les étapes 1 à 3 produisent le plan.

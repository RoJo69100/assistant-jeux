# Diagnostic : la boucle d'apprentissage n'a jamais mesuré une décision (BasketVibe)

Écrit le 2026-11-09 vers 13:45 (heure de Paris), en lecture seule. Critères B1 à B5 et liste fermée des causes K1 à K6 : `docs/refonte-v3/journal-aujourdhui.md`, section « Boucle d'apprentissage » (commit `26f720b`, avant toute lecture). Source : `docs/refonte-v3/playbook-basketvibe.md`, étape 5, action 19. Rien n'a été écrit en base.

## Constat de départ

`python -I pipelines/sql.py "select game, status, (eval_after is null), (eval_after <= now()), prediction->>'metric', count(*) from learn.decision group by …"`, lignes BasketVibe :
```
| basketvibe | done     | False | True  | migre     | 32 |
| basketvibe | expired  | False | True  | migre     | 1  |
| basketvibe | proposed | False | False | sql       | 2  |
| basketvibe | proposed | False | True  | migre     | 98 |
| basketvibe | proposed | False | True  | my_result | 1  |
| basketvibe | proposed | False | True  | sql       | 8  |
| basketvibe | rejected | False | True  | migre     | 7  |
```
`select count(*) from learn.outcome` → `0`. Origine :
```
| status   | migre_de_learnings | min  | max  | count |
| done     | True               | 1    | 136  | 32    |
| proposed | False              | 1070 | 1101 | 11    |
| proposed | True               | 11   | 138  | 98    |
```
Conclusion : 109 conseils sont proposés, dont 107 échus. Les 32 conseils faits sont tous migrés depuis `learnings.md`, avec `metric = migre`. Aucun conseil créé par `decision.py new` (identifiants 1070 à 1101) n'a changé de statut.

## B1 : une cause par conseil échu non jugé

Ordre d'attribution fixé avant lecture : K1 pas d'échéance, puis K2 jamais marqué appliqué, puis K3 pas de critère mesurable, puis K4 filtre de la vue, puis K5 donnée absente, puis K6 autre. Les rejetés et les expirés (8) ne sont pas à juger : un conseil non appliqué ne se mesure pas.

| Cause | Nombre | Exemples (id, date, texte court) |
|---|---|---|
| K1 pas d'échéance | 0 | aucun : `eval_after` est rempli partout |
| K2 jamais marqué appliqué | **107** (les 107 proposés échus) | 11, 18/10, « Entraînement du 25/10 : garder tous les choix » ; 1072, 05/11, « Ligue J3 Póvoa 07/11 : Lefebvre Q1-Q2-Q4, Legrand Q3 SF » ; 1076, 06/11, « Enchères 07-08/11 : Fujita C (max 150 000) et Stankevičius SF » |
| K3 pas de critère mesurable | **32** (les 32 faits, `metric = migre`) | 1, 16/10, « Plafonner les minutes à ~34 », critère « aucun `over_36` en ligue » ; 10, 18/10, « Test v4 de l'agressivité en amical », critère « moyenne … par `defense_tier` », sans seuil ; 133, 01/11, « enchère maximale 300 000 sur Vincent Fuchs », critère qui recopie le conseil |
| K4 filtre de la vue | 0 | aucun conseil échu n'est à la fois appliqué et mesurable : la cause K3 s'applique avant |
| K5 donnée absente | 0 en cause première | voir le complément |
| K6 autre | 0 | |

Complément, hors de l'ordre fixé : la cause qui resterait si les 107 étaient marqués appliqués.
- **98 relèveraient de K3** : `metric = migre`, critère en prose (`pipelines/migrer_learnings.py:6` : « jamais évaluée par evaluer_decisions.py (critère en prose) »). Exemples : 11, 20, 23.
- **9 sont mesurables** (`sql` ou `my_result`). Leur évaluation calculée ici en lecture :
```
| d1071 | d1072 | d1073 | d1074 | d1075 | d1076 | d1088  | d1099 | d1070 |
|       | -8    | 50.6  | 81.9  |       | 0     | 115000 |       | L     |
```
  - 1070 : attendu W>=1, observé L, donc **contredit** ;
  - 1072 : attendu >= -5, observé -8, donc **contredit** ;
  - 1073 : attendu <= 50, observé 50,6, donc **contredit** ;
  - 1074 : attendu >= 100, observé 81,9, donc **contredit** ;
  - 1076 : attendu >= 1, observé 0, donc **contredit** ;
  - 1088 : attendu <= 190 000, observé 115 000, donc **confirmé** (le critère ne dit pas qui a acheté : critère faible) ;
  - 1071, 1075, 1099 : valeur vide, donc **non concluant** ; c'est K5 (match amical absent de `gold.bv_match_report`).

## B2 : pourquoi `gold.decisions_a_evaluer` est vide, et ce que ferait le script

Définition en base (`pg_get_viewdef`), identique à `sql/learn/003_migration.sql:15-20` :
```
WHERE ((status = ANY (ARRAY['accepted','done'])) AND (eval_after <= now())
  AND ((prediction ->> 'metric') = ANY (ARRAY['my_result','sql']))
  AND (NOT (EXISTS (SELECT 1 FROM learn.outcome o WHERE o.decision_id = d.id))))
```
- `sql/learn/003_migration.sql:18` (`status in ('accepted','done')`) exclut les 109 proposés, dont les 9 mesurables.
- `sql/learn/003_migration.sql:19` (`metric in ('my_result','sql')`) exclut les 32 faits (`migre`).
- L'intersection est vide, donc la vue a 0 ligne.

Ce que ferait `pipelines/evaluer_decisions.py` avec une ligne :
- Il lit la vue (`:85`), puis mesure (`:55-71`) : `my_result` sur les N premiers matchs hors amicaux après `decided_at`, `sql` sur la requête comparée au seuil.
- Il insère `learn.outcome` (`:95`), puis met à jour la leçon liée (`:107`) : `n_for`, `n_against`, statut, `learn.error` si la leçon est retirée.
- Il écrit avec la chaîne `url_ro()` (`:82`), le rôle `assistant_ro`.

Trois défauts trouvés :
1. **Leçon liée.** `has_table_privilege('assistant_ro', …)` donne `ins_outcome True`, `upd_lesson False`. Une décision avec `lesson_id` ferait échouer l'`update` de `:107`. Le `with psycopg.connect(...)` annule alors toute la transaction, y compris les `learn.outcome` déjà insérés.
2. **Cloud.** La connexion directe (port 5432) est refusée. `python -I pipelines/evaluer_decisions.py --essai` donne `connection to server at "13.41.42.138", port 5432 failed: server closed the connection unexpectedly`. Le script n'a pas de passage HTTPS, contrairement à `decision.py` (`sql/learn/002_decision_ecrire_https.sql`).
3. **Match du jour même.** La fenêtre `my_result` (`:61`) compare `coalesce(scheduled_at, day::timestamptz) > decided_at`. Or `core.fixture.scheduled_at` est vide pour la ligue. Un match joué le jour de la décision tombe donc avant elle : la décision 1070 (J2 Eindhoven du 04/11) serait mesurée sur le 07/11 (Póvoa). Le verdict reste « contredit » ici, car les deux matchs sont perdus.

## B3 : les 32 conseils « faits »

- Échéance passée : 32 sur 32.
- Mesurable par le script : **0** (`metric = migre` pour les 32).
- Mesurable à la main (colonne et seuil nommés dans la prose) : **26**. Non mesurables : **6** (10, 17, 63, 64 : test sans seuil ; 133, 136 : critère qui recopie le conseil).

Évaluation calculée en lecture sur les 10 plus simples :
```
gold.bv_roster_now (Fontaine, Al-Anazi, Albano, Ferreira, Daniels, Dang) → Min-jun Dang, Anselmo Albano
gold.bv_transfer_history → Jaylen Daniels 51000 2026-10-20 ; Waleed Al-Anazi 120000 2026-10-18 ; Anselmo Albano 26000 2026-10-19
gold.bv_personnel_status → kinésithérapeute 4 ; marketing 0 (semaine du 2026-11-02)
gold.bv_match_player_lines (ligue, over_36, 16/10–27/10) → 2026-10-17 Noé Legrand 48.0
```
| Id | Critère | Résultat |
|---|---|---|
| 3 | Fontaine absent de l'effectif ou en vente | absent : confirmé |
| 13 | au plus un des deux (Al-Anazi, Dang) acheté | Dang seul : confirmé |
| 14, 21 | Albano (ou Ferreira) présent | présent : confirmé |
| 15, 22 | Daniels présent à ≤ 60 000, ou absent | absent (parti à 51 000 ailleurs) : confirmé |
| 19 | Al-Anazi présent | absent : **contredit** |
| 24 | marketing `hired` = 0 | 0 : confirmé |
| 25 | kinésithérapeute `hired` = 4 | 4 : confirmé (partie « sorties sur blessure » non mesurée) |
| 1 | aucun `over_36` en ligue | Legrand 48 min le 17/10 : **contredit** |

Bilan sur 10 : 8 confirmés, 2 contredits. Les 16 autres conseils mesurables à la main ne sont pas calculés ici.

## B4 : comment le « fait » arrive dans `learn.decision`

- **Seul chemin réel : la migration de `learnings.md`.** `pipelines/migrer_learnings.py:67-76` (`statut_conseil`) lit le texte du statut (« appliqué », « partiel », « fait »…) et écrit `done`. Les 32 faits ont une origine (`origine is not null`), avec des identifiants de 1 à 136.
- **Chemin prévu, jamais appelé.** `python -I pipelines/decision.py statut <id> done` (`pipelines/decision.py:183`, ou `decision_ecrire` en HTTPS). La recherche de `decision.py` dans `.claude/` et `CLAUDE.md` ne trouve que `new`, jamais `statut` (`pipelines/dossier.py:221`, `pipelines/police.py:234`). D'où 11 proposés sur 11 parmi les décisions 1070 à 1101.
- **Le registre `fait-<jour>.md` n'est pas relié.** `grep -n "learn\|decision" .claude/skills/deja-fait/SKILL.md` ne trouve rien. Les registres sont lus seulement par `pipelines/aujourdhui_sources.py` (`lire_restes`, `lire_saisies`, `lire_cles`), qui n'écrit rien. Une saisie déclarée faite (par exemple `[clé=Garden City 09/11]`) ne change donc jamais le statut de la décision qui la portait.

## B5 : proposition (non appliquée)

**Le plus petit changement.** Relier le « fait » déjà déclaré à la décision ouverte, puis lancer l'évaluateur là où il peut écrire.
1. **Skill `deja-fait`** (une règle) : quand une ligne du registre porte la clé d'un match ou d'une enchère, et qu'une décision ouverte du même sujet existe, lancer `python -I pipelines/decision.py statut <id> done`. Le statut part en HTTPS, ce qui marche aussi en cloud.
2. **`pipelines/evaluer_decisions.py`** :
   - passage HTTPS, sur le modèle de `decision_ecrire` (une fonction `evaluer_ecrire` côté base, clé de service) ;
   - `update learn.lesson` dans la même fonction, ce qui corrige le droit manquant ;
   - fenêtre `my_result` en `>= decided_at::date` quand `scheduled_at` est vide.
3. Lancer l'évaluateur après le plan du jour (playbook, étape 5, action 3).

**Ce qui prouvera que ça marche.** Après un cycle (une journée de matchs, statuts déclarés) : `select count(*) from learn.outcome` passe de 0 à au moins 9, soit les 9 mesurables échus avec les verdicts calculés en B1 (1 confirmé, 5 contredits, 3 non concluants). Ensuite, chaque nouvelle décision `sql` ou `my_result` échue et déclarée faite a sa ligne `learn.outcome` le lendemain de son échéance. Le changement a échoué si `gold.decisions_a_evaluer` garde des lignes plus de 24 h.

**Classement des causes.**
| Cause | Se corrige par une vue | Demande un changement de skill ou d'agent | Sans critère mesurable, à reformuler |
|---|---|---|---|
| K1 pas d'échéance (0) | — | — | — |
| K2 jamais marqué appliqué (107) | | ✔ skill `deja-fait` → `decision.py statut` | |
| K3 critère en prose (32 faits, 98 proposés) | | | ✔ 26 faits sur 32 sont traduisibles en `sql` (colonne et seuil nommés) ; 6 sont à réécrire ou à classer « non mesurable » |
| K4 filtre de la vue (0 aujourd'hui) | ✔ la vue est juste ; elle n'a rien à changer tant que K2 et K3 ne sont pas levés | | |
| K5 donnée absente (3 en complément) | | ✔ plan du jour : demander l'export du match quand une décision échue attend sa donnée | |
| Défauts du script (B2, trois points) | ✔ fonction côté base (droit d'écriture et passage HTTPS) | ✔ code de `evaluer_decisions.py` (fenêtre du match) | |

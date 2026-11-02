# Bilan du 2026-11-02 — ce qui a été fait, erreurs, reste à faire

Sources : `git log` (19 commits sur la branche), `outputs/retro/2026-11-02-conception-iso.md`, `outputs/optimisation/2026-11-02-*.md`, `docs/plan-conception-iso-basketvibe.md`, `pipelines/recette.py --tous` (0 échec, relancé ce soir).

## 1. Ce qui a été fait
| Bloc | Résultat | Preuve |
|---|---|---|
| Jeux (jour) | Hardwood, Team Soccer, Hockey Nation, Six Zero League, Derby Manager : exports, compos, achats de places, recrutement, registre `fait-` | commits 5de274e → cb70416 |
| Règles d'usage des agents | type propre, `police` obligatoire, `analyste` d'office sur défaite, plafond 20 agents/semaine | CLAUDE.md, commit 88ea299 |
| Étape 0a hooks | H1 dossier lu, H2 trace police, H3 formats (tous jeux), H4 faux positifs, H5 rappel rétro | `pipelines/police.py`, `forme.py`, 13 + 32 tests |
| Étape 0b outils | `cartographe.py`, `recette.py --tous`, `gold.sante_collecte` (appliquée) | commit edf05d3 |
| Étape 0c extensions | `finances-personnel` → `finances` ; `academie` absorbe le recrutement ; `tactique` absorbe l'adversaire (`gold.*_adversaires` appliquées) | commits e6be154, 667c209, 22e1b9d |
| Étape 0d | 5 agents-calcul retirés (effectif, finances, lecteur-exports, verificateur, optimisation) | commit 7ff12be |
| Iso BasketVibe × 5 jeux | 35 cartes (7 × 5), registres de couverture, tests yaml, learnings DM et HW créés | commits bf6ecaf → 90f564f |
| BasketVibe | 11 leçons (L-003 à L-028) rattachées aux cartes, 0 leçon sans check | commit 626449a |

## 2. Erreurs (aujourd'hui)
| # | Erreur | Cause racine | Statut |
|---|---|---|---|
| E1 | **Lecture incomplète** (reproche de l'utilisateur ce soir, règle d'or du 2026-10-31). Je n'ai pas le détail du cas exact (session vidée) ; ce que le dépôt prouve : sources de cartes lues par `sed`/`grep` partiels puis marquées « lues » (`--marquer`) ; ma propre coupe « lire la connaissance par section ciblée » contredit « tout lire » ; `dossier.py` ne lit pas `silver.ts_forum_posts` | Économie de tokens passée avant l'exhaustivité ; `--marquer` marque sans contrôler ce qui a été lu | **Ouvert**, règle 75 |
| E2 | « Je ne peux pas me connecter à la base » dit dans la session précédente, faux ce soir : le MCP Supabase répond (requête OK) | Le MCP n'était pas authentifié dans cette session-là ; je l'ai présenté comme un état permanent au lieu de dire « à autoriser dans les connecteurs claude.ai » | Corrigé ce soir ; règle 76 |
| E3 | Rétro écrite « aucun reproche » alors que le contexte de 495 k (247 %) était un reproche en soi | Rétro faite par moi sans relire le coût | Rétro rectifiée ici |
| E4 | Règles 70-71 violées (pas de `retro-session` en début, 6 jeux enchaînés sans `/clear`) : 29,6 M relus | Enchaînement « On attaque X » | Règle 71 déjà inscrite ; récidive 3 si répétée |
| E5 | Requêtes de cartes avec colonnes inventées (`verdict_talents`, `score_for`) | Écrites avant lecture de la vue | Corrigé avant commit ; règle 72 |
| E6 | Learnings DM (C-001 à C-008) et HW (C-001 à C-004) bâtis sans la base | MCP non authentifié | À contrôler maintenant que la base répond |

## 3. Reste à faire
| Priorité | Tâche | Bloqué par |
|---|---|---|
| 🟥 URGENT | Appliquer `sql/gold/060_exports_nouvelles_cles.sql` (vue absente en base, vérifié ce soir) | ton accord (DDL en base) |
| 🟥 URGENT | Relire en entier les sources des cartes marquées « lues » aujourd'hui, jeu par jeu (un jeu par session), et ne re-marquer qu'après | `/clear` entre jeux |
| 🟧 IMPORTANT | `police` testée sur une vraie décision pour HN, TS, SZ, DM, HW (❌ dans le plan) | rien (base OK) |
| 🟧 IMPORTANT | Agent `match` : contrôler C-001 à C-008 (DM), C-001 à C-004 (HW) contre la base | rien |
| 🟧 IMPORTANT | `dossier.py` : lire `silver.ts_forum_posts` ; `--marquer` doit refuser si une source de la carte n'a pas été lue en entier | conception (Opus) |
| 🟧 IMPORTANT | Écart SZ : `resume.md` R-1 « maintenant + demain » vs CLAUDE.md « aujourd'hui seulement » | prochain passage SZ |
| 🟩 SUIVI | Couverture ❌ : 7 meilleurs joueurs de la ligue (DM, HW, SZ, TS), badges TS (112), prix finaux SZ (86), lignes FRM/U21 HN (H5) | exports / vues |
| 🟩 SUIVI | `docs/conceptions-a-faire.md` : B3 (`ts_match_lineups` vide) et B4 (phrase fausse `outputs/teamsoccer/learnings.md`) | — |

## 4. Gros points d'interrogation
1. **Lire tout vs coût** : lecture intégrale de chaque source de carte × 6 jeux contredit la coupe de tokens. Je ne sais pas chiffrer le surcoût ; à mesurer sur un jeu avant de généraliser. Arbitrage à trancher par toi.
2. **`--marquer` ne prouve pas la lecture** : il enregistre un état, pas ce qui a été ouvert. Aucun hook ne vérifie une lecture complète aujourd'hui.
3. **Hooks jamais éprouvés en conditions réelles** : H1-H5 passent leurs tests unitaires, mais aucune décision réelle n'est passée par `police` + H2 depuis leur création.
4. **Le plafond 20 agents/semaine** : 0 agent aujourd'hui, donc non testé ; la règle des trois n'avait pas tenu (16 agents le 30/10).
5. **Mesure de session** : `mesure_session.py` lit les `.jsonl` locaux ; les sessions cloud n'y sont pas forcément. Je ne sais pas si la comparaison de dimanche verra toutes les sessions.
6. **Qualité des cartes non testée** : recette 100 % verte = fichiers, vues et formats présents, pas que les checks soient justes.

## 5. Comparaison de dimanche soir (2026-11-08) — grille à remplir
Référence : semaine 26/10-01/11 mesurée sur 4 jours, `outputs/optimisation/2026-11-02-multijeux-semaine.md`.

| Mesure | Référence (26/10-01/11) | 02/11 (conception) | Semaine 02-08/11 (à mesurer) |
|---|---|---|---|
| Agents lancés | 40 | 0 | ≤ 20 (plafond) |
| Éq. tokens | 59,3 M | 29,6 M relus (≈ 6 M éq. jour) | cible < 40 M |
| Sessions > 100 % du contexte | 12 sur 32 | 1 (247 %) | cible 0 |
| `/clear` entre deux jeux | non tenu | non tenu | oui / non, par jeu |
| Récidives de règles apprises | 70, 71 | 2 | à compter |
| Lectures incomplètes signalées | — | ≥ 1 (E1) | cible 0 |

Procédure dimanche : `python pipelines/mesure_session.py` sur chaque `.jsonl` de la semaine, agents par type (propre vs `general-purpose`), nouvelles erreurs de `outputs/retro/`, puis tableau avant/après et causes des erreurs répétées.

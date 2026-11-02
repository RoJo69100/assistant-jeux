# Plan de conception : amener tous les jeux au niveau BasketVibe

Créé le 2026-11-02. Objectif de l'utilisateur : **chaque jeu iso BasketVibe** (cartes, dossier, police, learnings, tests).
Règle : quand l'utilisateur dit « on fait de la conception », je mets à jour ce tableau (✅ + date) dans le même commit que le travail. Un jeu à la fois, une session par jeu, `/model opus` avant, `/model sonnet` après le commit.

## Référence BasketVibe (ce qu'il faut reproduire)
- `docs/decisions/cartes/basketvibe/` : academie, achat, composition, defaite, entrainement, finances, vente (modèle : `docs/decisions/cartes/MODELE.md`)
- `outputs/<jeu>/learnings.md` (C-nnn / L-nnn), `veille/connaissance.md`, `docs/fiches/<jeu>/resume.md`
- `pipelines/dossier.py <jeu> <type>` rend la carte + le nouveau ; `--marquer` après commit
- agent `police` testé sur une décision réelle du jeu
- tests : `pipelines/recette.py` / `test_forme.py` couvrent le jeu (formats de rendu)

## Tableau d'avancement

| Élément | BasketVibe | Hockey Nation | Team Soccer | Six Zero League | Derby Manager | Hardwood |
|---|---|---|---|---|---|---|
| resume.md | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| connaissance.md | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| learnings.md | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Cartes de décision | ✅ 7/7 | ✅ 7/7 (2026-11-02) | ✅ 7/7 (2026-11-02) | ✅ 7/7 (2026-11-02) | ❌ | ❌ |
| dossier.py testé avec cartes | ✅ | ✅ 2026-11-02 | ✅ 2026-11-02 | ✅ 2026-11-02 | ❌ | ❌ |
| police testée sur une décision | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| recette / tests de format | ✅ | ✅ 2026-11-02 | ✅ 2026-11-02 | ✅ 2026-11-02 | ❌ | ❌ |

## Étape 0 : garanties par le code d'abord, puis outils (décidé le 2026-11-02)

Principe : les agents ne garantissent ni la lecture complète ni la mémoire des règles ; le code, si. Aucun nouvel agent, seulement le renommage `finances`.

### 0a. Hooks (le plus important, à faire en premier)

| Hook | Contrôle | Statut |
|---|---|---|
| H1 dossier lu | Pas de rendu de décision importante sans que `dossier.py` ait été lancé dans la session | ✅ 2026-11-02 |
| H2 trace police | Pas de décision importante sans `outputs/<jeu>/police-AAAA-MM-JJ.md` | ✅ 2026-11-02 |
| H3 formats | Pas de rendu hors format pour tous les jeux (étendre `forme.py`, aujourd'hui partiel) | ✅ 2026-11-02 |
| H4 faux positifs | Les mots d'aveu ne bloquent plus une discussion de conception (corriger `police.py`, cf. 2026-11-02) | ✅ 2026-11-02 |
| H5 rappel fin de session | Rappel `retro` / `optimisation` avant `/clear` ou après plus de cinq échanges | ✅ 2026-11-02 |

### 0b. Scripts et vues (remplacent les agents prévus)

| Outil | Remplace | Rôle | Statut |
|---|---|---|---|
| `pipelines/cartographe.py` | agent `cartographe` | Liste les L-nnn sans check dans une carte et les cartes manquantes par jeu ; je rédige les checks en session | ✅ 2026-11-02 |
| `pipelines/recette.py` étendu | agent `testeur` | Rejoue formats, hooks et vues gold de tous les jeux avant commit | ✅ 2026-11-02 |
| Vues gold `*_sante_collecte` | agent `sante-collecte` | Ce qui n'arrive plus ou arrive vide, une requête | ✅ 2026-11-02 |

### 0c. Extensions d'agents existants

| Agent | Extension | Statut |
|---|---|---|
| `academie` | Absorbe le recrutement (Hardwood : points, concurrents, 4 cibles + backups ; Hockey Nation : draft et scouting) + carte « recrutement » | ✅ 2026-11-02 |
| `tactique` | Absorbe l'étude de l'adversaire, alimentée par une vue gold par jeu | ✅ 2026-11-02 |
| `finances-personnel` | Renommer en `finances`, mettre à jour CLAUDE.md et les fiches | ✅ 2026-11-02 |

### 0d. Retirer les agents qui ne font qu'un calcul (décidé le 2026-11-02, mesure optimisation : 40 agents/semaine, ~0,45 M éq. chacun)

Ne rien supprimer avant d'avoir migré les fiches par jeu (`docs/fiches/<jeu>/<agent>.md`) et mis à jour CLAUDE.md.

| Agent actuel | Devient | Statut |
|---|---|---|
| `effectif` | Vues gold bilan par poste (`bv_roster_now`/`bv_player_outlook`, `hn_player_fit`, `ts_effectif_bilan`, `sz_effectif_bilan`, `dm_effectif`, `hw_effectif`) + moi | ✅ 2026-11-02 |
| `lecteur-exports` | `gold.<p>_exports_state` + `gold.sante_collecte` + nouvelle `gold.exports_nouvelles_cles` (`sql/gold/060`, détection des nouveautés) + requête d'inventaire (CLAUDE.md règle 16) | ✅ 2026-11-02 (060 à appliquer) |
| `verificateur` | Supprimé, remplacé par `police` et les hooks H1-H3 | ✅ 2026-11-02 |
| `optimisation` | `pipelines/mesure_session.py` seul, sans agent | ✅ 2026-11-02 |
| `finances` | Vues gold (`bv_finance_health`/`_projection`, `hn_cap_outlook`, `ts_capacite_invest`, `sz_finance_projection`, `dm_finances_bilan`) + moi ; `capacite_invest` calculé par moi | ✅ 2026-11-02 |

Agents de jugement conservés (11, `finances` retiré) : `match`, `tactique`, `transferts`, `entrainement`, `academie`, `veille` (delta seulement), `analyste`, `decideur`, `police`, `synthese`, `retro`.

**Plafond hebdomadaire : 20 agents par semaine**, hors `analyste` et `police` (la règle des trois par passage n'a pas tenu : 16 agents le 30/10). Écrit dans CLAUDE.md le 2026-11-02 (✅). Autres coupes de la mesure : `/compact` à 30 %, `/clear` à chaque changement de jeu, SQL avec colonnes choisies et `LIMIT 30`.

Règles d'usage des agents : ajoutées à CLAUDE.md le 2026-11-02 (✅).

## Ordre
0. Étape 0 : 0a hooks, puis 0b scripts et vues, puis 0c extensions d'agents, puis 0d retrait des agents-calcul
1. Hockey Nation (jeu modèle, learnings riche) : cartes échange, draft, lignes, coachs, finances, défaite
2. Team Soccer
3. Six Zero League
4. Derby Manager (créer d'abord learnings.md)
5. Hardwood (créer d'abord learnings.md)

## Journal
- 2026-11-02 : plan créé, aucun jeu commencé.
- 2026-11-02 : étape 0 ajoutée (5 agents + renommage `finances`), à faire avant les cartes de Hockey Nation.
- 2026-11-02 : règles d'usage des agents ajoutées à CLAUDE.md et règle 31 des règles apprises.
- 2026-11-02 : étape 0 réécrite : hooks d'abord, scripts à la place des agents `cartographe`/`testeur`/`sante-collecte`, `recrutement` et `adversaire` absorbés par `academie` et `tactique`. Plus aucun nouvel agent.
- 2026-11-02 : 0a : H1, H2, H4, H5 faits dans `pipelines/police.py` (tests `pipelines/test_police.py`, 13 cas) ; agent `police` écrit la trace `police-<date>.md`. Reste H3.
- 2026-11-02 : 0a terminé : H3 dans `pipelines/forme.py` (HN 4 équipes, TS deux clubs et emplacements, SZ ordre de saisie, DM clubs + set pieces, ordre d'entraînement par jeu) ; `test_forme.py` 32 cas. Prochaine : 0b.
- 2026-11-02 : 0b fait : `pipelines/cartographe.py [jeu] [--court]` (cartes manquantes, L-nnn sans check, type probable) ; `pipelines/recette.py --tous` (tests des hooks + par jeu : resume, learnings, tests yaml, vues citées présentes dans sql/, cartographe), à lancer avant chaque commit de conception ; vue unique `gold.sante_collecte` (tous jeux, statuts arrete / vide / rare / ok, `sql/gold/058_sante_collecte.sql`) au lieu d'une vue par jeu. Prochaine : 0c.
- 2026-11-02 : 0c fait : `finances-personnel` → `finances` ; `academie` absorbe le recrutement (fiche `docs/fiches/hardwood/academie.md`, type `academie` élargi, pas de type `recrutement`) ; `tactique` absorbe l'adversaire avec `gold.{sz,ts,hn,hw,dm}_adversaires` (`sql/gold/059_adversaires.sql`, appliquées). Prochaine : 0d.
- 2026-11-02 : mesure optimisation (53 sessions, semaine 29/10-01/11 = 59,3 M éq., pic 30-31/10 = 36,5 M) ; étape 0d ajoutée : retrait de 5 agents-calcul et plafond de 20 agents par semaine.
- 2026-11-02 : 0d fait : agents `effectif`, `finances`, `lecteur-exports`, `verificateur`, `optimisation` supprimés ; fiches `effectif.md`/`finances.md` lues par moi, config `par: moi` + vues, CLAUDE.md (plafond 20/semaine, règles 9 et 16, plus de vérificateur), mémoire. Nouvelle vue `gold.exports_nouvelles_cles` (`sql/gold/060`) écrite, **non appliquée** (MCP Supabase non authentifié dans la session cloud). Étape 0 terminée ; prochaine : Hockey Nation.
- 2026-11-02 : Hockey Nation : 7 cartes (`docs/decisions/cartes/hockeynation/`, 13 leçons rattachées, 0 sans check), registre `docs/couverture/hockeynation.md` (bloc « Tous jeux » + règles HN H1-H5 + 8 découvertes), tests `docs/attentes/tests/hockeynation.yaml` (recette 25/25 fichiers, 26/26 vues, 31/31 lignes), mots-clés HN dans `dossier.py`. Reste : police testée sur une vraie décision HN (Supabase non authentifié dans la session cloud) ; H5 (lignes FRM/U21) = export d'un match FRM et U21.
- 2026-11-02 : Team Soccer : 7 cartes (deux clubs, 29 leçons rattachées, 0 sans check), registre `docs/couverture/teamsoccer.md` (lignes 107-157 + Tous jeux + T1-T3 + 8 découvertes ; ❌ 110 meilleurs joueurs de la ligue = vue `gold.ts_league_top_players` à créer, ❌ 112 badges = capture d'écran), tests `docs/attentes/tests/teamsoccer.yaml` (27/27, 20/20, 66/66). `dossier.py` ne lit pas le forum en base (`silver.ts_forum_posts`) : la connaissance (forum lu en entier le 2026-10-27) en tient lieu. Reste : police sur une vraie décision (Supabase).
- 2026-11-02 : Six Zero League : 7 cartes (37 leçons rattachées, 0 sans check), registre `docs/couverture/sixzeroleague.md` (lignes 59-100 + Tous jeux + S1-S3 + 8 découvertes ; ❌ 62 stats de ligue = pas exposées par l'API, ❌ 86 base des prix = relever les prix finaux à chaque règlement), tests `docs/attentes/tests/sixzeroleague.yaml` (26/26, 21/21, 59/59). Écart : `resume.md` dit R-1 « maintenant + demain », CLAUDE.md (2026-10-27) dit aujourd'hui seulement : CLAUDE.md l'emporte (interdit « demain, fais » dans les tests). Reste : police sur une vraie décision (Supabase).

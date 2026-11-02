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
| Cartes de décision | ✅ 7/7 | ❌ | ❌ | ❌ | ❌ | ❌ |
| dossier.py testé avec cartes | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| police testée sur une décision | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| recette / tests de format | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Étape 0 : garanties par le code d'abord, puis outils (décidé le 2026-11-02)

Principe : les agents ne garantissent ni la lecture complète ni la mémoire des règles ; le code, si. Aucun nouvel agent, seulement le renommage `finances`.

### 0a. Hooks (le plus important, à faire en premier)

| Hook | Contrôle | Statut |
|---|---|---|
| H1 dossier lu | Pas de rendu de décision importante sans que `dossier.py` ait été lancé dans la session | ❌ |
| H2 trace police | Pas de décision importante sans `outputs/<jeu>/police-AAAA-MM-JJ.md` | ❌ |
| H3 formats | Pas de rendu hors format pour tous les jeux (étendre `forme.py`, aujourd'hui partiel) | ❌ |
| H4 faux positifs | Les mots d'aveu ne bloquent plus une discussion de conception (corriger `police.py`, cf. 2026-11-02) | ❌ |
| H5 rappel fin de session | Rappel `retro` / `optimisation` avant `/clear` ou après plus de cinq échanges | ❌ |

### 0b. Scripts et vues (remplacent les agents prévus)

| Outil | Remplace | Rôle | Statut |
|---|---|---|---|
| `pipelines/cartographe.py` | agent `cartographe` | Liste les L-nnn sans check dans une carte et les cartes manquantes par jeu ; je rédige les checks en session | ❌ |
| `pipelines/recette.py` étendu | agent `testeur` | Rejoue formats, hooks et vues gold de tous les jeux avant commit | ❌ |
| Vues gold `*_sante_collecte` | agent `sante-collecte` | Ce qui n'arrive plus ou arrive vide, une requête | ❌ |

### 0c. Extensions d'agents existants

| Agent | Extension | Statut |
|---|---|---|
| `academie` | Absorbe le recrutement (Hardwood : points, concurrents, 4 cibles + backups ; Hockey Nation : draft et scouting) + carte « recrutement » | ❌ |
| `tactique` | Absorbe l'étude de l'adversaire, alimentée par une vue gold par jeu | ❌ |
| `finances-personnel` | Renommer en `finances`, mettre à jour CLAUDE.md et les fiches | ❌ |

### 0d. Retirer les agents qui ne font qu'un calcul (décidé le 2026-11-02, mesure optimisation : 40 agents/semaine, ~0,45 M éq. chacun)

Ne rien supprimer avant d'avoir migré les fiches par jeu (`docs/fiches/<jeu>/<agent>.md`) et mis à jour CLAUDE.md.

| Agent actuel | Devient | Statut |
|---|---|---|
| `effectif` | Vue gold bilan par poste + moi | ❌ |
| `lecteur-exports` | Vue gold « état des exports » + script | ❌ |
| `verificateur` | Supprimé, remplacé par `police` et les hooks H1-H3 | ❌ |
| `optimisation` | `pipelines/mesure_session.py` seul, sans agent | ❌ |
| `finances-personnel` | Vue gold + moi, renommé `finances` (cf. 0c) | ❌ |

Agents de jugement conservés (12 avec `finances` si avis gardé) : `match`, `tactique`, `transferts`, `entrainement`, `academie`, `veille` (delta seulement), `analyste`, `decideur`, `police`, `synthese`, `retro`.

**Plafond hebdomadaire : 20 agents par semaine**, hors `analyste` et `police` (la règle des trois par passage n'a pas tenu : 16 agents le 30/10). À écrire dans CLAUDE.md avec 0d. Autres coupes de la mesure : `/compact` à 30 %, `/clear` à chaque changement de jeu, SQL avec colonnes choisies et `LIMIT 30`.

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
- 2026-11-02 : mesure optimisation (53 sessions, semaine 29/10-01/11 = 59,3 M éq., pic 30-31/10 = 36,5 M) ; étape 0d ajoutée : retrait de 5 agents-calcul et plafond de 20 agents par semaine.

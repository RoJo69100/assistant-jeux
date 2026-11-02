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

## Étape 0 : nouveaux agents (à créer AVANT les cartes des jeux, décidé le 2026-11-02)

| Agent | Rôle | Statut |
|---|---|---|
| `cartographe` | Relit `learnings.md` et les briefs après chaque cycle, transforme chaque L-nnn en check dans la carte du bon type de décision, signale les cartes manquantes. Rend la conception reproductible pour les 5 autres jeux. | ❌ à créer en premier |
| `recrutement` | Recrues Hardwood (points, concurrents, 4 cibles + backups) et scouting/draft Hockey Nation ; soulage `academie`. | ❌ |
| `adversaire` | Étude d'un adversaire (tactique lue, forces, faiblesses) en un seul endroit, au lieu de `match` + `tactique`. | ❌ |
| `testeur` | Rejoue formats de rendu, hooks (`forme.py`, `police.py`) et vues gold de chaque jeu après une modification ; étend `recette.py` à tous les jeux. | ❌ |
| `sante-collecte` | Repère ce qui n'arrive plus ou arrive vide (userscript cassé par un changement du site). | ❌ |
| Renommage `finances-personnel` en `finances` | Le nom ne doit pas lier l'agent à BasketVibe ; mettre à jour CLAUDE.md et les fiches. | ❌ |

Une fois créés, ils s'ajoutent à la liste des agents de CLAUDE.md (même commit) et au tableau ci-dessous si leur absence bloque un jeu.

## Ordre
0. Nouveaux agents (tableau ci-dessus), `cartographe` d'abord
1. Hockey Nation (jeu modèle, learnings riche) : cartes échange, draft, lignes, coachs, finances, défaite
2. Team Soccer
3. Six Zero League
4. Derby Manager (créer d'abord learnings.md)
5. Hardwood (créer d'abord learnings.md)

## Journal
- 2026-11-02 : plan créé, aucun jeu commencé.
- 2026-11-02 : étape 0 ajoutée (5 agents + renommage `finances`), à faire avant les cartes de Hockey Nation.

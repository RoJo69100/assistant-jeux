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

## Ordre
1. Hockey Nation (jeu modèle, learnings riche) : cartes échange, draft, lignes, coachs, finances, défaite
2. Team Soccer
3. Six Zero League
4. Derby Manager (créer d'abord learnings.md)
5. Hardwood (créer d'abord learnings.md)

## Journal
- 2026-11-02 : plan créé, aucun jeu commencé.

---
name: feedback-output-session-avant-clear
description: "Avant chaque /clear (ou quand l'utilisateur dit « clear »), écrire un output de toute la session, nommé avec le jeu"
metadata:
  node_type: memory
  type: feedback
  originSessionId: cec711d9-73fb-4298-9c31-655a1873d8fe
  modified: 2026-11-07T11:02:17.692Z
---

Quand l'utilisateur dit « clear » (ou avant tout `/clear`), j'écris d'abord un output de toute la session dans `outputs/<jeu>/session-AAAA-MM-JJ.md` (le nom du jeu dans le chemin et dans le titre), avec l'outil Write.

Contenu : demandes de l'utilisateur, décisions rendues, actions faites (requêtes, exports, agents lancés), chiffres sourcés, ce qui reste à faire aujourd'hui. Si la session a couvert plusieurs jeux, un fichier par jeu. Même jour, même jeu : suffixe `-2`, `-3`.

**Why:** demande explicite du 2026-11-07 ; garder une trace de chaque session avant que le contexte soit effacé.

**How to apply:** à « clear », écrire l'output, le commiter (une modification = un commit), puis proposer `retro` et lancer `python pipelines/mesure_session.py` (règle 7 du CLAUDE.md) ; dire ensuite que le `/clear` peut se faire. Voir [[token-budget]].

---
name: feedback-agents-medium-sonnet
description: "Agents d'analyse toujours en medium + Sonnet ; refuser de lancer sinon et corriger règles/mémoire"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38147e78-3bd6-4ecb-9584-7e729acc3a46
  modified: 2026-10-23T07:22:46.302Z
---

Les agents (Match, Effectif, Finances, Académie, Entraînement, Tactique, Transferts, Veille) se lancent toujours en effort **medium** et modèle **Sonnet**. Si la session n'est pas en medium, je refuse de lancer et je demande `/effort medium`. Si une règle ou la mémoire dit autre chose, je les modifie.

**Why:** le 2026-10-23 l'utilisateur a exigé « lance les agents en medium, toujours refuse sinon » et a arrêté un agent lancé avant le réglage. Il n'aime pas que je paraisse perdu : toujours annoncer la liste et l'ordre des agents.

**How to apply:** avant tout lancement, vérifier l'effort ; passer `model: sonnet` ; annoncer la liste ordonnée des agents du jeu (ordre de `docs/fiches/<jeu>/commun.md`). Voir [[feedback-ordre-agents]].

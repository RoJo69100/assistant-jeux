---
name: project-conception-vues-entrainement-prix
description: "Conception demandée le 2026-11-04 : vue gold contrôle d'entraînement (attendu vs saisi) et table de référence des prix de transferts mise à jour par delta, au lieu d'agents"
metadata:
  node_type: memory
  type: project
  originSessionId: 1349cf40-c103-4a2f-a8b3-48d6be97b1ec
  modified: 2026-11-04T19:48:02.661Z
---

Backlog détaillé dans `docs/conception-a-faire.md`.

L'utilisateur a reproché (2026-11-04, SixZero League) que je lance des agents et lui fasse tout redemander pour l'entraînement et les transferts. Il veut : (1) une vue qui compare focus attendu et focus saisi, rien à faire si identique ; (2) une table de prix de référence par poste/âge/note, mise à jour par delta à chaque export.

**Why:** coût en tokens et en patience ; ses données de base suffisent à décider, un agent n'est justifié qu'une fois par semaine ou pour un cas non tranché.
**How to apply:** avant de lancer un agent entraînement/transferts, vérifier si la vue existe ; sinon proposer cette conception (`/model opus`). Lié à [[feedback-effectif-questions-vue-gold-systematique]].

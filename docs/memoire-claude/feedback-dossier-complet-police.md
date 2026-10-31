---
name: feedback-dossier-complet-police
description: "Décision importante = dossier compilé (pipelines/dossier.py), grille docs/decisions/variables.md, agent police, hook qui bloque « pas tout lu » (2026-10-31)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3b2ef9ba-00fc-43a0-b4ef-79342b314a61
  modified: 2026-10-31T12:18:37.460Z
---

Avant toute décision importante (achat, vente, compo de ligue/coupe, défaite, entraînement, académie, finances), tout lire : règles + avis des amis (connaissance, Discord, chat) + chiffres de toute la saison. Jamais « je n'ai pas tout lu, il me manquait des données ».

**Why:** l'utilisateur, 2026-10-31 : « si tu as des données tu dois les exploiter… prendre les MEILLEURES DÉCISIONS avec la mine d'or que sont les règles et l'avis des amis, et l'étude des chiffres ».

**How to apply:** `python pipelines/dossier.py <jeu> <type> --mots "…"` → lecture intégrale → grille de variables + tableau Couverture → agent `police` (complète lui-même) → `synthese`. Le hook Stop/SubagentStop `pipelines/police.py` bloque les aveux de lecture partielle. Voir [[feedback-effectif-questions-vue-gold-systematique]].

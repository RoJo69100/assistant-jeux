---
name: feedback-seulement-ce-qui-est-possible
description: "Règle d'or — dire quoi faire seulement quand c'est possible maintenant ; exception transferts (cible, suivi d'enchère) (2026-11-01)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88eaa6d4-19df-4366-83a2-3bd5cb045d6c
  modified: 2026-11-01T07:24:02.869Z
---

Règle d'or : ne lister que les actions **faisables à l'instant** (export déjà possible, tactique d'un match dont le précédent est joué, entraînement). Rien « pour plus tard ».

**Exception : les transferts** — trouver une cible et suivre une enchère se disent toujours, même si l'action concrète vient plus tard.

**Why:** le 2026-11-01 (Six Zero League), mon tableau mélangeait export de J1 non joué, tactique de J2 impossible avant J1 et tactique de J3 ; il n'a retenu que l'entraînement et les exports Équipe/Transferts : « les autres infos sont pour plus tard ».

**How to apply:** avant de rendre un plan, retirer toute ligne dont la condition n'est pas remplie (match non joué, export pas encore possible). Tactique de Jn seulement après J(n-1) joué. Voir [[feedback-horizon-aujourdhui-demain]].

---
name: feedback-confirmer-exports-en-tableau
description: "Quand l'utilisateur dit ce qu'il a fait/exporté, répondre par un tableau « fait / vérifié / reste », puis lancer les agents si les exports suffisent"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38147e78-3bd6-4ecb-9584-7e729acc3a46
  modified: 2026-10-23T13:00:59.269Z
---

Quand l'utilisateur écrit « j'ai fait X, Y, Z » (exports, réglages), je réponds par un **tableau** : une ligne par chose faite, avec la preuve en base (page, club, heure) et le statut ; puis un bloc « Reste à faire ». Si les exports voulus sont là, je lance directement les agents dans l'ordre, sans redemander.

**Why:** le 2026-10-23, l'utilisateur a validé le tableau « exports à faire » pour Team Soccer comme le bon format : « c'est comme ça qu'on doit faire un tableau, je te dis j'ai fait ça et tu donnes en réponse un tableau avec les choses faites ».

**How to apply:** une requête `bronze.raw_pages` (jeu, `page_type`, `captured_at`) avant de répondre ; noter aussi dans `outputs/<jeu>/fait-AAAA-MM-JJ.md`. Voir [[feedback-ne-pas-redemander]] et [[feedback-resultats-en-tableau]].

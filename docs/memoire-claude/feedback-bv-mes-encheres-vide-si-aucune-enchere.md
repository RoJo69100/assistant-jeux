---
name: feedback-bv-mes-encheres-vide-si-aucune-enchere
description: "BasketVibe : ne pas redemander l'export « Mes enchères » quand aucune enchère n'a été placée (2026-11-08)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: eece216f-10e9-44e9-972d-13b5f5925a27
  modified: 2026-11-08T10:13:11.444Z
---

Ne pas demander l'export « Mes enchères » en BasketVibe quand l'utilisateur n'a placé aucune enchère : la page est vide et l'userscript ne l'envoie pas, donc l'écran reste « à refaire » à tort.

**Why:** le 2026-11-08 j'ai redemandé cet export 4 fois de suite ; l'utilisateur : « tu me saoules avec mes enchères, on n'a pas fait d'enchère ». Il n'y avait rien à exporter.

**How to apply:** avant de mettre « Mes enchères » en ligne Export, vérifier s'il y a une enchère d'achat en cours (brief transferts, `gold.bv_market_bargains`, ou la dernière page reçue). Sans enchère, ne pas écrire la ligne et ignorer ce « à refaire » (une demi-ligne dans le commentaire au plus). Voir [[feedback-bv-que-faire-complet-reference]].

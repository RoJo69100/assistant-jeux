---
name: feedback-bv-preview-ligue-toujours
description: "BasketVibe ligue — toujours demander l'export de l'aperçu (Preview) du prochain match de ligue avant la saisie ; il est visible dès J-2"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-05T13:30:00Z
---

Avant toute saisie d'un match de ligue (ou de coupe) BasketVibe, je demande **toujours** l'export de l'aperçu (Preview) de ce match, même si je connais l'adversaire par des confrontations passées. L'aperçu est visible au moins deux jours avant (confirmé le 2026-11-05 pour la J3 du 07/11). Amicaux : jamais de Preview ([[feedback-bv-amical-sans-preview]]).

**Why:** le 2026-11-05, j'ai rendu la fiche contre Póvoa avec les 14 noms des matchs de septembre et octobre, sans demander l'aperçu ; l'effectif adverse peut avoir changé et l'ordre de l'écran diffère.

**How to apply:** si `gold.bv_saisie_adversaires` n'a aucune ligne pour le prochain match de ligue, la première ligne du plan est « Exporte l'aperçu du match contre X » ; la fiche adversaires n'est rendue qu'après cet export.

---
name: project-hook-forme-formats
description: Hook Stop pipelines/forme.py contrôle tous les formats de rendu (plan, entraînement, tactique, adversaires, Hardwood, Team Soccer, HN) ; test pipelines/test_forme.py
metadata:
  type: project
---

Le hook Stop `pipelines/forme.py` (avec `police.py`) bloque toute réponse dont un tableau sort du format validé. Entraînement BasketVibe : joueurs dans l'ordre de l'export (`gold.bv_saisie_entrainement`, cache `docs/ordre-export/basketvibe-entrainement.json`) avec leur entraînement, ou seulement ceux qui changent (Joueur | Actuel | À mettre).

**Why:** 2026-10-31, l'utilisateur veut « TOUJOURS la même forme » et jamais « pas tout lu » ; le contrôle doit être automatique (hook), pas dépendre de moi.
**How to apply:** après une nouvelle export d'entraînement, mettre à jour le cache d'ordre ; ajouter tout nouveau format dans `forme.py` + un cas dans `pipelines/test_forme.py`. Voir [[feedback-format-tactique-parfait]], [[feedback-dossier-complet-police]].

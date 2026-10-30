---
name: project-derbymanager
description: "Derby Manager (6e jeu, football) — conçu le 30/10 : 2 clubs QoS 547 / Marmandes 307, vues dm_*, veille Discord complète ; Marmandes jamais exporté"
metadata:
  node_type: memory
  type: project
  originSessionId: f07efc27-6d3a-4d49-8734-08e8a50d484e
  modified: 2026-10-30T21:42:40.390Z
---

Derby Manager conçu le 2026-10-30 : userscript `userscripts/derbymanager.user.js`, silver/gold `dm_*` (sql 047-050), veille Discord intégrale (125 932 messages) → `outputs/derbymanager/veille/connaissance.md` + skills `derbymanager-regles|tactique|effectif-entrainement|club`, fiche `docs/fiches/derbymanager/resume.md`, checklist `docs/checklist-derbymanager.md` (périmètre `docs/chose-a-DM.txt`).

Deux clubs à toujours séparer : 547 Queen of the South (Écosse D1, 8 équipes, pas de relégation) et 307 Marmandes (France D4).

**Why:** au 30/10, seul Queen of the South est exporté (fin de saison 26 : 1 V en 28 matchs, 20,4 M en caisse) ; Marmandes = zéro export. Le marché exporté était filtré à ≤ 7,5 M.

**How to apply:** à la reprise, vérifier `gold.dm_exports_etat` ; demander d'abord les exports de Marmandes et le marché 8-20 M. Plan du 30/10 dans `outputs/derbymanager/briefs/2026-10-30-plan.md` (541 défensive, Vigerie GK, Almgren promu). `gold.dm_marche_postes` est défectueuse (suppression en attente de confirmation) : lire `gold.dm_marche_notes`. Voir [[feedback-hockeynation-modele-reference]].

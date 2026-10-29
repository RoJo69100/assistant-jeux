---
name: feedback-hockeynation-rendu-tableaux
description: "Hockey Nation — rendu obligatoire en tableaux par équipe, scouts avec joueurs listés dans une colonne, règles coachs U17/U21 par expérience"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e9f79813-9a90-4327-8302-c94389b83069
  modified: 2026-10-29T15:37:41.269Z
---

À « on fait quoi Hockey Nation » : (1) un tableau par équipe, jamais de puces, liste complète puis 20 titulaires ; (2) tableau scouts `gold.hn_scout_liste` avec les joueurs à repérer écrits dans des colonnes (top poste+nation, poste, nation), jamais « pour voir la liste, requête X » ; (3) coachs : U21 note ≤ 69 et xp ≤ 7, U17 note ≤ 54 et xp ≤ 4 avec 2 talents forts de match et grande marge ; un coach arrivé par offre cette saison ne se remplace pas ; (4) Carpentier et Jasiński ne bougent pas.

**Why:** colères du 2026-10-29 (puces au lieu de tableaux, Carpentier déplacé, Vrábel proposé en U21, « pour voir la liste »). L'utilisateur a validé les choix de coachs (« tu as tout compris, grave ça dans le marbre »).
**How to apply:** charger `docs/fiches/hockeynation/resume.md`, interroger les vues gold, afficher le contenu au lieu de renvoyer à la vue. Voir [[project-hockeynation-cap-s27]].

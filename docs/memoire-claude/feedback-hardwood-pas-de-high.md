---
name: feedback-hardwood-pas-de-high
description: Hardwood recrues — ne jamais afficher ni utiliser le niveau High des concurrents (colonne, verdict, commentaire)
metadata:
  type: feedback
---

Dans tout tableau ou verdict de recrues Hardwood, aucune colonne « High », `teams_high` ni mention du niveau High des concurrents. Seul le nombre d'équipes intéressées peut figurer.

**Why:** décision déjà prise et commitée (da6757e, « le niveau High des concurrents n'entre plus dans le verdict »). Je l'ai réaffiché le 2026-10-30 et l'utilisateur s'est fâché : « on a dit d'enlever les High, comment tu as pu oublier ça direct ».

**How to apply:** avant de rendre un tableau recrues, ne choisir que les colonnes utiles hors `teams_high`. Les recrues déjà engagées (`engage_tot`) sortent de la liste. Voir [[project-hardwood]] et [[feedback-hardwood-notes-competences-cles]].

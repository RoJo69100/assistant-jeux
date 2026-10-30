---
name: project-derbymanager-reprise-31-10
description: "Derby Manager : à creuser le 31/10 — pourquoi la condition ne remonte pas, ce qui reste à faire, tout le contexte dans un brief"
metadata:
  node_type: memory
  type: project
  originSessionId: f07efc27-6d3a-4d49-8734-08e8a50d484e
  modified: 2026-10-30T22:59:45.958Z
---

Demande de l'utilisateur le 2026-10-30 : « garde tout, on creuse demain ». Tout le détail (explications des codes SUB/CON/FRM/SHA/BU/PBU/POT/FIT/EXP/TR, scouting 3/jour max 20, vieux joueurs, plan Queen of the South, manques) est dans `outputs/derbymanager/briefs/2026-10-30-reprise-demain.md`.

**Why:** l'utilisateur dit qu'il n'arrive pas à faire remonter la condition malgré une rotation constante de l'équipe. En base, la condition est 83-100 % ; ce qui est bas est la **forme** (Bjerg 13, Kjer 21, Vigerie 26…). Hypothèse : il parle de la forme, et la rotation permanente l'empêche de monter (elle ne monte qu'en jouant). Il veut que je comprenne ce point de mon côté, même s'il ne le comprend pas.

**How to apply:** à la reprise, commencer par ce point : lui demander quelle colonne et quels joueurs, chercher dans `connaissance.md` et Discord le gain de forme/condition par match, répondre colonne par colonne. Puis : exports Marmandes (rien reçu), marché 8-20 M, pages adversaires, calendrier saison 27. Accord attendu pour supprimer `gold.dm_marche_postes` et `gold.dm_joueurs`. Conception SQL = rappeler `/model opus`. Voir [[project-derbymanager]].

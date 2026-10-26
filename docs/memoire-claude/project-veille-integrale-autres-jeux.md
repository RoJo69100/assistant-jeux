---
name: project-veille-integrale-autres-jeux
description: Tâche ouverte — refaire pour chaque autre jeu la veille intégrale Discord/chat (connaissance.md) faite sur Six Zero League le 2026-10-26
metadata:
  node_type: memory
  type: project
  originSessionId: 70822101-162c-4afd-bbda-630e631005f4
  modified: 2026-10-26T19:42:28.725Z
---

Six Zero League a eu le 2026-10-26 une lecture intégrale de toutes ses sources (Discord, `data/chat/`, chat en base, wiki) qui produit `outputs/sixzeroleague/veille/connaissance.md` (index par thème, source, date, auteur, statut confirmé / complété / contredit / en doute). Les autres jeux n'ont pas encore ça.

**Why:** les agents écrivaient « aucune source » alors que l'info était dans le Discord ou le chat (effet des tactiques, niveaux d'infrastructures des autres clubs). L'utilisateur : « c'est une mine d'or toutes ces informations ». Règle dans `CLAUDE.md` (« Connaissance Discord / chat »). [[feedback-defaites-agir-fort]]

**How to apply:** pour chaque jeu, un jeu par session, en medium + Sonnet : BasketVibe (`data/discord/basketvibe/`), Team Soccer, Hockey Nation, puis les autres de `docs/jeux.md` quand ils sont intégrés. Lancer l'agent `veille` en lecture intégrale avec la même consigne que pour Six Zero League (voir `outputs/sixzeroleague/veille/connaissance.md` comme modèle), vérifier l'existence de `docs/fiches/<jeu>/veille.md`, puis ajouter la règle « connaissance.md tenu à jour à chaque export ». Ensuite, à chaque nouvel export Discord/chat d'un jeu : veille sur le delta qui met à jour `connaissance.md`. Rappeler cette tâche à l'utilisateur quand il change de jeu.

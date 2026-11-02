---
name: feedback-calendrier-frais-avant-plan
description: "Avant tout « que faire », contrôler la fraîcheur et le statut du calendrier (silver.*_schedule), jamais l'agenda gold seul ; forfait = rien à exporter (2026-11-02)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9aba78ef-2a92-4600-a53e-63ace3c33be0
  modified: 2026-11-02T07:29:55.823Z
---

Le 2026-11-02, Six Zero League : j'ai rendu un plan depuis `gold.sz_agenda` alors que le calendrier datait du 31/10 (J2 « jouée », J3/J4/J5 listées). L'utilisateur : « tu me parles encore de choses que je peux pas faire aujourd'hui… je veux que ça ne se reproduise plus ».

**Why:** l'agenda gold est dérivé d'un calendrier exporté ; périmé, il fabrique des matchs joués et des actions impossibles (récidive de [[feedback-seulement-ce-qui-est-possible]]).

**How to apply:** avant tout plan du jour (tous jeux) : lire le calendrier lui-même (`status`, `kickoff_paris`, `captured_at`) ; plus de 12 h = seule ligne « exporte le calendrier ». Seul le prochain match à venir aujourd'hui se prépare. Victoire sur tapis vert = aucun export ni analyse de match. Règle 69 de `docs/retro/regles-apprises.md`, skill `sixzeroleague-aujourdhui` étape 0.

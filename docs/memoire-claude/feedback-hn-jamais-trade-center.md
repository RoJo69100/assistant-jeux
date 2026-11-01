---
name: feedback-hn-jamais-trade-center
description: Hockey Nation — ne jamais demander d'export Trade Center (offres ni recherche), ni les exports que l'utilisateur vient de faire ; lire resume.md et la base avant la liste d'exports
metadata:
  type: feedback
---

Hockey Nation (2026-11-01, colère : « je t'ai dit de NE PAS FAIRE TRADE CENTER on s'enfiche !!! ») : j'ai mis dans le plan « fais Trade Center > offres », « Trade Center > recherche », Classement, Training et Contract talks, alors que la consigne est écrite dans `docs/fiches/hockeynation/resume.md` (ligne 7) et que l'utilisateur avait déjà exporté Contract talks, l'évolution des joueurs et les coachs.

**Why:** il gère lui-même les échanges (Bélanger, centres) ; un export demandé pour rien l'énerve. `gold.hn_exports_state` dit « à refaire » selon l'âge, pas selon l'utilité (Classement : 0 changement).
**How to apply:** pour « que faire » sur Hockey Nation, relire `resume.md` (consignes [U]) avant la liste d'exports ; ne jamais lister Trade Center ; ne demander un export que si la base ne contient pas déjà la donnée du jour (`bronze.raw_pages` des 3 dernières heures) ; une offre d'échange reçue est mentionnée en une ligne, sans demander l'export. Voir [[feedback-hockeynation-rendu-tableaux]].

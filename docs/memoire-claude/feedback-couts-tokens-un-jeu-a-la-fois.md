---
name: couts-tokens-un-jeu-a-la-fois
description: "Le 2026-10-24, ~25 agents et ~2 millions de tokens pour 3 jeux ; règles de coût validées (déclencheur par nouveauté, plan en SQL, un jeu par session, briefs plafonnés)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3e03971f-6253-493c-bd76-f7ce89dde4b9
  modified: 2026-10-24T21:13:14.079Z
---

L'utilisateur a jugé « une honte » la consommation de tokens du 2026-10-24 (chaîne complète d'agents sur 3 jeux d'un coup, 12+ retours à la suite, rien d'actionnable clair) et s'inquiète du passage à ~25 jeux.

**Why:** il veut avancer « petit à petit » : peu d'infos à la fois, des décisions claires, pas de redemandes (le preset, le transfert) et pas de rafale d'agents. Voir [[feedback-synthese-precise-par-jeu]].

**How to apply:**
- Un agent seulement si un export plus récent que son brief est arrivé ; le plan du jour vient de `gold.*_agenda` + registre `fait-…`, sans agent.
- Un jeu par session (`/clear` entre deux jeux), tableau rendu avant de passer au suivant ; jamais plusieurs jeux d'agents en parallèle sans demande.
- Briefs d'une page, résumés d'agent de 10 lignes, delta du jour seulement.
- `lecteur-exports` en premier (SQL, détection des nouveautés), pour qu'aucun agent ne déclare « absent » une donnée déjà exportée ([[feedback-ne-pas-redemander]]).
- Règles 12 à 16 de CLAUDE.md.

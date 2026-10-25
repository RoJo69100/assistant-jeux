---
name: synthese-precise-par-jeu
description: "Rendu final = synthèse par jeu en tableaux catégorisés, saisies poste par poste, analyses détaillées des défaites, leviers de transfert proactifs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3e03971f-6253-493c-bd76-f7ce89dde4b9
  modified: 2026-10-24T20:45:20.397Z
---

L'utilisateur veut, après les agents, uniquement l'important : changements (composition, entraînement, transfert, académie), analyses, questions. Un tableau par jeu (jamais mélangés), priorité 🟥🟧🟩 + catégorie fixe (Composition, Tactique, Entraînement, Transferts, Académie/Draft, Finances, Export, Question, Analyse).

**Why:** le 2026-10-24 j'ai rendu un plan « fouillis » de 30 lignes, sans détail des postes, avec des lignes « rien à faire », un résultat de match mal lu (J12 annoncé gagné), des transferts non proposés pour améliorer l'équipe, et j'ai oublié que ses choix de draft Hockey Nation forment l'équipe U17 à montrer. Il a écrit « qu'est-ce que tu fous ».

**How to apply:**
- « Saisis l'équipe » ne suffit jamais : chaque poste, chaque joueur nommé, chaque consigne/focus/minute à appliquer ([[feedback-aucun-flou-noms-et-donnees]]).
- Défaite = analyse chiffrée détaillée + points d'amélioration nommés ; pas de résumé court.
- Volet « leviers » (achat/vente/recrutement nommés, prix) dans chaque rapport ; ne pas piétiner.
- Lire le résultat via `my_result`/`is_mine`, jamais le score brut.
- Hockey Nation : tout ajout de joueurs → montrer l'équipe résultante (20, talents vs poste).
- Règle écrite dans CLAUDE.md (« Règles universelles de rendu ») ; agent `synthese` pour la mise en forme. Voir [[feedback-resultats-en-tableau]], [[feedback-couleurs-et-deux-clubs]].

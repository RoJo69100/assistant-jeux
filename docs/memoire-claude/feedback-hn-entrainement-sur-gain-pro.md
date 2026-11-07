---
name: feedback-hn-entrainement-sur-gain-pro
description: "Hockey Nation — entraînement : ne proposer un changement que si l'export Training montre qu'un joueur PRO vient de gagner une caractéristique ; sinon aucune ligne entraînement"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3cbbcf3c-9549-42c3-ac03-8b13a5b95bf3
  modified: 2026-11-07T22:07:58.794Z
---

Hockey Nation, bloc 5 (entraînement) : je ne propose rien par défaut. L'utilisateur exporte le journal Training ; je regarde seulement si un joueur **PRO** a augmenté une caractéristique depuis le relevé précédent. Si oui → action d'entraînement pour ce joueur (compétence ouverte suivante, coach). Si non → aucune ligne entraînement.

Tactique PRO : elle ne change qu'après l'analyse des matchs (déclencheurs de la charte), pas à chaque passage.

**Why:** dit le 2026-11-07 (« quand tu vois un pro qui augmente une caractéristique tu peux faire un truc pour entraînement, sinon non »).
**How to apply:** dans `hockeynation-aujourdhui`, bloc 5 = comparaison du journal Training au précédent pour le PRO uniquement ; pas de tableaux d'ordre de choix pour les 4 équipes sauf demande. Voir [[feedback-hn-matchs-scouts-pas-finances]].

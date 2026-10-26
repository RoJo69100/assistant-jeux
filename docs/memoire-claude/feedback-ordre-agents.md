---
name: feedback-ordre-agents
description: "L'ordre de lancement des agents est ma responsabilité ; ne jamais livrer de retours incomplets, relancer l'agent concerné"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ce17fb8e-d89d-4645-b4c1-57e8994acdc1
  modified: 2026-10-22T13:44:03.643Z
---

L'utilisateur veut des retours d'agents complets. Je dois comprendre les dépendances entre agents, choisir l'ordre moi-même et le corriger si je me trompe (relancer l'agent dont le retour est incomplet avec les briefs du jour des autres).

**Why:** le 2026-10-22, Transferts et Finances ont été lancés en parallèle ; Transferts a rendu « salaires de Dang et Albano non relevés » et « aucun brief tactique postérieur au 18/10 », alors que Finances et Tactique les avaient. L'utilisateur n'accepte pas ces trous.

**How to apply:** ordre BasketVibe : Match, Effectif, Finances-personnel, Académie, Tactique, puis Transferts (il lit rotation et finances). Ne lancer en parallèle que des agents sans dépendance. Donner à chaque agent les briefs du jour des agents précédents. Si un retour dit « non relevé » ou « non lu », relancer avant de conclure. Voir [[feedback-pas-de-temporalite]].

---
name: feedback-pas-de-temporalite
description: "Ne pas dire « ce soir » ni donner d'heures : parler en actions à faire maintenant, par jour"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ce17fb8e-d89d-4645-b4c1-57e8994acdc1
  modified: 2026-10-24T08:09:47.162Z
---

Quand l'utilisateur demande « que faire aujourd'hui », il agit maintenant : lister les actions du jour sans « ce soir », sans horaires. Les actions journalières (amicaux, exports) se font avant les matchs ; dire « après un match » seulement quand c'est une vraie dépendance. Les amicaux BasketVibe ont lieu TOUS LES JOURS : vérifier tous les exports.

**Why:** correction explicite de l'utilisateur le 2026-10-22 (avait contredit la règle « après 19h » de CLAUDE.md pour ce cas).

**Précision du 2026-10-24 :** ne jamais lister une action qui dépend d'un événement futur (match, draft, export « après le match ») ni écrire « demain / ce soir ». Une action « après l'événement » n'est annoncée qu'une fois l'événement passé. Seules les actions faisables maintenant (composition, transfert, réglage, export d'un événement déjà passé) sont listées. Un match prévu dans la journée, avec compo déjà faite = « rien à faire ».

**How to apply:** ne pas écrire « ce soir » ; vérifier l'arrivée des exports en base avant de répondre. Voir [[feedback-ordre-agents]].

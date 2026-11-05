---
name: feedback-bv-que-faire-complet-reference
description: "Le « que faire » BasketVibe complet du 2026-11-05 est la référence : à rejouer tel quel à chaque test, puis à étendre aux autres jeux"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-05T14:00:00Z
---

Quand l'utilisateur me demande un tour de test (« lance un tour pour <jeu> »), le « que faire » doit être aussi complet que celui de BasketVibe du 2026-11-05, **sans qu'il ait à poser les questions** :
1. `deja-fait` d'abord, puis agenda, alertes et `gold.bv_exports_state` dans le même tour ; chaque export « à refaire » = une ligne Export.
2. Aperçu du prochain match de ligue/coupe demandé s'il n'est pas en base ([[feedback-bv-preview-ligue-toujours]]).
3. Historique global des transferts demandé depuis la dernière vente connue, puis Marché et Mes enchères → bonnes affaires par requête, sans agent.
4. Bilan du club par vues gold : finances (solde, résultat hebdo, % salaires, projection), effectif (poste le plus faible, âge, note d'équipe contre la ligue), personnel, entraînement le samedi → une décision tranchée par secteur.
5. Défaite de ligue/coupe → `analyste` ; amical perdu = test jugé à son échéance (arbitrage 15).
6. Saisie complète du prochain match, décision au journal (`decision.py new`, ou connecteur si le port 5432 est bloqué en cloud).
Méthode écrite dans `.claude/skills/basketvibe-aujourdhui/SKILL.md` (étapes 0 à 6).

**Why:** le 2026-11-05, l'utilisateur a dû poser chaque question (preview, transferts, finances, effectif) pour obtenir ce qu'il attendait seul ; « tu fais exactement ce que j'aimerais que tu fasses tout seul ».

**How to apply:** pour BasketVibe, suivre le skill. Pour un autre jeu, appliquer les mêmes six points avec ses vues gold, dans une session dédiée à ce jeu ; dire ce qui manque (vue absente) au lieu de le sauter.

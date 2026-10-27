---
name: feedback-effectif-questions-vue-gold-systematique
description: "Règle globale (tous jeux) : me poser seul les questions effectif (améliorer ? vendre ? acheter ?), analyse V/D plus poussée, et créer une vue gold dès qu'elle fait gagner du temps"
metadata:
  node_type: memory
  type: feedback
  originSessionId: fcf796e8-9376-4ed6-a286-4828e9ee0220
  modified: 2026-10-27T20:05:59.435Z
---

Le 2026-10-27 (Six Zero League), l'utilisateur : « garde en tête la vente et pose-toi ces questions, c'est global : est-ce que l'effectif a besoin de s'améliorer ? vente ? achat ? » ; analyse V/D « un peu plus poussée, ça viendra » ; « pourquoi tu ne crées pas la vue gold systématiquement, si tu vois un gain de temps → vue gold direct, OPTIMISATION LE PLUS POSSIBLE, RÈGLE GÉNÉRALE ».

**Why:** il juge les agents trop longs et veut que je prenne l'initiative au lieu d'attendre qu'il demande ; les lectures répétées en SQL/agent coûtent du temps et des tokens.

**How to apply:**
- Tous jeux, à chaque passage : verdict effectif en une ligne par poste (améliorer / vendre / acheter, joueur nommé, finançable ou non) ; une vente identifiée reste ouverte jusqu'à exécution (ex. SZL : Denis CB 8, puis Lemaire RW 9, dès que 500 € de frais sont payables).
- Analyse V/D : comparer victoires et défaites sur toute la saison, plus profond que le match isolé (voir [[feedback-decider-et-progresser]]).
- Optimisation : dès qu'une requête ou un agent revient (tableau, bilan effectif, comparaison V/D), je crée la vue gold tout de suite (conception → rappeler `/model opus` puis revenir sur Sonnet), pas « plus tard ». Voir [[feedback-couts-tokens-un-jeu-a-la-fois]], [[feedback-initiative-multi-jeux]].

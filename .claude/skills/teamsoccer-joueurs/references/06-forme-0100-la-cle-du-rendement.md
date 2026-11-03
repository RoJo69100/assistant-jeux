## Forme (0–100) — la clé du rendement
**Effet en match** [F:2026-06-27 Admin-Dev] : chaque action est multipliée par **0,70 + 0,30 × Forme / 100** (duels, tirs, passes, tacles ; pas le gardien sur penalty). Forme 100 → ×1,00 · 80 → ×0,94 · 60 → ×0,88 · 40 → ×0,82 · 30 → ×0,79. Effet dès la 1re minute : un joueur à 100 avec Forme 50 joue comme 85 [F:2026-08-28 Admin-Dev].
**Plafond et fatigue en match** (moteur v3, 2026-10-18) [F:2026-10-18 Admin-Dev] :
- La Forme d'avant-match fixe un plafond (Forme 60 → 88 %). Le joueur entre à 100 % de ce plafond, titulaire ou remplaçant.
- Toutes les 5 minutes jouées, son pourcentage baisse selon son **Endurance**. Sur 90 minutes : environ −9 points avec Forme 100, −16 avec Forme 60. Un remplaçant frais entre avec tout son plafond.
- Indicateur de force en direct à côté de chaque joueur dans le rapport v3.
**Évolution de la Forme** : seulement à l'entraînement hebdomadaire, jamais en match (officiel ou amical) [F:2026-06-30 Admin-Dev]. Table par intensité dans teamsoccer-entrainement. Minimum 30, maximum 100 ; un nouveau joueur commence à 85.
- **Fin de saison** : réponses contradictoires (« reste telle quelle » 2026-07-03 Admin-Dev ; « elle repart » 2026-09-14 PIPO68 ; « non, pas de remise à zéro » 2026-10-11 PIPO68). Dernière réponse : **pas de remise à zéro**. À vérifier au changement de saison avec nos exports.
- [Obs] Dans l'API `players`, `fitness` (0–100 : 98, 84, 46…) correspond vraisemblablement à la Forme, et `form` est un libellé (« Good », « 5 »). À confirmer avec la page Effectif.


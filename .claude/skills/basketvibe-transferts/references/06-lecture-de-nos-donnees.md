## Lecture de nos données
- `silver.bv_transfer_auctions` : joueurs vus sur le marché (compétences, PS, prix de départ et actuel, nombre d'enchères).
- `silver.bv_transfers` : transferts conclus (prix, âge, poste, clubs) issus de l'historique global, de la ligue et du club.
- [Obs 2026-10-16] Historique global : 1 231 transferts au total. On ne remonte pas le passé : on accumule chaque lundi (page 1 de l'historique global + marché). À terme, croiser `bv_transfer_auctions` (compétences) et `bv_transfers` (prix payé) sur `player_id` donnera la référence de prix.

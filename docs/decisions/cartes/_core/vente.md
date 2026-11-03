# Carte _core — vente (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta. Jamais de vente sans accord écrit de l'utilisateur (inviolable 2).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Effectif au poste | `select position, rang_poste, name, age, rating, salary, en_declin from gold.roster_bilan where game = :game order by position, rang_poste limit 40` | Remplaçant interne nommé et écart de niveau chiffré | `docs/decisions/variables.md` § vente |
| C2 | Bornes d'effectif | `select distinct team_id, effectif, blesses, effectif_min, effectif_max, alerte_effectif from gold.roster_bilan where game = :game limit 4` | Effectif min du jeu tenu après la vente | `core.game_params` |
| C3 | Mes ventes en cours | `select name, position, price, bids, ends_at at time zone 'Europe/Paris' as fin_paris from core.market_listing where game = :game and is_mine and (ends_at is null or ends_at > now()) order by ends_at limit 10` | Un joueur déjà en vente ne compte pas comme disponible | `gold.daily_alerts` (effectif_dispo) |
| C4 | Prix comparables | `select position, age, count(*) as n, round(avg(price)) as prix_moyen from core.market_listing where game = :game and price is not null and ends_at < now() group by 1, 2 order by 1, 2 limit 30` | Dernier prix vu, pas le prix final | `docs/attentes/jeux/<jeu>.yaml` core.market_listing |
| C5 | Âge de déclin | `select name, age, rating, age_declin from gold.roster_bilan where game = :game and en_declin order by age desc limit 15` | Déclin sourcé par jeu (`age_declin`) | `core.game_params` |
| C6 | Alertes | `select prio, domaine, alerte from gold.daily_alerts where game = :game and domaine in ('transferts', 'blessure', 'effectif') order by prio limit 10` | « Vente impossible » = pas de vente | `core.alert_rule` |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Chiffre lu dans un export périmé : le dire | `core.export_rule` |

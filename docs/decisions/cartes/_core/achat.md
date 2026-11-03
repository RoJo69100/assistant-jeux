# Carte _core — achat (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta. Jamais d'enchère sans accord écrit de l'utilisateur (inviolable 2).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Capacité d'investissement | `select as_of, balance, reserve, capacite_invest, cap_space, finances_age_days from gold.finance_health where game = :game` | Enchère max > `capacite_invest` moins les dépenses décidées (`fait-`) = cible abandonnée | `docs/regles/actives.md` E8 |
| C2 | Effectif au poste | `select position, rang_poste, name, age, rating, en_declin from gold.roster_bilan where game = :game order by position, rang_poste limit 40` | Gain mesuré contre le titulaire et le n° 2 du poste de la cible | `docs/decisions/variables.md` § achat |
| C3 | Bornes d'effectif | `select distinct team_id, effectif, effectif_min, effectif_max, alerte_effectif from gold.roster_bilan where game = :game limit 4` | Effectif max du jeu non dépassé après l'achat | `core.game_params` |
| C4 | Marché ouvert | `select name, position, age, rating, price, bids, ends_at at time zone 'Europe/Paris' as fin_paris from core.market_listing where game = :game and not is_mine and (ends_at is null or ends_at > now()) order by ends_at nulls last limit 20` | Relevé du marché de plus d'un jour = « exporte le marché » | `core.export_rule` |
| C5 | Prix comparables | `select position, age, count(*) as n, round(avg(price)) as prix_moyen, max(price) as prix_max from core.market_listing where game = :game and price is not null and ends_at < now() group by 1, 2 order by 1, 2 limit 30` | Dernier prix vu, pas le prix final (statut figé au dernier relevé) | `docs/attentes/jeux/<jeu>.yaml` core.market_listing |
| C6 | Alertes | `select prio, domaine, alerte from gold.daily_alerts where game = :game and domaine in ('transferts', 'finances', 'contrats') order by prio limit 10` | Vente ou achat impossible signalé = pas d'achat | `core.alert_rule` |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Chiffre lu dans un export périmé : le dire | `core.export_rule` |

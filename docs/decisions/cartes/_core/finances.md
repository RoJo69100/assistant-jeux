# Carte _core — finances (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta (variables propres, rendu figé, checks appris). Une variable du jeu qui répète une variable C ici renvoie à son numéro.

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Solde, charges, réserve, capacité | `select as_of, periode, balance, charges_periode, salaries, wage_cap, cap_space, reserve, capacite_invest, finances_age_days from gold.finance_health where game = :game` | Dépense ≤ `capacite_invest` moins les dépenses décidées du registre `fait-` ; capacité nulle (jeu sans trésorerie) : `cap_space` | `docs/regles/actives.md` E8 ; `core.game_params` `reserve_periodes` |
| C2 | Alertes d'argent | `select prio, domaine, alerte from gold.daily_alerts where game = :game and domaine in ('finances', 'contrats', 'transferts') order by prio limit 10` | Une alerte 🟥 passe avant toute dépense | `core.alert_rule` |
| C3 | Rang et points | `select team_label, rank, played, points, wins, losses, day from core.standing where game = :game and is_mine order by day desc limit 4` | Prime de classement et objectif de saison avant d'engager | `docs/decisions/variables.md` § finances |
| C4 | Série de résultats | `select day, competition_kind, my_result, my_score, opp_score, opponent from core.fixture where game = :game and my_result is not null order by day desc limit 5` | Résultat = `my_result`, jamais le score brut | CLAUDE.md, inviolable 4 |
| C5 | Masse salariale et effectif | `select distinct team_id, club_label, as_of, effectif, masse_salariale, effectif_min, effectif_max, alerte_effectif from gold.roster_bilan where game = :game limit 4` | Effectif dans les bornes du jeu après la dépense | `core.game_params` |
| C6 | Personnel | `select role, count(*) as n, sum(salary) as cout, max(day) as releve from core.staff where game = :game and day = (select max(day) from core.staff where game = :game) group by role order by role limit 15` | Relevé périmé (contrat core ❌ fraîcheur) = « exporte la page Personnel » avant de trancher | `pipelines/contrat_core.py` |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Chiffre lu dans un export périmé : le dire, ou demander l'export | `core.export_rule` |

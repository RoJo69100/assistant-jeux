# Carte _core — academie (tous jeux)

Cœur commun (refonte v2, 1.5) : variables lues dans les vues génériques, paramètre `:game`. `pipelines/dossier.py` remplace `:game`, lance chaque requête et remplit « Dernière valeur » ; la carte du jeu suit en delta (règles d'académie, draft ou recrutement propres au jeu).

## Variables
| # | Variable | Où la lire | Check | Source du check |
|---|---|---|---|---|
| C1 | Prospects récents | `select name, position, age, rating_min, rating_max, potential_min, potential_max, status, day from core.academy_prospect where game = :game and day >= current_date - 14 order by rating_max desc nulls last limit 20` | Potentiel non affiché = estimation du skill, avec sa confiance | `docs/attentes/jeux/<jeu>.yaml` core.academy_prospect |
| C2 | Besoin par poste | `select position, count(*) as n, max(rating) as meilleur, round(avg(age), 1) as age_moyen from gold.roster_bilan where game = :game group by 1 order by 1 limit 15` | Poste sans relève jeune = priorité | `docs/decisions/variables.md` § academie |
| C3 | Capacité d'investissement | `select as_of, balance, reserve, capacite_invest, cap_space from gold.finance_health where game = :game` | Test ou signature ≤ capacité moins dépenses décidées | `docs/regles/actives.md` E8 |
| C4 | Scouts et personnel | `select role, count(*) as n, max(day) as releve from core.staff where game = :game group by role order by role limit 15` | Relevé périmé : le dire | `pipelines/contrat_core.py` |
| C5 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = :game and statut <> '🟩 à jour' order by ordre limit 15` | Rapport d'académie périmé : « exporte » | `core.export_rule` |

## Couverture de `docs/decisions/variables.md` § academie
| Variable obligatoire | Où |
|---|---|
| Prospect : compétences, fourchettes, âge | C1 |
| Potentiel estimé | C1 si affiché ; sinon estimation du skill du jeu |
| Règles du jeu (coût, effet, probabilités) | skill académie / draft du jeu |
| Besoin de l'effectif par poste | C2 |
| Budget | C3 |
| Comparaison aux académies des autres clubs | carte du jeu |
| Recrutement Hardwood (taille, intérêt, points, offres) | carte Hardwood |
| Avis des amis, ce qui prouvera l'erreur | dossier et rendu |

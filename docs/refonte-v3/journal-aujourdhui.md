# Journal de `aujourdhui.py` (BasketVibe)

## Critères d'acceptation (écrits le 2026-11-06, avant le code ; le script doit produire le même « que faire » que le skill `basketvibe-aujourdhui`, en plus complet que les vues seules)

Jeu d'essai figé : `pipelines/jeu_essai/2026-11-06/` (copie des fichiers du 06/11). Test : `pipelines/test_aujourdhui.py` ; aucun commit de code tant qu'il n'est pas vert.

| # | Critère | Vérifié par |
|---|---|---|
| L1 | Brief tactique du jour (`briefs/<jour>-tactique.md`, `-tactique-amical.md`) : une ligne par match avec l'heure limite (verrou) et les tests « prouvera que j'avais tort ». Absent : le plus récent du même type. Plus de 3 jours pour un match du jour : la ligne le dit. | Plan 06/11 : Póvoa 19:45, Knight Jays 07:45 |
| L2 | Dossier d'achat (`dossier/<jour>-achat.md`) et `police-<jour>.md` : une ligne par cible avec montant maximum et heure limite (fin d'enchère en base). `police-<jour>.md` absent : la ligne dit « police d'abord ». | Plan 06/11 : Fujita 150 000, Stankevičius 100 000, police d'abord |
| L3 | Registre `fait-<jour>.md` : une ligne « reste à corriger / à faire » sort comme action (une par réglage), elle n'est pas seulement retirée. | Plan 06/11 : Knight Jays + 4 corrections d'écran |
| L4 | `learnings.md` : conseils ouverts dont l'échéance (date du critère) tombe aujourd'hui ou demain. | Fichier figé |
| F1 | Au plus 8 lignes, `HH:MM — action — détail (source)`, triées par heure limite (ce qui a une heure limite en tête), dernière ligne « Exports à faire aujourd'hui : … ». Le surplus va dans une ligne « Autres points ». Aucune ligne `clé=valeur`. | Sortie 06/11 |
| F2 | Le Personnel reste étiqueté Personnel. | Sortie 06/11 |
| D1 | Poste le plus faible : « acheter un <poste> de note ≥ X » ou « garder » en demi-ligne (jamais en ligne). Finances et transferts : même règle. Une règle absente de `docs/attentes/regles-decision-basketvibe.yaml` est marquée « (à valider) ». | Sortie 06/11 |

## Journal de durée (une ligne par exécution)

| Date | Jour du plan | Durée (s) | Requêtes |
|---|---|---|---|
| 2026-11-06 10:02 | aujourd'hui | 14.3 | 13 |
| 2026-11-06 10:02 | 2026-11-03 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-04 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-05 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-05 | 0.3 | 1 |
| 2026-11-06 10:29 | aujourd'hui | 30.0 | 13 |
| 2026-11-06 10:29 | aujourd'hui | 12.9 | 13 |
| 2026-11-06 14:45 | aujourd'hui | 17.6 | 13 |
| 2026-11-06 14:52 | aujourd'hui | 17.4 | 13 |
| 2026-11-06 15:18 | aujourd'hui | 13.4 | 12 |
| 2026-11-06 15:19 | aujourd'hui | 11.4 | 12 |
| 2026-11-06 15:19 | aujourd'hui | 11.1 | 12 |
| 2026-11-06 15:20 | aujourd'hui | 11.5 | 13 |

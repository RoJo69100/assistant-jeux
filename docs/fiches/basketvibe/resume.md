# BasketVibe — résumé pour les agents (remplace attentes.md + basketvibe.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md`, `docs/attentes/jeux/basketvibe.yaml` et `docs/fiches/basketvibe/commun.md`. N'ouvre ces trois fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces trois fichiers (2026-10-27).

## Jeu
- `basketvibe`, préfixe `bv_` (bronze `game = 'basketvibe'`). Un club : **Chomelix Cow** (senior). Ligue de 12. Heures affichées en Paris (`captured_at` est en UTC).
- Résultat d'un match = `my_result` / `is_mine`, jamais le score brut.
- **Connaissance par thème** (remplace la lecture en bloc de `connaissance*.md` et du skill `-communaute`) : `select public.kb_search('basketvibe', '<thème>', 0)` ou `python -I pipelines/kb.py basketvibe <thème>` (thèmes : `--domaines`) ; recopier le compteur « N total / N affichées ».
- Sources : `[M§x]` manuel > `[News date]` / `[Dev date]` > `[Com date, auteur]` (avis) > `[Obs]`. Connaissance : `outputs/basketvibe/veille/connaissance.md`, Discord `data/discord/basketvibe/`.

## Rythme et compétitions
| Quoi | Quand (Paris) | Saisie |
|---|---|---|
| Ligue | lun / mer / sam 20:00, verrou 19:45 ; saison 2 dès lun 02/11, moteur **v4** | oui, preset « League Tactic », à re-sélectionner sur chaque match planifié |
| Coupe | ex. 28/10 18:00 | oui, preset « League Tactic » (même id) |
| Amical | chaque jour 08:00, verrou 07:45, moteur v4 | composition de TEST complète (jamais le cinq de la coupe/ligue), réglages repris du dernier amical, **pas de preset**, adversaire sans importance (aucun aperçu à demander) ; un seul test à la fois (zone Rim/Middle/Perimeter ou un réglage de nos joueurs). Zone jouée : `gold.bv_zone_jouee` |
| Entraînement, salaires, personnel | dimanche 04:00 | réglages avant 04:00 |
| Rapport d'académie | jeudi 09:00 | — |
- Ligue ≠ amical : fatigue et expérience ≈ 1/10 en amical, pas de blessure [M§1.2]. Ne mélange pas v3 (ligue ≤ 26/10) et v4.

## Échelles de l'écran
- Consignes : écran 1–5 = données 0–4 (+1). Rôle 1 Passeur → 5 Scoreur ; Off. focus 1 Low → 5 Primary ; Tir 1 = 2 pts → 5 = 3 pts ; Agress. déf. 1 Soft → 5 Agressive.
- Focus défensif : 1 Give up, 2 Light, 3 Normal, 4 Intense, 5 Lock (export `off`). Zone : Rim / Middle / Perimeter (`area_step` 5 / 3 / 1, le 1 déduit) — **existe dans tous les matchs v4 : amical, coupe, ligue (confirmé le 2026-10-30)** ; toujours affichée avec le focus, une ligne par adversaire, ordre de l'export (par poste, alphabétique), jamais regroupée par valeur.
- Ordre de l'écran : par poste PG, SG, SF, PF, C, puis alphabétique (le JSON brut est alphabétique global : faux).
- Transferts : taxe 5 %, revente après 1 semaine, effectif minimum 8 (notre marge : 9).

## Vues prêtes (lis-les avant de calculer toi-même)
`gold.bv_agenda`, `gold.bv_daily_alerts`, `gold.bv_match_report`, `gold.bv_saisie_joueurs` + `gold.bv_saisie_adversaires` (tableaux de saisie R-10, `order by ordre`), `gold.bv_roster_now`, `gold.bv_slot_fit`, `gold.bv_fatigue_plan`, `gold.bv_next_opponents`, `gold.bv_league_top_players` (meilleurs adversaires croisés), `gold.bv_academy_chat` (chat sur l'académie : à lire après chaque export d'académie). Requêtes : colonnes choisies et `LIMIT`.
**Décision importante** : lis d'abord la carte `docs/decisions/cartes/basketvibe/<type>.md` (où lire chaque variable, check, rendu figé) ; couverture des demandes de l'utilisateur : `docs/couverture/basketvibe.md`.

## Détails
Attentes condensées (rendu, tactique R-10, amical, décider, coût), ordre des agents et pièges connus : `docs/fiches/basketvibe/resume-details.md`.

# BasketVibe — résumé pour les agents (remplace attentes.md + basketvibe.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md`, `docs/attentes/jeux/basketvibe.yaml` et `docs/fiches/basketvibe/commun.md`. N'ouvre ces trois fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces trois fichiers (2026-10-27).

## Jeu
- `basketvibe`, préfixe `bv_` (bronze `game = 'basketvibe'`). Un club : **Chomelix Cow** (senior). Ligue de 12. Heures affichées en Paris (`captured_at` est en UTC).
- Résultat d'un match = `my_result` / `is_mine`, jamais le score brut.
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

## Ordre des agents (tu lis les briefs du jour `outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille → Match → Effectif → Finances-personnel → Académie / Entraînement (parallèles) → Tactique (lit Match, Effectif, Entraînement) → Transferts (lit Effectif, Finances, Tactique, Académie). Un agent aval qui contredit un amont l'écrit en tête de son résumé.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`)
- **Rendu** : maintenant + demain seulement (R-1) ; des actions « fais X » avec joueur, valeur, heure limite (R-2) ; tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action (R-3) ; saisie complète dans l'ordre de l'écran (R-4) ; aucun « si », aucun seuil générique, donnée manquante = « il me manque X, fais l'export Y » (R-5) ; court (R-6) ; ne jamais redemander ce que `outputs/basketvibe/fait-AAAA-MM-JJ.md` ou la base prouvent (R-7) ; une décision, le doute en une demi-ligne avec ce qui prouvera l'erreur (R-8) ; tout chiffre vérifié en base (R-9).
- **Tactique (R-10)** : tableau joueur × quart-temps (Joueur, Poste, Q1–Q4, Prol., Min, Off. focus, Rôle, Tir, Agress.) + tableau adversaires (focus 1–5 ET zone), pour ligue, coupe et amical ; jamais « preset inchangé ».
- **Amical, tableau adversaires** : une ligne « les 12 : focus 3, zone X » (pas de noms). Tableau joueurs = format R-10 avec une composition de test ; la vue `gold.bv_saisie_joueurs` donne les réglages du dernier amical enregistré (lacune connue : pas d'export de tactique pour les amicaux du 28 et du 29/10).
- **Décider** : série de défaites = changement fort (A-1) ; défaite = analyse chiffrée joueur par joueur contre toute la saison (A-2) ; Finances dit quoi faire de l'argent (A-3) ; chaque rendu propose un achat / une vente nommé·e avec prix max, **jamais d'enchère ni de vente lancée sans accord** (A-4) ; nouveauté = test en amical (A-6) ; conseils suivis `C-nnn` → `L-nnn` dans `outputs/basketvibe/learnings.md`, deux échecs = conseil réécrit (A-7) ; retard mesuré contre les autres clubs (A-8) ; chercher dans toutes les sources avant « absent » (A-9).
- **Coût** : brief d'une page, résumé de 10 lignes, delta du jour seulement.

## Pièges connus
- Personnel médical : 85 000 au journal le 25/10 contre 60 000 affichés (à confirmer le 01/11).
- Page « academy » parfois en réalité la page finances (26/10).
- Options d'écran observées et non documentées : → source `commun.md` § Options observées (lecteur-exports seulement).
  Ajouts du 29/10 : moteur **v5 en amicaux seulement** (annonce du 28/10 : pas de 20 s mortes, tirs de fin de quart ; effet inconnu, mesure = points de Q4 des amicaux) ; compétences adverses de coupe en **fourchettes de 20 points** (`skill_brackets`) ; tactique de coupe enregistrable par match (`/cup-fixtures/<id>/match-tactics`, lue par silver depuis la migration 022) ; zone réellement jouée : `gold.bv_zone_jouee`.

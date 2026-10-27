# BasketVibe — fiche commune (tous les agents)

Les agents lisent d'abord `resume.md` (qui condense ce fichier) ; ils n'ouvrent celui-ci que pour une ligne « → source » (ex. Options observées). Toute modification ici se reporte dans `resume.md`.

## Identité
- Identifiant : `basketvibe` (bronze : `game = 'basketvibe'` ; vues `silver.bv_*`, `gold.bv_*`).
- Basket, ligue de 12 clubs. Club pilote du projet : les agents BasketVibe sont validés (checklist `docs/checklist-basketvibe.md`, partie E).

## Sources et codes de citation
- `[M§x]` manuel officiel (https://www.basketvibe.com/guide) > `[News date]` News de l'admin et `[Dev date, salon]` développeur sur Discord > `[Com date, auteur, salon]` communauté (avis, jamais une règle) > `[Obs]` nos observations.
- Skill de la communauté : `.claude/skills/basketvibe-communaute/SKILL.md`.

## Rythme
- Semaine du jeu = semaine réelle : matchs de ligue lun / mer / sam, entraînement et forme le dimanche (sauvegarder avant 04:00, Paris), rapport de l'académie le jeudi 09:00, salaires le dimanche (skill basketvibe-saison [M§1.3]).
- Un amical **chaque jour** (08:00, à domicile ou à l'extérieur) : chaque amical a son export, vérifie qu'il est arrivé.
- **Fin de saison 1 (dates 2026)** : dernière journée de ligue lundi 26/10 ; changement de saison dans la nuit, ligues neuves mardi 27/10 ; une semaine sans ligue ; première journée de la saison 2 lundi 02/11 (déduit) [Dev 2026-10-18/22]. Dimanche 25/10 = dernier entraînement avant le +1 an ; jeudi 29/10 = premier rapport d'académie de la saison 2. Le moteur passe en v4 en ligue dès la saison 2 [News 2026-10-19]. Détail dans basketvibe-saison.
- **Moteur** : ligue en v3 jusqu'au 26/10 inclus, v4 ensuite ; ne pas mélanger les deux dans les tendances.

## Pièges communs
- Ligue et amicaux ne se comparent pas (fatigue et expérience à ≈ 1/10 en amical, pas de blessure) [M§1.2].
- Moteur : ligue v3 jusqu'au 26/10 inclus ; v4 ensuite, sans autre changement prévu [Dev 2026-09-30, News 2026-10-19].
- Consignes : l'écran affiche 1–5 = nos données 0–4 (+1) (confirmé par l'utilisateur le 2026-10-18). Donne toujours les valeurs de l'écran.

## Ordre des agents et briefs du jour (règle du 2026-10-22)
Un agent ne rend jamais un retour incomplet parce qu'un autre agent n'est pas encore passé. Ordre de lancement, chaque agent lisant les briefs du jour (`outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md`) des agents placés avant lui :

| # | Agent | Lit les briefs du jour de | Pourquoi |
|---|---|---|---|
| 0 | Veille (si nouvelle source) | — | une règle qui change pèse sur tous |
| 1 | Match | — | résultats et conseils contrôlés dans `learnings.md` |
| 2 | Effectif | Match | forme, fatigue, blessures, minutes |
| 3 | Finances-personnel | Effectif | salaires, solde, plafond d'enchères |
| 4 | Académie | Finances | budget d'investissement et de tests |
| 5 | Entraînement | Effectif | choix par joueur (samedi, avant dimanche 04:00) |
| 6 | Tactique | Match, Effectif, Entraînement | rotation, cinqs, focus défensif, depth chart |
| 7 | Transferts (dernier) | Effectif, Finances, Tactique, Académie | qui joue, ce qu'il coûte, ce qu'on peut payer |

- Les agents sans dépendance entre eux peuvent tourner en parallèle (ex. Académie et Entraînement), jamais un agent avec ceux qu'il doit lire.
- Avant d'écrire « donnée non relevée » ou « brief absent », cherche dans les briefs du jour des agents en amont. Si elle n'y est pas, dis lequel et quel export manque, en tête du résumé.
- Si un agent en aval change une conclusion d'un agent en amont (ex. Transferts libère un joueur présent au depth chart de la Tactique), il l'écrit en tête de son résumé pour que l'agent en amont soit relancé.

## Options observées (lecteur-exports, 2026-10-25)
| Élément | Où | Valeur actuelle | Effet |
|---|---|---|---|
| `estimated_chance` {home_pct, away_pct} | `match` / `friendly`, aperçu (`body.estimated_chance`) | J22 contre Wolves Empire : 53 % domicile / 47 % extérieur | Effet inconnu : à comparer au résultat de chaque match, mesure = écart entre `home_pct` et `my_result` |
| `league_hardiness` | `club` / `notifications`, `body.league_hardiness` (avec `standings`) | 54,4 | Effet inconnu : à relever chaque semaine, mesure = évolution et lien avec la force des adversaires |
| Focus défensif `off` | `body.defensive_focus[].focus`, ligue du 26/10 (un adversaire) | valeurs vues : give_up, light, normal, intense, off ; `area_step` 3 partout | `off` non décrit dans les fiches : à tester sur un seul adversaire, mesure = points marqués par lui |
| Onglets Progress et Recent changes | Training (DOM) | non exportés | Recent changes alimente `silver.bv_training_changes` (arrêté au 18/10) |
| `hide_match_results_until_replay` | `club`, `body.preferences` | false | Préférence d'affichage, sans effet de jeu connu |
| Coupe FR (match 28/10 18:00 contre MACCABI) | `club`, `body.cup_fixtures` et `active_enrollments` | tactique non enregistrée | Non lue par silver (`bv_fixtures`, `bv_matches` sans cette date) |
| Notification `training_resolved` | `notifications` | 13 améliorés, top Bernard rebond +2 | Contrôle rapide du résultat de l'entraînement |

Ajouts du lecteur-exports 2026-10-26 (export de 20:08 UTC) :

| Élément | Où | Valeur actuelle | Effet |
|---|---|---|---|
| Préréglages `active_friendly_preset_id` / `active_league_preset_id` / `active_cup_preset_id` | `match`/`friendly`, page tactique (`body.presets`, 2 presets : « League Tactic » 43d784f8, « Friendly » 924952fc) | amical = « Friendly » ; ligue = « League Tactic » ; **coupe = « League Tactic »** (même id que la ligue) | La coupe du 28/10 reprend donc le preset de ligue ; effet sur le résultat inconnu : mesure = score et `my_result` du match de coupe |
| `player_directives` : `role_tier`, `shot_tier`, `offensive_focus_tier` (0–4) en plus de `defense_tier` | presets, par joueur | ex. Friendly : Bonnet role 4 / shot 4 / focus 4 ; Leclerc role 3 / shot 4 ; League Tactic : Bonnet idem, `defense_tier` 2 partout (Friendly : 0 sauf Dang et Albano à 2) | Seul `defense_tier` est documenté (fatigue) ; effet des trois autres inconnu : à tester une option à la fois, mesure = tirs tentés (`fga`) et points du joueur dans l'export du match |
| `possessions_per_quarter_n` | `match`/`friendly`, détail | 50 (Wolves et Debrecen) | Effet inconnu : à relever, mesure = tirs + pertes + lancers par équipe |
| `injuries` (match) | détail du match | J22 : Casadei (Wolves) blessé ; amical : aucun | Lecture : blessure adverse avant match, mesure = minutes de l'adversaire |
| `club_strength` | `notifications`, `standings[]` | Chomelix Cow 53,6 ; plage de la ligue 52,2 à 58,4 (KK Uola) | Effet inconnu : à comparer au rang final (nous 8e avec 53,6) |
| `manager_last_seen_at`, `manager_is_online`, `is_banned`, `entry_direction` | `notifications`, `standings[]` | BARIUM vu pour la dernière fois le 26/08, Thrylos le 17/08 | Clubs abandonnés repérables ; effet de jeu inconnu |
| `popularity`, `weekly_medical_staff_cost`, `weekly_medical_staff_peak_cost`, `transfer_lock` | page typée `academy` (en réalité finances) | 0,67 ; 60 000 ; 60 000 ; false | Le journal montre 85 000 de personnel médical le 25/10 contre 60 000 affichés : écart à expliquer |
| `skills_visibility`, `is_academy_junior`, `primary_display` / `secondary_display` | `training`, `body.players[]` | « full » ; false | Affichage entier des compétences (skill_display) vs `stats` décimales |

## Sorties
- Briefs : `outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md`.
- Journal : `outputs/basketvibe/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`).
- Veille : `outputs/basketvibe/veille/`.

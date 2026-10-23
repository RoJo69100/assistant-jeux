# BasketVibe — fiche commune (tous les agents)

Lue en premier par chaque agent, avant la fiche de son domaine (`docs/fiches/basketvibe/<agent>.md`).

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

## Sorties
- Briefs : `outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md`.
- Journal : `outputs/basketvibe/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`).
- Veille : `outputs/basketvibe/veille/`.

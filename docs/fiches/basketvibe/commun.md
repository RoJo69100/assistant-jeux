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
- Un amical presque chaque jour (08:00, à domicile).

## Pièges communs
- Ligue et amicaux ne se comparent pas (fatigue et expérience à ≈ 1/10 en amical, pas de blessure) [M§1.2].
- Moteur : ligue en v3 en saison 1, amicaux en v4, ligue en v4 en saison 2 [Dev 2026-09-30, News 2026-10-11/16/17].
- Consignes : l'écran affiche 1–5 = nos données 0–4 (+1) (confirmé par l'utilisateur le 2026-10-18). Donne toujours les valeurs de l'écran.

## Sorties
- Briefs : `outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md`.
- Journal : `outputs/basketvibe/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`).
- Veille : `outputs/basketvibe/veille/`.

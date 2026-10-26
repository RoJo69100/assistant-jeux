---
name: hockeynation-coachs-entrainement
description: Règles Hockey Nation sur les coachs et l'entraînement — 3 types de coachs, 6 compétences d'entraînement et 5 de match (OFP, DFP, BAT, PP, PK), head coach compté double, compétences spéciales débloquées par l'expérience, plafonds U17/U21, embauche (jours 1-35, meilleure offre), promotion sans retour, renvoi, retraite à 65 ans ; entraînement quotidien, choix du coach, ordre de choix, vitesse, maxings, déclin. À charger pour recruter ou former un coach, ou régler l'entraînement PRO/FRM.
---

# Hockey Nation — coachs et entraînement

Sources : **[G:Coaches]**, **[G:Training]** (guide du 30/09/2026, lu le 2026-10-23).

## Coachs
- Types : réguliers (compétences plafonnées entre 4 et 10, 3 compétences spéciales), intérimaires (3-5, aucune spéciale, remplacent un poste vide), amateurs (équipes nationales).
- Staff par équipe : 1 head coach + 3 assistants. Le head coach supervise 9 joueurs à l'entraînement, un assistant 6.
- **6 compétences d'entraînement** au hasard parmi les 15 compétences de joueur (1 à 3 de gardien : 60 % en ont 1, 30 % 2, 10 % 3 ; un ancien gardien en a 3).
- **5 compétences de match** : OFP jeu offensif à 5 contre 5 (mieux avec une note offensive élevée), DFP jeu défensif (note défensive), BAT duels (note physique), PP supériorité, PK infériorité. **Celles du head coach comptent double.**
- Compétences spéciales : 3, débloquées à des niveaux d'expérience secrets (1re entre Bad et Average, 2e entre Solid et Very Good, 3e entre Excellent et Elite). **Seules celles du head coach jouent en match.** Utiles : Eye For Talent (meilleur joueur de 25 ans ou moins +1), Shining Star, Commander, Meditation, First/Second/Third Period.
- Progression : un coach employé progresse chaque jour ; un coach sans emploi ne progresse pas. Plafond en U17 : note 54 et expérience Average ; en U21 : note 69 et Very Good. Au-delà, il ne progresse plus.
- Expérience : par match officiel, plus vite en PRO qu'en FRM, U21 ou U17 (ex. None → Awful = 31 matchs PRO à domicile, 40 en U17).
- **Former un jeune coach** [U] : l'embaucher en U17 (le guide conseille de remplir l'U17 d'abord), le promouvoir quand il atteint le plafond. Promotion sans retour possible, seulement vers un poste tenu par un intérimaire, jusqu'au jour 35.

## Choix des coachs (consigne de l'utilisateur, 2026-10-25 ; [Discord, #general, 2025-12-24])
- Le critère est la **somme des 5 compétences de match** (OFP+DFP+BAT+PP+PK), le head comptant double ; l'entraînement vient après. PRO : la meilleure note de match tout en gardant les compétences d'entraînement utiles. FRM : jeunes coachs à potentiel. U21 : meilleur entraînement sans note de match nulle. U17 : jeunes coachs à développer, ou plafonnés à 54.
- Toujours proposer des jeunes coachs à potentiel : âge ≤ 45, expérience ≤ 3, au moins 2 compétences de match à 7 ou plus. Promotion U17/U21 → FRM/PRO quand ils sont plafonnés [Discord, #general, 2026-02-17].
- Limite d'expérience en FRM : non trouvée dans le guide ni dans Discord (10-25) ; à tester à l'offre.

## Embauche, renvoi, retraite
- Embauche du jour 1 au jour 35 (fin de la fenêtre I) ; jusqu'à 12 offres par jour (une par poste) ; réponse au début de la journée suivante, rien le 1er jour.
- Le coach choisit la **meilleure offre** : PRO > FRM > U21 > U17, puis head coach > assistant au même niveau ; à égalité, tirage au sort.
- Contrat permanent, salaire non public, hors plafond salarial.
- Protégé du renvoi pendant sa 1re saison au club. Renvoi immédiat ensuite (intérimaire à la place).
- Retraite à 65 ans ; un coach libre peut se retirer après 1 à 3 saisons sans club. Anciens joueurs de 38 ans et plus : peuvent postuler comme coach.

## Entraînement
- Quotidien, une compétence à la fois. Réglable en PRO et FRM seulement ; U21 et U17 entraînent une compétence au hasard, sans bonus ni malus.
- Chaque joueur choisit le coach le plus fort dans la compétence qu'il travaille, dans l'**ordre de choix** réglable (sinon aléatoire). Sans coach compétent : aucun bonus.
- Vitesse : âge (effet maximal dès 25 ans), niveau actuel (9 → 10 plus lent), Work Ethic, **niveau du coach dans la compétence** (effet fort). Le journal d'entraînement (`silver.hn_training_log`, `training_rate`) montre le coach choisi et la vitesse.
- Plafond atteint : le joueur passe à une compétence au hasard. Déclin dès 32 ans, les coachs n'y peuvent rien.

## Vues
`silver.hn_coaches`, `silver.hn_free_coaches`, `gold.hn_coach_board` (`match_sum` = OFP+DFP+BAT+PP+PK, `skills_open` = compétences encore sous leur plafond, `years_to_retire`), `silver.hn_training_log`.

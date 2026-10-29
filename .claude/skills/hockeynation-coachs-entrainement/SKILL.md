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

## [Veille 2026-10-29] Mise à jour (V-20261029-5)
- Le **rating d'équipe des coachs est un score calculé des compétences de match**, pas la note affichée du coach (cas du 29/10 : remplacement d'un intérimaire 43 → rating 57 puis 61). [Discord #general, hnadmin, 2026-10-29 11:49]
- Un coach à Puck Battling 80+ renforce les joueurs aux bonnes compétences physiques mais ne comble pas les faiblesses (avis du modérateur d0ghouse, 2026-08-24 20:04). Les compétences du head coach restent doubles après S27 (avis gordie_79, 2026-10-25). Coach Development Boost (S27) : effet exact non publié.

## [Veille intégrale 2026-10-29] Coachs et entraînement (V-A-13 à A-15, V-B-2, V-C-9)
- **Marché de coachs (depuis S17)** : marché ouvert ; une offre réussie renvoie automatiquement le coach en place (pas besoin de le renvoyer d'abord) ; le coach choisit la meilleure offre de poste (PRO > FRM > U21 > U17, puis head > assistant) et refuse un poste trop bas ; un coach renvoyé revient aussitôt dans le pool ; 2 jours de recherche. **Une seule offre de head coach par jour** (kenvald 2026-08-25) ; empiler les offres sur le n° 1 du marché fait perdre les autres bons coachs (avis). Remplace la réponse « début de la journée suivante ». [hnadmin 2025-01-02, 2025-02-04 ; d0ghouse 2025-04-10 ; V-A-13, C-9]
- **Spéciales par parcours** : coach U17 seul = max 1 spéciale, U21 = max 2, PRO = max 3 [d0ghouse 2024-03-24]. Arrêt de l'expérience et arrêt des compétences sont séparés ; un pop peut dépasser le plafond (U17 54, U21 69).
- **Places d'entraînement** : un head coach prend 9 joueurs, un assistant 6 ; une fois ses places remplies, il n'est plus choisissable (segi_3554 2024-03-29). Candidatures des jours 1-35 : 1 + intérimaires, plafonné à 10 (erzac 2024-03-25, formule d'avant le FRM, à revérifier). Anciens joueurs : coach dès 38 ans, scout dès 36 ans. Pool « Coaches → Tracker → Fired ». À vérifier à l'écran : « 12 offres par jour » du skill contre « 11/16 » cité par talonflame1 (2025-04-10). [V-B-2]
- **Spécialiser les coachs** : la note d'équipe des coachs est une moyenne de formule type OVR ; spécialiser par catégorie (OFP / DFP / BAT / PP / PK) donne une meilleure note ; chaque note booste les joueurs de ce type et ne comble pas les faiblesses : privilégier la catégorie où nos joueurs sont forts (croiser avec `gold.hn_coach_options`). [d0ghouse 2025-09-17, 2026-08-24 ; V-A-14]
- **Vitesse d'entraînement** : depuis S12 le « 100 % » du journal vaut ≈ 1,5 × l'ancien ; dépend de l'âge, du niveau (bas niveaux plus vite), de Work Ethic et du coach ; attaquants > défenseurs > gardiens ; U21 : entraînement aléatoire, même vitesse qu'en PRO. [hnadmin 2024-03-24 ; d0ghouse 2024-04-09, 2025-10-17 ; V-A-15]

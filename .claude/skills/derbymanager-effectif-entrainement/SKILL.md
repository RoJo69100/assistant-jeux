---
name: derbymanager-effectif-entrainement
description: Règles Derby Manager de l'entraînement et de la relève — loi de croissance, formule P × (F + C), niveau max et pic d'entraînement, 3 installations (technique, decisions, movement), intensité Low/Medium/High, Training Requirement (TR) et minutes jouées, mentors, icônes, déclin par l'âge, school S25 (4 jeunes, salaire = installations, 3 saisons), coût et rendement d'un jeune, scouting (niveaux 0-3, régions, fuites). À charger pour régler l'entraînement, projeter un joueur, choisir un jeune de l'école ou utiliser les scouts.
---

# Derby Manager — effectif, entraînement, school, scouting

Sources : `outputs/derbymanager/veille/connaissance.md` (2026-10-30). `dev` = développeur. Statut « confirmé » sauf mention.

## Principes d'entraînement
- Plus la compétence est haute, plus elle est dure à monter (1→2 facile, 19→20 difficile) ; les mauvais joueurs s'entraînent mieux que les bons — #italy 2024-11-22, dev ; #updates 2025-05-20, dev. Mieux vaut pousser 10→15 que 19→20.
- **Formule (2025-06-29)** : P (potentiel), F (installations), C (club fit + âge + autres), S (sharpness) ⇒ « something like P × (F + C) » ; S donne le pourcentage de ce nombre comme chance ; P et C cachés — #general 2025-06-29, dev. Le rôle de S est remplacé par le TR (2026-05-10) : contredit en partie.
- Toutes les compétences ont une chance de progresser, la compétence choisie une chance bien plus grande, avec « a small fixed chance to grow at all times » — #general 2025-06-29 ; #updates 2025-07-02, dev.
- Niveau max = potentiel + installations + tier + club fit ; le pic d'entraînement est un peu sous le max ; plus on s'en éloigne, moins on s'entraîne (courbe en cloche) — #general 2024-09-13 ; #italy 2025-03-17 / 2025-04-14, dev.
- Optimum : joueurs de 2-4 étoiles (2025-07-02) ; 2-3,5 étoiles (2025-10-24) ; 1,5-2 (2025-10-30) ; pic d'âge 18-25 — #updates / #discussion, dev — valeurs variables.
- 3 installations d'entraînement (technique, decisions, movement), chacune pour son jeu de compétences ; optimum quand niveau de l'installation = niveau de la compétence — #updates 2025-07-02, dev.
- Potentiels séparés : Movement (bonus jeune, pénalité vieux), Decisions (l'inverse), Technical (club fit) ; 1/3, 2/3, 3/3 catégories verrouillées (jaune) — #updates 2025-07-17, dev. Conseil : monter au maximum une catégorie pour que chaque joueur entraîne ≥ 1/3 de ses compétences — #discussion 2025-07-18, dev.
- Satisfaction d'entraînement : catégories au-dessus de l'exigence 0 ⇒ rouge, 1 ⇒ jaune, 2 ⇒ bleu, 3 ⇒ vert ; bleu = aucune pénalité — #quick-questions 2025-08-02 ; #discussion 2025-04-19, dev.
- Pas d'entraînement individuel (refusé par le développeur) ; si un joueur ne gagne rien : High intensity, sinon trop jeune, passé son pic ou mauvais fit — #discussion 2025-10-31, dev.
- Les rôles et les actions de match n'influencent pas la progression — #quick-questions 2026-05-08 / 2026-08-19, joueurs — complété.
- Mise à jour nocturne ~3 h (heure UK, joueur agunbiac9498) ; changer l'entraînement (même vers la même valeur) force le recalcul — #italy 2025-08-08, dev.

## Intensité et Training Requirement
- Intensité par joueur : Low = 50 % d'entraînement (+4 % de récupération), Medium = 100 % (+3 %), High = 150 % (+2 %) ; défaut Medium ; seule la config au moment de la mise à jour nocturne compte — #updates 2025-10-15, dev ; #discussion 2025-10-22, dev.
- **Training Requirement (TR, 2026-05-10)** : exigence de 3 à 7 jours entre deux matchs ; plus l'âge caché et la puissance sont hauts, plus l'exigence est basse — #updates 2026-05-10, dev.
- Jouer donne un boost le jour même, entraînement standard les jours suivants de la fenêtre, puis rien (exemple 2026-05-15 : match le 13, entraînements 13-17, rien le 18) — #updates 2026-05-10 / 2026-05-15, dev.
- **TR après match (2026-10-25)** : −1 s'il joue ≥ 20 min, −2 s'il joue ≥ 45 min, retombe à 1 s'il joue ≥ 75 min — #updates 2026-10-25, dev. (30/60/90 min du #inconnu 2026-10-22 : contredit.)
- Un joueur qui ne joue pas stagne et perd de la valeur ; sans entraînement la perte est plus forte pour les vieux (défenseur −30 pts ⇒ −4,5 M) — #italy 2025-10-16 ; #belgium 2026-10-08, dev.
- Joueurs de l'école : s'entraînent sans jouer ; promus en équipe, ils ne grandissent que s'ils jouent — #quick-questions 2025-01-27, dev ; #general 2025-01-13, dev.
- Gardiens : entraînement trop facile (2× plus vite, 2× plus haut) ; le développeur envisage −10 points/−30 % et un rythme plus lent — #italy 2026-09-03, dev — intention.

## Mentors et installations
- Mentors toujours actifs depuis 2025-07-02/17 ; valeur sur une seule zone (technique, decisions, movement) ; 1 point = 0,05 étoile de installations (10 = demi-étoile) — #updates 2025-07-02 ; #general 2024-06-30, dev.
- Chaque point de mentor = 1 M pour les installations à la retraite du joueur — #updates 2025-07-17, dev. Auto-retraite entre saisons : le perk reste — #updates 2025-04-23, dev.
- Les mentors ne s'achètent pas, ils se forment ; ils perdent 1 point en changeant de club (voulu) — #italy 2025-04-14, dev ; joueur furysk 2026-09-17.
- Un mentor est mentor de son groupe (GK / D / M / F), équipe et jeunes confondus — #quick-questions 2024-05-28, dev.
- Message « near/close/at the limit » : à near et close le joueur peut encore grandir — #quick-questions 2026-06-15, dev.
- Un joueur près de sa limite dans un club faible peut faire 20-30 sauts de compétences dans une meilleure équipe — #quick-questions 2025-08-13, dev.

## Âge et déclin
- Les compétences baissent surtout par blessure ou non-jeu ; entre 28 et 34 ans les baisses deviennent plus fréquentes (« 1 saison ou 5 si chanceux ») ; les jeunes ne perdent presque pas — #discussion 2024-12-13 → 2025-10-31, dev.
- Net ±4 par saison = stagne ; croissance à +8 ou +16 par saison — #discussion, dev.
- Natural fitness maximale vers 26 ans ; retraite automatique en fin de saison une fois l'icône posée ; 37+ ne prolonge plus ; âge réel caché ±3 ans — #quick-questions 2025-02-04 / 2025-10-20, dev ; #updates 2024-07-16, dev ; #belgium 2026-10-08, dev.
- Joueurs libres qui grandissent : +4 M (+30 %) en 17 jours — #inconnu 2026-10-15, dev.

## School et jeunes (règle actuelle S25, 2026-08-22/24)
- **4 jeunes max à l'école** ; plus de coachs : le jeune demande un salaire égal au coût de vos installations ; on peut en couvrir une petite part par un upfront fee — #updates 2026-08-22/24, dev.
- Contrats futurs de 3 saisons ; jeunes libérés vers le marché libre à 19 ans (22 avant) ; marché des jeunes = 18 ans et moins — #updates 2026-08-24, dev ; âge de recrutement 21 cité le 2026-08-15 et 2026-10-03 : en doute.
- Prix, tier, étoiles et expérience des jeunes sont masqués jusqu'à la promotion — #updates 2026-08-10 / 2026-08-22, dev.
- Refonte du 2026-06-17 : 400 jeunes par grande région, 250 ailleurs, redistribués à chaque début de saison ; pas de re-roll (promouvoir pour en obtenir un nouveau) — #updates 2026-06-17, dev.
- Salaire d'école : hors plafond salarial mais compte contre le revenu (2026-07-13, dev) ; des joueurs rapportent qu'il pèse sur le plafond depuis le 2026-08-21 — contradiction non tranchée.
- Coût total (2026-08-15) : installations dans les 40 ⇒ 1 an d'école + 3 ans d'équipe ≈ 6 M ; installations dans les 20 ⇒ ≈ 3 M ; un 2 M coûte ≈ 5 M sur le marché — #quick-questions, dev.
- « Facilities as a bet » : petites installations ⇒ n'importe qui, entraîner, vendre (1 M → 3 M) ; grandes ⇒ jeunes forts (3 M+ → 7 M) — #quick-questions 2026-08-14, dev.
- En D4 on ne sort que des 3 M de l'école (pas des 6 M) — #quick-questions 2026-08-15, dev.
- Promotion : impossible à 25 joueurs ; sortir 10 jeunes coûte ~1 M ; interdit de relancer 19 fois puis promouvoir à 0 jour — #general 2024-12-16 ; #england 2025-09-05 / 2025-09-12, dev.
- Jeunes ex-école : 5 % des frais de transfert à l'équipe formatrice — #updates 2026-09-06, dev.
- Jeunes comptés « fringe » au Team Spirit (≈ −1 % par jeune) — #discussion 2026-08-19 ; #quick-questions 2026-08-19, dev.
- Un jeune à l'école atteint ~2-3 étoiles sans temps de jeu — #discussion 2025-05-21, dev.
- Message « can't grow in school anymore » : lié au niveau de départ, pas à l'âge — joueurs 2026-07-29 → 08-15 — en doute.
- Avis du développeur : « School players are free, the only risk is you can't sell them and you pay salaries » ; « If school is too expensive it's because your facilities are » — #discussion 2025-05-16 / 2026-07-25, dev.
- Equilibre d'effectif conseillé : 5 oldies / 5 peak / 5 growing / 5 school — #discussion 2025-05-16, dev.

## Scouting
- Niveau 0 : fourchettes larges ; 1 : fourchettes plus petites + étoiles + fitness ; 2 : fourchettes encore plus petites + potentiel + expérience ; 3 : compétences exactes + personnalité — #updates 2026-02-14, dev.
- « Avec 1 scout on voit 3,5 étoiles et une excellente fitness, souvent tout ce qui m'importe » — #discussion 2026-02-14, dev.
- Les niveaux baissent d'un cran par semaine ; un joueur découvert disparaît le lundi suivant sans nouveau scout — #quick-questions 2024-06-15 ; #discussion 2026-06-29, dev.
- Scouter ne change pas la chance de signer ; il faut scouter au moins une fois pour enchérir — #updates 2024-07-16 / 2025-06-18, dev.
- 3 scouts gratuits par jour (« worked 5+ years ») ; 20 scouts distribués le 2026-06-17, ramenés à 20 la nuit — #discussion 2025-01-24, dev ; #updates 2026-06-17, dev.
- **Régions (2026-06-17)** : 11 régions = 5 ligues jouables (jeunes non assignés) + 6 régions avec joueurs de clubs ; un scout découvre ~3 % de la région parmi les 10-50 meilleurs ; « knowledge » plafonnée à 100 — #updates 2026-06-17, dev.
- **Fuites** : scouter un joueur peut le faire fuiter vers d'autres managers, chance multipliée par la connaissance de chacun — #updates 2026-06-17, dev.
- Stratégie du développeur : 2 régions en profondeur ou 6 en surface ; 6-12 scouts par mois ; Europe centrale (Portugal, Pays-Bas), Amérique du Sud — #general 2026-06-17, dev.
- Jeunes découverts : « Les 5 jeunes découverts ont déjà le 1er scout, il en faut 2 de plus » — #updates 2026-10-18, dev.
- Rapport d'équipe : scouter toute une équipe coûte 1 scout ; après le 3e scout, stats de match détaillées ; vos joueurs comptent comme 3 scouts — #updates 2026-10-18, dev.
- Rapport de potentiel : probabilité d'atteindre un tier ou plus au-dessus (« high potential to reach lower league tier ») — #updates 2025-01-08, dev.
- Prix d'un scout et durée de vie d'un rapport après S26 : inconnus.

## Pièges
- Ne pas appliquer le « 8 jeunes à l'école » (2026-07-05 → 2026-08-19) : remplacé par 4 le 2026-08-24.
- Le TR change avec les minutes : un joueur qui joue < 20 minutes ne réduit pas son exigence — #updates 2026-10-25.
- Intensité High = 150 % mais récupération +2 % seulement : ne pas l'appliquer à un joueur dont la condition est basse.
- Un jeune promu qui ne joue pas ne grandit pas.
- Un jeune dont le prix est masqué peut être surévalué ou sous-évalué : aucune valeur avant promotion.
- Un joueur « trop bon pour le club » ne s'entraîne plus et bloque la prolongation — #quick-questions 2026-08-24.
- Le pool de jeunes du scouting semble affaibli en octobre 2026 (joueurs) — en doute.
- Les chiffres « 50 max » pour les mentors sont ambigus (#italy 2025-04-14) : ne pas les citer sans vérification.

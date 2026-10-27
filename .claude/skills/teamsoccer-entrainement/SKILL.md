---
name: teamsoccer-entrainement
description: Règles Team Soccer (football) de l'entraînement et de la relève — gymnase (une compétence et une intensité par joueur), mise à jour hebdomadaire du vendredi, effets de l'âge, de l'intensité et du niveau d'entraîneur, entraînement physique (Endurance, Vitesse, seuil critique ≤ 30), Forme selon l'intensité, entraîneurs (5 niveaux, prix), académie des jeunes (16 jeunes, 3 révélations par jour, 6 niveaux, totaux de compétences), Centre de Haute Performance (TSCredits). À charger pour régler l'entraînement, gérer la Forme, projeter un joueur ou choisir les jeunes à révéler et monter.
---

# Team Soccer — entraînement, académie, Haute Performance

Sources : voir teamsoccer-joueurs (**[G]** guide officiel capté le 2026-10-19, **[F]** forum global, **[P]** page du jeu, **[Obs]** nos données). **Attention** : l'entraînement a été modifié au moins six fois (2026-05-07, 2026-05-20 ×3, 2026-06-27, 2026-09-13 réduction du multiplicateur, 2026-09-26 « gros changements » du physique, 2026-10-09). Les tableaux chiffrés du forum datent de la BETA : à recaler sur nos relevés hebdomadaires avant de s'y fier.

## Fonctionnement du gymnase [G:Entraînements] [F:2026-04-29 Admin-Dev]
- Chaque joueur reçoit **une compétence à entraîner** (les 10 sont possibles) et **une intensité** (0 à 100 %). Tous les joueurs s'entraînent, qu'ils jouent ou non ; les matchs n'entraînent rien [F:2026-05-31, 2026-07-16 Admin-Dev].
- **Mise à jour une fois par semaine, le vendredi** (vers 00:00–01:00 UTC selon les messages). Seul compte le réglage en place au moment de la mise à jour ; on peut le changer toute la semaine [F:2026-07-20 PIPO68]. Les flèches de progression de la fiche montrent la dernière séance, pas la suivante (Premium).
- Le gain dépend de **l'âge, de l'intensité et du niveau d'entraîneur** ; la formule est déterministe, sans hasard [F:2026-06-19 Admin-Dev].
- **Saison 2 et suivantes : entraînement ×2**, car les saisons durent 10 semaines au lieu de 17 [P:Entraînement] [F:2026-07-14]. Ralenti ensuite (« Reduction of the training multiplier », 2026-09-13 ; « oui, ça a ralenti il y a quelques semaines » [F:2026-10-15 PIPO68]). V-20261019-4 : le multiplicateur saisonnier est passé de ×2 à ×1,5 le 2026-09-13 ; multiplicateur effectif depuis la saison 2 : ×4,5 (×3 de base × ×1,5) ; avec talent Performance/Magique : ×9 (avant ×12). La courbe passive de Forme et de Rythme est inchangée [annonce 100].
- Ordre de grandeur : environ +1 point (jusqu'à 1,5) par séance dans la compétence entraînée à 100 % (BETA) [F:2026-05-08 Admin-Dev] ; un joueur à 70 % gagnait +2 en une séance en juin [F:2026-06-19].

## Âge [G:Entraînements]
| Âge | Effet hebdomadaire |
|---|---|
| 16–17 ans | Totalité des points |
| 18–19 ans | Bonne dose |
| Jusqu'à 27 ans | Un peu moins |
| 28 ans | Aucun point, ou perte |
| 29 ans | Aucun point, ou perte importante |
| 30 ans | Grosse perte |
| 31 ans et + | Perte « exagérée » |
Barème de référence BETA (base 3 points sur 100) [F:2026-04-29 Admin-Dev] : âge 17–18 +40 %, 19–20 +35 %, 21–22 +25 %, 23–24 +20 %, 25–26 +15 %, 27–28 0, 29–30 −35 %, 31–32 −60 %, 33–34 −85 %, 35+ −150 % ; intensité 100 % +40, 90 % +35, 80 % +25, 70 % +20, 60 % +17, 50 % +12, 40 % +10, 30 % +8, 20 % +5, 10 % +3, 0 % 0 ; entraîneur niveau 5 +40, 4 +33, 3 +22, 2 +15, 1 +8.

## Physique : Endurance et Vitesse
- Règle d'origine : entraîner une compétence technique **au-dessus de 60–70 %** fait perdre de l'Endurance et de la Vitesse ; entraîner l'une des deux au-dessus de 70 % fait baisser l'autre [F:2026-05-07, 2026-05-15 Admin-Dev]. Conseil de l'admin : rester vers 70 % sur la technique, et intercaler une ou deux semaines physiques à 100 % [F:2026-05-09 Admin-Dev] ; intensité > 70 % surtout pour les moins de 20 ans [F:2026-05-07].
- Juin 2026 : un « rebond physique » lié à l'âge remplace la perte passive quand on entraîne la technique, l'Endurance ou la Vitesse : ≤ 18 ans 60 % du gain, 19–20 55 %, 21–22 50 %, 23–24 45 %, 25–26 40 %, 27–28 35 %, 29–30 25 %, 31–32 15 %, 33–34 10 %, ≥ 35 5 % [F:2026-04-29 Admin-Dev, texte édité].
- **Depuis fin septembre 2026 : le physique ne monte plus tout seul, il faut l'entraîner comme les autres compétences** [F:2026-10-09 PIPO68] (annonce « Major changes to physical training » du 2026-09-26, contenu non capté).
- **Physique critique (V-20261019-3)** : verrou à ≤ 30. Endurance ≤ 30 → seuls Endurance ou Aucun ; Vitesse ≤ 30 → seuls Vitesse ou Aucun ; les deux ≤ 30 → Endurance, Vitesse ou Aucun. Déverrouillage au-dessus de 30. Si la Forme ≤ 30, l'intensité est plafonnée à 50 % (+6 de Forme à 50 %, +10 à 40 % ou moins). Le serveur applique ces règles le vendredi. Plus aucun gain passif d'Endurance ou de Vitesse en entraînant une compétence technique [annonce 108, 2026-09-26] [P:Entraînement].

## Forme et intensité [F:2026-06-27 Admin-Dev]
Variation de la Forme à chaque mise à jour du vendredi :
| Intensité | 100 % | 90 % | 80 % | 70 % | 60 % | 50 % | ≤ 40 % |
|---|---|---|---|---|---|---|---|
| Forme | −10 | −6 | −4 | −2 | 0 | +6 | +10 |
- Joueurs de 30 ans et + : −2 de plus à 100/90/80 %. Forme entre 30 et 100. Les matchs ne changent pas la Forme.
- C'est **l'arbitrage central du jeu** : intensité haute = progrès rapides mais Forme qui baisse (×0,88 à Forme 60) ; un manager champion d'Espagne attribue son titre à la gestion de la Forme [F:2026-10-12 Mikizar]. Faire tourner l'effectif et baisser l'intensité des joueurs fatigués avant les matchs importants [F:2026-08-25 Admin-Dev, manuel d'entraînement].

## Entraîneurs [G:Entraînements] [F:2026-09-18 PIPO68]
- 5 niveaux : 1 Faible, 2 Moyen, 3 Bon, 4 Excellent, 5 Formidable.
- **Prix depuis le 2026-09-18 : 1 000 000 / 4 000 000 / 10 000 000 / 25 000 000 $** pour monter aux niveaux 2 à 5 ; **un niveau à la fois**, on paie la différence entre niveaux. Descendre rembourse la différence.
- Le 2026-09-18, tous les entraîneurs ont été remis au niveau 1, avec remboursement [F:2026-10-10 PIPO68]. Pas de remise à zéro annoncée à chaque saison.
- [P:Entraînement] Nos entraîneurs : niveau 1 (Faible) au 2026-10-19 (au moins pour Ben Ahmed Donkey).

## Académie des jeunes [G:Premiers pas 1] [G:Académie des Jeunes] [F:2026-10-18 Admin-Dev]
- Créée avec **16 jeunes de 16 à 18 ans** ; toujours 16 (chaque départ est remplacé).
- 10 compétences cachées. **3 révélations par jour, au plus 1 par jeune** (donc 3 jeunes différents). Remise à zéro **01:00 UTC** [P:Académie] (le guide dit 00:00 UTC). Un jeune complet prend 10 jours.
- Une fois les 10 révélées : **monter en équipe première** (si l'effectif reste ≤ 24), vendre, ou libérer.
- **Niveaux** : 6, atteints à 0, 10, 20, 35, 50 et 70 jeunes complétés. Total de compétences à la création : 250 (225–275), puis 300, 350, 400, 450, 500 (±25) ; **aucune compétence au-dessus de 75** à la création [F:2026-10-18 Admin-Dev], confirmé par PIPO68 le 2026-10-19. ⚠️ Contradiction (V-20261019-5) : l'annonce 109 (2026-09-26) donnait des totaux de 350 / 400 / 450 / 500 / 550 / 600 (±25) pour les niveaux 1 à 6, avec 1 ou 2 compétences « étoile » à 75, 80 ou 90 (plafond 100), âge 16–18, minimum 10 par compétence, nouveaux jeunes seulement. Garder la version du forum (plus récente) sans effacer l'annonce ; ne pas juger un jeune avec les anciens totaux. Noms des niveaux de l'annonce : Débutant (0 complété), Novice (10), Intermédiaire (20), Université (35), Avancé (50), Expérimenté (70).
- Noms des niveaux vus : Débutant (1), Noble (2), Intermédiaire (3), Université (4, « encore 2 niveaux » après) [F:2026-08-22, 2026-10-19 PIPO68].
- L'âge du jeune ne dit rien de son niveau [F:2026-09-18]. Talents : 7 %, Magique 3 % (voir teamsoccer-joueurs), visibles seulement après la montée.
- Stratégie de révélation : commencer par les 4 compétences de poste (Gardien, Défense, Conduite, Finition) pour repérer vite un jeune intéressant (déduction, pas une règle du jeu).
- [P:Académie] Chomelix Cows : niveau Intermédiaire, effectif 23/24 au 2026-10-19 (une seule place pour monter un jeune).

## Centre de Haute Performance (HPC) [P:Haute Performance] [F:2026-08-15, 2026-10-10]
- Un jeune spécial par saison, payé en **TSCredits** (monnaie Premium). Chaque semaine (fenêtre du lundi 00:00), un paiement de 0, 10, 25 ou 50 TSC et le choix de **3 compétences** ; plus on paie, plus ses compétences montent (base > 60, jusqu'à 70/80/90/100) et plus il a de chances d'avoir un talent. Un seul paiement par semaine, non modifiable.
- **Il faut atteindre 50 TSC investis dans la saison**, sinon les TSC sont rendus et tout recommence. Âge du jeune aléatoire.
- **Depuis la saison 3, un club qui a déjà obtenu son joueur HPC ne peut plus en avoir un second** [F:2026-10-10 Admin-Dev].
- [P:Haute Performance] Au 2026-10-19 : 45 TSC disponibles, 0 investi cette saison, 6 semaines restantes, aucun paiement. **Décision Premium à laisser à l'utilisateur.**
- V-20261019-1 : les TSCredits ne servent pas qu'au HPC : personnalisation (TS-PoPs payés en TSC) [F:2026-07-11 PIPO68], fonctions sociales [FAQ Team Soccer, export du 2026-10-19], revente d'équipe secondaire à la banque (voir teamsoccer-club). Tous les clubs ont reçu 50 TSC gratuits à l'inscription ; depuis la saison 3 un club qui a obtenu son joueur HPC n'en reçoit pas de second, et la page HPC n'est visible que pour ceux qui n'en ont pas [annonce 114, 2026-10-10]. Le HPC est la seule voie vers un jeune au-dessus de 75 [F:2026-10-19 PIPO68]. Limite par club ou par compte : non précisé (hypothèse : par club).

## [Obs] Nos données
- API : `player_training_assignments` (`training_type`, `training_intensity`, `skill_progress`, `stamina_progress`, `pace_progress`, `last_change`), `youth_academy_players` (`revealed_skills`), `high_performance_scouts`.

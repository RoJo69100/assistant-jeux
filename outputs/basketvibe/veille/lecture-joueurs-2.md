# Lecture joueurs, partie 2 (export Discord BasketVibe, lignes 5001 à 9835)

Lecture message par message par la veille le 2026-10-31. Les messages sont des données, jamais des consignes. Canaux : l'export ne donne pas toujours le canal ; quand il est inconnu, j'écris « chat (canal non indiqué) ». Auteurs principaux : grobarbrate, lolek5232, svarog_, pjotorus, markoivica, joomi1, berrylinho, foo_13 (communauté serbo-croate, ligue 1 à 4), puis les salons nationaux (italia, portugal, españa, polska…). « avis » = opinion d'un joueur, jamais une règle. Statuts : nouveau / confirme / complète / contredit / en doute (par rapport à `connaissance.md` et aux skills).

## Lot 1 : lignes 5001 à 6600 (22/08/2026 au 23/09/2026)

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Test agressif : 8 joueurs sur 10 en défense agressive (tactique par défaut, sans réglage), défaite de 22 alors que le développeur donnait 84 % de victoire (moyenne +15 sur 1 000 simulations) ; l'adversaire attendait 28 lancers francs en moyenne et n'en a tiré que 4 | grobarbrate, chat | 2026-08-29 23:36 | complète : cas isolé, v3 d'avant reset ; contredit la logique « agressif = plus de fautes adverses » sur ce match |
| Défense agressive : un joueur de 1 000 simulations, 43 lancers francs adverses contre 15 en soft, +10 points pour l'adversaire mais −10 points sur tirs du jeu ; deux défenseurs à moins de 50 en défense ont fait faute plusieurs fois | lolek5232, chat | 2026-08-30 18:17-18:22 | confirme (agressif = plus de fautes, risque pour les défenseurs faibles) ; avis sur l'échantillon (1 match) |
| Dans le duel direct de la feuille de match, soft = −14 en défense et agressif = +14 (écart de 28 points de compétence entre les deux) ; l'utilisateur ne comprend pas « défense as unit −4,4 en moyenne » | grobarbrate, svarog_, chat | 2026-08-30 18:23-18:28 | nouveau (v3 pré-reset) : valeurs lues sur la feuille de match, à comparer au tableau agressivité du manuel |
| Un joueur avec une bonne défense gagne à être agressif ; un joueur à défense faible empire (avis) | grobarbrate, svarog_, chat | 2026-08-29 | avis, cohérent avec « double tranchant » (connaissance.md 19/09) |
| Focus défensif fonctionne : un joueur « fermé » à 5 n'a pas tiré un quart entier (SG de 12 min), les ailiers abaissés à 1-2 ont tiré beaucoup (PF 14 trois-points sur 24 tirs) ; mélanger focus haut sur les uns et bas sur les autres est risqué pour les deux camps (avis) | svarog_, grobarbrate, lolek5232, chat | 2026-09-06 17:16-17:25 | confirme (focus redistribue les tirs, cohérent avec 07/09 « 50 % à un joueur ») |
| Deux attaquants bloqués par le focus adverse ont tiré 4 fois à eux deux sur un match ; un adversaire a fait l'inverse (abaissé tous les attaquants, fermé les centres) et gagné | grobarbrate, svarog_, chat | 2026-09-09, 2026-09-07 | confirme |
| 3P fortement réduits après le réglage de début septembre : avant 20 trois-points par équipe, maintenant 7-8 à 12-13 par joueur de pointe, 70-69 et 85-66 au lieu de 130-120 ; un tireur à 22 % en trois points, un Français 0 sur 13 | grobarbrate, svarog_, chat | 2026-09-04, 2026-09-06, 2026-09-07, 2026-09-12 | confirme (cohérent release-notes 24/08, 14/09 sur plafond 3P) |
| Chaque tir à 3 points entraîne souvent 3 lancers francs et des fautes en masse | pjotorus, grobarbrate, chat | 2026-09-04 19:07-19:08 | avis (observation sur peu de matchs) |
| Pénalité de fatigue des 5 joueurs à 48 min : chiffre cité « 10 % dans le dernier quart seulement » ; la Q4 est quand même gagnée en moyenne de +2,88 en déplacement et +5,12 à domicile par une équipe à 5×48 min | grobarbrate, lolek5232, chat | 2026-09-04 19:19, 2026-09-12 21:15 | complète (donne la mesure du dev avant le durcissement à 12,5 puis 20 % du 13/09) |
| Un joueur à 78 de tir à 3 points a tiré 0 sur 9 à 45 de défense adverse puis tout réussi au quart suivant : l'aléa domine sur un match | lolek5232, chat | 2026-09-04 19:26 | avis |
| Un joueur à fatigue 32 et 20-40 de tir a mis 4 trois-points sur 7 contre une défense à 62 et fait perdre presque le match | lolek5232, chat | 2026-09-16 20:36 | avis (aléa) |
| Un passeur placé « tir » donne un très mauvais pourcentage ; remis « passe » : 12 passes décisives et meilleur pourcentage | lolek5232, chat | 2026-09-09 18:43 | nouveau (avis, 1 cas) ; cohérent avec le réglage passe/tir du skill |
| Un PG avec Pass 70 et tir à 2 points 70 mais 31 en défense et tir à 3 points 31 : placé « passe » il ne marque pas, placé « tir » plus personne ne passe | grobarbrate, chat | 2026-09-01 13:22 | avis |
| Un joueur de 205 cm joue SF à C sans pénalité de compétence si sa taille convient ; 197 cm à PF ≈ 2-3 % de pénalité (« 3 % sur 80 = 2 points ») ; face à un joueur de 215 cm, léger avantage pour le grand | lolek5232, grobarbrate, chat | 2026-09-05 10:06, 2026-09-16 13:17-13:18 | complète (mesure indicative ; le skill dit « aucune pénalité de poste hors rebonds ») ; avis |
| Mettre un joueur plus grand que le tireur à chaque poste a donné de bons résultats | jeremiahcross., chat | 2026-09-07 19:49 | avis |
| Rebonds : un centre à 80 et un PF à 72 en rebond (36 min chacun) battus de 10 rebonds offensifs par une équipe sans pivot ; le développeur a reconnu un bug de distance au panier (déjà dans les release-notes) ; l'adversaire cite l'athlétisme, la forme (forme 3 contre 7), le domicile et une taille inférieure de quelques centimètres | grobarbrate, markoivica, chat | 2026-09-14 18:49, 2026-09-15 08:40-10:48 | confirme (bug 14-16/09 de connaissance.md) ; manuel cité par markoivica : « Rebounding — skill, height, court slot, athleticism stack » |
| L'athlétisme renforce les autres compétences (surtout la défense) mais ne fait rien si les compétences de base sont faibles | grobarbrate, chat | 2026-09-16 15:33 | avis, hypothèse conforme au skill (athlétisme = multiplicateur) |
| Défense de soft à l'extérieur : 93-92 perdu après avoir mené, deux blessures dans un quart malgré soft ; un autre perd son meilleur joueur au début du Q4, remplacé par PS 40 | lolek5232, joomi1, chat | 2026-09-16 18:37-18:51 | complète : soft n'évite pas les blessures |
| Avantage du domicile : « petite » (avis), un joueur a gagné de 1 à domicile contre un bot et de 60 à l'extérieur contre un autre : aléa plus fort que le domicile | lolek5232, foo_13, chat | 2026-09-09 18:28, 2026-09-21 19:50-20:01 | avis |
| Le développeur envisage d'appliquer une pénalité aux équipes qui laissent 5 joueurs à 48 min ; grobarbrate lui a écrit pour demander 50 %, d'autres s'y opposent (cas de blessures, 6 fautes) | grobarbrate, pjotorus, chat | 2026-09-04 19:28-19:30 | complète (précède les hausses 12,5 % / 20 % du 13/09, connaissance.md) |
| « Le premier tour de la coupe BV Cup, le rôle du 25 % » : fatigue de coupe = 25 % d'un match de ligue ; l'expérience de coupe = 25 % de la ligue (accord GM-développeur à 25 % au lieu de 50 %) | svarog_, grobarbrate, pjotorus, chat | 2026-09-09 16:20, 2026-09-12 20:05 | complète (pilote de coupe de septembre, périmé pour la coupe actuelle : News 23/10 : « aucune fatigue ») |

### Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Perte de fatigue par jour = 10 % de la fatigue + 0,5 (10 de fatigue → −1,5 ce jour-là) ; 0 de fatigue inatteignable sauf remise de fin de saison ; 1 minimum | lolek5232, chat | 2026-09-13 11:56-11:58 | nouveau (avis chiffré d'un joueur, v3) ; à comparer avec la table du manuel (récupération selon endurance) |
| Les joueurs de 14 de fatigue au 1er jour de coupe atteignent 20+ en quelques matchs ; 5 matchs de ligue + 7 amicaux par semaine rendent la gestion « impossible » | grobarbrate, chat | 2026-09-12 18:55, 18:48 | avis (v3) |
| Un joueur de 60+ d'endurance devrait pouvoir jouer toute la saison à 24 min en Normal | lolek5232, grobarbrate, chat | 2026-09-13 11:59 | avis |
| Amical : « 1/10 de fatigue et d'expérience d'un match de ligue » ; rapport 17-20 k par amical, environ 120-150 k par semaine | grobarbrate, svarog_, chat | 2026-09-01 10:38-10:43, 2026-09-11 14:32 | confirme (connaissance.md : « 10 % ») ; complète le montant (17-20 k, avant la baisse de 30 % du 21/08 ? non : après) |
| Les joueurs de 3 sur 4 en Normal avaient fatigue 1 en amical sans ligue | svarog_, chat | 2026-09-01 10:31 | avis |
| Les psychologues « ne servent à rien » pour la forme | grobarbrate, chat | 2026-09-20 08:44 | avis (contredit l'effet +5 % du skill économie ; échantillon inconnu) |
| La forme d'un joueur est remise à 6 en début de saison et un joueur à forme 7 domicile compte dans un rebond gagné | markoivica, chat | 2026-09-15 10:34 | confirme |
| Un jeune de 16 ans à l'académie 80 tire jusqu'à 54-55 de compétence (17 ans : +2 par compétence) ; à 92 % la compétence max est de 55 environ | lolek5232, grobarbrate, chat | 2026-09-10 10:52, 2026-09-14 20:02-20:04 | complète (tranche de l'académie, avis ; à vérifier sur `silver.bv_academy_candidates`) |

### Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Multiplicateur de potentiel : potentiel 10 = 2,2 en principal, 1,1 en secondaire ; potentiel 8 = 1,6 / 0,8 ; ralentissement après 18 ans, 21 ans, puis aux paliers de 70 ou 75, 80, 90 (lolek5232 ne sait pas si c'est 70 ou 75) | lolek5232, chat | 2026-09-14 19:54-19:56, 2026-09-16 14:28 | complète / en doute (le skill dit ralentissement au-dessus de 70 ; le chiffre 1,6 pour pot 8 est à vérifier dans `gold.bv_*` historique d'entraînement) |
| Avant le 10/08 : pot 1 ≈ 6 compétences par saison, pot 5 ≈ 12, pot 10 ≈ 18 ; maintenant pot 10 jusqu'à 26 | grobarbrate, chat | 2026-09-14 20:40-20:41 | confirme (connaissance.md : 26) |
| Potentiel des joueurs générés au départ : de 3 à 9 (aucun pot 10 dans l'effectif de départ) | lolek5232, chat | 2026-09-14 20:39 | nouveau (avis, vérifiable sur nos données) |
| Pour juger un jeune à acheter : demander l'historique d'entraînement au manager après 5-6 entraînements ; si le primaire gagne +2 à chaque fois, potentiel élevé | grobarbrate, lolek5232, chat | 2026-09-14 19:52 | avis (méthode, cohérente avec `bv` historique d'entraînement du 25/10) |
| Un jeune acheté 270 k (annonce) est monté à 660 k après une guerre d'enchères ; il avait gagné 1 compétence par entraînement, potentiel 5-6 | lolek5232, foo_13, chat | 2026-09-18 08:40-11:01 | nouveau (prix) |
| Un joueur de 25 ans ne gagne plus rien en entraînement depuis la réforme ; toute l'équipe de départ de lolek5232 est à potentiel 3 hors un rookie | lolek5232, grobarbrate, chat | 2026-09-06 06:59-08:32 | confirme (connaissance.md 06/09 : 25 ans = 9 compétences pour pot 6 ; ici pot 3 → quasi rien) |
| Un jeune acheté sans test : « tu achètes à l'aveugle », compétences fortes ≠ potentiel élevé | grobarbrate, chat | 2026-09-22 19:28 | confirme |

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| « Send for tests » : 25 k par joueur, 75 k par semaine pour 3 ; 3 étoiles = potentiel 8-10 (High) ; investissement max abaissé de 200 k à 100 k | grobarbrate, lolek5232, chat | 2026-09-03 08:09-08:27, 2026-09-16 14:29 | confirme |
| Chance de potentiel 10 : 10 % à l'académie 100, 5 % à 99 ; probabilité de High 40 %+ à 80 % ; stratégie : accepter un High dès 80 % plutôt qu'attendre 100 % ; 5-6 joueurs pot 8 valent mieux qu'un pot 10 (avis) | lolek5232, grobarbrate, chat | 2026-09-14 19:57-20:02 | confirme le tableau du skill ; avis sur la stratégie |
| À 92 %, le minimum d'athlétisme d'un jeune est 35 ; le niveau d'académie fixe les bornes de compétence (60 % → max 46, 70 % → 48) | lolek5232, chat | 2026-09-10 10:51, 2026-09-14 19:49 | complète (avis chiffré, pas dans le skill) |
| Académie à 29 % : « mieux de ne plus tirer » | svarog_, chat | 2026-09-10 09:39 | avis |
| Le potentiel d'un jeune mis en vente n'est pas visible (les joueurs réclament High/Medium/Low) ; vendeur peut mentir | grobarbrate, svarog_, chat | 2026-09-18 16:50, 2026-09-22 19:28-20:05 | complète (précède le sondage du 24/09) |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Après le reset du 29/08 : prix à 500-600 k pour un joueur correct (05/09), 800 k (12/09), > 1 M (3 joueurs à plus d'un million le 11/09), 1,2 M pour un C de 24 ans (19/09), 1,7 M revente (20/09), 1,9 M pour un 16 ans (20/09) ; un 16 ans à 30 de compétences partout : 420 k ; un 32 ans : 800-900 k et plus | lolek5232, grobarbrate, markoivica, chat | 2026-09-05 → 2026-09-22 | nouveau (série de prix post-reset, avant la saison 1 ; à comparer à `gold.bv_market_price_known`) |
| Conseil de ne pas thésauriser : acheter tôt car les prix montent ; d'autres vendent et attendent | lolek5232, markoivica, grobarbrate, chat | 2026-09-05, 2026-09-14, 2026-09-18 | avis (hypothèse d'inflation vérifiée par les prix ci-dessus) |
| Les joueurs de 28-32 ans achetés cher (300-800 k) ne servent qu'une saison ; un club de bas de division gagne à jouer jeune | grobarbrate, svarog_, chat | 2026-09-14 20:19-20:26 | avis |
| Taxe de 5 % non discutée ici ; un propriétaire de rookie a baissé le prix demandé de 300 à 250 pour attirer des enchères, qui ont monté à 660 | lolek5232, chat | 2026-09-18 08:41 | complète (stratégie : prix de départ bas) |
| Une équipe a vendu un C de 30 ans (Pass 70) 300 k au 02/09 | grobarbrate, svarog_, chat | 2026-09-02 20:15 | nouveau (prix) |
| Un joueur de 206 cm / 70 défense sans autre compétence : 35 k ; il « s'enfuit » (enchère perdue) | grobarbrate, chat | 2026-09-03 16:16 | nouveau (prix bas pour profil défensif nu) |
| Un 210 k à 410 k de pointe : attaquant bon mais « critique ailleurs » ; mauvais achat | grobarbrate, chat | 2026-09-03 16:02 | avis |

### Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Après le 21/08 : sponsor plus élevé, salaires multipliés (« triplés »), investissement académie max 100 k ; salaire minimum 12-13 k par joueur | grobarbrate, svarog_, chat | 2026-08-23 19:05-19:15, 2026-09-01 10:40 | confirme (connaissance.md 21/08) |
| Bonus des joueurs de l'académie : 200 par minute jouée, plafond 40 000 par semaine (soit 200 minutes) ; un joueur seul plafonne à 144 minutes | lolek5232, chat | 2026-09-11 14:55 | confirme (skill économie ; ajoute « 1 joueur max 144 » = 4 matchs × 36) |
| Avec 100 k par semaine en académie, un club est « à peine au-dessus de zéro » après trois matchs à l'extérieur et un à domicile | svarog_, chat | 2026-09-14 20:13 | avis |
| Revenu de départ 600 k, récupéré « en deux matchs à domicile » | foo_13, chat | 2026-09-19 22:03 | avis |
| Docteurs inutiles avant la première blessure (avis) ; 2 docteurs récupèrent une blessure de 3 jours en 2 jours | grobarbrate, chat | 2026-08-31 18:53, 2026-09-07 20:27 | complète (skill économie : médecins −50 % durée max) |

### Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un club peut choisir un pays de son choix à la création (pas la région) ; certains pays africains ont une première division « de difficulté 44 » | foo_13, chat | 2026-09-21 09:19, 21:21 | nouveau (hors de notre situation) |
| 7 amicaux par semaine possibles (programmés), payant 17-20 k chacun ; « résultat sans effet sur rien » | svarog_, grobarbrate, chat | 2026-09-01, 2026-09-11 | confirme |
| Après le reset du 29/08 : liguesde 4.13 pleines de bots, 6 bots dans la ligue de lolek5232, ; la 4e division se gagne en jouant 5×48 min contre des bots | lolek5232, berrylinho, chat | 2026-09-05, 2026-09-11 | confirme (skill : bots −10) |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Minutes sauvegardées (30 min PF et C) non appliquées après avoir tiré un jeune ; la tactique est restée comme avant | grobarbrate, pjotorus, chat | 2026-09-12 18:28-18:30 | complète (connaissance.md : « sauvegarde des tactiques après transfert 19-21/09 » ; ici 12/09, cause = tirage d'un jeune) |
| Première composition qui n'enregistre pas : PG au C, un PF de 16 ans au poste de meneur | foo_13, chat | 2026-09-16 12:00, 2026-09-20 10:19 | complète (même bug de lineup) |
| PS retiré des lignes de transferts sur mobile (déplacé sous le prix) | foo_13, lolek5232, chat | 2026-09-21 21:25 | nouveau (interface) |
| Bug de distance au panier sur les rebonds (cité) | grobarbrate, markoivica, chat | 2026-09-15 | confirme |

## Lot 2 : lignes 6601 à 7991 (23/09/2026 au 09/10/2026 ; puis salons #polska et #italia)

Le salon des joueurs serbo-croates s'arrête à la ligne 7326 ; le fichier continue avec #polska (7329), #italia (7496), puis #pilipinas (7994).

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un focus offensif posé sur un seul joueur : s'il se blesse en 12 min, le remplaçant sans focus « coule » l'équipe ; le focus défensif sur un tireur a fermé un joueur (3 tirs sur 15) | lolek5232, chat | 2026-09-24 06:16, 2026-10-02 20:09 | avis |
| Défense agressive adverse : 19 lancers francs tentés contre 6 (17 contre 5 réussis) pour l'équipe de lolek5232 en demi-finale de coupe, soit 12 points en 6 min ; « l'agressif est tout ce qui rend l'adversaire proche » | lolek5232, chat | 2026-10-04 20:19-20:49 | confirme (agressif = lancers francs pour l'attaquant) |
| À fatigue 33-40, un titulaire adverse a fait 27 points environ ; « les pénalités sont ridicules » | lolek5232, grobarbrate, chat | 2026-10-04 20:36-20:37 | contredit pour le v4 (−15 % à 40) ; v3 : 4-6 % à 25-30 (même source, 02/10 18:17) |
| Trop de focus défensif sur peu de joueurs ou à 1 : un centre adverse à focus 1 a marqué 48 points ; un joueur trop abaissé « et qui n'avait jamais joué » a puni ; trop de focus défensif globalement fait pleuvoir les trois-points adverses (60 %) | tankre1792, grillanza_60069, uthred9751, #italia | 2026-09-09 20:15, 2026-09-13 07:58, 2026-09-21 18:30, 2026-09-22 07:55 | confirme (focus 1 = « Give up » du skill) ; avis sur le reste |
| Aggressivité réglée « moyenne » en ligue et coupe, « minimale » en amical ; « trop agressif ne paie pas, rester sur moyenne » | grillanza_60069, tankre1792, #italia | 2026-09-22 05:06, 08:42 | avis |
| Un joueur posé hors poste (centre de 215 cm en garde, garde de 59 à 0/10) n'est pas pénalisé : « le moteur ne punit pas le hors-poste » | uthred9751, #italia | 2026-09-21 18:29, 2026-09-30 18:28 | confirme (skill : aucune pénalité de poste hors rebonds) |
| Poids : une PF de 194 cm pèse 102 kg ; question restée sans réponse sur le changement de rôle à l'entraînement | uthred9751, #italia | 2026-09-23 22:07 | avis |
| Un meneur « passeur » à 9 passes décisives de moyenne, tireur à 4 sur 26 en 5 matchs avec réglage « tir à 3 » : changer de réglage | faraone85_69754, #italia | 2026-09-05 08:42-08:45 | avis |
| Les 5 titulaires à 48 min adverses : « vaincu en Q4 de 20 points » (15/09) mais « 22-20 pour moi » (16/09) ; la pénalité de 20 % annoncée n'est pas encore sensible | faraone85_69754, grillanza_60069, #italia | 2026-09-15 11:57-15:58, 2026-09-16 21:04 | complète (après la hausse du 13/09 à 20 %) ; avis |
| Les gros écarts de fatigue se jouent contre l'adversaire : un titulaire en forme et reposé contre un adversaire épuisé par la coupe = victoire de 39 en déplacement ; les tactiques peuvent « exploiter » la fatigue adverse | faraone85_69754, #italia | 2026-10-03 06:59, 2026-10-07 20:14 | avis (1 cas ; cohérent avec la lecture de la fatigue adverse du skill) |
| Le 01/10, 3P % « plus hauts » mais tentatives plafonnées pour les meilleurs ; seul le focus offensif individuel a changé | grillanza_60069, uthred9751, faraone85_69754, #italia | 2026-10-01, 2026-10-02 | confirme (connaissance.md 14/09 et v3) |
| Passeurs en « passe » ne prennent plus de tirs : « enfin ça a un sens de poser la tactique » (introduction du focus offensif ; 10 passes décisives faisables) | svarog_, foo_13, chat | 2026-10-03 18:44-19:25 | confirme (V-20261029-1 focus offensif v3) |
| Rebonds : « skill, taille, emplacement, athlétisme » (manuel) ; trois joueurs à 60+ en rebond ramassent presque tout ; ordre d'importance C puis PF puis SF | jopencjusz, markoivica, #polska | 2026-09-13 21:50-21:55 | confirme |
| Défense de l'équipe plus utile que le tir ; « bon d'avoir une défense raisonnable partout » ; sans pivot à rebond, la défense seule laisse les rebonds offensifs | jopencjusz, #polska | 2026-09-13 21:45-21:51 | avis |
| Athlétisme = pas de rôle seul mais renforce toutes les autres compétences ; un SF à 53/56 de tir et 75 d'athlétisme marque beaucoup, un SG à 72/73 et 61 d'athlétisme moins | .doman, #polska | 2026-07-24, 2026-09-16 08:54 | avis, cohérent avec le skill |
| Focus et équipe adverse jouant 48 min : un joueur n'a gagné que d'un point (cup) ; 150 points au total en coupe contre 120 de moyenne en ligue | gothart_90207, #polska | 2026-09-30 06:25 | avis |
| Un centre avec seulement Défense et Rebond est peu utile contre des joueurs actifs ; utile contre des bots | marekb9231, #polska | 2026-10-08 15:34 | avis |
| Questions sur le « focus individuel » : pour un centre, 2P et rebond d'abord, puis physiques ; 3P ou passe pas en primaire | dcarra., tankre1792, #italia | 2026-10-03 10:41-10:50 | avis |

### Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Forme : ±1 au changement hebdomadaire, mais avec rappel vers les valeurs centrales (une forme 7 fait plus probablement −1) ; l'effet est faible sauf à forme 1-2 (dcarra.) ; la forme ne se gagne pas en jouant | grillanza_60069, dcarra., #italia | 2026-09-16 09:57-11:04 | complète (connaissance.md : « ±1 aléatoire » ; ajoute le rappel vers le centre, avis) |
| Expérience : « boost jusqu'à un maximum de 10 % » (manuel) ; 1 point d'expérience ≈ 100 minutes de ligue + 18 minutes d'amical = 180 min d'amical (hypothèse ; suivantes 210, 330 min ?) | grillanza_60069, svg07, #italia | 2026-09-17 09:57, 2026-08-01 11:53 | en doute (hypothèse d'un joueur, 1 observation) |
| Gestion de la fatigue sous 20 le jour du match : tourner à 12 joueurs, laisser les 2 plus fatigués hors des amicaux, 5 jeunes de 16 ans pour les amicaux ; 10 joueurs à 20 min ne suffisent pas toujours | tankre1792, uthred9751, grillanza_60069, #italia | 2026-09-23 19:06, 09-25 13:06, 09-26 10:46 | avis (v3, 3 matchs par semaine ligue/coupe) |
| « Le système de fatigue est calibré pour obliger à choisir entre coupe et championnat » | _stefax (lu ailleurs), #italia | 2026-09-26 09:34 | avis (source indirecte) ; cohérent avec Dev 15/09 |
| Les joueurs libres (agents libres) arrivent avec jusqu'à 10 d'expérience | uthred9751, #italia | 2026-09-25 12:10 | confirme (connaissance.md : plafond à 10) |
| La blessure : retour à 02:00 du jour indiqué ; 4 kinés ramènent le risque de 2 % (Normal) à 1 % ; 2 kinés « −25 % » | lolek5232, foo_13, chat | 2026-09-30 20:21-20:24 | confirme (skill : kinés −50 % de risque max) ; chiffre 2 % = avis |
| Un joueur de 16 ans blessé la veille d'un entraînement en soft ; plusieurs jeunes blessés en peu de jours ; l'utilisateur embauche 4 kinés | grobarbrate, foo_13, chat | 2026-09-26 18:25, 2026-09-30 20:24, 2026-10-03 18:42 | avis (blessures aléatoires) |
| 6 fautes en 12 min pour un défenseur à 80 de défense et 60 d'athlétisme en soft (19 fautes cumulées sur 8 matchs en soft) | lolek5232, chat | 2026-09-25 20:17-21:17 | avis (aléa) |
| Taille : un joueur à 200 cm joue 4 postes ; à 201 cm au poste de meneur la pénalité est faible mais le bonus de taille du duel disparaît hors de la plage recommandée ; 209 cm SF = pénalité inférieure à 2 % | lolek5232, grobarbrate, chat | 2026-09-30 20:04-20:07, 2026-10-02 19:54-19:55 | complète (chiffres de joueurs, non vérifiés) ; avis |
| Taille de croissance : environ 4 cm par saison pour un jeune ; 207 cm à 18 ans pour un 16 ans de 199 cm | kotryk, #polska | 2026-09-29 19:07 | avis |

### Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Le tableau du manuel : potentiel 7 → 1,5 par entraînement principal, potentiel 8 → 1,6 (cité par foo_13) ; lolek5232 avait dit 1,6 pour pot 8 et 2,2 pour pot 10 | foo_13, lolek5232, chat | 2026-09-30 19:55, 2026-09-16 14:28 | complète : trois valeurs concordantes pour 7/8/10 ; à comparer au §8.3 du manuel dans `basketvibe-entrainement` |
| Un jeune qui gagne +2 en principal au deuxième entraînement est « High probable » (≥ 8) ; un pot 7 ne peut gagner +2 que si la décimale est à .9 ; première semaine peu parlante car valeurs initiales arrondies par erreur | grobarbrate, foo_13, chat | 2026-09-25 11:07-11:09, 2026-09-30 19:53-19:55 | confirme la méthode « historique d'entraînement » (V-20261029-5 / connaissance.md 25/10) ; avis sur le seuil |
| Un jeune à 1-2-1-2 en gain de compétence = 7 ou 8, à confirmer après plus d'entraînements ; 3 entraînements : +4 principal et +2 secondaire, PS 52 → High | lolek5232, joomi1, chat | 2026-09-30 22:15, 2026-10-07 21:40-21:48 | avis (méthode d'estimation) |
| Entraînement : à partir de 70 ralentissement, à partir de 80 « drastique », 0,63 du rythme des compétences sous 70 | marekb9231, kotryk, #polska | 2026-10-06 17:45-17:48 | nouveau (chiffre 0,63 jamais vu ; à vérifier dans le manuel §8) ; contredit lolek5232 (75) |
| Pour un centre : rebond à 80 d'abord, défense, 2P ; pour un pivot « tireur », 3P et 2P en primaires, passe en secondaire (guide) | .doman, uthred9751, #polska, #italia | 2026-10-06 10:23, 2026-10-03 17:28 | avis ; « Stretch Big » cité du manuel |
| Acheter un jeune : prendre le tirage 16 ans 3 étoiles à PS 45 (55 max à 100 % d'académie) est « de luxe » | tankre1792, dcarra., #italia | 2026-09-03 16:44 | confirme (max 55 à 100 % ; vaut dans la tranche du skill) |
| Un jeune acheté pour l'expérience : jouer ≥ 24 min en ligue le fait monter en expérience (2 d'expérience à la vente) | faraone85_69754, #italia | 2026-09-27 19:01, 2026-10-04 08:24 | avis |
| Trois entraînements en 2 semaines pour des prix de vente de 11 points ; un jeune 17 ans 203 cm a gagné 11 points en 5 entraînements (« pas 40 ») | lolek5232, chat | 2026-10-04 16:39 | complète (11 points / 5 entraînements = pot 7-8) |

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Le développeur confirme : le junior est tiré après le saut hebdomadaire du jeudi, avec le nouveau niveau ; passer de 99 à 100 donne le bonus de 100 % ; sans investissement, −5 ; l'argent ajouté après l'apparition du rapport ne change pas les trois candidats | vachacz, #polska | 2026-09-28 08:24 | confirme (connaissance.md 28/09) |
| Promouvoir un jeune relance le décompte de 7 jours du prochain rapport, depuis la date du choix (pas depuis la mise à jour) | faraone85_14932, svg07, #italia | 2026-08-04 12:32-22:51 | nouveau (août, avant le jeudi fixe du 09/08 ; à ne pas appliquer sans vérification) |
| Avec la baisse de −50 % du tirage, seuls les meilleurs tirages sont promus ; certains attendent 100 % pour piocher en semaine 1 de la saison 2 | dcarra., grillanza_60069, #italia | 2026-09-04 14:52-14:55 | confirme |
| 3 étoiles = 8-10 ; 2 étoiles = 5-7 (différence 7 contre 8 possible) | grillanza_60069, svg07, #italia | 2026-09-04 16:50-17:37 | confirme |
| Le rendement d'un tirage à 85 % : 3 étoiles « catastrophe » en compétences ; mieux vaut attendre un meilleur tirage | lolek5232, grobarbrate, chat | 2026-10-02 18:29-18:30, 2026-10-01 | avis |
| À l'académie 66 %, 50 k de tests pour 2 « decent » ; aucun High attendu | foo_13, chat | 2026-09-24 09:32 | confirme |
| Un jeune de 16 ans tiré en premier jour avec 2 étoiles et 2 d'expérience a été vendu 3 M, un autre 49 PS / 3 étoiles payé 3 M | faraone85_69754, dcarra., #italia | 2026-09-27 15:53-17:05 | nouveau (prix) |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Prix 16 ans : 3 M (26/09), 1,5 M pour un 16 ans (Danois, 30/09), 2,1 M pour un 17 ans (01/10), 3 M pour un 16 ans 3 étoiles espagnol (03/10), 3,5 M « record » proposé pour un 17 ans de 203 cm et vendu entre amis ; PG 1,7-1,8 M (27/09), C défense seule 1,5 M, défense + rebond 2 M | grobarbrate, lolek5232, svarog_, chat | 2026-09-26 → 2026-10-03 | nouveau (série de prix ; à comparer au `bv_market_price_known` max 2 894 063 du 22/10) |
| Joueur de 26+ ans : prix qui stagnent, certains en seconde mise en vente à un prix inférieur | lolek5232, chat | 2026-09-27 18:24 | avis |
| Prix des 25-28 ans : Rohan acheté 500 k au début de la saison, vendu 1,2 M le 30/09 ; Trajkovic 27 ans vendu 600 k ; 28 ans payé 800 k utile en coupe | svarog_, grobarbrate, lolek5232, chat | 2026-09-30, 2026-10-04 | complète (revente utile) |
| Revente rapide d'un 16 ans de PS 35 : +96 k en 18 jours, sans taxe selon l'acheteur ; « on ne peut pas revendre avant 7 jours » | uthred9751, grillanza_60069, #italia | 2026-09-23 19:09-20:57 | en doute (le skill dit taxe de 5 % ; l'affirmation « pas de taxe » est un avis) |
| Joueur mis à 500 k « au hasard » (remplaçant moyen) : des enchères ; 16 ans à PS 38 mis à 300 k : sans sens ; 16 ans vers 50 : au moins 1 M | tankre1792, _stefax, #italia | 2026-09-23 21:34, 2026-10-03 17:34, 2026-09-23 22:04 | avis (prix demandés) |
| La nuit les enchères coûtent moins (moins de concurrents) | uthred9751, #italia | 2026-09-23 22:07 | avis |
| PS 40 de 16 ans : 150 k (1re semaine) puis 300 k ; PS 42 : 350 k puis 500 k ; en bêta un joueur très fort à 400 k valait 3 M après une saison | mkeffe, dcarra., #italia | 2026-09-11 09:15-09:20 | nouveau (série) |
| Enchère finale « à l'aveugle » : arrive environ 20-30 minutes après l'échéance d'origine ; une offre scellée, la plus haute gagne | gianlukk76, #italia | 2026-10-02 18:32 | confirme (skill transferts) |
| Plus d'équipe active : les joueurs ne sont pas mis au marché mais effacés quand une équipe inactive devient bot (« les joueurs n'existent plus dans nos matchs ») | lolek5232, antoski.a, chat | 2026-10-09 07:33-08:10 | nouveau (conséquence de l'inactivité) |
| Soupçons de comptes multiples / VPN (Philippines, Japon, Corée) vendant leurs équipes et achetant cher : flux de 1,7 M entre deux clubs signalé | grobarbrate, foo_13, lolek5232, chat | 2026-09-27, 2026-10-02, 2026-10-03 | avis, non vérifié ; cf. règle « transferts entre comptes de la même IP interdits » |
| Selon plusieurs joueurs la 4e division ne participe pas à la coupe ; la demi-finale du 04/10 compte 3 équipes sur 4 de division 3 | lolek5232, foo_13, chat | 2026-10-04 20:49, 2026-10-07 21:36 | complète (coupe pilote de septembre, périmé) |

### Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Début de semaine 1 : 600 k + amicaux 17 k ×5 = 685 k ; académie 100 k, salaires 342 k, il reste ~243 k | _stefax, #italia | 2026-09-02 09:02 | complète (ordres de grandeur post-reset) |
| Recette à domicile ≈ 290 k en division 1 et en 3 ; 312 k à popularité 80 (victoires à domicile) ; pas de gain à jouer dans une division supérieure, seule la popularité compte (DH proche) | gianlukk76, faraone85_69754, grillanza_60069, #italia | 2026-09-27 10:09-11:31 | confirme (skill économie) ; ajoute la mesure |
| Une saison rapporte environ 2 M, donc le capital de départ passe à 2,6 M à la saison 2 (inflation des prix) | grillanza_60069, #italia | 2026-10-04 05:45 | avis |
| Inégalité de calendrier : 3 matchs à domicile sur 4 donnent environ 800 k contre 500 k de moins pour 3 matchs à l'extérieur | dcarra., mkeffe, grillanza_60069, #italia | 2026-09-11 08:32-08:58 | complète (impact 300 à 500 k sur la première quinzaine) |
| Bonus des jeunes de l'académie : 3 quarts-temps par joueur, ~40 k par semaine | foo_13, chat | 2026-10-08 08:52 | confirme |
| Les kinés par 4 coûtent moins qu'une blessure de jeune ; les médecins divisent par deux (avis) | lolek5232, chat | 2026-09-30 20:02-20:22 | confirme |
| Le salaire d'un joueur de 29 points par match : 56 k par semaine | svarog_, chat | 2026-10-07 19:14 | avis |

### Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Coupe pilote : 16 équipes au 02/10 et 8 au 04/10 ; la coupe était jouée en parallèle de la ligue | lolek5232, chat | 2026-10-02 20:13, 2026-10-04 | complète (périmé : coupe actuelle = News 23/10) |
| Premières journées de ligue (07-08/09) : victoires très larges (+45, +52, +36) contre l'équipe aléatoire du départ | grillanza_60069, tankre1792, faraone85_69754, #italia | 2026-09-08 | avis |
| Les amicaux sont « inutiles » face à des équipes à 48 min mais rapportent de l'argent et de l'expérience | _stefax, grillanza_60069, #italia | 2026-09-08, 2026-09-09 | confirme |
| Fatigue de coupe : 25 % de la fatigue d'un match de ligue | dcarra., #italia | 2026-09-12 11:33 | complète (coupe pilote) |
| Mobile : tactiques possibles sur la version mobile ; glisser-déposer du cinq impossible sur la version « bureau » du téléphone | ale92c, grillanza_60069, uthred9751, #italia | 2026-09-22 20:13-21:07 | confirme / complète (UI) |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Rapport d'académie qui ne se met pas à jour (« prochain rapport 19 juillet ») | fabio_76142, dcarra., #italia | 2026-07-19 | confirme (connaissance.md 22/07) |
| Critère de relégation erroné signalé | nightkill79, #italia | 2026-07-21 | complète (ancien) |
| Après un patch, le play-by-play ne fonctionne plus sur tablette | uthred9751, #italia | 2026-10-03 18:00 | nouveau (UI) |
| Composition non enregistrée dans le second quart (mauvais joueur) : « j'étais convaincu de l'avoir sauvée » | uthred9751, #italia | 2026-10-05 20:57-21:01 | complète (bug lineup ou erreur d'utilisateur) |

## Lot 3 : lignes 7994 à 9835 (#pilipinas, #españa, #lietuva, #portugal ; 11/08/2026 au 09/10/2026)

Constat de contrôle : les chiffres de taille, de fatigue, de ralentissement et de multiplicateur de potentiel cités par les joueurs viennent du manuel et sont déjà dans les skills `basketvibe-joueurs` et `basketvibe-entrainement` (comparés ligne à ligne ci-dessous).

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Efficacité offensive d'un joueur de 210 cm : SF −2 %, SG −10 %, PG −17 % ; de 200 cm : C −4 % (cités du manuel §6.2.1) | jorgeac25, #portugal | 2026-10-07 16:48-16:49 | confirme (table du skill joueurs : 210 cm = 98/90/83, 200 cm au C = 96) |
| « Le libellé de poste est une étiquette ; le moteur ne le lit pas ; seule compte l'adéquation de la taille et de la physique à l'emplacement » (manuel cité) | carlomtlopes_69000, #portugal | 2026-09-14 19:43 | confirme (skill joueurs) |
| Focus défensif « Lock » ou « Intense » sur les meilleurs tireurs détourne les tirs vers les joueurs les moins efficaces ; une série de victoires (132-79) après avoir commencé à le faire, contre 50/50 avant ; un autre voit pourtant le joueur ciblé à focus maximum marquer le plus (aucun des siens ne tire) | jorgeac25, nhegas12, #portugal | 2026-09-28 21:29-21:32, 2026-10-07 20:14-20:22 | avis (2 cas opposés) ; la lecture « l'adversaire a monté le focus offensif de son SG, notre point faible » est une piste d'analyse d'adversaire (carlomtlopes) |
| Agressivité défensive : niveau 4 seulement pour les joueurs à plus de 55 de défense, niveau 5 au-dessus de 60 ; 45-55 en niveau 4 pour 12 min au plus ; sous 3 « faute stupide » | chanceler, carlomtlopes_69000, #portugal | 2026-09-17 12:23-12:25 | avis |
| Tir à 3 : après le patch d'octobre, une équipe a tiré 20/30 aux trois points (60 de ses 148 points) ; un joueur a fait 9/13 à 3 points (43 points) ; « avantage au joueur à fort 3P » | chanceler, carlomtlopes_69000, #portugal | 2026-10-03 23:16, 2026-10-05 19:08-19:09 | confirme (V3 : plafond de tirs à 3 levé pour les meilleurs tireurs, connaissance.md 14/09) |
| Joueurs avec un tir à 2 posé « tout à 2 » (passe, 2P) tirent quand même des trois-points (un pivot a pris 5 trois-points sans en marquer) | cobisixer, #españa | 2026-09-14 18:01 | nouveau (avis, 1 cas ; cohérent avec le réglage de choix de tir qui n'est qu'une tendance) |
| Le live d'un match : l'écran de prévisualisation ouvert après le coup d'envoi affiche le score final ; la notification de coupe révélait aussi le résultat (12/09, corrigé 14/09) | chanceler, vansteam, #portugal | 2026-09-12 18:21, 2026-10-05 20:01 | complète (bug de fuite du score encore constaté le 05/10 par clic accidentel sur la prévisualisation) |
| Les équipes inactives/bots jouent leurs 5 titulaires 48 min ; leur pénalité est faible ; au total la pénalité « jouer 3 quarts » vaut environ 5 % de perte en Q4 selon un joueur, puis 15 % (26/09) | jorgeac25, carlomtlopes_69000, #portugal | 2026-09-23 22:33, 2026-09-26 21:04-22:25 | complète (cohérent avec 20 % du 13/09 et v4) ; avis |
| Le moteur défavorise les lancers francs de 48 min : 22-20 en Q4 pour l'équipe qui tourne contre 5×48 min (15-16/09) | faraone85, #italia | 2026-09-16 21:04 | avis (cf. lot 2) |
| Statistiques de rebond : « un pivot à 77 de rebond et 72 de défense aux titulaires, les remplaçants jeunes à 49/36 » ; une équipe qui perd 22-44 aux rebonds a ses deux intérieurs sous 40 | chanceler, nhegas12, #portugal | 2026-09-12 17:41, 2026-09-26 19:03 | avis |
| La fatigue 20-40 : « -3 à -10 % en attaque, -2 à -6 % en défense » (manuel v3) ; les joueurs ne la sentent pas, mais le Q4 des 48 min est dévastateur | shakezito, chanceler, #portugal | 2026-10-05 19:22, 19:30, 20:29 | confirme v3 (skill) ; contredit pour le v4 (voir connaissance.md : −15 % à 40) |
| Défense d'un 182 cm en PF : un joueur de 182 cm a été utilisé à PF par défaut chez un adversaire inactif (blessés) | vansteam, #portugal | 2026-10-05 20:18 | avis (remplacement automatique d'une équipe inactive) |

### Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Formule de fatigue du manuel (cité) : gain = minutes × 0,19 × multiplicateur d'agressivité × (1,5 − 0,008 × endurance) ; récupération chaque nuit = 0,5 + 10 % de la fatigue actuelle, identique pour tous (l'endurance n'accélère pas la récupération) ; remise à 0 à la fin de la saison | carlomtlopes_69000, #portugal | 2026-09-15 18:49-18:50 | confirme (skill joueurs) ; **contredit connaissance.md ligne 26** (« plus l'endurance est basse, plus la fatigue tombe lentement » : seul le GAIN dépend de l'endurance, pas la récupération) |
| Fatigue stabilisée du samedi (extrait du manuel) citée ailleurs ; 2 jours de récupération entre samedi, lundi et mercredi | jorgeac25, #portugal | 2026-09-17 17:46 | confirme |
| Les kinés : 2 kinés = −25 % de risque en match (cité) mais blessures malgré 2 kinés (fatigue 16) ; 3 blessures sans jamais dépasser 19-20 de fatigue ; « probabilité trop haute » | nhegas12, sakota0, #portugal | 2026-10-03 20:27-20:31 | confirme le skill (−12,5 % par kiné) ; avis sur le taux |
| Un joueur n'a jamais été blessé en embauchant le maximum de kinés dès le départ ; un autre en a 4 pour la coupe | montabelas, shakezito, #portugal | 2026-10-07 19:43-19:50 | avis (échantillon faible) |
| Médecins : 2 médecins ramènent la durée d'arrêt à 50 % ; un joueur embauche 2 médecins à chaque blessure et les licencie avant le prélèvement du dimanche, dit-il | arodrigues84, chanceler, nhegas12, #portugal | 2026-10-01 06:59, 2026-09-30 20:29, 2026-10-03 18:25 | **contredit le skill économie** si cela évite le coût : le skill dit « on paie le nombre maximum de chaque rôle employé pendant la semaine » ; chanceler lui-même note « destiné à passer le dimanche avec la dépense de 2 médecins » |
| Un jeune blessé manque l'entraînement du dimanche (« le jeune sans entraînement ») ; la blessure se termine à la date affichée, au début du jour | nhegas12, sakota0, #portugal | 2026-09-30 21:15, 2026-10-01 17:17 | confirme (News 25/10 : entraînement manqué pour blessure) |
| Forme : variation hebdomadaire aléatoire ; un joueur est passé de 5 à 2 en continu malgré un psychologue ; le second psychologue n'ajoute que « 10 % » de chances | nhegas12, sakota0, #portugal | 2026-09-25 21:24-21:32 | confirme (+5 points par psychologue) ; avis |
| Expérience : un joueur libre à 10 d'expérience (24 ans) joué aux quarts 1-2 ; avis que l'expérience compte surtout au dernier quart | nhegas12, chanceler, #portugal | 2026-10-07 12:07-12:17 | avis |
| Les jeunes gagnent l'expérience plus vite que les adultes au même temps de jeu ; les amicaux à 48 min ne valent pas un quart d'un match de ligue | carlomtlopes_69000, #portugal | 2026-10-01 17:37, 17:41 | confirme (skill : plus vite jusqu'à 21 ans ; amical 1/10) |
| Taille cible cachée : un jeune de 16 ans peut gagner au plus +4 cm par saison restante (+20 cm au maximum à 16 ans, +16 cm à 17 ans) ; en moyenne +10 cm | carlomtlopes_69000, #portugal | 2026-09-23 21:30 | confirme (skill : +0 à +4 cm par saison) ; précise le plafond de projection |
| Équipe de départ (message du développeur du 13/08, cité) : ~4 600 points de TSP par équipe (±1 %) ; 5 titulaires de 24-28 ans à potentiel 6-7, TSP moyen 440 (max 490) ; 5 remplaçants de 21-31 ans à potentiel 4-7, TSP moyen 350 (max 440) ; 2 juniors tirés « de l'académie virtuelle à 60 % » (un de 16-17 ans, un de 18-19 ans) ; endurance plafonnée à 60 ; rebond plafonné à 60 pour les PG et SG titulaires | vachacz (cité par carlomtlopes_69000), #portugal | 2026-08-13 15:39 (cité le 2026-10-07 08:13) | **nouveau** (connaissance.md ne cite que l'académie à 80 % du reset) ; source de seconde main |
| Un joueur de l'équipe de départ à 16 ans a monté de +2 à chaque entraînement : potentiel 10 (arodrigues84, montabelas) ; contre « un joueur de l'équipe d'origine n'a jamais potentiel 8 ou 9 » (carlomtlopes_69000) ; jorgeac25 et chanceler pensent que c'est possible à 9 | arodrigues84, montabelas, carlomtlopes_69000, jorgeac25, #portugal | 2026-10-06 22:25, 2026-10-07 07:49-08:01 | **en doute** : le message du 13/08 dit juniors tirés d'une académie à 60 %, donc potentiel 10 rare mais possible ; les vendeurs affirmant un High pour un joueur « d'origine » sont à vérifier (10/08, chanceler) |
| Un 16 ans passé d'un PS de 39 à 39 en 3 semaines = pas de potentiel acceptable (inférence d'un joueur) | daniel3duarte, #portugal | 2026-10-06 18:11 | avis |

### Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Multiplicateurs du manuel cités : potentiel 7 = 1,5 ; potentiel 8 = 1,6 par entraînement principal | foo_13, #lot 2 | 2026-09-30 19:55 | confirme (skill entraînement : 1,50 / 1,60) |
| « À partir de 80 le ralentissement est drastique, seulement 0,63 du rythme sous 70 » | kotryk, #polska | 2026-10-06 17:48 | **contredit le skill** : 80 = ×0,75 ; ×0,63 correspond à 85 ; 70 = ×1 |
| Les compétences basses montent plus vite : une défense à 35-45 en principal semble monter plus vite que les autres | arodrigues84, chanceler, #portugal | 2026-10-07 15:20-16:27 | avis, cohérent avec le skill (décimales, valeurs basses) |
| Première semaine d'entraînement trompeuse : les valeurs de départ n'ont pas de décimales (ex. 55,0) et les suivantes affichent 55,7 / 55,8 ; les très jeunes à compétence faible montent chaque semaine même à potentiel moyen ; 5 semaines pour fixer le potentiel | carlomtlopes_69000, sakota0, #portugal | 2026-09-27 15:57-15:58, 2026-10-06 22:25 | confirme (skill : sensible aux arrondis) ; complète (jeune à compétence faible) |
| 4 entraînements pour juger : le primaire +2 deux fois de suite à compétence proche de 60-70 = potentiel moyen-haut ; un 17 ans a monté +2 chaque semaine (PS 46 à 72 % d'académie) | carlomtlopes_69000, nhegas12, #portugal | 2026-09-13 14:30, 2026-09-20 16:32-16:34 | confirme la méthode ; avis |
| Plan pour un intérieur : défense et rebond d'abord (≈ 70 puis autres), pour un PG passe et dribble ; l'athlétisme en secondaire, seulement après les compétences-clés | carlomtlopes_69000, chanceler, #portugal | 2026-09-18 23:04, 2026-10-06 21:10-21:16 | avis, cohérent avec le skill (athlétisme = catalyseur) |
| « Un joueur d'origine qui monte 1 à 2 compétences par semaine n'est pas forcément High » ; un vendeur a dit High pour un joueur qui montait 1 et parfois 2 | chanceler, sakota0, #portugal | 2026-10-08 22:03-22:12 | confirme la prudence du skill |
| La défense monte plus vite en premier entraînement (impression) | arodrigues84, #portugal | 2026-10-07 12:48 | avis |
| Un joueur de 24 ans qui gagne chaque semaine dans sa compétence principale (potentiel visible) | marekb9231, #polska | 2026-09-13 22:02 | avis |

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Tests : seul le recrutement fait baisser la force de l'académie ; l'envoi aux tests ne la baisse pas | carlomtlopes_69000, #portugal | 2026-09-12 17:49 | confirme (skill académie) |
| Recrutement observé : force 59 % → 35 % après un recrutement (−24 points) ; deux recrutements → 44 % ; un autre : 82 % puis 89 % sans 3 étoiles | carlomtlopes_69000, jorgeac25, nhegas12, #portugal | 2026-09-24 12:08, 2026-09-20 11:14, 2026-10-03 21:20, 2026-10-08 17:35 | complète (le skill dit « environ la moitié » : 59 → 35 = 59 % de la jauge, plus l'investissement de la semaine) |
| Observation : investir 71 000 donne la même force d'académie que 100 000 à ce moment (jauge plafonnée par le niveau actuel) ; à confirmer d'une semaine à l'autre | nhegas12, chanceler, #portugal | 2026-09-13 16:13-16:48 | **nouveau / en doute** : le skill dit « 100 000 maintient 100 % ; 50 000 plafonne vers 89 % » (courbe non linéaire) ; vérifier avec `silver.bv_academy_weekly` |
| Tirages observés par niveau : 72 % → 17 ans PS 46 (monte +2) ; 85-86 % → 16 ans PS 49 / 206 cm ; 59 % → un PG PS 50 à 3 étoiles (chanceler : « bombe ») ; 58 % → PF une étoile non promu | nhegas12, carlomtlopes_69000, jorgeac25, #portugal | 2026-09-20 11:25, 2026-09-24 12:08-12:19 | complète (exemples de tirages) |
| Un recrutement sur 3 étoiles à 3 reprises dans la semaine d'investissement ; « 2 étoiles » 4 fois d'affilée à 58-60 % | nhegas12, sakota0, #portugal | 2026-09-25 21:19-21:23 | avis |
| Promouvoir seulement un 16 ans à 3 étoiles ; ne pas promouvoir un 17 ans sauf bombe ; au-dessus de 80 % ne pas promouvoir un médiocre, sauf en début de saison | carlomtlopes_69000, chanceler, #portugal | 2026-09-12 17:42, 2026-09-13 05:42, 2026-10-08 19:24-19:25 | avis (cohérent avec le skill) |
| Le développeur (cité) : une manière plus simple d'augmenter l'offre de jeunes serait de créer des agents libres de 18-21 ans « moyens », en réservant les 16-17 ans à l'académie, à cause des « prix insensés » | vachacz (cité par chanceler), #portugal | 2026-10-01 16:47 | nouveau (intention, non livrée) |
| Le niveau d'académie fixe ce que l'on peut tirer : « on ne tire pas plus de 55 de compétence » ; PS max 55 à 100 % | tankre1792, lolek5232, #italia | 2026-09-03, 2026-09-30 | confirme (skill) |
| Pour l'académie à 100 %, attendre pour tirer en début de saison (et non en fin) | foo_13, grobarbrate, chat | 2026-10-08 08:57-08:58 | avis |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Frais de vente de 5 % confirmé : mise à 1 010,0 k, reçu 959,5 k | heldermoreno, #portugal | 2026-10-03 17:27 | confirme (skill transferts ; contredit l'affirmation « pas de taxe » d'uthred9751, lot 2) |
| Série de prix : record 1 365 000 pour un SG de 25 ans PS 59 (15/09) ; PF/SG 27 ans (80 de 2P et 80 de défense) vendu 670 k (16/09) ; 28 ans PS élevé 910 k puis plus d'un million (17/09) ; 16 ans PS 47 / 199 cm 1,6 M (23/09) ; 16 ans 176 cm PS 43 : 690 k (23/09) ; 16 ans PS 52 en vente à 5 M (28/09) ; 16 ans PS 50 payé 3 M (28/09) ; 16 ans PS 35 : 500 k et plus (01/10) ; PS 47 ordinaire 360 k (01/10) ; 28 ans PG vendu 660 k (05/10) ; 1 M pour un 25-28 ans vendu par heldermoreno | carlomtlopes_69000, chanceler, jorgeac25, heldermoreno, #portugal | 2026-09-15 → 2026-10-05 | nouveau (prix datés ; l'estimation « 2,5 M » du PG a été démentie par le 660 k réel) |
| Soupçon de transferts truqués entre comptes asiatiques (un joueur banal acheté 60 k puis revendu 850 k à un compte japonais ; 30 transactions) ; équipe de contrôle créée par le développeur (05/10) ; 5 comptes bannis (08/10) | carlomtlopes_69000, chanceler, sakota0, #portugal | 2026-10-03 14:02, 2026-10-05 12:04, 2026-10-08 22:42 | nouveau : les prix du 27/09 au 04/10 peuvent être faussés ; ne pas s'en servir comme référence de marché sans filtre |
| Aucun achat à la hâte : acheteur « fait confiance » au vendeur pour le potentiel ; le vendeur peut mentir ; les historiques d'entraînement antérieurs sont conservés à l'achat (vérification possible) | carlomtlopes_69000, jorgeac25, sakota0, #portugal | 2026-10-06 22:13, 2026-10-08 22:09-22:20 | confirme le skill (historique d'entraînement visible) |
| Durée d'une mise en vente ~48 h (Charazay 72 h) ; enchère maximale modifiable après avoir pris la tête ; les enchères automatiques ne sont pas comptées dans le compteur d'enchères affiché | sakota0, chanceler, #portugal | 2026-10-03 16:59, 17:38, 20:40, 22:05 | confirme (skill transferts) ; compteur d'enchères = nouveau (UI) |
| Enchère : chaque offre dans les 2-3 dernières minutes prolonge ; puis phase finale à l'aveugle (« lance cego ») | carlomtlopes_69000, heldermoreno, chanceler, #portugal | 2026-09-16 14:47, 2026-09-23 21:36, 2026-10-05 19:15 | confirme |
| Les propriétaires de jeunes tiennent le prix : un 28 ans a été sous-estimé (estimé 700-900 k, vendu 660 k) ; revendre un 28 ans est « win now » seulement | jorgeac25, carlomtlopes_69000, #portugal | 2026-09-16 13:43, 2026-10-03 13:37, 2026-10-05 14:43 | avis |
| Stratégie « trader » : mettre en vente à un prix supérieur au marché (peu de frais de mise en vente) | jorgeac25, #portugal | 2026-10-01 18:12-18:14 | avis |
| Les 16 ans valent moins quand ils viennent de l'équipe d'origine (potentiel moyen) ; 25 16 ans vendus récemment : 10 achetés par des équipes portugaises | carlomtlopes_69000, #portugal | 2026-10-06 18:07-18:11, 21:53 | avis |

### Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Conseil de départ (août) : minimum de 10 joueurs pour économiser les salaires ; un salaire de 11 000 et plus = qualité de titulaire ; toujours régler la tactique avant chaque match | shiftyy25, #pilipinas | 2026-08-11 10:46 | en doute (pré-reset, minimum devenu 8) ; avis |
| Revenus : un match à domicile payait « toutes les factures de la semaine » à 50 k d'investissement académie (début de saison) | chanceler, #portugal | 2026-09-13 14:46 | avis |
| Les jeunes : salaires bas à 16 ans ; une saison de revenus ≈ 2 M ; un joueur qui joue 20 min sur une saison donne ≈ 88 k de bonus de formation (skill) | carlomtlopes_69000, grillanza_60069, #portugal, #italia | 2026-09-20 11:23, 2026-10-04 05:45 | confirme |
| Sponsor : proposition communautaire (prime à l'objectif selon l'attente du manager) ; le développeur a une proposition similaire | nhegas12, sakota0, chanceler, #portugal | 2026-10-02 15:50-21:07 | complète (idée) |
| Personnel : un joueur préfère ne rien embaucher tant qu'il n'y a pas de blessure ; les médecins en cas de blessure | carlomtlopes_69000, chanceler, #portugal | 2026-09-12 17:35 | avis |

### Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un amical programmé demande une date libre chez les deux ; l'invitation expire à une date limite ; l'amical est placé à la première date commune ; pas d'amical la veille/le jour de match de ligue sans le vouloir | chanceler, sakota0, #portugal | 2026-09-12 17:53, 2026-09-17 15:44-15:55 | confirme (skill saison) |
| Le buzzer : matchs de ligue à 19:00 « nos » (heure du Portugal), entraînement à 07:00, coupe à 21:00 | carlomtlopes_69000, #portugal | 2026-09-15 23:05 | complète (heure locale non convertie ; le skill saison fait foi) |
| Les joueurs de division 4 : un utilisateur inactif devient bot après un nombre de jours ; les 2e et 3e de la division inférieure peuvent monter ; une division 3.6 comptait 5 équipes inactives | carlomtlopes_69000, nhegas12, #portugal | 2026-09-26 06:52-06:57, 2026-10-05 18:23-18:55 | confirme (skill saison) |
| Les joueurs « inactifs depuis août » se lisent à la date de dernière connexion (03/08, 22/08/2026) | nhegas12, vansteam, #portugal | 2026-09-26 19:37, 2026-10-05 20:18 | nouveau (indice : date de dernière connexion visible) |
| Un utilisateur dont l'équipe est fermée : joueurs effacés (équipe passée en bot) | lolek5232, antoski.a, chat | 2026-10-09 08:10 | nouveau |
| Coupe : le match de coupe n'est pas visible en direct pour les non-participants (09/10) ; pas de lien « watch » | foo_13, carlomtlopes_69000, chat, #portugal | 2026-10-09 18:39, 18:44 | complète |
| Début de saison à 12 équipes (ligues de 12) | heldermoreno, chanceler, #portugal | 2026-09-28 21:35 | confirme |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Changer la tactique générale ne met pas à jour la tactique du match déjà planifié : il faut ouvrir le calendrier, choisir le match et sélectionner la tactique créée (deux nouveaux joueurs n'ont pas joué) | nhegas12, chanceler, jorgeac25, #portugal | 2026-09-20 20:36-21:00, 2026-09-21 12:15-12:16 | **important** : complète le bug « sauvegarde des tactiques après transfert » (19-21/09) ; vérifier à chaque match que la tactique du match (pas seulement la générale) est celle voulue |
| Une équipe mise en sommeil joue avec des remplaçants absurdes (182 cm au PF) ; remplacement automatique par défaut | vansteam, #portugal | 2026-10-05 20:18 | avis |
| Compteur d'enchères qui n'affiche que les offres manuelles (9 affichées pour 15 réelles) ; offre automatique réglable ; utilisateur ne peut pas ajuster à l'avance | sakota0, #portugal | 2026-10-03 20:40-20:46 | nouveau (UI) |
| Un utilisateur a pu envoyer un amical un jour où l'adversaire avait déjà 10 amicaux programmés | nhegas12, #portugal | 2026-10-03 20:49-20:51 | nouveau (hypothèse de bug) |

## Synthèse du lot 3
- #pilipinas et #lietuva : bavardage, aucune donnée de règle ; seules les lignes de #pilipinas du 24/09 donnent des signes de potentiel (premier entraînement +1 secondaire = pot 10, avis).
- #españa : 3 faits (accepter un jeune baisse l'académie, l'envoi aux tests non ; 3P pris malgré réglage à 2P ; amicaux et fatigue en août).

## Synthèse de la lecture (lignes 5001 à 9835 = 4 835 lignes lues, dans l'ordre, sans échantillon)

Entrées par thème (tous lots) : Tactique/moteur 51 · Joueurs/fatigue/forme 31 · Entraînement/potentiel 24 · Académie 21 · Transferts/prix 27 · Finances/sponsor/personnel 17 · Calendrier/coupes/amicaux 15 · Bugs 12 = 198.

Cinq trouvailles qui changent une décision :
1. **Tactique du match ≠ tactique générale** (#portugal, 20-21/09) : modifier la tactique générale ne met pas à jour un match déjà planifié ; deux joueurs achetés n'ont pas joué. Vérifier la tactique de chaque match dans le calendrier.
2. **Prix du marché 27/09 → 04/10 faussés** par des transferts entre comptes asiatiques suspects (60 k → 850 k ; 5 comptes bannis le 08/10, #portugal) : ne pas caler nos plafonds d'enchère sur ces ventes.
3. **Équipe de départ** (message du développeur du 13/08, cité) : titulaires 24-28 ans à potentiel 6-7, remplaçants 4-7, 2 juniors tirés d'une académie virtuelle à 60 % ; un joueur « d'origine » vendu comme High est donc à traiter comme potentiel moyen sauf preuve par l'historique d'entraînement (la preuve se lit aux 4-5 premiers entraînements).
4. **Frais de 5 % confirmés** (1 010,0 k vendu, 959,5 k reçu, #portugal 03/10) ; revente rapide possible (7 jours) mais la marge doit couvrir les 5 %.
5. **Défense agressive et lancers francs adverses** (#chat 29-30/08 et 04/10 ; v3, avis) : une équipe en agressif concède 19 lancers francs contre 6 ; l'agressivité ne rapporte que si les défenseurs sont bons (cohérent avec « double tranchant »).

Contredit ou corrige (skills et connaissance.md) :
- connaissance.md ligne 26 : « plus l'endurance est basse, plus la fatigue tombe lentement » ; le manuel cité (#portugal 15/09) et le skill disent que l'endurance joue sur le gain de fatigue, pas sur la récupération (0,5 + 10 % pour tous).
- Skill entraînement : kotryk (#polska 06/10) dit « ×0,63 dès 80 » ; le skill fait foi (×0,75 à 80, ×0,63 à 85). Pas de changement à faire.
- Skill économie (« on paie le nombre maximum de chaque rôle employé pendant la semaine ») : des joueurs disent licencier les médecins avant le dimanche pour ne pas payer ; chanceler constate le contraire. À vérifier sur une semaine réelle avant d'adopter le geste.
- Académie : « 71 000 donnent la même force que 100 000 » (nhegas12, 13/09) ; non conforme à la courbe du skill ; à tester avec `silver.bv_academy_weekly` avant de baisser l'investissement.
- Taxe de revente : uthred9751 affirmait « pas de taxe » (23/09) ; démenti par heldermoreno (03/10).
- Les chiffres de taille (210 cm : SF −2 %, SG −10 %, PG −17 %), de fatigue v3 (20-40 : −3 à −10 % attaque), de multiplicateurs de potentiel (7 = 1,5 ; 8 = 1,6 ; 10 = 2,2) et de formule de fatigue cités par les joueurs sont exactement ceux des skills (confirmé).

Aucun skill ni `connaissance.md` n'a été modifié.

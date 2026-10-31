# Lecture joueurs BasketVibe — partie 1 (lignes 1-5000 de discord_BasketVibe_export.txt)

Veille, 2026-10-31. Lecture message par message. Période de cette partie : 2026-05-31 -> (voir fin). Beaucoup d'éléments sont d'AVANT le reset annoncé le 2026-08-11 (moteur v1/v2, économie de beta) : marqués « pré-reset ». Un avis n'est jamais une règle. Statut = vs `connaissance.md`.

## Avancement
Lignes 1-800 lues (2026-05-31 -> 2026-08-13).

## Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| BMI/poids sans effet sur la performance (v1) ; moteur calibré par une app dédiée | vachacz, #general | 2026-06-20 18:26 | confirme (v1 déjà noté) |
| Dev : un match n'est jamais 100-0 ; il simule le même match jusqu'à 1000 fois (snapshots de roster fatigue incluse) pour juger chance vs bug | vachacz, #general | 2026-06-27 14:02 | confirme (connaissance : 1 000 simulations) ; ajoute la date de création de l'outil |
| Avis : un score final ne prouve pas le moteur, regarder comment le match est joué (53 lancers francs contre soi = suspect) | grobarbrate, #general | 2026-06-27 14:19 | avis |
| Rebonds v2 : la taille pèse beaucoup plus qu'en v1 ; règle de proximité du cercle (un PG, loin du cercle, a moins de chances) ; rebond de tous les postes « travaillent ensemble » mais le dev refuse de dire si le rebond partout vaut mieux que 2 grands | vachacz, #general | 2026-07-13 15:50-15:58 | confirme (matchup/rebonds) ; la question « rebond d'équipe » reste sans réponse officielle |
| Avis chiffré (lecture du manuel) : au-dessus de 2 m, +1,8 % par cm ; rebond 80 vaut 66 à 190 cm, 80 à 200 cm, 94 à 210 cm | lucadrago5, #general | 2026-07-13 17:29 | avis ; à comparer au manuel (non vérifié ici) |
| Avis : pénalité de poste « 5 % SG, 7 % SF » | grobarbrate, #general | 2026-07-15 21:17 | contredit (dev : aucune pénalité de poste hors rebonds, v2) — avis erroné |
| Pénalité 48 min : « déjà là, ~8 % » (28/07) ; joueurs réclament 15 % ou plus (« 50 % min » pour un PF-C sur PG) ; test de 15 % suggéré | vachacz (8 %), grobarbrate, lucadrago5, lordgohan_67459, #general | 2026-07-28 10:47-15:42 | confirme (skill : 8 % -> 10 % -> 12,5 % -> 20 %) |
| Constat joueurs : équipes de bots/inactifs à 5 x 48 min battent des équipes humaines ; Q4 meilleur que Q1-Q3 pour des équipes à 48 min (svarog_) | grobarbrate, szulim90, svarog_, #general | 2026-07-28, 2026-08-01, 2026-08-02 | complète (cause du nerf 48 min) ; pré-v4 |
| Avis : 3P% trop haut (40-60 % à 30-40 tirs, vs 35 % réel) | txetx, #general | 2026-07-28 09:46 | complète (v2 ; 3P% élevé déjà noté en v3) |
| Tirs : un tireur SG < 190 cm « tout 3P » ne prend presque pas de 3P (30 FG, 7 à 3P ; 1 seul 3P un soir) ; soupçon : la taille joue | svarog_, #general | 2026-08-01 19:02, 08-02 07:50 | nouveau (avis, une observation) — pas de réponse dev |
| Directives = un seul joueur par poste et par quart-temps ; minutes granulaires refusées par le dev (gros changement UI, votes contre) ; depth chart sert de 6e homme | vachacz, #general | 2026-07-29 20:27, 2026-08-08 10:26 | confirme (skill tactique) |
| Dernier passeur / compétences utiles par poste non documentées ; débats d'avis : « tout poste a besoin de tout » | airgk32, rarz09, grobarbrate | 2026-07-21 | avis |
| Joueurs perçus : un 190 cm sans rebond inutile au poste ; PF-C placé au poste PG avec 73 3P : bonus de taille > 8 % | lolek5232 | 2026-07-28 10:51-10:52 | avis, une observation |

## Joueurs / fatigue / forme / expérience
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Endurance 20 -> 20 min de jeu = fatigue 77 (v1, jugée trop forte) | dcarra., #general | 2026-06-29 04:35 | nouveau (mesure pré-reset, v1) ; ordre de grandeur cohérent avec « endurance basse = fatigue rapide » |
| Match v1 : équipe 5 joueurs x 48 min avec endurance 21-40 gagne de ~50 points ; l'auteur perd tout en soft ; joue ses amicaux en soft avec les moins bons et gagne | grobarbrate, #general | 2026-07-06 23:48-00:07 | complète (v1 ; cause du nerf) |
| Expérience : « croissance linéaire, impact non linéaire : les 10 premiers points comptent plus que 80-90 » ; table à ajouter au manuel | vachacz, #general | 2026-08-02 10:19 | confirme (skill joueurs) |
| Expérience de départ très inégale (20+ vs 0-1 à âge égal) en saison 1 | svarog_, cimi | 2026-07-16 14:00 | confirme (génération cassée pré-reset) |
| Compétences de joueurs ont des décimales (51,99 -> 53 en un cran) | vachacz « I confirm », #general | 2026-08-02 08:50 | confirme (skill : décimales cachées) |
| Blessures : date de retour visible dans les notifications (navigateur) ; pas sur mobile | shiftyy25, svarog_, lolek5232 | 2026-07-13, 2026-08-03 | complète (interface) |

## Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un joueur de potentiel moyen : « 12 compétences par saison à 16 ans » (calcul d'avis) | airgk32, #general | 2026-07-15 13:16 | avis, pré-reset (réforme 10/08) |
| Indice de potentiel : 2 compétences qui « poppent » en une semaine = au moins pot 6 ; une 2e série dans la même compétence = piste pot 9-10 ; décimales : un saut 51,99 -> 53 peut être un faux signal | dcarra., hahehi0188, grobarbrate, #general | 2026-08-02 08:44-09:04 | avis (heuristique de tests, non chiffrée) |
| « Training camp » : les recrues (rookies) reçoivent un petit boost hors saison (+1 sur six compétences à la montée en saison), choisi par le jeu | vachacz, #general | 2026-07-21 11:47 | nouveau (périmé après réforme du 10/08 ? en doute) |
| Entraînement du samedi : un junior tiré en semaine 1 pourrait avoir 8 séances ; l'académie doit tomber avant le samedi -> jeudi 9h retenu | lolek5232, vachacz, #general | 2026-08-06 11:34-12:13 | confirme (jeudi 09:00) ; « 8 séances possibles pour un junior tiré en semaine 1 » complète |
| Rookies : « de 40 à 70 il faut 3-4 saisons à 7-8 compétences primaires/saison » | grobarbrate, #general | 2026-07-20 20:37 | avis, pré-reset |

## Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Changer le niveau d'académie ne renouvelle pas le rapport le même jour ; le dev « égalise » | grobarbrate, vachacz, #general | 2026-07-20 15:32-15:35 | complète (comportement pré-reset) |
| Avant le reset : « signer baisse la jauge de 50 % » (ex. 75 % -> 50 %, 3 semaines pour revenir) ; avis : « il vaut mieux attendre qu'investir 1,2 M pour monter la jauge » | grobarbrate, dcarra., #general | 2026-07-29 12:49-14:14 | confirme (-50 %) ; l'avis « pas rentable de monter à 100 % pour un junior à 2 M+ » = avis |
| 1 pull à 50 % -> la jauge tombe à 25 % puis +10 ; max d'investissement observé 80 k puis 100 k | grobarbrate, airgk32, #general | 2026-07-01 | confirme (-50 %) |
| Avis : « 25k de test de potentiel pour des recrues déjà tirées : refusé, « tu sauras dans 3-4 semaines » » | grobarbrate, vachacz | 2026-07-30 20:28-20:30 | confirme (tests à 25 000 sur les juniors de la semaine seulement) |
| Avis : « il y a un pot élevé dans pratiquement chaque lot de trois » (txetx) ; « devrait être plus rare » | txetx, #general | 2026-07-31 07:02 | avis ; à contrôler vs table du skill |
| Rapport d'éclaireur : tirage « Sunday Academy Day » proposé puis Thursday 9:00 ; rapport hebdo quel que soit le tirage | vachacz, trainerrox, #general | 2026-08-06, 2026-08-08 | confirme |
| Après le reset : académie à 80 % pour tous, pull = tâche d'onboarding | vachacz, #general | 2026-08-12 16:57 | confirme |
| Régions: 16 ans = ~3 saisons d'entraînement jusqu'à 19 ans (avis) | airgk32 | 2026-07-16 09:19 | avis |
| Juniors vs 100 % : « prise à 75 %, reb et BH inversés » -> 50-50 (avis : à 100 % c'était un pull sûr) | dcarra., #general | 2026-07-29 12:48 | avis |
| Joueur de 16 ans max de 480 compétences au total (6 x 8), compétence max 60 à 16 ans (pré-reset) | lolek5232, #general | 2026-07-16 08:16, 08:47 | confirme (pré-reset) |

## Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Prix observés pré-reset : premier > 1 M le 16/07 ; transfert à 1,7 M (20/07) ; 21 ans PG Willems à 1,6 M (airgk32 par 1 M de plus) ; C polonais « 950 k » pour une bonne cible | grobarbrate, dcarra., airgk32, #general | 2026-07-16, 2026-07-20 | complète (prix pré-reset, économie remise à zéro) |
| Salaire d'un joueur change-t-il à l'achat ? question sans réponse | svarog_ | 2026-07-20 16:37 | en doute |
| Enchère maximale : la somme des enchères max actives bloquait le solde même quand l'enchère était dépassée -> bug, corrigé le 26/07 ; règle « si tu fais une enchère maximale tu dois avoir le cash » | dcarra., grobarbrate, vachacz, #general | 2026-07-26 10:47-11:22 | confirme (skill : l'enchère max ne peut pas dépasser le solde) ; bug corrigé |
| Phase finale : enchère « 3 minutes supplémentaires » mal comprise par un enchérisseur (1,5 M -> 1,6 M) | s6o7537, dcarra. | 2026-07-25 04:59 | confirme (anti-snipe / phase à l'aveugle) |
| Durée du marché : 4 jours -> 2 jours (23/07) | vachacz, #general | 2026-07-23 12:12, 07-25 | confirme |
| Agents libres : dev préfère les supprimer ou les utiliser pour créer des juniors | vachacz, #general | 2026-07-27 17:11 | complète (en doute, jamais annoncé) |
| Joueur à 0 : « vendre pour 0 n'est pas vendre » ; minimum de mise en vente de 10 k suggéré | lujo2486 | 2026-08-12 19:17 | avis |
| Reset : joueurs gardés = « transferts vers alpha = créer de l'argent » (argument de lolek5232) | lolek5232 | 2026-08-13 07:21 | avis |

## Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Économie T2/T3 alignée sur T1 ; compensation de 400 k pour les clubs T2-T3 (2026-07-07) | vachacz, #general | 2026-07-07 19:50 | complète (pré-reset) |
| Sponsor annuel 500 k -> hebdo ; compensations aux nouveaux ; solde négatif = interdiction de transfert, tests de juniors bloqués | vachacz, #general | 2026-07-22 09:18, 09:25 | confirme |
| Recette d'amical : domicile = extérieur (14/07) | vachacz, #general | 2026-07-14 10:30 | confirme |
| Avis : matchs à l'extérieur en série -> trésorerie négative (5 matchs à l'extérieur d'affilée) | grobarbrate, dcarra. | 2026-06-29, 2026-07-05 | avis |
| Investissement académie : 100 k hebdo observé ; avis « si on ne mise pas gros, autant mettre 0 » | lucadrago5 | 2026-07-12 17:43 | avis |

## Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Idée d'amical : un non coté, un par jour à 8h Europe ; sans fatigue/exp/stats (v-juin) | vachacz, #general | 2026-06-26 21:09 | complète (devenu 10 % exp/fatigue) |
| BV Championship / coupe de tous les humains envisagée (23/07) | vachacz, grobarbrate | 2026-07-23 22:30-22:49 | complète (devenu BV Cup puis coupes nationales) |
| Reset annoncé : après saison 1/2 initiale ; roster de départ = 5 « décents » par poste + 7 plus faibles aléatoires ; inactivité 30 ou 45 jours | vachacz, #general | 2026-08-11 18:25 | confirme |
| Fuseau APAC Asia/Tokyo, 20:00 | vachacz | 2026-08-08 10:20 | confirme |

## Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Tactiques non fonctionnelles / presets disparus (juillet) | grobarbrate | 2026-06-27 21:54, 07-07 00:12 | complète (historique) |
| Remplaçant blessé affiché comme titulaire à chaque quart (alors qu'il n'a pas joué) ; deux SG dans le rapport | svarog_ | 2026-07-18 18:44 | confirme (bug déjà noté « lineup de quart faux ») |
| Résultat de match visible avant la fin en direct (spoiler) ; notification "league win" casse le suspense | fabio_87838, svarog_, lolek5232 | 2026-07-09, 07-27 | complète (corrigé ensuite, mode sans spoiler) |
| Bug enchère max (voir Transferts) | | 2026-07-26 | confirme |
| Fautes/lancers : 45 FT vs 6, 53 FT contre soi | airgk32, grobarbrate | 2026-07-01, 06-27 | avis pré-reset |

---
# BLOC B — lignes 801 à 1810 (2026-08-13 -> 2026-09-19), même grille par thème

## B1 Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Mesure du dev sur ~100 matchs de ligue : la différence moyenne au Q4 d'une équipe 5 joueurs x 48 min est +5,12 à domicile et +2,88 à l'extérieur (moyenne : on trouve aussi -5) ; le dev refuse de durcir davantage (« Doncic à 48 min reste Doncic », un 5 de fer plus fort que l'adversaire doit pouvoir gagner) ; pénalité presque doublée le 12/09 alors qu'il visait des paliers de 2,5 % | vachacz, #general | 2026-09-12 20:59-21:17 | complète (chiffre nouveau ; v3 d'avant le 13/09) |
| Le dev a relancé le match d'un joueur 1 000 fois : « tu gagnais 98 % » malgré un 18-32 au Q4 contre 3 joueurs à 48 min | vachacz, #general | 2026-09-07 20:49 | confirme (aléa du Q4) |
| Même série : les victoires de grobarbrate sans tactique le 24/08 : le moteur donnait 68 % ; les 4 matchs précédents avec tactique : 94, 86, 63, 82 % | vachacz, #general | 2026-08-24 21:55 | nouveau (n = 5, ne prouve pas l'effet de la tactique) |
| Avis : un joueur à 48 min est contré facilement par la tactique (cinq connu, mêmes minutes) | elemke., #general | 2026-09-12 21:18 | avis |
| Après le reset, 3P% très bas : grobarbrate 5/29, 8/34, 7/32, 7/23 (~20 %) alors qu'avant le reset même de mauvais tireurs marquaient ; elemke 40 % (un match à 27 %) ; marekb9231 : un tireur à 3P élevé mais balle en main faible rate (avis) ; correction « 3P mineure » du v3 le 16/09 | grobarbrate, elemke., marekb9231, vachacz, #general | 2026-09-13 20:52-21:05, 2026-09-16 19:34 | complète (3P% bas au moment de l'écart ; correction v3 du 16/09 connue) |
| Fautes : pas de corrélation avec la défense, seulement avec l'agressivité défensive | vachacz, elemke., #general | 2026-09-14 16:22-16:24 | confirme |
| Défense agressive : 2 joueurs x 12 min = 2 blessés (08/19) ; fautes et lancers « dans tous les sens » (28/08) ; 8 joueurs x 24 min en agressif ont perdu de 20 face à un 2 joueurs x 48 min (29/08) ; un test contre un bot à fatigue 50 presque perdu (28/08) | grobarbrate, svarog_, lolek5232, #general | 2026-08-19, 08-28, 08-29 | avis (aucun gain observé de l'agressif ; cohérent avec « double tranchant ») |
| Prolongation : les joueurs du Q4 jouent aussi la prolongation (le cinq du depth chart n'est pas repris) | jagmn, insartin, #general | 2026-09-17 06:53-10:32 | complète (bug OT cité ; connaissance : lineup propre à l'OT déjà annoncé) |
| Avis : sans fréquence de tir par joueur, « le jeu est un générateur de nombres aléatoires » ; le dev décide d'implémenter un focus offensif | aaaoooaaaa / vachacz, #general | 2026-09-06 16:35 | confirme (origine du focus offensif) |
| Coupe pilote : l'équipe au TS le plus faible joue à domicile ; l'avantage du terrain n'est pas retiré | vachacz, #general | 2026-09-03 15:50 | confirme (déjà noté et périmé) |
| Q4 : 48 min « pénalité de 10 % pour le dernier quart » | vortexraijin, #general | 2026-09-05 14:06 | confirme (8-12,5 % selon la date) |
| Un joueur de petite taille aux postes intérieurs n'est pénalisé qu'aux rebonds ; tout poste jouable | cimi, #general | 2026-09-05 14:05 | confirme (skill) |
| Une équipe de 5 x 48 min qui joue 3 matchs de suite : finit avec un 18-32 au Q4 contre soi puis gagne de 36 ; un autre voit un Q4 37-17 pour lui (effet de la fatigue constaté le 14/09) | faraone85_69754, #general | 2026-09-07, 2026-09-14 | confirme (aléa fort sur le Q4) |

## B2 Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Récupération : fatigue 20 -> -2,5 par jour (avis) ; « la fatigue baisse plus vite quand elle est haute, il y a une table » ; « fatigue 20 a un impact mineur » ; histogramme de la fatigue des équipes humaines présenté par le dev | grobarbrate (avis), vachacz, #general | 2026-09-13 12:52-13:31 | confirme (table du manuel, v3) ; le -2,5/jour est un avis |
| Fatigue de coupe = 25 % d'un match de ligue ; fatigue d'amical = 1/10 de la ligue (avis) ; un amical n'empêche pas de récupérer la nuit | aeolian06, vortexraijin, #general | 2026-09-09 16:04, 2026-09-15 13:28 | avis (pour la coupe pilote ; périmé : News 23/10 coupes sans fatigue) |
| Repos du dev : « le repos ne dépend pas de l'endurance, je crois » ; repos manuel pour toute l'ligue possible à un clic | vachacz, #general | 2026-09-09 16:02, 2026-09-13 13:31 | confirme (en doute déjà noté) |
| Forme : tend à revenir vers le milieu (3 monte, 8 baisse) ; un joueur peut jouer en vedette et voir sa forme baisser | grillanza_60069, cimi, #general | 2026-09-05 14:32-14:44 | avis (non confirmé par le dev) |
| Un mélange de 5 x 48 min en début de saison peut donner 2-3 bonnes semaines puis chute (fatigue + blessures) | random_player_123., #general | 2026-09-01 09:16 | avis |
| Un 17 ans sur le marché : on ne sait pas s'il vient de l'académie (idée : date de naissance) ; homegrown = tiré de l'académie, icône maison | elemke., grillanza_60069, vachacz, #general | 2026-09-07 14:00, 2026-08-29 09:24 | confirme (homegrown) |
| Bonus homegrown : la coupe ne compte pas | vachacz, #general | 2026-09-10 21:19 | nouveau (cohérent avec News 23/10 : coupes sans revenu) |
| Postes : « Hauteur importante, pas le poste » : PG joués par 4 joueurs hauts | grobarbrate, #general | 2026-08-30 19:54 | avis |
| Après reset, résultats d'amicaux déséquilibrés (52 points d'écart avec un cinq contre des remplaçants) : 5 meilleurs >> banc reçu | lujo2486, random_player_123., #general | 2026-09-01 09:00-09:16 | avis (cohérent : banc de départ faible) |
| Défense : cimi estime que « le mélange de fatigue 36+ fait mal ; au début de saison jouer 48 min peut améliorer ses chances » | cimi, #general | 2026-09-05 14:04 | avis |

## B3 Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Après reset, les compétences de départ étaient en xx,00 (aucune décimale) : tout joueur qui « pop » en semaine 1 révèle son potentiel ; seuls 3 « pops » à l'équipe de grobarbrate ; avis lolek5232 : pot 3 = le plus bas du seeding, pot 4+ devaient tous « pop » (multiplicateur 1x) | grobarbrate, airgk32, lolek5232, vachacz, #general | 2026-09-06 08:15-08:33 | nouveau (indice de potentiel réel au 1er entraînement post-reset ; avis sur « pot 4 = 1x » non confirmé) |
| Le dev : l'algorithme d'âge existe depuis la saison 2, il ralentit les 25+ ; majorité des joueurs pot 6-7 ; 25 ans pot 6 = 9 compétences/saison ; pot 10 = +26 dans deux compétences à 16 ans ; simulateur du dev : 6 pot équilibré à 16 ans = 16,2 compétences/saison (manuel : ~15), 25 ans = 9,9 (manuel : ~9) | vachacz, random_player_123., #general | 2026-09-06 08:29-10:35 | confirme (skill §8.3) ; la différence manuel/simulateur est nouvelle (+1 environ) |
| Les juniors de l'académie sortaient aussi en xx,00 (bug : on repère un pot 10 au premier entraînement) ; le dev répond « je corrige en décimales » | aaaoooaaaa, grillanza_60069, vachacz, #general | 2026-09-06 09:47-10:13 | nouveau (bug corrigé ; vérifier si nos juniors affichent des décimales) |
| Après calibrage d'âge (16/08) un C de 27 ans pot 9 n'a gagné aucune compétence ; un 23 ans +2 = probable pot 8-9 ; un +3 à 16-18 ans = pot 10 (avis) ; 17 ans +2 = au moins pot 5 | dcarra., random_player_123., #general | 2026-08-16 08:34-10:10 | avis (heuristiques d'avant la table d'âge) |
| Réforme entraînement 16/08 : « 8 entraînements/saison, 16-18 ans = 9 pops en compétence principale » (avis) ; potentiel « retravaillé » ; chapitre 6.1 du manuel = meilleures compétences | random_player_123., dcarra., #general | 2026-08-16 08:46, 09:13 | avis |
| Nouveau PS (TSP) : top joueur ~555, deux 20 ans à 550 ; ses meilleurs joueurs à 61-65 | vachacz, svarog_, random_player_123., #general | 2026-08-16 16:19, 18:18 | complète (pré-reset ; échelle de PS) |
| Formule PS volontairement simple (somme), ne pénalise pas les écarts ; avis : devrait compter plus les compétences > 70 | vachacz, random_player_123., #general | 2026-08-16 21:12-21:16 | confirme (PS = indicateur) |
| Seeding du reset : somme des TSP de toutes les équipes entre 4 554 et 4 646 (4 600 +/-1 %) ; TS de club va de 51 à 55 selon les ligues (calcul sur les 8 meilleurs, pas 12) ; banc potentiel 4-7 (13/08) | vachacz, kembb, rems3132, #general | 2026-08-31 15:50-17:15, 2026-08-13 16:01 | complète (genèse des effectifs de départ) |
| Un 16 ans vit ~3 ans réels ; hauteur de croissance : ~10 mois pour atteindre la taille finale (avis) | vachacz, pijonghoo, #general | 2026-09-04 20:50, 09-05 04:45 | confirme (calcul) |
| Entraînement du samedi ; un junior tiré en semaine 1 a 8 séances (lolek5232, 06/08) | lolek5232, #general | 2026-08-06 | confirme (voir bloc A) |

## B4 Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Départ post-reset : académie à 80 %, tirer un junior est une tâche d'onboarding | vachacz, #general | 2026-08-12 16:57 | confirme |
| Les nouvelles équipes (créées en cours de saison) ont eu un rapport instantané (2 juniors de 16 ans au lieu de 3) : bug | grobarbrate, rene779, #general | 2026-09-02 23:12-23:24 | nouveau (bug de création d'équipe) |
| Avis : à 100 % d'académie, mieux vaut attendre une semaine pour signer ; un 3 étoiles refusé par un enchérisseur | usylum, vortexraijin, #general | 2026-09-17 00:13 | avis |
| Avis de cimi à un débutant : 100 k d'académie « oui, tout de suite, pour tirer un bon junior tôt, ils perdent moins d'entraînement » | cimi, #general | 2026-09-05 14:04 | avis |
| Tests de potentiel : High = 8-10 (pour les tests académie) | cimi, #general | 2026-09-05 14:09 | confirme (skill) |
| Rapport d'académie 03/09 puis jeudi (03/09 fixé, 10/09 suivant) | vachacz, grobarbrate, #general | 2026-08-31 16:38-16:48 | confirme |

## B5 Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Records de prix post-reset : ~1,2 M (dev, 17/09) puis 1,365 M (carlomtlopes) | vachacz, carlomtlopes_69000, #general | 2026-09-17 22:28-23:00 | nouveau (plafond observé 17/09 ; nos données : max 2 894 063 au 22/10) |
| Prix de comparaison : un joueur de même poste et même note qu'un C « à 30 rebonds » se vend 500 k+ ; un SF de 61 de note à 24 ans est jugé « bradable » | vincent1467, k1tzera, #general | 2026-09-07 18:27-18:29 | avis |
| Revente : délai de 15 jours ramené à 7 (14/09) ; idée d'un malus dégressif sur le prix si revendu vite (10 % par jour détenu jusqu'à 100 % à 10 jours) -> ajoutée à la roadmap #64 | grobarbrate, vachacz, #general | 2026-09-14 17:54-17:56 | complète (idée, non appliquée) |
| Effectif min 8 (03/09), débattu 5 vs 8 vs 10 vs génération automatique ; le dev garde 8 « et l'examinera comme indicateur de salaire : les salaires sont un peu hauts pour garder 14-15 joueurs » | vachacz, gulon84, svg07, lolek5232, #general | 2026-09-03 18:36, 09-05 12:50-13:25 | confirme (skill) |
| On ne peut pas annuler sa propre mise en vente ; un meilleur enchérisseur ne peut pas annuler, mais peut baisser son maximum | praedyn, cimi, grobarbrate, #general | 2026-09-03 14:51-14:53 | nouveau (règle d'usage, pas de confirmation du dev) |
| Les agents libres : à leur arrivée « bagarre » attendue ; le dev : ils sont entre cinq de départ et banc | rarz09, vachacz, #general | 2026-09-02 12:26-13:10 | confirme (skill : TSP 360-420) |
| Les mises en vente de la première semaine : des équipes jetables vendent tous leurs joueurs (reset) -> règle d'un minimum | gulon84, vachacz, #general | 2026-09-03 18:36-19:02 | confirme |
| Un joueur auto-généré pour compenser sous la limite (idée) rejetée : « trop compliqué techniquement » | vachacz, #general | 2026-09-05 13:25 | confirme |
| Transferts entre comptes de même IP (frères) : retrait du joueur, pas de ban | vachacz, rene779, #general | 2026-09-13 09:29-10:38 | confirme |
| Coût de l'attente : « 1 enchère max sur 3 joueurs bloquait le solde même après dépassement » (corrigé 26/07, voir bloc A) | | | confirme |

## B6 Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Après reset : solde de départ 600 000 pour tous (onboarding : 10 k de récompense réduite aux joueurs déjà en cours, 1 k par étape sinon) ; les trophées bêta restent, les récompenses sont remises à zéro | vachacz, #general | 2026-08-31 17:29, 2026-09-01 11:09 | complète (historique, déjà dépassé) |
| Estimations de joueurs : recette de ligue à domicile ~200 k ; amical ~18 k ; sponsor ~100 k/semaine ; 250 k de dépenses/semaine pour une équipe novice | vortexraijin, delinaaaaaaa, upkep123, #general | 2026-09-17 02:00-02:03 | avis (ordres de grandeur ; à comparer à nos `bv_finance_weekly`) |
| Coupe pilote : 100 000 par tour gagné (~5,5 amicaux), finale jusqu'à 1 M (avis d'un joueur) | rene779, #general | 2026-09-09 17:11, 2026-09-15 13:28 | avis (périmé pour la coupe nationale actuelle) |
| Personnel : kinés = réduisent le risque ; médecins : les « points de blessure » retirés par jour augmentent -> on peut embaucher après la blessure et la durée se recalcule (« tout le personnel marche comme ça ») ; psychologues, marketing ; le dev n'ajoute plus de personnel (reste les coachs, recalibrage de l'entraînement requis) | vachacz, grobarbrate, #general | 2026-08-28 17:57-18:04, 08-31 17:43-17:49 | complète (conséquence pratique : médecins rentables seulement à l'arrivée d'une blessure ; kinés avant) |
| Avis débutant : kinés et médecins selon qu'on joue 24 ou 36 min | vortexraijin, #general | 2026-09-17 02:25 | avis |
| Pas d'argent de promotion pour la L1 (reset) ; bonus de promotion 200 000 (manuel §9.1.4) : le dev à vérifier | aaaoooaaaa, vachacz, #general | 2026-09-01 10:05-11:11 | confirme (manuel) |
| Salaire : dérivé de la somme des compétences ; « un peu haut pour garder 14-15 joueurs » | vachacz, #general | 2026-08-13 15:38, 2026-09-05 13:25 | confirme |

## B7 Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Coupe pilote BV Cup du 04/09 : un match et on est éliminé, automatique et sans plafond pour la vraie coupe ; 5 jours ; la vraie coupe ensuite « 1-2 matchs par semaine » ; tactique à régler depuis Club ou Schedule > Cups | vachacz, #general | 2026-09-03 15:50, 09-04 16:01, 09-05 07:46-07:48, 09-09 15:48 | confirme (périmé) |
| 07 jours de matchs par semaine (3 ligue + coupe + amicaux) après le reset ; un match par jour de fin août (29/08) | svg07, rarz09, #general | 2026-08-29 12:53 | complète |
| Amical + ligue le même jour : décision indécise du dev, prérequis à tout changement de fatigue | vachacz, #general | 2026-09-15 15:46 | confirme |
| Le v3 en ligue : « après le tour 11 de S1 ou avant S2 » | praedyn (citation du dev), #general | 2026-09-09 20:12 | confirme (v4 depuis) |
| Heure d'affichage : heure locale ; coup d'envoi 21:00 | elemke., #general | 2026-09-07 13:12 | confirme |
| Promotion/relégation du reset : relégation exécutée normalement, bots remplacés dans l'ordre | praedyn, vachacz, #general | 2026-08-31 10:48, 11:54 | complète |
| 1 an de jeu = 56 jours | vachacz, #general | 2026-09-04 20:50 | confirme |

## B8 Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Rapport d'amicaux : le total des amicaux repart à zéro au reset (06/09) | grobarbrate, vachacz | 2026-09-06 16:25-16:30 | nouveau (bug mineur) |
| Un quatrième joueur manque dans l'affichage du cinq (4v5 visuel) : purement visuel, corrigé | marekb9231, txetx, vachacz | 2026-09-16 18:17-18:21 | confirme (« quatre joueurs dans le lineup », 16/09) |
| Depth chart impossible à remplir sur mobile (09/09) ; liste de transferts retour à la page 1 | hein.6, pijonghoo, blackdead6468 | 2026-09-10, 09-14 | complète |
| TS affiché faux pour les nouvelles équipes : TS de bots avant mise à jour quotidienne (00:00 heure EU) | rene779, vachacz | 2026-09-02 23:16, 09-03 05:27, 21:56 | complète (horaire du recalcul : 00:00 EU, « I guess ») |
| Un changement de tactique 14 min avant le match n'est pas pris ; presets et tactique directe sont séparés par match | vachacz, grobarbrate | 2026-09-12 19:33-19:49 | confirme (verrou 15 min) |
| Enchère : erreur à la mise ; Onboarding non validé automatiquement | inkamint | 2026-09-07 18:47-18:53 | complète |
| Résultat visible dans la notification pendant le live (corrigé 13/09) | vortexraijin, vachacz | 2026-09-12 18:31, 09-13 20:10 | confirme |

---
# BLOC C — lignes 1811-2140 (#general fin, #economy) et 2471-2797 (#academy), 2026-07-21 -> 2026-10-09

## C1 Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Cotes d'avant-match : calculées sur la force (HS/TS) + forme + fatigue, pas sur les tactiques réglées ; une équipe plus faible peut gagner avec une bonne tactique sauf écart énorme ; le dev rejoue 1 000 fois : les vraies cotes ne sont jamais aussi serrées | lordgohan_67459 (avis), vachacz, #general | 2026-09-25 23:58, 09-26 00:00-10:28 | confirme (cotes indicatives) |
| Avis : blessures aléatoires même en défense soft chez un 16 ans ; le dev : « le personnel déplace les chances, il ne supprime pas les blessures » | grobarbrate, vachacz, #general | 2026-09-26 18:18-18:30 | confirme |
| Matchs extrêmes observés (v3) : 51 fautes et 83 lancers francs ; 30 rebonds offensifs avec 100 tirs + 28 lancers | marekb9231, #general | 2026-10-05 21:47-21:49 | complète (avis : valeurs extrêmes ; liens dans le texte) |
| Fin de match : une équipe menée de 1 à 13 s de la fin ne tente pas le tir gagnant et ne fait pas faute -> « problème connu, corrigé en v3 en amical, en ligue après le tour 11 » | usylum, vachacz, #general | 2026-09-28 11:50, 14:19 | confirme (fautes tactiques en fin de match, v3) |
| Libellé du jeu-par-jeu : une contre-passe ressort avec la mauvaise balle (« label issue ») | marekb9231, vachacz, #general | 2026-09-21 19:18-20:42 | complète (affichage, pas moteur) |
| Instructions de prolongation affichées dans la colonne des quarts-temps et gênantes (« O ressemble à Q ») -> colonne vide ajoutée | gulon84, vachacz, #general | 2026-09-28 08:45-11:06 | complète (UI) |
| 220 cm au poste PG qui marque 30 points : jugé « déséquilibre » par un joueur | grobarbrate, #academy | 2026-08-04 20:13 | avis (v2 d'août) |

## C2 Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Postes : « les positions n'ont pas d'importance, ce sont les compétences et le physique » | lordgohan_67459, #general | 2026-09-21 18:50 | confirme (avis conforme au dev) |
| Marché par âge : aucun 20-21 ans vendu (graine de départ : les adultes ont tous des âges proches « pour l'équité ») ; groupes dominants 24-25 et 27-28 ans, plus les 16-17 ans de l'académie | elemke., marekb9231, vachacz, #general | 2026-10-05 21:49-21:56 | nouveau (offre de 20-21 ans quasi nulle ; à vérifier sur `gold.bv_market_*`) |
| Croissance en taille : jusqu'à ~+4 cm par an (max ~+20 cm), possible +1 cm seulement | grillanza_60069, grobarbrate, #academy / #general | 2026-09-04 16:16, 09-25 07:38 | avis (manuel dit jusqu'à 4 cm/an ; minimum non confirmé) |
| Expérience : un junior qui ne joue pas n'en gagne pas ; pas de match interne payant (idée de gulon84) | gulon84, doman, lordgohan_67459, #academy | 2026-08-23 05:47, 08-24 16:14 | avis |
| Salaire : « plus haut = meilleur joueur » (avis) pour juger un joueur non issu de l'académie sans potentiel | vortexraijin, #general | 2026-10-07 15:07 | avis |
| Popularité : 11 matchs à domicile x +2 = 92 % max en fin de saison puis retour à 70 % ; le dev reconnaît ; remise à 70 plutôt « si en dessous de 70 » ; idée : victoire à l'extérieur plus précieuse | grillanza_60069, vachacz, aeolian06, marekb9231, #general | 2026-10-07 19:17-20:45 | complète (V-20261030-7) |

## C3 Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Multiplicateur d'entraînement : pot 10 = 2,25 (04/08, lolek5232) contre pot 7 = 1,4 ; (16/08 : 2,20 dans connaissance) | lolek5232, vachacz (silencieux), #academy | 2026-08-04 16:52 | complète (pot 7 = 1,4 : nouveau ; valeurs d'avant la réforme du 10/08, à vérifier dans le skill entraînement) |
| Un pot 10 de 16 ans : +18 compétences/saison en pré-réforme (lecture manuel/dev), donc 90 en 5 saisons ; exemple : junior à 333 de total à 16 ans -> ~423 ; un joueur auto-généré de 19-21 ans a déjà 434 | grobarbrate, #academy | 2026-07-21 20:25 | historique (pré-reset) |
| Dev : pour le futur, TSP maxi à 31 ans ; entraînement plus lent avec l'âge | vachacz, #academy | 2026-08-03 17:18 | confirme (skill) |
| Dev : une « compétence aléatoire dans la fourchette » pour les juniors (ex. rebond fort chez un petit) ; calibrage ultérieur avec l'entraînement | vachacz, #academy | 2026-07-30 17:03 | complète (génération non corrélée au poste) |

## C4 Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Table d'été (21/07) : 4 % de pot 1 à académie 0 % et 4 % de pot 10 à 100 % (25 % pour pot 5-6) ; le dev (21/07 19:48) : le niveau agrandit aussi les fourchettes de compétences, « peut-être plus important » ; remplacée le 27/07 par la table croissante + bonus à 100 % | grobarbrate, vachacz, #academy | 2026-07-21 19:44-21:02, 07-27 17:38 | confirme (déjà noté) |
| Courbe du 23/07 mesurée par lolek5232 : après un tirage à 100 %, revenir à 100 % demandait 5 semaines et 1 M ; avec la nouvelle courbe, de 50 % à 100 % : 8 semaines et 1,6 M ; tirage à 80 % -> 40 % puis remonte vite | lolek5232, vachacz, #academy | 2026-07-23 16:01-16:10 | nouveau (chiffre de coût à comparer à `basketvibe-academie`) |
| Dev : différence 90 % -> 100 % « très petite » en dehors du bonus ; indicateurs +1/+2/+3 affichés pour l'avancement | vachacz, #academy | 2026-07-23 16:12, 21:19 | confirme (skill) |
| Concept du 27/07 : P9/P10 démarrent vers 50 % mais très rares ; bonus de P8/P9/P10 à exactement 100 % (avis de tolgt3387 : « 10,7 % de bonus, trop ») ; tests = Low 1-3 / Decent 4-7 / High 8-10 ; 99 % puis 100 % garanti | vachacz, tolgt3387, #academy | 2026-07-27 17:38-17:44 | confirme (skill) ; le « 10,7 % » est un avis chiffré non vérifié |
| Les « profils » d'académie (Slasher, All-rounder) supprimés, remplacés par plus de rebonds chez les grands, plus de passes aux guards | vachacz, airgk32, #academy | 2026-07-22 10:45-11:46 | nouveau (historique) |
| Rapports : trois postes différents, répartition NBA (C 17 %, SG 23 %) ; refus de choisir le poste | vachacz, #academy | 2026-07-22 18:26-18:43 | confirme (déjà noté ; contredit par nos données du 15/10) |
| Étoiles du test : 3 étoiles = 8-10 ; « 2 étoiles peut valoir 4 » ; « 3 étoiles = probablement 8 » ; refus de passer à 5 étoiles | vachacz, tolgt3387, lordgohan_67459, #academy | 2026-08-05, 2026-09-06 10:35 | confirme (skill) ; « probablement 8 » est un avis |
| PS de sortie d'académie observés : 41, 48, 52 (16 ans, académie 92 %), 54 (17 ans) ; 47-50 de TS pour un C de presque 18 ans à 85 % | esmosinag, hamsterj1312, ale92c, ori1919, montabelas, #academy | 2026-09-13 12:51-14:24, 10-08 18:16 | nouveau (ordre de grandeur ; à comparer à `silver.bv_academy_candidates`) |
| Avis : un tirage ordinaire au milieu de saison à 85-100 % est mal valorisé ; attendre un tirage à ~100 % en début de saison ; « les prix des jeunes monteront avec plus de cash » | giovannidziadzia, doman, #academy | 2026-10-08 18:14-18:26 | avis |
| Avis : investir au max est supportable (« trois fois ça en un match à domicile ») | elemke., #academy | 2026-09-24 13:13 | avis (cohérent : 250-300 k pour un match à domicile) |
| Rapport hebdomadaire chaque jeudi (confirmé par les joueurs en septembre) ; PG/SG rares : les 3 candidats finissent souvent C/PF | grobarbrate, doman, #academy | 2026-09-25, 10-07 09:16 | complète (avis : surtout des grands ; nos données 22/10 et 29/10 : PF/SF/C et PG/C/SG) |
| Tests de 25 k : « rien aux premiers essais (75 k), haut potentiel au suivant » (aléatoire) | grobarbrate, doman, #academy | 2026-09-10 11:30, 11:47 | avis |
| Marché des 16-17 ans : « personne ne veut vendre » (10/09-09/10) ; un 3 étoiles à 2 M (avis) | dcarra., elemke., #academy | 2026-09-24 10:06, 10-09 12:14 | avis |

## C5 Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Prix d'un 19 ans de 208 cm / 116 kg PS 43, fort potentiel de progression : 200 k (acheté par elemke.) ; marekb9231 : « une affaire » | elemke., marekb9231, #general | 2026-09-21 15:12-15:17 | nouveau (une observation) |
| Avis d'inflation : 2 M achetaient 3-4 joueurs avant le reset, un seul bon joueur après ; d'autres répondent « j'ai acheté 3 très bons joueurs pour 2 M » ; revenus annuels ~2 M | grobarbrate, marekb9231, grillanza_60069, elemke., #general | 2026-09-22 12:14-13:28 | avis contradictoire |
| Enchère à l'aveugle vue en vrai pour la première fois : « équitable, termine une guerre d'enchères » | grobarbrate, vachacz, #general | 2026-10-05 10:33-10:46 | confirme (phase finale à l'aveugle ; but du dev : éviter les enchères sans fin) |
| Libération d'un joueur : aucune conséquence | vachacz, #general | 2026-09-23 05:10 | confirme |
| Prix économique d'été : meilleurs joueurs 2,5 M (avant reset) ; avis : le prix suit surtout l'offre de bons joueurs | vachacz, grobarbrate, #economy | 2026-08-21 07:31-07:59 | complète (historique) |

## C6 Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Économie du dev (19/08) : 7 amicaux/sem. sans académie = ~5 M/saison d'épargne ; avec 200 k d'académie + 2 tests médicaux en moyenne = 2,8 M ; amicaux seuls = 1,8 M ; après modifications (amicaux -30 %, académie max 100 k, salaires doublés de 120 k à 240 k après reset) : 3,1 M sans académie, 2 M avec 100 k d'académie et tests, 1 M sans amicaux ; « les amicaux restent financièrement importants » (21/08) | vachacz, #economy | 2026-08-19 16:27, 2026-08-21 06:58 | nouveau (chiffres annuels du dev ; à rapprocher de nos données financières hebdomadaires) |
| Sponsors : réflexion sur 3 types (performance / équilibré / sûr) puis plan : montant fixe, prime par victoire, prime de réussite top 8, top 3 ; brouillon du 02/10 avec montants très écartés (« champion 2 M versé en fin de saison, top 6 jusqu'à 1,1 M, moitié haute 25 k/sem. » selon chanceler) ; le dev retire le tout-ou-rien, refuse de changer en cours de saison (« le contrat signé reste signé ») ; aucune conséquence autre que financière | vachacz, chanceler, saivet_71082, ale92c, #economy / #general | 2026-08-19 18:12, 2026-10-02 15:55-18:45 | complète (version finale = 6 types dont « Stability » ; brouillon périmé) |
| Personnel prévu : psychologues 2 x 10 k (risque de forme), marketing 2 x 10 k (réduisent l'impact des défaites sur popularité et billetterie) ; non-linéarité des salaires à venir (non calculable sans données) ; sponsor lié à la dureté de la division à venir | vachacz, #economy | 2026-08-19 18:19, 2026-08-27 17:50 | complète (effet marketing : « impact des défaites » ; nouveau) |
| Bonus « homegrown » : proposition initiale « jusqu'à 500 k » remplacée par 200 par minute avec plafond 40 000/semaine ; idée de prime par renommée (MVP match 0,25, journée 0,5), débat contre | vachacz, praedyn, #economy | 2026-08-19 18:38-18:45, 2026-09-10 16:49-20:42 | confirme (skill) ; fame en doute (déjà noté) |
| Aucune extension de stade possible | vachacz, #general | 2026-09-29 11:45 | confirme |
| Taxe de revente ; idée 5 % du prix de départ puis 5 % du final | doman, #economy | 2026-08-22 10:13 | avis |
| Début de saison : 600 k de départ, 200 k de salaires/semaine, premier match à domicile 250-300 k ; 1 ou 2 matchs à domicile par semaine | jorgeac25, vachacz, #academy | 2026-09-05 14:49-14:55 | confirme (skill) |

## C7 Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Après saison : coupes nationales un match par jour, ensuite coupe complète ou système suisse ; saison de 9 semaines ? (première semaine vide) | vachacz, grillanza_60069, #general | 2026-10-04 12:53, 10-05 05:54 | confirme (déjà noté) |
| Live des amicaux : fonctionne en Europe ; bloqué sur « tactiques verrouillées » pour l'Asie jusqu'au 29/09 | vortexraijin, vachacz, #general | 2026-09-28 23:02, 09-29 12:21 | complète (bug fuseau) |
| Coupe pilote : on ne peut pas regarder le match si éliminé -> à corriger ; notifications de coupe affichées comme amicaux | vortexraijin, vachacz, #general / #academy | 2026-09-27 20:30, 09-04 16:22 | confirme (déjà noté) |
| Réunions : ~350 joueurs actifs par semaine (200 un mois plus tôt) ; 518 managers inscrits | vachacz, jagmn, #general | 2026-09-23 09:39, 17:55 | complète |

## C8 Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Joueurs d'académie : visages différents selon le navigateur (Chrome/Edge) ; chargement mobile bloqué (« Loading »), 5-10 s de coupure à chaque déploiement | gulon84, vachacz, rene779, #academy / #general | 2026-09-25, 09-27 | complète (sans effet décision) |
| Joueur non autorisé à jouer la prolongation avec les meilleurs (voir B1) | jagmn | 2026-09-17 | complète |

---
# BLOC D — lignes 2141-2470 (#economy fin, #engine, #academy début) et 2798-3097 (#help début), 2026-06-30 -> 2026-10-04

## D1 Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Remplacement d'un joueur blessé ou expulsé : le moteur le remplace par le suivant du depth chart ; si le suivant est déjà programmé (ex. C1 programmé 30 min, C2 blessé), C1 joue 40 min : pas de logique supplémentaire | vachacz, #engine | 2026-06-30 20:56 | complète (règle de secours ; détail minutes cumulées) |
| v2 (texte officiel) : défense agressive = « quelques points de moins pour l'adversaire à niveau égal, au prix de plus de fautes, plus de lancers francs adverses et plus de fatigue après le match » ; défense soft = l'adversaire tire plus facilement ; passe : bonus de tir pour le joueur assisté, assist crédité si le tir rentre ; maniement : moins de pertes de balle, plus de tirs dans la raquette ; athlétisme : pertes, rebonds, contres, interceptions, raquette | vachacz, #engine | 2026-07-09 21:47 | confirme (skill tactique) ; « quelques points par match » = chiffre qualitatif nouveau |
| Rebonds : le poste occupé sur le terrain (PG loin du cercle) et la taille se cumulent ; un petit au poste C ne prend pas de rebonds comme un vrai grand | vachacz, #engine | 2026-07-09 21:47 | confirme |
| Mesure du dev sur un 222 cm placé PG (v2, 21 pts, 0 perte) : 1 000 simulations -> 1,7 perte de balle de moyenne, jugé trop bas pour cette taille, à corriger ; autre test : un 188 cm au poste SF a presque fait un triple-double (10 rebonds) mais ses adversaires directs ont marqué plus de 40 en 4 quarts : « la taille pèse plus que la défense » (avis) | vachacz, lolek5232, svarog_, #engine | 2026-07-23 11:47, 07-24 08:22, 14:25 | confirme (taille > poste) ; mesure 1,7 TOV nouvelle |
| Fatigue / défense : un joueur peut avoir peu de fatigue pour beaucoup de minutes si la défense est « low focus » ; le manuel a une section « où la barre se stabilise » ; défense agressive = arme à double tranchant, alterner avec soft | montabelas, vachacz, #engine | 2026-09-19 16:45-17:04 | confirme |
| Fin de quart : l'équipe ne tire pas dans les ~13-29 dernières secondes (aucune action) ; fautes tactiques absentes ; rebonds concentrés sur 2-3 joueurs (80-90 %) ; And1 absents ; lancers manqués sans rebond -> tous listés pour v3 | grobarbrate, rushrat, rene779, glorious_monkey, vachacz, #engine | 2026-09-05 09:06, 09-07 14:39 | confirme (v3 les corrige : 08-09/09) |
| Pénalité >36 min : 12,5 % le 12/09 matin ; presque doublée le soir ; v2 gelé, changements seulement en v3 | vachacz, #engine | 2026-09-11 15:47, 09-12 08:36-08:38 | complète (date précise : 12/09 soir) |
| Défense : proposition « Defense area » (n'ajoute pas de défenses 3-2/2-3) ; avis : les zones devraient réduire le NOMBRE de tirs plutôt que le %, 3-2 +10 % défense PG/SG/SF, 2-3 +15 % défense PF/C | vachacz, grobarbrate, #engine | 2026-09-10 22:19-23:32 | confirme (déjà noté) |
| Dans les matchs de coupe, le préréglage d'amical est pris par défaut (bug avoué : « je ne l'ai pas corrigé ») -> le joueur ne s'en rend pas compte | svarog_, vachacz, #engine | 2026-09-18 20:08-20:16 | nouveau (à vérifier sur notre coupe quotidienne : lire la tactique enregistrée de la coupe, pas celle d'amical) |
| v3 live pour la prochaine ligue et coupe le 02/10 ; v4 = v3 le 04/10, v3 gelé, changements en v4 d'abord en amical | vachacz, pijonghoo, marekb9231, #engine | 2026-10-02 02:30-05:13, 10-04 11:44-11:48 | confirme (« v4 = v3 au 04/10 ») |

## D2 Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Fatigue : endurance « verte » a peu d'impact ; fatigue 5-10 presque sans effet ; plus l'endurance est basse, plus la fatigue tombe lentement ; un joueur à 20 de fatigue et 68 d'endurance a perdu 2/jour ; le dev suppose « 68 d'endurance = ~30 minutes » (« je ne me souviens pas exactement ») | vachacz, grobarbrate, #help | 2026-08-07 08:38-08:59 | confirme (v3) ; « 68 -> 30 min » en doute |
| Forme : +/-1 aléatoire par semaine, psychologues décalent légèrement vers la hausse ; s'applique à tous les matchs (ligue, coupe, amical) | vachacz, #help | 2026-09-11 05:26 | confirme (skill) |
| Hauteur par poste : PG pleine valeur de 180 à 200 cm, 95 % à 205 cm ; « entre 200 et 205 la baisse est linéaire » ; la position nominale ne change jamais (même si le joueur grandit) | vachacz, pijonghoo, #help | 2026-09-10 13:35-15:40, 2026-07-19 18:31 | complète (barème de taille par poste : valeurs du manuel, confirmé par le dev) |
| Les joueurs de moins de 21 ans grandissent (le manuel disait l'inverse : à corriger) ; les juniors d'académie et les effectifs de départ n'ont pas de décimales (défaut à corriger) | vachacz, elemke., #help | 2026-09-13 07:57 | confirme (skill) |
| Blessure : « très improbable avec 9 de fatigue et 4 minutes mais possible » ; âge pas un facteur (envisagé) ; refonte des blessures prévue avec le personnel médical | vachacz, #help | 2026-08-10 18:13-18:22 | confirme |
| Un joueur s'entraîne une fois par semaine quelles que soient ses minutes | vachacz, #help | 2026-09-21 17:19 | confirme |
| Pas de pénalité de poste (v2) ; changer le poste d'un joueur impossible | vachacz, #help | 2026-07-19 18:31, 2026-09-09 17:52 | confirme |

## D3 Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un 3 étoiles de 16 ans (pot 8-10) gagne « 18 à 24 compétences par saison selon le potentiel » | vachacz, #help | 2026-09-24 21:33 | confirme (skill : pot 10 = +26 à 16 ans) ; fourchette 18-24 pour 8-10 |
| Aucun plafond autre que 99 ; l'entraînement coûte plus cher plus haut ; potentiel des juniors égal pour tous les pays | vachacz, #help | 2026-09-08 05:26, 11:05 | confirme |
| Idée d'entraînement multi-compétences (1 -> tout, 2 -> moitié, 3 -> tiers) | vachacz, lucadrago5, #help | 2026-07-26 08:48-15:17 | confirme (déjà noté en doute, jamais livré) |
| Pot 10 = +2 par semaine en principale (avis) ; +2 principale et +1 secondaire dès le 1er entraînement d'un junior tiré ce jeudi = signal pot 10 (avis, une observation) | pijonghoo, nathanr_32176, #help | 2026-09-13 12:19-12:28 | avis |

## D4 Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Rapport de départ : gamme de 25 points (barres) ; le dev envisage des gammes de 10 ; on voit les compétences exactes à la signature | vachacz, wintersb_, #help | 2026-07-06 13:54-14:00 | confirme (historique) |
| Dev, 21/07 : « les malins tireront à 70 % (le recul est moindre) et auront 2 juniors corrects, pendant que ceux qui visent 100 % attendent sans junior » ; 100 % doit être « très cher », 75 % abordable | vachacz, #academy | 2026-07-21 19:25-19:28 | complète (conseil stratégique du dev avant la table du 27/07 ; à mettre en balance avec le bonus à 100 %) |
| Avis : le recul de 50 % à chaque tirage pousse à garder les prises pour un « parfait » et vide le marché de juniors | dcarra., #academy | 2026-07-21 17:00 | avis |
| Tests : « Send for tests » 25 k, fourchette réduite de 20 à 10 ; potentiel en 3 niveaux (1-3, 4-7, 8-10 après essais 1-4 / 5-6 / 7-10) | vachacz, #academy | 2026-07-14 18:42, 07-21 16:24 | confirme (skill) |
| Rapport hebdomadaire (14/07 : toutes les 2 semaines) ; âge 16-18 proposé par cimi ; la baisse de 50 % maintenue | vachacz, cimi, #academy | 2026-07-14 18:57, 07-15 22:25 | confirme |
| Potentiel des agents libres : aléatoire entre 3 et 9 | vachacz, random_player_123., #help | 2026-09-07 18:40-18:44 | nouveau (potentiel d'un agent libre : 3-9, jamais 1-2 ni 10) |
| Chronologie : rapport "mercredi" (grillanza_60069) puis jeudi corrigé ; page « prochain rapport » | grillanza_60069, #help | 2026-09-08 05:07-07:27 | confirme (jeudi) |

## D5 Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Enchères type eBay : prix visible = dernier maximum perdant + incrément ; prix final = dernière plus haute enchère ; +3 min sous la minute (« I guess »), 15 min au plus, puis phase à l'aveugle | vachacz, #help | 2026-07-21 15:59, 09-03 21:27 | confirme (skill) |
| Prix de juillet (pré-reset) : meilleur joueur 1,5-2 M, bon joueur de rotation 500 k-1 M | dcarra., #help | 2026-07-23 08:45 | complète (historique) |
| Personnel : on paie la somme maximale de salaires du personnel présente sur la semaine (embaucher puis licencier ne coûte pas deux fois) | vachacz, arodrigues84, #help | 2026-09-03 16:44 | nouveau (règle de facturation ; à vérifier dans `basketvibe-economie`) |
| Médecins : embauchables après la blessure, l'effet s'applique aux jours restants ; « embauche les médecins après la blessure » | lordgohan_67459, vachacz, pijonghoo, #help | 2026-09-14 03:34-05:20 | confirme (B6) |
| Aucune limite d'effectif ; solde négatif = interdit de marché, éventuellement restriction du personnel et de l'académie ; effectif minimum 8 | vachacz, vortexraijin, #help | 2026-09-12 16:56-17:03 | confirme |
| Pas de restriction de pays ; bonus homegrown max 40 k pour ~60 min par match avec des joueurs de l'académie (icône maison) | vachacz, #help | 2026-09-10 15:25-15:27 | confirme |

## D6 Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Début de saison 2 : sponsor fixe 100 k/semaine ; salaires 240-250 k/semaine (club neuf : coûts fixes -296 382/semaine) ; match de ligue à domicile 250 k jusqu'à 400 k selon la popularité ; amical ~17 k (7/semaine = 119 k) | vachacz, aaaoooaaaa, lolek5232, random_player_123., spapjh, #help | 2026-09-05 07:43-11:35, 09-08 15:24 | confirme (skill économie) |
| Avis chiffré : en incluant 120 k d'amicaux, 100 k de sponsor, 100 k d'académie et 250 k de salaires, il faudrait 95 k par match à domicile pour être à l'équilibre ; +1,5 M d'épargne par saison (avis) | random_player_123., #help | 2026-09-05 11:33-11:43 | avis (périmé : domicile 250-400 k) |
| Amicaux : ils rapportent ~44 k net par semaine avec 5 joueurs de 15 k ; 40 k de homegrown à 200 min en ligue ; l'avis de lolek5232 demande 30-40 % d'expérience en amical | lolek5232, #help | 2026-09-05 10:19 | avis |
| Prime de fin de saison selon le classement : « il y avait un petit montant, je vérifierai » | vachacz, #help | 2026-09-21 15:39 | en doute (non confirmé) |
| Facturation hebdo du personnel : max des salaires de la semaine | vachacz | 2026-09-03 | voir D5 |

## D7 Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Entraînement : dimanche (2/09, grobarbrate) puis samedi ; entraînement samedi 09:00 CET avant la réforme | grobarbrate, #help | 2026-09-02 19:51 | avis (non confirmé par le dev) |
| Le tactique de coupe se règle depuis Club ou la notification | vachacz, esmosinag, #help | 2026-09-03 16:44-17:04 | confirme |
| Amicaux : 1/10 de la fatigue et de l'expérience de ligue, pas de blessure (vérifié juillet, mais v4 met fin à « sans blessure ») | grobarbrate, #help | 2026-07-14 17:22, 09-02 03:15 | confirme (v4 contredit « pas de blessure ») |
| Tactique de match : changer un préréglage ne met pas à jour les matchs déjà programmés avec ce préréglage ; refaire le choix pour chaque match | vortexraijin, grobarbrate, #help | 2026-09-05 00:28-00:49 | nouveau (piège d'usage : après toute modification du préréglage, ré-appliquer à chaque match programmé) |

## D8 Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Impossible d'enregistrer une tactique après la vente d'un joueur du préréglage (cinq incomplet) : corrigé le 19/09 | tankre1792, heldermoreno, vachacz, #help | 2026-09-18 10:48, 09-19 15:57-16:26 | confirme (déjà noté) ; cause précisée (un joueur vendu reste dans le préréglage) |
| Tactique affichée non conforme dans un match (aucun des cinq prévus) ; bug créé | szulim90, vachacz, #help | 2026-08-29 18:18-18:27 | complète (anomalie isolée) |
| Rapport d'académie du 22/07 manquant (dates cassées après passage à 1 semaine) | rarz09, vachacz, #help | 2026-07-22 21:21-21:34 | confirme (déjà noté) |

---
# BLOC E — lignes 3098-3997 (#help fin, #ex-yugo : chat en serbo-croate, essentiellement d'avant le reset), 2026-07-17 -> 2026-10-04

## E1 Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un joueur réglé sur « passe » tire quand même : Filipović en passe a pris 17 tirs (le plus du match) ; Lazarević en passe 6 ; « les joueurs cherchent les trous et marquent même en passe » (1 match d'amical, v1) | grobarbrate, #ex-yugo | 2026-07-22 09:55-09:57 | nouveau (avis chiffré, v1 ; le focus offensif v3 corrige en partie) |
| Focus défensif : « inutile si le défenseur a 20 en défense » ; avec un seul attaquant principal par quart, un adversaire qui met le focus dessus le neutralise ; focus plus efficace que sur MBT | lolek5232, grobarbrate, #ex-yugo | 2026-07-21 17:13-17:14, 07-20 17:19 | avis |
| Mesure d'un joueur sur ses 10 derniers amicaux : points encaissés/inscrits par joueur ; Gajic (déf. 45) encaisse 12,1 et inscrit 25,2 (le meilleur bilan), Knezevic (déf. 72) encaisse 18,8 pour 11,4 ; Todorovic -4,5 ; lecture : la compétence de défense ne prédit pas seule le solde, le focus adverse pèse | grobarbrate, #ex-yugo | 2026-07-25 12:30-12:41 | nouveau (v1, avis ; ne pas utiliser comme règle) |
| Deux joueurs de bonne passe : « une bonne passe se sent en attaque » ; rebond de tout joueur aide l'équipe même sans prendre le rebond (Filipović, pire rebondeur de l'équipe, a eu 10 rebonds) ; 196 cm à 58 en rebond = 4 rebonds ; 180 cm à 70 en rebond au poste C = 8,5 rebonds | grobarbrate, lolek5232, svarog_, #ex-yugo | 2026-07-21 17:51-17:53, 07-22 09:53-09:54 | avis (v1) |
| 217 cm avec 35 en rebond « inutile » ; un 222 cm au poste PG fait 0 perte (voir D1) ; un 188 cm au poste SF presque triple-double | lolek5232, joomi1, svarog_, #ex-yugo | 2026-07-21 17:52, 07-23 07:31, 07-24 06:18 | avis (confirme « taille > poste ») |
| Rebond d'un meneur de 180+ avec 70 en rebond placé C par défaut : 8,5/match | svarog_, #ex-yugo | 2026-07-21 17:47 | avis (v1) |

## E2 Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Fatigue : aucune pénalité jusqu'à ~20, la barre passe au jaune ensuite avec une pénalité ; plus l'endurance est basse, plus on s'use | grobarbrate, #ex-yugo | 2026-07-21 12:36 | confirme (v3 : -4 % à 20, voir connaissance) |
| Blessés / retour : un joueur de retour de blessure le jour d'un match de coupe n'a pas joué (équipe d'Australie, fuseau soupçonné) ; réponse : « signale-le » | b.tothe.r, vachacz, #help | 2026-10-04 20:50-20:52 | nouveau (en doute : lien fuseau/coupe non confirmé) |
| Poids : aucun contrôle du poids pour l'instant | vachacz, #help | 2026-09-27 10:25 | confirme |
| Les défaites en amical n'affectent pas la popularité | grobarbrate, #help | 2026-10-03 07:26 | avis |

## E3 Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Lecture d'un joueur du gain par entraînement (v1) : compétence principale = 1 x potentiel (pot 5 -> +1, pot 10 -> +2, pot 1 -> +0,5), secondaire = moitié ; plafond de compétence d'un junior lié au niveau de l'académie (26 % -> 41 max, 55 % -> 47 max, 100 % -> 60 max) | lolek5232, #ex-yugo | 2026-07-18 15:37, 07-19 16:30, 07-22 10:07 | avis (v1, plafonds 2026-07 remplacés par la réforme du 10/08 ; pot 10 = 2x cohérent avec 2,20-2,25) |
| Un joueur avec « 5 compétences gagnées en 3 entraînements » = bon potentiel | lolek5232, #ex-yugo | 2026-07-26 16:29 | avis |
| Dev (pré-reset) : « le niveau d'académie limite le haut des fourchettes ; 60 est le maximum à 100 % » (confirmé par les joueurs) | lolek5232, svarog_, #ex-yugo | 2026-07-21 16:00 | avis (v1) |

## E4 Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Avis : à 82 % on peut déjà tirer un excellent junior toutes les 3 semaines ; l'écart 82 % -> 100 % est « négligeable pour 5 semaines d'investissement » | lolek5232, grobarbrate, #ex-yugo | 2026-07-23 16:19-16:21 | avis (pré-table du 27/07 ; concordant avec le dev 21/07 : viser ~70-80 %) |
| Tirage à 49 % : trois centres de 16 ans, compétences clés > 40 ; compétence de rebond tirée à 41 « par hasard » ; revente du junior à 1 M (marché) : un tirage pour revendre coûte ~3 semaines de remontée | lolek5232, grobarbrate, #ex-yugo | 2026-07-29 17:06-17:23 | avis (pré-reset) |
| Prix de revente de juniors tirés à ~50 % : 1 M (lolek5232), « au moins 1,5 M » (grobarbrate) | lolek5232, grobarbrate, #ex-yugo | 2026-07-29 17:08-17:24 | avis (pré-reset ; le 29/10 un 3 étoiles se vend 3,5-4 M selon connaissance) |

## E5 Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Records de prix (pré-reset) : PG hollandais 1,7-1,75 M (20/07) ; Espagnol 2,25 M (28/07), « record » ; Italien 1,5 M (24/07) ; centre de 23 ans autour de 1 M ; 27 ans à 700 k | grobarbrate, svarog_, lolek5232, #ex-yugo | 2026-07-20 16:22, 07-24 17:07-17:12, 07-28 12:14 | complète (historique pré-reset ; économie remise à zéro) |
| Achat-revente observé en juillet : joueur de 31 ans acheté 50 k revendu 200 k ; PG acheté 800 k revendu 1,75 M ; « la valeur est dans les joueurs, pas dans l'argent » (inflation) | grobarbrate, svarog_, #ex-yugo | 2026-07-18 13:36, 07-20 16:46, 07-28 15:02 | complète (historique : revente profitable en économie ouverte ; non transposable post-reset) |
| Prix d'un joueur 16-17 ans à plus de 500-600 k pour des profils moyens ; « on ne peut plus acheter un 16 ans sous 1 M » | lolek5232, grobarbrate, #ex-yugo | 2026-07-22 08:11, 07-25 10:29 | avis (pré-reset) |
| Les bots de haut niveau sont ~50 promus ; nouveaux joueurs placés dans les ligues basses | lolek5232, pjotorus, #ex-yugo | 2026-07-21 07:58-09:59 | complète (historique) |

## E6 Finances / sponsor
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Récompense de fin de saison : 200 k pour la victoire en ligue, « encore de la période d'avant le reset, je la revisiterai en fin de saison 1 » ; avis : les récompenses devraient dépendre de la division et du rang ; ajouter quelque chose pour la moitié haute | rems3132, vachacz, grillanza_60069, #help | 2026-09-27 10:48-10:53, 09-28 11:42-14:22 | confirme (connaissance : en doute) |
| Sponsor : types prévus pour S2 (mensuel, réussite saison versée en fin de saison, victoire) ; pas de changement en cours de saison | vachacz, kotryk, #help | 2026-09-27 10:56 | confirme |
| Aucune extension de stade possible ; logo dans Club > profil | vachacz, #help | 2026-09-29 05:31, 10-01 22:27 | confirme |
| Onboarding : peut être relancé par le dev avec 100 à 1 000 de récompense | vachacz, #help | 2026-10-03 15:51 | complète |

## E7 Calendrier / coupes
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Départage « h2h » (modifié récemment) | vachacz, #help | 2026-10-03 18:59 | confirme (connaissance) |
| Friendly finder dans le menu Schedule | vachacz, #help | 2026-10-04 12:53 | confirme |

## E8 Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Chrome ne charge pas le site pour un joueur (Edge OK) ; l'animation « tremble » | wintersb_, vachacz, #help | 2026-09-26 | complète (sans effet décision) |
| Même bug d'enchère maximale du 26/07 décrit en serbe (510 k comptés comme dépensés après dépassement) | grobarbrate, #ex-yugo | 2026-07-26 10:54-10:56 | confirme |
| Un faute d'un joueur qui n'est pas le défenseur direct (soupçon) | svarog_, #ex-yugo | 2026-07-26 08:52 | en doute (non vérifié, v2) |

---
# BLOC F — lignes 3998-5000 (#ex-yugo, chat en serbo-croate, 2026-07-29 -> 2026-08-22, tout pré-reset : moteur v2 d'août)

## F1 Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Le curseur 2P/3P est suivi : tout le monde en « tir à 3 » = 82 tirs à 3 (40 %) pour 6 tirs à 2 ; tout le monde en « tir à 2 » = 7 tirs à 3 ; mais un centre à 72 en 2P / 75 en 3P prend ~6 trois-points à chaque match quel que soit son réglage (1 observation) et un joueur à 20-40 en 3P réglé « 3 » marque 44-46 % (déséquilibre du 3P en v2) | grobarbrate, lolek5232, #ex-yugo | 2026-08-08 06:59-07:05, 08-09 09:56-10:17, 08-10 22:58 | complète (v2 d'août ; plafond 3P 70 -> 50 % des tirs le 24/08 corrigé ensuite) |
| Focus défensif : sur 5 joueurs réglés 1-5 (zone intérieure), les joueurs en focus 5 n'ont pris que 8 et 11 tirs en 48 min, mais ont gardé 8/11 et 6/8 -> le focus réduit le nombre de tirs de la cible, pas son efficacité (n = 2 joueurs, amical, v2) | grobarbrate, #ex-yugo | 2026-08-04 09:20-09:26 | avis (une observation) |
| Défense individuelle (v2 août) : « une équipe à 76-74-76-80-77 de défense par quart a encaissé 70 points en 2 quarts » ; « seul compte d'avoir plus d'attaque et de défense que l'adversaire » ; focus renforcé le 10/08 (« la défense seule ne protège pas, le focus aide ») | grobarbrate, #ex-yugo | 2026-08-09 10:28-10:30, 08-10 22:33-22:36 | avis (cohérent : release-notes 08-08/09 « tactique/focus défensif relevés ») |
| Focus adverse : une équipe inactive avec focus fort a fait passer un adversaire de 130 points/match à moins de 90 en 2 matchs (« du jour au lendemain ») | svarog_, #ex-yugo | 2026-08-22 11:04, 18:46 | nouveau (avis chiffré ; confirme que la tactique adverse compte) |
| Conseil de joueur : contre un bot ou une équipe inactive, ne pas toucher au focus défensif (l'attaque adverse se déplace vers le trou) ; régler 1 contre 1 et ne rien changer | svarog_, #ex-yugo | 2026-08-03 18:54-18:56 | avis (contradictoire avec : « inactif = même cinq, on peut préparer ») |
| Avantage du terrain évalué à ~10 % (avis) ; athlétisme important en défense (avis : 67 en tir / 40 en athlétisme n'a pas pu marquer contre 60-80 d'athlétisme) | lolek5232, #ex-yugo | 2026-08-01 18:45, 19:13 | avis |
| Bots / équipes à 5 x 48 min : le Q4 reste gagné par le bot (36-21, 46-30) en v2 d'août ; le dev baisse les bots de 10 | grobarbrate, lolek5232, #ex-yugo | 2026-08-03 18:03-18:12 | confirme (cause du nerf des 48 min ; voir bloc B) |
| Il n'y a pas de pénalité offensive de taille, seulement défensive (un 187 cm marque 49 en PF) | lolek5232, markoivica, #ex-yugo | 2026-08-04 07:10-07:36 | avis (v2) |
| Les joueurs peuvent jouer à 5 postes sans pénalité : « plutôt un bug ». Rebond d'un SF « pas inutile mais PF/C prennent les rebonds » | grobarbrate, lolek5232, #ex-yugo | 2026-08-04 09:21, 08-05 17:33, 08-10 22:38 | avis |

## F2 Joueurs / fatigue / forme
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Récupération (août) : de 1 à 10 de fatigue -1/jour, de 11 à 20 -2/jour, etc. ; manuel : « 0,5 point + 10 % par jour » ; l'endurance ne change pas la récupération (réponse du dev), elle change seulement ce que l'on gagne en jouant ; un 68 d'endurance à 20 de fatigue a perdu 2 en un jour | grobarbrate, svarog_, lolek5232, #ex-yugo | 2026-08-07 08:34-09:27 | confirme (skill joueurs, table) |
| Avis : l'endurance joue peu dans un match, elle fait monter la fatigue plus vite et la rend plus dure à enlever ; il faudrait 70 d'endurance pour ne jamais passer au jaune | lolek5232, #ex-yugo | 2026-08-01 21:08, 08-07 08:59 | avis |
| Deux défaites de suite avec « soft » pour reposer les joueurs : fatigue de l'équipe qui monte quand même ; blessures aléatoires (2 chez l'adversaire en soft) | grobarbrate, #ex-yugo | 2026-08-20 18:10-18:13 | avis |
| PS de joueurs en août : équipes de 53 à 58 de force, un 71 de PS à 20 ans, 20 ans à 56-57 achetés 1,5-2 M | grobarbrate, joomi1, lolek5232, svarog_, #ex-yugo | 2026-08-16 17:34-17:57, 08-17 10:07-10:19 | complète (échelle pré-reset ; les PS post-reset de 41-54 à la sortie d'académie : voir bloc C) |

## F3 Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Pot 10 : 18 compétences sur 8 entraînements en moyenne (lolek5232) ; 12 compétences en 6 entraînements avec deux fois +2 en défense = pot 9-10 (grobarbrate) | lolek5232, grobarbrate, #ex-yugo | 2026-08-02 02:35-08:38 | avis (pré-réforme du 10/08 ; dev 06/09 : pot 10 = +26 à 16 ans sur 2 compétences) |
| Un 20 ans tiré à 60 en 6 compétences ne peut pas atteindre 100 (calcul de lolek5232 : max 73 en 4 saisons + 1 entraînement) -> un joueur à 100 de total est « mathématiquement impossible » : cause des joueurs OP de départ | lolek5232, #ex-yugo | 2026-08-03 13:40 | confirme (origine du reset) |

## F4 Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Records (août, pré-reset) : 4,5 M pour un joueur (20/08), offre minimale suivante 2 370 375 pour un 19 ans PG ; un 20 ans parti à 90 k ; avant : « les premiers top-class à 300 k » | grobarbrate, lolek5232, #ex-yugo | 2026-08-03 20:45, 08-10 22:29, 08-20 07:24-09:48 | complète (historique : inflation x15 en 2 mois) |
| Jeunes 16 ans avec compétence > 40 : aucun vendu sous 1 M (30/07) ; avis : « revendre plutôt que garder » | lolek5232, #ex-yugo | 2026-07-30 17:23 | avis (pré-reset) |
| Après le reset, les prix repartiront bas puis monteront (avis) | grobarbrate, lolek5232, #ex-yugo | 2026-08-20 09:48, 11:25 | avis (confirmé par les prix de septembre : 1,2-1,365 M record) |

## F5 Divers
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Deux réglages par défaut distincts (ligue / amical) disponibles depuis début août ; édition directe d'un match possible mais seulement sur mobile (pas sur PC à cette date) | grobarbrate, lolek5232, #ex-yugo | 2026-08-07 09:35-10:12 | confirme (skill saison/tactique : tactiques de ligue et d'amical séparées) |
| Bug : le rapport d'académie arrivait à des heures différentes (3 fois à des moments différents), deux fois la même semaine | lolek5232, #ex-yugo | 2026-08-05 16:27-16:28 | confirme (bug déjà noté 29/07) |

---
# SYNTHÈSE (écrite en fin de lecture, 5000 lignes lues)

## Lignes lues
1 à 5000 de `data/discord/BasketVibe/discord_BasketVibe_export.txt`, message par message, canaux #general, #economy, #engine, #academy, #help, #ex-yugo. Période : 2026-05-31 -> 2026-10-09 (#general) et 2026-07/08 (autres canaux). Environ 60 % des lignes datent d'AVANT le reset (annoncé le 11/08, exécuté le 30/08) : économie, prix, moteur v1/v2 périmés. L'essentiel exploitable est dans les blocs B, C et D (septembre-octobre 2026, v3/v4).

## Trouvailles qui changent une décision (par ordre d'impact)
1. Coupe quotidienne : les matchs de coupe prennent par défaut le préréglage d'amical (bug avoué par le dev le 18/09, svarog_ + vachacz, #engine) ; correction non confirmée. Action : vérifier la tactique enregistrée du match de coupe, pas celle d'amical. (Bloc D1.)
2. Académie : le dev lui-même conseille de tirer vers 70-80 % (le recul absolu est moindre, deux juniors corrects pendant que ceux qui attendent 100 % n'en ont aucun) ; lolek5232 : l'écart 82 % -> 100 % est négligeable pour 5 semaines (21/07, 23/07, #academy / #ex-yugo). Cohérent avec une décision tirer/attendre au cas par cas ; ne remplace pas la table M§4.2. (Bloc C4.)
3. Personnel : la facture hebdomadaire = le MAX de la somme des salaires de la semaine (vachacz, #help, 03/09), et médecins/kinés : embaucher les médecins APRÈS la blessure fonctionne (durée recalculée, vachacz 14/09, 31/08). Action : ne pas payer de médecins en continu. (Blocs B6, D5.)
4. Potentiel d'un agent libre = aléatoire entre 3 et 9 (vachacz 07/09) ; marché : aucun 20-21 ans en vente (graine de départ, vachacz 05/10) ; groupes 24-25 et 27-28 ans. Action achat : la cible 20-21 ans n'existe pas, un agent libre ne dépasse jamais 9. (Blocs D4, C2.)
5. Moteur (v3, 12/09) : pénalité >36 min presque doublée ; mesure du dev sur ~100 matchs : un 5x48 min gagne encore le Q4 de +5,12 à domicile et +2,88 à l'extérieur en moyenne -> la composition à rotation courte reste viable en ligue, la tactique adverse (cinq connu) se prépare. (Bloc B1.)

## Ce qui contredit nos skills / connaissance.md (à valider avant tout changement ; je n'ai rien modifié)
- Académie, chronologie : le dev dit le 06/09 « un tirage académie sort sans décimale, à corriger » : vérifier si nos juniors affichent des décimales (si oui, le signal « pop = potentiel » du 1er entraînement s'efface). Non contradictoire avec les skills, mais à contrôler sur `silver`.
- Fatigue de coupe : en pilote 25 % (09/09) puis News 23/10 : coupe sans fatigue. Les avis de septembre sont périmés.
- Départage et formes : rien de nouveau en conflit direct avec connaissance.md.
- connaissance.md ligne 126 « niveau d'académie élargit aussi les tranches » : confirmé et précisé par les joueurs (pré-reset : plafond 41 à 26 %, 47 à 55 %, 60 à 100 % ; ne vaut plus tel quel après la réforme du 10/08).
- connaissance.md dit « TS recalculé une fois par jour » : le dev précise « chaque jour à 00:00 heure UE, je crois » (03/09) -> OK mais « I guess ».
- Pas de contradiction avec `basketvibe-tactique` sur l'absence de pénalité de poste ; confirmation répétée (vachacz 18/07, 09/09).

## Points « nouveau » à prioriser pour une vérification chiffrée (sources nos données)
Mesure du dev : 222 cm au poste PG ≈ 1,7 pertes de balle en moyenne (v2) ; économie du 19/08 : amicaux 120 k/semaine, sponsor 100 k, académie max 100 k, salaires de départ 240-250 k ; prix record 1,2-1,365 M (17/09) ; PS de sortie d'académie 41-54 ; 8 pops/saison pour un pot 10 à 16 ans (18 à 24 selon le dev pour un 3 étoiles, 24/09).

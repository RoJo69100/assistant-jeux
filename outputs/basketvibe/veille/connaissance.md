# Connaissance BasketVibe (index par thème)

Créé le 2026-10-27 par la veille ; complété le 2026-10-29 (Discord : delta du 29/10, 122 messages ; historique 2026-05-31 → 2026-10-09 jamais lu, 9 773 messages, dont 642 du développeur `vachacz`). Chaque entrée : fait, source, date, auteur, statut (confirmé / complété / contredit / en doute). Les entrées ne sont jamais effacées. Les entrées du 29/10 sont marquées « (29/10) ». Complété le 2026-10-30 par la lecture de l'historique Discord 2026-05-31 → 2026-10-09 (section « Lecture intégrale », propositions V-20261030-n). Les skills `basketvibe-*` contenaient déjà l'essentiel de l'historique (académie, sponsors, enchères, fatigue, 36 min) : les lignes ci-dessous marquées « confirmé (skill) » ne demandent aucune proposition.

## Tactique / moteur
| Fait | Source | Date | Statut |
|---|---|---|---|
| Fatigue v4 : pénalité 0 / −4 / −15 / −30 / −50 % à fatigue 0 / 20 / 40 / 60 / 80, attaque = défense | News | 2026-10-17, 2026-10-27 | confirmé (2 News ; `gold.bv_fatigue_plan.penalty_v4`) |
| Blessures : Soft 60 %, Medium soft 80 % du neutre ; +40 % au Q4 au-delà de 36 min | News | 2026-10-19, 2026-10-27 | confirmé |
| v4 actif en ligue, coupe, amical depuis le 27/10 | News | 2026-10-27 | confirmé (complète « juste après la saison 1 » du 19/10) |
| Duels : ~80 bat nettement ~40 ; bots plus faibles | News | 2026-10-27 | complété (nouveau) |
| Zone défensive Rim −3 % 2P% / +5 % 3P% max ; Perimeter inverse ; Neutral 0 | News | 2026-10-19, 2026-10-27 | **confirmé** : l'utilisateur, 2026-10-30 (« Rim existe, nouveauté du nouveau engine » ; actif en coupe et en ligue, `area_step` dans l'export de coupe) ; « amicaux seulement » (19/10) est dépassé |
| Origine de la zone : proposition du développeur « Defense area », shift de 2P/3P d'environ ±4-5 %, « l'effet pourrait être multiplié par le focus défensif » ; la zone remplace l'idée de défenses 3-2 / 2-3 / homme-à-homme (grobarbrate propose des bonus de 10 % PG-SG-SF pour 3-2 et 15 % PF-C pour 2-3, refusé implicitement) | Dev vachacz, #engine | 2026-09-10 20:19 et 21:03 | en doute : le multiplicateur « focus » est une proposition, non confirmée par la News (29/10) (V-20261029-3) |
| Idée jumelle « Driving frequency » (plus de tirs non assistés après action individuelle) : « fuzzy », pas annoncée depuis | Dev vachacz, #engine | 2026-09-10 | en doute |
| Focus offensif (v3, amicaux d'abord) : un focus ciblé peut rediriger jusqu'à 50 % des points vers un seul joueur si les autres sont en passe avec focus bas ; bouton Reset ajouté | Dev vachacz, annonces | 2026-09-07 18:08 | complété (V-20261029-1) |
| Rééquilibrage du focus offensif face au focus défensif adverse (cas limites corrigés) | Dev vachacz, annonces | 2026-09-14 06:23 | complété |
| Reprises de volée après rebond offensif, lancers francs manqués gérés, fautes tactiques en fin de match pour l'équipe qui court après le score (v3, nouveaux matchs) | Dev vachacz, annonces | 2026-09-08, 2026-09-09 | complété (V-20261029-2) |
| Pénalité >36 min : 8 % → 10 % → 12,5 % → 20 % (13/09) ; le dev propose « X entre 36-42 min et 2X entre 42-48 » (idée IA) pour limiter l'aléa des dernières minutes | Dev vachacz, general / engine | 2026-09-07, 2026-09-12 | confirmé (skill) ; l'idée X/2X en doute (non appliquée) |
| v4 = v3 au 04/10 (changement technique) ; v3 gelé ; changements du v4 jusqu'à la fin de la saison, d'abord en amical | Dev vachacz, #engine | 2026-10-04 | confirmé (cohérent avec News 19/10, 27/10) |
| Défense agressive = « arme à double tranchant » : boost sur un match au prix de la fatigue ; alterner avec Soft | Dev vachacz, #engine | 2026-09-19 | confirmé (cohérent v4 : fautes et blessures suivent l'agressivité) |
| Matchup : le défenseur principal est le joueur du même rôle (poste de terrain) que le tireur ; aucune pénalité de poste sauf aux rebonds ; la taille et la physique pèsent plus | Dev vachacz, #engine | 2026-07-09, 2026-07-18 | confirmé (skill) |
| Les fautes suivent l'agressivité ; Lock : fautes du défenseur plus réalistes | News | 2026-10-27 | complété (sens non précisé) |
| Moteur v5 de micro-améliorations ; v5 en amicaux seulement (annonce du 28/10 : pas de 20 s mortes, tirs de fin de quart) | News | 2026-10-27, 2026-10-28 | complété (effet inconnu ; mesure = points de Q4 en amical) |
| Avis « 48 min en défense normale avec fatigue < 30 ne se remarque pas » | Com heldermoreno | 2026-10-09 | contredit (v4 : −4 % à 20, −15 % à 40) |
| Avis « fatigue 30-40 % n'atrophie pas vraiment le jeu, c'est surtout le dernier quart des joueurs à 48 min » | Com chanceler, portugal | 2026-10-05 | contredit pour le v4 (−15 % à 40) ; vrai en v3 [Dev 2026-09-13 : « fatigue 20 : impact mineur »] |
| Fatigue v3 : à 5-10 presque aucun impact ; plus l'endurance est basse, plus la fatigue tombe lentement | Dev vachacz, help | 2026-08-07 | confirmé (skill, table du manuel ; v3) ; **corrigé le 2026-10-31** : le « it » est ambigu, l'endurance joue sur le GAIN de fatigue, la récupération est identique pour tous (0,5 + 10 %) [M§5.6 ; manuel cité #portugal 2026-09-15] ; « 10-20 de fatigue n'est pas grave » (Dev 2026-08-07) est en doute pour la v4 (−4 % à 20) |
| Orange = nouvelle zone défensive (barre de l'écran tactique/match, « I would say », la description est lisible en vue bureau) | GM elemke., general | 2026-10-29 08:39 | en doute (formulation dubitative ; un utilisateur demandait la légende des barres) (V-20261029-4) |

## Calendrier / coupes
| Fait | Source | Date | Statut |
|---|---|---|---|
| Saison 1 = 22 journées ; rollover 26/27.10 ; coupes 28/10 ; journée 1 saison 2 lundi 02/11 | News | 2026-10-24, 2026-10-27 | confirmé (lève le « déduit ») |
| Coupe nationale si ≥ 8 clubs actifs dans le pays, sinon Coupe multinationale (16 écarté) ; un match par jour dès le 28/10 | News | 2026-10-23 | contredit l'annonce Dev « 8 ou 16 équipes, other-cup » (Dev 2026-10-18/20) |
| Coupes : aucune blessure, revenu, expérience, fatigue, avantage du terrain | News | 2026-10-23 | complété (règles inconnues jusque-là) |
| Coupe pilote « BV Cup » (septembre) : l'équipe au TS le plus faible jouait à DOMICILE ; tactique réglable depuis la page de la coupe (promis) | Dev vachacz, general | 2026-09-03 13:50, 14:42 | contredit par la News du 23/10 (coupes sans avantage du terrain) : règle périmée pour la coupe actuelle |
| Après la saison : coupes nationales un match par jour pendant l'intersaison ; saison suivante soit coupe complète soit système suisse | Dev vachacz, general | 2026-10-04 10:53 | confirmé en partie (News 23/10 : un match par jour) ; système suisse en doute |
| Amicaux sur jours de ligue : indécis ; prérequis à tout changement de fatigue ; si moins d'amicaux, fatigue de coupe relevée | Dev vachacz, general | 2026-09-15 13:46 | en doute (décision jamais annoncée) |
| Une équipe ne peut pas dominer à la fois ligue et coupe : voulu | Dev vachacz, general | 2026-09-15 | confirmé (intention) |
| Équipes inactives : même cinq, même tactique ; on peut préparer la tactique adverse | GM elemke., general | 2026-09-12, 2026-10-07 | confirmé (avis GM) |

## Entraînement
| Fait | Source | Date | Statut |
|---|---|---|---|
| Historique d'entraînement : une ligne par semaine même sans gain, entraînement manqué pour blessure indiqué | News | 2026-10-25 | complété |
| Entraînement secondaire = la moitié du principal ; toutes les compétences montent à la même vitesse | Com txetx, españa | 2026-10-03 | confirmé (skill, manuel) |
| Idée du dev : choisir plusieurs compétences et répartir la puissance d'entraînement (1 → tout, 2 → moitié chacune, 3 → tiers) ; « pas d'urgence » | Dev vachacz, help | 2026-07-26 13:17 | en doute (jamais livré ; le jeu garde principal/secondaire) |
| Un joueur au potentiel 6 de 25 ans gagne 9 compétences par saison ; un potentiel 10 gagne +26 dans deux compétences à 16 ans ; la plupart des joueurs ont un potentiel 6-7 | Dev vachacz, general | 2026-09-06 06:37, 06:45 | confirmé (skill, §8.3) |
| Âge : l'algorithme de départ a été corrigé (les 30+ progressaient trop) ; courbe TSP max à 31 ans puis déclin | Dev vachacz, general / academy | 2026-08-03, 2026-09-06 | confirmé (skill) |
| Avis : potentiel 3 = « 2 crans par semaine, parfois 3 à potentiel maximal » | Com dixi2499, italia | 2026-10-29 11:40 | en doute (avis, non chiffré sur nos données) |
| Avis : le premier tirage de la saison a « de 1 à n entraînements de plus » que les tirages suivants ; l'an dernier un junior tiré avait fait 5 entraînements sur 8-9 | Com dollarius_80489 / lucadrago5, italia | 2026-10-29 11:08, 11:54 | complété (avis, plausible : un junior tiré dès le début de saison a plus de semaines) |
| Blessure : « points de blessure » décomptés chaque jour, les médecins en retirent plus : la blessure est fractionnaire ; l'âge n'est pas (encore) un facteur de blessure | Dev vachacz, general / help | 2026-08-31 15:43, 2026-08-10 16:22 | complété (V-20261029-5) |

## Interface / stats / divers
| Fait | Source | Date | Statut |
|---|---|---|---|
| Tirs affichés FT%, 2P%, 3P% ; ORB/DRB ; leaders ≥ 50 % de présences ; Totals/Averages ; notes privées effacées au transfert ; filtres marché ; affluence Schedule | News | 2026-10-22, 2026-10-25 | complété |
| Outil d'analyse avancée = pack Supporter 2027 | News | 2026-10-22 | complété |
| Vue bureau (« desktop view ») du site : légende des barres de l'écran | GM elemke., general | 2026-10-29 | complété (UI mobile sans description) |
| Le dev relance un match 1 000 fois pour juger la chance ; défaite à 68 % de victoire = normale ; les cotes d'avant-match utilisent forme et fatigue mais restent indicatives | Dev vachacz, general | 2026-08-24, 2026-09-26 | confirmé (skill) |
| Rapport de bug : salon dédié ou fonction Report du jeu (le dev ne suit pas les fils cachés) | Dev vachacz | 2026-07-19 … 2026-09-18 | confirmé |

## Transferts / finances / académie
| Fait | Source | Date | Statut |
|---|---|---|---|
| Taxe de revente dégressive : idée de joueur, non décidée ; test de potentiel peut être relevé | Dev | 2026-10-22 | en doute (rien de nouveau le 27/10) |
| Sponsors : Fluxora Balance = 640k garanti + 15k/victoire (plafond 970k) | Export finance_sponsor (fait-2026-10-27) | 2026-10-27 | confirmé (nos données, pas une News) |
| Sponsors : 6 contrats au choix, « Stability » par défaut ; avant : fixe 100 000 ; premier match à domicile 250-300k, jusqu'à 400k | Dev vachacz, economy / help | 2026-09-05, 2026-10-02 | confirmé (skill) |
| Prime de victoire de ligue 200 000 « encore de l'avant-reset, à revoir en fin de saison 1 » | Dev vachacz, help | 2026-09-27 08:48 | en doute (rien annoncé depuis) |
| Salaire = fonction des compétences entraînables ; TS recalculé une fois par jour, sur les 8 meilleurs | Dev vachacz, general | 2026-06-24, 2026-08-13, 2026-08-31, 2026-09-03 | confirmé (skill) ; complété le 2026-10-30 : le TS est aussi recalculé juste après un transfert réglé (News 2026-09-04), donc « une fois par jour » n'est plus exact (V-20261030-3) |
| Effectif minimum 8 (libération bloquée sous 8, mise en vente limitée au-dessus) ; discuté 5 ou 10, maintenu à 8 | Dev vachacz, general | 2026-09-03, 2026-09-05 | confirmé (skill) |
| Enchères : maximum auto, +3 par minute sous la minute / pas plus de 15 min, puis phase à l'aveugle ; l'enchère maximale ne peut pas dépasser le solde | Dev vachacz, help / general | 2026-07-21, 2026-07-26, 2026-09-03 | confirmé (skill ; « +3 » hérité de la mémoire du dev, « I guess ») |
| Aucune règle de pays pour le bonus homegrown (plafond 40 000 à ~60 min) | Dev vachacz, help | 2026-09-10 13:25 | confirmé (skill) |
| Académie : jeudi 09:00 ; courbe non linéaire (70-80 % rapide, 100 % cher), baisse fixe de 5 % ; répartition potentiel 10 % chacun (22/07) remplacée par la table croissante avec bonus à 100 % (27/07) ; test de potentiel Low 1-3 / Decent 4-7 / High 8-10 | Dev vachacz, academy | 2026-07-22, 2026-07-23, 2026-07-27, 2026-08-09 | confirmé (skill) ; la répartition « 10 % chacun » est périmée |
| Rapport tiré après le saut de force du jeudi (99 → 100 % : junior tiré de la barre 100 % avec bonus) | Dev vachacz, polska | 2026-09-28 06:24 | confirmé (skill) |
| Potentiel de nos joueurs visible sur la fiche (tranche) ; manuel §11 « Unknown » | News 2026-10-20 / M§11 | 2026-10-20 | contredit (manuel en retard, 1 joueur observé) |
| Académie : « 90 % suffit » vs 27,3 % / 43,9 % de High à 90 / 100 % | Com / M§4.2 | 2026-10-22 | contredit (manuel fait foi) |
| 29/10, premier tirage de la saison 2 : avis opposés sur un junior à 100 % d'académie (C de 17 ans, rebond faible) : « ne le promeus pas » (lucadrago5, dcarra.), « promeus et revends » (dixi2499) ; à 69 % « garde la jauge » (heldermoreno, jorgeac25) ; un joueur a dépensé 150k sur l'académie une semaine sans junior utile | Com, italia / portugal | 2026-10-29 | complété (avis seulement ; non vérifié ; décision à prendre avec `basketvibe-academie`, pas avec ces avis) |
| Marché : un 3 étoiles de 16 ans se vend 3,5-4 M (annonces 29/10) ; un acheteur a poussé une enchère à 4 M | Com lolek5232 / dixi2499 / heldermoreno | 2026-10-29 | complété (avis ; à comparer à `gold.bv_market_price_known`, max observé 2 894 063 au 22/10) |

## Lecture intégrale de l'historique Discord (passage du 2026-10-30)
Périmètre : `discord_BasketVibe_export.txt` (9 775 messages, 2026-05-31 → 2026-10-09 ; les 642 du développeur `vachacz` lus un par un, première ligne) + `export discord basketvibe.txt` (2 953 messages, 2026-05 → 2026-10 : release-notes lues en entier, 79 messages longs du dev relus en entier, avec le texte multi-lignes). Les messages de joueurs (≈ 9 100) n'ont pas été relus un par un : balayage par mots-clés (annonces de règles, mesures) sans résultat nouveau, donc les avis de joueurs restent des hypothèses. Dev = `vachacz` (Łukasz, développeur seul).

### Tactique / moteur
| Fait | Source | Date | Statut |
|---|---|---|---|
| v2 : aucune pénalité de poste hors rebonds ; hauteur et emplacement PG–C comptent ; défenseur principal = même emplacement que le tireur ; v2 en amical 09/07, en ligue 22/07 | Dev, #engine / release-notes | 2026-07-09 21:47, 2026-07-18 21:08, 2026-07-22 | confirmé (skill) |
| v1 : balle en main, athlétisme, poids/IMC sans effet ; lancers francs mal équilibrés (échec constaté par le dev) | Dev, #engine | 2026-07-06 18:49 | complété (historique, v2 corrige) |
| Le 3P influence les lancers francs (2/3 le 2P, 1/3 le 3P) ; tactique/focus défensif relevés ; pénalité >36 min 8 → 10 % | release-notes | 2026-08-08, 2026-08-09 | confirmé (skill) |
| Le passeur n'est plus une compétence d'équipe : « dernier passeur » choisi par poste et rôle ; hasard du tir réduit ; plafond 3P à 50 % des tirs (avant 70 %) ; rebonds redistribués (leaders > 20/match) | release-notes | 2026-08-24 | confirmé (skill communauté) |
| v3 : plafond de tirs à 3 levé pour les meilleurs tireurs à 3 (détail non divulgué) ; bug de distance au cercle dans la répartition des rebonds corrigé | release-notes | 2026-09-14, 2026-09-16 | complété (effet : 3P% un peu plus haut en v3) |
| Le dev ne divulgue ni formules ni équilibre des compétences ; la formule de PS « ne sert pas » au moteur, qui lit les compétences possession par possession | Dev, #engine | 2026-07-13, 2026-07-18, 2026-09-17 | confirmé (PS = indicateur, skill) |
| Tactiques verrouillées 15 min avant le match ; lineup propre à la prolongation (OT) ; ordre des consignes : focus offensif en premier ; tactiques de ligue et d'amical séparées ; préréglage modifiable par match | release-notes | 2026-08-05, 2026-09-11, 2026-09-27, 2026-10-08 | confirmé (skill saison M§1.3) ; l'OT et l'ordre sont complétés |
| Repos manuel : le dev a appliqué lui-même des « repos » (fatigue remise) aux joueurs : 19/08 (par jour sur les amicaux), 24/08 (erreur double), 29/08 (« daily »), avant la dernière journée du 29/08, 13/09 (« solution temporaire », par clic au back-office) | Dev, #general / release-notes | 2026-08-19, 2026-08-24, 2026-08-29, 2026-09-13 | en doute : on ignore s'il le fait encore en v4 ; l'historique de fatigue d'avant le 27/10 a pu être remis à zéro hors règles (V-20261030-6) |
| Le repos ne dépend pas de l'endurance | Dev, #general | 2026-09-09 16:02 | en doute (« if I recall ») |
| Défense agressive : fatigue après match (+ calibrage de l'impact) dès juin ; corrélation avec les fautes/blessures « seulement si défense agressive » | release-notes / Dev | 2026-06-21, 2026-09-14 | confirmé (cohérent v4) |
| Débits de score : 1 000 simulations d'un match ≈ 123,6–133,0 pts ; ~10 % de matchs > 150 pts jugés trop hauts ; moteur recalibré à des scores plus proches de la NBA | Dev, #general / release-notes | 2026-07-24 14:21, 2026-07-26 | complété (historique, avant reset) |
| Piste « équipe à 48 min » : le dev dit que jouer contre une équipe à 48 min ne garantit pas 100 % de victoire ; bots −10 en toutes compétences, expérience remise à zéro (2/08) | Dev / release-notes | 2026-08-21, 2026-08-02 | confirmé (skill) |
| Fan-out rejeté / en attente : tactiques d'équipe (zone 3-2, 2-3, individuelle) refusées au profit de la « Defense area » ; « Driving frequency » flou | Dev, #engine | 2026-09-10 | confirmé (voir lignes du 29/10) |

### Calendrier / classement / amicaux
| Fait | Source | Date | Statut |
|---|---|---|---|
| Points 2 victoire / 1 défaite jouée / 0 forfait ; forfait = 20–0 si le cinq ne peut pas être aligné | release-notes | 2026-08-13 | confirmé (skill saison) |
| Départage : « h2h » (confrontation directe) ; la News du 23/09 dit « h2h is not more important than +/- » (probable faute de frappe de « now more important ») | Dev, #help ; release-notes | 2026-10-03 18:59, 2026-09-23 | confirmé (skill) ; ordre exact en doute pour la News (V-20261030-2) |
| Promotion/relégation 4 montent, 4 descendent (pas de 2/4) ; T4 UE ajouté le 16/07 ; inactivité 30 ou 45 jours (45 retenu) | Dev, #general | 2026-07-16 20:08, 2026-08-11 | confirmé (skill) |
| Amicaux : lancés le 29/06 ; invitation valable 2 jours ; 5 programmés au plus ; toujours à domicile (jusqu'au 29/07), puis choix domicile/extérieur ; annulation possible (11/08) ; recettes domicile = extérieur (14/07) ; « friendly finder » (22/07, déplacé dans Schedule le 04/10, 2 sections le 26/09) ; pas de blessure, 10 % d'expérience/fatigue (juin) | release-notes | 2026-06-29, 2026-07-14, 2026-07-22, 2026-07-29, 2026-08-11, 2026-09-26 | complété (V-20261030-4) ; « pas de blessure » contredit par v4 (voir 19/10) |
| Coupe pilote : 5 manches, 1 par jour, dès 04/09 ; coupe « BV Cup » globale prévue à 10/11 manches, puis 1-2 matchs par semaine | release-notes / Dev | 2026-09-03, 2026-09-05 | contredit pour la forme actuelle (News 23/10 : un match par jour, nationale/multinationale) ; périmé |
| Fuseau Asie-Pacifique : Asia/Tokyo (UTC+9), coup d'envoi 20:00 | Dev, #general | 2026-08-08 10:20 | complété (sans effet pour nous : Europe) |
| Un joueur de 16 ans « vit ~3 ans réels » (56 jours ≈ 2 mois par saison) | Dev, #general | 2026-09-04 | confirmé (calcul : saison de 22 journées ≈ 8 semaines) |

### Entraînement / vieillissement
| Fait | Source | Date | Statut |
|---|---|---|---|
| Réforme d'entraînement du 10/08 : baisse des compétences de départ des juniors, plafond d'entraînement abaissé, vieillissement de toutes les compétences, juniors de 16-17 ans, suppression de l'entraînement en cours de saison ; juniors de 17 ans +2 en bandes ; retraite à la fin de l'année des 38 ans | release-notes | 2026-08-10, 2026-08-11 | confirmé (skill) |
| On peut entraîner jusqu'à 99, plus cher ; aucun autre plafond ; un joueur s'entraîne une fois par semaine quelles que soient ses minutes ; < 21 ans peuvent grandir ; académie/effectif de départ sans décimales | Dev, #help | 2026-09-08, 2026-09-21, 2026-09-13 | confirmé (skill) |
| Avant la réforme, un 16 ans gagnait 15 compétences par saison et une compétence de 45 à 60 (« réduit à 45 → 60 ») | Dev, #academy | 2026-07-14 19:13 | contredit (modèle remplacé le 10/08) |
| Multiplicateur d'entraînement du potentiel 10 = 2,20 ; le dev envisage 2,10 ou 2,00 | Dev, #reset | 2026-08-16 14:43 | en doute (aucune annonce de baisse depuis ; skill à vérifier) |
| Forme : variation aléatoire ±1 par semaine (psychologues décalent les chances) ; remise à 6 au changement de saison ; changement de forme affiché à côté de l'entraînement (03/10) | Dev / release-notes | 2026-07-20, 2026-09-11, 2026-10-03 | confirmé (skill) |
| Blessures : durée étendue à 3-12 jours (26/08) ; probabilités inchangées (fatigue, endurance, kinés, agressivité défensive, minutes) ; âge pas un facteur ; kinés −50 % de risque max, médecins −50 % de durée max | release-notes / Dev | 2026-08-10, 2026-08-26, 2026-09-26 | confirmé (skill économie) |

### Académie
| Fait | Source | Date | Statut |
|---|---|---|---|
| Rapport d'éclaireur chaque semaine (depuis le 14/07), tranches 25 → 20 (11/07) puis tests à 25 000 (21/07), potentiel révélé par les tests (30/07), âge 16-18 (16/07) puis 16-17 (10/08), jeudi 09:00 « jour de l'académie » (09/08) | release-notes | 2026-07-11 … 2026-08-10 | confirmé (skill) |
| Courbe non linéaire, baisse fixe de 5 % par semaine, signer = −50 % (le dev a envisagé 33 %, décidé « pas touché ») | Dev, #academy | 2026-07-14, 2026-07-15, 2026-07-22, 2026-07-23 | confirmé (skill) |
| Le niveau d'académie élargit aussi les tranches de compétences, « peut-être plus important que le potentiel » | Dev, #academy | 2026-07-21 19:48 | en doute (un message, non repris dans la table) |
| Les 3 candidats viennent de postes différents et suivent la répartition NBA (C 17 %, SG 23 %, un pivot « toutes les 2 semaines ») | Dev, #academy | 2026-07-22 18:26, 18:43 | contredit par nos données : rapport du 2026-10-15 = PG, SF, SF ; rapports du 22/10 (PF, SF, C) et 29/10 (PG, C, SG) conformes (`silver.bv_academy_candidates`) (V-20261030-5) |
| Départ post-reset : académie à 80 % pour tous ; 2 tirages à 60 % en plus (3,5 % de potentiel 9) ; 1,7 % de potentiel 10 au premier tirage | Dev, #reset | 2026-08-12, 2026-08-16 | confirmé (historique, sans effet aujourd'hui) |
| Visibilité du potentiel d'un joueur en vente : 4 options en sondage (masquer / montrer si révélé par le propriétaire / toujours / test par l'acheteur) | Dev, #general | 2026-09-24 22:33 | à surveiller (résultat du sondage inconnu ; 20/10 : visible sur nos joueurs) |

### Finances / transferts / personnel
| Fait | Source | Date | Statut |
|---|---|---|---|
| Sponsor : 500 000 une fois par saison (jusqu'au 22/07) → 100 000 par semaine ; 6 contrats au choix en début de saison, « Stability » par défaut, pas de changement en cours de saison, sans conséquence autre que financière ; tout-ou-rien supprimé | Dev / release-notes | 2026-07-22, 2026-10-02, 2026-10-03 | confirmé (skill économie) |
| Économie du 21/08 : recettes d'amical −30 %, investissement académie maximal 100 000, rapport d'éclaireur ne coûte plus plus cher que tous les salaires ; « plus facile de gonfler que de dégonfler » | Dev, #economy | 2026-08-19, 2026-08-21 | confirmé (skill : 100 000 par semaine) |
| Personnel : kinés 4 × 5 000, médecins 2 × 10 000 (26/08) ; psychologues 2 × 10 000 (+5 % de chance de hausse de forme) et marketing (28/08, annoncé à 10 000 par le dev, 12 500 constaté dans nos données le 16/10 : 70 000/semaine) | release-notes / skill | 2026-08-26, 2026-08-27, 2026-08-28 | confirmé (skill ; les 10 000 du dev étaient une proposition) |
| Popularité : +2 victoire, −3 défaite, à domicile seulement, remise à 70 ; bonus homegrown 200 par minute, plafond 40 000 par semaine (~66 min par match) | release-notes | 2026-08-28 | confirmé (skill) |
| Popularité : idée du dev que les matchs à l'extérieur comptent (« une victoire à l'extérieur vaut plus ») ; remise à 70 « si en dessous de 70 » (« au-dessus, bon… », phrase inachevée) | Dev, #help | 2026-10-07 20:24, 20:45 | en doute : la remise à 70 pourrait ne s'appliquer qu'aux clubs sous 70 ; notre club : 0,65 le 25/10 → 0,70 le 29/10 (`silver.bv_finance_weekly`), non concluant (V-20261030-7) |
| La DH (division hardiness) pourrait pondérer billetterie et sponsors ; « ajouter quelque chose pour la moitié haute » | Dev, #help | 2026-09-28 14:22 | en doute (intention, rien annoncé) |
| Renommée des joueurs (MVP match 0,25, MVP journée 0,5) → popularité/billetterie | Dev, #economy | 2026-09-10 | en doute (proposition, 11 ✅ de joueurs, rien livré) |
| Taxe forfaitaire de 5 % ; joueur acheté 2 semaines au club avant revente (29/07) → 7 jours (14/09) ; agents libres : naissance quotidienne, expérience plafonnée à 10 (16/07), enchère de 2 jours (30/07), TSP 360-420 (14/08) | release-notes | 2026-07-29, 2026-07-30, 2026-09-14, 2026-08-14 | confirmé (skill transferts/communauté) |
| Enchère maximale impossible au-dessus du solde ; enchère maximale abaissable ; historique d'enchères visible | Dev / release-notes | 2026-07-26, 2026-07-30 | confirmé (skill) |
| Transferts entre comptes de la même IP interdits (cas du 13/09 : joueur retiré du marché, pas de ban) ; solde négatif = blocage du marché | Dev, #general | 2026-09-03, 2026-09-13, 2026-09-12 | confirmé (skill pour le blocage) ; règle IP complétée |
| Pack Supporter : fonctions furtives (records individuels, vue du temps de jeu, comparaison de joueurs, planificateur d'entraînement) ; l'analyse avancée = ce pack | release-notes | 2026-09-26, 2026-09-27, 2026-09-29, 2026-10-03 | confirmé (skill) |

### Interface / stats
| Fait | Source | Date | Statut |
|---|---|---|---|
| +/- et PER (07/08) ; PER remplacé par EVAL (28/09), utilisé pour MVP et meilleur cinq (anciens MVP recalculés) ; FG% et 3P% de la page Joueurs : filtre « 10 » (texte tronqué) ; le dev note que les équipes à 5 × 48 min dominent le « top 5 de la saison » | release-notes | 2026-08-07, 2026-09-28 | complété (V-20261030-1) |
| Force : PS (joueur, visible seulement chez soi/en vente), TS (8 meilleurs), DH (11 meilleures équipes de la division) | release-notes | 2026-08-16 | confirmé (skill) |
| Coupes, chat de ligue (25/09), sondages dans les News (20/09), observateur en direct (12/09), calendrier (11/09), carte « Promote » (30/09) | release-notes | 2026-09-11 … 2026-09-30 | complété (sans effet sur les décisions) |

## Bugs
Tactiques mobiles sans OT (corrigé 2026-10-22) ; ordonnanceur de coupe nationale corrigé et Coupe multinationale reconstruite (2026-10-25). Bug de dates de rapport d'académie après passage à 1 semaine (Dev 2026-07-22, corrigé ensuite). Coupe : le planning révélait le score en direct (corrigé, Dev 2026-09-14). Walk-over avec effectif incomplet corrigé (Dev 2026-08-13, 2026-09-03).
Historique (release-notes 2026-06 → 2026-10, passage du 2026-10-30) : joueur à 7 fautes revenu au quart suivant (corrigé 02/07) ; plafond de 5 amicaux/invitations (corrigé 30/06) ; enchère au prix minimum refusée (corrigé 18/07) ; rapport d'éclaireur en double le même jour (corrigé 29/07) ; walk-over et coupe : planning décalé au 17/09 (03/09, à corriger) ; notifications de coupe affichées comme amicaux (04/09) ; quatre joueurs dans le lineup (corrigé 16/09) ; lineup de quart faux dans le play-by-play (15/09) ; depth chart utilisait le poste nominal au lieu de l'emplacement (corrigé 18/09) ; sauvegarde des tactiques après transfert (19-21/09, « retest requis ») ; résultat de coupe visible dans Schedule > Cups (corrigé 27/09) ; enchère à l'aveugle sans modification possible de l'enchère maximale (corrigé 27/09).

## Lecture intégrale des messages des joueurs (passage du 2026-10-31)
Périmètre : `discord_BasketVibe_export.txt` lignes 1-9835, `export discord basketvibe.txt` (16 225 lignes) et `discord_BasketVibe_part1.txt` (133 lignes), lus en entier par 3 agents (notes brutes : `lecture-joueurs-1.md` 494 lignes, `-2.md` 332, `-3.md` 254 ; ~490 entrées). Le corpus s'arrête au 09/10 : aucune mesure v4 (zone, agressivité, focus) n'y figure. ~60 % des lignes du premier fichier datent d'avant le reset (11/08) : prix, économie et moteurs v1/v2 périmés. Le skill `basketvibe-communaute` contenait déjà l'essentiel ; ci-dessous seulement ce qui change une décision. Statuts : avis = jamais une règle.

### Tactique / composition
| Fait | Source | Date | Statut |
|---|---|---|---|
| Changer un préréglage ou la tactique générale ne met PAS à jour un match déjà planifié : rouvrir le match et re-choisir | grobarbrate, vortexraijin (help) ; nhegas12, chanceler, jorgeac25 (#portugal) | 2026-09-05, 2026-09-20/21 | confirmé (3 sources ; deux joueurs achetés n'ont pas joué faute de ça) ; déjà dans `resume.md` |
| Vendre un joueur présent dans un préréglage bloquait la sauvegarde (« quarts non remplis ») ; contournement : éditer le préréglage ; correctif 19/09 18:20, « retest requis » 21/09 | tankre1792, heldermoreno, Dev (help) | 2026-09-18/21 | complété : après tout transfert, rouvrir le préréglage et vérifier les matchs planifiés |
| La coupe prenait le préréglage d'amical par défaut (bug avoué) | svarog_, vachacz (#engine) | 2026-09-18 | **à rouvrir (31/10)** : bug revu au tour 1 de la coupe du 28/10 (SF titulaire sur le banc, tactique différente des préréglages, le Dev soupçonne le préréglage de ligue ; usylum 2026-10-28) ; chez nous le match du 28/10 (MACCABI) porte le preset « League Tactic » dans `gold.bv_saisie_matchs`, les 29-31/10 « Cup » ; vérifier la tactique de chaque tour |
| Mesure du développeur sur ~100 matchs : un cinq à 48 min gagne encore le Q4 de +5,12 (domicile) et +2,88 (extérieur) en moyenne, malgré la pénalité > 36 min (presque doublée le 12/09) | Dev vachacz (#engine) | 2026-09-12 | complété (v3) ; la v4 n'est pas mesurée ; L-026 : Q4 −4 au-delà de 36 min en coupe |
| Défense agressive, 8 joueurs sur 10 : 43 lancers francs adverses contre 15 en soft, défaite de 22 ; seuils proposés : défense ≥ 55 pour le cran 4, ≥ 60 pour le cran 5 | chanceler, jorgeac25 (#portugal, chat) | 2026-08-29/30, 2026-10-04 | en doute (avis, v3 ; cohérent avec « double tranchant » et L-011/L-015) |
| Focus défensif 1 sur le pivot adverse : 48 points concédés | tankre1792 (help) | 2026-09-09 | avis (cohérent avec L-006) |
| Un joueur en « passe » tire quand même (17 tirs) ; « tout à 2 » tire des 3 pts ; un passeur réglé « tir » : mauvais pourcentage | grobarbrate, cobisixer, lolek5232 | 2026-07-22, 2026-09-09/14 | avis (1 cas chacun) |
| Pas de pénalité de poste hors rebonds, reconfirmé | vachacz | 2026-07-18, 2026-09-09 | confirmé (skill) |
| Un joueur de retour de blessure le jour d'un match de coupe n'a pas joué (fuseau soupçonné) | b.tothe.r, vachacz (help) | 2026-10-04 | en doute |

### Entraînement / académie
| Fait | Source | Date | Statut |
|---|---|---|---|
| Les juniors d'académie sortaient sans décimales (on repère un potentiel 10 au 1er entraînement) ; « je corrige » | aaaoooaaaa, grillanza_60069, vachacz | 2026-09-06 | **corrigé** : nos juniors (Bernard, Baron, Leclerc) ont des décimales dans `silver.bv_player_daily` au 30/10 |
| Potentiel d'un agent libre aléatoire entre 3 et 9 ; effectif de départ 3-9 ; potentiel des juniors identique selon les pays | vachacz (help) ; lolek5232 | 2026-09-07/08/14 | confirmé (Dev) ; déjà dans le skill communauté |
| Le développeur conseille de tirer vers 70-80 % d'académie ; l'écart 82 → 100 % « négligeable pour 5 semaines » | vachacz, lolek5232 (#academy) | 2026-07-21/23 | avis antérieur à la table du 27/07 ; ne remplace pas la table [M§4.2] |
| 71 000 par semaine donneraient la même force d'académie que 100 000 (2 captures non lues) | nhegas12, chanceler (#portugal) | 2026-09-13 | en doute : nos données n'ont que 100 000 par semaine (45 → 59 → 70, courbe du skill) ; aucun test possible sur l'historique |
| Équipe de départ : titulaires 24-28 ans potentiel 6-7, remplaçants 4-7, 2 juniors tirés d'une académie à 60 %, endurance plafonnée à 60 ; un jeune « d'origine » vendu High = potentiel moyen jusqu'à preuve (4-5 semaines d'historique) | Dev du 13/08, cité par carlomtlopes le 07/10 | 2026-10-07 | en doute (seconde main) |
| Mesures de sortie d'académie : PS 41, 48, 52 (16 ans, académie 92 %), 54 (17 ans) | esmosinag, hamsterj1312, ale92c, ori1919 (#academy) | 2026-09-13, 2026-10-08 | avis chiffré (ordre de grandeur) |
| Promouvoir un junior relancerait le délai de 7 jours du rapport (août) | faraone85, svg07 (#italia) | 2026-08-04 | périmé (jeudi 09:00 fixe depuis le 09/08) |

### Transferts / prix
| Fait | Source | Date | Statut |
|---|---|---|---|
| Taxe de 5 % confirmée : 1 010,0 k vendu, 959,5 k reçu ; « pas de taxe » (uthred9751, 23/09) est faux | heldermoreno (#portugal) | 2026-10-03 | confirmé (skill) |
| Prix du 27/09 au 04/10 probablement faussés : joueur banal acheté 60 k revendu 850 k à un compte japonais, 30 transactions suspectes, équipe de contrôle du développeur (05/10), 5 comptes bannis (08/10) | carlomtlopes, chanceler, sakota0 (#portugal) | 2026-10-05/08 | en doute (avis, non vérifié) : ne pas caler un plafond d'enchère sur ces ventes |
| Prix des 16 ans : PS 40 = 150 k (sem. 1) → 300 k (11/09) ; PS 42 = 350 k → 500 k ; 3 M (26/09, 03/10) ; 3,5 M entre amis ; un PS 52 listé 5 M (28/09) | mkeffe, grillanza_60069, dcarra. (#italia) ; #portugal | 2026-09-11 … 2026-10-03 | avis ; à comparer à `gold.bv_market_price_known` (max 2 894 063 au 22/10) |
| Aucun joueur de 20-21 ans en vente (graine de départ) ; groupes dominants 24-25 et 27-28 ans | vachacz, elemke., marekb9231 | 2026-10-05 | confirmé (Dev) |
| Le total de toutes les enchères maximales où l'on mène compte comme argent engagé | vachacz | 2026-07-26 ; confirmé 2026-09-06 | confirmé (déjà [M§10.3]) |

### Finances / personnel
| Fait | Source | Date | Statut |
|---|---|---|---|
| Personnel : la facture de la semaine = le maximum de la somme des salaires présents sur la semaine ; on peut embaucher les médecins APRÈS une blessure (durée recalculée) | vachacz (help) | 2026-09-03, 2026-08-31, 2026-09-14 | complété (déjà au skill économie) ; licencier les médecins avant le dimanche : chanceler paie quand même, **non testé** |
| Bonus homegrown : la coupe ne compte pas | vachacz | 2026-09-10 | confirmé (cohérent News 2026-10-23) |
| Fatigue de coupe 25 % en pilote (09/09) | #engine | 2026-09-09 | périmé (News 2026-10-23 : aucune fatigue en coupe) |
| Entraînement : jour de passage « samedi » (06/08, avant reset) | Dev | 2026-08-06 | périmé : dimanche 04:00 Paris observé |
| « ×0,63 dès 80 » | kotryk (#polska) | 2026-10-06 | contredit : le skill fait foi (×0,75 à 80, ×0,63 à 85) [M§8.4] |

## Lecture intégrale du 10/10 au 31/10, moteur v4 (passage du 2026-10-31, export Discord global)
Périmètre : 4 384 messages du 10/10 au 31/10 (export `discord_BasketVibe_part1.txt`, 14 581 messages), lus en entier par 2 agents (2 265 + 2 142 lignes ; notes `lecture-joueurs-4.md` ~150 entrées, `-5.md` ~95). **Aucune mesure v4 chiffrée de la pénalité de fatigue, de la zone, du focus ni de l'agressivité dans tout le corpus** : à produire par nos amicaux de test et `gold.bv_zone_jouee`. Le « 7,5 M » cité le 31/10 (nathanr_32176) n'a pas de nom de joueur.

### Tactique / moteur v4
| Fait | Source | Date | Statut |
|---|---|---|---|
| Zone défensive : −3 % de FG% dans la zone défendue, +5 % dans la zone laissée ; risque d'un pivot qui tire à 3 points | Dev vachacz, #polska | 2026-10-23 14:47 | confirmé (Dev) ; Rim à éviter face à un C tireur à 3 |
| Fautes v4 : 1 000 relances d'un match de coupe du 28/10 = 16,4 fautes par match pour notre côté (22 dans le match réel) ; moyenne v3/v4 presque égale (−0,1), ~17 en amical | Dev vachacz, #general | 2026-10-28 17:54 | confirmé (mesure du Dev) ; trois joueurs criaient au « trop de fautes » sur 1 à 3 matchs |
| Fautes selon le BMI : pivot au BMI élevé 3,5 fautes en amical soft contre 1,8 pour un pivot au BMI plus bas | montabelas, #italia | 2026-10-27 | avis (un seul joueur) |
| Le malus du Q4 s'applique dès la 1re seconde du Q4 à tout joueur qui joue 4 quarts ; 3 quarts (36 min) sans pénalité. En coupe : arodrigues84 ne voit pas le malus, jorgeac25 pense qu'il reste | elemke. (GM), #help ; arodrigues84, jorgeac25 | 2026-10-30 09:49 | confirmé (skill) ; coupe en doute, L-026 : Q4 −4 au-delà de 36 min en coupe |
| Le focus défensif a décidé deux matchs de coupe (Vans, Penafiel) selon les joueurs | #italia, #portugal | 2026-10 | avis |
| Changer le poste nominal d'un joueur ne change que le PS affiché (51 → 52), pas le jeu ; seniors seulement | #general | 2026-10 | confirmé (cohérent M§4) |
| Le +/- ne permet pas de juger un intérieur : il porte sur le cinq entier | #italia | 2026-10 | avis |
| La zone n'était pas à l'écran en saison 2 avant l'activation par vachacz le 27/10 | #italia | 2026-10-27 | confirmé (cohérent News 2026-10-27) |

### Calendrier / coupes
| Fait | Source | Date | Statut |
|---|---|---|---|
| Un blessé de la dernière journée de ligue ne joue pas la coupe | karolina.munde, inkamint, #lietuva | 2026-10-27/28 | confirmé (News 2026-10-23) |
| Coupe tour 1 du 28/10 : NT cup partie sur le réglage d'amical (jorgeac25) | #general | 2026-10-28 | en doute (voir ligne « à rouvrir » plus haut) |

### Académie
| Fait | Source | Date | Statut |
|---|---|---|---|
| Les juniors non tirés ne vieillissent pas à la saison 2 : « not implemented… next season » ; un junior tiré 3 jours avant le changement de saison est passé de 16 à 17 ans | vachacz #general 2026-10-27 06:07 ; elemke. #academy ; baldurazz0 #italia ; isr_shay | 2026-10-27 | confirmé (Dev) : attendre le jeudi ne coûte pas d'âge ; sondage sur le calendrier d'âge envisagé (28/10 21:46) |
| La taille augmente de 1 à 4 cm au changement de saison | #general | 2026-10 | confirmé (cohérent M§5.2) |
| Jauges des autres clubs : 75 à 100 %, tirages à 69 % et 63 % ; un « 120 % » cité (markoivica, 29/10) | #academy | 2026-10-29 | avis ; le « 120 % » est à vérifier (au-delà du maximum) |
| Premiers tirages de la saison 2 (29/10) décevants : heldermoreno ~550-600 k dépensés en 4 semaines sans junior utile ; nhegas12 aucun 3 étoiles malgré 100 k par semaine | #portugal | 2026-10-29 | avis |
| Les tests à 25 000 sont confirmés ; un pot 10 monte de +2,2 en compétence principale | #italia | 2026-10 | confirmé (skill) |
| 71 000 contre 100 000 : aucune mention dans ce lot | — | — | en doute (inchangé) |

### Transferts / prix
| Fait | Source | Date | Statut |
|---|---|---|---|
| Un bon 16 ans se paie 3 à 4 M fin octobre : enchère poussée à 4 M (dixi2499, 29/10), PF 16 ans TS 48 parti sous 4 M (montabelas, 30/10), 16 ans pot 8 à 1,3 M le 14/10, 17 ans à 2-3 M « facile » (27/10) ; « passé 7,5 M » sans nom (nathanr_32176, 31/10) | #italia, #portugal | 2026-10-14 … 2026-10-31 | avis ; à comparer à `gold.bv_market_price_known` (max 2 894 063 au 22/10) |
| Les 2 étoiles sont bon marché depuis que n'importe quel acheteur peut tester le potentiel à 25 000 | #italia | 2026-10 | avis |
| Taxe de revente dégressive (semaine 2 à 20 %, puis 15 %… jusqu'à 5 %) : non décidée | vachacz, #economy | 2026-10-22 15:57 | en doute (déjà noté) |

### Finances / sponsor
| Fait | Source | Date | Statut |
|---|---|---|---|
| La page sponsor a un outil « Season scenario » qui simule le gain de chaque contrat | grillanza_60069, #italia | 2026-10-27 13:44 | confirmé (écran du jeu) |
| « Top half » = les 6 premiers ; le titre de champion rapporte seulement 80 000 de plus que le podium ; le choix est définitif avant le début de saison | joueurs, #economy / #italia | 2026-10-27 | avis (palier non confirmé par le Dev) |
| Le montant affiché inclut-il les primes de fin de saison ? .doman dit oui, grillanza_60069 dit non : ne pas compter ces primes comme de la liquidité | #economy | 2026-10-27 | en doute |
| Contrats cités : « 50 k par semaine + 30 k par victoire » (foo_13) ; svarog_ « Top 3 » ; lolek5232 « Top 6 » (écart avec le titre : 200 k) | #economy, #italia | 2026-10-27/29 | avis |
| L'économie gonfle et il faudra « probablement réagir » ; le Dev refuse d'ajouter de l'argent et rejette les infrastructures lourdes (24/10) | vachacz, #economy | 2026-10-24, 2026-10-29/30 | complété (risque : mesures de limitation d'ici la fin de saison) |

### Entraînement
| Fait | Source | Date | Statut |
|---|---|---|---|
| « ×0,5 après 90 » (sans source) | grillanza_60069 | 2026-10 | confirmé : notre skill donne ×0,50 à 90 [M§8.4] |
| Fatigue < 20 avec endurance ≥ 50 pour toute l'équipe qui gagne la coupe | axolimpiamilano | 2026-10 | avis v3 ; la v4 donne −4 % à 20 |

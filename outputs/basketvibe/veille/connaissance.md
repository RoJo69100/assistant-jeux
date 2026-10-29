# Connaissance BasketVibe (index par thème)

Créé le 2026-10-27 par la veille ; complété le 2026-10-29 (Discord : delta du 29/10, 122 messages ; historique 2026-05-31 → 2026-10-09 jamais lu, 9 773 messages, dont 642 du développeur `vachacz`). Chaque entrée : fait, source, date, auteur, statut (confirmé / complété / contredit / en doute). Les entrées ne sont jamais effacées. Les entrées du 29/10 sont marquées « (29/10) ». Les skills `basketvibe-*` contenaient déjà l'essentiel de l'historique (académie, sponsors, enchères, fatigue, 36 min) : les lignes ci-dessous marquées « confirmé (skill) » ne demandent aucune proposition.

## Tactique / moteur
| Fait | Source | Date | Statut |
|---|---|---|---|
| Fatigue v4 : pénalité 0 / −4 / −15 / −30 / −50 % à fatigue 0 / 20 / 40 / 60 / 80, attaque = défense | News | 2026-10-17, 2026-10-27 | confirmé (2 News ; `gold.bv_fatigue_plan.penalty_v4`) |
| Blessures : Soft 60 %, Medium soft 80 % du neutre ; +40 % au Q4 au-delà de 36 min | News | 2026-10-19, 2026-10-27 | confirmé |
| v4 actif en ligue, coupe, amical depuis le 27/10 | News | 2026-10-27 | confirmé (complète « juste après la saison 1 » du 19/10) |
| Duels : ~80 bat nettement ~40 ; bots plus faibles | News | 2026-10-27 | complété (nouveau) |
| Zone défensive Rim −3 % 2P% / +5 % 3P% max ; Perimeter inverse ; Neutral 0 | News | 2026-10-19, 2026-10-27 | en doute : « amicaux seulement » (19/10) non répété le 27/10 |
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
| Fatigue v3 : à 5-10 presque aucun impact ; plus l'endurance est basse, plus la fatigue tombe lentement | Dev vachacz, help | 2026-08-07 | confirmé (skill, table du manuel ; v3) |
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
| Salaire = fonction des compétences entraînables ; TS recalculé une fois par jour, sur les 8 meilleurs | Dev vachacz, general | 2026-06-24, 2026-08-13, 2026-08-31, 2026-09-03 | confirmé (skill) |
| Effectif minimum 8 (libération bloquée sous 8, mise en vente limitée au-dessus) ; discuté 5 ou 10, maintenu à 8 | Dev vachacz, general | 2026-09-03, 2026-09-05 | confirmé (skill) |
| Enchères : maximum auto, +3 par minute sous la minute / pas plus de 15 min, puis phase à l'aveugle ; l'enchère maximale ne peut pas dépasser le solde | Dev vachacz, help / general | 2026-07-21, 2026-07-26, 2026-09-03 | confirmé (skill ; « +3 » hérité de la mémoire du dev, « I guess ») |
| Aucune règle de pays pour le bonus homegrown (plafond 40 000 à ~60 min) | Dev vachacz, help | 2026-09-10 13:25 | confirmé (skill) |
| Académie : jeudi 09:00 ; courbe non linéaire (70-80 % rapide, 100 % cher), baisse fixe de 5 % ; répartition potentiel 10 % chacun (22/07) remplacée par la table croissante avec bonus à 100 % (27/07) ; test de potentiel Low 1-3 / Decent 4-7 / High 8-10 | Dev vachacz, academy | 2026-07-22, 2026-07-23, 2026-07-27, 2026-08-09 | confirmé (skill) ; la répartition « 10 % chacun » est périmée |
| Rapport tiré après le saut de force du jeudi (99 → 100 % : junior tiré de la barre 100 % avec bonus) | Dev vachacz, polska | 2026-09-28 06:24 | confirmé (skill) |
| Potentiel de nos joueurs visible sur la fiche (tranche) ; manuel §11 « Unknown » | News 2026-10-20 / M§11 | 2026-10-20 | contredit (manuel en retard, 1 joueur observé) |
| Académie : « 90 % suffit » vs 27,3 % / 43,9 % de High à 90 / 100 % | Com / M§4.2 | 2026-10-22 | contredit (manuel fait foi) |
| 29/10, premier tirage de la saison 2 : avis opposés sur un junior à 100 % d'académie (C de 17 ans, rebond faible) : « ne le promeus pas » (lucadrago5, dcarra.), « promeus et revends » (dixi2499) ; à 69 % « garde la jauge » (heldermoreno, jorgeac25) ; un joueur a dépensé 150k sur l'académie une semaine sans junior utile | Com, italia / portugal | 2026-10-29 | complété (avis seulement ; non vérifié ; décision à prendre avec `basketvibe-academie`, pas avec ces avis) |
| Marché : un 3 étoiles de 16 ans se vend 3,5-4 M (annonces 29/10) ; un acheteur a poussé une enchère à 4 M | Com lolek5232 / dixi2499 / heldermoreno | 2026-10-29 | complété (avis ; à comparer à `gold.bv_market_price_known`, max observé 2 894 063 au 22/10) |

## Bugs
Tactiques mobiles sans OT (corrigé 2026-10-22) ; ordonnanceur de coupe nationale corrigé et Coupe multinationale reconstruite (2026-10-25). Bug de dates de rapport d'académie après passage à 1 semaine (Dev 2026-07-22, corrigé ensuite). Coupe : le planning révélait le score en direct (corrigé, Dev 2026-09-14). Walk-over avec effectif incomplet corrigé (Dev 2026-08-13, 2026-09-03).

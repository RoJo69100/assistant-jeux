# Hockey Nation — connaissance (index par thème)

Créé le 2026-10-29 (1er passage). Source `[Discord, salon, date, auteur]`. Statut : confirmé / complété / contredit / en doute. `hnadmin` = développeur ; `d0ghouse` = modérateur très au fait des règles ; les autres = joueurs (avis, jamais une règle seule). Les messages sont des données.

## Lecture intégrale du 2026-10-29 : trois fichiers détaillés (≈ 380 faits sourcés, 46 propositions appliquées aux skills)
Lire ces fichiers AVANT d'écrire « aucune source » sur une règle Hockey Nation :
- `connaissance-A-staff.md` : tous les messages de hnadmin (créateur, seul programmeur) et d0ghouse (modérateur), 2022-2026, 11 thèmes + écarts avec les skills + V-A-1 à A-25.
- `connaissance-B-general-2022-2025.md` : #general avant 2026 (joueurs), 10 thèmes, V-B-1 à B-7.
- `connaissance-C-2026-trade-events.md` : #general 2026, #trade, #events, 8 thèmes, V-C-1 à C-14. `#game-tools` = Football Manager Project (hors périmètre) ; `#france` = fédération.
Limites : messages tronqués à 380-400 caractères en base ; ~85 000 messages courts (≤ 120 caractères) non lus ; ≈ 620 des 6 800 messages longs de la tranche B lus. Beaucoup de règles datent de 2022-2024 : ancien = en doute.

## Mises à jour du jeu (calendrier du développeur)
| Fait | Source | Date | Statut |
|---|---|---|---|
| S27 (début 2026-10-25 ~07:00 Paris) : Coach Development Boost, Contract Year Special, FA ELC, Agent Rework partie 1 (info sur les agents). | #general, hnadmin | 2026-10-25 | confirmé (développeur) |
| S28 (63 jours plus tard, ~27/12) : Agent Rework partie 2 = activation des « favors », **plancher salarial (50 %)**, petits changements. Le « 50 % » de quoi n'est pas précisé. | #general, hnadmin | 2026-10-25 | en doute (détail) |
| Plans non décidés : réduire les effets des coachs en match (réglage « None / Low / Normal » dans le plan de jeu, ou curseur), coach draft pool, vote de la trade board à 66 % pour les clubs de moins de 5 saisons. | #general hnadmin 2026-08-25 ; #trade hnadmin 2026-08-27 | 2026-08 | en doute (idées) |

## Joueurs / talents / postes
| Fait | Source | Date | Statut |
|---|---|---|---|
| Patineurs : SHO et PAS = buts ; SKA et PWR = avoir le palet ; CHK et DEF = défendre ; DSC = pénalités prises ; FOF : un bon joueur de mise au jeu par ligne suffit, pas forcément le centre. | #general, talonflame1 | 2026-04-04 | complété (avis de joueur) |
| Notre hypothèse [H] « C = SHO PAS SKA FOF ; ailiers = SHO PAS SKA ; D = DEF CHK SKA » : compatible, mais PWR (avec SKA) manque pour tous et FOF n'est pas lié au centre. | idem | 2026-04-04 | complété |
| Gardiens : END = nombre de matchs avant fatigue, titulaire 7+ ; STK = la moins utilisée ; à END bas il ne reste ~60 % de condition en 3e période. | #general, talonflame1 | 2026-04-04 | confirmé (STK, END) |
| Endurance : L1 7+, L2 6+, D1 8+, D2 6+. | idem | 2026-04-04 | confirmé (déjà dans le résumé) |
| La perte de condition pèse relativement plus sur les hautes compétences ; un bon gardien a besoin d'un % d'arrêts plus haut pour un dSV positif. | #general, d0ghouse | 2025-12-03 | complété |
| Tout joueur peut jouer 25-30 min quel que soit END (« moteur simple »). Le temps de glace max des défenseurs a été réduit (nerf, date non précisée). | #general, d0ghouse | 2026-05-11 ; 2026-08-24 | en doute (portée) |
| Perte de condition : un joueur à 10/10/10 en SHO/PAS/DEF finirait à ~12 % de condition (plaisanterie). | #trade, krusher_kev | 2026-10-26 | en doute (avis) |
| Un joueur peut devenir « Elite » à 29 ans (Dujic RW, Duda) : l'expérience monte aussi par les matchs internationaux. | #events, jakkysosa / shackleton1892 | 2026-10-13 | complété (avis) |

## Coachs
| Fait | Source | Date | Statut |
|---|---|---|---|
| « Coach rating » d'équipe = score calculé des compétences de match des coachs ; la note affichée du coach (OVR) n'est pas ce score. Cas : remplacement par un intérimaire 43 -> rating 57 -> 61. | #general, hnadmin | 2026-10-29 11:49 | confirmé (développeur) |
| Les compétences du head coach comptent toujours double (« No change » après S27). | #general, gordie_79 | 2026-10-25 07:41 | confirmé (joueur) |
| Un coach à Puck Battling 80+ : investir dans des joueurs aux bonnes compétences physiques ; les notes de coach renforcent un style de jeu, elles ne comblent pas des faiblesses. | #general, d0ghouse | 2026-08-24 20:04 | complété |
| Coachs actuels : Coach Development Boost depuis S27 (contenu exact non publié). Têtes d'équipe et assistants prennent leur retraite (trunkxolotl, elitesteel). | #general, hnadmin 2026-10-25 ; trunkxolotl 2026-10-27 | 2026-10 | confirmé (retraite), en doute (boost) |
| Joueurs anciens qui postulent comme scouts (Tomi Liukkonen, Ha-ru To) à l'ouverture de S27. | #general, avakael / gordie_79 | 2026-10-25 | complété (scouts) |

## Entraînement
| Fait | Source | Date | Statut |
|---|---|---|---|
| Les amicaux ne donnent pas d'expérience ; ils servent à tester tactiques et lignes. | #general, krusher_kev ; d0ghouse | 2026-10-05 | confirmé |
| Dans un amical, la pénalité de mauvais poste s'applique ; seule la pénalité de plafond est désactivée (et elle ne frappe que le joueur au mauvais poste). | #general, d0ghouse | 2026-10-28 11:06 / 12:59 | complété |
| Un gardien jeune peu expérimenté souffre en playoffs : l'alterner tous les 3-4 matchs pour lui donner de l'expérience. | #general, krusher_kev | 2026-10-14 | complété (avis) |

## Draft / scouting
| Fait | Source | Date | Statut |
|---|---|---|---|
| Sans cible principale, la sim suit le classement pré-draft du GM, combiné aux besoins de poste réglés. | #general, d0ghouse | 2026-10-24 10:46 | complété |
| Les équipes sans propriétaire (inactives) draftent aussi ; un draftee sur une équipe sans GM peut être libéré (retiré) sauf conditions de « pending free agency » (saison entière + assez de matchs). | #events/#general, hnadmin | 2026-10-24 ; 2026-04-20 | complété |
| Avis : les deuxièmes tours produisent des 70+ si on scoute (trunkxolotl : s16, 70+ au 2e tour dans chaque ligue, 80+ dans deux) ; c0ntrail : choisir par build, pas par note ; tour tardif = min 64 possible. | #general, trunkxolotl / c0ntrail | 2026-10-17 à 10-27 | complété (avis) |
| U17 : chaque saison 7 jeunes de 15 ans arrivent ; vous choisissez un joueur, les 6 autres reçoivent un poste pour qu'aucun poste ne manque (ex. gardien manquant -> gardien). 5 draftables dans 3 saisons, 2 non draftables rejoignent U21. | #general, hnadmin | 2026-09-19 | complété |

## Contrats / plafond / rachats / agents
| Fait | Source | Date | Statut |
|---|---|---|---|
| FA ELC (S27) : agents libres de 24 ans ou moins et « ovr max 69 » ; 1re saison 3-way, 2 autres 2-way ; 3 ans (21 ans : 3y 3-way possible). | #general, gordie_79 | 2026-10-25 14:49/14:51 | contredit/en doute : « ovr max 69 » (potentiel max ?) contre notre « noté 69 ou moins » |
| Un FA ELC déplacé en Farm/U21 ne compterait pas dans le plafond (réponse « Yes » d'un joueur, pas du développeur). | #general, gordie_79 | 2026-10-25 07:41 | en doute |
| Contract Year Special : actif quand il reste 1 an au contrat actif, même si le joueur est prolongé tôt. Tous les joueurs en dernière année ne l'ont pas. | #general, hnadmin | 2026-10-22 04:29 ; 2026-10-21 11:01 | confirmé (développeur) |
| Rachat : le reste du salaire de la saison est effacé, le futur est remplacé par un salaire de rachat ; le coût baisse si on attend. Plafond libéré immédiatement à l'action. | #general, hnadmin | 2025-07-02 ; 2026-07-22 | complété (écart avec « moitié du restant » : le coût varie avec l'attente) |
| Échange : l'allègement du plafond et les pénalités s'appliquent à l'approbation du trade, pas à la fin du traitement. | #general, hnadmin | 2026-03-12 | complété |
| Agents : réponse instantanée au début d'une négociation, humeur remise à « happy » après un échange, réponse garantie à la dernière mise à jour de la saison. | #general, hnadmin | 2026-04-22 ; 2026-06-17 | confirmé |
| ELC de 24 ans impossible après la fenêtre I. | #general, d0ghouse | 2026-10-03 10:38 | confirmé |
| Repères de marché Frenzy S27 : Raymond Baker (LD/RD) 4 ans 9 050 000 $ (Odesa) ; Borer (min 81) demande 5,5 M x 5 ; les agents libres signés pendant la Frenzy sortent de la recherche avant l'annonce. | #events, .coleh / seany148 ; #general, seany148 | 2026-10-27 | complété (marché) |
| Valeur d'échange selon la note minimale : 80+ = 1er tour ; 70-79 = 1er ; 60-70 = 2e ; 60-64 = 3e ; 55-60 = 4e ; < 55 = 5e. Cap dump : < 1 M = 4e ; 1-2 M = 3e ; 2-4,5 M = 2e ; 4,5-7 M = 2e+3e ; 7-10 M = 1er. | #general, talonflame1 | 2026-04-14 | complété (avis, jamais une règle) |

## Matchs / lignes / plan de jeu
| Fait | Source | Date | Statut |
|---|---|---|---|
| Lignes modifiables tout de suite, mais **au moins 1 h avant le match** sinon risque de −30 % aux compétences. | #general, hnadmin | 2025-07-10 | confirmé (skill dit « 1 h avant » sans le −30 %) |
| Capitaine : leadership + expérience, limité à 3 joueurs (C + 2 A) ; plus d'expérience est mieux. | #general, d0ghouse | 2026-08-24 | confirmé |
| Gameplan : tout autre réglage que « ultra defensive » peut mal tourner pour certaines équipes (avis). | #general, heymelo27 | 2026-05-21 | en doute (avis) |
| Avis : les gardiens très cotés comptent moins ; formation de gardiens en ELC. | #trade, heymelo27 | 2026-04-20 | en doute |

## Échanges
| Fait | Source | Date | Statut |
|---|---|---|---|
| Marché S27 : beaucoup de U21 en surplus (krusher_kev ~35, jakkysosa 30/30 en FRM), demande surtout U21 C/RW/LD, RD de premier rang et gardiens U21 ; peu de preneurs de cap dumps (seany148 en prend). | #trade | 2026-10-24 à 10-29 | complété |
| Les choix de 1er tour futurs sont traités à égalité par la trade board (pas de classement prévisible). | #general, heymelo27 | 2026-10-16 16:00 | confirmé (usage de la trade board) |

## Bugs / pannes
| Fait | Source | Date | Statut |
|---|---|---|---|
| Serveur redémarré le 2026-10-21 (mises à jour PHP) ; processeur de matchs HS 2 h le 2026-01-10 ; trades « on hold » libérés trop tôt (2025-10-02, corrigé). | #general, hnadmin | divers | confirmé, sans impact |

# Lecture joueurs/GMs BasketVibe — partie 3 (`export discord basketvibe.txt`, 16 225 lignes) + part1 (133 lignes)

Veille, lecture intégrale message par message, créée le 2026-10-31. Format : canaux Community/academy, economy, engine, general, help (lignes 1-3855), release-notes, general (suite), help, reset, pays (portugal, polska, pilipinas, lietuva, italia, españa), release-notes, help. Dev = `vachacz`. Un avis n'est jamais une règle. Statuts vs `outputs/basketvibe/veille/connaissance.md` : nouveau / confirme / complète / contredit / en doute. Les skills et connaissance.md ne sont pas modifiés.

Légende : « Dev » = vachacz ; « avis » = joueur/GM sans preuve chiffrée.

## Passage 1 — lignes 1 à 2940 (academy, economy, engine, general jusqu'au 30/08, début help)

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Pénalité 48 min : « maintenant 12,5 % », prochaine itération à 15 % en v3 (v2 gelé). Le dev précise : un joueur 48 min peut rester plus fort et le hasard peut l'aider, donc 100 % de victoire au Q4 non garanti | Dev, engine | 2026-09-12 10:36-10:38 | confirme (connaissance : 8→10→12,5→20 %) ; la valeur 15 % annoncée n'a pas été suivie d'une mention directe (le 20 % du 13/09 est dans connaissance) |
| Propositions de joueurs de pénalités graduées : 1 joueur à 48 min −20 %, 2 → −25 %, 3 → −30 %, 4 → −35 %, 5 → −40 % (grobarbrate) ; pénalité qui double la 2e semaine si ≥ 4 joueurs > 36 min de moyenne (lordgohan_67459) ; −50 % (faraone85_69754) ; −10/15 % + fatigue doublée > 40 min (grillanza_60069) | grobarbrate, lordgohan_67459, faraone85_69754, grillanza_60069, engine | 2026-09-12 | avis (non appliqué ; v4 retient les paliers de fatigue) |
| Écart de Q4 face à une équipe à 48 min « encore petit » malgré la hausse (graphique du dev, pièce jointe non lue) | Dev, engine | 2026-09-11 17:47 | confirme (v3 pré-20 %) |
| Fatigue moindre à focus défensif bas : un joueur à 54 d'endurance avec 156 min de ligue + 108 min d'amical (montabelas) a la même fatigue qu'un adverse à 228 min ligue + 476 min amical ; le dev répond « peut-être le focus défensif bas qui génère moins de fatigue » ; « soft def pour s'offrir un match de défense agressive » | montabelas, Dev, engine | 2026-09-19 18:45-19:04 | confirme (skill : agressivité/focus et fatigue) ; l'effet du focus bas sur la fatigue est « peut-être », pas chiffré |
| Avis : l'impact des amicaux sur la fatigue vaut ~10 % de celui des matchs de ligue | jorgeac25, engine | 2026-09-19 18:55 | avis (« je crois ») ; compatible avec connaissance (10 % fatigue amicaux, juin) |
| Cotes du moteur avant match : grobarbrate 14-1, première fois sans tactique ni matchup (minutes seulement, joueurs moins fatigués), battu 128 pts reçus par une équipe 48 min ; le dev : 68 % de chances de victoire (94, 86, 63, 82 % avant) ; « transparence plus importante » | grobarbrate, Dev, general | 2026-08-24 23:47-23:55 | confirme (cotes dev) ; l'argument « les tactiques comptent » est un avis (échantillon de 1) |
| Défense agressive en pré-v4 : 8 joueurs à 24 min en Agressive + 2 sans, défaite de 20+ contre un adversaire à 2 joueurs 48 min, « pas à cause des fautes » ; autre essai : 2 joueurs 12 min en Agressive, les 2 blessés ; lolek5232 : Agressive a failli perdre contre un bot à 50 de fatigue ; svarog_ : fautes et lancers francs « partout » avec Agressive | grobarbrate, lolek5232, svarog_, general | 2026-08-19, 2026-08-28, 2026-08-29 | confirme (agressivité = fautes/blessures, v4) ; avis pour l'efficacité (anecdotes) |
| Le dev annonce répondre « avec des probabilités % plus tard » sur le risque de blessure en Agressive (jamais vu dans ce passage) | Dev, general | 2026-08-19 14:59 | en doute (promesse non suivie dans le fil ; chiffres v4 = News 19/10) |
| Fin de quart : des équipes ne tirent pas la dernière possession (13 s restantes), rushrat : aucune action sur les 29 dernières secondes d'un match ; le dev rouvre le ticket | grobarbrate, rushrat, Dev, engine | 2026-09-05 11:06-16:52 | confirme (corrigé en v5, annonce du 28/10 « tirs de fin de quart ») |
| Pas d'and-1, pas de fautes tactiques, dernière LF ratée = changement de possession sans rebond, des pertes de balle non comptées dans les stats | rene779, engine | 2026-09-06 00:08 | confirme (v3 : LF manquées et fautes tactiques corrigées 08-09/09, connaissance) ; and-1 : non annoncé, en doute |
| Cup/coupe : preset d'amical pris par défaut dans les matchs de coupe (bug admis par le dev « my bad ») | svarog_, Dev, engine | 2026-09-18 22:08-22:25 | confirme (skill communaute l.126 : corrigé, preset coupe depuis Dev 2026-09-19) ; absent de connaissance.md |
| Idées d'équipe : défense 3-2/2-3/homme, « driving frequency », option « clutch » (joueur 1 et 2 pour le dernier tir) proposée par grobarbrate | grobarbrate, Dev, engine | 2026-09-11 | confirme (connaissance : Defense area, 3-2/2-3 refusés) ; clutch = avis, non retenu |
| Le dev : la formule de PS « indicative », le moteur lit les compétences possession par possession ; PS simple, n'écrase pas les écarts de compétences | Dev, engine / general | 2026-09-17 16:15, 2026-08-16 23:12 | confirme |
| Rebonds : 2-3 joueurs prennent 80-90 % ; le dev : sur la liste courte pour v3, d'abord en amical | glorious_monkey_80768, Dev, engine | 2026-09-07 15:42-16:39 | confirme (connaissance 24/08 « rebonds redistribués ») |

### Joueurs / fatigue / forme / blessures
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Blessures : le dev répond « base probabilities not changed » (28/08) ; les kinés réduisent les probabilités ; un médecin embauché après blessure ne raccourcit pas une blessure « jusqu'à demain » (le dev : « doit être recalculé à l'embauche ») | Dev, lolek5232, grobarbrate, general | 2026-08-23, 2026-08-28 | confirme (kinés/médecins connaissance) ; recalcul à l'embauche : en doute (cas d'1 jour restant non concluant) |
| Plusieurs GMs signalent « trop de blessures » (7 matchs par semaine, repos manuel quotidien) ; random_player_123 : une saison entière sans jamais dépasser 15 de fatigue = 1 blessure (+1 en Agressive) ; propose revoir la chance de blessure à fatigue basse et un paramètre « minutes > 36 » | faraone85_69754, praedyn (6 blessures en 6 matchs), zhuchok25, random_player_123., general | 2026-08-23 12:54-15:19, 2026-08-29 09:23 | avis (cohérent avec « fatigue basse = blessure possible », v4 prévoit +40 % Q4 > 36 min) |
| Repos manuel appliqué par le dev quotidiennement pendant les 7 matchs par semaine, une fois en double par erreur (24/08) | Dev, general | 2026-08-19, 2026-08-24, 2026-08-29 | confirme (connaissance : V-20261030-6) |
| Entraînement : un +2 en un seul entraînement = potentiel « au-dessus de la moyenne », peut être 6, pas forcément 10 ; un +3 = pot 10 « à 100 % » ; il faut 4-5 entraînements pour estimer ; 8 entraînements par saison, 9 montées sur la compétence principale à 16-18 ans | dcarra., random_player_123., general | 2026-08-16 10:34-10:53 | avis ; à comparer au skill `basketvibe-entrainement` (gains par potentiel) — plausible mais non confirmé par le dev |
| Un joueur n'a pas besoin de jouer pour s'entraîner ; potentiel caché 1 à 10 | praedyn, general | 2026-08-26 13:43 | confirme |
| Les 16-18 ans : potentiel 9, âge 27 ans = pas de gain après recalibrage (dcarra.) | dcarra., general | 2026-08-16 11:36 | confirme (âge) |
| Meilleurs joueurs du jeu au 16/08 : TS max 555, deux joueurs de 20 ans à 550 ; top 10 = joueurs de 20 ans ; PS des meilleurs GM : 61-65 | Dev, grobarbrate, svarog_, random_player_123., general | 2026-08-16 | complète (historique, avant reset) |
| Le dev : « homegrown = joueur tiré de l'académie » (icône maison) | Dev, general | 2026-08-29 11:24 | confirme |

### Entraînement / potentiel
(Voir « Joueurs » ci-dessus pour les mesures d'entraînement ; aucune mesure de gain hebdomadaire chiffrée dans ce passage.)

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| 3 étoiles « High potential » = potentiel 8-10 | Dev, academy | 2026-09-06 12:35 | confirme (skill) |
| La taille des moins de 18 ans augmente (dev : oui) ; grillanza_60069 : +4 cm entre 16 et 22 ans (5 saisons, max +20 cm) | Dev, grillanza_60069, academy | 2026-09-04 18:11-18:16 | confirme (taille) ; +4 cm / +20 cm : avis |
| Meilleurs PS d'un junior tiré : 54 (17 ans), 52 à 16 ans avec académie à 92 %, 48, 41 (anecdotes) | hamsterj1312, ale92c, esmosinag, ori1919, academy | 2026-09-13 | complète (ordre de grandeur : PS d'un junior tiré 41-54 ; skill académie donne les fourchettes) |
| Tests : 25 000 « n'est rien, on les récupère en 1,5 amical » ; grobarbrate : 75k une semaine sans rien trouver, puis un High au premier essai la semaine suivante ; carlomtlopes_69000 : pareil | .doman, grobarbrate, carlomtlopes_69000, academy | 2026-09-10 13:30-14:19 | avis (cohérent avec 27,3 %/43,9 % de High) |
| « 100 % saute lentement après cette semaine » (le gain de jauge ralentit) : .doman | .doman, academy | 2026-09-10 13:30 | avis (compatible avec la courbe non linéaire du dev) |
| Fin de saison à 85 % d'académie : des GMs conseillent de ne pas tirer un C de ~18 ans (« 47-50 TS » estimé) et d'attendre le premier tirage de saison à ~100 % ; montabelas promeut ensuite « la bête » (09/10) | giovannidziadzia, .doman, montabelas, academy | 2026-10-08 20:11-20:25, 2026-10-09 13:51 | avis (stratégie ; pas une règle) ; compatible avec l'avis du 29/10 de connaissance |
| Aucun joueur de petit gabarit tiré : « toujours C et PF » ; réponse dcarra. : aléatoire | .doman, dcarra., academy | 2026-10-07 11:16 | en doute (nos données montrent des PG/SG/SF aussi, V-20261030-5) |
| Le rapport tombe chaque jeudi | dcarra., grobarbrate, grillanza_60069, academy | 2026-09-08, 2026-09-09, 2026-09-25 | confirme |
| Investissement académie au maximum : « tu reçois trois fois ça avec un seul match à domicile » | elemke., academy | 2026-09-24 15:13 | confirme (100 000/sem. vs 250-300k par match à domicile, Dev 05/09) |
| Un joueur de 3 étoiles de 16 ans à tirer ou pas : conseil dominant « prendre le plus jeune » (D'Angelo 16 ans) ; « 3 étoiles seulement » ; 2 étoiles peuvent avoir de bonnes compétences | elemke., kotryk, marekb9231, academy | 2026-09-17, 2026-09-18, 2026-09-24 | avis |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Tops du marché à 2,5 M (21/08) ; zamfir acheté 2,6 M en enchère (19/08) ; acheteur aaaoooaaaa sur un achat à ~3 M qui se blesse deux quarts après (rarz09, 28/08 : « 3 millions pour rien ») | Dev, s6o7537, rarz09, general / economy | 2026-08-19, 2026-08-21, 2026-08-28 | complète (historique pré-reset ; prix max observés 2,5-3 M) |
| Idée : 5 % de taxe prélevée même si le joueur n'est pas vendu (5 % du prix de départ + 5 % du prix final, minimum 10 k) | .doman, economy | 2026-08-22 12:13 | avis (non retenu) |
| Autres joueurs de l'académie non retenus refusés sur le marché (le dev : l'offre de juniors serait trop forte) ; agents libres fournissent des juniors | lordgohan_67459, Dev, economy | 2026-08-21 14:23-14:30 | complète (règle de conception) |

### Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Économie avant/après : 7 amicaux + pas d'académie ≈ 5 M par saison (avant), 3,1 M (après) ; amicaux seuls 1,8 M → ≈ 1 M ; académie max 100k + 2 tests médicaux moyens : 2 M ; sans amicaux, 100k académie + 2 tests = 1 M | Dev, economy | 2026-08-19 18:27 | confirme (connaissance : −30 %, 100k) |
| Plan dev 27/08 : homegrown bonus, personnel (psychologues, marketing), sponsors par type ; plus tard salaires non linéaires, sponsors selon dureté de division, arène, fanclub ; coach staff « demande recalibrer l'entraînement » (28/08) | Dev, economy / general | 2026-08-27 19:50, 2026-08-28 19:56 | confirme (connaissance : personnel) ; coachs : en doute (jamais livrés) |
| Staff = arbitrage voulu : « on peut tout embaucher et rester positif, mais court sur les transferts » ; si l'économie est étroite, le dev ajoutera des recettes de billetterie | Dev, general | 2026-08-28 19:56-20:00 | complète |
| Sponsors octobre : version 1 (draft) avec un contrat « champion » 2 M versé à la fin (rien en cours de saison), « top moitié » 25k/sem. + reste en fin de saison pour atteindre 1,1 M (déduction de chanceler) ; le dev retire le tout-ou-rien, rapproche les montants, pas de changement en cours de saison, premier choix en S2, tous en « Stability » d'ici là | chanceler, Dev, economy | 2026-10-02 17:55-23:48 | confirme (connaissance : 6 contrats, Stability) ; chiffres du draft = en doute (la version finale est une capture non lisible) |
| Écart de 400k entre l'option max et l'option « lazy » jugé « stupide » vu 300k+ par match à domicile ; le dev « livre comme prévu » | marekb9231, Dev, economy | 2026-10-02 23:24 | complète (sponsor max vs min ~400k) — à rapprocher du sponsor Fluxora observé (640k garanti + 15k/victoire) |
| Salaires hebdomadaires : proposition de passer à des salaires saisonniers (jeunes à fort potentiel doublent de salaire en cours de saison) | .doman, economy | 2026-10-08 08:05 | avis |

### Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Coupe pilote : manche 1 jouée le 04/09 ; notifications de coupe affichées comme amicaux ; pas de « reveal result » ; dev corrige | Dev, grobarbrate, academy | 2026-09-04 18:20-18:36 | confirme (connaissance : bug notifications, 04/09) |
| Coupe : 5 manches cumulables en milieu de saison ; un tournoi de 512 équipes = 9 manches, 2 matchs par semaine envisagés ; équipe nationale non prioritaire | Dev, grobarbrate, lolek5232, general | 2026-08-27 | complète (historique, périmé) |
| Fatigue des coupes/NT : avis « pas de fatigue en NT et BV Cup » (grobarbrate, aaaoooaaaa) ; « un peu de fatigue comme en amical, avec XP entre amical et ligue » (rene779) ; Charazay : 0,025 XP/match en ligue, amical 1/3 (0,0083), LdC 0,033, sélections 0,05 × minutes | grobarbrate, rene779, lucadrago5, general | 2026-08-20, 2026-08-21 | avis (News 23/10 : coupes sans fatigue ni expérience ; confirme le sens de l'avis, contredit rene779) |
| Académie 99 % et popularité 99 le 27/08 chez grobarbrate | grobarbrate, general | 2026-08-27 12:45 | complète (historique) |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Lineup/tactiques de ligue et d'amical confondus (blackdead6468) ; fil ouvert par le dev | blackdead6468, Dev, help | 2026-08-22 03:59 | complète (connaissance : tactiques séparées 27/09) |
| Fin de quart sans tir et possession mal gérée (voir Tactique) ; fatigue/repos en double (24/08) ; coupe en preset d'amical (18/09) | divers | 2026-08-24, 2026-09-18 | confirme (skill) ; absents de connaissance.md « Bugs » : coupe preset d'amical, repos double 24/08 |

## Passage 2 — lignes 2940 à 9710 (help 08-10/2026, release-notes 06-08/2026, general 05-08/2026)
Constat de méthode : `basketvibe-communaute` (skill) contient déjà presque tout ce passage (préréglage à re-sélectionner, médecins après blessure, décimales, agents libres 3-9, 200-205 cm). Ces lignes sont donc « confirme (skill) » ; elles manquent seulement dans connaissance.md.

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Si on modifie un preset, il faut le re-sélectionner sur chaque match déjà planifié, sinon l'ancienne version est utilisée | grobarbrate / vortexraijin, help | 2026-09-05 02:28-02:49 | confirme (skill communaute l.61) ; non dans connaissance.md ; à vérifier encore vrai en v4 (le 05/08 le dev avait livré « override par match sans changer le preset ») |
| Tactiques non sauvegardables après la vente d'un joueur présent dans le preset (« quarts non remplis ») ; contournement : éditer le preset ; correctif déployé le 19/09 18:20 | tankre1792, heldermoreno, Dev, help | 2026-09-18 12:48, 2026-09-19 17:57-18:26 | nouveau (bug) ; pertinent à chaque vente : après une vente, rouvrir le preset avant de planifier |
| Aucune pénalité de rôle sauf la taille et le rebond (PG loin du panier : pénalité aux rebonds, idem pour tous les postes) | praedyn, Dev, help | 2026-09-09 19:40-19:52 | confirme (connaissance : matchup, skill) |
| Entre 200 et 205 cm en PG la baisse est linéaire (tableau : 100 % à 200 cm, 95 % à 205 cm) | Dev, help | 2026-09-10 17:40 | confirme (skill communaute l.41) |
| Le moteur v2 donne plus de poids à la taille pour les rebonds ; règle de proximité du panier ; le dev refuse de dire si le rebond d'un meneur compense (« très proche de donner la formule ») | Dev, general | 2026-07-13 17:50-17:58 | confirme ; l'effet exact du rebond hors C/PF reste inconnu |
| Dérivé du manuel par un joueur : au-dessus de 2 m +1,8 % par cm sur le rebond, en dessous l'inverse (80 à 190 cm = 66 ; 210 cm = 94) | lucadrago5, general | 2026-07-13 19:29 | avis (calcul d'un joueur, non confirmé par le dev) |
| Un 210 cm PF au poste de PG tire 6-11 à 3P face à une défense 70+ : le joueur juge le bonus de taille « supérieur à 8 % » ; pénalité de 48 min alors ~8 % | lolek5232, grobarbrate, Dev, general | 2026-07-28 11:34-12:52 | avis (v2, périmé par la hausse 10 → 20 %) |
| 3P% jugé trop haut (40-60 % à 30-40 tirs) par txetx (v2) ; plafond des tirs à 3P 70 → 50 % le 24/08 | txetx, general ; release-notes | 2026-07-28 11:46 | confirme (connaissance : plafond 3P 24/08) |
| Simulation de 1 000 matchs : 29 % de victoires pour l'équipe réclamante, 7 % des matchs > 150 pts ; ajustement du dev vers des scores plus étroits | Dev, general | 2026-07-24 16:21 | confirme (connaissance : 123,6-133,0 pts) |
| Tireur à 3P (SG < 190 cm) prenant très peu de tirs à 3P malgré « full 3P » : soupçon d'effet de la taille sur l'emplacement | svarog_, general | 2026-08-01 21:02, 2026-08-02 09:50 | avis ; renvoyé à #engine, pas de réponse du dev dans le passage |
| Le dev ne divulgue pas la formule de rebond ; « dans tous les jeux les joueurs devinent seuls » | Dev, general | 2026-07-13 17:58 | confirme (connaissance : ne divulgue pas les formules) |

### Joueurs / fatigue / forme / blessures / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Forme : variation aléatoire ±1 par semaine, les psychologues décalent les chances ; elle s'applique à tous les matchs (ligue, coupe, amical) | Dev, help | 2026-09-11 07:26 | confirme (skill) |
| Médecins : embauchés après la blessure, effet sur les jours restants seulement ; blessure déjà « jusqu'à demain » non réduisible | Dev, lordgohan_67459, help | 2026-09-14 04:38-07:20, 2026-08-28 | confirme (skill communaute l.101) |
| Personnel : on paie la somme maximale de salaire atteinte pendant la semaine (embaucher puis libérer et ré-embaucher le même poste ne double pas) | Dev, help | 2026-09-03 18:44 | complète (skill communaute l.101 : « facturation = maximum de la semaine ») |
| Compétences stockées avec décimales ; juniors et effectifs de départ sans décimales (donc la première hausse d'un junior est lisible) | Dev, general / help | 2026-08-02 10:50, 2026-09-13 09:57 | confirme (skill l.65) |
| Expérience : croissance linéaire mais impact non linéaire (les 10 premiers points comptent plus que 80-90) ; le dev promet une table dans le manuel | Dev, general | 2026-08-02 12:19 | complète (à vérifier dans skill joueurs ; impact décroissant = utile pour juger 10 → 15 d'expérience) |
| Joueurs libres : potentiel aléatoire de 3 à 9 | Dev, help | 2026-09-07 20:44 | confirme (skill communaute l.121) |
| Taille : les moins de 21 ans peuvent grandir (manuel erroné) ; +4 cm de 16 à 22 ans, max +20 cm (estimation d'un joueur) | Dev, help ; grillanza_60069, academy | 2026-09-13 09:57, 2026-09-04 | confirme ; chiffres en cm : avis |
| Pas de limite d'effectif ; solde négatif = interdiction de marché, puis éventuellement personnel et académie | Dev, help | 2026-09-12 18:56-19:03 | confirme (skill l.105) ; complète : l'extension aux restrictions personnel/académie est une intention |
| Remplaçants quotidiens du dev (repos) pendant les 7 matchs par semaine : « j'applique le repos manuellement chaque jour » | Dev, general | 2026-08-29 15:03 | confirme (connaissance : V-20261030-6) |
| Un joueur de retour de blessure n'a pas joué un match de coupe (soupçon de fuseau horaire, GM d'Australie) | b.tothe.r, Dev, help | 2026-10-04 22:50 | en doute (bug à signaler, réponse du dev : enquête) ; à surveiller après une blessure qui expire le jour d'un match |
| Stamina jugée « OP » en v1 (20 d'endurance = 77 de fatigue en 20 min) | dcarra., general | 2026-06-29 06:35 | périmé (fatigue v4) |

### Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| On peut entraîner jusqu'à 99, plus cher, aucun autre plafond | Dev, help | 2026-09-08 07:26 | confirme (connaissance) |
| Un joueur s'entraîne une fois par semaine quelle que soit son temps de jeu | Dev, help | 2026-09-21 19:19 | confirme |
| 3 étoiles de 16 ans : 18 à 24 compétences gagnées par saison selon le potentiel | Dev, help | 2026-09-24 23:33 | confirme (cohérent avec connaissance : pot 6, 9 compétences à 25 ans ; skill §8.3) |
| Pot 10 = +2 par semaine sur la compétence principale (lecture de joueur) ; un +2/+1 dès le premier entraînement d'un junior = pot 10 « si c'est le premier » | pijonghoo, nathanr_32176, help | 2026-09-13 12:36-14:28 | avis ; compatible avec skill (junior sans décimales) mais nul n'a de contre-épreuve sur pot 9 |
| 8 entraînements possibles par saison pour un junior tiré en semaine 1 ; académie le jeudi 9h laisse 2 jours avant l'entraînement du samedi | lolek5232, Dev, general | 2026-08-06 13:34-14:13 | contredit en partie : le dev parle de « Saturday's training » (06/08, avant reset) ; un GM dit « Sunday » (02/09) ; la base (skill saison l.21) observe dimanche 02:00 UTC = 04:00 Paris : le « samedi » du 06/08 est périmé, jeudi 9h → dimanche = 3 jours pour tirer |
| Petit « camp d'entraînement » hors saison pour les juniors (+1 sur six compétences observé) | Dev, general | 2026-07-21 13:47 | en doute (antérieur à la réforme du 10/08) |

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Le potentiel des juniors est égal pour tous les pays | Dev, help | 2026-09-08 13:05 | nouveau (mineur) |
| Rapport d'éclaireur : chaque jeudi (page affichant « next scout on … ») | grillanza_60069, dcarra., help | 2026-09-08 09:27 | confirme |
| Tirer fait baisser la jauge de moitié : 3 semaines pour revenir à 75 % après un tirage à 75 % ; coût d'une montée de 1,2 M à ne pas gaspiller | dcarra., general | 2026-07-29 15:52, 16:08 | confirme (−50 %, skill) |
| Avis (pré-calibration) : « un High dans presque chaque lot de trois » : txetx le 31/07 ; calibrage final du dev le 30/07 | txetx, general | 2026-07-31 09:02 | périmé (calibrage du 30/07, 27,3 %/43,9 % de High à 90/100 %) |
| La première mise à jour de jauge : les rapports déjà tirés ne sont pas révélés pour ceux qui ont déjà payé le test ; « pas de cas spéciaux » (Dev) | grobarbrate, Dev, general | 2026-07-30 22:28-22:30 | complète (règle de conception) |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Enchères maximales : le total des enchères maximales où l'on mène compte comme argent engagé et plafonne le solde ; après un dépassement par un autre, la somme est rendue ; l'écran Économie affiche l'argent engagé en enchères actives | Dev, dcarra., grobarbrate, general | 2026-07-26 12:47-13:33 | complète (connaissance : « maximale ≤ solde » ; ajout : somme de toutes les enchères actives, pas seulement une) |
| Notification seulement quand notre enchère maximale est dépassée (système auto-bid) | grobarbrate, dcarra., general | 2026-07-18 14:07 | confirme |
| Marché : durée 4 jours → 2 jours (25/07) ; 1,7 M de transfert le plus cher du 20/07 (Van Der Berg, Willems 21 ans PG >1,5 M) ; premier joueur à > 1 M le 16/07 | Dev, dcarra., grobarbrate, general | 2026-07-16, 2026-07-20, 2026-07-25 | complète (historique avant reset) |
| Joueurs libres : le dev refuse de les améliorer (« supprimer ou générer des juniors ») | Dev, general | 2026-07-27 19:21 | confirme |

### Finances / sponsor
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Sponsor fixe 100 000 par semaine (05/09) ; match à domicile de ligue 250 000 à 400 000 selon la popularité ; le dev pourrait ajouter 50k aux sponsors ou aux amicaux si l'économie est trop basse | Dev, help | 2026-09-05 09:43-13:35 | confirme (connaissance) |
| Amical : ~17 000 par match, 119 000 pour 7 amicaux par semaine (joueur) ; bonus homegrown 40 000 par semaine pour 200 minutes jouées | lolek5232, help | 2026-09-05 12:19 | complète (avis chiffré ; compatible avec la règle 200/min, plafond 40 000) |
| Masse salariale de départ ≈ 296 382 par semaine (effectif non transformé) contre sponsor 100k + amical extérieur 17k + 2 « manager journey » 25k | spapjh, help | 2026-09-08 17:24-17:28 | complète (ordre de grandeur de la masse salariale initiale) |
| Salaire hebdomadaire de ~240-250k après reset (calcul GM) | random_player_123., help | 2026-09-05 15:24 | complète |
| Récompense de fin de saison : 200 000 pour la victoire de ligue, à revoir ; popularité remise à 70 ; sponsors par DH | Dev, help | 2026-09-27 12:48, 2026-09-28 16:22 | confirme (connaissance) |
| Pas d'agrandissement de stade ni de sièges (« pas encore ») | Dev, help | 2026-09-29 07:31 | confirme (skill) |
| Défaite d'amical : pas d'effet sur la popularité | grobarbrate, help | 2026-10-03 09:26 | confirme (release 2026-06-29 : « popularity unchanged ») |

### Calendrier / classement
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Départage h2h, changement récent | Dev, help | 2026-10-03 20:59 | confirme |
| Best Five de journée : algorithme antérieur au PER, à aligner (idée du dev) | Dev, help | 2026-09-11 21:57 | complète (connaissance : EVAL remplace PER 28/09) |
| Un entraînement : « Sunday » | grobarbrate, help | 2026-09-02 21:51 | confirme (notre routine) ; voir entrée « samedi » ci-dessus |
| Walk-over : 20-0 si 4 joueurs ou moins ; minimum 8 joueurs (idée de cimi) | lolek5232, cimi, general | 2026-08-13 21:27-21:34 | confirme (connaissance : 20-0, minimum 8) |
| Niveau de fatigue des coupes : avis « pas de fatigue » (aaaoooaaaa, grobarbrate) ou « comme un amical » (rene779) | general | 2026-08-20 | avis, tranché depuis par la News 23/10 |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Tactique d'un match : « quelque chose de bizarre » avec une équipe 48 min contre une équipe 48 min (capture) ; le dev : pas global, ticket demandé | szulim90, Dev, help | 2026-08-29 20:18-20:27 | en doute (aucun suivi) |
| Mobile : durée de blessure non visible (03/08) ; remplaçant affiché à la place d'un blessé dans le onze de départ du play-by-play (23/07) | svarog_, lolek5232, general | 2026-07-23, 2026-08-03 | confirme (corrigé : play-by-play affiche le remplacement, News 11/10) |
| Chrome ne charge pas la page de connexion (Edge OK) ; fuseau et page d'accueil | wintersb_, help | 2026-09-26 06:07-13:51 | complète (sans effet décision) |

## Passage 3 — lignes 9740 à 16 225 + part1 (help/reset 2026, pays pt/pl/ph/lt/it/es, release-notes 08-10/2026, help doublon) et `discord_BasketVibe_part1.txt` (133 lignes, 29/10)
Doublons constatés : le canal reset est exporté 3 fois (10376-11358), le canal help 2 fois (2835-3850 et 15202-16217), general 15/08-16/08 recopié (9551-9704) ; lus intégralement quand même.

### Tactique / moteur
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Focus défensif 1 (« laisser seul ») sur le pivot adverse : il a mis 48 points ; « je ne le ferai plus » | tankre1792, italia | 2026-09-09 22:15-22:24 | avis (anecdote chiffrée, 1 match) ; cohérent avec la description du focus 1 dans le skill tactique |
| Un défenseur sur-déchargé (focus bas sur un joueur qui n'avait pas joué) a coûté une défaite de championnat | grillanza_60069, italia | 2026-09-13 09:58 | avis |
| Focus défensifs « très importants, ils peuvent faire la différence sur un seul joueur » | dcarra., italia | 2026-09-05 10:44 | avis (compatible avec Dev 09/08 : impact du focus relevé) |
| Agressivité : moyenne en ligue/coupe, minimale en amical (grillanza_60069) ; « trop agressif en défense ne paie pas, rester sur moyen » (tankre1792) | grillanza_60069, tankre1792, italia | 2026-09-22 07:06, 10:51 | confirme (skill communaute l.59) |
| Contre une équipe 5×48 min : Q4 gagné de 20 points après la hausse à 20 % (faraone85_69754, 15/09) ; autre match Q4 22-20 seulement (16/09, adversaire en fatigue jaune) | faraone85_69754, italia | 2026-09-15 13:58, 2026-09-16 23:04 | confirme (la pénalité de 20 % ne garantit pas le Q4) |
| Contre une équipe 40 min en fatigue ~40 : 60 % à 3P concédés, défaite avec tous à 20 min ; le dev annonçait 70 % de chances de victoire | uthred9751, italia | 2026-09-21 20:29-22:52 | avis ; illustre l'aléa du moteur v2/v3 |
| Un pivot réglé « tout 2P/passe » tire 5 trois-points sans en marquer ; tireur à 3P réglé « full 3P » : 4/26 sur 5 matchs | cobisixer, faraone85_69754, españa/italia | 2026-09-14 20:01, 2026-09-05 10:42 | avis (plafond 3P à 50 % des tirs depuis le 24/08, levé le 16/09 pour les meilleurs tireurs) |
| Rebond : 3 joueurs à ≥ 60 raflent presque tout ; ordre d'importance C → PF → SF ; un C à 28 de contrôle de balle ne souffre pas, un joueur au contrôle plus bas fait plus de pertes (différence « visible » mais pas drastique) | jopencjusz, marekb9231, polska | 2026-09-13 23:41-23:56 | avis (observations d'un GM, ordre de grandeur) |
| SF à tirs 53/56, contrôle 38, athlétisme 75 : meilleur scoreur ; SG à tirs 72/73, contrôle 44, athlétisme 61 : moins bon | .doman, polska | 2026-09-16 10:54 | avis (1 cas) ; athlétisme important |
| Un C n'a pas besoin de gros 2P : taille + athlétisme + rebond suffisent à marquer | carlomtlopes_69000, portugal | 2026-09-14 22:31-22:32 | avis |
| Aucun malus de poste, seulement taille/physique (citation du manuel §6.2.1) ; label de poste = étiquette | carlomtlopes_69000, portugal | 2026-09-14 21:37-21:43 | confirme (skill) |
| Opposants : fourchettes de compétences visibles dans la section focus défensif de la tactique du match | Dev, release-notes | 2026-09-06 11:44 | complète (utile pour fixer les focus) |
| La tactique se verrouille 15 minutes avant le match ; l'engine remplit les trous si un joueur est vendu/libéré (29/08) | Dev, release-notes | 2026-09-11 20:12, 2026-08-29 21:13 | confirme (connaissance) ; mais bug de sauvegarde réapparu les 18-19/09 (voir passage 2) |
| Joueurs fatigués : « 10-20 de fatigue n'est pas un gros problème » ; 68 d'endurance ≈ 30 minutes ; le dev précise que la fatigue basse tombe lentement (« the lower it is the slower it falls ») | Dev, help | 2026-08-07 10:40-11:02 | en doute pour v4 (v4 : −4 % à 20) ; l'entrée connaissance « plus l'endurance est basse, plus la fatigue tombe lentement » pourrait lire « fatigue » : ambiguïté du « it » |

### Joueurs / forme / fatigue / expérience
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Forme : ±1 au hasard, plus de chances de revenir vers les valeurs centrales (7 → −1 plus probable) ; elle compte « pas tant que ça, sauf à 1-2 » ; jouer ne l'améliore pas | grillanza_60069, dcarra., faraone85_69754, italia | 2026-09-16 11:56-13:22 | confirme (Dev 20/07, 11/09) ; « pas tant sauf à 1-2 » : avis, à comparer au tableau du manuel |
| Expérience : jusqu'à ~+10 % d'efficacité maximum (manuel) | grillanza_60069, italia | 2026-09-17 12:46 | confirme (skill entrainement l.16) |
| Fatigue d'un amical ≈ 10 % de celle de ligue à minutes et agressivité égales (§1.2 du manuel) | carlomtlopes_69000, portugal | 2026-09-12 19:55 | confirme |
| Pas d'effet des tests sur la jauge d'académie : seule l'embauche la baisse | carlomtlopes_69000, portugal | 2026-09-12 19:49 | confirme (skill) |

### Entraînement / potentiel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Entraînement ralenti à partir de 70, puis « drastiquement » à partir de 80 (0,63 du rythme < 70) | kotryk, marekb9231, polska | 2026-10-06 19:45-19:48 | confirme (skill entrainement l.54 : ×0,63) |
| Débat de stratégie : monter le rebond d'un C à 80 d'emblée (doman) ou d'abord athlétisme/tirs (marekb9231) | .doman, marekb9231, kotryk, polska | 2026-10-06 → 2026-10-08 | avis (hypothèses, aucune mesure) |
| Premier entraînement d'un junior tiré : +2 sur la principale et +1 sur la secondaire => « pot 10 » (pijonghoo, vortexraijin, nathanr_32176) ; 3 points au total la première semaine => « sûrement pot 10 » | pijonghoo, vortexraijin, pilipinas / help | 2026-09-13, 2026-09-24 | avis, plausible avec départ sans décimales (Dev 13/09) ; pas de contre-épreuve |
| Un junior de 17 ans tiré qui monte 2 fois en principale + 1 fois en secondaire en 2 semaines = « jackpot » ; une 2e compétence qui monte = potentiel moyen-élevé ; un joueur de 22 ans +1 deux semaines de suite | carlomtlopes_69000, nhegas12, heldermoreno, portugal | 2026-09-13 16:30, 2026-09-14 14:42-19:40 | avis |
| 3 étoiles de 16 ans : à 207 cm à 18 ans si +4 cm par saison | kotryk, polska | 2026-09-29 21:07 | avis (estimation) |

### Académie
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Investir 71 000 ferait gagner la même jauge que 100 000 ; chanceler : « seul le \"agora\" change », plafond variable avec la force actuelle | nhegas12, chanceler, portugal | 2026-09-13 18:00-18:48 | en doute (2 captures non lues, skill communaute l.95 « non vérifié ») ; tester sur `silver.bv_academy_weekly` : gain possible de 29 000 par semaine |
| Le rapport est tiré après le saut de force du jeudi ; l'argent dépensé après la sortie du rapport ne change pas les 3 candidats | Dev, polska | 2026-09-28 10:24 | confirme (connaissance 28/09, skill académie) |
| Max PS à académie 100 % ≈ 55 (il faut 3 étoiles) ; deux 16 ans à PS 49 et 50 sur le marché sont « super chanceux » | tankre1792, dcarra., italia | 2026-09-03 18:44-18:48 | avis (ordre de grandeur) ; compatible avec 54 (17 ans) observé |
| 3 étoiles de 17 ans moins bon qu'un 16 ans 3 étoiles : « il faut une bombe pour compenser » ; attendre un 16 ans | carlomtlopes_69000, portugal | 2026-09-13 07:42, 16:24 | avis (compatible skill académie) |
| Premier tirage de saison = 1 à n entraînements de plus | dollarius_80489, italia | 2026-10-29 12:08 | confirme connaissance.md |
| 4 semaines sans junior utile à 69-82 % d'académie, 150k d'investissement cette semaine, 550-600k dépensés ; « j'aurais plus de 1 M en cash » ; potentiel 3 = minorité (« la grande majorité devrait être potentiel 2 ») | heldermoreno, portugal (part1) | 2026-10-29 10:28-11:01 | complète (coût réel d'un cycle d'académie sans résultat) ; avis sur 2/3 étoiles |
| 29/10 : un joueur a testé 25 000 sur un junior : 2 étoiles ; jauge 69 % ; plusieurs GMs conseillent « ne promouvez pas » à 100 % | jorgeac25, arodrigues84, montabelas, portugal (part1) | 2026-10-29 10:08-10:30 | confirme connaissance.md |

### Transferts / prix
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Prix des 16 ans en septembre : PS 40 vendu 150 000 en semaine 1 (S1), 300 000 le 11/09 ; PS 42 : 350 000 → 500 000 ; « les prix ont à peu près doublé » ; 800 000 offerts pour un top rookie, vendu > 1 M | mkeffe, grillanza_60069, italia | 2026-09-11 11:12-11:20, 10:44 | nouveau (série de prix 16 ans S1) ; à comparer à `gold.bv_market_price_known` |
| « Maintenant les prix de tous les 16 ans : bon moment pour vendre, même la ferraille part à prix déraisonnables » | smoothie_53551, lietuva | 2026-09-22 13:33 | avis |
| Prix demandés pour un pot 8-9 SG : 2 M-3 M (annonce) ; un High en vente à 1 M avec offre à 1,2 M ; offre 150 000 jugée provocation | vortexraijin, jonabe2972, delinaaaaaaa, pilipinas | 2026-09-24 05:20-05:44 | avis (prix demandés, non conclus) |
| 29/10 : C 3 étoiles de 16 ans estimé 3,5-4 M, offre à 1,8 M refusée ; « 4 M presque certain dès la première semaine » ; enchère montée à 4 M | grobarbrate, lolek5232, heldermoreno, dixi2499, ex-yugo/portugal/italia (part1) | 2026-10-29 11:11-12:39 | confirme connaissance.md (3,5-4 M) |
| Stratégie « acheter à 10 000 et revendre quand il y aura plus d'argent » (plus-values) ; 600k de départ + 17k × 5 = 685k de recettes de la première semaine, masse salariale 342k, académie 100k | _stefax, italia | 2026-09-02 11:02-11:03 | avis (S1) |
| Recettes de la première semaine : 3 matchs à domicile sur 4 = presque 800 k contre ~300 k pour 3 matchs à l'extérieur : 500 k d'écart | dcarra., mkeffe, italia | 2026-09-11 10:32-10:39 | confirme (250-400 k par domicile, Dev 05/09) |

### Finances / sponsor / personnel
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Un seul match de ligue à domicile paie toutes les factures de la semaine (académie à 50 000) ; il reste beaucoup ; il peut monter à 100 000 sans problème | chanceler, portugal | 2026-09-13 16:46 | avis ; cohérent avec 250-400 k par domicile |
| Médecins/kinés : seulement si blessures ; marketing utile pour les équipes qui attendent des défaites | carlomtlopes_69000, chanceler, portugal | 2026-09-12 19:35-19:37 | avis |
| 29/10 : cash de 750 k avec ~1 M épuisé en académie ; décision « sans réfléchir » critiquée par l'intéressé | heldermoreno, portugal (part1) | 2026-10-29 10:29 | avis (cas concret de coût d'opportunité) |

### Calendrier / coupes / amicaux
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Coupe de septembre : 25 % de fatigue et d'expérience | dcarra., italia | 2026-09-12 13:33 | confirme (skill communaute l.125, périmé par News 23/10) |
| Amical programmé par erreur un jour de ligue : fatigue ~10 % d'un match | chanceler, carlomtlopes_69000, portugal | 2026-09-12 19:53-19:55 | confirme |
| Amicaux « inutiles » : la plupart des adversaires jouent 48 minutes | _stefax, italia | 2026-09-08 19:16 | avis (lié au test de composition de notre amical quotidien) |
| Hors saison / amical : bonne source de caisse et d'expérience | faraone85_69754, italia | 2026-09-09 08:14 | avis |
| Sélection : 60 personnes regardent les matchs en direct (le dev, 29/09) | Dev, release-notes | 2026-09-29 22:35 | complète (sans effet sur la décision) |

### Bugs
| Fait | Auteur, canal | Date | Statut |
|---|---|---|---|
| Notification de résultat visible pendant un match en direct (bêta du direct le 12/09) ; corrigé 13-14/09 | chanceler, Dev, portugal / release-notes | 2026-09-12 20:21, 2026-09-13 15:27 | confirme (connaissance : bug planning, corrigé) |
| Tir de mi-terrain à 67 % (capture) et 4 tirs de loin pour 1 réussi en 8 minutes | svarog_, chanceler, general / portugal | 2026-08-01, 2026-09-12 | avis (v2/v3, pas de réponse du dev) |
| Le préréglage de coupe n'existait pas avant le 19/09 ; sauvegarde de tactique après transfert cassée (corrigée 19/09 puis 21/09 « retest requis ») | Dev, release-notes | 2026-09-19 21:21, 2026-09-21 22:02 | confirme (connaissance : 19-21/09) |

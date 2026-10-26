---
name: sixzeroleague-match
description: Règles Six Zero League (handball) du jeu et du moteur de match — terrain, 7 joueurs (gardien + 6), 2 × 30 min, zones de tir (9 m, 6 m, 7 m), exclusions de 2 min, cartons et suspensions, jeu passif, ce qui décide d'une action, avantage du terrain ; compétitions (ligues de 10, 5 divisions, points, départages, montée/descente, coupe, primes, forfaits). À charger pour analyser un match, préparer une composition ou toute question de calendrier et de classement.
---

# Six Zero League — jeu, match, compétitions

Sources : **[W:Rubrique]** = wiki officiel du jeu, lu en entier le 2026-10-18 (copie dans `bronze.raw_pages`, `game = 'sixzeroleague'`, `page_type = 'app_wiki'`, client 0.1.2). Le wiki affirme : « si une règle n'est pas écrite ici, elle n'est pas appliquée » [W:Introduction]. Pas de Discord exporté pour ce jeu. Jeu en **alpha** [W:Competitions].

## Le jeu [W:The game]
- Terrain 40 × 20 m ; but 3 × 2 m ; zone des 6 m (réservée au gardien) ; ligne de jet franc à 9 m ; jet de 7 m.
- 7 par équipe : gardien + 6 (2 ailiers, 2 arrières, demi-centre, pivot). Effectif de match : 10 [W:Introduction].
- 2 mi-temps de 30 min, horloge continue (~1 h réelle).
- Zone des 6 m appliquée strictement : un attaquant qui y entre avec le ballon le perd (renvoi du gardien). On peut tirer en suspension au-dessus de la zone.
- Faute → jet franc à 9 m (horloge arrêtée). Fautes techniques : marcher (la plus fréquente), passage en force (seulement avec un défenseur en face), reprise de dribble (rare).
- **Jeu passif** : après ~35 s d'attaque placée sans tir, avertissement ; puis 6 passes pour tirer, sinon ballon à l'adversaire. Un tir cadré remet le compteur à zéro, un tir contré non.
- **Jet de 7 m** : accordé quand une occasion nette est stoppée illégalement ; la meilleure occasion du jeu.
- Simplifications : pas d'arbitre (toute faute détectée est sifflée, pas d'avantage), pas de hors-jeu, **remplacements automatiques** (on choisit le cinq avant le match, pas pendant).

## Le match [W:Match]
- **Les 7 titulaires de chaque match = la composition par défaut sauvegardée** (Équipe → Tactique). Pas de composition par match : elle sert jusqu'à ce qu'on la change.
- Tirs de 3 distances : 9 m, 6 m, 7 m. Plus le tir est proche, plus il a de chances d'entrer.
- Chaque passe, tir, arrêt et interception est un tirage de probabilités selon les joueurs impliqués. Deux bons joueurs face à face s'annulent ; les écarts comptent quand un côté est nettement plus fort. **Petit avantage à domicile.**
- **Exclusion de 2 min** : beaucoup plus fréquente sur une faute qui donne un 7 m que sur une faute ordinaire. Jeu à un de moins, sans remplaçant. Jusqu'à 3 exclus en même temps. L'équipe en supériorité numérique arrive **beaucoup plus facilement aux 6 m**.
- **Cartons** : jaune = avertissement, un par joueur, 3 par équipe, seulement dans les 15 premières minutes. Rouge = 3e exclusion d'un joueur, ou très rarement direct. Rouge : 2 min à un de moins, puis un remplaçant entre (s'il en reste).
- **Suspension** : un rouge direct = suspendu pour le match suivant du club (ligue ou coupe) ; un rouge pour 3 exclusions, non. Une suspension non purgée en fin de saison est reportée au 1er match de la suivante.
- ⚠️ Le devlog 0.5.7 dit : un rouge « avec rapport de l'arbitre » = 2 journées de ligue de suspension [Dev chat, devlog 2026-10-04]. Le wiki (lu le 2026-10-18) dit : rouge direct = 1 match. **Tranché le 2026-10-23 [Obs utilisateur] :** le rouge direct de Roger (J9, 15:26) affiche **1 match** de suspension à l'écran, donc le wiki l'emporte (le « rapport de l'arbitre » du devlog est un autre cas). Blessure d'A. Bertin (J9) : **2 matchs**. Un joueur suspendu d'1 match rate le match suivant et revient au suivant.
- À l'écran, un même joueur ne peut pas être titulaire/remplaçant à deux postes : le doublon de remplaçant est impossible [Obs utilisateur 2026-10-23] ; un poste de remplaçant peut rester vide.
- Match visible en direct (Compétitions ou bouton Live) ; rapport de fin de match : buteurs, joueur du match de chaque côté, statistiques complètes.

## Compétitions [W:Competitions]
| Élément | Règle |
|---|---|
| Ligue | 10 clubs, matchs aller et retour (18 journées) ; ligue incomplète complétée par des bots |
| Divisions | 5 ; on entre en 5e division. Placement par un admin au début de saison ; inscription en cours de saison = on reprend la place d'un bot en 5e division |
| Points | Victoire 2, nul 1, défaite 0 |
| Départage | Points → différence de buts → confrontations directes → buts marqués → buts encaissés → club |
| Montée / descente | Le champion de chaque ligue monte ; les **3 derniers descendent**. Pas de montée depuis la 1re, pas de descente depuis la 5e. Les bots montent et descendent aussi |
| Multiplicateur de revenus par division | 5e ×1,0 · 4e ×1,3 · 3e ×1,6 · 2e ×2,0 · 1re ×2,5 (billets, sponsor, arena, boutique, primes ; coûts et entretien des infrastructures aussi ; **pas** les salaires ni la formation de rôle) |
| Primes de ligue (5e division) | Champion 15 000 €, 2e 8 000 €, 3e 4 000 € (× multiplicateur), clubs humains seulement, versées à la dernière journée |
| Coupe | Pour les clubs humains (au moins 2) ; élimination directe, terrain neutre, recette partagée, pas d'avantage du terrain. Tableau tiré en début de saison ; les mieux classés (divisions hautes d'abord) sont exemptés des premiers tours. Un tour de coupe se joue entre les deux journées de ligue d'une « semaine ». Égalité après 60 min → 2 × 5 min de prolongation → 7 m (5 tireurs différents, puis mort subite) ⚠️ En pratique, la prolongation s'est terminée au « but en or » le 2026-10-20 ; le développeur parle d'une erreur et a ajouté les tirs au but, quasi inatteignables à cause de la mort subite [Dev chat, chat jeu 2026-10-20 16:19 à 16:38]. Chaque tour de coupe paie une part de la recette et compte pour le développement des joueurs [Dev chat, devlog 0.6.0 2026-10-16]. |
| Prime de coupe | 10 000 € en 5e division (× multiplicateur de la division du vainqueur) |
| Trophées | Champion de ligue et vainqueur de coupe seulement |
| Forfait | Moins de 7 joueurs aptes → défaite 15–0 (0–0 et défaite pour les deux si les deux sont courts). En coupe : qualification de celui qui peut jouer, sinon du mieux classé au tirage |
| Fin de saison | Après la dernière journée, un admin clôture puis lance la saison suivante (montées, descentes, nouvelles ligues) |

## Le rythme du jeu [W:Finances, Training, Transfers]
**Tout se règle toutes les 2 journées de ligue terminées** (la « semaine » du jeu) : finances, entraînement, blessures, transferts. Ce cycle ne tourne que pendant une saison de ligue en cours.
- En pratique : **2 journées par jour** (12:00 et 20:00, heure de Lisbonne), donc une « semaine » par jour, réglée après le match du soir ; **saison de 9 à 11 jours, +1 an pour les joueurs à chaque saison** [Dev chat, voir sixzeroleague-communaute].

## [Obs] Nos données
- Le 2026-10-18 au soir : « Round 1 dans 15 h 45 », saison remise à zéro le jour même (dit l'utilisateur). Aucun match encore joué.
- API JSON : `/api/seasons/current`, `/api/seasons/current/my-competition`, `/api/leagues/<id>`, `/api/cups/current` (pages Overview et Competitions).

## [Veille 2026-10-26] Mises à jour (V-20261026-1, -3, -5)
- **0.6.1 « Tactical Depth » (2026-10-24)** : formation d'attaque **5-1 ou 4-2** ; formation de défense **6-0, 5-1, 3-2-1 ou 3-3** ; direction d'attaque ; agressivité **Light / Normal / Hard** ; **ordres de match** (jusqu'à 3 changements tactiques à une minute et un score choisis) ; **rapport tactique** (avantages et inconvénients de chaque choix, vérifiés contre nos joueurs) ; **scouting** : les tactiques des deux équipes figurent dans les stats et le rapport de match, la carte « prochain match » montre ce que l'adversaire a joué la dernière fois. Les formations sont équilibrées entre elles ; le 4-2 est une vraie alternative au 5-1. [Dev chat, devlog Discord 2026-10-24 13:26, D:L9 ; V-20261026-9, remplace V-20261026-1]
- **Contres** (écart « léger ») : l'attaque **5-1 est la meilleure contre une défense 6-0** ; le **4-2 fonctionne très bien contre le 3-3**, moins contre le 3-2-1, le 5-1 puis le 6-0 (dans cet ordre), mais contre quand même le 3-2-1 et le 5-1. Par défaut, joueurs et bots sont en 5-1 / 6-0 (les bots peuvent adapter leur tactique à leurs forces). **« Il vaut mieux jouer selon les forces de son équipe que contrer l'adversaire »** ; entre deux équipes égales, le contre peut décider. En 4-2 : LB, RB et **deux P**, pas de CB (l'écran affiche à tort « CB et P » ; la simulation compte les deux pivots) ; direction « left+centre » / « right+centre » = l'arrière de ce côté + les pivots, **« mixed » donne la même chose**. [Dev chat, Gazelle, Discord #chat 2026-10-24 18:14-18:33, D:L325-328 ; V-20261026-10]
- Un ailier ne peut pas défendre à l extérieur sans la pénalité de hors-poste ; règle annoncée comme transitoire, Gazelle cherche une solution [Dev chat, 2026-10-25 15:56 UTC ; V-20261026-3].
- Remplacements sur ordre : **pas encore** (réponse du développeur, sous le pseudo « Urban Fox » = Gazelle, à « no subs on orders? »). Les **ordres de match** de la 0.6.1 concernent des changements **tactiques** (3 au plus, à une minute et un score). [Dev chat, Gazelle alias Urban Fox, C:4f8014 / C:98bde4 2026-10-25 21:21-21:25 ; D:L9 ; V-20261026-12, corrige V-20261026-5]
- **0.6.1, jeu passif et exclusions** : après l'avertissement de jeu passif, **4 passes** (6 avant) et la passe qui prend un coup franc ne compte pas ; **moins d'exclusions de 2 min**, plus en rafale, données **seulement à un défenseur en contact** avec l'attaquant ; l'équipe en supériorité l'exploite mieux ; défenseurs qui marquent mieux les pivots (même contre deux) ; attaquants plus loin des défenses qui pressent ; **chance de blessure à l'entraînement divisée par deux**. **Rupture de série** : les stats d'exclusions, de fautes et de jeu passif d'avant le 2026-10-24 13:37 UTC ne se comparent pas à celles d'après. [Dev chat, D:L9 ; V-20261026-15]
- **Coupe (0.6.1)** : la prolongation est **toujours jouée en entier, sans but en or** ; seul un score encore égal après elle mène aux tirs au but ; les rapports de coupe indiquent la décision après prolongation ou aux tirs au but. **Seul le 1er prend le prix de la coupe.** Résout le ⚠️ du 2026-10-20/23 de la ligne Coupe ci-dessus (but en or : périmé). [Dev chat, D:L9 ; D:L318-319 2026-10-24 15:23 ; V-20261026-16]

---
name: sixzeroleague-entrainement
description: Règles Six Zero League (handball) de l'entraînement et de la relève — cycle toutes les 2 journées, intensité d'équipe (Light, Normal, High) et risque de blessure, focus par joueur (groupe ou compétence), effet de l'âge (bonus jusqu'à 20 ans, nul à 25, baisse dès 28, déclin physique dès 30), éthique de travail, formation à un 2e rôle, académie U18 (nouveau choix toutes les 8 journées, niveau, scouting). À charger pour régler l'entraînement, projeter un joueur ou choisir un prospect.
---

# Six Zero League — entraînement et académie U18

Sources : **[W:Rubrique]** = wiki officiel, lu le 2026-10-18 (voir sixzeroleague-match).

## Fonctionnement [W:Training]
- **Une semaine d'entraînement = 2 journées de ligue terminées** (même cycle que les finances et les transferts). Tourne seul ; ne tourne que pendant une saison de ligue.
- **Intensité d'équipe** (tout l'effectif) : Light · Normal · High. Plus haut = progrès plus rapides, mais **plus de blessures à l'entraînement et blessures plus longues** (en High : ~3 matchs d'absence, parfois 6 [W:Injuries]). « Un club qui s'entraîne dur a besoin d'un effectif plus profond. »
- **Focus par joueur** : un groupe entier (Physique, Attaque, Défense ou Gardien) ou une seule compétence de ce groupe. Sans focus, l'effort est réparti sur les 20 compétences. Changement possible à tout moment, effet à la semaine suivante.
- **« Le focus bat la dispersion »** : une compétence ciblée gagne son point bien plus vite que le même effort réparti sur 20.
- Progression lente et continue : le progrès s'accumule d'une semaine à l'autre jusqu'à un point entier, puis la compétence gagne +1. Plafond 100.
- **Temps de jeu** : les minutes jouées à chaque match (ligue et coupe) sont enregistrées et alimentent la semaine d'entraînement ; les joueurs réellement utilisés progressent plus vite [Dev chat, devlog 0.5.7 2026-10-04 et 0.6.0 2026-10-16]. Le rendement ne diminue pas avec le niveau : passer de 4 à 5 prend autant de temps que de 24 à 25 [Dev chat, chat jeu 2026-10-19 08:17].
- **Éthique de travail** (1–100) : trait fixe, sans effet en match ; décide seulement du rendement de l'entraînement.
- Rapport d'entraînement : liste des joueurs qui ont franchi un point et lesquelles de leurs compétences. Personne listé = personne n'a franchi de point, le progrès reste acquis.

## L'âge [W:Training, Players]
| Âge | Effet |
|---|---|
| ≤ 20 ans | Bonus d'entraînement complet |
| 21–24 | Le bonus baisse un peu à chaque anniversaire |
| 25 | Plus de bonus |
| à partir de 28 | Le gain hebdomadaire baisse chaque année |
| à partir de 30 | **Perte de compétences physiques à chaque changement de saison** (une part de chacune des 5, plus grande avec l'âge) |
| début de la trentaine | Le déclin dépasse ce que l'entraînement apporte : **pic de carrière** |
| ≥ 33 | Retraite possible (voir sixzeroleague-joueurs) |
« Continuer à entraîner un joueur âgé lui fait garder l'essentiel ; arrêter, et il décline. » Le bonus jeune est le même pour tous : c'est ainsi qu'un petit club à l'effectif jeune rattrape un riche.

## Formation à un 2e rôle [W:Training]
- Un joueur peut apprendre un 2e rôle et y jouer **sans la pénalité de hors-poste**.
- Les Training Facilities ouvrent un emplacement de formation aux niveaux **5, 10, 15 et 20** [W:Infrastructure].
- Apprentissage sur un certain nombre de journées, pour un coût hebdomadaire (rapport hebdomadaire) ; **annuler ne rembourse rien**. Durée : 2 saisons, soit 36 journées ; 3 rôles au maximum ; le joueur garde ses rôles précédents [Dev chat ; API 2026-10-18 : 36 journées, 150 € par semaine]. Le rôle de départ est définitif [Com chat]. Ce coût n'est pas multiplié par la division [W:Competitions].

## Académie U18 [W:U18]
| Élément | Règle |
|---|---|
| Nouveau choix | Toutes les **8 journées de ligue terminées** (horloge arrêtée hors saison de ligue) ; un choix attend dès la création du club |
| Prospects | 2, fixes jusqu'à ce qu'on en signe un |
| Signature | Un joueur complet rejoint l'effectif tout de suite, à **18 ans**, avec son nom et son poste ; taille, main forte et 20 compétences sont tirées **au niveau actuel de l'académie** |
| Compétences au niveau 1 | 1–20 |
| Plage des compétences selon le niveau | Observé : niveau 1 = 1 à 20, niveau 2 = 2 à 22, niveau 9 = 9 à 36 [Com chat, krzykaczpl_ 2026-10-20 ; pierrottingchrist_29708 2026-10-20]. Formule min = niveau, max = 18 + 2 × niveau : **vérifiée le 2026-10-23 sur `silver.sz_infrastructure_levels` (YouthAcademy, `effect_label`) pour les 20 niveaux** (niveau 20 = 20 à 58), donc plus une simple hypothèse. Dévoilement 2/4/6/8 compétences aux niveaux 3/8/13/18 et étrangers 2 % (niv. 5), 4 % (10), 6 % (15), 8 % (20) : mêmes données. La plage est lisible dans la description de l'infrastructure [Dev chat 2026-10-20]. |
| Compétences dévoilées avant signature | 2 / 4 / 6 / 8 aux niveaux 3 / 8 / 13 / 18 de l'académie (au hasard par prospect) ; monter le niveau en cours d'offre dévoile plus sur les 2 mêmes prospects |
| Prospects étrangers | Petite chance à partir du niveau 5, qui grandit lentement |
| Effectif | 30 au maximum : au plafond, on ne peut pas signer |
Après une signature, l'horloge repart : la paire suivante arrive 8 journées plus tard. L'académie sert surtout à **remplacer les retraités** ; un prospect doit encore s'entraîner pour progresser.

## [Obs] Nos données
- API : `/api/teams/mine/training` (plan), `/api/teams/mine/training/report` (rapport), `/api/teams/mine/role-training`, `/api/teams/mine/u18`.
- Aucun cycle d'entraînement encore joué le 2026-10-18 (saison remise à zéro).

## [Veille 2026-10-26] Mise à jour (V-20261026-4, -8)
- Un joueur blessé ne reçoit pas de points d entraînement [Dev chat, Gazelle, 2026-10-26 13:06 UTC ; V-20261026-4].
- Hypothèse (avis de joueur) : académie niveau 10 = compétences de 10 à 38, tirage moyen ~24, cohérent avec min = niveau et max = 18 + 2 x niveau [Com chat, Stoik, chat France 2026-10-23 08:45 ; V-20261026-8].
- Un rôle appris **reste avec le joueur s'il est vendu** (devlog 0.5.7). La fiche d'un joueur au marché montre les points physiques perdus avec l'âge la saison dernière (0.6.1). [Dev chat, D:L5, D:L9 ; V-20261026-21]

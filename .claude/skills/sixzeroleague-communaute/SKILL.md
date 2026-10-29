---
name: sixzeroleague-communaute
description: Ce que disent le chat du jeu Six Zero League et son développeur (Gazelle) — rythme réel (2 journées par jour, saison de 9 à 11 jours, +1 an par saison, entraînement et transferts réglés chaque soir), horaires des matchs, formation de rôle (2 saisons, 3 rôles max, rôle initial définitif), sponsor (re-signer = pas de prime), bots selon la division, conseils de joueurs (discipline, aléa des résultats). Chaque point est sourcé et daté. À charger avec les skills de règles sixzeroleague-*, surtout pour le calendrier et la planification.
---

# Six Zero League — communauté et développeur (chat du jeu)

## Comment lire cette skill
- **[Dev chat]** = Gazelle, qui déploie les mises à jour et lance les saisons : vaut une règle, mais le jeu est en alpha et change vite.
- Alias confirmé : **« Urban Fox » = Gazelle** (« This is Gazelle btw », C:82fda3, 2026-10-19 21:16) : ses messages sont des [Dev chat]. `Draugar` (jeu) = `krzykaczpl_` (Discord) ; `Scottern` = `sweeney4437`. [V-20261026-13]
- **[Com chat, pseudo]** = un joueur : opinion ou observation, **pas une règle**.
- **Le wiki l'emporte** en cas de contradiction ([W:Rubrique], skills sixzeroleague-*) ; les écarts sont signalés ⚠️.
- Source : export du chat global collé par l'utilisateur le 2026-10-18 (messages non datés, de la fin de la saison précédente au 18/10). Le chat est aussi capturé par le script (`/api/chat/messages?channel=global`).

## 1. Rythme réel du jeu (essentiel pour la planification)
- **Matchs de ligue à 12:00 et 20:00 (heure de Lisbonne)**, soit 13:00 et 21:00 à Paris : **2 journées par jour** [Com chat, 97777ali, confirmé « Yes! » par Dev chat].
- **Coupe** : 16:00 heure de Lisbonne selon le développeur = **17:00 à Paris** [Dev chat, chat jeu 2026-10-18 15:33]. Un joueur écrit 17:00 Lisbonne [Com chat, 97777ali 2026-10-18 17:55] : non confirmé par le développeur. Les matchs de coupe seront répartis dans la semaine plus tard [Dev chat]. (Ancienne version : 17:00 ou 18:00 incertain ⚠️, remplacée le 2026-10-23.)
- Une « semaine » du jeu = 2 journées de ligue [W:Finances], donc **en pratique un jour** : **l'entraînement se règle et le marché se clôt chaque soir après le match de 20:00 (Lisbonne)** [Dev chat]. Hors saison, aucune « semaine » ne passe.
- **Saison = 18 journées / 2 par jour = 9 jours**, jusqu'à 11 jours s'il y a beaucoup d'équipes en coupe [Dev chat]. **Les joueurs prennent donc 1 an tous les 9 à 11 jours** [Dev chat, à la question de Draugar].
  - Conséquence : le bonus jeune (jusqu'à 20 ans [W:Training]), le déclin (dès 30 ans) et la retraite (dès 33 ans) arrivent **très vite en temps réel**.
- Les annonces en cours se terminent au coup d'envoi suivant [Dev chat, début de saison].

## 2. Rôles et formation de rôle
- On ne change pas le rôle d'un joueur dans l'onglet Joueurs : il faut **l'entraîner au nouveau rôle** (onglet Entraînement), avec les Training Facilities au niveau 5 ou plus [Dev chat] — conforme au wiki.
- Apprendre un rôle prend **2 saisons au total** [Dev chat] ; nos données : 36 journées (`/api/teams/mine/role-training`, `totalRounds` = 36). **3 rôles au maximum** [Dev chat ; API `maxRoles` = 3]. Le joueur **garde ses anciens rôles** [Dev chat].
- On peut toujours aligner un joueur hors de son rôle, **avec une pénalité** [Dev chat] ; l'écran Tactique l'affiche en orange [Obs utilisateur, 2026-10-18].
- Le **rôle de départ, choisi à la création, est définitif** ; certains joueurs regrettent de l'avoir choisi avant de voir les compétences (« mon meilleur gardien est demi-centre ») [Com chat, Fundador23].
- [Obs utilisateur, 2026-10-18] L'utilisateur forme déjà un joueur à un 2e rôle : Sébastien Blanc, gardien, apprend ailier droit (3 journées sur 36 le 18/10).

## 3. Divisions, bots, saison
- Divisions introduites par une mise à jour : **tout le monde commence en 5e division**, montées et descentes à partir de la saison suivante [Dev chat].
- Le niveau des bots dépend de la division ; même en 1re division, ils n'ont **pas la moitié de la force** qu'une équipe humaine peut atteindre : c'est un frein pour le début du jeu [Dev chat].
- Résultats qui paraissent aléatoires (ex. défaite 16–24 puis victoire 28–20 contre le même leader) : selon le Dev, toutes les équipes sont encore faibles, la tactique a peu de profondeur, et **certaines compétences contrent ce qu'une équipe sait faire**, d'où des « affinités » entre équipes [Dev chat, à Draugar].
- Les ligues sont tirées au hasard, pas par niveau ; elles ont été remélangées en début de saison, d'où des ligues parfois plus fortes [Dev chat, 2026-10-07 et 2026-10-20]. Promotions et relégations seulement à la saison suivante : un champion promu, trois relégués (sauf 5e) [Dev chat, 2026-10-19]. Troisième saison du jeu [Dev chat, 2026-10-22].

## 4. Sponsor et argent
- Changer de sponsor ne fait pas perdre la prime de 3e place [Dev chat, à Carlinhos].
- **Re-signer le même sponsor** = ne pas en choisir un autre ; on perd alors la **prime de signature** [Dev chat, à Draugar].
- ⚠️ Bug connu : la prime de classement a été versée mais ne s'affichait pas dans l'onglet Finances [Dev chat].

## 5. Match, discipline, tactique
- Agressivité d'équipe **disponible depuis la 0.6.1** (Light, Normal, Hard) ; son effet n'est pas documenté ; elle était annoncée comme réponse aux jaunes et aux 2 min [Dev chat, C:911baf 2026-10-16 12:18 ; D:L9 ; V-20261026-14, remplace la puce « pas encore de réglage »]
- Pour moins de cartons et d'exclusions : travailler le **Marquage** d'abord, puis **Anticipation** et **Duels** [Com chat, Antarez] ; cohérent avec le wiki (Marquage et Duels = moins de fautes [W:Attributes]).
- Jeu passif : les équipes faibles tirent rarement pendant l'avertissement et perdent le ballon à la 7e passe ; selon le Dev, un tir pendant cette phase a pourtant actuellement **un taux de réussite plus élevé** ; point à revoir de son côté [Dev chat].
- Matchs joués avant la mise à jour des statistiques : seul le score est disponible [Dev chat].
- Le 7 m est tiré par le meilleur de l'équipe, sans choix possible [Dev chat, 2026-10-20]. Fautes de 2 min loin du ballon : bug en correction ; nombre d'exclusions en révision ; jeu passif : pression pour tirer ajoutée, mais les équipes faibles tirent encore peu [Dev chat, 2026-10-20 et 2026-10-21]. Seules les formations 5-1 / 6-0 existent ; un joueur ne peut pas être limité à l'attaque ou à la défense [Dev chat, 2026-10-10]. Stats adverses non visibles ; la formation adverse viendra dans les stats de match [Dev chat, 2026-10-22].

## 6. Économie, académie, alpha
- Coût des niveaux d'infrastructure caché volontairement ; Arena max > 9 999 par match à domicile, plus en division haute [Dev chat, Discord #chat 2026-10-19]. Bonus du Training Facilities +0,04 par niveau, linéaire (« si je ne me trompe pas ») ⚠️ contredit par nos données (+0,06 par niveau : ×1,30 au niveau 6 à ×2,14 au niveau 20, voir skill club) [Obs SQL 2026-10-26 ; V-20261026-17] [Dev chat, 2026-10-19].
- Fan Shop : 1,6 × (leader) à 0,7 × (dernier) selon le classement [Dev chat, devlog 0.5.7 2026-10-04].
- Conseil du développeur (avis) : revenus d'abord ; avec des Training Facilities hautes, garder les joueurs à forte éthique de travail puis les vendre [Dev chat, 2026-10-11].
- Joueur libéré : 10 % de chances d'être relisté en joueur libre [Dev chat, 2026-09-23].
- Les joueurs de l'alpha ne seront pas conservés à la sortie officielle ; tout le monde repart en dernière division [Dev chat, 2026-09-23].
- Prospect étranger : utile surtout pour les futures sélections nationales [Dev chat, 2026-10-20].
- Avis (pas des règles) : académie niveau 7 à 8 donne des joueurs vers 20 de note ; joueur d'académie ~5 à 5,5 mois de vie [Com chat, 2026-10-19 et 2026-10-20].

## [Veille 2026-10-26] Mises à jour (V-20261026-6, -7)
- Indices voulus par le jeu sur les adversaires : tactiques visibles dans les statistiques de match, scouting, niveau du club, rediffusions, MVP [Dev chat, Gazelle, 2026-10-23 10:00 UTC ; V-20261026-7].
- Anecdote : un joueur a eu 3 exclusions dans les 6 dernières minutes d un match de coupe [Com chat, 2026-10-25 17:32 UTC ; V-20261026-6].
- À surveiller (sans date) : pas d enchère plus grand pour les gros prix, page de statistiques de ligue. L export Discord #dev-log s arrête au 2026-10-22 : la 0.6.1 y manque.
- Jeu passif et exclusions modifiés en 0.6.1 (4 passes, moins d'exclusions, blessure d'entraînement divisée par deux) : voir skill match ; rupture de série au 2026-10-24 13:37 UTC [Dev chat, D:L9 ; V-20261026-15].
- Stratégies d'infrastructure observées : Stoik (2026-10-21) Arena 7, Training 1, Youth Academy 10, Fan Shop 10 ; martin (2026-10-22) Arena 9, Training 6, Academy 2, Fan Shop 1 ; pierrottingchrist_29708 (2026-10-20) Academy 9 ; Squidward : Academy 7 d'emblée (tirages 19 et 23). Avis opposés : Gazelle « revenus d'abord (Arena, Fan Shop) » (D:L215, L218) contre Stoik/Squidward « académie d'abord, entraînement en dernier » (C:0f6618, D:L255) — **avis, pas des règles**. [Dev chat / Com chat ; V-20261026-20]

## [Veille 2026-10-29] Mises à jour (V-20261029-1, -3, -8, -10, -11, -12)
- **Horaires 0.6.2** (Europe/Lisbonne → Paris) : 12:00 → 13:00 1er tour de ligue ; 16:00 → 17:00 coupe, s'il y en a un ; **18:00 → 19:00 Coupe du monde, s'il y en a une** ; 20:00 → 21:00 2e tour. La ligue 13:00/21:00 est inchangée. [Dev chat Gazelle, 2026-10-28 19:08 UTC ; V-1]
- **Sponsor** : au 2026-10-27 22:57 UTC, les clubs promus voient déjà de meilleures offres (non voulu : « some parts of the system think the season ended ») ; choisir tôt est sans problème, la ligue est terminée et les primes sont versées. [Dev chat Gazelle, 2026-10-27 21:25 et 22:57 UTC ; V-3]
- **Équipes nationales (0.6.2)** : tout pays avec assez de joueurs gérant un club a une sélection ; élection du sélectionneur en intersaison (« apply or vote »), un manager seul de son pays est élu d'office s'il a postulé ; sélection de 10 à 25 joueurs, changements seulement en intersaison ; classement mondial aux points de Coupe du monde. **Coupe du monde** : poules de 3 ou 4, élimination directe avec finale et match pour la 3e place, primes de fédération aux clubs des trois premiers pays ; ses matchs comptent pour blessures, suspensions, entraînement et stats. Un agent libre garde son appel en sélection quand un club le signe. Nous : aucune action tant qu'on ne postule pas. [Devlog 2026-10-28 12:08 UTC ; Dev chat 2026-10-28 19:08-19:37 UTC ; V-8]
- **Rythme futur (EN DOUTE, sans date)** : Gazelle prévoit de répartir les matchs sur la semaine et d'ajouter d'autres événements (« working towards a slower pace since the beginning ») ; le rythme actuel reste valable. [Dev chat 2026-10-28 11:08 et 18:42 UTC ; V-10]
- **Nouvelles couches joueurs (avis du développeur, sans date)** : main gauche 10 % des joueurs ; ambidextres prévus ; perks (très petite chance par joueur) ; talent. Visibilité de la main, de la taille, du talent ou de l'éthique à l'académie demandée par Stoik et DErick, Gazelle « not sure ». [Dev chat 2026-10-27 14:36, 15:32, 15:49 UTC ; V-6]
- **Triche signalée** : des comptes liés revendent deux joueurs sans valeur à 25 000 € (Perosinho Reborn, ZG Hooligans) ; Gazelle « on my radar » (2026-10-26 21:30 UTC). Ne pas prendre ces prix comme repère du marché. Clubs imbattables (Les Gaulois, 17/17, +110) : équipes très actives avec 1 à 2 saisons d'avance, pas un soupçon (Gazelle, 2026-10-27 13:35 UTC). [V-11]
- **Éthique de travail (avis Draugar, non confirmé par Gazelle)** : pas de changement dans la carrière, elle ralentit seulement l'entraînement. [Dev chat 2026-10-27 21:13 UTC ; V-12]

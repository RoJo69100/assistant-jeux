---
name: sixzeroleague-communaute
description: Ce que disent le chat du jeu Six Zero League et son développeur (Gazelle) — rythme réel (2 journées par jour, saison de 9 à 11 jours, +1 an par saison, entraînement et transferts réglés chaque soir), horaires des matchs, formation de rôle (2 saisons, 3 rôles max, rôle initial définitif), sponsor (re-signer = pas de prime), bots selon la division, conseils de joueurs (discipline, aléa des résultats). Chaque point est sourcé et daté. À charger avec les skills de règles sixzeroleague-*, surtout pour le calendrier et la planification.
---

# Six Zero League — communauté et développeur (chat du jeu)

## Comment lire cette skill
- **[Dev chat]** = Gazelle, qui déploie les mises à jour et lance les saisons : vaut une règle, mais le jeu est en alpha et change vite.
- **[Com chat, pseudo]** = un joueur : opinion ou observation, **pas une règle**.
- **Le wiki l'emporte** en cas de contradiction ([W:Rubrique], skills sixzeroleague-*) ; les écarts sont signalés ⚠️.
- Source : export du chat global collé par l'utilisateur le 2026-10-18 (messages non datés, de la fin de la saison précédente au 18/10). Le chat est aussi capturé par le script (`/api/chat/messages?channel=global`).

## 1. Rythme réel du jeu (essentiel pour la planification)
- **Matchs de ligue à 12:00 et 20:00 (heure de Lisbonne)**, soit 13:00 et 21:00 à Paris : **2 journées par jour** [Com chat, 97777ali, confirmé « Yes! » par Dev chat].
- **Coupe** : 16:00 heure de Lisbonne selon le Dev [Dev chat], 17:00 selon un joueur que le Dev confirme ensuite ⚠️ (17:00 ou 18:00 à Paris) ; ces matchs seront plus tard répartis dans la semaine [Dev chat].
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

## 4. Sponsor et argent
- Changer de sponsor ne fait pas perdre la prime de 3e place [Dev chat, à Carlinhos].
- **Re-signer le même sponsor** = ne pas en choisir un autre ; on perd alors la **prime de signature** [Dev chat, à Draugar].
- ⚠️ Bug connu : la prime de classement a été versée mais ne s'affichait pas dans l'onglet Finances [Dev chat].

## 5. Match, discipline, tactique
- Pas encore de réglage d'agressivité d'équipe : prévu dans une future mise à jour tactique [Dev chat].
- Pour moins de cartons et d'exclusions : travailler le **Marquage** d'abord, puis **Anticipation** et **Duels** [Com chat, Antarez] ; cohérent avec le wiki (Marquage et Duels = moins de fautes [W:Attributes]).
- Jeu passif : les équipes faibles tirent rarement pendant l'avertissement et perdent le ballon à la 7e passe ; selon le Dev, un tir pendant cette phase a pourtant actuellement **un taux de réussite plus élevé** ; point à revoir de son côté [Dev chat].
- Matchs joués avant la mise à jour des statistiques : seul le score est disponible [Dev chat].

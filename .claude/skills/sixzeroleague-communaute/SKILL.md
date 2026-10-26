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
- Pas encore de réglage d'agressivité d'équipe : prévu dans une future mise à jour tactique [Dev chat].
- Pour moins de cartons et d'exclusions : travailler le **Marquage** d'abord, puis **Anticipation** et **Duels** [Com chat, Antarez] ; cohérent avec le wiki (Marquage et Duels = moins de fautes [W:Attributes]).
- Jeu passif : les équipes faibles tirent rarement pendant l'avertissement et perdent le ballon à la 7e passe ; selon le Dev, un tir pendant cette phase a pourtant actuellement **un taux de réussite plus élevé** ; point à revoir de son côté [Dev chat].
- Matchs joués avant la mise à jour des statistiques : seul le score est disponible [Dev chat].
- Le 7 m est tiré par le meilleur de l'équipe, sans choix possible [Dev chat, 2026-10-20]. Fautes de 2 min loin du ballon : bug en correction ; nombre d'exclusions en révision ; jeu passif : pression pour tirer ajoutée, mais les équipes faibles tirent encore peu [Dev chat, 2026-10-20 et 2026-10-21]. Seules les formations 5-1 / 6-0 existent ; un joueur ne peut pas être limité à l'attaque ou à la défense [Dev chat, 2026-10-10]. Stats adverses non visibles ; la formation adverse viendra dans les stats de match [Dev chat, 2026-10-22].

## 6. Économie, académie, alpha
- Coût des niveaux d'infrastructure caché volontairement ; Arena max > 9 999 par match à domicile, plus en division haute [Dev chat, Discord #chat 2026-10-19]. Bonus du Training Facilities +0,04 par niveau, linéaire (« si je ne me trompe pas ») [Dev chat, 2026-10-19].
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

---
name: derbymanager-tactique
description: Règles Derby Manager de la tactique et du moteur de match — grille 5×5 et 3 lignes, formations, rôles (FB, WB, AWB, IWB, CD, LD, BPD, libero, HM, DLP, BTB, CM, TQ, DWG, AWG, HWG, WF, IF, CF, target man, F9), options (pressing, counters, build from defence, Careful/Risky), coups de pied arrêtés, remplacements (RAT/CON/AUTO/DEV/IMP/EMR), build up / prevent build up et 13 dots (octobre 2026), conversion des tirs, gardiens, conseils du développeur sur les formations. À charger pour composer, régler ou analyser un match.
---

# Derby Manager — tactique et moteur de match

Sources : `outputs/derbymanager/veille/connaissance.md` (2026-10-30). `dev` = développeur. Le moteur a été refondu en octobre 2026 : toute règle antérieure à 2026-10-21 sur le build up est « contredit » sauf mention.

## Formations et lignes
- Trois lignes : D | DM+M | AM+F ; grille 5×5 de positions fixes (25 combinaisons) ; positions DL DLC DC DRC DR, ML…MR, FL…FR — #italy 2025-02-24, dev ; #discussion 2024-06-19, dev.
- Le losange 4-4-2 n'existe pas : HM + TQ, ou CM + LIB — #italy 2026-07-17, joueurs faro1 / randykeys — complété.
- « Formations are the biggest part » ; 0-5-5 ⇒ 90 % de défaite, 235 ⇒ 80 % — #italy 2025-07-10 / 2024-11-27, dev.
- Petit bonus par joueur pour les formations régulières ; « solo FC works but not solo DC or MC » ; seuil de 20 % de joueurs par ligne — #italy 2025-04-28, dev.
- Méta voulue « moderate » : mélange d'âges, joueurs solides partout, pas 1-4-5 ni 5-0-5 — #general 2025-04-25, dev.
- Formations des bots 2025-07-25 : 433 = 1,82 pt/match, 442 = 1,79, 343 = 1,77 — #england 2025-07-25, dev — fait daté.
- Octobre 2026 : 523 jouable ; 433 et 343 « overflow the tactical spheres » ; 6 joueurs sur une ligne = problème connu ; 3TQ + 3CM perdent la condition plus vite — #belgium 2026-10-13 / 10-19 / 10-21 / 10-10, dev.
- Pas de formation 3 joueurs larges possible ; 13 places pour 11 joueurs refusé — #inconnu 2026-10-22 ; #belgium 2026-10-28, dev.

## Conseils du développeur
- « Try 541 with wingers. Si l'adversaire joue avec des attaquants larges : FB + DLP + BTB. S'il joue étroit : IWB + 2×BTB » — #italy 2025-08-13, dev.
- Ailiers : passing focus wide, threat focus autre que shoot, build up wide — #italy 2025-08-14, dev.
- « The real counterattacking formation is 523 » — #italy 2025-02-25, dev.
- Ne pas laisser les deux flancs vides ; un milieu de côté du même côté que l'attaquant de côté ; jouer les counters — #italy 2025-07-07, dev.
- Contre meilleur : jouer défensif (WB → FB ou 541 au lieu de 442) — #italy 2024-09-06, dev.
- 433/343 asymétriques OK pour le build up, 334 non ; 3 attaquants centraux problématiques sans 3 DC ; 3 défenseurs sans latéraux mauvais ; 532 trop défensif — #discussion 2025-07-17 ; #italy 2025-07-10 ; #spain 2025-02-21 ; #france 2025-05-03, dev.
- « Not even top teams use 11 players, it's about a strong team, not a strong 11 » — #italy 2025-08-23, dev.
- Un 523 du développeur génère plus qu'un 433 avec 6 joueurs au même endroit ; équilibre recommandé — #belgium 2026-10-08, dev — avis.

## Rôles (ce que fait chaque rôle)
- FB : reste toujours derrière ; WB : monte mais pas tout du long ; AWB : monte tout le long (presque un milieu) ; IWB : se rabat au milieu — #discussion 2024-09-27, dev ; #belgium 2026-10-19, dev.
- CD : monte sur coup de pied arrêté ; LD : reste derrière, ne presse pas vers l'avant ; BPD : pompe la 1re étape du build up et reste en défense ; LIB : DC qui monte quand le ballon est haut, coûte de la stamina — #updates 2025-02-10 ; #quick-questions 2024-11-15, dev.
- HM : reste en rangée DM ; DLP : rangées DM et MC ; BTB : défend et monte devant le CM, dépense de condition 9 ; CM : reste au milieu, plus offensif que le BTB, quasi exclusivement AM — #belgium 2026-10-10 ; #discussion 2024-09-22, dev.
- TQ (poste FC pour un AM pur) : passe et tire de loin, se joue avec un target man devant ; TM : vise les têtes, attire 2 défenseurs, tir 2 ; CF : pousse la ligne et tire dès qu'il peut ; F9 proche du TQ — #discussion 2025-02-24 / 2025-07-03 ; #quick-questions 2024-12-12, dev.
- WF : centres et menace devant ; AWG : comme le WF, revient au centre dans notre surface ; HWG : milieu puis côté pour centrer ; IF : coupe vers l'intérieur — #discussion 2024-09-27, dev.
- Chiffres BU/PBU (2025-08-08, #discussion, dev) : FB 1/6, WB 4/4, IWB 2/5, AWB 6/3 ; DWG 4/7, WM 6/4, IWG 5/5, WG 8/3 ; FLR 1-3 en BU, 0 en PBU ; TQ BU 4 ; LIB BU 1 ; LD empêche 5 comme un CM génère 5 ; DWG + FB = 8 de prévention (+60 %) — #italy 2025-02-07, dev. DLP 4/4 (« Test your tactic », 2026-05-23, joueur).
- Dépense de condition par rôle (échelle réelle 5-9) : BTB 9, DWG 8, DLP 7 — #inconnu 2026-10-19, dev.
- Compétences clés par rôle : non définies par le développeur (« I don't know which skills are the most important for each role », #quick-questions 2024-09-05) ; toutes les compétences sont également importantes (2026-07-10) ; liste dans le wiki, hors veille.
- Les rôles n'influencent pas l'entraînement — #quick-questions 2026-05-08, joueur faro1 — complété.

## Curseurs et options
- Careful : build up central en prévention 15 ⇒ 17, création 20 ⇒ 20 ; Risky : 15 / 22 ; effet global ≈ 5 % ; sans coût de condition — #italy 2025-08-21, dev ; #quick-questions 2025-04-24, dev.
- Pressing : sans pressing A presse B s'il est à B1/B2 dans sa moitié, B1 dans celle de B ; avec pressing jusqu'à B3 dans les deux moitiés ; **coûte de la condition** ; +50 % pour empêcher le build up défensif — #quick-questions 2026-10-05 ; #updates 2025-02-24, dev.
- Build from defence : +50 % aux chiffres de rôle (3 ⇒ 4,5) ; coûte de la stamina — #updates 2025-02-24, dev.
- **Chaque option tactique cochée coûte 1 % de condition à tous** — #updates 2026-10-18, dev.
- Ligne défensive : positionne seulement ; low block = joueurs plus bas qui pressent plus bas — #quick-questions 2026-10-05, dev.
- Passing focus narrow : plus de points aux joueurs centraux ; passe vers l'avant +1/+2 points ; mentality sans effet sur les passes — #general 2024-12-05, dev.
- Tirs : 4 options Shoot, Box, Cross, Mix ; « From the box » n'influence pas les têtes ; Shoot et Box réduisent les centres — #quick-questions 2024-11-23 ; #discussion 2024-12-18, dev.
- Counters : un contre est joué si le ratio défenseurs/attaquants devant le ballon le permet (4 contre 4 oui, 3 contre 4 non en passes courtes ; avec « counters » même 1 contre 4) — #discussion 2025-05-05, dev.
- S26 (2026-09-28) : options « decoupled », certaines nouvelles, d'autres retirées ; liste détaillée (Defensive line, Pass preference, Pass focus, Shooting, Headers) absente de la veille — #updates dev — en doute.
- Run with ball : avance de 15 m si réussi, sinon l'adversaire prend le ballon ; les joueurs ralentissent plus ils courent — #quick-questions 2025-06-01 ; #updates 2025-05-31, dev.
- Through balls (passes en profondeur) occasionnelles depuis S26, sans prise en compte de la vitesse — #updates 2026-09-28, dev.

## Coups de pied arrêtés
- Preneurs réglables depuis S25 (2026-09-28) ; priorité des placements ; « si tout le monde est dans la surface, c'est comme ne rien régler » ; un tireur « long shot » pour coups francs, « long pass » pour corners — #updates 2026-09-28, dev ; #discussion 2026-10-01, dev.
- Sans réglage : un des 3 meilleurs en set pieces ; 6 joueurs aux valeurs les plus hautes montent dans la surface ; un but est « set piece » s'il survient dans les 3 actions — #updates 2025-02-16/18, dev ; #italy 2026-03-15, dev.
- Corner ≈ 0,06 xG — #italy 2025-02-15, dev.

## Remplacements (2026-10-21/25)
- 5 remplaçants (4 selon #inconnu 2026-10-22 : contredit, remplacé le 2026-10-25) ; remplacements autour de la 55e-65e minute, le 3e vers la 110e ; on ne choisit ni le joueur exact remplacé ni la minute — #updates 2026-10-21/25, dev.
- Statuts d'entrée : RAT (remplace un joueur dont la note est ≥ 0,5 sous la moyenne de l'équipe), CON (condition < 80 %), AUTO (mix condition + note + jaunes), DEV (score ±2), IMP (priorité si l'équipe ne gagne pas), EMR (blessure seulement) — #updates dev.
- Statuts de sortie : RAT (note ≥ 0,5 sous la moyenne ou < 6,5), CON (< 80 %), AUTO, DEV (priorité si pas gagnant), IMP (seulement si +2 buts), EMR — #updates dev.
- Un GK remplaçant se règle « blessure seulement » — #inconnu 2026-10-22, dev. Les cartons jaunes ajoutent du poids ; blessures et cartons possibles en match.

## Build up / PBU (règle actuelle, octobre 2026)
- BU et PBU d'un joueur = rôle (0-9) × compétence × multiplicateur (≤ 2 : créativité/pressing, tier, forme) ; exemple « 20/60 » avec rôle 5/5 ⇒ 6 et 8 — #updates 2025-04-23 / 2025-09-08, dev.
- Compétences : BU = creativity, dribbling (technique), first touch, tier ; PBU = anticipation, positioning, tackling, tier — #updates 2025-08-04, dev.
- Un seul build up avec **matrice build up/pressing** ; **13 dots : 5 pressing + 8 build up** ; chaque dot demande 2 joueurs dans une direction précise ; **−10 % de build up par dot manquant** — #updates 2026-10-21 ; #inconnu 2026-10-22, dev.
- Avertissement quand trop de joueurs dans une zone ou trop peu dans une zone critique ; chaque avertissement réduit le build up — #updates 2026-10-25, dev.
- Points rouges à l'écran effectif = problème de couverture ; 1 point rouge n'est pas fatal (≈ 2-3 actions de moins) ; on clique un point pour voir qui contribue — #inconnu 2026-10-22, dev.
- Sans joueur de prévention (0 point) on cède le milieu (433 contre 415 va à 433) — #belgium 2026-10-11, dev.
- Lecture : « 4/8 » = 4 build ups réussis sur 8 ; « 9:10 (47 %) » = BU 9 contre PBU 10 — #quick-questions 2026-07-16 / 2026-09-10, joueurs — complété.
- Ancien système (2 étapes défensif + L/C/R, 50 % puissance relative + 50 % tactique) : contredit pour la mécanique, valable comme historique — #general 2025-02-25 ; #discussion 2025-03-03, dev.

## Moteur de match
- Chaque minute une équipe tente une action ; ~18 build ups par match ; la moitié des actions finissent après 2 passes ; moteur « turn based underneath » — #general 2025-02-25 ; #discussion 2025-06-03 ; #belgium 2026-10-02, dev.
- Conversion des tirs : normal ≈ 17-21 %, long ≈ 11-14 %, tête ≈ 11-18 %, penalty ≈ 73-80 % (2026-03-11 → 2026-04-22) ; 2026-09-03 : close 20 %, long 14 %, headers 16 % ; ~22 % des tirs sont des têtes — #general 2026-03-11 ; #quick-questions 2026-04-22 ; #italy 2026-09-03, dev.
- Long shot = hors de la surface — #general 2026-03-11, dev.
- xG depuis 2026-03-14 : sans compétences mais avec la pression sur le joueur ; inclut le blocage (2026-10-09) — #italy 2026-03-14 ; #quick-questions 2026-10-09, dev.
- Gardiens : +1 point d'attributs ≈ +0,3 à 0,4 % de save rate ; meilleur 79,5 %, pire 66,7 % ; expérience « quite important » — #italy 2026-09-03, dev.
- Élan : ≈ 1 % pour 1 but d'écart, ≈ 10 % pour 3 buts, ne touche que le build up — #italy 2024-09-03, dev. Rien n'est prévu pour perdre des points volontairement — #italy 2026-10-08, dev.
- Écarts de puissance (2024-07-27) : +1000 ⇒ 79 % des points ; +500-1000 ⇒ 54 % ; +100-500 ⇒ 45 % ; <100 ⇒ 26 % — #discussion, dev — complété.
- Avantage du terrain : ≤ 10 % par joueur en ligue, aucun en coupe — #discussion 2026-02-14 ; #england 2026-09-16, dev.
- Pénalités de poste, TS (×0,75 à ×1,10), sharpness et condition s'appliquent en plus : voir `derbymanager-regles`.

## Pièges
- Le build up d'avant octobre 2026 (L/C/R + 2 étapes) n'est plus la règle : ne pas conseiller « surcharger une zone sans pénalité ».
- Chaque option cochée (pressing, counters, build from defence…) coûte 1 % de condition à tous : ne pas tout cocher par défaut.
- TQ et CM rangés tous deux en AM : en empiler 6 est un problème connu du développeur.
- Pas de remplacements avant 2026-10-21 : les analyses de matchs antérieurs n'en contiennent pas.
- Le contre-attaque « gratuit » est en cours de correction (2026-10-30) — en doute.
- Les statistiques de tirs sont des échantillons d'un jour ou d'un tour ; le développeur veut une conversion globale d'environ 1 tir sur 10, pas 1 sur 6 — #quick-questions 2026-04-22.
- Hors-jeu : « offside trap » mentionné le 2026-10-30 (#inconnu) ; absent jusqu'en 2025-02 — en doute.
- Un joueur « individualistic » tire plus qu'il ne passe : à éviter en rôle de passeur.

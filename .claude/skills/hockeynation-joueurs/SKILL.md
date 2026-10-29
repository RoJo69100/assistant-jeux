---
name: hockeynation-joueurs
description: Règles Hockey Nation sur les joueurs — 4 équipes (PRO, FRM, U21, U17) et ce que le GM contrôle dans chacune, compétences (0-10) des patineurs et gardiens, plafonds (maxings), talents fort/faible et lecture par poste, double poste, compétences spéciales, attributs cachés, expérience, âge, déclin, retraite, recrues. À charger pour évaluer un joueur, une ligne, un échange ou une extension.
---

# Hockey Nation — joueurs

Sources : **[G:Rubrique]** = guide officiel (mis à jour le 30/09/2026, lu le 2026-10-23, `bronze.raw_pages` page_type `guide`). **[U]** = règle de l'utilisateur. **[H]** = hypothèse à confirmer.

## Les 4 équipes [G:Teams]
| Équipe | Âges | Ce que le GM contrôle |
|---|---|---|
| PRO | tous | tout : coachs, échanges, contrats PRO, rachats, rétrogradations, entraînement, lignes A/B/C et plan de jeu |
| FRM (Farm, depuis 04/2025) | 22+ en pratique | coachs, entraînement complet, contrats ; lignes automatiques ; 30 joueurs et 30 contrats Farm au maximum |
| U21 | 18-21 | draft (5 choix), échanges, contrats ELC ou Farm, libération ; **pas d'entraînement réglable**, lignes automatiques |
| U17 | 15-17 | rien de plus que les coachs ; 7 jeunes de 15 ans par saison, 5 draftables, 2 non draftables (NDE, dont 1 via l'Import Draft) |
Lignes FRM, U21, U17 : construites sur le **poste principal** d'abord ; le 2e poste ne sert que pour combler. « Swap position » échange poste principal et secondaire à tout moment (PRO, FRM, U21) [G:Lineups].

## Compétences [G:Players]
- Patineurs, 0 à 10 : SKA patinage, END endurance, PWR puissance, SHO tir, PAS passe (principale source d'occasions), DEF défense (« crucial » pour empêcher les occasions), CHK mise en échec (récupérer le palet), DSC discipline, FOF mises au jeu (attaquants seulement).
- Gardiens : REF réflexes, END (nombre de matchs avant fatigue), POS placement, PAD jambières, BLO bloqueur, GLO mitaine, STK canne (arrêt le moins fréquent).
- Seul un **niveau entier** compte en match ; les points partiels ne servent à rien [G:Training].
- Plafond (maxing) propre à chaque compétence, entre 4 et 10 (3 à 5 pour les amateurs). `max: true` = plafond atteint ; le joueur entraîne alors une compétence au hasard [G:Training].

## Talents : la lecture prioritaire [U, 2026-10-23]
- Talents = les **2 compétences au plus fort potentiel** et **la plus faible** [G:Scouting].
- Compétences clés par poste [H, tiré des définitions] : C = SHO, PAS, SKA, FOF ; LW/RW = SHO, PAS, SKA ; LD/RD = DEF, CHK, SKA ; G = REF, POS, PAD, BLO, GLO (`gold.hn_position_keys`).
- Verdict (`gold.hn_player_fit`, `gold.hn_draft_board`) : **idéal** = 2 talents forts clés et talent faible hors clés ; **correct** = 1 talent fort clé ; **contre-emploi** = aucun. Exemple de l'utilisateur : un ailier aux talents DEF + CHK ne nous intéresse pas.
- Double poste : vérifier les deux postes ; Blednov (RW/C, talents DEF + FOF) est « correct » au centre et « contre-emploi » à l'aile (2026-10-23).
- Mauvais poste en ligne = **−20 %** sur les compétences [G:Lineups].

## Compétences spéciales [G:Players]
0 à 3 par joueur. Les plus utiles à suivre : Inspire, Tactician, Team Player (effets collectifs), Powerplay Specialist, Penalty Killer, Second Wind, Brick Wall (gardien), Goalie Tandem (2 gardiens). Late Bloomer : débloquée à 25 ans.

## Attributs cachés, expérience, capitaine
- Work Ethic (effort à l'entraînement, varie chaque jour) et Leadership (capitanat) [G:Players].
- Expérience 0 (None) à 10 (Elite), gagnée en match officiel : 100 % en PRO, 75 % FRM, 50 % U21, 25 % U17 ; pas en amical. Ex. None → Awful = 25 matchs PRO, 34 FRM, 50 U21, 100 U17 [G:Competitions].
- Capitaine choisi sur expérience + leadership ; « Veteran Leadership » aide à gagner les duels : à ne pas sous-estimer dans une équipe jeune [G:Lineups].

## Âge [G:Players, Training]
- Entraînement un peu moins efficace avec l'âge, effet maximal dès 25 ans.
- Déclin possible dès 32 ans sur les compétences plafonnées (sauf DSC), maximal vers 35-39 ; les coachs n'y changent rien.
- Retraite annoncée dès 35 ans (jour 1), effective en fin de saison ; pic de probabilité à 39.
- Recrue (rookie) : 23 ans ou moins et 10 matchs PRO au plus.

## [Veille 2026-10-29] Mises à jour (V-20261029-6, -7)
- **Compétences clés par poste — hypothèse [H] complétée, avis de joueur** : SHO et PAS = buts ; SKA et PWR = possession du palet ; CHK et DEF = défense ; DSC = pénalités prises ; FOF : un bon joueur de mise au jeu par ligne suffit, pas forcément le centre. PWR serait donc à ajouter à SKA pour C/LW/RW/D, à tester sur les lignes avant de modifier `gold.hn_position_keys` (rendu tactique figé). [Discord #general, talonflame1, 2026-04-04 ; V-6]
- **Gardiens** : END = nombre de matchs avant fatigue, titulaire 7+ ; STK est la compétence la moins utilisée ; un gardien à END bas arrive à ~60 % de condition en 3e période (avis talonflame1, 2026-04-04). La perte de condition pèse relativement plus sur les hautes compétences (d0ghouse, 2025-12-03). [V-7]

## [Veille intégrale 2026-10-29] OVR, spéciales, déclin, expérience, potentiel (V-A-1 à A-4, A-22, A-23, A-25, V-B-1, B-6, V-C-6 à C-8)
- **OVR joueur (hnadmin 2022-09-28)** : moyenne des compétences où chaque niveau au-dessus de la moyenne compte deux fois ; décimales gardées, arrondi à la fin ; l'expérience n'est pas comptée. Exemple : 4 compétences à 4 et 4 à 8 → somme 48, excédent 8 → (48 + 8) / 8 = 7 → OVR 70. La formule « (somme + excédents) / n » est une déduction de l'exemple : vérifier sur un joueur de l'effectif avant de modifier `gold.hn_potential`. [V-A-1]
- **Spéciales (règles chiffrées)** : *Equalizer* annule une spéciale adverse au hasard (deux Equalizers = les deux spéciales d'un joueur) ; ordre : Equalizers, puis Telepathy, puis les autres ; *Telepathy* copie une spéciale que le joueur n'a pas (jamais Equalizer ni une annulée) ; *Team Player* +2 par joueur quand 5 jouent ensemble (+10) ; *Inspire* : un seul bonus actif à la fois par joueur ; *Patriot* : +1 à une compétence au hasard d'un compatriote, une fois par match, ne se cumule pas ; *Mr Game Five* +1 à toutes les compétences, *Playoff Beard* +1 à deux ; cumul : gardiens +9, défenseurs +10, attaquants +11 ; *Agitator* : −1 DSC au mieux noté adverse (jamais sous 0) ; *Goalie Tandem* : l'autre gardien reçoit +2 sur la meilleure compétence du premier (hasard entre ex æquo, tirée au début du match) ; les deux gardiens doivent l'avoir (avis avakael 2026-04-16). Questions sans réponse : +1 Patriot sur une compétence à 10 ? Patriot d'un gardien remplaçant ? [hnadmin / d0ghouse 2022-2025 ; V-A-2, B-6, C-8]
- **Déclin** : seules les compétences **plafonnées** déclinent ; DSC ne décline jamais ; chaque jour une compétence est tirée au hasard et, si elle est en déclin, ajoute des points de déclin (1 en déclin sur 8 = 12,5 % par jour) ; dépend de l'âge (max à 35 ans) et du poste (attaquants > défenseurs > gardiens) ; l'entraînement accumulé n'y change rien. [hnadmin 2023-04-20, 2023-11-10 ; V-A-3]
- **Expérience** : gagnée selon le niveau de la compétition (PRO 100 %, FRM 75 %, U21 50 %, U17 25 %), pas selon le temps de glace ; gardien : titulaire remplacé 100 %, remplaçant qui entre 100 %, remplaçant qui ne joue pas 25 %. **Capitaine** : leadership caché **fixe** + expérience ; un joueur nommé A ou C avec des coéquipiers plus expérimentés révèle un fort leadership ; seuls les 3 titulaires du capitanat en profitent. [d0ghouse 2022-09-06, 2023-08-15, 2025-08-16 ; hnadmin 2025-02-17 ; segi_3554 2024-08-16 ; V-A-4, B-1, B-6]
- **Potentiel** : minimum et maximum se déduisent des talents (2 plus forts, 1 plus faible) ; compétences plafonnées visibles (pucs rouges) ; plancher 4 (3 pour les amateurs, plafond 3-5) ; aucun rapport de scout n'indique le potentiel. [hnadmin 2022-04-11, 2024-03-24 ; d0ghouse 2022-07-30, 2025-07-08 ; V-A-25]
- **Rating d'équipe (avis, rétro-ingénierie de valyxn 2026-05-09, non confirmée)** : OFF = SHO + PAS ; DEF = DEF + CHK ; PHY = SKA + END + PWR ; DSC et FOF ne comptent pas — complète l'hypothèse [H] de `gold.hn_position_keys` (PWR et END). [V-C-6]
- **Blessures — hypothèse** : aucune n'est implémentée à notre connaissance ; proposées en 2023 (9 par saison, 25 % majeures), rejetées par un vote de la communauté (2023-07 → 2024-04), hnadmin a dit qu'elles pouvaient être annulées ; ne bâtir aucun plan dessus. [.coleh 2023-07-04 ; hnadmin 2023-03-24, 2023-04-17 ; fishyicee 2026-02-19 ; V-A-23, B-1, C-7]
- **Comptes inactifs** : non connecté depuis 28 jours = marqué à supprimer (suppression au changement de saison) ; Mode vacances +28 jours ; leurs choix de draft et joueurs suivent les règles des bots. [hnadmin 2026-02-10, 2026-07-21 ; V-A-22]

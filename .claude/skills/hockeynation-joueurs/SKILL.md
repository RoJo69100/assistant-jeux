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

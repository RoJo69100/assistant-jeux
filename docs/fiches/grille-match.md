# Grille d'analyse de match — agent `match`, tous jeux

Minimum à chaque passage, victoire comme défaite (règle du 2026-10-24 : « % nul, voilà pourquoi » ne suffit pas ; reproche du 2026-11-07 : « tu regardes juste 3P et rim »). Chaque chiffre cite sa vue ; les requêtes propres au jeu sont dans `docs/fiches/<jeu>/match-grille.md`. Saison officielle seulement, amicaux à part.

## 0. Intégrité des données, avant tout
- Les feuilles de match lues sont bien les nôtres (nom de l'équipe) ; sinon les écarter et le dire.
- Séries et bilans comptés par requête (`count`), jamais à l'œil (règle N17).
- Un plan tactique changé = une période à part : ne pas mélanger les matchs joués avec des réglages différents.

## 1. Chaque nouveau match (un tableau)
Match | marge | écart de force (indice du jeu : WSI/TPI, note, OVR…) | tir pour et contre par zone | facteur décisif | absents. Dire si le résultat vient du niveau, du plan ou de la réussite adverse.

## 2. Victoires contre défaites, toute la saison
- Tableau W/L : n, marge moyenne, écart de force, tir pour et contre par zone (réussite et volume), pertes, rebonds, fautes quand le jeu les donne.
- Corrélation de la marge avec chaque facteur (`corr()` en SQL, n cité), facteurs classés du plus fort au plus faible. Un facteur fort qui dépend du niveau adverse (volume de tirs concédés, écart de force) n'est pas de la chance.
- Moins de 3 matchs d'un côté : le dire, confiance faible.

## 3. Joueurs
- Par joueur, sur nos feuilles : minutes moyennes, points, +/-, pertes et fautes ramenés à un temps de jeu fixe (36 min au basket), fatigue relevée. Meilleur, plus faible, qui joue trop, quel remplaçant coûte.
- Blessés et absents : marge avec et sans eux, n cité ; dire ce que perd la composition du prochain match.

## 4. Adversaire et ligue
- Tactique adverse lue dans l'export (BasketVibe : Preview et focus ; Six Zero League : `teams.tactics` ; Team Soccer : formation, style, consignes ; Hockey Nation : lignes et coachs ; Hardwood : `opp_man/opp_zone/opp_press`), ce qu'elle a fait, ce que nous ajustons.
- Autres clubs quand l'export le permet (classement, leader, ceux qui nous ont battus) : quelle tactique gagne dans cette ligue.
- Prochain adversaire : son écart de force estimé ; s'il manque, l'export à faire.

## 5. Fin
- 3 à 5 points d'amélioration applicables à l'écran (joueur nommé, réglage, valeur), chacun avec son chiffre, sa confiance et le match qui prouvera qu'il est faux.
- Grosse défaite ou 2e d'affilée : recommander l'agent `analyste`.

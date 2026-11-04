## Lire un match (feuille /game/<id>) [E]
- **Notre tactique demandée** (1re mi-temps, 2e mi-temps ou « No Change ») → `silver.hw_games`.
- **Défense réellement jouée par les deux équipes** : % Man, Zone, Pressure, 2nd Chance, Transition, Intentional Foul, et Extend au début, à la mi-temps et à la fin → `silver.hw_game_teams`. **C'est notre seule lecture de la tactique adverse** : on ne voit pas ses réglages.
- Efficacité par zone : au cercle, intérieur, mi-distance, à 3 points (réussis/tentés) ; SI pondéré et TPI des deux équipes ; blessés ; joueurs en Overwork.
- Box score → `silver.hw_game_box` : poste joué, minutes, tirs, OFG (tirs de l'adversaire direct), +/-, DIST (distance moyenne de tir), PITP, FBP, FD, **fatigue** (-, Lght, Mod, Hvy).
- Pour préparer un adversaire : ses matchs précédents (défense mesurée, efficacité par zone) et ses SI/TPI.


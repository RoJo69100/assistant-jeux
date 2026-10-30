---
name: hardwood-tactique
description: Règles Hardwood de la tactique et du match — Game Plan par match (depth chart + Game Tactics), ordre de remplissage des postes, Pace, Inside/Outside Emphasis, % Man/Zone/Pressure, Extend, Substitution Mode (Mass, Staggered A/B/C et leurs minutes de repos), ajustements de mi-temps (le premier qui se déclenche), Game Management par joueur (Green Light, Offensive Positioning, Playing Time, Foul Trouble Hook, Red Shirt), lecture de la feuille de match (efficacité par zone, défense adverse mesurée, fatigue, Overwork). À charger pour régler un match, lire un adversaire ou analyser un résultat.
---

# Hardwood — tactique et match

Sources : **[R:Rubrique]** = manuel officiel (capturé le 2026-10-30). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/v-tactique.md`, statut entre parenthèses). **[E]** = nos exports (vues `silver.hw_tactics`, `hw_management`, `hw_games`, `hw_game_teams`, `hw_game_box`).

## Game Plan [R:Game Strategy, Depth Chart & Game Plan]
- **Chaque match peut avoir son propre Game Plan** (lien « (set) » du calendrier) = un depth chart + des Game Tactics avec ajustements. Sans plan spécifique, le **plan par défaut** s'applique ; il sert aussi de point de départ à chaque plan de match.
- Depth chart : les 5 titulaires (tous différents) en haut, puis les remplaçants ; un même joueur peut doubler deux postes. Le moteur remplit les trous dans l'ordre **PG, C, PF, SF, SG**.

## Game Tactics [R:Setting Up Your Game Tactics] [E]
| Réglage | Valeurs | Effet |
|---|---|---|
| Pace | -5 à +5 | + = plus vite, plus de transition, moins de temps de possession |
| Inside/Outside Emphasis | I, i, ~, o, O | I = cherche les tirs intérieurs, O = extérieurs |
| Zone % / Pressure % | 0 à 100 par pas de 5 | le reste = individuelle (Man-to-Man). Zone : PG, SG, SF dehors, PF et C dedans [R:Glossary] |
| Extend | -5 à +5 (NC = inchangé à la mi-temps) | + = défense étendue vers l'arc, - = resserrée sous le panier ; elle dérive pendant le match selon les réussites adverses |
| Substitution Mode | Mass, Staggered A, B, C | voir ci-dessous |
- **Ajustements de mi-temps : 5 au plus**, chacun avec un déclencheur (Point differential, Points in the paint, 3-pointers made, Personal fouls, Opponent points in the paint, Opponent 3-pointers made) et un seuil bas et/ou haut (-25 à +25). **Seul le premier qui remplit son critère s'applique.**

### Repos des titulaires (minutes restantes dans la mi-temps) [R]
| Mode | Repos |
|---|---|
| Mass | tous entre la 7e et la 15e minute |
| Staggered A | C 18-11 ; PG et SF 15-8 ; SG et PF 12-5 |
| Staggered B | **PG et C 18-11** ; SG et PF 12-5 ; SF 15-8 (garde les postes clés occupés par les meilleurs) |
| Staggered C | repos courts : C 18-15 et 12-9 ; PF 15-12 et 6-3 ; SF 12-6 ; SG 18-15 et 6-3 ; PG 15-12 et 9-6 |
Le repos dépend aussi du Playing Time de chaque joueur.

## Game Management, par joueur [R:Game Management Settings] [E]
| Réglage | Valeurs | Effet |
|---|---|---|
| Green Light | x, --, -, (neutre), +, ++ | fréquence de tir ; x = ne tire jamais |
| Offensive Positioning | I, i, (neutre), o, O | où il joue. Arrière ou ailier en I : coupe vers le panier et évite l'arc. Grand en o/O : joue dehors (stretch-4). Influe aussi sur le rebond offensif |
| Playing Time | 0 à 40 min (1 à 15 « non recommandé ») | 40 ≈ tout le match ; **32 = moyen** ; 25 = plus bas conseillé ; **minimum 15 pour un titulaire** ; ignoré en prolongation ; 0 pour un redshirt |
| Foul Trouble Hook | none, slow, average, quick | vitesse de sortie en cas de fautes |
| Red Shirt | case à cocher | voir `hardwood-regles` |
- Nous, le 30/10 [E] : les 20 joueurs ont tous 32 min, average, Green Light et positionnement au neutre ; c'est le réglage par défaut, jamais personnalisé.

## Ce que dit la communauté [D]
- Pressure fait plus de fautes que Man, et Man plus que Zone ; le consensus est de mélanger les trois (confirmé par plusieurs joueurs).
- La zone est une seule zone (de type 3-2), sans 2-3 ni 1-3-1 (consensus 2026-01, sans réponse de Steve).
- Avant 2026, Extend négatif par défaut. **Le 2026-08-23, Steve a modifié Extend et le spacing** (scoring intérieur plus dur, plus d'ouvertures dehors) : tout conseil plus ancien est à retester.
- Les tirs à 3 points ont été relevés début 2026 (réglage de Steve).
- Pace et Foul Hook sont les deux grands leviers des fautes ; la taille pèse beaucoup dans le moteur.

## Lire un match (feuille /game/<id>) [E]
- **Notre tactique demandée** (1re mi-temps, 2e mi-temps ou « No Change ») → `silver.hw_games`.
- **Défense réellement jouée par les deux équipes** : % Man, Zone, Pressure, 2nd Chance, Transition, Intentional Foul, et Extend au début, à la mi-temps et à la fin → `silver.hw_game_teams`. **C'est notre seule lecture de la tactique adverse** : on ne voit pas ses réglages.
- Efficacité par zone : au cercle, intérieur, mi-distance, à 3 points (réussis/tentés) ; SI pondéré et TPI des deux équipes ; blessés ; joueurs en Overwork.
- Box score → `silver.hw_game_box` : poste joué, minutes, tirs, OFG (tirs de l'adversaire direct), +/-, DIST (distance moyenne de tir), PITP, FBP, FD, **fatigue** (-, Lght, Mod, Hvy).
- Pour préparer un adversaire : ses matchs précédents (défense mesurée, efficacité par zone) et ses SI/TPI.

## Inconnu
Bonus du terrain (réel d'après les joueurs, non chiffré), poids exact de la vitesse, de l'IQ et de la taille, effet des notes Game Tactics et Motivation du coach, algorithme des remplacements (« To Do » dans le manuel).

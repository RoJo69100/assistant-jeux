# Profil par rôle

Sources : skill sixzeroleague-joueurs [W:Players, Attributes, Injuries], -match [W:The game, Match], -entrainement. Compétences de 1 à 100, 20 au total en 4 groupes ; un joueur de champ utilise Physique, Attaque et Défense, un gardien Physique et Gardien [W:Attributes].

## Comment le jeu joue les compétences [W:Attributes, Match]
- Elles inclinent les probabilités (tirs, passes, interceptions, arrêts) sans décider seules ; en duel les deux notes comptent, deux bons joueurs s'annulent.
- **Taille** : avantage pour gardiens, arrières, demi-centres et pivots (plus petit que la moyenne coûte un peu). **Main forte** : ailiers et arrières jouent mieux du côté de leur main forte.
- **Hors poste** : pénalité « légère » sur attaque, défense, gardien, pas sur le physique ; ampleur non documentée. La note de rôle (`role_overalls`) est calculée **avant** la pénalité [Obs SQL 2026-10-18].
- Échelle : 1-14 Grassroots, 15-29 Amateur, 30-44 Semi-pro, 45-59 Professional, 60-74 Elite, 75-89 World class, 90-100 Legendary [W:Attributes]. Nos notes de joueur vont de 7 à 13 : Grassroots [Obs 2026-10-18].
- Le tireur de 7 m est le meilleur tireur et technicien sur le terrain (Tir et Technique) [W:Attributes].

## Les 7 rôles
| Rôle | Mission [W:Players] | Compétences clés [W:Attributes] | Piège |
|---|---|---|---|
| **Gardien (GK)** | Arrêts, arrêts propres, relance | Réflexes (arrêt principal), Un contre un (clé sur les 7 m), Placement, Prise de balle, Relance : toutes | Taille utile. Un gardien remplaçant ne joue dans le champ qu'en dernier recours [W:Injuries] |
| **Demi-centre (CB)** | Meneur, construit l'attaque au centre | Passe, Technique, Jeu sans ballon, Tir ; engagement et jets francs passent par lui | Passe basse = pertes de balle (Passe : moins de passes ratées ou interceptées) |
| **Arrière gauche / droit (LB / RB)** | Tireurs de loin, depuis les 9 m | Tir, Détente, Technique, Passe | Bien plus exposés aux blessures [W:Injuries] ; main forte à considérer |
| **Ailier gauche / droit (LW / RW)** | Couloir : vont aux 6 m, convertissent les occasions proches | Vitesse, Agilité, Tir, Contrôle du ballon | Main forte à considérer ; moins exposés aux blessures [W:Injuries] |
| **Pivot (P)** | Joueur de ligne : tient sa place aux 6 m, finit sous pression | Force, Contrôle du ballon, Jeu sans ballon, Tir | Bien plus exposé aux blessures [W:Injuries] ; avantage de taille |

Autres compétences utiles à tous : Endurance (peu d'endurance = plus d'erreurs et moins d'efficacité à mesure que le match avance), Marquage, Duels et Anticipation (moins de fautes, interceptions) [W:Attributes].

## Notre effectif au 2026-10-20 [Obs `silver.sz_players`, brief Tactique]
Note au rôle entre parenthèses ; 12 joueurs, aucun blessé.
| Rôle | Titulaire | Remplaçant naturel |
|---|---|---|
| GK | Bourgeois (11) | Blanc (9), en formation RW |
| CB | Simon (9) | Denis (7) |
| LB | A. Bertin (10) | Leroy (8) |
| RB | Roger (10) | **aucun** |
| LW | Lefebvre (13) | **aucun** |
| RW | Lemaire (8) | G. Bertin (8) |
| P | Benoit (10) | Chevalier (9) |

- **Focus d'entraînement à viser** (brief Entraînement 2026-10-20, avis, confiance moyenne) : Simon CB sur Passe (clé la plus basse, 1), Lefebvre LW et Lemaire RW sur Tir au lieu de Jeu sans ballon, qui n'est pas clé d'ailier.
- **Plan B** (brief Tactique, avis, confiance faible) : Lefebvre absent, un RW à l'aile (hors poste) ; Roger absent, Leroy (LB) en RB.
- **Marché** (brief Transferts) : un LW de 29 ans (note 10) et un RB de 29 ans (note 11) visés comme doublures ; résultat au règlement après J4.
- Tous les joueurs de champ sauf Denis sont droitiers : la main forte ne départage personne [Obs `silver.sz_players.preferred_hand`, brief Entraînement].

## Blessures et absences [W:Injuries]
- Durée 1 à 6 matchs du club, le plus souvent 1 ou 2 ; comptée sur ligue et coupe ; reportée sur la saison suivante. Un remplaçant par rôle ; sinon un autre joueur valide est placé automatiquement.
- À court de joueurs : défense moins bonne, moins d'espaces et de tirs en attaque. Jamais de forfait pour une blessure pendant le match.

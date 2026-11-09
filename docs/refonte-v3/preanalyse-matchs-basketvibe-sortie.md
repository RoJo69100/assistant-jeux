## Matchs analysés par groupe (box score des deux côtés)

| groupe | matchs | dont nous | dont autres équipes |
|---|---|---|---|
| G1 ligue v3 | 22 | 22 | 0 |
| G2 ligue v4 | 5 | 3 | 2 |
| G3 coupe v4 | 10 | 2 | 8 |
| G4 amical v4 | 15 | 15 | 0 |
| G5 amical v5 | 10 | 10 | 0 |

### Question 1 : ce qui sépare victoires et défaites (ligue seulement)

Corrélation de l'écart « nous − eux » du facteur avec la marge ; IC de Fisher à 98.75 % (α = 0.0125 par test) ; effet minimal r = 0.5 ; n requis 40.

| groupe | facteur | r [IC] | p | n disponible | n requis | verdict |
|---|---|---|---|---|---|---|
| G1 | eFG % | 0.92 [0.77 ; 0.97] | 0.000 | 22 | 40 | n trop petit |
| G1 | rebonds offensifs % | 0.77 [0.42 ; 0.92] | 0.000 | 22 | 40 | n trop petit |
| G1 | pertes de balle % | -0.59 [-0.85 ; -0.10] | 0.004 | 22 | 40 | n trop petit |
| G1 | lancers francs par tir | 0.18 [-0.37 ; 0.64] | 0.413 | 22 | 40 | n trop petit |
| G2 | eFG % | 0.99 [0.78 ; 1.00] | 0.001 | 5 | 40 | n trop petit |
| G2 | rebonds offensifs % | 0.19 [-0.92 ; 0.96] | 0.756 | 5 | 40 | n trop petit |
| G2 | pertes de balle % | -0.67 [-0.99 ; 0.74] | 0.219 | 5 | 40 | n trop petit |
| G2 | lancers francs par tir | -0.12 [-0.96 ; 0.93] | 0.847 | 5 | 40 | n trop petit |

Description (moyenne en victoire / en défaite de « nous », écart « nous − eux » du facteur) :

| groupe | facteur | victoires (n) | défaites (n) |
|---|---|---|---|
| G1 | eFG % | 0.075 (10) | -0.122 (12) |
| G1 | rebonds off. % | 0.084 (10) | -0.087 (12) |
| G1 | pertes % | -0.056 (10) | 0.024 (12) |
| G1 | LF par tir | 0.022 (10) | 0.016 (12) |
| G2 | eFG % | 0.277 (1) | -0.042 (4) |
| G2 | rebonds off. % | -0.006 (1) | -0.060 (4) |
| G2 | pertes % | 0.009 (1) | 0.043 (4) |
| G2 | LF par tir | -0.035 (1) | -0.007 (4) |

### Question 2 : minutes lourdes et fatigue

(a) Évaluation par minute au Q4 contre Q1 à Q3, joueurs avec ≥ 3 quarts, ≥ 27 min avant le Q4, ≥ 1 min au Q4. Effet = différence moyenne / moyenne de base (rapport des moyennes) ; IC par la méthode du delta (dénominateur fixé) ; α = 0.025 ; effet minimal −15 % ; joueurs d'un même match non indépendants.

| groupe | effet relatif [IC] | différence moyenne par minute | n disponible (joueurs-matchs, matchs) | n requis | verdict |
|---|---|---|---|---|---|
| G1 | -4.4 % [-27.8 ; 19.1] | -0.016 (base 0.362) | 116 / 20 | 523 (σ relatif 1.11) | n trop petit |
| G2 | -39.7 % [-136.4 ; 56.9] | -0.133 (base 0.333) | 13 / 4 | 783 (σ relatif 1.36) | n trop petit |
| G3 | -21.0 % [-66.3 ; 24.4] | -0.115 (base 0.551) | 18 / 6 | 259 (σ relatif 0.78) | n trop petit |
| G4 | -56.6 % [-84.5 ; -28.7] | -0.269 (base 0.475) | 32 / 10 | 190 (σ relatif 0.67) | n trop petit |
| G5 | -43.4 % [-89.9 ; 3.2] | -0.198 (base 0.456) | 24 / 7 | 382 (σ relatif 0.95) | n trop petit |

Contrôle hors critères (non retenu pour le verdict) : mêmes mesures pour les joueurs avec ≥ 3 quarts et de 5 à 26 minutes avant le Q4.

| groupe | effet relatif au Q4 [IC] | n (joueurs-matchs) |
|---|---|---|
| G1 | -1.3 % [-25.3 ; 22.7] | 43 |
| G2 | 8.4 % [-42.8 ; 59.7] | 21 |
| G3 | -4.3 % [-28.2 ; 19.6] | 71 |
| G4 | 14.0 % [-19.3 ; 47.4] | 47 |
| G5 | -20.9 % [-72.6 ; 30.9] | 26 |

(b) Fatigue (dernier relevé du jour ou de la veille) et évaluation par minute dans le match, nos joueurs, ≥ 1 minute ; r de Pearson, IC de Fisher à 97.5 % ; effet minimal r = −0,3 ; n requis 103.

| groupe | r [IC] | p | n disponible (joueurs-matchs) | n requis | verdict |
|---|---|---|---|---|---|
| G1 | -0.01 [-0.32 ; 0.30] | 0.945 | 51 | 103 | n trop petit |
| G2 | -0.14 [-0.53 ; 0.29] | 0.460 | 29 | 103 | n trop petit |
| G3 | -0.01 [-0.64 ; 0.63] | 0.969 | 12 | 103 | n trop petit |
| G4 | -0.04 [-0.26 ; 0.17] | 0.654 | 107 | 103 | décidable : effet absent |
| G5 | 0.07 [-0.17 ; 0.29] | 0.525 | 94 | 103 | n trop petit |

Plage de fatigue observée (valeurs du relevé, échelle non documentée ; le skill cite des paliers 0, 20, 40, 60, 80) :

| groupe | minimum | médiane | maximum | écart-type | joueurs-matchs au-dessus de 10 |
|---|---|---|---|---|---|
| G1 | 0.00 | 11.72 | 24.63 | 5.62 | 33 |
| G2 | 0.00 | 1.95 | 8.84 | 2.88 | 0 |
| G3 | 0.00 | 0.00 | 0.47 | 0.17 | 0 |
| G4 | 0.18 | 6.47 | 24.63 | 6.51 | 30 |
| G5 | 0.17 | 0.57 | 8.84 | 1.80 | 0 |

Sensibilité (non retenue pour le verdict) : joueurs-matchs avec ≥ 10 minutes.

- G1 : r = -0.01 [-0.32 ; 0.30], n = 51
- G2 : r = -0.14 [-0.53 ; 0.29], n = 29
- G3 : r = -0.01 [-0.64 ; 0.63], n = 12
- G4 : r = -0.01 [-0.23 ; 0.21], n = 103
- G5 : r = 0.07 [-0.17 ; 0.29], n = 94

### Question 3 : rotation

Corrélation de l'écart « nous − eux » avec la marge ; IC de Fisher à 97.5 % ; effet minimal r = 0.4 ; n requis 56.

| groupe | mesure | r [IC] | p | n disponible | n requis | verdict |
|---|---|---|---|---|---|---|
| G1 | joueurs utilisés | 0.62 [0.21 ; 0.85] | 0.002 | 22 | 56 | n trop petit |
| G1 | part des minutes des 5 premiers | -0.70 [-0.88 ; -0.34] | 0.000 | 22 | 56 | n trop petit |
| G2 | joueurs utilisés | 0.92 [0.02 ; 1.00] | 0.026 | 5 | 56 | n trop petit |
| G2 | part des minutes des 5 premiers | -0.94 [-1.00 ; -0.12] | 0.019 | 5 | 56 | n trop petit |
| G3 | joueurs utilisés | -0.67 [-0.93 ; 0.04] | 0.036 | 10 | 56 | n trop petit |
| G3 | part des minutes des 5 premiers | 0.66 [-0.05 ; 0.93] | 0.036 | 10 | 56 | n trop petit |
| G4 | joueurs utilisés | 0.58 [0.02 ; 0.86] | 0.023 | 15 | 56 | n trop petit |
| G4 | part des minutes des 5 premiers | -0.77 [-0.93 ; -0.36] | 0.001 | 15 | 56 | n trop petit |
| G5 | joueurs utilisés | 0.64 [-0.09 ; 0.92] | 0.048 | 10 | 56 | n trop petit |
| G5 | part des minutes des 5 premiers | -0.64 [-0.92 ; 0.08] | 0.045 | 10 | 56 | n trop petit |

### Question 4 : tirs à 3 points

(i) Points par tir à 3 tenté moins points par tir à 2 tenté, moyenne des deux équipes par match ; t de Student, IC à 97.5 % ; effet minimal 0,10 ; n requis = ((z + z_β)·σ/0,10)².
(ii) Corrélation de l'écart « nous − eux » de la part de tirs à 3 avec la marge ; IC de Fisher ; effet minimal r = 0.4 ; n requis 56.

| groupe | mesure | effet [IC] | n disponible | n requis | verdict |
|---|---|---|---|---|---|
| G1 | (i) 3 pts − 2 pts par tir | -0.185 [-0.311 ; -0.059] pt/tir (σ 0.245) | 22 | 57 | n trop petit |
| G1 | (ii) part de tirs à 3 → marge | r = -0.73 [-0.89 ; -0.39] | 22 | 56 | n trop petit |
| G2 | (i) 3 pts − 2 pts par tir | -0.231 [-0.588 ; 0.125] pt/tir (σ 0.228) | 5 | 50 | n trop petit |
| G2 | (ii) part de tirs à 3 → marge | r = -0.55 [-0.98 ; 0.74] | 5 | 56 | n trop petit |
| G3 | (i) 3 pts − 2 pts par tir | -0.125 [-0.373 ; 0.122] pt/tir (σ 0.291) | 10 | 81 | n trop petit |
| G3 | (ii) part de tirs à 3 → marge | r = -0.59 [-0.91 ; 0.17] | 10 | 56 | n trop petit |
| G4 | (i) 3 pts − 2 pts par tir | -0.154 [-0.285 ; -0.023] pt/tir (σ 0.202) | 15 | 39 | n trop petit |
| G4 | (ii) part de tirs à 3 → marge | r = -0.16 [-0.67 ; 0.45] | 15 | 56 | n trop petit |
| G5 | (i) 3 pts − 2 pts par tir | -0.313 [-0.542 ; -0.085] pt/tir (σ 0.269) | 10 | 70 | n trop petit |
| G5 | (ii) part de tirs à 3 → marge | r = -0.19 [-0.78 ; 0.57] | 10 | 56 | n trop petit |

### Question 5 : avantage du terrain

(a) Marge domicile − extérieur, t de Student, IC à 97.5 % ; effet minimal 3 points ; n requis = ((z + z_β)·σ/3)². (b) Victoires à domicile contre 0,5, test binomial exact ; effet minimal 60 % ; n requis 236.

| groupe | mesure | effet [IC] ou taux | n disponible | n requis | verdict |
|---|---|---|---|---|---|
| G1 | (a) marge à domicile | 6.6 [-8.0 ; 21.2] pts (σ 28.3) | 22 | 848 | n trop petit |
| G1 | (b) victoires à domicile | 13 sur 22 (p exact 0.523) | 22 | 236 | n trop petit |
| G2 | (a) marge à domicile | -11.2 [-48.4 ; 26.0] pts (σ 23.8) | 5 | 598 | n trop petit |
| G2 | (b) victoires à domicile | 1 sur 5 (p exact 0.375) | 5 | 236 | n trop petit |
| G3 | (a) marge à domicile | -7.5 [-23.0 ; 8.0] pts (σ 18.3) | 10 | 353 | n trop petit |
| G3 | (b) victoires à domicile | 3 sur 10 (p exact 0.344) | 10 | 236 | n trop petit |
| G4 | (a) marge à domicile | 1.7 [-9.4 ; 12.8] pts (σ 17.1) | 15 | 311 | n trop petit |
| G4 | (b) victoires à domicile | 8 sur 15 (p exact 1.000) | 15 | 236 | n trop petit |
| G5 | (a) marge à domicile | 4.7 [-17.8 ; 27.2] pts (σ 26.5) | 10 | 742 | n trop petit |
| G5 | (b) victoires à domicile | 4 sur 10 (p exact 0.754) | 10 | 236 | n trop petit |

### Question 6 : points de différence par point de force d'équipe (ligue seulement)

Écart de `club_strength` (dernier relevé ≤ jour du match) et marge ; r de Pearson, IC de Fisher à 95 % ; effet minimal r = 0.5 ; n requis 30.

| groupe | r [IC] | pente (points de marge par point de force) [IC] | n disponible / matchs du groupe | n requis | verdict |
|---|---|---|---|---|---|
| G1 | — | — | 4 / 22 | 30 | n < 5 : aucun calcul |
| G2 | 0.92 [0.18 ; 0.99] | 17.61 [3.48 ; 31.73] | 5 / 5 | 30 | n trop petit |

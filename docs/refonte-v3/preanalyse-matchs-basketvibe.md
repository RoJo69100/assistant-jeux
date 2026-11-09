# Préanalyse des matchs BasketVibe : que peut-on apprendre du moteur avant de demander de nouveaux exports ?

Écrit le 2026-11-09. Lecture seule (aucune écriture en base), requêtes par `python -I pipelines/sql.py`. Les moteurs v3, v4 et v5, la ligue, la coupe et les amicaux ne sont jamais mélangés.

## Synthèse : tableau question / n disponible / n requis / verdict / décision possible

Moteur actuel de la ligue = v4 (G2). Les nombres sont des matchs (question 2 : joueurs-matchs). Détail, intervalles et autres groupes : étape 3 et `docs/refonte-v3/preanalyse-matchs-basketvibe-sortie.md`.

| # | Question | n disponible : ligue v4 (G2) ; meilleur autre groupe | n requis | Verdict | Décision possible aujourd'hui |
|---|---|---|---|---|---|
| 1 | Ce qui sépare victoires et défaites (eFG, rebonds offensifs, pertes de balle, lancers francs) | 5 ; 22 en ligue v3 (G1, historique) | 40 | n trop petit | Aucune. Indice v3 : eFG r = 0,92 [0,77 ; 0,97] (presque tautologique : un tir réussi est un point), rebonds offensifs 0,77 [0,42 ; 0,92], pertes de balle −0,59 [−0,85 ; −0,10], lancers francs 0,18 [−0,37 ; 0,64] |
| 2a | Minutes lourdes (≥ 27 min avant le Q4) : évaluation par minute au Q4 | 13 ; 32 en amical v4 (G4) | 783 (σ de G2) ; 190 (σ de G4) | n trop petit | Aucune. Indice, amical v4 : −56,6 % [−84,5 ; −28,7] contre +14,0 % [−19,3 ; 47,4] pour les joueurs moins sollicités |
| 2b | Fatigue du matin et évaluation par minute (nos joueurs) | 29 ; 107 en amical v4 (G4) | 103 | Ligue v4 : n trop petit. **Amical v4 : décidable, effet absent** | Amical v4 seulement : r = −0,04 [−0,26 ; 0,17] pour une fatigue de 0,18 à 24,6 : un effet de corrélation d'au moins 0,3 est écarté dans cette plage |
| 3 | Rotation (joueurs utilisés, minutes des cinq premiers) | 5 ; 15 en amical v4 | 56 | n trop petit | Aucune. Signe opposé en coupe v4 (joueurs utilisés −0,67, contre +0,58 à +0,92 dans les autres groupes) ; un match déjà gagné vide le banc (cause inverse) |
| 4 | Tirs à 3 points : (i) points par tir à 3 moins par tir à 2 ; (ii) part de tirs à 3 contre marge | 5 ; 22 en ligue v3 | (i) 50 (σ de G2) ; (ii) 56 | n trop petit | Aucune. Indice : (i) négatif dans les 5 groupes (−0,13 à −0,31 point par tir) |
| 5 | Avantage du terrain | 5 ; 22 en ligue v3 | (a) 598 (σ de G2) ; (b) 236 | n trop petit | Aucune, et hors de portée en ligue v4 cette saison (132 matchs au total) |
| 6 | Points de marge par point de force d'équipe | 5 sur 5 ; 4 sur 22 en ligue v3 (force connue dès le 18/10) | 30 | n trop petit (ligue v3 : n < 5, aucun calcul) | Aucune. La force d'équipe de la base (`club_strength`) n'est pas la PS : à ne pas utiliser pour un achat |

**Lecture honnête** : sur six questions, une seule est décidable (2b, amical v4, effet absent dans une plage de fatigue étroite). Les indices des questions 1 à 4 n'atteignent pas le n requis fixé avant le calcul ; seul l'indice des minutes lourdes (2a) va dans le sens d'une annonce du moteur (fatigue plus punitive en v4), sans en être une preuve.

## Étape 1 : inventaire

### 1.1 Version du moteur : aucune colonne, déduite des dates
Aucune page de match ne porte de champ de version. La version est déduite des annonces du skill `basketvibe-communaute` (`references/02-1-moteur-de-match-versions-et-calibrage.md`) : ligue en v3 jusqu'au 26/10 (dernière journée de la saison 1) ; amicaux en v4 dès le 11/10 ; v4 « actif en ligue, coupe et amical depuis le 27/10 » ; v5 en amical seulement depuis le 28/10 (déploiement dans tous les matchs sans date). Règle appliquée (écrite avant tout calcul) :

| Compétition | Dates | Moteur retenu |
|---|---|---|
| Ligue | jusqu'au 26/10 (saison 1) | v3 |
| Ligue | dès le 02/11 (saison 2) | v4 |
| Coupe | 28/10 à 31/10 | v4 |
| Amical | 10/10 | v3 (veille de l'annonce) |
| Amical | 11/10 au 27/10 | v4 |
| Amical | dès le 28/10 | v5 |

Incertitude : la date exacte de bascule des amicaux (10/10 et 11/10, 27/10 et 28/10) vient de textes de la communauté et des annonces, pas d'une mesure en base. Un match à la date frontière peut être mal classé : ils sont listés à part au besoin.

### 1.2 Matchs par groupe (moteur, compétition, équipe), détail disponible
Requête (sortie ci-dessous) : voir `Annexe A`. Seuls les matchs `finished` de `silver.bv_matches` sont comptés.

| Moteur | Compétition | Équipe | Matchs | Période | Adversaires distincts | Box score par joueur et par quart | Play-by-play | Composition de début de quart | Réglages tactiques lisibles |
|---|---|---|---|---|---|---|---|---|---|
| v3 | ligue | nous | 22 | 07/09 au 26/10 | 11 | 22 (les 2 équipes) | 22 | 22 : la nôtre et celle de l'adversaire | 22 : les nôtres |
| v3 | amical | nous | 1 | 10/10 | 1 | 1 | 1 | 1 : les deux | 1 : les nôtres |
| v4 | ligue | nous | 3 | 02/11 au 07/11 | 3 | 3 | 3 | 3 : les deux | 3 : les nôtres |
| v4 | ligue | autres équipes | 2 | 02/11 au 04/11 | non applicable | 2 (les 2 équipes) | 2 | absente | absents |
| v4 | coupe | nous | 2 | 28/10 au 30/10 | 2 | 2 | 2 | 1 sur 2 | 1 sur 2 : les nôtres |
| v4 | coupe | autres équipes | 8 | 28/10 au 31/10 | non applicable | 8 (les 2 équipes) | 8 | absente | absents |
| v4 | amical | nous | 16 | 11/10 au 27/10 | 16 | 16 (15 avec les 2 équipes) | 16 | 14 sur 16 : les deux | 14 sur 16 : les nôtres |
| v5 | amical | nous | 10 | 29/10 au 08/11 | 10 | 10 | 10 | 9 sur 10 : les deux | 9 sur 10 : les nôtres |
| Total | | | 64 | 07/09 au 08/11 | 56 équipes en tout dans `bv_matches` (07/09 au 09/11) | 64 | 64 | 50 | 50 |

Matchs sans détail (score seul) : saison 1, ligue, 242 matchs des autres équipes (`silver.bv_fixtures`, aucun dans `silver.bv_matches`) ; saison 2, ligue, 8 matchs terminés des autres équipes sur 10 ; 120 matchs de ligue de la saison 2 programmés. Un match « score seul » ne sert à aucune des six questions.

### 1.3 Ce que contient chaque niveau de détail
- **Score et quarts-temps** : `quarter_scores` pour les 64 matchs (points domicile et extérieur par quart).
- **Box score par joueur** (`silver.bv_match_player_stats`) : les deux équipes, une ligne par joueur et par période (0 = match entier, 1 à 4 = quarts) : minutes, points, tirs à 2/3/LF réussis et tentés, rebonds offensifs et défensifs, passes, interceptions, contres, pertes de balle, fautes, +/-, évaluation. Pas de fatigue ni de forme du joueur dans le box score.
- **Play-by-play** (`silver.bv_match_events`) : 64 matchs, 27 236 événements (somme de la requête 4 ; tirs réussis et manqués, rebonds, fautes, pertes de balle, passes, lancers, remplacements pour 39 matchs, blessures pour 13 matchs, entre-deux). Coordonnées de tir (`shot_x`, `shot_y`) disponibles.
- **Composition de début de quart** (`silver.bv_match_tactics`) : `lineup_by_quarter` (la nôtre) et `opponent_lineup_by_quarter` (celle de l'adversaire), les deux équipes, 50 matchs dont 3 de ligue v4.
- **Réglages tactiques** : les nôtres seulement. `defensive_focus` (focus défensif par joueur adverse), `player_directives` (rôle, niveau de tir, focus offensif, niveau de défense de chaque joueur). Ceux de l'adversaire : **non lisibles** (on ne voit que sa composition et ce qu'il a fait en match).
- **Fatigue, forme, PS des joueurs** : `silver.bv_player_daily` (18 joueurs à nous, 287 lignes, 16/10 au 08/11) ; PS de l'adversaire : non lisible. Force d'équipe des autres clubs : `club_strength` de `silver.bv_standings_weekly` (31 équipes, 67 lignes, 18/10 au 08/11 seulement : rien avant le 18/10).

## Étape 2 : critères (écrits le 2026-11-09 avant tout calcul sur les matchs)

### 2.1 Règles communes
- **Groupes** (jamais mélangés) : G1 ligue v3 (nous) ; G2 ligue v4 (nous et autres équipes) ; G3 coupe v4 (nous et autres) ; G4 amical v4 ; G5 amical v5. Le seul amical v3 (1 match) n'est pas analysé. La ligue v3 ne décrit pas le moteur actuel (fatigue et duels changés en v4) : son verdict est dit « historique, non transférable ».
- **Unité** : le match (une ligne par match) pour les questions 1, 3, 4, 5, 6 ; le couple joueur-match pour la question 2. Pour les matchs des autres équipes (box score des deux côtés, sans réglages), le côté « nous » est le côté domicile.
- **Seuils** : risque α = 0,05 par question (partagé en Bonferroni quand une question a plusieurs tests : α par test indiqué), puissance 80 % (β = 0,20), tests bilatéraux. z(0,975) = 1,960 ; z(0,9875) = 2,241 ; z(0,99375) = 2,498 ; z(0,80) = 0,842.
- **n requis** : pour une corrélation r, `n = ((z_α + z_β) / atanh(r))² + 3` (transformation de Fisher) ; pour une moyenne, `n = ((z_α + z_β) · σ / δ)²` avec σ = écart-type observé de la mesure dans le groupe (« variance observée », mesuré à l'étape 3, jamais choisi) ; pour une proportion contre 0,5, formule exacte du test binomial approchée par `n = ((z_α·0,5 + z_β·√(p(1−p))) / (p − 0,5))²`.
- **Verdict** : « décidable » si n disponible ≥ n requis ; alors l'effet est dit *présent* (intervalle de confiance à 95 % entièrement du même côté de 0 et |effet| ≥ effet minimal), *absent* (intervalle inclus dans ±effet minimal) ou *entre les deux*. Sinon « n trop petit » : l'effet et son intervalle sont donnés pour information, sans conclusion. **n disponible < 5 : aucun effet n'est calculé.**
- **Effets minimaux** : ils sont fixés par ce qu'il faudrait pour changer une décision, pas par ce que les données suggèrent. Aucun n'est une règle du jeu.

### 2.2 Les six questions

| # | Mesure | Test | Effet minimal et pourquoi | n requis |
|---|---|---|---|---|
| 1 | Pour chaque match : écart « nous − eux » des quatre facteurs (eFG % = (réussis + 0,5 × réussis à 3) / tentés ; rebonds offensifs en % = ORB / (ORB + DRB adverse) ; pertes de balle en % = TOV / (tentés + 0,44 × LF tentés + TOV) ; lancers francs tentés par tir tenté) et marge du match (nous − eux) ; ligue seulement. Description en plus : moyenne de chaque facteur en victoire et en défaite. | Corrélation de Pearson de l'écart de chaque facteur avec la marge, intervalle de Fisher. 4 tests : α = 0,0125 par test. | r = 0,5 (effet « large » : en dessous, un facteur n'oriente pas une tactique) | **40** (r = 0,5 ; α = 0,0125 ; puissance 80 %) |
| 2 | (a) Pour chaque joueur-match avec au moins 3 quarts joués et au moins 27 minutes cumulées avant le Q4 (minutes lourdes ; le moteur pénalise au-delà de 36 minutes) : évaluation par minute au Q4 contre sa moyenne des Q1 à Q3 (différence relative). (b) Fatigue du joueur le matin du match (dernier relevé de `bv_player_daily` du jour ou la veille) et évaluation par minute dans le match, nos joueurs seulement. | (a) t apparié sur les joueurs-matchs. (b) Corrélation de Pearson, intervalle de Fisher. 2 tests : α = 0,025 par test. | (a) −15 % de l'évaluation par minute, l'ordre de grandeur de l'effet annoncé d'une fatigue de 40 (−15 %, skill `basketvibe-tactique`, V-20261027-1). (b) r = −0,3 | (a) `((2,241 + 0,842) · σ / 0,15)²` avec σ = écart-type observé de la différence relative ; (b) **103** pour r = 0,3 et α = 0,025 |
| 3 | Pour chaque match : écart « nous − eux » (i) du nombre de joueurs utilisés (au moins 1 minute) et (ii) de la part des minutes jouées par les cinq joueurs qui jouent le plus ; et marge du match. | Corrélation de Pearson de chaque écart avec la marge. 2 tests : α = 0,025 par test. | r = 0,4 (un rotation qui expliquerait 16 % de la marge) | **56** (r = 0,4 ; α = 0,025) |
| 4 | (i) Pour chaque match et chaque équipe : points par tir à 3 tenté (3 × réussite à 3) moins points par tir à 2 tenté (2 × réussite à 2). (ii) Écart « nous − eux » de la part de tirs à 3 (3PA / FGA) et marge du match. | (i) t à un échantillon (moyenne de la différence contre 0). (ii) Corrélation de Pearson. 2 tests : α = 0,025 par test. | (i) 0,10 point par tir : déplacer 20 tirs de 2 vers 3 rapporte 2 points par match, le plus petit gain qui changerait la répartition. (ii) r = 0,4 | (i) `((2,241 + 0,842) · σ / 0,10)²` avec σ observé de la différence par match ; (ii) **56** |
| 5 | Pour chaque match : marge de l'équipe qui reçoit (points domicile − points extérieur) ; victoire de l'équipe qui reçoit (oui / non). Tous les matchs du groupe, nos matchs et ceux des autres équipes. | (a) t à un échantillon de la marge contre 0. (b) test binomial exact du taux de victoire à domicile contre 0,5. 2 tests : α = 0,025 par test. | (a) 3 points de marge (avec un écart-type de la marge proche de 12, 3 points valent environ 60 % de victoires). (b) taux de victoire de 60 % contre 50 % | (a) `((2,241 + 0,842) · σ / 3)²` avec σ observé de la marge ; (b) **236** (p = 0,6 ; α = 0,025 ; puissance 80 %) |
| 6 | Pour chaque match de ligue : écart de force d'équipe « nous − eux » (`club_strength` du dernier relevé de `bv_standings_weekly` avant le match ; proxy de l'écart de PS d'équipe, ce que la colonne mesure exactement n'est pas documenté) et marge du match. Pente de la droite (points de marge par point d'écart de force). | Corrélation de Pearson et pente par moindres carrés, intervalle de Fisher et intervalle de la pente. 1 test : α = 0,05. | r = 0,5 | **30** (r = 0,5 ; α = 0,05 ; puissance 80 %) |

Calcul des n requis fixes (Fisher, `n = ((z_α + z_β)/atanh(r))² + 3`, arrondi à l'entier supérieur, vérifié par un calcul Python avant tout calcul sur les matchs : première version erronée à la main, corrigée) : Q1 39,96 → **40** ; Q2(b) 102,22 → **103** ; Q3 et Q4(ii) 55,96 → **56** ; Q6 29,01 → **30** ; Q5(b) (binomial, p = 0,6) 235,01 → **236**.

### 2.3 Limites connues avant calcul
- Question 6 : les relevés de `club_strength` commencent le 18/10 : les 18 premiers matchs de la ligue v3 (du 07/09 au 17/10) n'ont pas de force d'équipe ; leur n disponible est donc plus petit que 22.
- Question 2(b) : 18 joueurs et 287 relevés quotidiens depuis le 16/10 ; les matchs avant le 16/10 n'ont pas de fatigue connue.
- Questions 1, 3, 4 : la marge d'un match dépend de la force des deux équipes ; l'écart de facteur la reflète en partie (corrélation, pas causalité). La question 6 est la seule à contrôler la force.
- Les matchs successifs de la même équipe (les nôtres) ne sont pas indépendants (même effectif, même tactique) : les intervalles sont plus étroits qu'ils ne devraient ; le verdict « décidable » est donc un minimum à exiger, pas une garantie.
- La version du moteur par date est une déduction (§ 1.1).

### 2.4 Complément du 2026-11-09 : questions 5 et 6 sur les matchs à score seul (critères écrits avant tout calcul)
Les 242 matchs de ligue de la saison 1 des autres équipes n'ont pas de box score mais ont un score (`silver.bv_fixtures`) : ils servent les questions 5 et 6, qui ne demandent que le score. Contrôle de qualité fait avant les critères : 264 matchs terminés, aucun score absent, aucun nul, aucun score nul à zéro. Les 264 matchs viennent de 24 équipes (deux divisions de 12, 12 matchs par journée, 22 journées du 07/09 au 26/10), moteur v3. Les deux divisions sont poolées (même moteur).

| # | Mesure et population | Test | Effet minimal | n requis |
|---|---|---|---|---|
| 5' | Matchs de ligue de la saison 1 (`season_id = 8fa19101-…`), `status = 'finished'`, scores présents ; nos matchs et ceux des autres équipes. (a) Victoire de l'équipe qui reçoit (oui / non) ; (b) marge de l'équipe qui reçoit (points domicile − points extérieur). | (a) test binomial exact bilatéral du taux de victoires à domicile contre 0,5 ; (b) t de Student de la moyenne de la marge contre 0, intervalle à 97,5 %. 2 tests : α = 0,025 par test. | (a) 60 % contre 50 % ; (b) 3 points | (a) **236** (déjà fixé, § 2.2) ; (b) `((2,241 + 0,842) · σ / 3)²` avec σ = écart-type de la marge **mesuré sur ce groupe** |
| 6' | Force d'une équipe à la date d'un match = moyenne, sur ses matchs terminés de la même saison dont le jour est **strictement antérieur** à celui du match, de (points marqués − points encaissés) ; **au moins 3 matchs antérieurs** pour chacune des deux équipes (même seuil que le test de prédiction du journal, `MIN_PRECEDENTS = 3` de `pipelines/palier5_test.py`). Écart de force = force du domicile − force de l'extérieur ; marge = points domicile − points extérieur. | Pente des moindres carrés de la marge sur l'écart de force (intervalle de Student), et corrélation de Pearson avec intervalle de Fisher. 1 test : α = 0,05. | r = 0,5 | **30** (déjà fixé, § 2.2) |

Règles : le verdict suit § 2.1 (n disponible ≥ n requis pour « décidable »). La population de 6' est l'ensemble des matchs pour lesquels les deux équipes ont au moins 3 matchs antérieurs.

**Limites écrites avant calcul**
- Moteur v3 : résultat **historique, non transférable** à la ligue actuelle (v4 : fatigue et duels changés) ni aux amicaux v5.
- 5' : chaque paire d'équipes se rencontre à domicile et à l'extérieur (double ronde) : la différence de force entre équipes s'annule en moyenne dans la marge domicile − extérieur, sans quoi la mesure ne vaudrait rien ; la compétition (ligue, saison 1) est la seule à avoir ce plan.
- 6' : la force est une moyenne de marges, non corrigée de la force des adversaires déjà rencontrés (aucun ajustement) ; la pente attendue d'une force parfaitement connue n'est pas 1 (régression vers la moyenne) ; la marge du match inclut l'avantage du terrain, qui ne change pas la pente si l'écart de force est symétrique.
- Les matchs d'une même équipe ne sont pas indépendants : les intervalles sont plus étroits qu'ils ne devraient.

## Étape 3 : calculs (script `pipelines/preanalyse_matchs_basketvibe.py`, rejouable, 8 s)

Commande : `python -I pipelines/preanalyse_matchs_basketvibe.py --sensibilite`. Sortie complète collée en annexe C (et dans `preanalyse-matchs-basketvibe-sortie.md`). Matchs analysés (box score des deux côtés) : G1 ligue v3 22 ; G2 ligue v4 5 (3 à nous, 2 des autres) ; G3 coupe v4 10 (2 à nous, 8 des autres) ; G4 amical v4 15 ; G5 amical v5 10 (un amical v4 sans les deux côtés est écarté).

**Verdict par question et par groupe** (effet, intervalle, n disponible contre n requis : tableaux de l'annexe C) :
- **Question 1** (ligue) : G1 et G2 « n trop petit » (22 et 5 contre 40) pour les quatre facteurs.
- **Question 2(a)** : « n trop petit » partout (13 à 116 joueurs-matchs contre 190 à 783).
- **Question 2(b)** : G1 51, G2 29, G3 12, G5 94 : « n trop petit » ; **G4 107 contre 103 : décidable, effet absent** (r = −0,04 [−0,26 ; 0,17]).
- **Questions 3 et 4(ii)** : « n trop petit » partout (5 à 22 contre 56).
- **Question 4(i)** : « n trop petit » partout (5 à 22 contre 39 à 81).
- **Question 5** : « n trop petit » partout (5 à 22 contre 311 à 848 pour la marge, 236 pour les victoires).
- **Question 6** : G1 : n = 4 (force d'équipe connue seulement dès le 18/10) : aucun calcul ; G2 : 5 sur 5, « n trop petit ».

**Lectures à garder en tête avant d'utiliser un chiffre**
- Le critère écrit avant calcul dit « n trop petit » même quand l'intervalle exclut déjà l'effet minimal. Exemple : eFG en ligue v3, r = 0,92 [0,77 ; 0,97] avec n = 22 contre 40. Ce chiffre est un indice, pas un verdict ; de plus, l'eFG contient les tirs réussis, donc les points : la corrélation avec la marge est presque tautologique.
- Question 2(a), contrôle hors critères : les joueurs qui jouent 5 à 26 minutes avant le Q4 ne baissent pas au Q4 (G1 −1,3 % [−25,3 ; 22,7] ; G4 +14,0 % [−19,3 ; 47,4]). La baisse des joueurs lourds en amical v4 (−56,6 % [−84,5 ; −28,7], n = 32) et v5 (−43,4 % [−89,9 ; 3,2], n = 24) n'est donc pas un simple effet « le Q4 est plus faible pour tout le monde », mais l'échantillon est petit (190 à 382 requis) et l'écart-type relatif est de 0,7 à 1,4. En ligue v3 : −4,4 % [−27,8 ; 19,1] (n = 116), ce qui va dans le sens de l'annonce « fatigue plus punitive en v4 » ([News 2026-10-17], skill `basketvibe-communaute`) ; ce n'est pas une preuve.
- Question 2(b) : l'échelle de la fatigue du relevé quotidien n'est pas documentée ; plage observée en amical v4 : 0,18 à 24,63 (médiane 6,47 ; 30 joueurs-matchs au-dessus de 10). En coupe v4 (maximum 0,47) et en amical v5 (maximum 8,84), la plage est trop étroite pour tester quoi que ce soit. « Effet absent » ne vaut que dans la plage observée : les effets annoncés par le moteur (−4 % à une fatigue de 20, −15 % à 40) sont de toute façon trop petits pour être vus avec r ≥ 0,3.
- Question 5 : l'écart-type de la marge est de 17 à 28 points ; il faudrait 311 à 848 matchs pour mesurer 3 points. Les 22 matchs de la ligue v3 sont tous les nôtres : la marge « domicile − extérieur » mélange l'avantage du terrain et l'écart de force entre nous et chaque adversaire.
- Question 6 : `club_strength` est un proxy de la force d'équipe dont la définition n'est pas documentée ; la pente en ligue v4 (17,6 points de marge par point de force, [3,5 ; 31,7], 5 matchs) est trop grande pour être crédible sur une étendue de force de 50,8 à 58,4.
- Questions 1, 3, 4 : corrélations entre un écart de statistique et la marge du même match ; elles ne disent pas ce qui cause la victoire (un match gagné d'avance fait jouer le banc, et une équipe qui perd tire plus à 3 points).

## Étape 4 : conclusions

### (a) Décisions que l'historique permet déjà
1. **Une seule, limitée aux amicaux v4** : une fatigue du matin dans la plage 0,18 à 24,6 n'explique pas la performance du joueur dans le match (question 2(b), r = −0,04 [−0,26 ; 0,17], n = 107 ≥ 103). Décision : en amical v4, ne pas sortir un joueur du cinq pour la seule raison d'une fatigue du matin dans cette plage. Elle ne dit rien de la ligue, du v5, ni d'une fatigue supérieure à 25.
2. **Rien d'autre.** Aucune décision de tactique, de minutes ou d'achat n'est décidable au sens du critère. Les indices non décisifs, à ne pas traiter comme des règles :
   - minutes lourdes : −56,6 % [−84,5 ; −28,7] au Q4 pour les joueurs de plus de 27 minutes avant le Q4 (amical v4, 32 joueurs-matchs) ;
   - tirs à 3 points : un tir à 3 rapporte moins de points qu'un tir à 2 dans les cinq groupes (−0,185 [−0,311 ; −0,059] en ligue v3, −0,154 [−0,285 ; −0,023] en amical v4, −0,313 [−0,542 ; −0,085] en amical v5 ; intervalles contenant 0 en ligue v4 et en coupe v4) ;
   - aucun indice utilisable pour un achat : la pente de la force d'équipe repose sur 5 matchs et sur une grandeur qui n'est pas la PS.

### (b) Matchs détaillés manquants par question non décidable (ligue v4, le moteur actuel)
Capacité : une journée de ligue compte 6 matchs, 3 journées par semaine (lundi, mercredi, samedi) ; 132 matchs de ligue au total dans la saison 2, 12 terminés, 5 avec détail. Retard immédiat : 8 matchs terminés d'autres équipes sans box score. Les n requis des questions 2(a), 4(i) et 5(a) utilisent l'écart-type de G2 (5 matchs, peu fiable) : ils sont à recalculer à chaque ajout.

| Question | n requis | n disponible (ligue v4) | Manque | En journées de ligue complètes (6 matchs) après le retard de 8 |
|---|---|---|---|---|
| 1 facteurs | 40 matchs | 5 | 35 | 5 |
| 3 rotation ; 4(ii) tirs à 3 | 56 matchs | 5 | 51 | 8 |
| 4(i) points par tir | 50 matchs (σ de G2) | 5 | 45 | 7 |
| 6 force d'équipe | 30 matchs | 5 | 25 | 3 |
| 2(b) fatigue | 103 joueurs-matchs de nos joueurs | 29 | 74, soit environ 8 de nos matchs (9,7 joueurs-matchs par match) | non applicable (nos matchs seulement) : environ 3 semaines |
| 2(a) minutes lourdes | 783 joueurs-matchs (σ de G2), 190 avec le σ de G4 | 13 | de 177 à 770, soit de 55 à 237 matchs (3,25 joueurs-matchs par match en ligue v4) | hors de portée avec un σ de G2 ; 8 journées avec le σ de G4 |
| 5 avantage du terrain | 236 victoires ; de 311 à 848 matchs pour la marge selon le groupe (σ de G2 : 598) | 5 | plus que les 132 matchs de la saison | hors de portée en ligue v4 cette saison |

Équipes dont il faut les matchs, dans l'ordre demandé :
1. **Les prochains adversaires** : Naked Spartans (journée 4, 09/11), BC KIT (journée 5, 11/11), BC Gelrode (journée 6, 14/11) ont chacun 2 matchs terminés sans box score en base (6 matchs au plus, certains peuvent être le même match entre deux d'entre eux). Póvoa Riptide, dernier adversaire, a déjà ses matchs en base.
2. **Les meilleures équipes** : Žirmūnai (2e, 3 victoires en 3) et Eindhoven Wizards (3e, 3 victoires en 3), puis Águias do Guadiana (5e).
3. **Le reste de la ligue** : les autres matchs des 12 équipes, jusqu'à compléter les 8 matchs de retard puis chaque journée jouée.
Rappel : seules des pages de match exportées par l'utilisateur entrent en base (inviolable 1), et les box scores des autres équipes existent déjà pour 10 matchs (8 de coupe, 2 de ligue) : une page de match d'une autre équipe suffit, sans réglage tactique.

### (c) Ce que les données ne montrent pas
- **Les réglages tactiques de l'adversaire** (focus, rôles, niveaux de tir) : seuls les nôtres sont lisibles ; l'adversaire n'apparaît que par sa composition de début de quart et par ses actions.
- **Les compositions des autres équipes** dans leurs matchs entre elles : absentes (les tactiques sont lues sur nos matchs seulement).
- **La PS et la fatigue des joueurs adverses** : absentes ; la force d'équipe (`club_strength`) n'existe qu'à partir du 18/10 et sa définition n'est pas documentée.
- **La version du moteur par match** : déduite des dates, jamais lue en base ; les matchs à la frontière (10-11/10 et 27-28/10 en amical) peuvent être mal classés.
- **La cause** : toutes les mesures sont des corrélations entre statistiques d'un même match ; un match gagné d'avance (banc, tirs à 3 en fin de match) renverse le sens apparent des questions 3 et 4.
- **L'indépendance** : les matchs de notre équipe partagent effectif, tactique et adversaires déjà vus ; les joueurs d'un même match ne sont pas indépendants : les intervalles sont trop étroits.
- **Les minutes réellement jouées dans le quart** au-delà du box score (entrées et sorties) : le play-by-play contient 123 remplacements seulement, pour 39 matchs.
- **Aucune des six questions ne dit comment acheter** : pas de lien mesuré entre une compétence achetée et un résultat.

## Annexe A : sorties collées de l'étape 1

Requête 1 (matchs par saison, compétition, statut) : `select season_id, competition, status, (my_side is not null) mien, count(*) n, min(match_day) du, max(match_day) au from silver.bv_matches group by 1,2,3,4 order by 1,2,3,4`

```
| saison (début) | compétition | statut | mien | n | du | au |
| 86a63498 | cup | finished | False | 8 | 2026-10-28 | 2026-10-31 |
| 86a63498 | cup | finished | True | 2 | 2026-10-28 | 2026-10-30 |
| 86a63498 | cup | scheduled_lineups | True | 2 | 2026-10-29 | 2026-10-31 |
| 86a63498 | friendly | finished | True | 11 | 2026-10-27 | 2026-11-08 |
| 86a63498 | friendly | scheduled_lineups | True | 1 | 2026-11-09 | 2026-11-09 |
| 86a63498 | league | finished | False | 2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | league | finished | True | 3 | 2026-11-02 | 2026-11-07 |
| 86a63498 | league | scheduled_lineups | True | 1 | 2026-11-09 | 2026-11-09 |
| 8fa19101 | friendly | finished | True | 16 | 2026-10-10 | 2026-10-26 |
| 8fa19101 | league | finished | True | 22 | 2026-09-07 | 2026-10-26 |
```

Requête 2 (inventaire final par moteur, compétition, équipe) : texte exact en `Annexe B`. Sortie :

```
| moteur | competition | equipe | matchs | du | au | adversaires_distincts | box | box_2cotes | pbp | lineups_nous | lineups_adv |
| v3 | friendly | nous | 1 | 2026-10-10 | 2026-10-10 | 1 | 1 | 1 | 1 | 1 | 1 |
| v3 | league | nous | 22 | 2026-09-07 | 2026-10-26 | 11 | 22 | 22 | 22 | 22 | 22 |
| v4 | cup | autres | 8 | 2026-10-28 | 2026-10-31 | 0 | 8 | 8 | 8 |  |  |
| v4 | cup | nous | 2 | 2026-10-28 | 2026-10-30 | 2 | 2 | 2 | 2 | 1 | 1 |
| v4 | friendly | nous | 16 | 2026-10-11 | 2026-10-27 | 16 | 16 | 15 | 16 | 14 | 14 |
| v4 | league | autres | 2 | 2026-11-02 | 2026-11-04 | 0 | 2 | 2 | 2 |  |  |
| v4 | league | nous | 3 | 2026-11-02 | 2026-11-07 | 3 | 3 | 3 | 3 | 3 | 3 |
| v5 | friendly | nous | 10 | 2026-10-29 | 2026-11-08 | 10 | 10 | 10 | 10 | 9 | 9 |
```

Requête 3 (matchs sans détail) : `select f.season_id, f.is_mine, f.status, count(*) fixtures, count(m.fixture_id) dans_matches, min(f.match_day) du, max(f.match_day) au from silver.bv_fixtures f left join silver.bv_matches m using (fixture_id) group by 1,2,3 order by 1,2,3`

```
| 86a63498 | False | finished  |  10 |  2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | False | scheduled | 100 |  0 | 2026-11-07 | 2026-12-21 |
| 86a63498 | True  | finished  |   2 |  2 | 2026-11-02 | 2026-11-04 |
| 86a63498 | True  | scheduled |  20 |  2 | 2026-11-07 | 2026-12-21 |
| 8fa19101 | False | finished  | 242 |  0 | 2026-09-07 | 2026-10-26 |
| 8fa19101 | True  | finished  |  22 | 22 | 2026-09-07 | 2026-10-26 |
```

Requête 4 (play-by-play par type d'événement) : `select kind, count(*) n, count(distinct fixture_id) matchs from silver.bv_match_events group by 1 order by 2 desc` : miss 6 057, dreb 4 495, fg2 3 704, ft 3 062, foul 2 173, turnover 2 132, assist 1 886, oreb 1 475, fg3 1 148, dead_ball 373, period_end 256, period_start 256, substitution 123 (39 matchs), jump_ball 64, endgame 16, injury 16 (13 matchs). 64 matchs partout sauf mention.

Requête 5 (périodes du box score) : `select period, count(*) lignes, count(distinct fixture_id) matchs from silver.bv_match_player_stats group by 1 order by 1` : périodes 0 à 4, 1 704 lignes et 64 matchs chacune.

Requête 6 (équipes et période) : `select count(distinct team_id) eq, min(match_day), max(match_day) from (select home_team_id team_id, match_day from silver.bv_matches union all select away_team_id, match_day from silver.bv_matches) x` : 56 équipes, du 2026-09-07 au 2026-11-09.

Requête 7 (force d'équipe et fatigue) : `select count(*) n, count(distinct team_id) eq, min(day) du, max(day) au from silver.bv_standings_weekly` : 67 lignes, 31 équipes, 18/10 au 08/11. `select count(*) n, count(distinct player_id) joueurs, min(day) du, max(day) au from silver.bv_player_daily` : 287 lignes, 18 joueurs, 16/10 au 08/11.

## Annexe B : requête d'inventaire

```sql
with m as (
  select fixture_id, competition, (my_side is not null) mien, match_day, season_id, home_team_id, away_team_id, my_side,
    case when competition='league' and match_day <= '2026-10-26' then 'v3'
         when competition='friendly' and match_day <= '2026-10-10' then 'v3'
         when competition='friendly' and match_day >= '2026-10-28' then 'v5'
         else 'v4' end moteur
  from silver.bv_matches where status='finished'),
ps as (select fixture_id, count(distinct team_side) cotes from silver.bv_match_player_stats group by 1),
ev as (select distinct fixture_id from silver.bv_match_events),
tc as (select fixture_id, bool_or(lineup_by_quarter is not null) lu, bool_or(opponent_lineup_by_quarter is not null) lo from silver.bv_match_tactics group by 1)
select moteur, competition, case when mien then 'nous' else 'autres' end equipe, count(*) matchs, min(match_day) du, max(match_day) au,
  count(distinct case when mien then (case when my_side='home' then away_team_id else home_team_id end) end) adversaires_distincts,
  count(ps.fixture_id) box, sum((ps.cotes=2)::int) box_2cotes, count(ev.fixture_id) pbp, sum(tc.lu::int) lineups_nous, sum(tc.lo::int) lineups_adv
from m left join ps using (fixture_id) left join ev using (fixture_id) left join tc using (fixture_id)
group by 1,2,3 order by 1,2,3
```

## Annexe C : sortie complète du script (étape 3)

Commande : `python -I pipelines/preanalyse_matchs_basketvibe.py --sensibilite` (8 s, code 0), le 2026-11-09. Les titres de la sortie sont descendus d'un niveau.

#### Matchs analysés par groupe (box score des deux côtés)

| groupe | matchs | dont nous | dont autres équipes |
|---|---|---|---|
| G1 ligue v3 | 22 | 22 | 0 |
| G2 ligue v4 | 5 | 3 | 2 |
| G3 coupe v4 | 10 | 2 | 8 |
| G4 amical v4 | 15 | 15 | 0 |
| G5 amical v5 | 10 | 10 | 0 |

##### Question 1 : ce qui sépare victoires et défaites (ligue seulement)

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

##### Question 2 : minutes lourdes et fatigue

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

##### Question 3 : rotation

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

##### Question 4 : tirs à 3 points

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

##### Question 5 : avantage du terrain

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

##### Question 6 : points de différence par point de force d'équipe (ligue seulement)

Écart de `club_strength` (dernier relevé ≤ jour du match) et marge ; r de Pearson, IC de Fisher à 95 % ; effet minimal r = 0.5 ; n requis 30.

| groupe | r [IC] | pente (points de marge par point de force) [IC] | n disponible / matchs du groupe | n requis | verdict |
|---|---|---|---|---|---|
| G1 | — | — | 4 / 22 | 30 | n < 5 : aucun calcul |
| G2 | 0.92 [0.18 ; 0.99] | 17.61 [3.48 ; 31.73] | 5 / 5 | 30 | n trop petit |

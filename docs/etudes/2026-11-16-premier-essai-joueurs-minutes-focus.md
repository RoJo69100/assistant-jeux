# BasketVibe — premier essai : joueurs, minutes, focus adverse (16/11/2026, mise à jour de 11 h)

Étude, pas de décision. Lecture seule. Aucun chiffre ne mélange deux groupes de moteur.
Mise à jour : C recalibré sur tous nos matchs (off = Lock), étoiles par demi-échantillons ; B2 avec forces ; A et B1 relancés sur la base du 16/11 11 h.

## Périmètre (recalculé par les scripts)
- Saison `86a63498…`, `silver.bv_fixtures` status `finished` : 192 matchs ; avec box period 0 + box Q1–Q4 + play-by-play : **43** (42 au premier passage, 1 de plus de la ligue 5fdd).
- `groupe(competition, jour)` : 43/43 en **v4 ligue**. Ligues : 45ca 10 (09/11–14/11), 5fdd 18 dont 6 à nous (02/11–14/11), a725 15 (02/11–11/11).
- Contrôles : 86 équipes-matchs, toutes à 240 minutes, aucune prolongation.
- Graine 20261116, 2 000 tirages bootstrap (percentiles). « Association présente » si l'IC 95 % exclut 0 ; moins de 8 matchs : pas de verdict. n requis = n × ((1,96 + 0,84) × ET / |estimé|)², indicatif.

---

## A. Caractéristiques du joueur et production à son poste

**Mesure.** Joueur avec ≥ 3 matchs ; production = éval/min, points, rebonds, passes pour 36 min. Explicatives : milieu de tranche des 8 compétences (`silver.bv_club_roster`), taille, poids, âge, expérience, forme, poste. Effet par +10 points de compétence, autres variables par +1 écart-type. Arrières PG/SG, ailiers SF, intérieurs PF/C. Milieu de tranche justifié par l'inventaire du 16/11 (`docs/etudes/2026-11-16-inventaire-ingestion.md` § e : valeur exacte à 0,54 de la tranche en moyenne).
**Données (relance).** 103 joueurs avec ≥ 3 matchs, 43 matchs, 381 joueurs-matchs ; 326 avec snapshot (120 antérieurs, 206 postérieurs). Cas complets : arrières 34, ailiers 18, intérieurs 41.
**Méthode.** Pente univariée ; ridge en contrôle (lambda par validation croisée généralisée). IC : bootstrap à deux voies (joueurs dans leur groupe de postes × matchs).

### A1. Associations présentes (10 sur 57 tests ; ≈ 2,9 attendues par hasard)
| groupe de postes | sortie | variable | n joueurs | n matchs | estimé | IC 95 % | verdict |
|---|---|---|---|---|---|---|---|
| arrières | pts/36 | deux points (+10) | 34 | 32 | +3,52 | [+0,99 ; +6,67] | association présente |
| arrières | pts/36 | trois points (+10) | 34 | 32 | +3,62 | [+0,67 ; +6,34] | association présente |
| arrières | passes/36 | passe (+10) | 34 | 32 | +2,23 | [+1,11 ; +3,84] | association présente |
| arrières | passes/36 | dribble (+10) | 34 | 32 | +2,09 | [+0,52 ; +4,10] | association présente |
| arrières | éval/min | forme (+1 ET = 1,1) | 34 | 32 | +0,090 | [+0,002 ; +0,186] | association présente (borne à 0) |
| ailiers | éval/min | endurance (+10) | 18 | 31 | +0,240 | [+0,156 ; +0,339] | association présente (fragile : 3 valeurs de tranche) |
| ailiers | éval/min | athlétisme (+10) | 18 | 31 | +0,105 | [+0,006 ; +0,203] | association présente (borne à 0) |
| ailiers | pts/36 | deux points (+10) | 18 | 31 | +3,27 | [+0,46 ; +6,84] | association présente |
| intérieurs | pts/36 | deux points (+10) | 41 | 33 | +2,28 | [+0,25 ; +4,59] | association présente |
| intérieurs | rebonds/36 | rebond (+10) | 41 | 33 | +1,90 | [+0,74 ; +3,00] | association présente |

### A2. Ridge (éval/min)
Arrières : seule la forme sort, +0,034 par ET [+0,003 ; +0,059]. Ailiers : aucune (endurance +0,058 [−0,000 ; +0,098], VIF 12,4). Intérieurs : aucune ; endurance constante, exclue.

**Ce qu'on peut dire.** En v4 ligue, la compétence attendue va avec la statistique attendue (deux points → points aux trois postes, passe et dribble → passes chez les arrières, rebond → rebonds chez les intérieurs). Associations ; confusion probable : les meilleurs joueurs sont dans les clubs les plus forts.
**Ce qu'on ne peut pas encore dire.** Quelle compétence pèse le plus sur l'éval/min à un poste (ridge non séparant, 18 à 41 joueurs pour 13 variables).
**n requis.** 34 à 100 joueurs par groupe de postes pour les pentes proches du seuil ; un 2e snapshot antérieur aux matchs réduirait l'erreur de mesure (206 snapshots postérieurs).

---

## B. Minutes

### B1. Production par minute par quart (joueurs aux 4 quarts) — relance
« 5 × 48 » = ≥ 5 joueurs à ≥ 44 min : 7 équipes-matchs sur 86.
| sous-ensemble | n joueurs-matchs | n matchs | stat | Q1 | Q4 | Q4 − Q1 | IC 95 % | verdict | n matchs requis |
|---|---|---|---|---|---|---|---|---|---|
| tous | 82 | 24 | éval/min | 0,343 | 0,272 | −0,071 | [−0,173 ; +0,039] | indéterminé : n trop petit | ≈ 110 |
| tous | 82 | 24 | pts/min | 0,389 | 0,309 | −0,081 | [−0,148 ; −0,014] | association présente | — |
| 5 × 48 | 35 | 7 | éval/min | 0,345 | 0,239 | −0,106 | — | indéterminé (< 8 matchs) | — |
| tournent | 47 | 17 | éval/min | 0,342 | 0,299 | −0,043 | [−0,176 ; +0,062] | indéterminé : n trop petit | ≈ 260 |
| tournent | 47 | 17 | pts/min | 0,397 | 0,289 | −0,108 | [−0,210 ; −0,027] | association présente | — |
| écart 5 × 48 − tournent | — | 7 / 17 | éval/min | — | — | −0,063 | — | indéterminé (< 8 matchs « 5 × 48 ») | ≈ 190 par sous-ensemble |

### B2. Concentration des minutes et marge, avec et sans force (marge = points − points adverses, box)
Force = `club_strength` de `silver.bv_standings_weekly`, dernière valeur au plus tard le jour du match ; 86/86 équipes-matchs ont les deux forces (42,8 à 58,6).
| variable | modèle | n équipes-matchs | n matchs | pente de la marge | IC 95 % | verdict |
|---|---|---|---|---|---|---|
| +10 pts de part des 5 premiers | sans force | 86 | 43 | −8,83 | [−12,40 ; −5,02] | association présente |
| +10 pts de part des 5 premiers | avec force club + adversaire | 86 | 43 | −4,74 | [−8,45 ; −0,59] | association présente |
| +1 joueur > 36 min | sans force | 86 | 43 | −7,78 | [−10,49 ; −4,80] | association présente |
| +1 joueur > 36 min | avec force club + adversaire | 86 | 43 | −4,80 | [−8,17 ; −0,92] | association présente |
Niveau équipe (13 équipes ≥ 3 matchs, sans force) : −12,1 [−17,3 ; −2,7] pour +10 pts de part des 5 premiers.
Modèle complet : force du club +2,34 pts de marge par point de force, adversaire −3,21 ; corrélation part des 5 premiers ~ force du club −0,54.

**Ce qu'on peut dire.** La pente **ne disparaît pas** avec les forces : elle baisse d'environ moitié (−8,8 → −4,7 ; −7,8 → −4,8) et son IC reste hors de 0. Environ la moitié de l'association passait par la force (les clubs faibles concentrent leurs minutes).
**Ce qu'on ne peut pas encore dire.** Si concentrer les minutes coûte des points (cause) ou si un autre trait des mêmes clubs (manager inactif, effectif court, 3 clubs moteurs : KK Glen Johnson, Chara legends, C.B.Granada au premier passage) explique le reste. Borne haute à −0,6 / −0,9 : fragile.
**n requis.** Pour la baisse au Q4 en éval/min : ≈ 110 matchs ; pour comparer 5 × 48 et rotation : ≥ 8 matchs « 5 × 48 », ≈ 190 par sous-ensemble.

---

## C. Focus défensif adverse (inféré)

**Libellés.** off = **Lock** (validé par l'utilisateur le 21/10, learnings L-018) ; intense, normal, give_up, light ; « normal (pas de plan) » exclu. Lignes gardées : 762 joueurs-matchs, 62 de nos matchs (toutes compétitions, toutes versions).

### C1. Part de tirs du joueur visé (%), tous nos matchs
| groupe | Lock | Intense | Normal | Light | Give up |
|---|---|---|---|---|---|
| v3 ligue | 3,49 (n 8, 6 m) | 8,08 (5, 3) | 8,48 (207, 21) [8,11 ; 8,99] | 8,86 (17, 5) | 6,64 (34, 6) |
| v4 ligue | 8,57 (3, 3) | 10,41 (8, 5) | 8,21 (51, 6) | 7,22 (10, 4) | 0,00 (1, 1) |
| v4 coupe | 1,20 (3, 2) | 4,15 (2, 2) | 7,62 (10, 2) | 2,98 (4, 2) | 14,27 (7, 1) |
| v4 amical | 3,25 (2, 1) | — | 8,38 (151, 13) [7,69 ; 9,27] | — | 6,82 (4, 1) |
| v5 amical | — | — | 8,07 (223, 18) [7,82 ; 8,30] | — | — |

**Normal entre groupes** (écart à v5 amical, grappes) : v3 ligue +0,41 [−0,06 ; +0,95] comparable ; v4 amical +0,31 [−0,45 ; +1,28] comparable ; v4 ligue +0,14, v4 coupe −0,45, v3 amical +0,27 : non testables (< 8 matchs). Comparabilité non établie pour tous → **calibration par groupe**.

| écart au Normal | groupe | n (niveau) | n matchs | estimé | IC 95 % | verdict |
|---|---|---|---|---|---|---|
| Lock − Normal | v3 ligue | 8 | 6 | −4,99 | [−7,46 ; −3,22] | indéterminé (< 8 matchs du niveau) |
| Give up − Normal | v3 ligue | 34 | 6 | −1,84 | [−5,76 ; +0,65] | indéterminé |
| Intense − Normal | v3 ligue | 5 | 3 | −0,40 | [−8,54 ; +4,60] | indéterminé |
| Lock − Normal | v4 ligue | 3 | 3 | +0,35 | — | indéterminé |
| Intense − Normal | v4 ligue | 8 | 5 | +2,20 | — | indéterminé |
| Lock − Normal | v4 coupe | 3 | 2 | −6,42 | — | indéterminé |

En écart à la référence du joueur (Δpart, ≥ 3 autres matchs du groupe en base) : 19 joueurs-matchs, 2 matchs, tous v4 ligue (Lock 1 : −20,0 ; Intense 3 : −2,29 ; Normal 12 : +0,09) → indéterminé.

### C2. Application en sens inverse (inféré), v4 ligue, étoiles par demi-échantillons
Autres matchs de chaque joueur tirés en deux moitiés : A choisit les étoiles (2 plus gros tireurs/min), B donne la référence.
| sous-ensemble | n joueurs-matchs | n matchs | Δpart | IC 95 % | Δtirs/min | IC 95 % | verdict |
|---|---|---|---|---|---|---|---|
| étoiles | 44 | 21 | +0,70 | [−1,00 ; +2,55] | +0,021 | [−0,034 ; +0,084] | indéterminé (inféré) |
| non-étoiles | 125 | 17 | −0,18 | [−1,00 ; +0,57] | −0,014 | [−0,042 ; +0,011] | indéterminé (inféré) |
| témoin : tous | 169 | 21 | +0,05 | [−0,33 ; +0,46] | −0,005 | [−0,024 ; +0,012] | indéterminé (inféré) |
| étoiles − non-étoiles | — | 21 | +0,89 | [−1,44 ; +3,43] | — | — | indéterminé (inféré) |
Niveau le plus proche par étoile-match (calibration Δpart v4 ligue, n 44) : Normal 61 %, Intense 36 %, Lock 2 % — **inféré, non fiable** (calibration sur 1 à 3 observations par niveau).

**Ce qu'on peut dire.** (1) En v3 ligue, le joueur que nous mettions en Lock prenait ≈ 5 points de part de tirs de moins qu'en Normal (8 joueurs-matchs, 6 matchs : sous le seuil de 8 matchs, donc indicatif). (2) La baisse des étoiles du premier passage (Δpart −1,43, tirs/min −0,051) **disparaît** avec les demi-échantillons (+0,70, +0,021) : c'était bien une régression vers la moyenne. Aucun signe, dans les matchs des autres clubs, d'un focus qui réduirait les tirs des étoiles.
**Ce qu'on ne peut pas encore dire.** L'effet du Lock en v4 (3 joueurs-matchs, +0,35) ni, donc, le focus des autres clubs.
**n requis.** ≥ 8 matchs par niveau et par groupe (règle) ; avec l'écart v3 (−5 points, ET ≈ 1,1 sur la moyenne), ≈ 3 joueurs-matchs suffiraient en puissance, la contrainte est donc le nombre de matchs : ≥ 5 matchs de ligue v4 de plus avec un Lock (8 au total), autant avec Intense (3 de plus).

---

## Sources (exécutées le 16/11, 11 h)
- `python -I pipelines/etudes/premier_essai_a_joueurs.py` (3 requêtes)
- `python -I pipelines/etudes/premier_essai_b_minutes.py` (3 requêtes : matchs, box, forces `silver.bv_standings_weekly`)
- `python -I pipelines/etudes/premier_essai_c_focus.py` (4 requêtes : `gold.bv_match_opp_focus`, box toutes saisons, matchs, box)
- `pipelines/etudes/premier_essai_communs.py` (ajouts : `box_toutes_saisons()`, `forces()`).
- `sql.py` : couverture de `club_strength` (72 équipes, 120 lignes, 01/11–16/11) ; niveaux de focus par compétition.

## Limites communes
- A : 206 snapshots postérieurs au match ; milieu de tranche = erreur de ± 10 points qui atténue les pentes.
- B2 : marges opposées des deux équipes d'un match (grappes de matchs) ; force du classement = mesure du jeu, pas de l'effectif aligné.
- C : calibration v4 quasi vide ; v3 non transposable à v4 tant que le Normal v4 ligue n'est pas testable (6 matchs).

## Export demandé
- Pour comprendre le Match Engine, j'ai besoin de : exporte les onglets Details, Stats par quart et Play-by-play des matchs de ligue listés dans l'inventaire du 16/11 (§ b), parce qu'il faut ≈ 110 matchs pour la baisse au Q4 en éval/min et ≥ 8 matchs « 5 × 48 ».
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page match (Details + Stats par quart) de chacun de nos prochains matchs de ligue où un adversaire est en Lock ou Intense, parce qu'il faut ≥ 8 matchs v4 ligue par niveau pour calibrer le focus.

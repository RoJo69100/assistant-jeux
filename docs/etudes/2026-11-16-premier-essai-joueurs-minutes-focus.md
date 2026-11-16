# BasketVibe — premier essai : joueurs, minutes, focus adverse (16/11/2026)

Étude, pas de décision. Lecture seule. Toutes les données tombent dans un seul groupe de moteur : **v4 ligue** (contrôle ci-dessous) ; aucun chiffre ne mélange de groupes.

## Périmètre (recalculé par les scripts)
- Saison `86a63498…`, `silver.bv_fixtures` status `finished` : 192 matchs ; avec box period 0 + box Q1–Q4 + play-by-play : **42**.
- Groupe par `groupe(competition, jour)` : 42/42 en **v4 ligue** (competition = league, du 02/11 au 14/11). Ligues : 45ca 10 matchs (09/11–14/11), 5fdd 17 (dont 5 à nous), a725 15. Aucun autre groupe dans le périmètre.
- Contrôles : 84 équipes-matchs, toutes à 240 minutes, aucune prolongation. Les 42 matchs v4 ligue avec box 0 sont tous dans le périmètre (le pool « box 0 » de l'étude C est identique).
- Graine 20261116, 2 000 tirages bootstrap partout (percentiles). Verdict « association présente » si l'IC 95 % exclut 0 ; moins de 8 matchs : pas d'intervalle. n requis = n × ((1,96 + 0,84) × ET / |estimé|)², ET déduit de l'IC (puissance 80 %), indicatif.

---

## A. Caractéristiques du joueur et production à son poste

**Mesure.** Unité : joueur avec ≥ 3 matchs (minutes > 0) ; production = éval/min, points, rebonds, passes pour 36 min (ratio de sommes). Explicatives : milieu de tranche des 8 compétences (`silver.bv_club_roster`), taille, poids, âge, expérience, forme. Effet par +10 points de compétence ; autres variables par +1 écart-type du groupe de postes. Postes réels du box : PG, SG, SF, PF, C → arrières PG/SG, ailiers SF, intérieurs PF/C.
**Justification du milieu** : l'inventaire du 16/11 (`docs/etudes/2026-11-16-inventaire-ingestion.md`, § e) place la valeur exacte en moyenne à 0,54 de la tranche (52 joueurs) ; chiffre repris de ce document, non recalculé ici.
**Données.** 102 joueurs, 93 avec tranches (9 sans snapshot d'effectif), 35 matchs, 371 joueurs-matchs (326 avec snapshot : 120 antérieurs au match, 206 postérieurs — le plus proche après faute d'antérieur). Tranches toutes de largeur 19 (bornes fixes de 20 points). Par poste : arrières 38 (34 avec tranches), ailiers 19 (18), intérieurs 45 (41).
**Méthode.** Pente univariée (principale) ; ridge multivarié en contrôle (variables standardisées, lambda par validation croisée généralisée). IC : bootstrap à deux voies (joueurs rééchantillonnés dans leur groupe de postes ET matchs rééchantillonnés).

### A1. Pentes univariées retenues (associations présentes ; le reste en sortie du script)
| groupe de postes | sortie | variable | n joueurs | n matchs | estimé | IC 95 % | verdict |
|---|---|---|---|---|---|---|---|
| arrières PG/SG | pts/36 | deux points (+10) | 34 | 32 | +3,52 | [+1,04 ; +6,73] | association présente |
| arrières PG/SG | pts/36 | trois points (+10) | 34 | 32 | +3,62 | [+0,68 ; +6,25] | association présente |
| arrières PG/SG | passes/36 | passe (+10) | 34 | 32 | +2,23 | [+1,16 ; +3,81] | association présente |
| arrières PG/SG | passes/36 | dribble (+10) | 34 | 32 | +2,09 | [+0,53 ; +4,16] | association présente |
| arrières PG/SG | éval/min | deux points (+10) | 34 | 32 | +0,073 | [+0,000 ; +0,151] | association présente (borne à 0) |
| arrières PG/SG | éval/min | forme (+1 ET = 1,1) | 34 | 32 | +0,090 | [+0,001 ; +0,190] | association présente (borne à 0) |
| ailiers SF | éval/min | endurance (+10) | 18 | 31 | +0,240 | [+0,163 ; +0,328] | association présente (fragile, voir ci-dessous) |
| ailiers SF | pts/36 | deux points (+10) | 18 | 31 | +3,27 | [+0,46 ; +6,73] | association présente |
| intérieurs PF/C | pts/36 | deux points (+10) | 41 | 33 | +2,28 | [+0,17 ; +4,51] | association présente |
| intérieurs PF/C | rebonds/36 | rebond (+10) | 41 | 33 | +1,90 | [+0,77 ; +3,03] | association présente |

Indéterminés notables (n trop petit) : intérieurs rebonds/36 ~ taille +1,31 [−0,18 ; +2,67] (n requis ≈ 100 joueurs) ; ailiers éval/min ~ deux points +0,112 [−0,005 ; +0,216] (≈ 36) ; ailiers éval/min ~ athlétisme +0,105 [−0,004 ; +0,198] (≈ 34) ; arrières éval/min ~ taille +0,086 [−0,002 ; +0,163] (≈ 66). Endurance des intérieurs : constante (tous dans la même tranche), non estimable.
**Multiplicité** : 10 associations sur 57 tests, environ 2,9 attendues par hasard.

### A2. Ridge (éval/min)
| groupe de postes | n joueurs | lambda | VIF max | seule variable dont l'IC exclut 0 |
|---|---|---|---|---|
| arrières PG/SG | 34 | 42,2 | 4,6 (âge) | forme +0,034 par ET [+0,003 ; +0,059] |
| ailiers SF | 18 | 31,6 | 12,4 (endurance) | aucune (endurance +0,058 [−0,000 ; +0,096]) |
| intérieurs PF/C | 41 | 31,6 | 3,8 (poids) | aucune |

**Ce qu'on peut dire.** En v4 ligue, la compétence attendue va avec la statistique attendue : deux points avec les points (trois groupes de postes), passe et dribble avec les passes chez les arrières, rebond avec les rebonds chez les intérieurs. Associations, pas causes ; confusion probable : les meilleurs joueurs d'une compétence sont aussi les mieux armés ailleurs et jouent dans les clubs les plus forts.
**Ce qu'on ne peut pas encore dire.** Quelle compétence compte le plus pour l'éval/min à un poste donné : le ridge ne sépare aucune compétence (n de 18 à 41 joueurs pour 13 variables, forte régularisation). L'effet de l'endurance chez les ailiers : l'endurance ne prend que 3 valeurs (tranches 21–40, 41–60, 61–80 ; requête ci-dessous), presque tous en 41–60 ; la pente vient de très peu de joueurs.
**Colinéarité** : corrélations entre milieux de tranche au plus +0,39 (deux points ~ athlétisme), puis défense ~ endurance +0,34, trois points ~ athlétisme +0,32 (n = 93).
**n requis** : 34 à 100 joueurs par groupe de postes pour les pentes proches du seuil ; plusieurs centaines au-delà.

---

## B. Minutes

### B1. Production par minute par quart (joueurs ayant joué les 4 quarts)
« 5 × 48 » = équipe-match avec ≥ 5 joueurs à ≥ 44 min : 7 équipes-matchs sur 84 (distribution du nombre de joueurs à ≥ 44 min : 0 → 62, 1 → 6, 2 → 1, 3 → 4, 4 → 4, 5 → 7). La répartition est bimodale ; 44 min isole les équipes qui ne sortent pas leurs titulaires.
| sous-ensemble | n joueurs-matchs | n matchs | stat | Q1 | Q4 | Q4 − Q1 | IC 95 % | verdict |
|---|---|---|---|---|---|---|---|---|
| tous | 78 | 23 | éval/min | 0,321 | 0,269 | −0,051 | [−0,154 ; +0,054] | indéterminé : n trop petit (≈ 193 matchs) |
| tous | 78 | 23 | pts/min | 0,373 | 0,311 | −0,062 | [−0,121 ; +0,004] | indéterminé : n trop petit (≈ 48 matchs) |
| 5 × 48 | 35 | 7 | éval/min | 0,345 | 0,239 | −0,106 | — | indéterminé : n trop petit (< 8 matchs) |
| 5 × 48 | 35 | 7 | pts/min | 0,379 | 0,333 | −0,045 | — | indéterminé : n trop petit (< 8 matchs) |
| tournent | 43 | 16 | éval/min | 0,300 | 0,295 | −0,005 | [−0,121 ; +0,082] | indéterminé : n trop petit |
| tournent | 43 | 16 | pts/min | 0,368 | 0,291 | −0,077 | [−0,158 ; −0,002] | association présente (borne à 0) |
| écart 5 × 48 − tournent | — | 7 / 16 | éval/min | — | — | −0,101 | — | indéterminé : n trop petit (≈ 62 matchs par sous-ensemble, indicatif) |

### B2. Concentration des minutes et marge (marge = points de l'équipe − points adverses, box period 0)
| niveau | n | variable (+1 unité) | marge estimée | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|
| équipe (≥ 3 matchs) | 13 équipes | +10 pts de part des 5 premiers | −12,2 | [−17,7 ; −3,0] | bootstrap sur les équipes, r = −0,77 | association présente |
| équipe-match | 84 (42 matchs) | +10 pts de part des 5 premiers | −9,3 | [−12,6 ; −5,2] | grappes de matchs | association présente |
| équipe (≥ 3 matchs) | 13 équipes | +1 joueur > 36 min | −9,7 | [−12,3 ; +25,5] | bootstrap sur les équipes | indéterminé : n trop petit (≈ 100 équipes) |
| équipe-match | 84 (42 matchs) | +1 joueur > 36 min | −8,0 | [−10,6 ; −4,8] | grappes de matchs | association présente |

**Ce qu'on peut dire.** En v4 ligue, les équipes qui concentrent les minutes ont une marge plus faible. L'association vient surtout de trois clubs qui alignent 4 à 5 joueurs au-delà de 36 min : KK Glen Johnson (marge moyenne −32,0 sur 3 matchs), Chara legends (−43,3 sur 3), C.B.Granada (−9,7 sur 3). Recoupé par une seconde requête SQL sur toute la saison (y compris hors périmètre) : −32,0 / −37,5 (4 matchs) / −9,7.
**Ce qu'on ne peut pas encore dire.** Si jouer à 5 × 48 fait baisser la production en fin de match (7 matchs seulement), ni si la baisse au Q4 est générale.
**Confusion probable.** Clubs faibles ou sans rotation réglée (manager inactif). *Hypothèse* : ces clubs ont une force d'équipe plus basse ; confirmée si la pente disparaît quand on ajoute la force du club (classement gold) en covariable, infirmée si elle reste. Pour le Q4 : état du score (fin de match jouée ou non) et fatigue de l'adversaire.

---

## C. Focus défensif adverse (inféré)

**Constat préalable : le niveau « Lock » n'existe pas dans nos données.** Niveaux vus dans `gold.bv_match_opp_focus` : off, light, normal, intense, give_up. La calibration Lock/Normal demandée est impossible ; je la fais sur **intense/normal**. *Hypothèse* : « intense » est le niveau le plus fort de l'interface (pas de Lock) ; confirmée par l'écran de focus défensif de la page tactique, infirmée si Lock y figure.
**Mesure.** Δpart = part des tirs du joueur (FGA / FGA de son équipe, %) dans le match moins sa part moyenne dans ses autres matchs (≥ 3, même groupe) ; Δtirs/min idem en tirs par minute. Étoiles = 2 joueurs de l'équipe en attaque aux plus hauts tirs/min hors du match testé.

| volet | n joueurs-matchs | n matchs | estimé | IC 95 % | verdict |
|---|---|---|---|---|---|
| calibration : intense | 3 | 2 | Δpart −2,29 | — | indéterminé : n trop petit |
| calibration : normal | 12 | 2 | Δpart +0,09 | — | indéterminé : n trop petit |
| calibration : light / off | 3 / 1 | 1 / 1 | +0,18 / −20,0 | — | indéterminé : n trop petit |
| inféré : étoiles, matchs des autres clubs | 44 | 21 | Δpart −1,43 | [−2,79 ; +0,06] | indéterminé : n trop petit (inféré) |
| inféré : étoiles, tirs/min | 44 | 21 | −0,051 | [−0,097 ; −0,003] | IC hors 0, non interprétable comme focus (voir limite) |
| témoin : tous joueurs avec référence | 169 | 21 | Δpart +0,15 | [−0,12 ; +0,40] | indéterminé |

Calibration : nos matchs v4 ligue du périmètre = 5 ; 39 joueurs adverses avec un focus, 19 avec ≥ 3 autres matchs. Écart intense − normal observé : −2,38 points de part, écart-type commun 5,71 → **n requis ≈ 91 joueurs-matchs par niveau, soit ≈ 61 de nos matchs de ligue** (1,5 joueur visé « intense » avec référence par match). Calcul fragile : l'écart repose sur 3 observations.
Application : 74 équipes-matchs d'autres clubs, 22 avec 2 étoiles ; 30 % des étoiles ont Δpart ≤ −5 points.

**Ce qu'on peut dire.** Rien sur le focus adverse : la calibration n'a pas de quoi distinguer intense de normal, donc aucune étoile ne peut être classée « visée ».
**Ce qu'on ne peut pas encore dire.** Si le moteur réduit la part de tirs d'un joueur visé, ni de combien.
**Limite majeure (hypothèse)** : la baisse des tirs/min des étoiles est attendue sans aucun focus (régression vers la moyenne : les étoiles sont choisies sur les mêmes matchs qui servent de référence). Confirmée si la baisse persiste quand les étoiles sont choisies sur une moitié des autres matchs et la référence calculée sur l'autre moitié (il faut ≥ 4 autres matchs par joueur) ; infirmée si elle disparaît.

---

## Sources (exécutées le 16/11)
- `python -I pipelines/etudes/premier_essai_a_joueurs.py 2000` (3 requêtes : matchs, box, effectifs)
- `python -I pipelines/etudes/premier_essai_b_minutes.py 2000` (2 requêtes : matchs, box)
- `python -I pipelines/etudes/premier_essai_c_focus.py 2000` (3 requêtes : matchs, box, `gold.bv_match_opp_focus`)
- Module commun : `pipelines/etudes/premier_essai_communs.py` (périmètre recalculé, groupe() de `pipelines/etude_evenements_basketvibe.py`).
- `sql.py` : colonnes par `information_schema` (bv_fixtures, bv_matches, bv_match_opp_focus, bv_club_roster) ; niveaux de focus par compétition ; inventaire du périmètre par compétition et ligue ; tranches d'endurance par poste (`select position, stamina_min, stamina_max, count(*) from silver.bv_club_roster where skills_visibility = 'bracket' group by …`) ; recoupement marge et joueurs > 36 min par club (CTE sur `silver.bv_match_player_stats`).

## Limites communes
- Un seul groupe (v4 ligue), 42 matchs, 3 ligues toutes partiellement captées.
- A : 206 joueurs-matchs sur 326 avec un snapshot postérieur au match (entraînement entre les deux non corrigé) ; milieu de tranche = erreur de mesure jusqu'à ± 10 points, qui atténue les pentes ; mêmes joueurs et mêmes équipes dans plusieurs lignes (pris en compte par le bootstrap à deux voies).
- B2 : les deux équipes d'un match ont des marges opposées (grappes de matchs pour en tenir compte).

## Export demandé
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page tactique de notre prochain match de ligue avec l'écran du focus défensif ouvert, parce que la liste des niveaux possibles (Lock existe-t-il ?) n'est pas en base : seuls off, light, normal, intense, give_up apparaissent dans `defensive_focus`.
- Pour comprendre le Match Engine, j'ai besoin de : exporte les onglets Details, Stats par quart et Play-by-play des matchs de ligue listés dans l'inventaire du 16/11 (§ b), parce qu'il faut ≈ 48 à 193 matchs pour la baisse au Q4 et ≥ 8 matchs « 5 × 48 » pour la comparer aux équipes qui tournent.

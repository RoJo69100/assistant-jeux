# Étude du moteur de match BasketVibe au niveau de l'événement

Écrit le 2026-11-09. Lecture seule (aucune écriture en base). Contexte : le développeur écrit que le moteur joue possession par possession ([Dev 2026-09-17, engine], skill `basketvibe-communaute`) ; la préanalyse (`docs/refonte-v3/preanalyse-matchs-basketvibe.md`) comptait des matchs. Ici l'unité est l'événement (tir, possession, joueur-quart). Les moteurs v3, v4 et v5 ne sont jamais mélangés, ni la ligue, la coupe et les amicaux.

Groupes : v3 ligue (07/09 au 26/10), v3 amical (10/10), v4 ligue (dès le 02/11), v4 coupe (28/10 au 31/10), v4 amical (11/10 au 27/10), v5 amical (dès le 28/10). La version est déduite des dates (aucune colonne ne la porte) : règle du § 1.1 de la préanalyse.

## Étape 1 : relevé et inventaire (relevé du 2026-11-09, 11:40 Paris)

### 1a) Matchs de ligue v4 terminés, par division
Source : `silver.bv_api` (pages `/leagues/<division>/seasons/<saison>/fixtures`), saison 2 (`86a63498-…`), croisée avec `silver.bv_matches`.

| Division | Matchs au calendrier | Terminés | Terminés avec box score | Terminés sans box score |
|---|---|---|---|---|
| `5fdd980c` (la mienne) | 132 | 18 | 10 | 8 |
| `a7250ea5` | 132 | 18 | 9 | 9 |
| `45caebc5` | 132 | 18 | 0 | 18 |
| Total | 396 | 54 | 19 | 35 |

Les 8 matchs de MA division terminés sans box score (liste exacte, `silver.bv_fixtures` moins `silver.bv_matches`) :

| Journée | Date | Match (domicile − extérieur) |
|---|---|---|
| 1 | 02/11 | BC Gelrode − Naked Spartans |
| 1 | 02/11 | BC KIT − Águias do Guadiana |
| 2 | 04/11 | BC KIT − BC Gelrode |
| 2 | 04/11 | Naked Spartans − Astur Hoops |
| 2 | 04/11 | Wrzos Zmigrod − Chara legends |
| 3 | 07/11 | Astur Hoops − BC KIT |
| 3 | 07/11 | BC Gelrode − Águias do Guadiana |
| 3 | 07/11 | C.B.Granada − Naked Spartans |

### 1b) Niveau événement : `silver.bv_match_events` (33 127 événements, 78 matchs)
Les chiffres ci-dessous sont ceux du relevé de 11:40 ; la base grossit à chaque export, et le script `pipelines/etude_evenements_basketvibe.py inventaire` les rejoue (10 s). Types d'événements et nombre par groupe :

| type | v3 ligue | v3 amical | v4 ligue | v4 coupe | v4 amical | v5 amical | total |
|---|---|---|---|---|---|---|---|
| miss / miss_fg | 2001 | 88 | 1548 | 819 | 1394 | 916 | 6766 |
| dreb / dreb | 1532 | 67 | 1289 | 699 | 1116 | 733 | 5436 |
| ft / ft_make | 784 | 40 | 608 | 381 | 513 | 287 | 2613 |
| fg2 / fg2_make_paint | 588 | 26 | 711 | 350 | 540 | 285 | 2500 |
| assist / assist | 588 | 23 | 690 | 314 | 487 | 321 | 2423 |
| fg2 / fg2_make_mid | 616 | 29 | 485 | 242 | 431 | 310 | 2113 |
| oreb / oreb | 507 | 20 | 438 | 233 | 376 | 203 | 1777 |
| turnover / steal | 434 | 22 | 394 | 227 | 294 | 190 | 1561 |
| fg3 / fg3_make | 401 | 20 | 306 | 134 | 307 | 196 | 1364 |
| foul / foul | 372 | 11 | 317 | 159 | 287 | 149 | 1295 |
| foul / shooting_foul | 379 | 18 | 304 | 191 | 251 | 135 | 1278 |
| turnover / turnover | 303 | 10 | 260 | 136 | 211 | 126 | 1046 |
| ft / ft_miss | 301 | 6 | 233 | 148 | 230 | 113 | 1031 |
| miss / block | 107 | 5 | 174 | 109 | 98 | 47 | 540 |
| dead_ball / dead_ball | 133 | 7 | 97 | 64 | 86 | 63 | 450 |
| period_start / period_start | 88 | 4 | 76 | 40 | 64 | 40 | 312 |
| period_end / period_end | 88 | 4 | 76 | 40 | 64 | 40 | 312 |
| jump_ball / jump_ball | 22 | 1 | 19 | 10 | 16 | 10 | 78 |
| foul / tactical_foul | 5 | 0 | 9 | 14 | 14 | 10 | 52 |
| substitution / foul_out | 17 | 0 | 9 | 9 | 12 | 3 | 50 |
| substitution / substitution_foul_trouble | 17 | 0 | 9 | 9 | 12 | 3 | 50 |
| substitution / player_injury_in | 12 | 0 | 10 | 0 | 0 | 0 | 22 |
| injury / player_injury_out | 12 | 0 | 10 | 0 | 0 | 0 | 22 |
| substitution / substitution_unavailable | 5 | 0 | 7 | 5 | 2 | 0 | 19 |
| endgame / endgame_cue | 2 | 0 | 3 | 4 | 5 | 3 | 17 |

Contenu des événements (requêtes en annexe A) :
- **Tir** : `fg2` (réussi, `fg2_make_paint` cercle ou `fg2_make_mid` mi-distance), `fg3` (réussi), `miss` (`miss_fg` raté, `block` raté contré). Les réussis portent leur zone dans le type ; les ratés ne la portent que dans `payload.shot_zone` (`paint`, `mid`, `three` : 2 288 ratés sur 6 766, versions de coordonnées récentes). L'indicateur `is_three` est renseigné pour les ratés (`miss_fg`) ; il vaut `True` pour 2 réussis seulement : il n'est donc pas fiable pour les réussis, dont le type donne l'information.
- **Coordonnées** `shot_x` et `shot_y` (0 à 1 000 sur chaque axe) : tous les réussis, 6 969 ratés sur 7 306. Tirs avec coordonnées : v3 ligue 3 606 sur 3 713, v4 ligue 3 224 sur 3 224, v4 coupe 1 545 sur 1 654, v4 amical 2 672 sur 2 770, v5 amical 1 736 sur 1 754.
- **Joueur** : `player_id` du tireur, du rebondeur, du passeur (`player2_id` pour la passe) et `payload.player_ids` ; **faute** : `shooting_foul` (faute sur tir, avec `ft_count` lancers), `foul` (autre faute), `tactical_foul` ; **entre-deux** : un par match (`jump_ball`, côté gagnant dans `payload.side`).
- **Remplacements** : 141 événements pour 47 matchs sur 78 (types : sortie pour cinq fautes, gêne de fautes, blessure, joueur indisponible) : pas de remplacement tactique dans le quart. L'effectif sur le terrain d'un quart est donc la composition de début de quart, sauf ces 141 cas.

Couverture par groupe :

| groupe | matchs | événements | tirs | tirs avec coordonnées | fautes sur tir | remplacements | matchs avec remplacement | entre-deux |
|---|---|---|---|---|---|---|---|---|
| v3 ligue | 22 | 9314 | 3713 | 3606 | 379 | 51 | 18 | 22 |
| v3 amical | 1 | 401 | 168 | 163 | 18 | 0 | 0 | 1 |
| v4 ligue | 19 | 8082 | 3224 | 3224 | 304 | 35 | 12 | 19 |
| v4 coupe | 10 | 4337 | 1654 | 1545 | 191 | 23 | 7 | 10 |
| v4 amical | 16 | 6810 | 2770 | 2672 | 251 | 26 | 8 | 16 |
| v5 amical | 10 | 4183 | 1754 | 1736 | 135 | 6 | 2 | 10 |

Compositions de début de quart et réglages tactiques (`silver.bv_match_tactics`) :

| groupe | matchs | dont à nous | avec réglages | composition nôtre | composition adverse | réglages par joueur (nôtres) | focus défensif (nôtre) |
|---|---|---|---|---|---|---|---|
| v3 ligue | 22 | 22 | 22 | 22 | 22 | 22 | 22 |
| v3 amical | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| v4 ligue | 19 | 3 | 3 | 3 | 3 | 3 | 3 |
| v4 coupe | 10 | 2 | 1 | 1 | 1 | 1 | 1 |
| v4 amical | 16 | 16 | 14 | 14 | 14 | 14 | 14 |
| v5 amical | 10 | 10 | 9 | 9 | 9 | 9 | 9 |

La composition de début de quart existe **pour les deux équipes** dans nos matchs (50 au total) ; les 16 matchs de ligue v4 d'autres équipes, les 8 de coupe v4 d'autres équipes n'ont ni composition, ni réglage. Les réglages par joueur (rôle, niveau de tir, focus offensif, niveau de défense) sont **les nôtres seulement**.

### 1c) Compétences
**Nos joueurs** (`silver.bv_player_daily`) : 287 lignes, 18 joueurs, 18 jours distincts (relevés les 16, 18, 19, 20, 22 à 27, 29 à 31 octobre, 1er, 2, 4, 6 et 8 novembre), du 2026-10-16 au 2026-11-08, 14 à 17 joueurs par jour ; huit compétences et fatigue, forme, expérience, PS ; compétences à une décimale (`*_exact`) sur 193 lignes sur 287. Avant le 16/10 : aucun relevé. Joueurs-matchs à nous (au moins 1 minute) dont un relevé date de moins d'un jour avant le match :

| groupe | joueurs-matchs à nous | avec un relevé de compétences ≤ 1 jour avant | dont à une décimale |
|---|---|---|---|
| v3 ligue | 163 | 51 | 41 |
| v3 amical | 10 | 0 | 0 |
| v4 ligue | 29 | 29 | 0 |
| v4 coupe | 12 | 12 | 12 |
| v4 amical | 148 | 107 | 79 |
| v5 amical | 94 | 94 | 37 |

**Adversaires, page Preview** (`/fixtures/<id>/preview`, `/friendlies/<id>/preview`, `/cup-fixtures/<id>/preview` ; `silver.bv_api`) :
- Page d'un match **à venir** (`kind = scheduled_lineups`) : 27 pages, 21 matchs. Les joueurs adverses portent `skill_brackets` : **fourchettes de 20 points** (observées : 0–20, 21–40, 41–60, 61–80) pour chacune des huit compétences, avec `skills_visibility = bracket` (334 lignes de joueurs adverses) ; nos joueurs y sont en visibilité complète (`full`, 443 lignes). La page porte aussi la fatigue, la forme et l'expérience des joueurs adverses, leurs statistiques de saison, la composition de début de quart des deux équipes et `estimated_chance` (probabilité estimée de victoire).
- Parmi ces 21 matchs à venir, **17 sont devenus des matchs terminés de nos équipes avec box score** : v3 ligue 4 (19/10, 21/10, 24/10, 26/10), v4 ligue 3 (02/11, 04/11, 07/11), v4 coupe 2 (28/10, 30/10), v4 amical 5 (20/10, 21/10, 24/10, 26/10, 27/10), v5 amical 3 (30/10, 31/10, 05/11) ; 8 à 15 joueurs adverses avec fourchettes par page. Ce sont les seuls matchs où les compétences adverses sont lisibles, sous forme de fourchettes. Les 17 sont tous des matchs de nos équipes (colonne « nous » de la requête de l'annexe A) ; je n'ai pas de preuve qu'une page Preview à venir d'un match d'une autre équipe existe.
- **Page d'un match TERMINÉ** (`kind = finished`), échantillon : 86 pages, 78 matchs, 2 277 lignes de joueurs, dont les matchs d'autres équipes (coupe : 8 ; ligue v4 : 16) : **aucune ligne ne contient de compétence** (`skills`, `skill_brackets` ou `skills_visibility`). Réponse : **non**. La page d'un match terminé porte le box score, la taille, le poids, le numéro de maillot, l'évaluation, `possessions_per_quarter_n`, `estimated_chance`, les quarts-temps et la dynamique du score (`score_momentum`), pas les compétences.
- Autres pages avec compétences d'un joueur : `/players/<id>/season-profile` (14 pages) : profil de statistiques (carrière, moyennes), sans les huit compétences.

## Étape 2 : critères (écrits le 2026-11-09 avant tout calcul d'effet ; seuls des comptages d'événements ont été faits : `python -I pipelines/etude_evenements_basketvibe.py comptes`, 9 s)

### 2.1 Règles communes
- **Groupes** : v3 ligue, v3 amical (un seul match : écarté), v4 ligue, v4 coupe, v4 amical, v5 amical. Jamais mélangés. Les valeurs « annoncées » viennent des skills `basketvibe-tactique` et `basketvibe-joueurs` (le manuel `[M§…]`, les annonces `[News …]`, le développeur `[Dev …]`) ; une annonce de moteur v4 s'applique à v4 et v5 (v5 = micro-améliorations de v4, [News 2026-10-28]) ; une annonce « v3 » à v3 seulement.
- **Intervalle de confiance** : à 95 %, par rééchantillonnage des **matchs** (bootstrap par grappes, 2 000 tirages, centiles), parce que les événements d'un même match ne sont pas indépendants. Aucun intervalle ne traite deux tirs du même match comme indépendants. Sous 8 matchs dans un groupe, aucun intervalle n'est calculé (verdict « non identifiable »).
- **Verdict** : **conforme** si l'intervalle contient la valeur annoncée et que sa demi-largeur ne dépasse pas l'effet minimal ; **en écart** si l'intervalle exclut la valeur annoncée ; **non identifiable** sinon, ou si la condition d'identifiabilité de la mesure n'est pas remplie, ou si la valeur annoncée n'existe pas. Pour un chiffre annoncé sous forme de plafond ou de fourchette, « contient » devient « tient dans ».
- **n requis** (calculé sur la variance observée) : `n requis = n disponible × (erreur-type observée × (1,96 + 0,84) / effet minimal)²`, en événements ; l'erreur-type vient du même rééchantillonnage par matchs.
- **Tir** : un tir est un `fg2` ou `fg3` (réussi) ou un `miss_fg` (raté), **sans les tirs contrés** (`block`, 540 : le type n'est pas renseigné) ni les lancers francs. Type 3 points : `fg3`, ou `miss_fg` avec `is_three = True`. Type 2 points : `cercle` (`fg2_make_paint`, ou `shot_zone = paint` pour un raté) ou `mi-distance` (`fg2_make_mid`, ou `shot_zone = mid`) ; un tir à 2 sans étiquette est classé par `shot_y` (cercle si `shot_y < Y0`), `Y0` choisi par pas de 10 entre 100 et 400 pour maximiser l'exactitude sur les tirs à 2 **étiquetés**, sans regarder leur réussite ; exactitude publiée ; sous 85 %, les tirs à 2 non étiquetés sont exclus (et comptés).
- **Nos joueurs** : le tireur est de notre équipe (le camp du tir est le nôtre dans un match qui est le nôtre) et un relevé de `bv_player_daily` date du jour du match ou de la veille. Compétence à une décimale (`*_exact`) quand elle existe, sinon la valeur entière (réglage marqué).
- **Camp d'une faute** : `team_side` d'un événement de faute est le camp **fautif** (vérifié : sur les 1 278 fautes sur tir, le camp des lancers francs qui suivent est toujours l'autre). `payload.side` d'un entre-deux est supposé être le camp vainqueur de l'entre-deux ; **cette lecture n'est pas encore vérifiée** : elle le sera à l'étape 3 par le camp du premier tir ou revirement qui suit, et si elle échoue la mesure 8(a) est « non identifiable ».

### 2.2 Les huit chiffres : valeur annoncée, mesure, test, unité, effet minimal, identifiabilité, n disponible

**1. Réussite d'un tir selon le type et la compétence du tireur (nos joueurs).**
- *Annoncé* ([M§7.1], skill `basketvibe-tactique`, « Quelles compétences pour quelle action ») : tir à 2 au cercle : Deux points, Athlétisme (+ taille, poids), qualité de la passe ; tir à 2 mi-distance : Deux points, qualité de la passe ; tir à 3 : Trois points, qualité de la passe. Aucun chiffre ; en v4, « un défenseur à ~80 pèse plus contre un attaquant à ~40 » ([News 2026-10-16]).
- *Mesure* : pente de la probabilité de réussite sur la compétence **nommée** (Deux points pour un tir à 2, Trois points pour un tir à 3), en points de pourcentage pour +10 points de compétence ; pente sur la compétence **non nommée** (Trois points pour un tir à 2, Deux points pour un tir à 3). Par type de tir (cercle, mi-distance, 3 points) et par groupe.
- *Test* : modèle de probabilité linéaire (réussite 0 ou 1 sur la compétence), pente et intervalle par rééchantillonnage des matchs. *Unité* : le tir. *Annoncé retenu* : pente nommée > 0, pente non nommée = 0. *Effet minimal* : 2,0 points de réussite pour +10 points de compétence.
- *Identifiabilité* : au moins 150 tirs du type dans le groupe et au moins 8 matchs.
- *n disponible* (tirs de nos joueurs avec compétences) : v3 ligue 428 (3 points 127 ; cercle étiqueté 104 ; mi-distance 60 ; 2 points non étiquetés 137) ; v4 ligue 235 (92 ; 89 ; 54 ; 0) ; v4 coupe 157 (55 ; 36 ; 25 ; 41) ; v4 amical 961 (355 ; 200 ; 161 ; 245) ; v5 amical 839 (347 ; 219 ; 200 ; 73) ; v3 amical 0.

**2. Tirs provoquant une faute selon l'agressivité défensive.**
- *Annoncé* ([M§6.3], skill `basketvibe-tactique`, « Consignes par joueur ») : tirs adverses provoquant une faute ~12 % (soft, niveau 0), ~16,5 % (équilibrée, niveau 2), ~21 % (agressive, niveau 4) ; dépendance à l'agressivité **moyenne des cinq** sur le terrain. [News 2026-10-11] : en v4 les fautes suivent l'agressivité défensive ; « manquait en v3 » : pour v3, on attend **aucune pente**.
- *Mesure* : taux = fautes sur tir de **notre** défense / (tirs adverses + ces fautes), par quart où notre composition est connue ; exposition = moyenne des niveaux de défense (0, 2 ou 4) de nos cinq joueurs. Pente du taux par niveau moyen d'agressivité et taux par tranche (moins de 1 ; de 1 à 3 ; plus de 3).
- *Test* : probabilité linéaire sur le niveau moyen, rééchantillonnage des matchs. *Unité* : le tir adverse. *Annoncé retenu* : pente de 2,25 points par niveau (de 12 % à 21 % sur 4 niveaux) pour v4 et v5, 0 pour v3 ; niveau à 16,5 % pour une défense équilibrée. *Effet minimal* : 1,0 point par niveau.
- *Identifiabilité* : au moins 3 tranches d'exposition avec chacune au moins 150 tirs adverses. *n disponible* (tirs adverses dans des quarts à composition connue ; fautes sur tir de notre défense ; quarts) : v3 ligue 1 853 ; 184 ; 88 ; v4 ligue 259 ; 27 ; 12 ; v4 coupe 82 ; 9 ; 4 ; v4 amical 1 250 ; 98 ; 56 ; v5 amical 803 ; 56 ; 36.

**3. Effet de la fatigue sur la réussite et les pertes de balle, par joueur-quart.**
- *Annoncé* v4 et v5 ([News 2026-10-17], skill `basketvibe-joueurs`) : une seule échelle pour l'attaque et la défense : 0 %, −4 %, −15 %, −30 %, −50 % à une fatigue de 0, 20, 40, 60, 80 ; fixée par la fatigue au coup d'envoi, constante pendant le match. v3 ([M§5.6]) : attaque −3, −10, −20, −40 % à 20, 40, 60, 100 ; défense −2, −6, −13, −26 %.
- *Mesure* : pente de la réussite (points de pourcentage pour +10 de fatigue) et du nombre de pertes de balle par quart de nos joueurs (fatigue du relevé du jour ou de la veille). La pénalité annoncée s'applique aux compétences : la limite haute de l'effet sur la réussite est la pénalité annoncée × la réussite moyenne (borne retenue, hypothèse : une pénalité de x % sur la valeur d'une action ne baisse pas la réussite de plus de x % en relatif).
- *Test* : probabilité linéaire, rééchantillonnage des matchs. *Unité* : le tir, et le joueur-quart pour les pertes de balle. *Effet minimal* : 2,0 points de réussite à la fatigue maximale observée du groupe.
- *Identifiabilité* : la fatigue maximale observée du groupe doit atteindre le palier annoncé (20, 40, 60, 80) et au moins 100 tirs doivent avoir une fatigue d'au moins 20 ; sinon, le palier est « non identifiable ». *n disponible* (tirs de nos joueurs avec fatigue connue ; avec fatigue ≥ 10 ; ≥ 20 ; fatigue maximale) : v3 ligue 428 ; 295 ; 27 ; 24,63 ; v4 ligue 235 ; 0 ; 0 ; 8,84 ; v4 coupe 157 ; 0 ; 0 ; 0,47 ; v4 amical 961 ; 209 ; 43 ; 24,63 ; v5 amical 839 ; 0 ; 0 ; 8,84. **Les paliers de 40 à 80 ne sont observés dans aucun groupe**, et le palier de 20 l'est par 43 tirs au plus : le critère annonce déjà « non identifiable » pour 40, 60, 80 dans les cinq groupes.

**4. Pénalité au-delà de 36 minutes au dernier quart.**
- *Annoncé* ([M§5.7], skill `basketvibe-joueurs`) : −20 % fixe sur toutes les actions à partir de 36 minutes jouées dans le match, prolongation comprise ; un joueur qui joue les trois premiers quarts en entier est pénalisé dès la première seconde du Q4 ([GM 2026-10-30]).
- *Mesure* : différence de réussite au tir (points de pourcentage) entre le Q4 et les Q1 à Q3, pour les joueurs à 36 minutes cumulées avant le Q4 (minutes aux Q1 à Q3 ≥ 35,5), **moins** la même différence pour les joueurs de contrôle (de 12 à 30 minutes cumulées avant le Q4). Les deux équipes sont utilisées (aucune compétence n'entre : la comparaison est interne au joueur). Même mesure pour les pertes de balle par minute.
- *Test* : différence de différences en probabilité linéaire, rééchantillonnage des matchs. *Unité* : le tir. *Annoncé retenu* : un effet **négatif, d'au plus −20 % en relatif**, soit entre −9 et 0 point de réussite pour une réussite de base de 45 %. *Effet minimal* : 3,0 points.
- *Identifiabilité* : au moins 100 tirs de joueurs lourds au Q4 et 8 matchs. *n disponible* (tirs au Q4 ; joueurs à 36 min ou plus ; contrôle) : v3 ligue 910 ; 445 ; 420 ; v4 ligue 745 ; 108 ; 590 ; v4 coupe 392 ; 78 ; 301 ; v4 amical 665 ; 145 ; 475 ; v5 amical 408 ; 99 ; 245 ; v3 amical 42.

**5. Part de tirs à 3 points selon le focus de tir.**
- *Annoncé* ([M§6.3], skill `basketvibe-tactique`) : focus de tir en 5 crans de « 2 pts » à « 3 pts » ; au maximum environ 2 tirs à 3 pour 1 tir à 2 (soit 66,7 % des tirs du joueur) ; toute l'équipe au maximum plafonne à environ 50 % de tirs à 3 ; [Dev 2026-08-24] : plafond de 50 % des tirs pour un joueur réglé « tout à 3 pts » ; plafond relevé le 2026-09-16, valeur non publiée.
- *Mesure* : part de tirs à 3 points d'un joueur dans un match (tirs sans contrés), au moins 8 tirs, par niveau de tir (0 à 4) de ses réglages ; part de l'équipe par match. Moyenne par niveau, rééchantillonnage des matchs.
- *Test* : intervalle de la moyenne au niveau maximal (4) comparé à deux plafonds : 66,7 % et 50 %. *Unité* : le joueur-match. *Annoncé retenu* : moyenne du niveau 4 ≤ 66,7 % (plafond du manuel) et ≤ 50 % (plafond du développeur) ; la part augmente avec le niveau. *Effet minimal* : 5 points de pourcentage.
- *Identifiabilité* : au moins 15 joueurs-matchs au niveau 4 et 8 matchs. *n disponible* (joueurs-matchs à au moins 8 tirs ; niveaux 0 / 2 / 3 / 4) : v3 ligue 115 (24 ; 78 ; 5 ; 8) ; v4 ligue 13 (6 ; 4 ; 0 ; 3) ; v4 coupe 4 ; v4 amical 73 (34 ; 17 ; 10 ; 12) ; v5 amical 47 (16 ; 22 ; 0 ; 9) ; aucun groupe n'atteint 15 joueurs-matchs au niveau 4.

**6. Part de tirs selon le focus offensif.**
- *Annoncé* ([M§6.3]) : focus offensif en 5 crans de Low à Primary ; « deux scoreurs, l'un Primary et l'autre Normal : le Primary tente environ un tiers de tirs en plus », soit un rapport de 1,33.
- *Mesure* : tirs par quart sur le terrain d'un de nos joueurs (composition de début de quart, réglages du match), par niveau de focus offensif ; rapport de la moyenne du niveau 4 (Primary) à celle du niveau 2 (Normal), et des autres niveaux au niveau 2.
- *Test* : rapport de moyennes, rééchantillonnage des matchs. *Unité* : le joueur-quart. *Annoncé retenu* : 1,33 pour Primary contre Normal. *Effet minimal* : écart de 0,15 au rapport.
- *Identifiabilité* : au moins 30 joueurs-quarts au niveau 4 et au niveau 2, et 8 matchs. *n disponible* (joueurs-quarts ; niveaux 0 / 1 / 2 / 3 / 4 ; tirs) : v3 ligue 440 (16 ; 48 ; 334 ; 26 ; 16 ; 1 735) ; v4 ligue 60 (9 ; 12 ; 15 ; 15 ; 9 ; 233) ; v4 coupe 20 ; v4 amical 280 (2 ; 120 ; 90 ; 68 ; 0 ; 1 129) ; v5 amical 180 (0 ; 58 ; 91 ; 29 ; 2 ; 758). **Aucun groupe n'a 30 joueurs-quarts au niveau 4** : le critère annonce « non identifiable » dans les cinq groupes.

**7. Rythme : possessions par équipe.**
- *Annoncé* : **aucune valeur de rythme** dans les skills ; [News 2026-10-28] (v5) : plus de possession de plus de 24 secondes dans le play-by-play, plus de 20 secondes d'inaction en fin de quart.
- *Mesure* : possessions par équipe et par match = tirs tentés (contrés compris) + 0,44 × lancers francs tentés − rebonds offensifs + pertes de balle (box score) ; par groupe ; à comparer, quand elle existe, à la valeur `possessions_per_quarter_n` de la page du match. Écart d'horloge entre événements consécutifs d'un même quart (hors début et fin de quart, balle morte et remplacements) : part des écarts de plus de 24 secondes, par groupe.
- *Test* : moyenne par groupe et différence entre groupes, rééchantillonnage des matchs (comparaison, pas mélange). *Unité* : l'équipe-match. *Annoncé retenu* : aucun niveau annoncé ; v5 : part des écarts de plus de 24 secondes nulle. *Effet minimal* : 3 possessions par équipe et par match entre deux moteurs.
- *n disponible* (équipes-matchs) : v3 ligue 44, v4 ligue 38, v4 coupe 20, v4 amical 32, v5 amical 20. Le niveau de rythme n'ayant aucune valeur annoncée, son verdict est « non identifiable » par construction ; seule la règle des 24 secondes de v5 est testable.

**8. Avantage du terrain à l'entre-deux et en réussite de tir.**
- *Annoncé* ([M§6.1]) : « petit bonus de compétence à domicile et meilleure chance de gagner l'entre-deux du premier quart-temps » ; aucun chiffre.
- *Mesure* : (a) part des entre-deux gagnés par l'équipe qui reçoit (un par match) contre 0,5 ; (b) réussite au tir (hors lancers francs) de l'équipe qui reçoit moins celle de l'équipe qui se déplace, en points de pourcentage.
- *Test* : (a) binomial exact ; (b) probabilité linéaire sur l'indicateur domicile, rééchantillonnage des matchs. *Unité* : l'entre-deux ; le tir. *Annoncé retenu* : (a) part supérieure à 0,5 ; (b) un bonus positif et petit : entre 0 et +3 points. *Effet minimal* : (a) part de 0,60, soit 194 entre-deux au moins pour une puissance de 80 % (non atteint dans aucun groupe : 10 à 22) ; (b) 1,5 point.
- *n disponible* (entre-deux ; tirs) : v3 ligue 22 ; 3 606 ; v4 ligue 19 ; 3 050 ; v4 coupe 10 ; 1 545 ; v4 amical 16 ; 2 672 ; v5 amical 10 ; 1 707. (a) est « non identifiable » dans les cinq groupes par construction (n inférieur à 194).

## Annexe A : requêtes et sorties de l'étape 1

Commande de l'inventaire (groupes, événements, compositions, compétences de nos joueurs) : `python -I pipelines/etude_evenements_basketvibe.py inventaire` (10,6 s, code 0 ; sortie en tableaux ci-dessus).

Requête 1a (matchs par division) : `select substring(a.endpoint from '^/leagues/([0-9a-f-]{8})') division, count(distinct f->>'id') fixtures, count(distinct f->>'id') filter (where f->>'status'='finished') termines, count(distinct f->>'id') filter (where f->>'status'='finished' and exists (select 1 from silver.bv_matches m where m.fixture_id = (f->>'id')::uuid)) avec_box from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8' group by 1 order by 1` : `45caebc5 132 18 0` ; `5fdd980c 132 18 10` ; `a7250ea5 132 18 9`.

Requête 1a bis (8 matchs manquants de ma division) : `select x.round_number journee, x.match_day jour, x.home_team domicile, x.away_team exterieur from silver.bv_fixtures x where x.season_id = '86a63498-c133-44ea-aedb-f1310ad51ae8' and x.fixture_id in (select (f->>'id')::uuid from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/5fdd980c-032b-4ea3-b608-5eadc0c61f44/seasons/' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8') and x.status = 'finished' and not exists (select 1 from silver.bv_matches m where m.fixture_id = x.fixture_id) order by x.match_day, x.home_team` : 8 lignes (tableau du 1a).

Requête 1b (détails et coordonnées des tirs) : `select kind, detail, count(*) n, count(shot_x) avec_coord, sum(is_three::int) trois from silver.bv_match_events group by 1,2 order by 1, 3 desc` : 25 types ; champs du `payload` par type : `select kind, k, count(*) n from silver.bv_match_events e, jsonb_object_keys(e.payload) k group by 1,2 order by 1, 3 desc` (tir : `sx`, `sy`, `player_ids`, `shot_coords_version`, `putback`, `dunk`, `alley_oop`, `buzzer`, `heave`, `shot_zone` ; faute : `ft_count`, `bonus` ; lancer : `ft_att`, `ft_made` ; entre-deux : `side` ; revirement : `channel`).

Requête 1c (types de pages) : `select regexp_replace(endpoint, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'ID', 'g') motif, count(*) pages, min(captured_at)::date du, max(captured_at)::date au from silver.bv_api group by 1 order by 2 desc` ; Preview par type : `select body->>'kind' kind, count(*) pages from silver.bv_api where endpoint ~ '/preview$' group by 1` : `finished 86`, `scheduled_lineups 27` ; échantillon des pages terminées : `select count(*) pages_terminees, count(distinct a.body->>'fixture_id') matchs, sum(jsonb_array_length(a.body->'players')) joueurs_lignes, sum((select count(*) from jsonb_array_elements(a.body->'players') p where p ? 'skills' or p ? 'skill_brackets' or p ? 'skills_visibility')) avec_competences from silver.bv_api a where a.endpoint ~ '/preview$' and a.body->>'kind'='finished'` : `86 78 2277 0` ; fourchettes des matchs à venir : `select p->'skill_brackets' ... where a.body->>'kind'='scheduled_lineups'` : exemple `{"defense": {"min": 41, "max": 60}, "passing": {"min": 21, "max": 40}, ...}` ; visibilité : `bracket` 334 lignes, `full` 443 lignes.

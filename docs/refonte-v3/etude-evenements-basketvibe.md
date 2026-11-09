# Étude du moteur de match BasketVibe au niveau de l'événement

Écrit le 2026-11-09. Lecture seule (aucune écriture en base). Contexte : le développeur écrit que le moteur joue possession par possession ([Dev 2026-09-17, engine], skill `basketvibe-communaute`) ; la préanalyse (`docs/refonte-v3/preanalyse-matchs-basketvibe.md`) comptait des matchs. Ici l'unité est l'événement (tir, possession, joueur-quart). Les moteurs v3, v4 et v5 ne sont jamais mélangés, ni la ligue, la coupe et les amicaux.

Groupes : v3 ligue (07/09 au 26/10), v3 amical (10/10), v4 ligue (dès le 02/11), v4 coupe (28/10 au 31/10), v4 amical (11/10 au 27/10), v5 amical (dès le 28/10). La version est déduite des dates (aucune colonne ne la porte) : règle du § 1.1 de la préanalyse.

**Résumé** : sur les huit chiffres, un seul est conforme (la règle des 24 secondes de v5), un seul est contredit (la mi-distance qui dépend du Trois points, amical v4), un présente un écart de niveau dont le dénominateur du manuel n'est pas défini (les fautes sur tir, amical v4), deux pentes du chiffre 1 sont « effet présent, taille imprécise » (cercle, amical v4 ; 3 points, amical v5), et tous les autres sont « non identifiables » avec les données actuelles. Le tableau chiffre / valeur annoncée / n d'événements / résultat / verdict est à l'étape 3 ; les pages à exporter à l'étape 4(b) ; la faisabilité d'un simulateur à l'étape 4(c).

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

## Étape 3 : calculs (`python -I pipelines/etude_evenements_basketvibe.py calculs`, 12 s, code 0 ; tests figés `pipelines/test_etude_evenements.py` : 24 sur 24)

Intervalles à 95 % par rééchantillonnage de 2 000 tirages de **matchs** ; graine fixe (20261109). Sortie complète : annexe B et `docs/refonte-v3/etude-evenements-basketvibe-sortie.md`. Sous 8 matchs dans un groupe, aucun intervalle n'est calculé : c'est le cas de la ligue v3 (5 matchs avec compétences connues, car les relevés de compétences commencent le 16/10), de la ligue v4 (3) et de la coupe v4 (2) pour les mesures qui demandent les compétences de nos joueurs.

### Tableau : chiffre / valeur annoncée / n d'événements / résultat / verdict
Groupes cités : « v4 amical » = amicaux du 11/10 au 27/10 ; « v5 amical » = amicaux depuis le 28/10 (le moteur des amicaux aujourd'hui) ; ligue v4 = moteur de la ligue actuelle.

| # | Chiffre | Valeur annoncée (source) | n d'événements | Résultat | Verdict |
|---|---|---|---|---|---|
| 1 | Réussite du tir selon le type et la compétence du tireur | Cercle : Deux points, Athlétisme ; mi-distance : Deux points ; 3 points : Trois points (+ qualité de la passe) ; aucun chiffre ([M§7.1]) | tirs de nos joueurs avec compétences : v4 amical 961 (cercle 313, mi 293, 3 pts 355 ; 12 matchs), v5 amical 839 (256, 236, 347 ; 10 matchs), ligue v4 235 (3 matchs) | v4 amical cercle : +6,81 points de réussite par +10 de Deux points [4,02 ; 9,01] ; mi-distance : Deux points −2,09 [−6,11 ; 1,32] et **Trois points +8,63 [1,36 ; 14,77]** ; 3 pts : +1,90 [−6,04 ; 8,45]. v5 amical 3 pts : +2,32 [0,61 ; 5,06] | **effet présent, taille imprécise** pour le cercle de v4 amical (+6,81 [4,02 ; 9,01]) et le 3 points de v5 amical (+2,32 [0,61 ; 5,06]) : l'intervalle exclut 0 mais sa demi-largeur (2,5 et 2,2) dépasse l'effet minimal de 2,0 ; **non identifiable** pour les autres (intervalle qui contient 0 ou n insuffisant, n requis 871 à 9 470 tirs) ; la règle écrite avant calcul (demi-largeur supérieure à 2,0 : « non identifiable ») reste celle des étapes 2 et 3 et de l'annexe B ; **en écart** pour la mi-distance de v4 amical (la compétence non nommée, Trois points, pèse) |
| 2 | Tirs provoquant une faute selon l'agressivité | 12 % (soft), 16,5 % (équilibrée), 21 % (agressive), soit 2,25 points par niveau ([M§6.3]) ; v3 : aucun lien ([News 2026-10-11]) | tirs adverses et fautes : v4 amical 1 348 (14 matchs), v5 amical 859 (9), v3 ligue 2 037 (22), ligue v4 286 (3) | v4 amical : pente 1,01 point par niveau [−0,35 ; 1,60] ; taux 6,6 % (niveau moyen < 1), 6,5 % (1 à 3), 11,9 % (> 3). v3 ligue : pente 1,76 [−0,04 ; 3,47], taux 9,7 % [8,5 ; 11,0] pour une défense équilibrée | **pente de 2,25 exclue** pour v4 amical (calculée avec le dénominateur retenu) et **écart de niveau, dénominateur du manuel non défini** (6,5 % au lieu de 16,5 % avec « tirs adverses + fautes » ; 7,0 % à 11,0 % tous niveaux confondus avec « tirs adverses seuls », 6,5 % à 9,9 % avec « tirs adverses + fautes », sur les cinq groupes, calculés avec les n de l'étape 2 : 184/1 853, 27/259, 9/82, 98/1 250, 56/803) ; **non identifiable** pour v3, ligue v4, coupe v4, v5 (aucune tranche « agressive » : 3 tranches de 150 tirs requises) |
| 3 | Fatigue sur la réussite et les pertes de balle | v4/v5 : −4, −15, −30, −50 % à 20, 40, 60, 80 ; v3 : −3, −10, −20, −40 % à 20, 40, 60, 100 ([News 2026-10-17], [M§5.6]) | tirs avec fatigue connue : v4 amical 961 (43 avec fatigue ≥ 20), v5 amical 839 (aucun ≥ 10), ligue v4 235 (aucun ≥ 10) | v4 amical : pente −0,52 point par +10 de fatigue [−4,51 ; 4,34] ; effet annoncé à la fatigue maximale observée (24,6) : −3,2 points ; effet détectable : 15,5 points ; pertes de balle −0,023 par quart et par +10 [−0,186 ; 0,191] | **non identifiable** (fatigue maximale observée : 24,63 en v3 et v4 amical, 8,84 en ligue v4 et v5, 0,47 en coupe : **les paliers 40, 60 et 80 ne sont jamais observés**) |
| 4 | Pénalité au-delà de 36 minutes au dernier quart | −20 % fixe sur toutes les actions ([M§5.7]) ; borne retenue : entre −9 et 0 point de réussite | tirs au Q4 de joueurs à 36 minutes : v3 445, ligue v4 108, coupe v4 78, v4 amical 145, v5 amical 99 | différence de différences de réussite : v4 amical −14,24 points [−22,03 ; −5,81] ; ligue v4 −6,96 [−18,69 ; 6,43] ; v5 amical −6,99 [−18,90 ; 5,01] ; ligue v3 +0,16 [−5,66 ; 5,70] | **non identifiable** partout (n requis de 26 000 à 110 000 tirs) |
| 5 | Part de tirs à 3 points selon le focus de tir | au plus 2 tirs à 3 pour 1 à 2 (66,7 %) ([M§6.3]) ; équipe environ 50 % ; [Dev 2026-08-24] : plafond de 50 % pour un joueur « tout à 3 pts » | joueurs-matchs (≥ 8 tirs) au niveau 4 : ligue v3 8, v4 amical 12, v5 amical 9, ligue v4 3 ; 115 à 13 joueurs-matchs au total par groupe | niveau 4 : ligue v3 65,4 % [58,2 ; 72,3], v4 amical 65,5 % [59,1 ; 71,9] ; niveau 3 : 63,1 % (v4 amical) ; niveau 2 : 47,2 % (ligue v3), 40,6 % (v4 amical), 42,4 % (v5) ; niveau 0 : 10,1 à 16,6 %. Équipe : moyenne 30,6 à 41,7 %, maximum 54,7 % (13 équipes-matchs sur 154 au-dessus de 50 %) | **non identifiable** (15 joueurs-matchs au niveau 4 requis, aucun groupe ne les atteint) ; indice : le joueur au niveau 4 tire environ 2 à 3 pour 1 à 2, pas 50 % ; l'équipe reste autour de 50 % au plus |
| 6 | Part de tirs selon le focus offensif | Primary tente environ un tiers de tirs en plus qu'un joueur Normal : 1,33 ([M§6.3]) | joueurs-quarts Primary : ligue v3 16, ligue v4 9, coupe v4 4, v4 amical 0, v5 amical 2 | ligue v3 : rapport Primary / Normal 1,47 [1,27 ; 1,70] (16 contre 334 joueurs-quarts) | **non identifiable** (30 joueurs-quarts requis au niveau 4 ; l'intervalle de la ligue v3 contient 1,33) |
| 7 | Rythme : possessions par équipe | aucun niveau annoncé ; v5 : aucune possession de plus de 24 s ([News 2026-10-28]) | équipes-matchs : 44 (v3), 38, 20, 31, 20 ; 31 000 écarts d'horloge | 100,3 à 102,2 possessions par équipe et par match selon le groupe ; **`possessions_per_quarter_n` vaut 50 sur les 86 pages de match (3 moteurs)** ; v5 amical − v4 amical : +1,3 [+0,1 ; +2,5] ; écarts de plus de 24 s : 2 % en v3 et v4 (maximum 41 à 48 s), **0,00 % en v5 (maximum 17 s)** | niveau de rythme : **non identifiable** (aucune valeur annoncée), mais constant ; règle des 24 s de v5 : **conforme** |
| 8 | Avantage du terrain à l'entre-deux et au tir | « petit bonus de compétence à domicile », meilleure chance à l'entre-deux ; aucun chiffre ([M§6.1]) | entre-deux : 22, 19, 10, 16, 10 (un par match) ; tirs : 3 606, 3 050, 1 545, 2 672, 1 707 | entre-deux gagnés par l'équipe qui reçoit : 13/22, 8/19, 4/10, 8/16, 4/10 (p ≥ 0,52) ; lecture de `payload.side` confirmée à 77 % seulement ; réussite à domicile moins à l'extérieur : +1,54 [−3,74 ; 7,06] (ligue v3), −0,01 [−8,03 ; 8,22] (ligue v4), +1,57 [−3,94 ; 7,32] (v4 amical), +3,29 [−2,70 ; 9,68] (v5 amical) | **non identifiable** : (a) 194 entre-deux requis, 10 à 22 disponibles et lecture non confirmée ; (b) 58 000 à 182 000 tirs requis |

### Lectures
- **Une seule valeur est contredite** (en écart) : la mi-distance qui dépend du Trois points en amical v4 (+8,63 [1,36 ; 14,77] points par +10). **Fautes sur tir, amical v4** : pente de 1,01 au lieu de 2,25 point par niveau (dénominateur retenu : tirs adverses + fautes) et **écart de niveau, dénominateur du manuel non défini** : 6,5 % pour une défense équilibrée au lieu de 16,5 % ; tous niveaux confondus, 7,0 % à 11,0 % avec les tirs adverses seuls et 6,5 % à 9,9 % avec les tirs adverses plus les fautes, contre 12 à 21 % annoncés. Les deux reposent sur 12 à 14 matchs et sur 18 joueurs : un indice fort, pas une loi.
- **Une valeur est conforme** : la règle des 24 secondes de v5 (aucun écart d'horloge de plus de 17 s sur 3 981 écarts, contre 41 à 48 s en v3 et en v4).
- **Les paliers de fatigue 40 à 80 sont inobservables** avec nos données : nos joueurs ne dépassent pas 24,6 de fatigue au coup d'envoi.
- Les verdicts de la question 1 appliquent la règle écrite avant calcul : une pente de +6,81 [4,02 ; 9,01] a une demi-largeur (2,5) qui dépasse l'effet minimal (2,0) : la règle écrite avant calcul la classe « non identifiable » (elle reste à côté, non effacée) ; comme l'intervalle exclut 0, le verdict lisible est « effet présent, taille imprécise » (de même pour +2,32 [0,61 ; 5,06], demi-largeur 2,2, v5 amical 3 points) ; elle ne dit pas que la pente est nulle.
- Question 8 : la lecture de `payload.side` (camp vainqueur de l'entre-deux) est confirmée par le premier tir dans 77 % des cas, sous le seuil de 90 % fixé : (a) est donc non identifiable ; le camp domicile gagne 49 % des 78 entre-deux. Le jeu publie lui-même une chance de victoire à domicile (`estimated_chance`) de 49 % à 57 %, moyenne 51,7 % sur 27 pages de matchs à venir de nos équipes : un bonus d'environ 2 points, ce qui va dans le sens de « petit bonus » sans le mesurer.

## Étape 4 : conclusions

### (a) Ce que le moteur fait qui n'est ni dans le manuel ni dans les données (résidus)
1. **Un rythme fixe** : `possessions_per_quarter_n = 50` sur les 86 pages de match (07/09 au 08/11, v3, v4 et v5, sans prolongation), soit environ 25 possessions par équipe et par quart, 100 par équipe et par match ; le box score donne 100,3 à 102,2. Le manuel et les skills ne donnent aucun nombre de possessions. La version ne change pas le rythme de plus de 1,3 possession (v5 contre v4, amical).
2. **Un niveau de fautes sur tir inférieur à celui du manuel** : 7,0 % à 11,0 % des tirs adverses seuls, ou 6,5 % à 9,9 % avec le dénominateur « tirs adverses plus ces fautes » (tous niveaux confondus, cinq groupes), contre 12 à 21 % annoncés. Le manuel parle de « tirs adverses provoquant une faute » ; la définition du dénominateur (contacts, pénétrations, tirs contestés) n'est pas donnée : **écart de niveau, dénominateur du manuel non défini** : aucun des deux dénominateurs ne rejoint 12 %, mais le plus haut (coupe v4, 1 match) s'en approche.
3. **Une mi-distance qui dépend du Trois points** (+8,63 points par +10, v4 amical), alors que le manuel ne cite que Deux points pour ce tir ; peut être de la colinéarité entre compétences des mêmes joueurs (18 joueurs), à tester sur d'autres effectifs.
4. **Une pénalité de minutes lourdes qui paraît plus forte que −20 %** en amical v4 (−14,2 points de réussite, au-delà de la borne de −9), mais ni en ligue v3 (+0,2), ni significative en ligue v4 : à ne pas lire sans plus de données.
5. **Une règle de 24 secondes appliquée en v5** (aucun écart de plus de 17 s), cohérente avec l'annonce du 28/10 ; en v3 et v4, 2 % des écarts dépassent 24 s.
6. **Un plafond de tirs à 3 points d'équipe d'environ 50 %** : maximum 54,7 % sur 154 équipes-matchs, 13 au-dessus de 50 % (bruit d'échantillonnage attendu de 5 points sur 85 tirs) ; mais un joueur au niveau 4 tire environ 65 % de ses tirs à 3 points (2 pour 1), ce qui contredit un plafond individuel de 50 %.

### (b) Pages à exporter pour rendre identifiables les chiffres qui ne le sont pas
Les compétences d'un joueur ne se lisent que pour **nos** joueurs (page Équipe, relevé du jour) : les matchs d'autres équipes apportent le box score et le play-by-play, **jamais** les compétences ni les réglages. Un match d'une autre équipe ne rend donc identifiable aucun des chiffres 1, 2, 3, 5 et 6 ; il n'aide que les chiffres 4, 7 et 8, qui restent hors de portée (n requis de 26 000 à 182 000 tirs). Ces matchs d'autres équipes servent encore à étudier la rotation, les minutes et les compositions, non traitées ici.

Pages par match de nos équipes (amical, ligue ou coupe) : le box score (`period-box`), le play-by-play, les réglages et compositions (`match-tactics-used`) et l'aperçu avant match (`preview`, qui porte les fourchettes de compétences adverses et `estimated_chance`) : **4 pages par match**, plus la page Équipe (aperçu, joueurs) du jour du match (compétences et fatigue).

| Chiffre | Ce qui manque | Matchs et pages à ajouter (nos matchs, amicaux v5) |
|---|---|---|
| 1 (3 pts, v5) | 871 tirs à 3 points avec compétences, 347 disponibles (34,7 par match) | **16 amicaux de plus**, soit 64 pages et 16 pages Équipe. Cercle et mi-distance : 3 091 et 4 867 tirs requis, hors de portée |
| 2 (fautes) | 3 tranches d'agressivité de 150 tirs adverses chacune ; 859 tirs disponibles, tous dans la tranche « soft » | **au moins 4 amicaux de plus** avec une défense uniforme à 2 (2 matchs) et à 4 (2 matchs) pour nos cinq (environ 95 tirs adverses par match) : 16 pages. Ce réglage change le jeu de l'équipe : à décider par l'utilisateur |
| 3 (fatigue) | 100 tirs à fatigue ≥ 20 en v5 (0 aujourd'hui) ; les paliers 40 à 80 : aucun | aucun export ne suffit : il faut des joueurs fatigués au coup d'envoi (défense agressive et minutes lourdes sur plusieurs semaines), c'est un protocole de jeu, pas une page |
| 4 (minutes lourdes) | de 26 000 à 110 000 tirs | hors de portée (la ligue entière compte moins de 70 000 tirs) |
| 5 (focus de tir) | 15 joueurs-matchs au niveau 4 ; 9 en v5 | **3 amicaux de plus** avec 2 tireurs au niveau 4 (6 joueurs-matchs de plus) : 12 pages |
| 6 (focus offensif) | 30 joueurs-quarts Primary ; 2 en v5 | **7 amicaux de plus** avec un joueur Primary dans chaque quart (4 joueurs-quarts par match) : 28 pages |
| 7 (rythme) | rien : valeur constante de 50 possessions par quart | aucune page |
| 8 (terrain) | 194 entre-deux par groupe (1 par match) ; 58 000 à 182 000 tirs | hors de portée avec des matchs réels |

Les amicaux v4 (11/10 au 27/10) ne grossissent plus : le moteur des amicaux est v5 depuis le 28/10. Pour la ligue v4 (3 matchs à nous avec réglages), la même liste vaut mais à raison de 3 matchs par semaine. Restent aussi à exporter les 35 matchs de ligue v4 terminés sans box score (8 dans ma division, listés au 1a, 9 et 18 dans les deux autres) : 2 pages par match (`period-box`, `play-by-play`), soit 70 pages, qui n'aident que les chiffres 4, 7 et 8.

### (c) Faisabilité d'un simulateur possession par possession
- **Déjà connu (fixé ou observé)** : 50 possessions par quart-temps (les deux équipes), 4 quarts ; un cinq par quart pour chaque équipe (nos matchs : les deux compositions ; remplacements seulement pour fautes, blessures, indisponibilités : 141 événements sur 78 matchs) ; chaque possession finit par un tir, une perte de balle ou des lancers francs ([M§7.3]) ; 25 types d'événements ; type et zone de chaque tir (coordonnées `shot_x`, `shot_y`) ; part de tirs à 3 points par niveau de tir (10 à 17 % au niveau 0, 41 à 47 % au niveau 2, 63 à 66 % aux niveaux 3 et 4) ; tirs par quart par niveau de focus (rapport 1,47 en v3) ; pénalités annoncées de fatigue et de minutes lourdes ; écart d'horloge moyen de 6,8 à 7,2 s entre événements.
- **À estimer** : réussite par type de tir en fonction des compétences du tireur et du défenseur, de la passe, de l'athlétisme, de la taille et du poids (environ 15 paramètres) ; fautes sur tir (niveau et pente d'agressivité) ; rebonds offensifs et défensifs ; pertes de balle, interceptions, contres ; lancers francs ; effet de la fatigue et des minutes lourdes sur ces probabilités ; avantage du terrain ; au total de l'ordre de 40 à 60 paramètres.
- **Ce qui manque pour estimer** : les compétences et réglages des adversaires (fourchettes de 20 points pour 17 matchs seulement, aucun réglage) ; les 13 283 tirs de la base, dont 2 620 seulement sont de nos joueurs avec compétences, répartis sur cinq groupes de moteur : 839 en v5 amical, 235 en ligue v4. Pour estimer une pente de compétence à ± 2 points de réussite, il faut 871 à 9 470 tirs par type et par moteur (question 1) : de l'ordre de 30 à 100 matchs à nous détaillés par moteur.
- **Validation prévue** : rejouer chacun de nos matchs 1 000 fois avec les compositions et réglages réels (adversaire inconnu : réglages moyens, compétences au milieu de la fourchette) ; couverture : au moins 85 % des marges réelles dans l'intervalle central à 90 % des marges simulées ; calibration des probabilités de victoire par décile (au moins 40 matchs par moteur pour voir un écart de 10 points) ; comparaison des possessions, de la part de tirs à 3 points, des fautes sur tir et des lancers francs simulés aux valeurs observées.
- **Nombre de matchs détaillés nécessaires** : au moins 40 de nos matchs par moteur avec les quatre pages et la page Équipe du jour (aujourd'hui : v5 amical 10, ligue v4 3, v4 amical 15, ligue v3 22 mais sans compétences avant le 16/10) ; soit de l'ordre de 30 amicaux v5 de plus (environ un mois à raison d'un par jour) ou de 12 semaines de ligue v4.
- **Verdict de faisabilité** : un simulateur de structure est faisable dès maintenant (rythme fixe, compositions, sélection de tirs) ; **un simulateur calibré sur les compétences n'est pas faisable avec les données actuelles**, parce que les pentes de compétence du chiffre 1 ne sont identifiables que pour une seule famille de tirs (3 points, v5). Il le devient avec environ 30 à 40 matchs détaillés de plus pour la partie « nos tirs », mais **pas pour la défense adverse** (compétences adverses inconnues). Le jeu publie une probabilité de victoire (`estimated_chance`, 49 à 57 % sur 27 pages) qui pourrait servir de point de comparaison : elle varie très peu.

## Annexe A : requêtes et sorties de l'étape 1

Commande de l'inventaire (groupes, événements, compositions, compétences de nos joueurs) : `python -I pipelines/etude_evenements_basketvibe.py inventaire` (10,6 s, code 0 ; sortie en tableaux ci-dessus).

Requête 1a (matchs par division) : `select substring(a.endpoint from '^/leagues/([0-9a-f-]{8})') division, count(distinct f->>'id') fixtures, count(distinct f->>'id') filter (where f->>'status'='finished') termines, count(distinct f->>'id') filter (where f->>'status'='finished' and exists (select 1 from silver.bv_matches m where m.fixture_id = (f->>'id')::uuid)) avec_box from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/[0-9a-f-]{36}/seasons/[0-9a-f-]{36}/fixtures$' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8' group by 1 order by 1` : `45caebc5 132 18 0` ; `5fdd980c 132 18 10` ; `a7250ea5 132 18 9`.

Requête 1a bis (8 matchs manquants de ma division) : `select x.round_number journee, x.match_day jour, x.home_team domicile, x.away_team exterieur from silver.bv_fixtures x where x.season_id = '86a63498-c133-44ea-aedb-f1310ad51ae8' and x.fixture_id in (select (f->>'id')::uuid from silver.bv_api a cross join lateral jsonb_array_elements(a.body->'fixtures') f where a.endpoint ~ '^/leagues/5fdd980c-032b-4ea3-b608-5eadc0c61f44/seasons/' and a.body->>'season_id' = '86a63498-c133-44ea-aedb-f1310ad51ae8') and x.status = 'finished' and not exists (select 1 from silver.bv_matches m where m.fixture_id = x.fixture_id) order by x.match_day, x.home_team` : 8 lignes (tableau du 1a).

Requête 1b (détails et coordonnées des tirs) : `select kind, detail, count(*) n, count(shot_x) avec_coord, sum(is_three::int) trois from silver.bv_match_events group by 1,2 order by 1, 3 desc` : 25 types ; champs du `payload` par type : `select kind, k, count(*) n from silver.bv_match_events e, jsonb_object_keys(e.payload) k group by 1,2 order by 1, 3 desc` (tir : `sx`, `sy`, `player_ids`, `shot_coords_version`, `putback`, `dunk`, `alley_oop`, `buzzer`, `heave`, `shot_zone` ; faute : `ft_count`, `bonus` ; lancer : `ft_att`, `ft_made` ; entre-deux : `side` ; revirement : `channel`).

Requête 1c (types de pages) : `select regexp_replace(endpoint, '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', 'ID', 'g') motif, count(*) pages, min(captured_at)::date du, max(captured_at)::date au from silver.bv_api group by 1 order by 2 desc` ; Preview par type : `select body->>'kind' kind, count(*) pages from silver.bv_api where endpoint ~ '/preview$' group by 1` : `finished 86`, `scheduled_lineups 27` ; échantillon des pages terminées : `select count(*) pages_terminees, count(distinct a.body->>'fixture_id') matchs, sum(jsonb_array_length(a.body->'players')) joueurs_lignes, sum((select count(*) from jsonb_array_elements(a.body->'players') p where p ? 'skills' or p ? 'skill_brackets' or p ? 'skills_visibility')) avec_competences from silver.bv_api a where a.endpoint ~ '/preview$' and a.body->>'kind'='finished'` : `86 78 2277 0` ; fourchettes des matchs à venir : `select p->'skill_brackets' ... where a.body->>'kind'='scheduled_lineups'` : exemple `{"defense": {"min": 41, "max": 60}, "passing": {"min": 21, "max": 40}, ...}` ; visibilité : `bracket` 334 lignes, `full` 443 lignes.

## Annexe B : sortie complète des calculs (étape 3)

Commande : `python -I pipelines/etude_evenements_basketvibe.py calculs` (12 s, code 0), le 2026-11-09. Les titres de la sortie sont descendus d'un niveau.


#### 1. Réussite d'un tir selon le type et la compétence du tireur (nos joueurs)

Classement des tirs à 2 non étiquetés par `shot_y` : seuil Y0 = 220, exactitude sur les tirs étiquetés = 90.3 % (retenu).

| groupe | type de tir | tirs | matchs | pente compétence nommée (points / +10) | pente non nommée (points / +10) | n requis (tirs) | verdict |
|---|---|---|---|---|---|---|---|
| v3 ligue | cercle | 172 | 5 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v3 ligue | mi | 129 | 5 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v3 ligue | 3 | 127 | 5 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 ligue | cercle | 89 | 3 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 ligue | mi | 54 | 3 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 ligue | 3 | 92 | 3 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 coupe | cercle | 54 | 2 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 coupe | mi | 48 | 2 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 coupe | 3 | 55 | 2 | — | — | — | nommée : non identifiable ; non nommée : non identifiable |
| v4 amical | cercle | 313 | 12 | 6.81 [4.02 ; 9.01] | 1.22 [-3.63 ; 6.85] | 930 | nommée : non identifiable ; non nommée : non identifiable |
| v4 amical | mi | 293 | 12 | -2.09 [-6.11 ; 1.32] | 8.63 [1.36 ; 14.77] | 1971 | nommée : non identifiable ; non nommée : en écart |
| v4 amical | 3 | 355 | 12 | 1.90 [-6.04 ; 8.45] | -0.14 [-4.86 ; 5.18] | 9470 | nommée : non identifiable ; non nommée : non identifiable |
| v5 amical | cercle | 256 | 10 | 2.54 [-3.90 ; 8.27] | -1.37 [-9.29 ; 6.02] | 4867 | nommée : non identifiable ; non nommée : non identifiable |
| v5 amical | mi | 236 | 10 | 2.32 [-2.89 ; 7.20] | 6.01 [-2.04 ; 12.93] | 3091 | nommée : non identifiable ; non nommée : non identifiable |
| v5 amical | 3 | 347 | 10 | 2.32 [0.61 ; 5.06] | -2.62 [-6.07 ; 0.05] | 871 | nommée : non identifiable ; non nommée : non identifiable |

#### 2. Tirs provoquant une faute selon l'agressivité défensive

| groupe | tirs adverses + fautes | matchs | pente (points par niveau) | annoncée | n requis (tirs) | taux par tranche d'exposition | identifiabilité | verdict |
|---|---|---|---|---|---|---|---|---|
| v3 ligue | 2037 | 22 | 1.76 [-0.04 ; 3.47] | 0.0 | 12482 | moins de 1 : 433 tirs, 6.5 % (moins de 8 matchs) ; de 1 à 3 : 1604 tirs, 9.7 [8.5 ; 11.0] % ; plus de 3 : 0 tirs | tranches insuffisantes (3 tranches de 150 tirs requises) | non identifiable |
| v4 ligue | 286 | 3 | — | 2.25 | — | moins de 1 : 193 tirs, 8.8 % (moins de 8 matchs) ; de 1 à 3 : 93 tirs, 10.8 % (moins de 8 matchs) ; plus de 3 : 0 tirs | tranches insuffisantes (3 tranches de 150 tirs requises) | non identifiable |
| v4 coupe | 91 | 1 | — | 2.25 | — | moins de 1 : 0 tirs ; de 1 à 3 : 91 tirs, 9.9 % (moins de 8 matchs) ; plus de 3 : 0 tirs | tranches insuffisantes (3 tranches de 150 tirs requises) | non identifiable |
| v4 amical | 1348 | 14 | 1.01 [-0.35 ; 1.60] | 2.25 | 2553 | moins de 1 : 888 tirs, 6.6 [5.1 ; 8.3] % ; de 1 à 3 : 292 tirs, 6.5 % (moins de 8 matchs) ; plus de 3 : 168 tirs, 11.9 % (moins de 8 matchs) | identifiable | en écart |
| v5 amical | 859 | 9 | -2.12 [-6.23 ; 1.48] | 2.25 | 26452 | moins de 1 : 859 tirs, 6.5 [5.2 ; 8.0] % ; de 1 à 3 : 0 tirs ; plus de 3 : 0 tirs | tranches insuffisantes (3 tranches de 150 tirs requises) | non identifiable |

#### 3. Fatigue : réussite et pertes de balle

| groupe | tirs | pente de la réussite (points / +10 de fatigue) | fatigue maximale observée | effet annoncé à cette fatigue | effet détectable à cette fatigue (points) | paliers | verdict |
|---|---|---|---|---|---|---|---|
| v3 ligue | 428 | — | 24.63 | 4.6 % soit -2.28 point de réussite | — | 27 tirs à fatigue ≥ 20 ; paliers atteints : [20] | non identifiable |
| v4 ligue | 235 | — | 8.84 | 1.8 % soit -0.90 point de réussite | — | 0 tirs à fatigue ≥ 20 ; paliers atteints : aucun | non identifiable |
| v4 coupe | 157 | — | 0.47 | 0.1 % soit -0.05 point de réussite | — | 0 tirs à fatigue ≥ 20 ; paliers atteints : aucun | non identifiable |
| v4 amical | 961 | -0.52 [-4.51 ; 4.34] | 24.63 | 6.5 % soit -3.24 point de réussite | 15.51 | 43 tirs à fatigue ≥ 20 ; paliers atteints : [20] | non identifiable |
| v5 amical | 839 | 2.41 [-17.10 ; 28.76] | 8.84 | 1.8 % soit -0.77 point de réussite | 34.40 | 0 tirs à fatigue ≥ 20 ; paliers atteints : aucun | non identifiable |

Pertes de balle par joueur-quart (box score), pente par +10 de fatigue :

| groupe | joueurs-quarts | pente (pertes de balle par quart / +10 de fatigue) | verdict |
|---|---|---|---|
| v3 ligue | 99 | — | non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante) |
| v4 ligue | 61 | — | non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante) |
| v4 coupe | 40 | — | non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante) |
| v4 amical | 244 | -0.023 [-0.186 ; 0.191] | non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante) |
| v5 amical | 200 | 0.311 [-0.486 ; 0.786] | non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante) |

#### 4. Pénalité au-delà de 36 minutes au dernier quart

| groupe | tirs par cellule | différence de différences de réussite (points) [intervalle] | n requis (tirs) | verdict (annoncé : entre −9 et 0) |
|---|---|---|---|---|
| v3 ligue | 445 (Q4 lourds) ; 420 (Q4 contrôle) ; 1434 (Q1-3 lourds) ; 1217 (Q1-3 contrôle) | 0.16 [-5.66 ; 5.70] | 26309 | non identifiable |
| v4 ligue | 108 (Q4 lourds) ; 590 (Q4 contrôle) ; 570 (Q1-3 lourds) ; 1686 (Q1-3 contrôle) | -6.96 [-18.69 ; 6.43] | 109949 | non identifiable |
| v4 coupe | 78 (Q4 lourds) ; 301 (Q4 contrôle) ; 306 (Q1-3 lourds) ; 834 (Q1-3 contrôle) | -9.12 [-22.87 ; 6.49] | 64227 | non identifiable |
| v4 amical | 145 (Q4 lourds) ; 475 (Q4 contrôle) ; 641 (Q1-3 lourds) ; 1256 (Q1-3 contrôle) | -14.24 [-22.03 ; -5.81] | 35630 | non identifiable |
| v5 amical | 99 (Q4 lourds) ; 245 (Q4 contrôle) ; 526 (Q1-3 lourds) ; 773 (Q1-3 contrôle) | -6.99 [-18.90 ; 5.01] | 50498 | non identifiable |

#### 5. Part de tirs à 3 points selon le focus de tir

| groupe | niveau de tir | joueurs-matchs (≥ 8 tirs) | part de tirs à 3 points [intervalle] | verdict (niveau 4 : annoncé ≤ 66,7 % et ≤ 50 %) |
|---|---|---|---|---|
| v3 ligue | 0 | 24 | 10.1 [7.6 ; 14.2] % | — |
| v3 ligue | 2 | 78 | 47.2 [44.6 ; 49.6] % | — |
| v3 ligue | 3 | 5 | — | — |
| v3 ligue | 4 | 8 | 65.4 [58.2 ; 72.3] % | plafond 66,7 % : non identifiable ; plafond 50 % : non identifiable |
| v4 ligue | 0 | 6 | — | — |
| v4 ligue | 2 | 4 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 ligue | 3 | 0 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 ligue | 4 | 3 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 coupe | 0 | 2 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 coupe | 2 | 1 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 coupe | 3 | 0 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 coupe | 4 | 1 | — | non identifiable (moins de 5 joueurs-matchs) |
| v4 amical | 0 | 34 | 14.3 [12.1 ; 16.9] % | — |
| v4 amical | 2 | 17 | 40.6 [33.7 ; 47.7] % | — |
| v4 amical | 3 | 10 | 63.1 [56.1 ; 70.7] % | — |
| v4 amical | 4 | 12 | 65.5 [59.1 ; 71.9] % | plafond 66,7 % : non identifiable ; plafond 50 % : non identifiable |
| v5 amical | 0 | 16 | 16.6 [12.9 ; 20.8] % | — |
| v5 amical | 2 | 22 | 42.4 [35.7 ; 47.6] % | — |
| v5 amical | 3 | 0 | — | non identifiable (moins de 5 joueurs-matchs) |
| v5 amical | 4 | 9 | — | non identifiable |

Part de tirs à 3 points de l'équipe par match (les deux équipes de chaque match) :

| groupe | équipes-matchs | moyenne (%) | 95e centile (%) | maximum (%) | équipes-matchs au-dessus de 50 % |
|---|---|---|---|---|---|
| v3 ligue | 44 | 39.7 | 53.5 | 54.7 | 5 |
| v4 ligue | 38 | 33.2 | 53.1 | 54.2 | 4 |
| v4 coupe | 20 | 30.6 | 47.0 | 50.6 | 1 |
| v4 amical | 32 | 36.9 | 48.8 | 53.4 | 1 |
| v5 amical | 20 | 41.7 | 51.3 | 52.3 | 2 |

#### 6. Tirs par quart selon le focus offensif

| groupe | joueurs-quarts Primary (niveau 4) | joueurs-quarts Normal (niveau 2) | rapport des tirs par quart, Primary / Normal [intervalle] | verdict (annoncé 1,33) |
|---|---|---|---|---|
| v3 ligue | 16 | 334 | 1.47 [1.27 ; 1.70] | non identifiable (moins de 30 joueurs-quarts au niveau 4) |
| v4 ligue | 9 | 15 | — | non identifiable (moins de 30 joueurs-quarts au niveau 4) |
| v4 coupe | 4 | 1 | — | non identifiable (moins de 5 joueurs-quarts au niveau 4 ou 2) |
| v4 amical | 0 | 90 | — | non identifiable (moins de 5 joueurs-quarts au niveau 4 ou 2) |
| v5 amical | 2 | 91 | — | non identifiable (moins de 5 joueurs-quarts au niveau 4 ou 2) |

#### 7. Rythme

| groupe | équipes-matchs | possessions par équipe et par match [intervalle] |
|---|---|---|
| v3 ligue | 44 | 100.5 [100.1 ; 100.9] |
| v4 ligue | 38 | 100.3 [99.9 ; 100.7] |
| v4 coupe | 20 | 100.8 [100.0 ; 101.7] |
| v4 amical | 31 | 100.9 [100.3 ; 101.5] |
| v5 amical | 20 | 102.2 [101.2 ; 103.1] |

Comparaison entre moteurs (deux groupes sans mélange) :

- v4 ligue − v3 ligue : -0.2 possessions [-0.8 ; +0.3] par équipe et par match (effet minimal 3).
- v5 amical − v4 amical : +1.3 possessions [+0.1 ; +2.5] par équipe et par match (effet minimal 3).

Écarts d'horloge entre événements consécutifs d'un quart (hors début et fin de quart, balle morte, remplacements, entre-deux) :

| groupe | écarts | part des écarts de plus de 24 s [intervalle] | écart moyen [intervalle] | écart maximal (s) | restes modulo 6 s |
|---|---|---|---|---|---|
| v3 ligue | 8830 | 2.05 [1.81 ; 2.29] % | 7.0 [6.8 ; 7.1] s | 48 | [0, 1, 2, 3] |
| v4 ligue | 7690 | 1.91 [1.64 ; 2.16] % | 6.9 [6.8 ; 7.0] s | 42 | [0, 1, 2, 3] |
| v4 coupe | 4116 | 2.11 [1.61 ; 2.67] % | 6.8 [6.6 ; 7.0] s | 41 | [0, 1, 2, 3] |
| v4 amical | 6485 | 2.04 [1.74 ; 2.33] % | 6.9 [6.8 ; 7.0] s | 41 | [0, 1, 2, 3] |
| v5 amical | 3981 | 0.00 [0.00 ; 0.00] % | 7.2 [7.0 ; 7.3] s | 17 | [0, 1, 2, 3] |

#### 8. Avantage du terrain

Lecture de `payload.side` : le camp du premier tir qui suit l'entre-deux est le même dans 77 % des 78 entre-deux ; part de `home` : 49 % des 78.

| groupe | entre-deux | (a) gagnés par l'équipe qui reçoit | tirs | (b) réussite à domicile moins à l'extérieur [intervalle] | n requis (tirs) | verdict |
|---|---|---|---|---|---|---|
| v3 ligue | 22 | 13 sur 22 (p exact 0.523) | 3606 | 1.54 [-3.74 ; 7.06] points | 94210 | non identifiable (moins de 194 entre-deux) ; (b) non identifiable |
| v4 ligue | 19 | 8 sur 19 (p exact 0.648) | 3050 | -0.01 [-8.03 ; 8.22] points | 181581 | non identifiable (moins de 194 entre-deux) ; (b) non identifiable |
| v4 coupe | 10 | 4 sur 10 (p exact 0.754) | 1545 | -3.31 [-9.95 ; 2.89] points | 57045 | non identifiable (moins de 194 entre-deux) ; (b) non identifiable |
| v4 amical | 16 | 8 sur 16 (p exact 1.000) | 2672 | 1.57 [-3.94 ; 7.32] points | 78332 | non identifiable (moins de 194 entre-deux) ; (b) non identifiable |
| v5 amical | 10 | 4 sur 10 (p exact 0.754) | 1707 | 3.29 [-2.70 ; 9.68] points | 60381 | non identifiable (moins de 194 entre-deux) ; (b) non identifiable |

La lecture de `payload.side` n'est pas confirmée par le premier tir : le point (a) est non identifiable dans tous les groupes.

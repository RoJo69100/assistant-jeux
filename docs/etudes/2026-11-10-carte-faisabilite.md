# Carte de faisabilité BasketVibe (2026-11-10)

**Question** : pour chaque question de la demande, ce qu'on peut mesurer aujourd'hui dans les groupes de moteur ouverts (v4 ligue, v5 amical) : n disponible, n requis pour l'effet minimal, délai au rythme actuel, verdict. Pour 1a et 1b, la mesure elle-même.
**Méthode du n requis** : celle de l'étude des 3 points (`docs/etudes/2026-11-10-trois-points-competence.md`) : erreur type supposée proportionnelle à 1/racine(n), puissance 50 %, n = n0 × (1,96 × ET0 / effet minimal)². Pour deux bras neufs : n par bras = 2 × (1,96 × sigma / effet)².
**Règle de verdict** : « faisable maintenant » si n disponible ≥ n requis, ou si l'IC à 95 % exclut déjà zéro (l'effet est plus grand que l'effet minimal). Moins de 8 matchs dans un groupe : pas d'intervalle.
**Rythme** : 12 amicaux v5 du 29/10 au 09/11, soit 1,00 par jour ; 4 matchs de ligue v4 joués, 18 journées programmées du 11/11 au 21/12 (22 au total).
**Groupes** : les questions 2 à 5 ne portent pas sur le moteur de match, donc `groupe()` ne s'y applique pas. Le marché est découpé par saison (≤ 26/10, ≥ 27/10).

## Tableau

| Question | n disponible | n requis | délai | Verdict |
|---|---|---|---|---|
| 1a fatigue d'un amical v5 (k_am) | 10 amicaux v5, 7 intervalles de relevés, 104 joueurs-intervalles | 2 amicaux (effet minimal 0,10) | 0 | faisable maintenant |
| 1a comparaison avec la ligue v4 (D = k_lg − k_am) | 4 matchs de ligue v4 | 8 (plancher ; 3 d'après l'ET, tirée de moins de 8 matchs) | 9 jours (matchs des 11, 14, 16 et 18/11, puis le relevé du 19/11) | dans 9 jours |
| 1b blessures en amical v5, par minute | 12 amicaux, 5 760 minutes-joueur, 0 blessure | 31 amicaux (14 748 min) pour exclure un taux ≥ 25 % de celui de la ligue | 19 jours | dans 19 jours |
| 1c focus défensif adverse | 0 réglage adverse sur 53 lignes | 66 amicaux v5 ; 49 de nos matchs de ligue (la saison n'en compte que 22) | v5 : 66 jours après l'export ; ligue : au-delà de la saison | bloquée par : exporte les réglages utilisés vus côté adversaire |
| 1d E1 agressivité (réussite adverse) | 0 amical de la file | 24 (12 par niveau) | 24 jours | dans 24 jours |
| 1d E5 zone (réussite adverse à 2 points) | 0 | 39 (13 par zone) | 39 jours | dans 39 jours |
| 1d E2 focus de tir (tirs à 3 points tentés) | 0 | 8 (4 par niveau) | 8 jours | dans 8 jours |
| 1d E3 Primary (tirs par quart du joueur désigné) | 0 | 16 (8 par niveau) | 16 jours | dans 16 jours |
| 1d E4 habituel (pente 3 points / compétence) | 12 amicaux v5, 423 tirs | 11 | 0 | faisable maintenant (résultat : indéterminé) |
| 1d file E1+E5+E2+E3 à la suite | 0 | 87 | 87 jours | dans 87 jours |
| 2 prix : PS et âge | 345 ventes en saison 2, 148 en saison 1 (hors agents libres) | effet détecté | 0 | faisable maintenant |
| 2 prix : poste | 345 ventes en saison 2 | 9 204 à 37 953 ventes (effet minimal 10 %) | 334 à 1 418 jours de vente | dans 334 jours |
| 3a force du club et victoires | 36 équipes, 120 équipes-matchs (3,33 matchs par équipe) | 4 matchs par équipe ; effet détecté | 0 | faisable maintenant |
| 3b pourquoi les premiers le sont (compétences, tactique) | compétences : 1 équipe (la nôtre) ; tactique adverse : 0 | - | - | bloquée par : exporte la page Équipe des clubs de tête |
| 4a rendement d'un achat-revente (marché) | 99 reventes sur 25 jours | 572 (médiane, effet minimal 10 pts) ; effet détecté | 0 | faisable maintenant |
| 4b usage de notre argent et rendement | 1 club, 5 semaines, 2 saisons | non calculable : aucune variation entre clubs | - | bloquée par : une seule équipe observée (aucun export connu ne la lève) |
| 5a entraînement principal contre secondaire | 34 gains, 15 joueurs, 2 semaines | 4 semaines ; effet détecté | 0 | faisable maintenant |
| 5b personnel | 4 semaines, 2 configurations (la même depuis le 19/10), 0 blessure chez nous | non calculable | - | bloquée par : une seule configuration observée (aucun export ne la lève) |
| 5c académie | 4 semaines, 1 niveau d'investissement (100 000) | non calculable | - | bloquée par : un seul niveau d'investissement observé (aucun export ne la lève) |

## Mesures 1a et 1b

| groupe | n événements | n matchs | estimé | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|
| 1a v5 amical : k_am (part du gain de la formule ligue du manuel) | 104 joueurs-intervalles | 10 | +0,076 (≈ +0,16 point de fatigue par 10 min) | [+0,032 ; +0,113] (≈ [+0,07 ; +0,23] point par 10 min) | régression avec effet fixe par intervalle, bootstrap par grappes d'intervalles (chaque match est dans un seul intervalle), 2000 tirages, graine 20261110 | association présente : environ 1/10 de la ligue, comme le manuel |
| 1a v4 ligue : k_lg | 104 joueurs-intervalles | 4 | +0,83 | - | même modèle | indéterminé : n trop petit (< 8 matchs) |
| 1b v5 amical | 0 blessure / 5 760 min | 12 | 0 pour 1000 min | [0 ; 0,666] | Wilson (par minute-joueur) | indéterminé : n trop petit (31 amicaux requis) |
| 1b v4 ligue (référence) | 10 blessures / 9 600 min | 20 (deux camps) | 1,042 pour 1000 min | [0,566 ; 1,917] | Wilson | association présente |
| 1b différence v5 amical − v4 ligue | - | 12 et 20 | −1,042 pour 1000 min | [−1,771 ; −0,312] | bootstrap par matchs dans chaque groupe, 2000 tirages, graine 20261110 | association présente : moins de blessures en amical v5 |
| 1b v4 amical (groupe fermé, en complément) | 0 / 7 440 min | 16 | 0 | [0 ; 0,516] | Wilson | n définitif (groupe fermé) |

- 1a, le manuel attend k_am ≈ 0,1 et k_lg ≈ 1 (`basketvibe-joueurs/references/06-fatigue-0100.md`, [M§5.6]). Repère : avec la formule ligue, une défense équilibrée et l'endurance moyenne de l'effectif, on attend 2,06 points de fatigue par 10 minutes.
- 1b : aujourd'hui, la borne haute du taux en amical v5 vaut 64 % du taux de ligue v4 observé (50 % en v4 amical). Les 28 amicaux v4 et v5 sans blessure s'accordent aussi bien avec le manuel (« aucune ») qu'avec un taux faible non nul (News du 2026-10-19). On ne peut pas trancher. Recoupement : 0 date de retour de blessure sur les 137 relevés quotidiens de nos joueurs depuis le 28/10. Les aperçus d'amicaux ont `injuries` vide ou nul.

## Sources (exécutées ce tour)
- `python -I pipelines/etudes/carte_faisabilite.py 2000 20261110 coup` (script `pipelines/etudes/carte_faisabilite.py`) : tous les chiffres du tableau.
- `python -I pipelines/etudes/carte_faisabilite.py 2000 20261110 tick` : contrôle de la règle d'horodatage de 1a.
- `python -I pipelines/etudes/carte_faisabilite_marche_seuil.py 1000 2000 20261110` : sensibilité de la question 2.
- Requêtes `sql.py` d'inventaire :
  - matchs par jour et `my_result` depuis le 11/10 ;
  - `silver.bv_fixtures` programmés ;
  - heures de capture des relevés `overview` (`silver.bv_api`) et de `bronze.raw_pages` ;
  - `kind` injury dans `silver.bv_match_events` ;
  - clés de `silver.bv_fixture_api` (`match-tactics-used` : 53 lignes, toutes `viewer_is_primary` = true) ;
  - `injuries` des aperçus ;
  - `skills_visibility` des aperçus ;
  - `silver.bv_player_overview` (1 équipe) ;
  - `gold.bv_transfer_history` (58 ventes sous 1 000) ;
  - `silver.bv_standings_weekly` ;
  - finances, personnel, académie ;
  - `gold.bv_training_gains_exact` par semaine (gains : 120/120 le 18/10, 16/136 le 25/10, 0/128 le 01/11, 0/112 le 08/11) ;
  - amical v5 sans réglages utilisés (29/10, Chomelix Cow contre BC Statyba Telsiai).

## Limites
- **1a, horodatage.**
  - Règle retenue : un match compte dans l'intervalle de relevés qui contient son coup d'envoi (heure de Paris).
  - La variante « jour suivant » est exclue : 5 joueurs sans minute y auraient pris +5,68 de fatigue entre le 08/11 et le 09/11, ce qui est impossible sans match.
  - Hypothèse : la fatigue s'applique au coup d'envoi. Elle serait infirmée par un relevé pris entre 8 h et 20 h un jour de ligue qui ne montrerait pas la fatigue de l'amical du matin.
- **1a, modèle.** k_am (v5) et k_lg (v4) sont deux paramètres distincts, sans chiffre global. Le terme de récupération est commun aux deux : c'est une hypothèse.
- **1a, récupération.** Les joueurs restés au repos dans les intervalles amicaux ont une variation proche de 0, alors que le manuel annonce 0,5 + 10 % par nuit. C'est une hypothèse à vérifier sur des joueurs plus fatigués.
- **1a, données manquantes.** 31 joueurs-matchs n'ont pas de niveau d'agressivité ; on leur applique le multiplicateur 1,0.
- **1a, confusion.** Les mêmes titulaires jouent la ligue et de longues minutes en amical. Chaque jour de ligue a aussi un amical à 8 h.
- **1b.** Wilson par minute-joueur suppose des minutes indépendantes ; c'est une approximation pour un taux rare. Confusion possible : les minutes et l'agressivité diffèrent entre amical et ligue.
- **1c.** Le n requis est simulé avec une cible tirée au hasard parmi les 5 plus gros tireurs. Le vrai focus porte un niveau par joueur.
- **1d.**
  - Les mesures retenues sont des choix de l'étude, pas des règles du jeu :
    - E1 : réussite adverse ;
    - E5 : réussite adverse à 2 points ;
    - E2 : tirs à 3 points tentés, effet minimal 5 ;
    - E3 : +30 % de tirs par quart, quarts supposés indépendants ;
    - E4 : 3 pts par +10 de compétence.
  - Les références B de E2 et E3 ne sont pas « déjà en base ». Dans chacun des 11 amicaux v5 qui ont leurs réglages, 1 ou 2 joueurs jouaient au tir cran 4 et 1 joueur au focus offensif cran 4. Le niveau B doit donc être joué aussi ; il est compté dans le n requis.
  - L'agressivité observée en v5 est aux crans 0 et 2 ; le cran 4 de E1 n'a jamais été joué.
  - Les `amicaux_vises` du fichier `docs/attentes/experiences-amicales-basketvibe.yaml` (4, 3, 3, 7) sont inférieurs aux n requis (24, 39, 8, 16).
  - E4 : pente +1,2 pt par +10, IC [−1,5 ; +4,0], donc indéterminé.
- **2. Prix.**
  - Les ordres de grandeur dépendent des ventes à prix symbolique (58 sous 1 000). Sans elles, en saison 2 :
    - +5 PS : +440 % [+365 ; +508] ;
    - +1 an : −26 % [−29 ; −24] ;
    - C contre PG : +85 % [+19 ; +185] (non significatif dans le modèle principal).
  - Le sens de l'effet de PS et d'âge est robuste ; l'effet du poste ne l'est pas.
  - Confusion probable : potentiel, compétences au-delà du PS, dynamique d'enchère.
- **3a.** Pente de +0,154 de part de victoires par écart type de force, IC [+0,094 ; +0,296], bootstrap par équipes. Limites :
  - les victoires viennent du classement, pas de `my_result` (qui n'existe que pour nos matchs) ;
  - la force est relevée le 09/11, pas au jour de chaque match ;
  - hypothèse : les 36 équipes jouent toutes avec le moteur v4.
- **4a.**
  - Rendement net médian d'une revente : +18,8 %, IC [+3,3 ; +47,2], bootstrap par jour.
  - Part des reventes en gain : 63,6 %, Wilson [53,8 ; 72,4].
  - La moyenne n'a pas de sens : des achats à 1 la tirent vers le haut.
- **5a.** Écart principal − secondaire : +0,518 par semaine, IC [+0,295 ; +0,795]. C'est déjà la règle du manuel (secondaire = moitié de la principale, [M§8.2], `sql/gold/005_bv_training.sql`). Seules 2 semaines ont des gains.
- **4b, 5b, 5c.** Il n'existe aucun contraste à mesurer : un seul club, une seule configuration, un seul niveau. Seul un changement de réglage par l'utilisateur en créerait un, et cette décision ne relève pas de l'étude.

## Export demandé
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Effectif les jours de ligue entre l'amical de 8 h et le match de 20 h, puis après le match de ligue, parce que les 4 intervalles de relevés qui contiennent un match de ligue v4 contiennent aussi 1 ou 2 amicaux, et que la colonne `fatigue` n'y est relevée qu'au début et à la fin. Note : `silver.bv_player_daily` ne garde que la dernière capture du jour (`sql/silver/001_bv_players.sql`, ligne 5) ; la capture de mi-journée se lira dans `silver.bv_api`.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés d'un match vue côté adversaire (si le jeu l'affiche), parce que le `defensive_focus` adverse est absent : 0 ligne adverse sur 53 dans `silver.bv_match_tactics`, toutes les captures `match-tactics-used` ont `viewer_is_primary` = true. Hypothèse : cette page existe. Si le jeu ne la montre pas, la question 1c est hors d'atteinte.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Équipe (effectif) des clubs de tête du classement, parce que les compétences de leurs joueurs manquent : `silver.bv_player_overview` ne contient que notre équipe, et les aperçus de match ne donnent au mieux que des fourchettes (`skill_brackets`). Hypothèse : cette page montre les compétences d'un club adverse.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Entraînement chaque semaine, juste avant et juste après l'entraînement, parce que les compétences à une décimale (`*_exact`) manquent dans les relevés hebdomadaires du 01/11 et du 08/11 (0 gain calculé sur 128 et 112 lignes de `gold.bv_training_gains_exact`). Hypothèse sur le moment de l'entraînement, non vérifiée ici.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés de l'amical du 29/10 (Chomelix Cow contre BC Statyba Telsiai), parce que c'est le seul amical v5 sans `player_directives` ni `defensive_focus` en base.

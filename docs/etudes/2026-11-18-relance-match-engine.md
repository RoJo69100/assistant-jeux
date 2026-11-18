# BasketVibe — relance de l'étude du Match Engine (18/11/2026, 10 h)

Étude, pas de décision. Lecture seule. Relance de `2026-11-16-premier-essai-joueurs-minutes-focus.md` sur la base du 18/11. Aucune règle changée.
Le « 75 en base » du plan du 18/11 n'est pas repris : tous les comptes ci-dessous viennent de requêtes de ce tour.

## 1. Matchs en base (box joueur period 0 + Q1–Q4 + play-by-play), par groupe de moteur
| groupe | à nous | autres clubs | dont complets (nous / autres) | joués depuis le 16/11 en base |
|---|---|---|---|---|
| v4 ligue | 8 | 244 | 7 / 243 | 2 à nous (18/11 non joué ou non exporté), 35 autres |
| v4 coupe | 5 | 28 | 3 / 28 | 0 |
| v5 amical | 21 | — | 19 | 4 (18/11 et 19/11 sans box) |
| v4 amical / v3 | 16 / 23 | — | complets | — |

Périmètre de l'étude (v4 ligue complets) : **250 matchs** (43 le 16/11), 6 ligues de 41–42 matchs, 02/11–16/11, 500 équipes-matchs, 2 prolongations.

| question | seuil | n le 16/11 | n le 18/11 | atteint |
|---|---|---|---|---|
| A pentes compétence → production | 34–100 joueurs par groupe de postes | 34 / 18 / 41 | 112 / 65 / 144 | oui |
| B1 baisse au Q4 (éval/min) | ≈ 110 matchs | 24 | 123 | oui |
| B1 5 × 48 contre rotation | ≥ 8 matchs 5 × 48 ; ≈ 150 par sous-ensemble | 7 | 29 / 95 | 8 oui ; 150 non |
| B2 minutes et marge | IC hors de 0 | 43 matchs | 250 | oui |
| C focus Lock / Intense (v4 ligue, nos matchs) | ≥ 8 matchs par niveau | 3 / 5 | 3 / 5 | non |
| 1a fatigue ligue (D = k_lg − k_am) | 8 matchs de ligue v4 à nous | 4 | 7 complets | non (1 de moins) |
| 1b blessures en amical v5 | 31 amicaux | 12 | 19 complets | non |

## Résultats relancés (v4 ligue, 250 matchs ; graine 20261116, 2 000 tirages)
**A.** Les associations du 16/11 tiennent (deux points → points aux trois postes, passe/dribble → passes des arrières, rebond → rebonds). Nouvelles, en ridge (éval/min) : arrières deux points +0,024 [+0,003 ; +0,044] ; ailiers deux points +0,045 [+0,015 ; +0,068], athlétisme +0,033 [+0,005 ; +0,056] ; intérieurs deux points +0,033 [+0,014 ; +0,052], rebond +0,029 [+0,005 ; +0,051], âge +0,031 [+0,001 ; +0,064]. La forme des arrières (+0,034 le 16/11) ne sort plus. Limites : 1 130 snapshots postérieurs sur 2 017, tranches de 19 points.
**B1.** Baisse au Q4 : éval/min −0,110 [−0,156 ; −0,059], pts/min −0,065 [−0,100 ; −0,030] (386 joueurs-matchs, 123 matchs) : **association présente** (indéterminée le 16/11). Rotation : −0,134 [−0,191 ; −0,071] ; 5 × 48 : −0,072 [−0,151 ; +0,012] indéterminé. Écart 5 × 48 − rotation +0,062 [−0,036 ; +0,160] : indéterminé, ≈ 150 matchs par sous-ensemble requis.
**B2.** +10 pts de part des 5 premiers : −5,33 [−6,85 ; −3,83] sans force, **−1,57 [−3,00 ; −0,19] avec forces** (−4,74 le 16/11). +1 joueur > 36 min : −2,84 [−4,31 ; −1,45] avec forces. La part liée à la force passe d'environ la moitié à environ 70 % ; il reste un effet résiduel faible. Association, pas cause.
**C.** Le script `premier_essai_c_focus.py` dépasse le délai de Supabase sur `gold.bv_match_opp_focus` : comptes lus dans `silver.bv_match_tactics` directement. Nos niveaux en v4 ligue : Lock 3 joueurs-matchs (3 matchs), Intense 8 (5), Light 10 (4), Normal 51 (6) : inchangés depuis le 16/11, pas de recalcul. `silver.bv_match_tactics` : 64 lignes, toutes de notre équipe ; 0 réglage adverse.

## 2. Expériences amicales E1 à E5
Registre `outputs/basketvibe/fait-*.md` : **0 ligne `[expérience=…]`** ; aucune expérience n'est vérifiée au sens du fichier `docs/attentes/experiences-amicales-basketvibe.yaml`. Réglages joués (`gold.bv_amical_reglage`, amicaux depuis le 10/11) :
| exp. | n requis (carte du 10/11) | réglage joué conforme | verdict |
|---|---|---|---|
| E1 agressivité 3 / 5 | 24 (12 par niveau) | A : 1 (14/11) ; B : 0 | n insuffisant |
| E5 zone Perimeter / Middle / Rim | 39 (13 par zone) | Middle 6, Perimeter 1, Rim 0 ; agressivité non uniforme (constantes non tenues) | n insuffisant |
| E2 focus de tir cran 4 sur deux tireurs | 8 (4 par niveau) | 8 amicaux v5 avec ≥ 2 tireurs au cran 4 (04/11–17/11), 11 sans | indéterminé (voir dessous) |
| E3 Primary aux 4 quarts | 16 (8 par niveau) | 0 (1 quart au plus) | n insuffisant |
| E4 habituel | 11 | non démarrée (après E3) | n insuffisant |

E2, mesure indirecte au niveau équipe (pas le protocole : tirs de toute l'équipe, zone Middle et Primary 1 quart en même temps) : 3 pts tentés par match 34,25 (n 8) contre 35,91 (n 11), écart −1,66 [−5,3 ; +1,9] (Welch) ; part des tirs à 3 points 40,3 % contre 40,7 %, écart −0,4 [−4,5 ; +3,7]. Indéterminé ; à refaire au niveau des deux tireurs désignés.

## 3. Entraînement (`gold.bv_training_gains_exact`)
Semaines avec gains exacts : **2 sur 5** (18/10 : 120 lignes, 15 joueurs ; 15/11 : 96 lignes, 12 joueurs). 25/10 : 16 gains sur 136 ; 01/11 et 08/11 : 0.
| entraînement | n | gain moyen mesuré | IC 95 % | attendu (base, [M§8.2]) | verdict |
|---|---|---|---|---|---|
| principal | 27 | +0,971 | [+0,757 ; +1,185] | +1,0 | conforme |
| secondaire | 27 | +0,430 | [+0,322 ; +0,537] | +0,5 | conforme |
Autres compétences : +0,02 (18/10), 0,00 (15/11). L'attendu de base ignore âge, potentiel et ralentissement au-dessus de 70.
Dernière capture : `training` 17/11 21:47 UTC (43 captures), `player_training` 17/11 21:48 UTC, `training_progress` 17/11 17:06 UTC (`bronze.raw_pages`).

## 4. Exports encore nécessaires
- Pour comprendre le Match Engine, j'ai besoin de : exporte les onglets Details, Stats par quart et Play-by-play du match de ligue du 18/11 dès qu'il est joué, parce que 1a demande 8 matchs de ligue v4 à nous et la base en a 7.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page match de chaque match de ligue où nous mettons un adversaire en Lock ou Intense, parce que C demande ≥ 8 matchs par niveau (Lock 3, Intense 5).
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés vue côté adversaire (si le jeu l'affiche), parce que 0 des 64 lignes de `silver.bv_match_tactics` n'est adverse.
- Pour comprendre le Match Engine, j'ai besoin de : exporte les box et le play-by-play des matchs de coupe du 29/10 et du 31/10, parce qu'ils n'ont aucune ligne de box ni d'événement.
- Pour comprendre le Match Engine, j'ai besoin de : exporte les amicaux du 18/11 et du 19/11 une fois joués, parce que 1b demande 31 amicaux v5 complets et la base en a 19.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Entraînement le samedi soir et le dimanche après 04:00, parce que 3 semaines sur 5 n'ont pas de gain exact.
- Hors export : chaque amical joué selon E1 doit avoir sa ligne `[expérience=E1:A|B]` dans le registre, sinon aucune expérience n'avance.

## Sources (exécutées le 18/11, 10 h)
- `python -I pipelines/etudes/premier_essai_a_joueurs.py` (3 requêtes), `premier_essai_b_minutes.py` (3 requêtes) ; `premier_essai_c_focus.py` : délai Supabase dépassé.
- `sql.py` : comptes par groupe sur `silver.bv_matches`, `silver.bv_match_player_stats`, `silver.bv_match_events` ; `silver.bv_match_tactics` ; `gold.bv_amical_reglage` ; `gold.bv_training_gains_exact` ; `bronze.raw_pages`.

# Carte derbymanager — entrainement (un entraînement par groupe GK / DEF / MID / FWD, intensité par joueur ; deux clubs)

Sources lues : commit a0787e7 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `derbymanager-effectif-entrainement` ; connaissance § 5 ; learnings). Consigne du 2026-11-01 : l'intensité est une « action très importante ». Saisie dans l'ordre de l'écran Training (`pipelines/forme.py`, ordre d'entraînement DM).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:46 | caractéristiques à entraîner | var. 1 |
| :47 | suivre le progrès | var. 4 |
| :48 | comprendre le progrès, talent du joueur | var. 2, 3 |
| :49 | mentor | var. 7 |
| :50 | intensité | var. 5 |
| :51 | satisfaction | var. 8 |
| :52 | lien avec le pot | var. 3 |
| :53 | entraînement par poste | var. 1 |

## Rendu (figé)
Un bloc par club : 1) `| Groupe | Entraînement actuel | Conseillé | Compétence clé la plus basse | Niveau d'installation (tec / dec / mov) |` ; 2) `| Joueur | Groupe | Âge | Pot | TR (jours sans match / exigence) | Intensité actuelle | Intensité conseillée | Gains / pertes | Icône |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Entraînement par groupe | `select team_id, groupe, actuel, tec_lvl, dec_lvl, mov_lvl, competence, categorie, moyenne, conseille from gold.dm_entrainement_plan` | Compétence clé la plus basse du groupe ; optimum quand le niveau de l'installation = niveau de la compétence | connaissance § 5 | D Anticipation, M/F First Touch, GK Reaction (C-007) |
| 2 | Loi de croissance | — | Plus la compétence est haute plus c'est dur ; P × (F + C) ; pic d'âge 18-25 ; optimum 2-4 étoiles | dev 2024-11-22, 2025-06-29 | |
| 3 | Potentiel | `pot` (low / med / high = chance du tier suivant) | Niveau max = potentiel + installations ; « Nearing his growth limit at this club » = installations trop basses | connaissance § 5 ; `resume.md` § Pièges | |
| 4 | Gains mesurés | `select club, groupe, name, pos, age, intensity, pot, tr, mentor, gained, lost, solde, price_change, tendance from gold.dm_entrainement order by club, solde limit 40` | Rien gagné : high intensity, sinon trop jeune, passé son pic ou mauvais fit | connaissance § 5 | |
| 5 | Intensité | `intensity` ; `gold.dm_verdict_joueurs` (intensité conseillée) | Low 50 % (+4 % récup.), Med 100 % (+3 %), High 150 % (+2 %) ; HIGH récupère le moins vite | connaissance § 5 (S16) | 10 joueurs en HIGH (30/10) |
| 6 | Training Requirement | `jours_sans_match`, `tr_exigence`, `ne_s_entraine_pas` | TR 3-7 jours ; −1 à ≥ 20 min jouées, −2 à ≥ 45 min, retombe à 1 à ≥ 75 min ; un jeune qui ne joue pas ne progresse pas | dev 2026-10-25 | |
| 7 | Mentors | `mentor` | Valeur fixe sur une zone ; 10 points = demi-étoile d'installations, max 30 par groupe | connaissance § 5 | |
| 8 | Satisfaction d'entraînement | plaintes `silver.dm_player_tips` | Catégories au-dessus de l'exigence : 0 rouge, 1 jaune, 2 bleu, 3 vert ; « Unhappy with training facilities and mentors » = installations trop basses | connaissance § 5 ; `resume.md` § Pièges | 9 plaintes (31/10) |
| 9 | Gardiens | — | Entraînement GK « trop facile » (2× plus rapide) : ne pas y mettre l'effort en priorité | connaissance § 5 | |
| 10 | Pré-saison | — | Repos de pré-saison : vérifier l'intensité après | connaissance § 13 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-003 | La forme ne monte qu'en jouant : relier intensité, minutes et TR | 2026-11-02 | à contrôler (C-008) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

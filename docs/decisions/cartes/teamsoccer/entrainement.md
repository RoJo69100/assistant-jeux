# Carte teamsoccer — entrainement (gymnase : compétence + intensité par joueur, vendredi ; deux clubs)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `entrainement.md`, skills `teamsoccer-entrainement`, `-joueurs` ; connaissance § 4). Règles : seul compte le réglage en place le vendredi soir ; saisie dans l'ordre de l'écran Entraînement (`pipelines/forme.py`).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:143 | compétence et intensité par joueur | var. 1-5 |
| :144 | suivre le progrès | var. 6 |
| :145 | comprendre le progrès | var. 3, 7 |
| :157 | niveau de l'entraîneur | var. 8 |

## Rendu (figé)
Un tableau par club, dans l'ordre de l'écran : `| Joueur | Âge | Zone | Compétence clé | Endurance / Vitesse | Forme | Compétence entraînée | Intensité | Gain mesuré (dernier vendredi) | Forme attendue vendredi | Garder / changer |`. Puis alertes : Endurance ≤ 35, Forme < 60, 28 ans et plus à haute intensité.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Réglage actuel | `silver.ts_training` (`training_type`, `intensity`, `last_trained_type`) | Seul compte le réglage au moment de la mise à jour du vendredi | connaissance 4.2 | |
| 2 | Compétence à travailler | `key_name`, `key_skill` de `gold.ts_effectif_bilan` | Compétence clé du poste (GB Gardien, DEF Défense, MIL Conduite, ATT Finition), Contrôle en 2e | `resume.md` § Juger un joueur | |
| 3 | Intensité et Forme | `forme` | Forme par vendredi : 100 % −10, 90 % −6, 80 % −4, 70 % −2, 60 % 0, 50 % +6, ≤ 40 % +10 ; 30 ans et plus −2 de plus à 80-100 % | connaissance 4.4 | |
| 4 | Physique | `silver.ts_players` (Endurance, Vitesse) | Ne monte plus seul ; ≤ 30 → seul l'entraînement d'Endurance possible ; Forme ≤ 30 plafonne l'intensité à 50 % | connaissance 4.8 | |
| 5 | Âge | `age` | Pleins gains 16-17 ans, moins jusqu'à 27, rien ou perte dès 28 : pas de haute intensité technique à 28 ans et plus | fiche entraînement § 4 | |
| 6 | Gains mesurés | `select team_id, name, age, prev_day, day, d_ovr, d_forme, d_value, training_type, intensity from gold.ts_player_progress order by team_id, d_ovr desc limit 40` | Mesurer avant d'en tirer une règle (barèmes BETA périmés, multiplicateur ×1,5 depuis le 2026-09-13) | connaissance 4.1, 4.7 | |
| 7 | Talent | `talent` | Performance / Magique : gain ×2 | connaissance 4.11 | |
| 8 | Entraîneur | skill entraînement § Entraîneurs ; `gold.ts_capacite_invest` | Niveau 2 = 1 000 000 $, puis 4, 10, 25 M ; un niveau à la fois ; impossible si solde négatif ; comparer à l'achat d'un joueur avec la même somme | connaissance 4.10 ; carte `finances` var. 6 | niveau 1 les deux clubs |
| 9 | Forme et match | `gold.ts_upcoming` | Le match ne fait pas baisser la Forme ; seule la séance du vendredi la change | connaissance 4.5 | |
| 10 | Avis des amis | connaissance § 4 | Forme au changement de saison : contradictoire (repart / reste) | connaissance 4.6 (en doute) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-009 | Forme uniforme à 84 (équipe première) : multiplicateur 0,952, titulaires Chomelix à 98 (0,994) : l'intensité règle la Forme du match suivant | 2026-11-02 | à surveiller |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

# Carte basketvibe — entrainement (choix du dimanche)

Sources lues : commit 58975fe (2026-10-31)

Écrite le 2026-10-31 (skill `basketvibe-entrainement`, vues gold d'entraînement). Échéance : réglages sauvegardés avant le dimanche 04:00 (Paris).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:41 | principale et secondaire après un export | var. 1-5 |
| :42 | suivre les progrès | var. 6 |
| :43 | comprendre le progrès, le talent | var. 7 |

## Rendu (figé)
`| Joueur | Poste | Âge | Principale | Secondaire | Pourquoi (poids au poste × mult. de niveau) | Gain attendu / sem. | Changement ? |` dans l'ordre de l'écran (PG→C, puis alphabétique). Puis les progrès de la semaine passée : `| Joueur | Compétence | Avant | Après | Gain | Attendu |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Options par joueur | `select name, age, position, skill, value, ps_weight, level_mult, is_primary, is_secondary from gold.bv_training_options order by name, ps_weight * level_mult desc` | Principale = compétence au plus grand poids à l'emplacement joué × multiplicateur de niveau (> 70 ralentit : 75 ×0,88, 80 ×0,75, 90 ×0,50) | [M§8.4] ; `gold.bv_ps_weight` [M§2.2] | |
| 2 | Âge | `gold.bv_player_outlook.age` | 30 ans : rien ; ≥ 31 : déclin, l'entraînement ne compense pas | [M§8.5] | |
| 3 | Blessés | `gold.bv_roster_now.injury_return_on` | Blessé = pas de progression cette semaine | [M§8] | |
| 4 | Emplacement réellement joué | `gold.bv_slot_fit` (rang 1-2) et composition en cours | L'emplacement compte, pas le libellé | [M§6.2] | |
| 5 | Base du gain | — | Principale +1,0, secondaire +0,5 × potentiel × niveau × âge | [M§8.2] | |
| 6 | Progrès mesurés | `select name, skill, v_before, v_after, gain, training_primary from gold.bv_training_gains_exact where week = (select max(week) from gold.bv_training_gains_exact)` ; `gold.bv_skill_progress_weekly` | Gain < attendu deux semaines = revoir l'estimation de potentiel | skill entraînement § Méthode | |
| 7 | Potentiel | `select name, potential_est, confidence from gold.bv_potential_estimate` ; potentiel révélé sur la fiche | Potentiel 7 et 8 identiques 4 semaines | [M§8.3] ; News 2026-10-20 | |
| 8 | Avis des amis | connaissance § Entraînement, § Entraînement / vieillissement | « secondaire = moitié » confirmé | connaissance | |

Limite connue : `silver.bv_training_changes` arrêtée au 18/10 ; l'export « Recent changes » après 04:00 le dimanche la complète.

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

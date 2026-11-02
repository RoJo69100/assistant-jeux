# Carte sixzeroleague — vente (mise en vente, libération)

Sources lues : commit 4bd592f (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, `effectif.md` § Surplus par rôle, skill `sixzeroleague-club` § Marché ; connaissance § 6). Règles : jamais de vente lancée sans accord ; une vente identifiée reste ouverte jusqu'à exécution ; annulation impossible.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:81 | ce joueur est-il à vendre | var. 1, 2 |
| :88 | faut-il vendre nos joueurs | var. 1-6 |

## Rendu (figé)
`| Priorité | Joueur | Rôle | Rang au rôle | Âge | Note | Notes aux autres rôles (après pénalité) | Matchs | Salaire | Mise en vente ou libération | Frais | Effectif après |`. Une ligne par joueur : pourquoi, ce qui prouvera l'erreur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats | `select poste, rang_poste, joueur, age, note, salaire, matchs_feuille, buts, tirs, pct_tir, statut, retraite, en_vente, effectif from gold.sz_effectif_bilan where statut = 'surplus' or retraite limit 20` | Surplus = ni titulaire ni doublure | fiche effectif | |
| 2 | Autres rôles | `silver.sz_players.role_overalls` | Avant de vendre un surplus, lire ses notes à tous les rôles après pénalité (−20 % att., −10 % déf.) | fiche effectif § Surplus par rôle | |
| 3 | Frais et limites | — | Mise en vente 500 € (non remboursés), libération 500 € ; pas pendant un match de ligue de l'équipe ; effectif 7 à 30 ; retraite annoncée = invendable | connaissance 6.10, 6.12, 6.13 | |
| 4 | Solde pour les frais | `silver.sz_finances.balance` | 500 € de frais impossibles si le solde ne les couvre pas | C-051 | |
| 5 | Âge | `age` | Déclin dès 28-30 : vendre avant la baisse, pas après | connaissance 5.9 | |
| 6 | Temps de jeu | `matchs_feuille` | Un joueur utilisé progresse plus vite ; un jeune jamais aligné perd ce gain | fiche effectif § Livrable 3 ; connaissance 5.3 | |
| 7 | Stats visibles | — | Les stats d'un joueur ne sont publiques que s'il est en vente | connaissance 6.7 | |
| 8 | Avis des amis | connaissance § 6 | — | connaissance | ventes G. Bertin et F. Denis (27/10, 90 €) |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

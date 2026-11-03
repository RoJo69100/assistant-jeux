# Carte hardwood — achat (sans objet : pas de transferts)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02. **Hardwood n'a ni marché ni transferts** : « hardwood doesn't have player transfers… players aren't really bought or sold in college basketball » (Steve, veille `v-recrutement.md` § 3). Toute arrivée de joueur passe par le recrutement : carte `academie`. Cette carte existe pour que `dossier.py hardwood achat` renvoie au bon endroit au lieu de compiler un dossier vide.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:10 | pas de transferts, points de recrutement | var. 1 |

## Rendu (figé)
Une ligne : « Pas de transferts dans Hardwood : voir le recrutement (carte `academie`) ». Aucun tableau d'achat.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Arrivée d'un joueur | carte `academie` | Recrutement (lycée, JuCo, international) avec contacts et offre de bourse ; walk-ons attribués au hasard | v-recrutement § 3 | |
| 2 | Coach | carte `finances` (coachs) | Le seul « achat » possible est un coach (marché des coachs) | `resume.md` § Écrans | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

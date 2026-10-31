# Carte <jeu> — <type>

Sources lues : commit 0000000 (AAAA-MM-JJ)

Carte = mémoire de **où** se trouve chaque information d'une décision et **comment** la juger. Écrite la première fois (dossier complet), puis seulement tenue à jour : au passage suivant, `pipelines/dossier.py` ne donne que la carte et le **nouveau** depuis le commit ci-dessus. Ne pas remplacer la ligne « Sources lues » à la main : `python pipelines/dossier.py <jeu> <type> --marquer`.

## Variables (une ligne par variable de `docs/decisions/variables.md` § <type>, plus celles apprises)
| # | Variable | Où la lire (requête exacte ou fichier § section) | Check (règle, seuil, sens) | Source du check (skill §, connaissance, Discord + date, L-nnn) | Dernière valeur (date) |
|---|---|---|---|---|---|
| 1 | Fatigue de chaque joueur | `select name, fatigue from gold.<vue> where ... limit 15` | <seuil chiffré tiré de la règle> | `.claude/skills/<jeu>-joueurs/SKILL.md` § Fatigue | <joueur : valeur> (AAAA-MM-JJ) |
| 2 | Avis des amis sur <réglage> | `outputs/<jeu>/veille/connaissance.md` § Tactique, lignes « <mot> » | <ce qu'ils disent, statut confirmé/en doute> | Discord <auteur> AAAA-MM-JJ | — |

## Checks appris des matchs
Une leçon `L-nnn` de `outputs/<jeu>/learnings.md` qui touche ce type devient une ligne ici (ou modifie un check ci-dessus). Un check contredit deux fois par les résultats est réécrit, pas répété.
| L-nnn | Check | Ajouté le | Résultat depuis (confirmé / contredit, matchs) |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi (source nouvelle) |
|---|---|---|---|

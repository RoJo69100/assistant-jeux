# Carte <jeu> — <type>

Sources lues : commit 0000000 (AAAA-MM-JJ)

Carte = mémoire de **où** se trouve chaque information d'une décision et **comment** la juger. Écrite la première fois (dossier complet), puis seulement tenue à jour : au passage suivant, `pipelines/dossier.py` ne donne que la carte et le **nouveau** depuis le commit ci-dessus. Ne pas remplacer la ligne « Sources lues » à la main : `python pipelines/dossier.py <jeu> <type> --marquer`.

## Lignes de la liste de l'utilisateur couvertes par cette carte
Chaque ligne de `docs/chose-a-faire*.txt` / `docs/chose-a-DM.txt` (+ bloc « Tous jeux ») qui touche ce type. Statut et preuve dans `docs/couverture/<jeu>.md`.
| Ligne (fichier:n°) | Texte court | Variable(s) ou section qui y répond |
|---|---|---|

## Rendu (figé, identique à chaque fois)
Le format exact rendu à l'utilisateur pour ce type : tableaux, colonnes, **ordre de l'écran ou de l'export du jeu**, pastilles 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI, aujourd'hui seulement, pas de « si », chaque joueur nommé, chaque réglage avec sa valeur. Copier ici le gabarit (en-têtes de tableaux) et citer la règle d'origine (CLAUDE.md, mémoire `feedback-…`, fiche du jeu). Un rendu qui s'écarte du gabarit est une récidive.

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

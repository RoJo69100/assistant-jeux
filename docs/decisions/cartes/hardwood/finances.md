# Carte hardwood — finances (pas d'argent : coachs head et assistants)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `hardwood-regles` § Coachs ; veille `v-calendrier-competitions.md` § 5, `v-joueurs-entrainement.md`, `v-recrutement.md` § 2). **Pas de finances, de budget ni d'installations** (« there is no budgeting in the game ») : le type `finances` couvre ici les coachs (personnel), comme `hardwood.yaml` (`finances` lit `personnel`, écrit `choix_coach`).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:15 | aucune notion de finance | var. 5 |
| :38 | head coach et assistants | var. 1, 2 |
| :39 | changer de coach : impacts et bénéfices | var. 3, 4 |

## Rendu (figé)
`| Rôle | Coach actuel | Compétences clés (recrutement, développement, match) | Meilleur candidat | Gain | Coût (pénalité de recrutement si head) | Fenêtre (avant la conférence / après la saison) | Décision |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Nos coachs | `select * from gold.hw_coach_board limit 20` ; `silver.hw_coaches` | Head + 3 assistants | skill règles | Schmidt assistant à la place de Brady (C-004) |
| 2 | Candidats | `silver.hw_coach_market` | Un recrutement de coach par jour réel | `resume.md` § Saison | exports Coach Search du 30/10 (616 et 3 525 candidats) |
| 3 | Fenêtre | `gold.hw_today` (`debut_conference`) | Assistants remplaçables seulement avant la conférence ou après la saison ; changements bloqués pendant le flip | `resume.md` § Saison ; v-recrutement § 1 | conférence commencée le 01/11 |
| 4 | Effet sur le recrutement | — | Recruteur à 19 économise des contacts ; changer de head coach = « pretty hefty penalty » sur les recrues suivies | v-recrutement § 2 | |
| 5 | Argent | — | Seul effet : un assistant payé 1 M$ ou plus (ou de 50 ans) devient head coach la saison suivante ; salaires automatiques | v-calendrier § 5 | |
| 6 | Avis des amis | v-joueurs, v-recrutement | — | veille | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

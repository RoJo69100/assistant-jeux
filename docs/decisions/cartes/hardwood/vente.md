# Carte hardwood — vente (pas de vente : départs de fin de saison, bourses libérées, redshirt)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `hardwood-regles` ; veille `v-recrutement.md` § 3-4). Pas de vente ni de coupe de joueurs : un joueur part en fin de cursus (4 ans, 5 avec redshirt). La décision qui ressemble à une vente = qui part, quelle bourse se libère, qui redshirter.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:23 | redshirter un jeune ? | var. 3 |
| :11 | nombre de joueurs à recruter | var. 1, 2 |

## Rendu (figé)
`| Joueur | Poste | Classe | Part en fin de saison | Bourse libérée | Remplaçant interne | Recrue visée (carte academie) |`, puis `| Jeune | Redshirt ? | Matchs joués (limite 5) | Pourquoi |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Départs | `select name, pos, class, si, pot, part_fin_saison from gold.hw_effectif where part_fin_saison and not walk_on` | Pas de départ anticipé ; on remplit les bourses libérées, 2 à 4 recrues par classe | v-recrutement § 3 | Corey (PG), Barbieri (PF), Harkins (SF), Adkins (SG) |
| 2 | Bourses | `select bourses_libres from gold.hw_today` | 13 bourses au plus ; walk-ons hors bourses, ne se coupent pas | v-recrutement § 3 | 3/4 libres (02/11) |
| 3 | Redshirt | `gold.hw_effectif` (`red_shirt`, `g`) | Redshirt = 5e année ; 5 matchs au plus pour le garder (exhibitions non comptées) ; malus de recrutement d'une 4-5 étoiles l'année suivante | v-calendrier § 3 ; v-recrutement § 2 | Wallace RS |
| 4 | Remplaçant interne | `gold.hw_roster_notes` (même groupe) | Note actuelle et avenir (potentiel) | fiche académie | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

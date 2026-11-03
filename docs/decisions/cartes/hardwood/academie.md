# Carte hardwood — academie (recrutement : 4 cibles + 2 remplaçants, points, offres de bourse)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02 (fiche `academie.md`, `resume.md`, skill `hardwood-recrutement` ; veille `v-recrutement.md` ; learnings). Format figé [U] contrôlé par `pipelines/forme.py` (hw-recrues) : 4 lignes exactement ; jamais de niveau High ; un grand ≥ 2,02 m ; recrues déjà engagées ou parties retirées.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:10 | fonctionnement du recrutement, points, classes (JC SO, JC FR…) | var. 1-4 |
| :11 | nombre de joueurs à recruter | var. 5 |
| :12 | recruter ce jeune ? | var. 6-9 |

## Rendu (figé)
`| Priorité | Poste (qui part) | Cible | Remplaçant 1 | Remplaçant 2 |` (4 lignes) ; chaque cellule : nom, classe/État, taille, note actuelle → plafond, équipes intéressées. Sous le tableau : points à dépenser aujourd'hui recrue par recrue (offre oui / non) et pages à exporter (`gold.hw_recrues_a_ouvrir`) si moins de 15 fiches.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Points | `select tour_recrutement, points_recrutement, bourses_libres from gold.hw_today` | +2 par tour, 53 tours, plafond 45 ; au-delà de 10 non dépensés au dernier jour : divisé par 2 ; dépenser tôt | v-recrutement § 1 | 0 au 02/11 |
| 2 | Engagement | `silver.hw_recruiting` | Il faut au moins 1 contact et une offre ; HS-SR dès le jour 5, JuCo jour 10, international jour 15 ; offre de bourse sans coût en points | v-recrutement § 1 | |
| 3 | Intérêt | `our_interest`, `teams_interested`, `teams_high` | Un niveau complet de retard = fortement défavorisé ; jamais de cible High [U] | v-recrutement § 1 ; fiche académie § 2 | |
| 4 | Modificateurs | — | In-State > niveau de ligue > région > durée du contact > prestige > coachs > temps de jeu ; changer de head coach = pénalité sur les recrues suivies | v-recrutement § 2 | |
| 5 | Besoin | `gold.hw_recruit_board.besoin` ; carte `vente` var. 1 | Remplacer par poste les SR qui partent, puis meilleure note ; 2 à 4 recrues par classe | `fait-2026-11-02.md` ; v-recrutement § 3 | Sturgeon engagé ; Simon, Woodling, Tolliver (C-002) |
| 6 | Fiches lues | `select verdict, rang, prospect, class, pos, height_m, si, pot, teams_interested from gold.hw_recrues_a_ouvrir limit 20` | 15 fiches au moins avant de juger | fiche académie § Données | |
| 7 | Note actuelle et plafond | `select verdict, name, poste, class, state, height_m, si, pot, note_now, note_plafond, cles, teams_interested, our_interest, we_offered, contacts from gold.hw_recrue_fiches order by note_plafond desc limit 20` | Juger sur compétences clés et phrases du scout, jamais le SI seul ; phrase rédhibitoire = écarter | fiche académie § Règles 1 | |
| 8 | Taille | `height_m` | Grand ≥ 2,02 m ; vérifier la taille, pas l'étiquette de poste (Simon 1,91 m étiqueté C) | [U] ; L-002 | |
| 9 | Déjà engagé | `silver.hw_recruiting` | Retirer une recrue engagée chez nous ou ailleurs ; « Eager to commit early » ≠ recrutée | [U] 2026-10-30 ; L-002 | |
| 10 | Avis des amis | v-recrutement § 2 | « Would prefer to play close to home » = moins cher pour la région ; « not much of a student » = JuCo 50/50 | v-recrutement § 2 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-002 | Lire les engagés et la taille avant de proposer une cible | 2026-11-02 | confirmé (02/11) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|

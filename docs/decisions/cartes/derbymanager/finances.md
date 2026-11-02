# Carte derbymanager — finances (argent par jour, plafond salarial, installations ; deux clubs)

Sources lues : commit a0787e7 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `derbymanager-club` ; connaissance § 9, § 10 ; learnings). Plus d'agent `finances` depuis le 2026-11-02. Tout l'argent est **par jour**. Un bloc par club.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:16 | solde actuel | var. 1 |
| :17 | dépenses | var. 2 |
| :18 | salaires | var. 3 |
| :19 | entrées d'argent | var. 2 |
| :20 | acheter ? rien ? | var. 4, 8 |
| :21 | quoi faire dans le futur | var. 5 |
| :66 | comprendre tous les bâtiments | var. 6 |
| :67 | augmenter ou non | var. 6, 7 |

## Rendu (figé)
Un bloc par club : 1) `| Argent | Flux / jour | Salaires engagés / plafond | Marge salariale / jour | Capacité d'investissement | Installations (niveau, prochain palier) | Attente du conseil (rang) |` ; 2) une décision unique (joueur, installation ou garder) avec le chiffre.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Argent | `select club, captured_at, money, flux_jour_estime, flux_jour_hors_stade, capacite_invest from gold.dm_finances_bilan` | Solde arrondi à l'écran dès 950 k | connaissance § 9 | QoS 20,4 M (30/10) |
| 2 | Flux | `broadcasting, sponsorship, merchandise, brand, subsidy, maintenance, youth_school, stadium_daily` ; `silver.dm_money_flow` | Sponsors le lundi selon les résultats ; stade selon l'affluence ; primes 200 k / 300 k / 500 k / 800 k par victoire (D4 → D1), moitié pour un nul | connaissance § 9 | +805 k/jour (30/10) |
| 3 | Plafond salarial | `salaries_committed, salary_cap, marge_salaire_jour` | Dépend de la réputation et du sponsoring ; faux jusqu'au lundi après un changement de saison | connaissance § 9, § 13 | marge 634 k/jour |
| 4 | Capacité | `capacite_invest` moins les dépenses décidées (`fait-`, C-006) | Achat > capacité = abandon | CLAUDE.md § Horizon | 20,4 − 8 = 12,4 M (31/10) |
| 5 | Attente du conseil | `expectation_rank, expectation_pct` | Récompenses de fin de saison seulement pour les 4 premiers (20 / 10 / 5 / 2,5 M) | connaissance § 9 | 6e attendu (QoS) |
| 6 | Installations | `facilities_level, upgrade_at, facilities_value, facilities_daily_change` ; `silver.dm_facilities` | +5 niveaux au-dessus de l'attente du conseil au plus ; −1 niveau à −5 M ; le conseil investit seul entre 20 et 50 M en caisse ; niveaux appropriés : D4 10-16, D3 16-22, D2 22-28, D1 28-34 | dev 2026-08-24 ; connaissance § 10 | niveau 16 (QoS) |
| 7 | Plaintes d'installations | `silver.dm_player_tips` | « Unhappy with training facilities » = installations trop basses pour l'effectif | `resume.md` § Pièges | 9 plaintes |
| 8 | Effectif d'abord | carte `achat` | « Always squad » avant installations quand les moyens manquent (avis) ; « tu peux tout faire avec ce que tu as » (dev) | connaissance § 9, § 10 | C-006 a choisi les installations |
| 9 | Argent thésaurisé | — | Seuil « tier × 5 M » ; argent moyen visé 6-10 M | connaissance § 9 | |
| 10 | Avis des amis | connaissance § 9, § 10 | < 25 M en D4 : viser D3 et la réputation | #france 2025-05-22 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
